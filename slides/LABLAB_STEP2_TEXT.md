# Lablab.ai Step 2 — Pre-filled submission fields

All text ready to paste during Step 2/3 final submission. Open lablab.ai
team page → REPOMIND → continue to Step 2 → paste each field.

---

## Cover image

**File**: `assets/cover.png` (1200×630 PNG)

If updating with verified numbers, replace cover.png with refreshed
version showing the 31/31, 3/3, 9/9 highlights. Optional — current
cover is solid.

---

## Project Title

```
REPOMIND
```

(or `REPOMIND — Repo-scale coding agent on AMD MI300X` if a longer
field is offered)

---

## Short Description (typically ≤255 chars)

```
Open-source repo-scale coding agent verified on AMD MI300X. Single
GPU, Qwen3-Coder-Next-FP8, 256K context. 31/31 users at 8K-64K, 3/3
needle 200K, 9/9 correct on pytorch/vision (1.3M tokens). 124-min
stress test, AITER tuning A/B. MIT.
```

(~252 chars — within typical 255 limit)

---

## Long Description (typically ≤2000 chars, often 1500-1900 ideal)

```
REPOMIND is an open-source repo-scale coding agent that ingests an
entire git repository at 256K context on a single AMD MI300X and
reasons across the whole codebase with multi-step tool use. MIT
licensed. Built for the AMD Developer Hackathon 2026.

Why MI300X specifically: Qwen3-Coder-Next-FP8 weights (~80 GB) + 256K
KV cache @ FP8 (~38 GB) + activations (~25 GB) = ~143 GB total. NVIDIA
H100 80 GB cannot accommodate this on a single card by VRAM
accounting; MI300X 192 GB has the headroom. AMD's Day-0 ROCm 7 support
post (Feb 2026) positioned this exact workload — REPOMIND is the
first open-source proof shipped.

Verified on real hardware (2026-05-05/06, 124-min stress test across 2
sessions, $4.12 total):

• Memory: 77.29 GiB weights + 94.58 GiB KV cache available + 92% VRAM
  peak. /v1/models confirms max_model_len=262144.

• Concurrency (24-cell matrix, default Triton): 31/31 success at 8K,
  16K, 32K, AND 64K — every realistic-developer context. 25/31 at
  128K. 6-8 at 256K within a 15-min window.

• Long-context coherence: 3/3 needle-in-haystack pass at 200K. Model
  recovers embedded sentinel function and constant from middle of
  199K-token prompt.

• End-to-end repo Q&A: 9/9 correct across REPOMIND self (68K), Flask
  (408K), pytorch/vision (1.3M tokens — 5× larger than any context
  window). Priority-aware chunker fits to 180K.

• Tuning attempt: tried --attention-backend ROCM_AITER_FA. Throughput
  2-4× higher BUT output degenerates to repeating punctuation tokens
  on FP8 KV cache (137/144 cells broken). Default Triton stays
  production-safe; filed for AMD upstream investigation.

Stack: Qwen3-Coder-Next-FP8 + vLLM 0.17.1 + ROCm 7.2 + SC-TIR agent
loop + 5 tools (read_file, grep_codebase, execute_code, run_tests,
git_log).

Market unlock: banks, defense, pharma, Apple iOS team — they legally
can't use SaaS coding agents. $1.99/hr cloud, 70-140 dev seats per
MI300X. Owned MI300X breaks even vs Cursor in 3-6 months at team-of-
100 usage. For compliance-locked enterprises, REPOMIND is the first
option that exists.

Full evidence pack: 7 JSON results + 5 plots + raw model outputs +
rocm-smi snapshots + run logs + reproducible benchmark scripts.
```

(~1995 chars — fits typical 2000 limit)

---

## Tags / Technologies (typically 3-5 fields)

```
amd-mi300x
rocm
vllm
qwen3-coder
long-context
agents
coding-agent
fp8
mit
```

---

## Categories / Tracks selected

- [x] **AI Agents & Agentic Workflows** (primary)
- [x] **Hugging Face Special Prize** (Space in event org, like-driven)
- [x] **Build-in-Public Extra Challenge** (≥2 X/LinkedIn posts compliant)
- [x] **Qwen partner challenge** (uses Qwen3-Coder-Next-FP8)
- [ ] (Optional) Fine-Tuning on AMD GPUs (only if LoRA done in time)

---

## Tech Update Links (3 required)

```
https://github.com/SRKRZ23/repomind/blob/main/EVOLUTION.md
```

```
https://github.com/SRKRZ23/repomind/tree/main/benchmarks/2026-05-05-mi300x-stress-test
```

```
https://x.com/SardorRazi99093  (Build-in-Public posts thread)
```

(Add LinkedIn / Forum links if 4+ slots available; LinkedIn longer post
mentioned in POSTS_DRAFTS.md is good fit)

