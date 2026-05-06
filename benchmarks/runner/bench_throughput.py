"""Throughput vs context-length sweep.

For each target context length in {8K, 32K, 64K, 128K, 256K} we send a single
request with that prompt size and a fixed `max_tokens` decode budget, then
record:
    - prompt tokens (server-reported)
    - completion tokens
    - wall-clock elapsed
    - tokens/sec aggregate (completion / elapsed)
    - approximate time-to-first-token via a streaming version

Output: benchmarks/results/bench_throughput.json
"""
from __future__ import annotations
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    CallResult,
    get_tokenizer,
    http_post_completion,
    log,
    make_question_prompt,
    write_result,
)


DEFAULT_LENGTHS = [8192, 32768, 65536, 131072, 262144 - 4096]  # leave headroom for completion


def stream_first_token(base_url: str, model: str, messages, max_tokens: int = 64, timeout: float = 600.0):
    """Time-to-first-token using SSE stream. Returns (ttft_seconds, total_seconds, completion_tokens)."""
    import urllib.request
    import urllib.error
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.0,
        "stream": True,
    }
    data = json.dumps(payload).encode("utf-8")
    url = base_url.rstrip("/") + "/chat/completions"
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "Authorization": "Bearer EMPTY", "Accept": "text/event-stream"},
        method="POST",
    )
    t0 = time.perf_counter()
    ttft = None
    completion_tokens = 0
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            for raw in resp:
                line = raw.decode("utf-8", errors="replace").strip()
                if not line.startswith("data:"):
                    continue
                payload_s = line[5:].strip()
                if payload_s == "[DONE]":
                    break
                try:
                    chunk = json.loads(payload_s)
                except json.JSONDecodeError:
                    continue
                delta = (chunk.get("choices") or [{}])[0].get("delta") or {}
                content = delta.get("content")
                if content:
                    if ttft is None:
                        ttft = time.perf_counter() - t0
                    completion_tokens += 1  # rough — one delta ~1 token
        total = time.perf_counter() - t0
        return ttft, total, completion_tokens
    except Exception as e:
        return None, time.perf_counter() - t0, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-tokens", type=int, default=64)
    ap.add_argument("--lengths", default=",".join(str(x) for x in DEFAULT_LENGTHS),
                    help="Comma-separated target prompt token counts")
    ap.add_argument("--timeout", type=float, default=900.0)
    args = ap.parse_args()

    lengths = [int(x) for x in args.lengths.split(",") if x.strip()]
    enc = get_tokenizer()
    runs = []

    for ctx in lengths:
        log(f"context={ctx} — building prompt")
        messages = make_question_prompt(ctx, enc)

        # Non-streaming: total wall-clock + token counts
        log(f"context={ctx} — non-streaming call")
        r = http_post_completion(
            args.base_url, args.model, messages,
            max_tokens=args.max_tokens, temperature=0.0, timeout=args.timeout,
        )
        cr = CallResult.from_http(r)
        log(f"context={ctx} ok={cr.ok} elapsed={cr.elapsed:.2f}s prompt={cr.prompt_tokens} completion={cr.completion_tokens}")

        # Streaming: time-to-first-token
        log(f"context={ctx} — streaming call for TTFT")
        ttft, total, _ = stream_first_token(
            args.base_url, args.model, messages, max_tokens=args.max_tokens, timeout=args.timeout,
        )
        log(f"context={ctx} ttft={ttft} total_stream={total:.2f}")

        runs.append({
            "target_context_tokens": ctx,
            "result": cr.to_dict(),
            "ttft_seconds": ttft,
            "stream_total_seconds": total,
            "tokens_per_sec": (cr.completion_tokens / cr.elapsed) if cr.ok and cr.elapsed > 0 else None,
            "decode_throughput_tps": (cr.completion_tokens / max(0.001, cr.elapsed - (ttft or 0.0))) if cr.ok and ttft is not None else None,
        })

    payload = {
        "benchmark": "throughput_vs_context",
        "model": args.model,
        "base_url": args.base_url,
        "max_completion_tokens": args.max_tokens,
        "runs": runs,
    }
    write_result("bench_throughput.json", payload)


if __name__ == "__main__":
    main()
