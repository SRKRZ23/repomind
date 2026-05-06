"""Generate slide-ready PNGs from the JSON results.

Reads bench_throughput.json, bench_concurrency.json, bench_cost.json from
benchmarks/results/ and writes 1280x720 dark-theme PNGs back into the same
folder.

Runs locally (no GPU). Requires matplotlib only.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import RESULTS_DIR, log


AMD_RED = "#ED1C24"
WHITE = "#FFFFFF"
BG = "#0E0E10"
GRID = "#2A2A2E"
TEXT = "#EDEDED"


def setup_axes(ax):
    ax.set_facecolor(BG)
    ax.spines["bottom"].set_color(TEXT)
    ax.spines["left"].set_color(TEXT)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors=TEXT, which="both")
    ax.yaxis.label.set_color(TEXT)
    ax.xaxis.label.set_color(TEXT)
    ax.title.set_color(WHITE)
    ax.grid(True, color=GRID, linestyle="--", linewidth=0.5)


def plot_throughput(out_dir: Path) -> Path | None:
    p = out_dir / "bench_throughput.json"
    if not p.exists():
        log(f"skip throughput plot — missing {p}")
        return None
    import matplotlib.pyplot as plt  # type: ignore
    data = json.loads(p.read_text())
    runs = [r for r in data.get("runs", []) if r.get("tokens_per_sec")]
    runs.sort(key=lambda r: r["target_context_tokens"])
    xs = [r["target_context_tokens"] / 1024 for r in runs]
    ys = [r["tokens_per_sec"] for r in runs]
    ttfts = [r.get("ttft_seconds") for r in runs]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 7.2), facecolor=BG)
    fig.suptitle("REPOMIND on MI300X — throughput vs context length",
                 color=WHITE, fontsize=16, fontweight="bold")
    setup_axes(ax1); setup_axes(ax2)

    ax1.plot(xs, ys, color=AMD_RED, marker="o", linewidth=2.5, markersize=10)
    ax1.set_xlabel("Context length (K tokens)")
    ax1.set_ylabel("Completion tokens / sec")
    ax1.set_title("Single-user throughput")
    for x, y in zip(xs, ys):
        ax1.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(8, 8), color=WHITE)

    ttft_pairs = [(x, t) for x, t in zip(xs, ttfts) if t is not None]
    if ttft_pairs:
        xs2 = [p[0] for p in ttft_pairs]
        ys2 = [p[1] for p in ttft_pairs]
        ax2.plot(xs2, ys2, color=WHITE, marker="s", linewidth=2.5, markersize=9)
        ax2.set_xlabel("Context length (K tokens)")
        ax2.set_ylabel("Time to first token (sec)")
        ax2.set_title("Latency to first token")
        for x, y in zip(xs2, ys2):
            ax2.annotate(f"{y:.2f}s", (x, y), textcoords="offset points", xytext=(8, 8), color=WHITE)

    out = out_dir / "plot_throughput.png"
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(out, dpi=100, facecolor=BG)
    plt.close(fig)
    log(f"wrote {out}")
    return out


def plot_concurrency(out_dir: Path) -> Path | None:
    p = out_dir / "bench_concurrency.json"
    if not p.exists():
        log(f"skip concurrency plot — missing {p}")
        return None
    import matplotlib.pyplot as plt  # type: ignore
    data = json.loads(p.read_text())
    cells = data.get("cells", [])
    if not cells:
        return None

    contexts = sorted({c["target_context_tokens"] for c in cells})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 7.2), facecolor=BG)
    fig.suptitle("REPOMIND on MI300X — concurrency stress",
                 color=WHITE, fontsize=16, fontweight="bold")
    setup_axes(ax1); setup_axes(ax2)

    palette = [AMD_RED, "#FFA500", "#42C0FB"]
    for i, ctx in enumerate(contexts):
        rows = sorted([c for c in cells if c["target_context_tokens"] == ctx],
                      key=lambda r: r["concurrency"])
        xs = [r["concurrency"] for r in rows]
        ys_p95 = [(r["latency"].get("p95") or 0) for r in rows]
        ys_agg = [(r["tokens"].get("aggregate_completion_tps") or 0) for r in rows]
        c = palette[i % len(palette)]
        label = f"{ctx//1024}K context"
        ax1.plot(xs, ys_p95, color=c, marker="o", linewidth=2.5, markersize=9, label=label)
        ax2.plot(xs, ys_agg, color=c, marker="s", linewidth=2.5, markersize=9, label=label)

    ax1.set_xlabel("Concurrent users"); ax1.set_ylabel("p95 latency (sec)")
    ax1.set_title("p95 latency vs concurrency")
    leg = ax1.legend(facecolor=BG, edgecolor=GRID); [t.set_color(WHITE) for t in leg.get_texts()]

    ax2.set_xlabel("Concurrent users"); ax2.set_ylabel("Aggregate tokens / sec (sum)")
    ax2.set_title("Aggregate throughput vs concurrency")
    leg2 = ax2.legend(facecolor=BG, edgecolor=GRID); [t.set_color(WHITE) for t in leg2.get_texts()]

    out = out_dir / "plot_concurrency.png"
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(out, dpi=100, facecolor=BG)
    plt.close(fig)
    log(f"wrote {out}")
    return out


def plot_cost(out_dir: Path) -> Path | None:
    p = out_dir / "bench_cost.json"
    if not p.exists():
        log(f"skip cost plot — missing {p}")
        return None
    import matplotlib.pyplot as plt  # type: ignore
    data = json.loads(p.read_text())
    scen = (data.get("scenarios") or [{}])[0]
    if not scen:
        return None

    fig, ax = plt.subplots(1, 1, figsize=(12.8, 7.2), facecolor=BG)
    fig.suptitle("REPOMIND vs Cursor Teams — annual cost",
                 color=WHITE, fontsize=16, fontweight="bold")
    setup_axes(ax)

    cursor = scen.get("cursor_equivalent_yearly_usd_for_those_devs", 0)
    rmd = scen.get("mi300x_cloud_yearly_usd", 0)
    saved = scen.get("annual_savings_usd", cursor - rmd)
    devs = scen.get("max_devs_per_mi300x", 0)

    bars = ax.bar(
        ["Cursor Teams", "REPOMIND on MI300X (cloud)"],
        [cursor, rmd],
        color=[WHITE, AMD_RED], edgecolor=GRID, linewidth=1.5,
    )
    for b, v in zip(bars, [cursor, rmd]):
        ax.text(b.get_x() + b.get_width() / 2, v, f"${v:,.0f}",
                ha="center", va="bottom", color=WHITE, fontsize=14, fontweight="bold")
    ax.set_ylabel("Annual cost (USD)")
    ax.set_title(f"For {devs:.0f} devs served by 1 MI300X — saving ${saved:,.0f} / year")

    out = out_dir / "plot_cost.png"
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(out, dpi=100, facecolor=BG)
    plt.close(fig)
    log(f"wrote {out}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(RESULTS_DIR))
    args = ap.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    plot_throughput(out_dir)
    plot_concurrency(out_dir)
    plot_cost(out_dir)


if __name__ == "__main__":
    main()
