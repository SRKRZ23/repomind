"""Generate combined PHASE 1 + PHASE 2 plots.

Reads results from both:
  - benchmarks/2026-05-05-mi300x-stress-test/  (session 1, default Triton, 32K/128K/256K)
  - benchmarks/2026-05-05-mi300x-stress-test/extended/benchmarks/results/
      (session 2, default + AITER, 8K/16K/64K + 32K AITER A/B)

Writes combined plots into the extended/ folder:
  - plot_concurrency_combined.png   default Triton, 6 contexts, 24 cells
  - plot_throughput_combined.png    hot TTFT vs context, 6 points
  - plot_aiter_quality.png          AITER vs default output-quality regression
"""
from __future__ import annotations
import json
from pathlib import Path

import matplotlib.pyplot as plt  # type: ignore

ROOT = Path(__file__).resolve().parent.parent / "2026-05-05-mi300x-stress-test"
EXT = ROOT / "extended" / "benchmarks" / "results"
OUT = ROOT / "extended"
OUT.mkdir(parents=True, exist_ok=True)

AMD_RED = "#ED1C24"
WHITE = "#FFFFFF"
BG = "#0E0E10"
GRID = "#2A2A2E"
TEXT = "#EDEDED"
ORANGE = "#FFA500"
BLUE = "#42C0FB"
GREEN = "#4CAF50"


def setup_axes(ax):
    ax.set_facecolor(BG)
    for spine in ("bottom", "left"):
        ax.spines[spine].set_color(TEXT)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors=TEXT, which="both")
    ax.yaxis.label.set_color(TEXT)
    ax.xaxis.label.set_color(TEXT)
    ax.title.set_color(WHITE)
    ax.grid(True, color=GRID, linestyle="--", linewidth=0.5)


def load_session1_concurrency() -> dict:
    return json.loads((ROOT / "bench_concurrency.json").read_text())


def load_extended_concurrency() -> dict:
    return json.loads((EXT / "bench_concurrency_realistic_extended.json").read_text())


def load_aiter_concurrency() -> dict:
    return json.loads((EXT / "bench_concurrency_realistic_aiter.json").read_text())


def cells_by_ctx(d: dict) -> dict[int, list]:
    out: dict[int, list] = {}
    for c in d.get("cells", []):
        out.setdefault(c["target_context_tokens"], []).append(c)
    for v in out.values():
        v.sort(key=lambda r: r["concurrency"])
    return out


def is_broken(content: str) -> bool:
    s = content.strip() if content else ""
    return bool(s) and len(set(s)) <= 2


def plot_combined_concurrency() -> Path:
    s1 = cells_by_ctx(load_session1_concurrency())
    ext = cells_by_ctx(load_extended_concurrency())
    combined: dict[int, list] = {}
    combined.update(s1)
    combined.update(ext)
    contexts = sorted(combined.keys())

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 7.4), facecolor=BG)
    fig.suptitle(
        "REPOMIND on MI300X — concurrency stress (default Triton, 24 cells)",
        color=WHITE,
        fontsize=16,
        fontweight="bold",
    )
    setup_axes(ax1)
    setup_axes(ax2)

    palette = [AMD_RED, ORANGE, BLUE, GREEN, "#9C27B0", "#00BCD4"]
    for i, ctx in enumerate(contexts):
        rows = combined[ctx]
        xs = [r["concurrency"] for r in rows]
        ys_p95 = [r["latency"].get("p95") or 0 for r in rows]
        ys_agg = [r["tokens"].get("aggregate_completion_tps") or 0 for r in rows]
        c = palette[i % len(palette)]
        label = f"{ctx // 1024}K"
        ax1.plot(xs, ys_p95, color=c, marker="o", linewidth=2.4, markersize=8, label=label)
        ax2.plot(xs, ys_agg, color=c, marker="s", linewidth=2.4, markersize=8, label=label)

    ax1.set_xlabel("Concurrent users (N)")
    ax1.set_ylabel("p95 latency (sec)")
    ax1.set_title("p95 latency vs concurrency")
    ax1.set_yscale("log")
    leg = ax1.legend(facecolor=BG, edgecolor=GRID, title="Context")
    leg.get_title().set_color(WHITE)
    for t in leg.get_texts():
        t.set_color(WHITE)

    ax2.set_xlabel("Concurrent users (N)")
    ax2.set_ylabel("Aggregate tok/s (sum across all users)")
    ax2.set_title("Aggregate throughput vs concurrency")
    leg2 = ax2.legend(facecolor=BG, edgecolor=GRID, title="Context")
    leg2.get_title().set_color(WHITE)
    for t in leg2.get_texts():
        t.set_color(WHITE)

    out = OUT / "plot_concurrency_combined.png"
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(out, dpi=110, facecolor=BG)
    plt.close(fig)
    return out


