# Hakob follow-up reply — AMD Developer Community Forum thread #505

Reply text ready to paste on the existing Hakob_Arzumanyan thread, AFTER
the lablab final submission lands. This is the data-rich follow-up to the
initial brief acknowledgment that's already posted.

Title in Hakob's reply: "30 tok/s at 8K feels slow… concurrency at 8K-32K?"

---

## The reply

```
Hi Hakob — measured both questions you raised. Posting the data here
because it's exactly the kind of detail that belongs on a community
forum, not buried in a hackathon submission.

== Q1: "30 tok/s at 8K feels slow" ==

That number was a cold-start outlier in my session-1 spot check (the
8K cell was the very first request after vLLM startup and ate the
torch.compile + CUDA-graph capture tail). I re-measured everything
hot, no startup contamination:

  Hot single-user TTFT (default Triton attention backend):
    8K  context: 0.46s
    16K context: 1.55s
    32K context: 3.20s
    64K context: 10.0s
    128K       : 33.0s
    256K       : 117.8s

  Linear in prompt size, exactly as theory predicts (prefill-bound).

  Aggregate 31-user concurrent throughput, default Triton:
    8K:  78.5 tok/s
    16K: 31.4 tok/s
    32K: 12.1 tok/s
    64K:  3.6 tok/s

  31/31 success at every one of those four contexts. So the realistic-
  developer-workload range you asked about is solid.

== Q2: "concurrency at 8K-32K where most users live" ==

Full 24-cell matrix, default Triton, all 144 outputs clean:

         N=1    N=8    N=16   N=31 success
  8K     36.5   69.4   75.2   78.5 (31/31 ✅)
  16K    21.2   30.2   30.9   31.4 (31/31 ✅)
  32K     9.95  11.85  11.87  12.08 (31/31 ✅)
  64K     3.41   3.57   3.60   3.61 (31/31 ✅)

  (numbers = aggregate completion tok/s)

  At 128K we lose 6 of 31 to the 15-min timeout; at 256K compute
  saturates around N=8 (this is from session 1's 12-cell matrix).

== Bonus: vLLM tuning attempt — measured regression ==

You asked specifically if I tried any vLLM settings to push throughput.
I did. Tried --attention-backend ROCM_AITER_FA (AMD's hand-tuned MI300X
attention kernels). Two findings:

  Throughput went 2-4× higher under AITER:
    8K  × 31:  78.5 → 168.4 tok/s  (+114%)
    16K × 16:  30.9 →  89.9 tok/s  (+191%)
    64K × 31:   3.6 →  18.5 tok/s  (+411%)
    TTFT @ 64K: 10.0s → 3.54s      (~2.8× faster)

  AITER also reports slightly higher max concurrency at startup
  (31.31× vs 31.08×) and a much faster torch.compile warmup
  (~21s vs ~59s).

  BUT: the output degenerated to repeating punctuation tokens on the
  FP8 KV cache configuration. Out of 144 AITER cells, 137 produced
  responses like:

    "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

  …instead of real text. The few cells that stayed coherent were
  mostly 8K N=1, where prefill is fast enough that the bug doesn't
  trigger (or triggers at a lower rate I couldn't characterize from
  one sample).

  Default Triton on the same configuration: 0 of 144 cells broken.

So the tuning lever exists but has a caveat. Default Triton is the
production-safe choice on Qwen3-Coder-Next-FP8 + FP8 KV cache for now.

vLLM startup logs flag both q_scale and prob_scale as uncalibrated
for the FP8 attention path — likely related. Filing as an upstream
issue after the hackathon submission lands; happy to share the full
evidence pack with whoever owns the ROCm attention kernel path.

== Evidence pack ==

All numbers above reproducible from:
github.com/SRKRZ23/repomind/tree/main/benchmarks/2026-05-05-mi300x-stress-test

Two-session total: 124 min wall clock, $4.12 of credits.
Single MI300X x1, vLLM 0.17.1 + ROCm 7.2 Quick Start image.

Thanks for the question — surfacing this AITER regression in public
is more useful for the community than burying it in a hackathon
submission.

— Sardor (Tashkent 🇺🇿, REPOMIND)
```

---

## When to post this

POST AFTER:
1. Lablab final submit lands (Step 3 confirmation email arrives)
2. Initial X / LinkedIn posts have gone live (T+0 to T+1h post-submit)
3. ~T+2h post-submit, paste this on Hakob's existing reply thread

NOT BEFORE: keeps the "wow factor" of the submission's evidence pack
intact and lets the AMD Forum thread amplify the reveal rather than
preempt it.

## Why this reply works strategically

1. **Direct answers** to both Hakob's questions, with measured numbers.
   Not opinion, not deflection — data.

2. **Bonus content** he didn't ask for (AITER A/B) shows we went deeper
   than required. This is the kind of post community moderators
   recognize and the AMD product team forwards internally.

3. **Honest reporting of regression** is better signal than only
   reporting wins. Anyone who's worked with vLLM + ROCm at scale knows
   AITER + FP8 KV cache is finicky; calling that out publicly builds
   credibility with the people who matter most (AMD compute, vLLM
   maintainers, ROCm engineers).

4. **Clear path forward**: filing upstream after submission. Doesn't
   leave AMD on the hook for "fix this in 24 hours" — gives them the
   data and the option.

5. **Tags location and project** at the end without being promotional —
   forum culture rewards substance, not pitching.