---

## AMD Developer Experience Feedback (typically 500-1000 chars)

```
The MI300X x1 droplet experience exceeded expectations on three
dimensions worth flagging:

1. Time-to-first-token: spin up + vLLM serve = ~5 min from droplet
   creation to working /v1/models endpoint with max_model_len 262144.
   The vLLM 0.17.1 + ROCm 7.2 Quick Start image worked zero-config —
   docker exec, single vllm serve command, done. No ROCm install pain.

2. Cost transparency: $1.99/hr per-second billing, accurate dashboard.
   124-min full benchmark suite (2 sessions) cost $4.12 — predictable.

3. The 192 GB single-card story is real and matters. We measured 77.29
   GiB weights + 94.58 GiB KV cache + 92% peak utilization at full
   256K context. On H100 80 GB this configuration would require 2-4×
   sharding with AllReduce overhead. MI300X just runs it.

Three flags for the team:

* The "Maximum concurrency: 31.08x" line in vLLM startup logs assumes
  chunked-prefix-cache sharing — clarifying this in developer
  documentation would help newcomers calibrate expectations for
  unique-prompt workloads.

* AITER attention backend (--attention-backend ROCM_AITER_FA) +
  --kv-cache-dtype fp8 currently produces broken output on
  Qwen3-Coder-Next-FP8 — 137/144 cells in our test produced repeating
  punctuation tokens instead of real text. Default Triton was clean
  (0/144 broken). Worth investigating; vLLM startup logs flag
  q_scale and prob_scale as uncalibrated for FP8 attention. Happy to
  share the full evidence pack with whoever owns the ROCm attention
  kernel path.

* GPU capacity in ATL1 was occasionally constrained on 2026-05-05;
  multiple Discord users reported "out of GPUs" errors recreating
  destroyed droplets. Worth surfacing this in the dashboard so users
  can plan around capacity windows.

Overall: 9/10 developer experience. Will deploy on AMD again.
```

---

## Demo Video URL

```
[paste YouTube/Vimeo URL after recording is done]
```

---

## Slide Deck URL

```
[paste Google Drive / Dropbox / GitHub link to SLIDE_DECK.pdf]
```

(Suggest uploading PDF to GitHub repo at `slides/SLIDE_DECK.pdf` and
linking that — keeps everything in one MIT-licensed bundle)

---

## GitHub Link

```
https://github.com/SRKRZ23/repomind
```

---

## HuggingFace Space Link

```
https://huggingface.co/spaces/lablab-ai-amd-developer-hackathon/repomind
```

---

## Live Demo URL (if requested)

```
https://huggingface.co/spaces/lablab-ai-amd-developer-hackathon/repomind
```

(Same as HF Space — the Space IS the live demo)

---

## Author / Team

```
Sardor Razikov (@Sardor_R on lablab) — solo

Tashkent 🇺🇿
ML engineer · AI researcher

Background:
- Kaggle SPR 2026 #7/371 (Top 1.9%) — Portuguese medical NLP, BI-RADS classification
- Kaggle S6E3 #23/4,142 (Top 0.55%) — Customer Churn
- AIMO3 39/50 — XTX $2.2M olympiad with custom SC-TIR pipeline on gpt-oss-120B
- Author: Epistemic Curie Benchmark (Zenodo DOI 10.5281/zenodo.19791329)
- TriageGuardian: 99.62% accuracy on 80K ED records

Lablab participant ID: 9361 (Approved)
GitHub: SRKRZ23
HuggingFace: ZeroR3
X: @SardorRazi99093
LinkedIn: linkedin.com/in/sardorrazikov
Email: razikovs777@gmail.com
```

---

## Submission Checklist (before clicking "Final Submit")

- [ ] Cover image uploaded (assets/cover.png or refreshed)
- [ ] Title field filled
- [ ] Short Description filled (~242/255 chars)
- [ ] Long Description filled (~1972/2000 chars)
- [ ] Tags / Technologies (3-5 selected)
- [ ] Tracks selected (4 of them)
- [ ] Tech Update Links (3-4 URLs pasted)
- [ ] AMD Feedback filled
- [ ] Demo Video URL pasted (after recording)
- [ ] Slide Deck URL pasted (after upload)
- [ ] GitHub link
- [ ] HF Space link
- [ ] Author info
- [ ] Save Draft → review → Final Submit

After Final Submit confirmation email arrives:
- Trigger build-in-public posts wave per POSTS_DRAFTS.md schedule
- Push verified data to GitHub + HF Spaces (one big commit)
- Send DMs to Clem (HF CEO), Jeff Boudier (HF VP Product), VB, Qwen team (note: Junyang Lin stepped down March 2026, reach via Qwen team channels)