def plot_combined_throughput() -> Path:
    """Hot TTFT and decode tps across 6 contexts (default Triton)."""
    s1 = json.loads((ROOT / "bench_throughput.json").read_text())
    ext = json.loads((EXT / "bench_throughput_hot_extended.json").read_text())

    points = []
    for r in s1.get("runs", []):
        ctx = r.get("target_context_tokens")
        ttft = r.get("ttft_seconds")
        if ttft is None or ctx is None:
            continue
        points.append({
            "ctx_k": ctx / 1024,
            "ttft": ttft,
            "decode": r.get("decode_throughput_tps") or 0,
            "label": "session 1",
        })
    for r in ext.get("runs", []):
        ctx = r.get("target_context_tokens")
        ttft = r.get("ttft_seconds")
        if ttft is None or ctx is None:
            continue
        points.append({
            "ctx_k": ctx / 1024,
            "ttft": ttft,
            "decode": r.get("decode_throughput_tps") or 0,
            "label": "extended (hot)",
        })

    by_ctx: dict[float, dict] = {}
    for p in points:
        prev = by_ctx.get(p["ctx_k"])
        if prev is None or p["label"] == "extended (hot)":
            by_ctx[p["ctx_k"]] = p
    points = sorted(by_ctx.values(), key=lambda p: p["ctx_k"])

    xs = [p["ctx_k"] for p in points]
    ys_ttft = [p["ttft"] for p in points]

    fig, ax1 = plt.subplots(1, 1, figsize=(11, 6.5), facecolor=BG)
    fig.suptitle(
        "REPOMIND on MI300X — TTFT vs context length (hot, no cold-start)",
        color=WHITE,
        fontsize=16,
        fontweight="bold",
    )
    setup_axes(ax1)
    ax1.plot(xs, ys_ttft, color=AMD_RED, marker="o", linewidth=2.5, markersize=10)
    ax1.set_xlabel("Context length (K tokens)")
    ax1.set_ylabel("TTFT (sec)")
    ax1.set_title("Time-to-first-token (single hot user, default Triton)")
    ax1.set_yscale("log")
    for x, y in zip(xs, ys_ttft):
        ax1.annotate(f"{y:.2f}s", (x, y), textcoords="offset points", xytext=(8, 8), color=WHITE)

    out = OUT / "plot_throughput_combined.png"
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(out, dpi=110, facecolor=BG)
    plt.close(fig)
    return out


def plot_aiter_quality() -> Path:
    """Side-by-side: throughput gain vs output-quality loss (AITER)."""
    default = cells_by_ctx(load_extended_concurrency())
    aiter = cells_by_ctx(load_aiter_concurrency())

    rows = []
    for ctx in sorted(default.keys()):
        for d_cell in default[ctx]:
            n = d_cell["concurrency"]
            a_cell = next((c for c in aiter.get(ctx, []) if c["concurrency"] == n), None)
            if a_cell is None:
                continue
            d_tps = d_cell["tokens"]["aggregate_completion_tps"]
            a_tps = a_cell["tokens"]["aggregate_completion_tps"]
            a_broken = sum(1 for r in a_cell["per_request"] if is_broken(r["content"]))
            a_total = len(a_cell["per_request"])
            rows.append({
                "label": f"{ctx//1024}K×{n}",
                "ctx": ctx,
                "n": n,
                "default_tps": d_tps,
                "aiter_tps": a_tps,
                "broken_pct": 100.0 * a_broken / max(a_total, 1),
            })

    rows.sort(key=lambda r: (r["ctx"], r["n"]))
    labels = [r["label"] for r in rows]
    default_tps = [r["default_tps"] for r in rows]
    aiter_tps = [r["aiter_tps"] for r in rows]
    broken_pct = [r["broken_pct"] for r in rows]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8.5), facecolor=BG, sharex=True)
    fig.suptitle(
        "REPOMIND tuning attempt — AITER backend regression on FP8 KV cache",
        color=WHITE,
        fontsize=16,
        fontweight="bold",
    )
    setup_axes(ax1)
    setup_axes(ax2)

    x = list(range(len(labels)))
    width = 0.4
    ax1.bar([i - width / 2 for i in x], default_tps, width, label="default Triton", color=AMD_RED)
    ax1.bar([i + width / 2 for i in x], aiter_tps, width, label="AITER", color=ORANGE)
    ax1.set_ylabel("Aggregate tok/s")
    ax1.set_title("Throughput: AITER 2-4× higher")
    leg = ax1.legend(facecolor=BG, edgecolor=GRID)
    for t in leg.get_texts():
        t.set_color(WHITE)

    bars = ax2.bar(x, broken_pct, color=[AMD_RED if v >= 50 else ORANGE if v > 0 else GREEN for v in broken_pct])
    ax2.set_ylabel("% broken output (AITER)")
    ax2.set_title("Output quality regression: 137/144 (95%) AITER cells produce repeating-punctuation gibberish")
    ax2.set_ylim(0, 110)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=30, ha="right", color=TEXT)
    for b, v in zip(bars, broken_pct):
        ax2.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.0f}%", ha="center", color=WHITE, fontsize=9)

    out = OUT / "plot_aiter_quality.png"
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(out, dpi=110, facecolor=BG)
    plt.close(fig)
    return out


if __name__ == "__main__":
    print("[plot] combined concurrency →", plot_combined_concurrency())
    print("[plot] combined throughput →", plot_combined_throughput())
    print("[plot] AITER quality →", plot_aiter_quality())
