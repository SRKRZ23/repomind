# Submission checklist (for May 11 00:00 Tashkent)

## Required deliverables

- [ ] `book.pdf` style demo video, 3–5 min, hosted on YouTube unlisted
- [ ] GitHub repo public at `github.com/SRKRZ23/repomind`, MIT license
- [ ] HuggingFace Space at `huggingface.co/spaces/Sardor_R/repomind` runnable
- [ ] Devpost / lablab.ai project page filled
- [ ] Submission link on `lablab.ai/event/amd-developer-hackathon`

## Hackathon page form

- **Project Title**: `REPOMIND`
- **Tagline (≤ 50 chars)**: `Open-source repo-scale coding agent on MI300X`
- **Track**: Track 1 (AI Agents) — primary; Track 2 (Fine-Tuning) if LoRA shipped
- **Tags**: `rocm`, `mi300x`, `vllm`, `qwen3-coder`, `agent`, `long-context`, `open-source`

## Description (long form)

### Problem
Engineering teams pay $40/dev/month for Cursor or Claude Code. Both are closed
source. Both refuse to send entire repositories to the model — they retrieve
fragments. For enterprises with regulated code (medical, legal, finance), the
status quo is "close the laptop and hope".

### Solution
REPOMIND ingests an entire git repository into a 256K-token context window
on a single AMD MI300X, then answers questions across the whole codebase
with a 5-tool agent loop.

### Why MI300X
192 GB HBM3 single-GPU is unique. NVIDIA H100 80GB physically OOMs at this
context length. AMD's Day-0 ROCm support for Qwen3-Coder-Next is the
foundation — REPOMIND is the productization.

### What's open
Everything: ingestion, agent loop, tools, vLLM client, UI, benchmarks. MIT.
Self-host on your own MI300X; your code never leaves your infrastructure.

### Demo
[YouTube link]
- 0:00 hook (Linux kernel → trace one slab allocation)
- 0:20 ingestion (paste GitHub URL, watch tokens count up)
- 1:30 agent reasoning live, tool calls visible
- 2:30 benchmark frame (H100 OOM vs MI300X)
- 3:00 closing pitch + open-source links

## Build-in-Public proof

- [ ] Twitter post Day 1 (kickoff)
- [ ] Twitter post Day 3 (first real ingest)
- [ ] Twitter post Day 5 (benchmarks)
- [ ] Twitter post Day 6 (submission)
- [ ] LinkedIn long-form Day 6
- [ ] All tagged `@AIatAMD @lablabai #AMDHackathon`

## Pre-submit smoke checks

- [ ] `pytest tests/ -v` shows 27/27 passing
- [ ] `python -m scripts.ingest --path . --out /tmp/x.json` works
- [ ] `python -m scripts.ask_agent --backend mock` produces an answer
- [ ] HF Space cold-start under 60 s
- [ ] vLLM endpoint on AMD Cloud reachable from HF Space (or backend hosted there)
- [ ] README badges all green

## After submit

- [ ] Tweet "submitted" with the demo video link
- [ ] Slack the lablab Discord `#submissions` channel with the link
- [ ] Tag judges relevant to the angle (Mahdi Ghodsi, Maharshi Trivedi)
- [ ] Save backup videos / repo snapshot to local disk
