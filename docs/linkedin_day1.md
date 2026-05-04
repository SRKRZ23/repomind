# LinkedIn Day-1 post — REPOMIND kickoff

**Post tonight (4 May 2026) right after the X tweet.** LinkedIn rewards
longer-form storytelling than X — go for narrative, not stats list.

---

## Final text — copy-paste ready

```
Six days from now I'll submit to the AMD Developer Hackathon.

I'm going solo. I'm going Track 2 (Fine-Tuning) plus the AI Agents track plus
the HuggingFace Special prize plus Build-in-Public — all with one project.

It's called REPOMIND.

Here's the pitch:

Cursor and Claude Code charge $40/dev/month, and they're closed source. For
enterprises with regulated code (medical, legal, finance), that's a non-starter
— the code can't leave their infrastructure. There's no real open-source
alternative because doing it right requires 192 GB of GPU memory on a single
chip. Only AMD MI300X has that today.

REPOMIND will ingest an entire git repository — up to 256K tokens, FP8 —
on a single MI300X, then answer any question across the codebase using
five tools: read_file, grep_codebase, execute_code, run_tests, git_log.

The phantom piece is hardware, not software. NVIDIA H100 80GB physically
cannot hold weights + 256K KV cache + activations on a single card. MI300X
192GB just runs it. That's not a CUDA-vs-ROCm story — it's a memory-architecture
story, and AMD's strategy paper from February 2026 already positioned MI300X
exactly for this workload (Day-0 ROCm support for Qwen3-Coder-Next).

Status today, Day 1:

  • Ingestion pipeline (tree-sitter + smart chunker + priority token budget)
  • 5-tool agent registry with sandboxed code execution
  • SC-TIR-style agent loop (adapted from the math reasoning pipeline I used
    on AIMO3 — XTX Markets $2.2M olympiad, score 39/50)
  • 27 unit tests passing without a GPU
  • vLLM ROCm 7 client wired and ready
  • Gradio UI scaffold

What's left: $100 AMD Cloud credits arrive in 2 business days; spin up MI300X;
fine-tune a small LoRA adapter for the Track 2 bonus; HuggingFace Space deploy;
benchmarks vs H100 OOM; demo video; submit by May 11.

Everything will be MIT. The story I want AMD's marketing team to be able to
tell at re:Invent: "the open-source coding agent that proves the MI300X memory
advantage matters for real workflows."

Day-by-day on X: [your X handle here]
Repo goes public tonight: github.com/SRKRZ23/repomind

#AMDHackathon #ROCm #OpenSource #LLM #AIInfrastructure
```

---

## Variations

### Shorter version (if 250-word version feels too long)

```
Six days. Solo. AMD Developer Hackathon.

Building REPOMIND — an open-source coding agent that ingests an entire git
repository (up to 256K tokens, FP8) on a single AMD MI300X, then answers
any question across the codebase with multi-step reasoning + 5 tools.

Why MI300X? 192 GB HBM3 single-GPU memory. NVIDIA H100 80GB physically can't
hold the model + 256K KV cache + activations. AMD can. This isn't a
CUDA-vs-ROCm story — it's a memory-architecture story.

Day 1 status:
✓ Ingestion pipeline + 5-tool registry + SC-TIR agent loop
✓ 27 unit tests passing without a GPU
✓ vLLM ROCm client wired

Day 2: MI300X spinup, Qwen3-Coder-Next-FP8 smoke tests.

Open source MIT. Day-by-day build-in-public.
Repo: github.com/SRKRZ23/repomind

#AMDHackathon #ROCm
```

### After-action version (post-submit, May 11)

Hold this until submission day. Lead with the demo video; the story above
becomes the second half.

---

## What to include below the post

- **Image / GIF**: a single screenshot of the architecture diagram from
  README.md, exported to PNG. Or a terminal recording (`asciinema` → SVG)
  of `pytest tests/` passing 27/27. Engagement on LinkedIn doubles with
  any embedded media.
- **Link card**: the GitHub repo URL — LinkedIn will auto-fetch the README
  badges and create a clean card.

## Tagging (LinkedIn-specific)

Tag these company pages directly in the post (`@` while typing):

- AMD
- Hugging Face
- lablab.ai

Tag people only if you've actually interacted with them before. Don't
spray-tag judges — LinkedIn shows that as low-quality signal and your
post gets demoted in feed.

## Posting time

Best LinkedIn windows for AI/ML audience: Tuesday–Thursday, 8–11 AM US ET
(which is 17:00–20:00 Tashkent). Tonight (Monday 4 May), post around
**21:30 Tashkent** — that's 10:30 AM East Coast, optimal for Anthropic /
Google DeepMind / Meta AI feeds.
