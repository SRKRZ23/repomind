"""Cost-per-query analysis using already-collected throughput + concurrency data.

This benchmark consumes no GPU. It loads the JSON from bench_throughput and
bench_concurrency and computes:

    - cost per 1M completion tokens (USD), at AMD Cloud $1.99/hr per MI300X
    - cost per "average dev query" (assumed: 30K context in + 500 tokens out)
    - break-even vs Cursor Teams ($40/dev/month) at observed concurrency

Output: benchmarks/results/bench_cost.json
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import RESULTS_DIR, log, write_result


HOURLY_USD = 1.99           # AMD Developer Cloud, ATL1, MI300X x1, May 2026
SECONDS_PER_HOUR = 3600.0


def load(name: str) -> dict | None:
    p = RESULTS_DIR / name
    if not p.exists():
        log(f"missing: {p}")
        return None
    return json.loads(p.read_text())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--avg-context", type=int, default=30_000,
                    help="Average dev query context length in tokens")
    ap.add_argument("--avg-completion", type=int, default=500,
                    help="Average dev query completion length in tokens")
    ap.add_argument("--cursor-monthly-usd", type=float, default=40.0,
                    help="Cursor Teams seat price per dev per month")
    ap.add_argument("--hourly-usd", type=float, default=HOURLY_USD)
    args = ap.parse_args()

    tput = load("bench_throughput.json")
    conc = load("bench_concurrency.json")

    out = {
        "benchmark": "cost_economics",
        "hourly_usd_per_mi300x": args.hourly_usd,
        "assumed_average_query": {
            "context_tokens": args.avg_context,
            "completion_tokens": args.avg_completion,
        },
        "cursor_teams_monthly_usd_per_dev": args.cursor_monthly_usd,
        "cursor_teams_yearly_usd_per_dev": args.cursor_monthly_usd * 12,
        "throughput_curve": [],
        "concurrency_curve": [],
        "scenarios": [],
    }

    # Per-context cost-per-1M-tokens from single-user throughput
    if tput:
        for run in tput.get("runs", []):
            tps = run.get("tokens_per_sec")
            ctx = run.get("target_context_tokens")
            if not tps or tps <= 0:
                continue
            usd_per_1m_completion = (1_000_000 / tps) / SECONDS_PER_HOUR * args.hourly_usd
            out["throughput_curve"].append({
                "context_tokens": ctx,
                "single_user_tps": tps,
                "usd_per_1m_completion_tokens": usd_per_1m_completion,
            })

    # Per-cell aggregate cost from concurrency matrix
    if conc:
        for cell in conc.get("cells", []):
            agg = cell.get("tokens", {}).get("aggregate_completion_tps")
            if not agg or agg <= 0:
                continue
            usd_per_1m = (1_000_000 / agg) / SECONDS_PER_HOUR * args.hourly_usd
            out["concurrency_curve"].append({
                "context_tokens": cell["target_context_tokens"],
                "concurrency": cell["concurrency"],
                "successful": cell["successful"],
                "aggregate_tps": agg,
                "usd_per_1m_completion_tokens_aggregate": usd_per_1m,
            })

    # Break-even: how many devs per MI300X at the assumed average query rate?
    # If a single MI300X delivers `agg_tps` aggregate completion tokens per second,
    # and a dev fires Q queries / hour with `avg_completion` tokens each, then:
    #   max_devs = (agg_tps * 3600) / (Q * avg_completion)
    queries_per_hour_active = 6   # conservative: heavy dev fires 6 substantive queries / hour
    if out["concurrency_curve"]:
        # Use the highest aggregate throughput we measured (any context, any concurrency)
        best = max(out["concurrency_curve"], key=lambda r: r["aggregate_tps"])
        completion_per_hour = best["aggregate_tps"] * SECONDS_PER_HOUR
        completion_per_dev_per_hour = queries_per_hour_active * args.avg_completion
        max_devs = completion_per_hour / max(1, completion_per_dev_per_hour)
        cursor_yearly = max_devs * args.cursor_monthly_usd * 12
        rmd_yearly = args.hourly_usd * 24 * 365
        annual_savings = cursor_yearly - rmd_yearly
        out["scenarios"].append({
            "name": "best_observed_aggregate_throughput",
            "best_cell": best,
            "queries_per_active_dev_per_hour": queries_per_hour_active,
            "max_devs_per_mi300x": max_devs,
            "cursor_equivalent_yearly_usd_for_those_devs": cursor_yearly,
            "mi300x_cloud_yearly_usd": rmd_yearly,
            "annual_savings_usd": annual_savings,
            "break_even_owned_mi300x_months":
                (18000 / max(1, (cursor_yearly - 6000)) * 12) if cursor_yearly > 6000 else None,
        })

    write_result("bench_cost.json", out)


if __name__ == "__main__":
    main()
