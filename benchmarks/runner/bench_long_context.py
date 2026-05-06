"""Long-context coherence test — does 256K actually work, or just start up?

We embed a sentinel marker deep inside a ~200K-token code corpus, then ask the
model a question that can only be answered if it actually attended to that
section. This is a pass/fail signal that the 256K window is *usable*, not
just allocated.

The sentinel is a unique function name and an explicit fact. The grader checks
whether the response contains the expected substrings.

Output: benchmarks/results/bench_long_context.json
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    CallResult,
    CORPUS_SNIPPET,
    build_prompt,
    count_tokens,
    get_tokenizer,
    http_post_completion,
    log,
    write_result,
)


SENTINEL_FUNC_NAME = "calc_repomind_token_budget_v7"
SENTINEL_FACT = "the magic constant is 4242"


def make_long_context_prompt(target_tokens: int, sentinel_position: str, enc) -> list:
    """Embed a sentinel function definition at the requested position.

    sentinel_position: "early" | "middle" | "late"
    """
    sentinel_def = (
        f"\n\n# IMPORTANT REGION\n"
        f"def {SENTINEL_FUNC_NAME}(repo_size_tokens: int) -> int:\n"
        f"    \"\"\"Computes how many tokens REPOMIND should reserve for KV cache.\n"
        f"    Note: {SENTINEL_FACT}.\n"
        f"    Returns the magic constant baseline.\n"
        f"    \"\"\"\n"
        f"    return 4242 + repo_size_tokens // 8\n\n"
    )

    half = (target_tokens - 500) // 2
    front = build_prompt(half, enc) if sentinel_position != "early" else ""
    back = build_prompt(half, enc) if sentinel_position != "late" else ""

    if sentinel_position == "early":
        body = sentinel_def + back
    elif sentinel_position == "late":
        body = front + sentinel_def
    else:
        body = front + sentinel_def + back

    user = (
        "You will read a long Python codebase. Somewhere inside it, there is a function "
        f"with a unique name starting with 'calc_repomind_'.\n\n"
        "After reading, answer two questions in JSON format:\n"
        "  1. What is the EXACT name of that function? (key: \"function_name\")\n"
        "  2. What is the magic constant mentioned in its docstring? (key: \"magic_constant\")\n\n"
        f"```python\n{body}\n```\n\n"
        'Reply with one line of JSON only, e.g. {"function_name": "...", "magic_constant": 0}.'
    )
    return [
        {"role": "system", "content": "You are a precise code-reading assistant. Reply in valid JSON."},
        {"role": "user", "content": user},
    ]


def grade(content: str) -> dict:
    found_name = SENTINEL_FUNC_NAME in content
    found_fact = "4242" in content
    return {
        "found_function_name": found_name,
        "found_magic_constant": found_fact,
        "passed": found_name and found_fact,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--target-tokens", type=int, default=200_000,
                    help="Target prompt length in tokens (default ~200K, leaves headroom under 256K)")
    ap.add_argument("--max-tokens", type=int, default=128)
    ap.add_argument("--positions", default="early,middle,late")
    ap.add_argument("--timeout", type=float, default=900.0)
    args = ap.parse_args()

    enc = get_tokenizer()
    runs = []
    for pos in args.positions.split(","):
        pos = pos.strip()
        if not pos:
            continue
        log(f"position={pos} target={args.target_tokens} — building prompt")
        messages = make_long_context_prompt(args.target_tokens, pos, enc)
        prompt_chars = sum(len(m["content"]) for m in messages)
        log(f"position={pos} prompt_chars={prompt_chars} approx_tokens={count_tokens(messages[1]['content'], enc)}")

        r = http_post_completion(
            args.base_url, args.model, messages,
            max_tokens=args.max_tokens, temperature=0.0, timeout=args.timeout,
        )
        cr = CallResult.from_http(r)
        graded = grade(cr.content)
        runs.append({
            "position": pos,
            "target_tokens": args.target_tokens,
            "result": cr.to_dict(),
            "grading": graded,
        })
        log(f"position={pos} ok={cr.ok} elapsed={cr.elapsed:.2f}s passed={graded['passed']}")

    payload = {
        "benchmark": "long_context_needle",
        "model": args.model,
        "base_url": args.base_url,
        "sentinel_function_name": SENTINEL_FUNC_NAME,
        "sentinel_fact": SENTINEL_FACT,
        "runs": runs,
    }
    write_result("bench_long_context.json", payload)


if __name__ == "__main__":
    main()
