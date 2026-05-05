# REPOMIND

> Open-source repo-scale coding agent for self-hosted use. Ingest an entire git repo (256K tokens), reason across it with tools — on a single AMD MI300X.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ROCm 7](https://img.shields.io/badge/ROCm-7.0-red)](https://rocm.docs.amd.com/)
[![vLLM](https://img.shields.io/badge/vLLM-Day0_Qwen3_Coder-blue)](https://www.amd.com/en/developer/resources/technical-articles/2026/day-0-support-for-qwen3-coder-next-on-amd-instinct-gpus.html)
[![AMD Hackathon](https://img.shields.io/badge/AMD_Developer_Hackathon-2026-orange)](https://lablab.ai/ai-hackathons/amd-developer)
[![HF Space](https://img.shields.io/badge/🤗_Hugging_Face-Space-blue)](https://huggingface.co/spaces/lablab-ai-amd-developer-hackathon/repomind)

## What this is

A **long-context coding agent** designed to read an entire git repository (up to 256K tokens, FP8) on a **single AMD Instinct MI300X**, then answer any question about the code with multi-step reasoning and real tool use (read, grep, execute, test, git).

Closed-source coding agents (Cursor, Claude Code, etc.) can't do this:

- They are closed source. Your enterprise code can't leave your infrastructure.
- They don't load entire repositories — they retrieve fragments.
- They cost $19–$40 per developer per month.

REPOMIND is open-source MIT, runs on your own GPU, sees your whole codebase by design.

## Why MI300X

The phantom piece is **192 GB HBM3 on a single chip**. NVIDIA H100 caps at 80 GB. By VRAM accounting, running Qwen3-Coder-Next at 256K context in FP8 requires weights (~80 GB) + KV cache (~38 GB) + activations (~25 GB) ≈ ~143 GB total — exceeding single-GPU H100 80 GB capacity, while comfortably fitting MI300X 192 GB. AMD's own [Day-0 ROCm support post](https://www.amd.com/en/developer/resources/technical-articles/2026/day-0-support-for-qwen3-coder-next-on-amd-instinct-gpus.html) confirms this is exactly the workload MI300X was built for. Empirical validation on real MI300X hardware is the Day 2-3 milestone.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                       User (Browser / API)                   │
│              "Explain mm/slab.c → call graph"                │
└───────────────┬──────────────────────────────────────────────┘
                │ Gradio / SSE
                ▼
┌──────────────────────────────────────────────────────────────┐
│  Ingestion                                                   │
│  GitPython clone → tree-sitter AST → smart chunk →           │
│  priority-aware truncation (README ▷ top-level ▷ details)    │
└───────────────┬──────────────────────────────────────────────┘
                ▼
┌──────────────────────────────────────────────────────────────┐
│  Agent Loop (SC-TIR style — adapted from AIMO3)              │
│  PLAN → CALL TOOL → OBSERVE → THINK → ANSWER                 │
│  Tools: read_file · grep_codebase · execute_code             │
│         run_tests · git_log                                  │
│  Tool calls parsed by vLLM's qwen3_coder parser              │
└───────────────┬──────────────────────────────────────────────┘
                ▼
┌──────────────────────────────────────────────────────────────┐
│  Inference (single-GPU MI300X, ROCm 7)                       │
│  Qwen/Qwen3-Coder-Next-FP8  —  80B params, 3B active (MoE)   │
│  vLLM ROCm 7 backend, FP8 KV cache, 256K max_model_len       │
└──────────────────────────────────────────────────────────────┘
```

## Status

**Verified on real MI300X hardware (2026-05-05 smoke test):**

- [x] Repo skeleton, LICENSE, .gitignore, requirements
- [x] Ingestion pipeline scaffolding (no GPU)
- [x] Tool layer (read_file / grep / execute / tests / git_log)
- [x] SC-TIR agent loop (mock LLM client; runs unit tests offline)
- [x] Gradio UI scaffold
- [x] Unit tests passing without GPU (27 tests)
- [x] HuggingFace Space deploy (in `lablab-ai-amd-developer-hackathon` org)
- [x] $100 AMD Cloud credits (received in 2 hours, not 2 business days)
- [x] lablab.ai team + Step 1 of submission saved
- [x] **MI300X x1 spinup + vLLM 0.17.1 (ROCm 7.2) Quick Start image — verified working**
- [x] **Qwen/Qwen3-Coder-Next-FP8 served at `--max-model-len 262144` (256K) — verified, `Application startup complete`, `/v1/models` returns `max_model_len: 262144`**
- [x] **Real Python code generation through `/v1/chat/completions` — verified (merge sort, LCS, Hello World)**

**Pending:**

- [ ] Repo ingestion smoke test on Linux kernel
- [ ] LoRA fine-tune on code-specific subset (Track 2 bonus)
- [ ] Demo video (3–5 min)
- [ ] Step 2 + Step 3 of lablab submission (cover image + video + slides)
- [ ] Final submit on lablab.ai before 2026-05-11 00:00 Tashkent

## Quickstart (local, no GPU)

```bash
git clone https://github.com/SRKRZ23/repomind.git
cd repomind
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run unit tests (no GPU, no network)
pytest tests/ -v

# Ingest a small repo (filesystem mode, no clone)
python -m scripts.ingest --path . --out .repomind_cache/self.json

# Run agent against the mock LLM (sanity check)
python -m scripts.ask_agent --question "what does the chunker do?" \
                             --repo .repomind_cache/self.json \
                             --backend mock
```

## Quickstart (MI300X, ROCm 7)

```bash
# On AMD Developer Cloud, ROCm 7 image
docker run --device=/dev/kfd --device=/dev/dri \
    --group-add video --shm-size 16g -p 8000:8000 \
    -v $PWD:/workspace -w /workspace \
    rocm/vllm:rocm7.0_vllm_qwen3coder_next \
    bash -c "vllm serve Qwen/Qwen3-Coder-Next-FP8 \
              --tool-call-parser qwen3_coder \
              --max-model-len 262144 \
              --kv-cache-dtype fp8"

# Then query
python -m scripts.ask_agent --question "..." --repo ... --backend vllm \
                             --base-url http://localhost:8000/v1
```

## Repo layout

```
repomind/
├── README.md
├── LICENSE                          MIT
├── requirements.txt
├── ingestion/                       GitHub URL → JSON chunks
│   ├── cloner.py                    GitPython wrapper, shallow clone
│   ├── parser.py                    tree-sitter AST per language
│   ├── chunker.py                   smart, structure-aware chunking
│   └── token_budget.py              priority-aware truncation to N tokens
├── tools/                           Agent tool layer
│   ├── read_file.py
│   ├── grep.py
│   ├── execute_code.py              sandboxed Python runner
│   ├── run_tests.py
│   └── git_log.py
├── agent/                           SC-TIR style loop
│   ├── loop.py                      PLAN → CALL → OBSERVE → THINK
│   ├── prompts.py                   system + tool prompts
│   └── parser.py                    qwen3_coder tool-call format
├── serving/                         LLM backend abstraction
│   ├── base.py                      LLMClient protocol
│   ├── vllm_client.py               OpenAI-compatible client for vLLM
│   └── mock_client.py               offline test backend
├── ui/                              Gradio web UI
│   └── app.py
├── benchmarks/                      H100 OOM reference + AMD numbers
│   └── README.md
├── tests/                           pytest suite (no GPU)
└── scripts/                         CLIs
    ├── ingest.py
    └── ask_agent.py
```

## Verified benchmarks — single AMD MI300X, vLLM 0.17.1 + ROCm 7.2

Smoke test on AMD Developer Cloud (`MI300X x1`, $1.99 / GPU / hour, ATL1) on 2026-05-05.

**Memory budget for Qwen/Qwen3-Coder-Next-FP8 + 256K context, FP8 KV cache:**

| Component | Verified (rocm-smi + vLLM logs) |
| --- | --- |
| Model weights in VRAM | **77.29 GiB** |
| Available KV cache memory | **95.26 GiB** |
| GPU KV cache size | **2,080,752 tokens** |
| VRAM peak (vLLM running) | **176.6 GiB / 191.7 GiB** (92% utilization) |
| `--max-model-len 262144` | started, `Application startup complete` |
| `/v1/models` `max_model_len` | **262144** (verified via API) |
| **Maximum concurrency at 256K context** | **31.31× simultaneous full-256K-context users on a single MI300X** |
| Generation throughput (warm, 8K config) | 30 tokens/s (vLLM Engine logs) |
| Cold start (download + compile + warmup) | ~3 min 30 sec |
| Warm restart (model cached, 256K config) | ~1 min 30 sec |

H100 80 GB single-card cannot hold this configuration by VRAM accounting:
weights (~77 GiB) + 256K KV cache (~38 GiB) + activations + framework
overhead exceed 80 GiB. MI300X 192 GiB has the headroom and is empirically
the only single-GPU answer for this class of workload today.

Full evidence (rocm-smi, vLLM startup logs, JSON completion responses)
is available in `benchmarks/2026-05-05-mi300x-smoke-test/`.

For Qwen3-Coder-Next-FP8 + 256K context window, the memory budget breakdown was:
- Weights: ~80 GB
- 256K KV cache @ FP8: ~38 GB
- Activations: ~25 GB
- **Total: ~143 GB**

| Workload | NVIDIA H100 80GB (single-GPU) | AMD MI300X 192GB (single-GPU) |
| --- | --- | --- |
| Qwen3-Coder-Next-FP8 @ 128K context | exceeds capacity by VRAM math | within headroom (target) |
| Qwen3-Coder-Next-FP8 @ 256K context | exceeds capacity by VRAM math | within headroom (target) |
| Linux kernel ingest (15M tokens → 256K window) | requires multi-GPU sharding | single-card design target |

H100 single-card cannot accommodate this configuration by VRAM accounting; sharding across 2–8 cards would be required to match the per-card memory of MI300X. The architectural argument is mathematical; **empirical confirmation (throughput, latency, real-world stability at 256K) is the Day 2-3 milestone**.

## Roadmap (post-hackathon)

- Multi-repo ingestion + cross-repo search
- Streaming UI with live tool-call traces
- LoRA adapters for specific languages / domains (Rust kernel, K8s, etc.)
- Slack / GitHub bot integrations
- Quantization experiments (INT4 for 384K context on MI300X)

## License

MIT — see [LICENSE](LICENSE).

## Author

[Sardor Razikov](https://lablab.ai/u/@Sardor_R) — ML engineer & independent researcher · Tashkent 🇺🇿
- Kaggle SPR 2026 #7/371 (Top 1.9%) · S6E3 #23/4,142 · AIMO3 39/50 (XTX $2.2M)
- Author: [Epistemic Curie Benchmark](https://doi.org/10.5281/zenodo.19791329)
- TriageGuardian: 99.62 % accuracy on 80 K ED records

Built for the [AMD Developer Hackathon 2026](https://lablab.ai/ai-hackathons/amd-developer).
