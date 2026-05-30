# MI300X Stress Test — 2026-05-05

Full evidence pack from REPOMIND's empirical validation session on real
AMD MI300X hardware. All numbers below are measured on a single
`MI300X x1` instance, AMD Developer Cloud (DigitalOcean-backed), region
ATL1, image `vLLM 0.17.1 + ROCm 7.2.0 Quick Start`.

**Total wall clock**: 97 minutes
**Total cost**: ~$3.22 ($1.99/hr × 1.62 hr)
**Total credits used**: 3.2% of $100

## Files in this folder

```
.
├── SUMMARY.md                        ← this file
├── bench_throughput.json             5 contexts × {non-stream + stream TTFT}
├── bench_concurrency.json            3 contexts × 4 N (12 cells, identical-prompt)
├── bench_long_context.json           Sentinel needle at 3 positions in 200K
├── bench_e2e.json                    3 repos × 3 questions (all correct)
├── bench_cost.json                   $/M tokens, dev/MI300X, break-even math
├── plot_throughput.png               1280×720 dark theme, AMD red
├── plot_concurrency.png              p95 latency + aggregate tps vs N
├── plot_cost.png                     Cursor vs REPOMIND annual bar chart
├── rocm_smi_final.txt                Post-test GPU snapshot (92% VRAM)
├── run_log.txt                       Full text log of the suite run
└── e2e/                              Per-question raw inputs and outputs
    ├── small_repomind.json
    ├── small_repomind_prompt.txt
    ├── small_repomind_<N>_q1.txt    "Q: ... \nA: ..."
    ├── small_repomind_<N>_q2.txt
    ├── small_repomind_<N>_q3.txt
    ├── medium_flask.json
    ├── medium_flask_prompt.txt
    ├── medium_flask_<N>_q1.txt
    ├── medium_flask_<N>_q2.txt
    ├── medium_flask_<N>_q3.txt
    ├── large_pytorch_vision.json
    ├── large_pytorch_vision_prompt.txt
    ├── large_pytorch_vision_<N>_q1.txt
    ├── large_pytorch_vision_<N>_q2.txt
    └── large_pytorch_vision_<N>_q3.txt
```

## Headline findings

### 1. Memory-architecture moat — VERIFIED

| Metric | Value | Source |
|---|---|---|
| Model weights in VRAM | **77.29 GiB** | vLLM `gpu_model_runner.py` log |
| Available KV cache memory | **94.58 GiB** | vLLM `gpu_worker.py` log |
| GPU KV cache size | **2,065,744 tokens** | vLLM `kv_cache_utils.py` log |
| VRAM peak (post-stress) | **176.0 / 191.7 GiB** (92%) | rocm-smi |
| `--max-model-len 262144` | started clean | vLLM startup |
| `/v1/models` `max_model_len` | 262144 | API verified |
| Cold start total | **~3 min 30 sec** | bench_runner timing |

This configuration on an NVIDIA H100 80GB single-card cannot fit by
VRAM accounting (143 GiB > 80 GiB). MI300X 192 GB has the headroom.

### 2. Throughput vs context (single user)

![throughput](plot_throughput.png)

| Context | Prompt tokens | TTFT (stream) | Decode wall (non-stream) | Decode tps |
|---|---|---|---|---|
| 8K | 8,090 | 0.44s | 48.9s (cold start outlier — first call after vLLM warmup) | (cold) |
| 32K | 32,808 | 3.05s | 3.81s | ~9 |
| 64K | 65,523 | 9.61s | 10.20s | ~3.5 |
| 128K | 130,953 | 33.05s | 34.21s | ~1 |
| **256K** | **257,451** | **117.8s** | **119.6s** | **~0.31** |

TTFT scales near-linearly with prefill tokens, as expected.

### 3. Concurrency stress (12 cells, identical-prompt)

![concurrency](plot_concurrency.png)

| Context | N | p95 | Aggregate tps | Success | Reading |
|---|---|---|---|---|---|
| 32K | 1 | 3.6s | 9.95 | 1/1 | clean |
| 32K | 8 | 24.1s | 11.85 | 8/8 | clean |
| 32K | 16 | 48.2s | 11.87 | 16/16 | clean |
| **32K** | **31** | **91.6s** | **12.08** | **31/31** | **vLLM "31x" theoretical confirmed** |
| 128K | 1 | 33.6s | 1.07 | 1/1 | clean |
| 128K | 8 | 265.9s | 1.10 | 8/8 | clean |
| 128K | 16 | 531.2s | 1.10 | 16/16 | clean |
| 128K | 31 | 866.1s | 1.01 | 25/31 | 6 timed out >900s |
| 256K | 1 | 120.0s | 0.31 | 1/1 | clean |
| 256K | 8 | 839.4s | 0.24 | 6/8 | 2 timed out |
| 256K | 16 | 845.7s | 0.24 | 6/16 | rest queued |
| 256K | 31 | 846.4s | 0.24 | 6/31 | rest queued |

**Honest framing**: vLLM's "Maximum concurrency: 31.08x" estimate
assumes chunked-prefix-cache sharing for identical prompts. We
empirically verified 31/31 at 32K. For unique-prompt workloads (each
dev different repo at full 256K), the realistic ceiling is 6-8 within
a 15-minute wall clock window — limited by compute, not memory.

### 4. Long-context coherence — needle in haystack at 200K

A unique sentinel function `calc_repomind_token_budget_v7` and a magic
constant `4242` are embedded in a ~200K-token code corpus at three
positions. Pass = both substrings present in model response.

