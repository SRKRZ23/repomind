# Benchmarks plan

The headline pitch is one table. To deliver it credibly we need three runs:

## R1 — H100 reference (off-machine, cite vendor specs)

We don't burn AMD credits on H100 runs. Cite published vLLM benchmarks for
Qwen3-Coder-Next-FP8 KV cache footprint:

- KV cache per token at FP8 ≈ 2 × 2 bytes × num_kv_heads × head_dim × num_layers
  → for Qwen3-Coder-Next-FP8: ~150 KB / token across all layers
- 256K tokens × 150 KB ≈ 38 GB just for the KV cache
- Plus model weights (~80B params, FP8 ≈ 80 GB) → 118 GB minimum
- H100 80GB physically can't hold both.

Source: AMD's own [Day-0 Qwen3-Coder-Next post](https://www.amd.com/en/developer/resources/technical-articles/2026/day-0-support-for-qwen3-coder-next-on-amd-instinct-gpus.html).

## R2 — MI300X smoke test (when credits arrive)

```
sequence_length    tokens/sec    p95_latency    KV cache used
   16,384             ~120           220 ms        ~2 GB
   65,536              ~80           420 ms        ~10 GB
  131,072              ~55           780 ms        ~20 GB
  262,144              ~30          1700 ms        ~38 GB
```

(Numbers are the *targets* before measurement. Will be replaced with real measurements.)

## R3 — End-to-end task

Pick three repos of escalating size and difficulty:

| Tier | Repo | Tokens (approx) | Sample question |
| --- | --- | --- | --- |
| Small | this repo (REPOMIND) | ~10K | "What does the chunker prioritize?" |
| Mid | `pytorch/vision` (subset) | ~100K | "Show all transforms that touch alpha channel." |
| Large | `torvalds/linux` mm/ subtree | ~256K (truncated to fit) | "Trace one slab allocation through the call graph." |

For each, capture:
- Total tool calls
- Wall-clock latency
- Whether the answer cites correct file:line ranges
- (Subjective) quality vs Cursor / Claude Code on the same question

## What goes in the demo video

Three side-by-side numbers in a single frame:

```
                  H100 80GB        MI300X 192GB
  64K context:    ✓ works          ✓ works
 128K context:    ✗ OOM            ✓ works
 256K context:    ✗ OOM            ✓ ~30 tok/s
```

Then a live ingest of the Linux kernel + a multi-step reasoning question.

## Plotting

Plotting will use plain matplotlib so it runs without a GPU during dev.
A single 1280×720 dark-theme PNG per benchmark run, saved into
`benchmarks/results/`.
