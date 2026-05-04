---
title: REPOMIND
emoji: 🧠
colorFrom: indigo
colorTo: red
sdk: gradio
sdk_version: "4.40.0"
app_file: ui/app.py
pinned: false
license: mit
hardware: cpu-basic
short_description: Repo-scale coding agent on AMD MI300X (256K context, FP8)
tags:
  - amd-mi300x
  - rocm
  - vllm
  - qwen3-coder
  - long-context
  - coding-agent
  - rag
  - open-source
---

# REPOMIND

> Open-source Cursor for self-hosters. Ingest an entire git repository
> (256K tokens, FP8), reason across it with tools — on a single AMD MI300X.

## What this Space does

This Space is the **frontend**: it lets you paste a GitHub URL or a local path,
choose a backend (mock for offline demo / vLLM for real), and ask any question.

The **backend** runs Qwen3-Coder-Next-FP8 on a real AMD MI300X via vLLM ROCm 7.
For demos, point the `vLLM base URL` field at any OpenAI-compatible endpoint
serving that model.

## Why this exists

| | H100 80GB | MI300X 192GB |
| --- | --- | --- |
| Qwen3-Coder-Next-FP8 @ 64K context | ✅ | ✅ |
| Qwen3-Coder-Next-FP8 @ 128K context | ❌ OOM | ✅ |
| Qwen3-Coder-Next-FP8 @ 256K context | ❌ OOM | ✅ |
| Linux kernel ingest in single context | impossible | demo target |

The 192 GB HBM3 single-GPU memory is genuinely unique to MI300X. Anything
needing >80 GB at FP8 KV cache + weights only runs on AMD.

## Links

- GitHub (MIT): https://github.com/SRKRZ23/repomind
- AMD Hackathon page: https://lablab.ai/ai-hackathons/amd-developer
- Author: https://lablab.ai/u/@Sardor_R

## License

MIT.