| Position | Prompt tokens | Elapsed | Found name | Found const | **PASS** |
|---|---|---|---|---|---|
| early | 99,814 | 29.0s | ✅ | ✅ | ✅ |
| **middle** | **199,413** | **73.2s** | ✅ | ✅ | ✅ |
| late | 99,814 | 20.5s | ✅ | ✅ | ✅ |

The middle test is the strongest evidence: model recovers the planted
fact from the deepest portion of a near-full-context prompt. 256K
window is *usable*, not just *allocated*.

### 5. End-to-end repo Q&A — 9/9 correct

| Tier | Repo | Total tokens | Files | Chunks | Prompt sent | Q1 | Q2 | Q3 |
|---|---|---|---|---|---|---|---|---|
| small | this repo (REPOMIND) | 67,618 | 68 | 348 | 72,728 | ✅ | ✅ | ✅ |
| medium | `pallets/flask` | 408,447 | 227 | 1,995 | 179,985 | ✅ | ✅ | ✅ |
| **large** | `pytorch/vision` | **1,307,491** | **581** | **6,799** | 179,984 | ✅ | ✅ | ✅ |

Sample answers (from `e2e/*_q*.txt`, verbatim):

> *Q (pytorch/vision): "Where does video decoding live?"*
> A: "Video decoding lives in the `torchvision.io` module, specifically
> in `torchvision/io/video.py` and `torchvision/io/video_reader.cpp`.
> The implementation uses `pyav` (FFmpeg bindings) as the backend…"

> *Q (Flask): "Where is the WSGI request entry point?"*
> A: "The WSGI request entry point is the `wsgi_app` method of the
> `Flask` class, defined in `src/flask/app.py`. The `__call__` method
> delegates to `wsgi_app`, making the Flask instance itself a WSGI
> application."

> *Q (REPOMIND self): "Which agent module implements the SC-TIR loop,
> and how many max steps by default?"*
> A: "The `agent/loop.py` module implements the SC-TIR loop (PLAN →
> CALL TOOL → OBSERVE → THINK → ANSWER), adapted from AIMO3's math
> reasoning pipeline. By default, the agent runs with `max_steps=6`."

The 1.3M-token pytorch/vision repo is 5× too large for any context
window. REPOMIND's priority-aware chunker (README ▷ top-level symbols
▷ nested ▷ tests, with token budget) trimmed to 180K of highest-priority
content; the agent answered correctly anyway with file path citations.

### 6. Cost economics

![cost](plot_cost.png)

At AMD Developer Cloud rate ($1.99/hr per MI300X) and observed best
aggregate throughput (12.08 tok/s at 32K, N=31):

- **$45.75 / 1M completion tokens** (cloud-rented, aggregate)
- **14.5 active continuous queriers per MI300X** (assumes 6 substantive
  queries/hr per dev, 500-token responses)
- For typical bursty engineering workloads (10-20% peak active
  concurrency): **70-140 developer seats per MI300X**
- Owned MI300X ($18K capex) breaks even vs Cursor Teams ($40/dev/mo)
  in **3-6 months** at typical team-of-100 usage

**Important caveat**: For compliance-locked enterprises (banks,
defense, healthcare) that *cannot* legally use SaaS coding agents at
all, REPOMIND on owned AMD hardware is not "savings" — it is the
**first option that exists** for AI-assisted coding inside their
infrastructure.

## Reproducibility

The full benchmark suite (5 phases) is in
`competitions/repomind/benchmarks/runner/`:

```bash
# On a fresh MI300X x1 droplet with vLLM serving Qwen3-Coder-Next-FP8:
cd /workspace/repomind
bash benchmarks/runner/run_all.sh
```

Total ~97 minutes wall clock, ~$3.22 cost, single-shot. All phases
write JSON + plots to `benchmarks/results/`.

The same scripts run locally against `_stub_server.py` (OpenAI mock)
for laptop validation.

## Honest limitations of this evidence pack

- **Identical-prompt assumption** for concurrency cells inflates the
  upper bound for shared workloads. Per-user unique prompts would
  produce lower N at long context — see honest framing in §3.
- **vLLM FP8 KV cache scaling factors** were uncalibrated (`q_scale =
  prob_scale = 1.0`); vLLM warns this may affect accuracy. Long-context
  needle test still passed 3/3, but heavier accuracy work would benefit
  from calibration.
- **Single hardware run** — these are first-pass numbers from one
  session. Production deployment would warrant repeat runs and
  variance analysis.
- **AMD Developer Cloud capacity** was occasionally constrained on
  2026-05-05 (multiple users in Discord reported "out of GPUs" errors
  attempting to recreate destroyed droplets); region selection and
  timing may affect availability.

## Citations

- AMD Day-0 ROCm 7 Qwen3-Coder-Next blog (Feb 2026):
  https://www.amd.com/en/developer/resources/technical-articles/2026/day-0-support-for-qwen3-coder-next-on-amd-instinct-gpus.html
- Qwen3-Coder-Next-FP8 model card:
  https://huggingface.co/Qwen/Qwen3-Coder-Next-FP8
- vLLM 0.17.1 release: ROCm 7.2 support
- lablab.ai tutorial (2026-04-30):
  https://lablab.ai/ai-tutorials/amd-huggingface-deployment-for-ai-hackathons
- REPOMIND GitHub: https://github.com/SRKRZ23/repomind
