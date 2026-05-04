# Day-1 X / Twitter post — REPOMIND kickoff

**Send tonight, 4 May 2026.** Tag `@AIatAMD` and `@lablabai`. Pin to your profile.

---

## Variant A — single tweet (recommended; tightest)

```
Day 1 of @AIatAMD x @lablabai hackathon 🟢

Building REPOMIND: an open-source repo-scale coding agent on AMD MI300X.

Ingest an entire git repo (256K tokens, FP8) on a SINGLE GPU.
H100 80GB physically OOMs at this context. MI300X 192GB doesn't.

27 unit tests already passing on the agent loop ✅
Day 2: vLLM Qwen3-Coder-Next-FP8 spinup.

#AMDHackathon #ROCm
```

Length: ~340 chars. Add link to GitHub repo once it's public.

---

## Variant B — short thread (use if you want amplification)

**Tweet 1/4** (the hook):
```
Why is no one building open-source Cursor?

Because doing it right needs 192 GB of GPU memory on a single chip.

Only AMD MI300X has it.

So I'm building it. 6 days. AMD Developer Hackathon. #AMDHackathon
```

**Tweet 2/4** (what):
```
2/ REPOMIND ingests an entire git repository — up to 256K tokens — and answers
any question with multi-step reasoning + 5 tools (read, grep, execute, test, git).

Cursor and Claude Code: closed-source, fragment retrieval.
REPOMIND: MIT, full-repo context.
```

**Tweet 3/4** (proof):
```
3/ Why MI300X specifically?

Qwen3-Coder-Next-FP8 (80B params, 3B active MoE) at 256K context:
  · weights ≈ 80 GB
  · KV cache @ FP8 ≈ 38 GB
  · activations + slack ≈ 25 GB
Total: ~143 GB on ONE card.

H100 80GB: physically can't.
MI300X 192GB: just runs.
```

**Tweet 4/4** (CTA):
```
4/ Day 1 status:
✅ Ingestion pipeline (tree-sitter + smart chunker + token budget)
✅ 5-tool registry (read/grep/execute/tests/git)
✅ SC-TIR agent loop (adapted from my AIMO3 math pipeline)
✅ 27/27 unit tests passing without GPU

Repo goes public tonight. Build-in-public, day-by-day.
@AIatAMD @lablabai #AMDHackathon #ROCm
```

---

## Tags & accounts to include

| Where | What |
| --- | --- |
| `@AIatAMD` | Required for AMD discoverability |
| `@lablabai` | Required for hackathon's Build-in-Public prize tracking |
| `#AMDHackathon` | Hashtag the hackathon team monitors |
| `#ROCm` | AMD developer audience |
| `#OpenSource` | Optional, broadens reach |

---

## Posting checklist

- [ ] GitHub repo public **before** posting (so the link actually works — see `git_push_commands.md`)
- [ ] Pin the tweet (or thread's first tweet) to your X profile
- [ ] Cross-post Variant A to LinkedIn (see `linkedin_day1.md`)
- [ ] Drop the tweet link in the lablab.ai Discord `#build-in-public` channel
- [ ] DM `@AIatAMD` saying you're building on MI300X — sometimes they retweet

## After posting

Save the tweet URL — you'll need it for the submission form on May 11. Lablab
verifies your Build-in-Public claim by checking timestamps + tags.
