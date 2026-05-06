"""Concurrency stress test — verifies the 31.31x estimate from vLLM.

Sends N parallel requests to the same vLLM server with a fixed context length,
all firing within ~50ms of each other. Records per-request latency, success,
prompt/completion tokens, and aggregate throughput.

Default matrix:
    contexts: [32768, 131072, 262144 - 4096]
    concurrency: [1, 4, 8, 16, 24, 31]

Each (context, N) cell costs ~1 sustained call worth of GPU time, so the full
matrix at 256K is what really stresses the box.

Output: benchmarks/results/bench_concurrency.json
"""
from __future__ import annotations
import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
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


DEFAULT_CONTEXTS = [32768, 131072, 262144 - 4096]
DEFAULT_CONCURRENCY = [1, 4, 8, 16, 24, 31]


def percentile(values, q):
    if not values:
        return None
    s = sorted(values)
    k = max(0, min(len(s) - 1, int(round((q / 100.0) * (len(s) - 1)))))
    return s[k]


def run_cell(base_url: str, model: str, ctx_tokens: int, n_concurrent: int,
             max_tokens: int, timeout: float, enc) -> dict:
    log(f"cell ctx={ctx_tokens} N={n_concurrent} — building prompt")
    messages = make_question_prompt(ctx_tokens, enc)

    def one_call(idx: int):
        # Stagger sub-50ms to simulate near-simultaneous arrival without a true thundering herd.
        time.sleep(idx * 0.02)
        return CallResult.from_http(
            http_post_completion(base_url, model, messages,
                                 max_tokens=max_tokens, temperature=0.0, timeout=timeout)
        )

    t_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=n_concurrent) as ex:
        futures = [ex.submit(one_call, i) for i in range(n_concurrent)]
        results = [f.result() for f in as_completed(futures)]
    wall_clock = time.perf_counter() - t_start

    ok = [r for r in results if r.ok]
    failed = [r for r in results if not r.ok]
    latencies = [r.elapsed for r in ok]
    completion_tokens = sum(r.completion_tokens for r in ok)
    prompt_tokens = sum(r.prompt_tokens for r in ok)

    cell = {
        "target_context_tokens": ctx_tokens,
        "concurrency": n_concurrent,
        "wall_clock_seconds": wall_clock,
        "successful": len(ok),
        "failed": len(failed),
        "errors": [r.error for r in failed][:5],
        "latency": {
            "min": min(latencies) if latencies else None,
            "p50": percentile(latencies, 50),
            "p95": percentile(latencies, 95),
            "max": max(latencies) if latencies else None,
        },
        "tokens": {
            "prompt_total": prompt_tokens,
            "completion_total": completion_tokens,
            "aggregate_completion_tps": (completion_tokens / wall_clock) if wall_clock > 0 else None,
        },
        "per_request": [r.to_dict() for r in results],
    }
    log(f"cell ctx={ctx_tokens} N={n_concurrent} ok={len(ok)}/{n_concurrent} "
        f"wall={wall_clock:.2f}s p95={cell['latency']['p95']} agg_tps={cell['tokens']['aggregate_completion_tps']}")
    return cell


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-tokens", type=int, default=64)
    ap.add_argument("--contexts", default=",".join(str(x) for x in DEFAULT_CONTEXTS))
    ap.add_argument("--concurrency", default=",".join(str(x) for x in DEFAULT_CONCURRENCY))
    ap.add_argument("--timeout", type=float, default=900.0)
    args = ap.parse_args()

    contexts = [int(x) for x in args.contexts.split(",") if x.strip()]
    concurrency = [int(x) for x in args.concurrency.split(",") if x.strip()]

    enc = get_tokenizer()
    cells = []
    for ctx in contexts:
        for n in concurrency:
            cell = run_cell(args.base_url, args.model, ctx, n,
                            args.max_tokens, args.timeout, enc)
            cells.append(cell)

    payload = {
        "benchmark": "concurrency_matrix",
        "model": args.model,
        "base_url": args.base_url,
        "max_completion_tokens": args.max_tokens,
        "cells": cells,
    }
    write_result("bench_concurrency.json", payload)


if __name__ == "__main__":
    main()
