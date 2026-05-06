"""End-to-end repo ingestion + question answering with timing.

Runs against three repos of escalating size:
    - tier 1 small  : REPOMIND itself (~10K tokens)
    - tier 2 medium : a Flask subset or similar  (~80K tokens)
    - tier 3 large  : a torvalds/linux mm/ subtree  (~200K tokens, truncated to fit)

For each repo, we:
    1. Ingest (clone + chunk + token-budget) — measure wall-clock
    2. Build a single chat-completion prompt that includes the top-N chunks
    3. Ask 3 questions of escalating difficulty
    4. Measure: total wall clock, prompt tokens, completion tokens, tok/s

This is the "real demo" benchmark. Output: bench_e2e.json + per-question
plain-text dumps in benchmarks/results/e2e/.
"""
from __future__ import annotations
import argparse
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    CallResult,
    count_tokens,
    get_tokenizer,
    http_post_completion,
    log,
    write_result,
    RESULTS_DIR,
)


# Three tiers (the runner script can override via env if a clone fails).
TIERS = [
    {
        "label": "small_repomind",
        "kind": "path",
        "path": str(REPO_ROOT),
        "questions": [
            "What does the chunker module prioritize when truncating to a token budget?",
            "Which agent module implements the SC-TIR loop, and how many max steps by default?",
            "Name three tools in the agent's tool layer.",
        ],
    },
    {
        "label": "medium_flask",
        "kind": "url",
        "url": "https://github.com/pallets/flask",
        "questions": [
            "Where is the WSGI request entry point in this codebase?",
            "How does Flask handle URL routing — name the central object and its method.",
            "What does the `Flask.run()` method delegate to?",
        ],
    },
    {
        "label": "large_pytorch_vision",
        "kind": "url",
        "url": "https://github.com/pytorch/vision",
        "questions": [
            "Name three transforms that touch the alpha channel.",
            "Which file defines the ResNet bottleneck block?",
            "Where does video decoding live in this repo?",
        ],
    },
]


def build_prompt_from_repo(repo_summary: dict, max_tokens_total: int, enc) -> str:
    """Concatenate as many chunks as fit, sorted by priority. Falls back to char-trim."""
    chunks = repo_summary.get("chunks", [])
    # priority 0 = README/docs (highest), 1 = top-level symbols, etc. Lower number = higher priority.
    chunks_sorted = sorted(chunks, key=lambda c: c.get("priority", 99))
    out_parts = []
    used = 0
    for c in chunks_sorted:
        body = f"\n# FILE: {c.get('path', '?')}\n```{c.get('language', '')}\n{c.get('text', '')}\n```\n"
        body_tokens = count_tokens(body, enc)
        if used + body_tokens > max_tokens_total:
            continue
        out_parts.append(body)
        used += body_tokens
    return "".join(out_parts), used


def run_question(base_url, model, repo_block, question, max_tokens, timeout):
    messages = [
        {"role": "system", "content": "You are a code-reading assistant. Cite file paths in your answer when possible. Be concise."},
        {"role": "user", "content": f"Below is the contents of a repository:\n\n{repo_block}\n\nQuestion: {question}\nAnswer in 3 sentences max."},
    ]
    r = http_post_completion(base_url, model, messages, max_tokens=max_tokens, temperature=0.2, timeout=timeout)
    return CallResult.from_http(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("--target-context", type=int, default=180_000,
                    help="Tokens to fit into the prompt when chunking large repos")
    ap.add_argument("--cache-dir", default=str(REPO_ROOT / ".repomind_cache"))
    ap.add_argument("--tiers", default="small_repomind,medium_flask,large_pytorch_vision")
    ap.add_argument("--timeout", type=float, default=1200.0)
    args = ap.parse_args()

    # Lazy imports so we don't fail on droplets without git or tree-sitter
    from ingestion.chunker import ingest_to_json
    selected = set(args.tiers.split(","))
    enc = get_tokenizer()

    e2e_dir = RESULTS_DIR / "e2e"
    e2e_dir.mkdir(parents=True, exist_ok=True)

    tiers_out = []
    for tier in TIERS:
        if tier["label"] not in selected:
            continue
        log(f"=== tier {tier['label']} ===")
        cache_dir = Path(args.cache_dir) / "repos"

        json_out = e2e_dir / f"{tier['label']}.json"
        if tier["kind"] == "path":
            repo_root = Path(tier["path"]).resolve()
            t0 = time.perf_counter()
            ingest_to_json(
                repo_root, str(json_out),
                repo_label=tier["label"], max_tokens_per_chunk=2048,
            )
            ingest_seconds = time.perf_counter() - t0
        else:
            from ingestion.cloner import clone
            t_clone_0 = time.perf_counter()
            res = clone(tier["url"], cache_dir=str(cache_dir), depth=1)
            clone_seconds = time.perf_counter() - t_clone_0
            t0 = time.perf_counter()
            ingest_to_json(
                res.local_path, str(json_out),
                repo_label=tier["label"], max_tokens_per_chunk=2048,
            )
            ingest_seconds = time.perf_counter() - t0 + clone_seconds

        # ingest_to_json strips chunks from its return value, but writes the full
        # summary (including chunks) to disk. Read the disk version.
        full_summary = json.loads(Path(json_out).read_text())
        repo_block, used_tokens = build_prompt_from_repo(full_summary, args.target_context, enc)
        log(f"tier={tier['label']} ingest={ingest_seconds:.2f}s prompt_tokens~{used_tokens}")

        # Save the prompt block so we can reuse / inspect it
        (e2e_dir / f"{tier['label']}_prompt.txt").write_text(repo_block)

        questions_out = []
        for q in tier["questions"]:
            log(f"  question: {q[:80]}")
            cr = run_question(args.base_url, args.model, repo_block, q,
                              args.max_tokens, args.timeout)
            questions_out.append({
                "question": q,
                "result": cr.to_dict(),
                "tokens_per_sec": (cr.completion_tokens / cr.elapsed) if cr.ok and cr.elapsed > 0 else None,
            })
            log(f"    ok={cr.ok} elapsed={cr.elapsed:.2f}s prompt={cr.prompt_tokens} completion={cr.completion_tokens}")
            # Save full content per question
            (e2e_dir / f"{tier['label']}_{cr.prompt_tokens or 'na'}_q{tier['questions'].index(q)+1}.txt").write_text(
                f"Q: {q}\n\nA:\n{cr.content}\n"
            )

        tiers_out.append({
            "label": tier["label"],
            "ingest_seconds": ingest_seconds,
            "prompt_tokens_used": used_tokens,
            "chunks_total": full_summary.get("n_chunks", 0),
            "n_files": full_summary.get("n_files", 0),
            "total_repo_tokens": full_summary.get("total_tokens", 0),
            "questions": questions_out,
        })

    payload = {
        "benchmark": "end_to_end_repos",
        "model": args.model,
        "base_url": args.base_url,
        "max_completion_tokens": args.max_tokens,
        "target_context_tokens": args.target_context,
        "tiers": tiers_out,
    }
    write_result("bench_e2e.json", payload)


if __name__ == "__main__":
    main()
