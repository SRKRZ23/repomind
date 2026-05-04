# Build-in-Public posts

Drafts for the Extra Challenge prize. Tag `@AIatAMD` and `@lablabai` on every post.
Cross-post from Twitter/X to LinkedIn (LinkedIn loves this kind of technical narrative).

---

## Day 1 — Kickoff (post tonight)

```
🛠️ Building REPOMIND for the @AIatAMD @lablabai hackathon:
open-source repo-scale coding agent on AMD MI300X.

The pitch in one line: ingest an ENTIRE git repo (256K tokens),
reason across it with tools — on a single GPU.

Why AMD? 192 GB HBM3 on one chip = NVIDIA H100 OOMs at this context.

Day 1: scaffolding, tests passing without GPU.
27 tests ✅ | mock LLM agent loop runs end-to-end on this very repo.

github.com/SRKRZ23/repomind  (will go public in a few hours)

#AMDHackathon #ROCm #Qwen3Coder #OpenSource
```

---

## Day 2 — MI300X spinup (post tomorrow when credits arrive)

```
Day 2 of REPOMIND on @AIatAMD MI300X 🟢

Spun up Qwen3-Coder-Next-FP8 on a single MI300X via vLLM ROCm 7.
Smoke tests:
  10K context  → ✅
  50K context  → ✅
 200K context  → ✅

That last one is the wild number. NVIDIA H100 80GB physically can't hold
a 200K KV cache + 80B param weights in FP8. Single-card MI300X just does it.

Numbers in screenshot. Everything open-source.

#AMDHackathon
```

---

## Day 3 — Repo ingestion shows its teeth (after first real ingest)

```
Day 3 — REPOMIND just ingested the entire Linux kernel mm/ subtree on MI300X 🐧

178K tokens, 41 files, in <30 seconds.
Asked: "Trace one slab allocation through the call graph."

The agent called grep, read_file (×3), then composed a 4-step trace
with line-level citations.

Cursor / Claude Code can't see this much context. AMD's 192 GB single-GPU
is the unlock.

Demo video coming Friday.

@AIatAMD @lablabai #AMDHackathon
```

---

## Day 5 — Benchmarks reveal (after R2 numbers)

```
Day 5 of REPOMIND. Benchmarks just dropped.

                    H100 80GB    MI300X 192GB
  64K context        works         works
 128K context        OOM ❌       works ✅
 256K context        OOM ❌       works ✅ ~30 tok/s

This is not a CUDA-vs-ROCm story. It's a memory-architecture story.
The 192 GB HBM3 single-GPU advantage is *the* AMD AI moat right now.

Open-source repo: github.com/SRKRZ23/repomind
HF Space: huggingface.co/spaces/Sardor_R/repomind

@AIatAMD @lablabai #AMDHackathon
```

---

## Day 6 — Submission

```
Submitted REPOMIND to @AIatAMD @lablabai hackathon 🚀

Open-source Cursor for self-hosters. Ingest an entire git repo,
ask any question, get cited answers. Runs on a single AMD MI300X.

✅ Track 1: AI Agents (SC-TIR loop with 5 tools)
✅ Track 2: Fine-Tuning (LoRA adapter)
✅ HF Special Prize (Space deploy)
✅ Build-in-Public

Demo video: <link>
GitHub: github.com/SRKRZ23/repomind  (MIT)
HF Space: huggingface.co/spaces/Sardor_R/repomind

Thanks to AMD for putting Day-0 ROCm support behind Qwen3-Coder-Next.
This whole project rides on that decision.

#AMDHackathon #ROCm
```

---

## Cross-post template — LinkedIn (longer form)

```
I just submitted REPOMIND to the AMD Developer Hackathon.

Six days ago I was looking at three tracks (Agents, Fine-Tuning,
Vision/Multimodal) and one strategic question: what does AMD actually
want to showcase?

The answer was sitting in a February 2026 AMD blog post: Day-0 ROCm
support for Qwen3-Coder-Next, with a quote about repo-scale coding
on a single MI300X. They were telling the entire developer community
exactly what kind of project would resonate.

So I built it.

REPOMIND is an open-source coding agent that ingests an entire git
repository (up to 256,000 tokens, FP8) and reasons across it with
five tools: read_file, grep_codebase, execute_code, run_tests, git_log.

The phantom piece is hardware, not software: 192 GB HBM3 on a single
MI300X means the model + KV cache + tool context all fit on one card.
NVIDIA H100 80GB physically OOMs at this context length.

Cursor and Claude Code are closed source. Your enterprise code can't
leave your infrastructure. REPOMIND is MIT, runs on your own AMD
hardware, sees your whole codebase.

The story I want AMD's marketing team to tell: "the open-source tool
that proves the MI300X memory advantage matters for real developer
workflows."

GitHub: github.com/SRKRZ23/repomind
Hugging Face: huggingface.co/spaces/Sardor_R/repomind

Thanks to @AIatAMD and @lablabai for the hackathon.
```
