# REPOMIND — Project Evolution Log

Single-source-of-truth for the project's day-by-day evolution. Each entry
links artifacts, decisions, and verified outcomes from that day.

---

## 2026-05-04 (Mon) — Day 1: Launch

### State at start of day
- AMD Developer Hackathon 2026 announced earlier (April).
- Sardor Razikov has just finished SPR 2026 mammography Kaggle (#7/371,
  Apr 29) and AIMO3 olympiad (39/50, XTX $2.2M).
- Decision to compete solo. No code yet; idea exploration phase.

### What landed by end of day
- **Project decided**: REPOMIND — repo-scale coding agent on AMD MI300X
  (chosen over Math reasoning port, ROCm Bridge, InfinitePrompt; the
  256K-on-single-GPU memory-architecture moat is the clearest defensible
  pitch — see `info.md` for the full ideation log)
- **GitHub `SRKRZ23/repomind`** (MIT) — repo skeleton, README, 27 unit
  tests passing without GPU
- **HF Space deployed** — first to personal `ZeroR3/repomind`, then
  duplicated to event org `lablab-ai-amd-developer-hackathon/repomind`
  (judged for HF Special Prize — Reachy Mini robot + 6mo HF PRO + $500
  credits for #1 by likes)
- **5-tool registry** built: read_file, grep_codebase, execute_code
  (sandboxed), run_tests, git_log
- **SC-TIR agent loop** adapted from Sardor's AIMO3 math pipeline
- **AMD Developer Program signup** → $100 cloud credits delivered in
  ~2 hours (lablab page implied 2 business days; AMD over-delivered)
- **lablab.ai team REPOMIND** created, **Step 1 saved**: title, short
  description, long description (1977/2000 chars), 4 categories, 4
  tracks, 3 technologies, all 3 Tech Update Links + AMD Developer
  Experience Feedback
- **Public posts**: X main + Update #2 (Build-in-Public compliant with
  @AIatAMD @lablabai @AMDDevHub @huggingface @vllm_project tags),
  LinkedIn long-form (~140 words)
- **Cover image**: 1200×630 PNG + SVG, white/black/AMD-red, memory
  comparison bar chart
- **Discord auto-mod ban**: 2× banned for legitimate project shares
  (automod aggressive on new accounts); appeals sent via 4 channels
  (Discord DM, email community@, email pawel.czech@, LinkedIn DM)

### Key decisions / hard-won lessons
- **Conservative claim discipline**: every public surface re-framed
  from promo language ("just runs", "physically OOMs", "Cursor for
  self-hosters") to engineering language ("has the headroom", "by VRAM
  accounting cannot accommodate", "open-source repo-scale coding agent")
- **Trademark cleanup**: dropped "Cursor for self-hosters" tagline to
  avoid potential nominative-fair-use issue
- **Status discipline**: every README split into VERIFIED ✅ +
  PENDING ⏳ explicit columns

### Cost so far
$0 spent of $100 credits.

---

## 2026-05-05 (Tue) — Day 2: Verified

### State at start of day
- Day 1 launched. Public artifacts live but mock-backend on HF Space.
- No empirical hardware data yet. F9 (memory-architecture moat) was
  first-principles math only.
- Sardor going into ~7-hour deep-work session ~21:00 Tashkent.

### What landed by end of day

**Discord unmute (early evening)**:
- Stephen Kimoi (lablab) lifted 7-day auto-timeout via email
- Sardor regained full Discord access, posted naked intro in
  `#introduce-yourself`
- Steve Kimoi later responded to Sardor by name during Twitch workshop
  ("Yes @sardor_r" + "feel free to type down your questions") —
  established direct rapport

**MI300X stress test (16:01 UTC → 17:38 UTC = 21:01 → 22:38 Tashkent)**:
- Spin up MI300X x1 droplet (ATL1, vLLM 0.17.1 + ROCm 7.2 image)
- Cold start verified: 3 min 30 sec total (download 80 GB + load +
  torch.compile 59s + CUDA graph capture 35s + warmup)
- vLLM `Application startup complete` confirmed
- `/v1/models` returns `max_model_len: 262144` ✅
- Full 5-phase benchmark suite ran cleanly under nohup
- 97 min wall clock total
- $3.22 spent of $100 credits (verified via DigitalOcean billing)

**Empirically verified**:

| Metric | Value | Source |
|---|---|---|
| Model weights in VRAM | 77.29 GiB | vLLM logs |
| Available KV cache | 94.58 GiB (2,065,744 tokens) | vLLM logs |
| VRAM peak | 176/191.7 GiB (92% utilization) | rocm-smi |
| `--max-model-len 262144` | started cleanly | vLLM logs + /v1/models |
| 32K context @ N=31 concurrency | **31/31 success** | bench_concurrency.json |
| 128K context @ N=31 | 25/31 success (6 timeouts) | bench_concurrency.json |
| 256K context @ N=8 | 6/8 success | bench_concurrency.json |
| Long-context needle 200K | **3/3 PASS** (early/middle/late) | bench_long_context.json |
| End-to-end repo Q&A | **9/9 correct** across 3 repos | bench_e2e.json |
| pytorch/vision (1.3M tokens) | priority-fitted to 180K, all 3 questions correct | bench_e2e.json |
| Cost / 1M completion tokens | $45.75 (32K aggregate) | bench_cost.json |
| Active queriers / MI300X | 14.5 (continuous), 70-140 (bursty) | derived from agg tps |

**Stream + Discord engagement**:
- Watched Steve Kimoi's "Build and Deploy AI App on AMD MI300X as a HF
  Space" Twitch workshop (lablabai, 7-9 PM CEST = 22:00-00:00 Tashkent)
- Established direct rapport with Steve in stream chat
- Read tutorial published earlier same day:
  https://lablab.ai/ai-tutorials/amd-huggingface-deployment-for-ai-hackathons
- Identified gap: tutorial mandates `amd-hackathon-2026` tag for
  discoverability — added to local README updates

**Public artifacts updated** (then **reverted** to keep verified data
local-only until submission):
- HF org Space (`lablab-ai-amd-developer-hackathon/repomind`):
  pushed verified update `3965a53` → reverted to pre-stress-test
  `f81271c` per user strategy decision
- HF personal Space (`ZeroR3/repomind`):
  pushed verified update `361d96d` → reverted to conservative-wording
  `53f2b06` per user strategy decision
- Local files updated and ready (will publish post-submission):
  README.md, hf_space/README.md, benchmarks/2026-05-05-mi300x-stress-test/

### Key decisions / hard-won lessons
- **Pre-submission discipline (NEW)**: any verified-numbers updates
  on public surfaces should be **reverted / deferred until AFTER
  lablab final submission**. Reasoning:
  1. Pre-submission leak reduces "wow factor" of submission's evidence
     pack
  2. Trickle-update creates confusing public timeline ("31x then 14,
     what's true?")
  3. Post-submission ONE coherent push tells the full story at once
- **vLLM concurrency nuance**: `Maximum concurrency: 31.08x` is for
  chunked-prefix-cache sharing of identical prompts. Per-user unique
  prompts at 256K saturate compute around N=8. Both numbers are real;
  marketing must specify the workload assumption.
- **Memory-architecture moat (F9) promoted from B-tier (math) to D-tier
  (measured)**: 77.29 GiB weights + 94.58 GiB KV cache + 92% VRAM
  utilization, all on real hardware. The architectural argument now
  has empirical foundation, not just first-principles math.
- **Long-context coherence is real**: 3/3 needle pass at 200K refutes
  the worry that "256K window" is allocated-but-not-usable.
- **Priority-aware chunking solves the "your repo is bigger than my
  context window" objection**: pytorch/vision (1.3M tokens) trimmed
  to 180K, all 3 questions answered correctly with file path citations.

### Cost so far
$3.22 spent of $100 credits = $96.78 remaining for demo recording +
optional LoRA + buffer.

### Artifacts
```
~/Desktop/
├── repomind_results.tar.gz                      2.2 MB raw archive
└── repomind_bench_runner.tar.gz                 16 KB scripts (re-deploy ready)

competitions/repomind/
├── README.md                                    ← verified data (LOCAL only)
├── hf_space/README.md                           ← verified data (LOCAL only)
├── benchmarks/2026-05-05-mi300x-stress-test/
│   ├── 5 JSON results
│   ├── 3 PNG plots (1280×720 dark theme, AMD red)
│   ├── e2e/  (15 files)
│   ├── rocm_smi_final.txt
│   └── run_log.txt
└── benchmarks/runner/                           ← 12 files (5 bench scripts + common + stub-server + plotter + run_all.sh + README + __init__)
```

### Public state at end of day
- HF org Space: `f81271c` (pre-stress-test smoke test status)
- HF personal Space: `53f2b06` (conservative wording + amd-hackathon-2026 tag)
- GitHub: unchanged (locally updated, not yet pushed)
- Discord: unmuted, intro posted, rapport with Steve established
- X / LinkedIn: Day-1 posts standing, no Day-2 update yet (deferred to
  post-submission wave)

---

---

## 2026-05-06 (Wed, early hours UTC) — Day 3: Extended + AITER A/B

### State at start of day
- Day 2 complete with full session-1 evidence pack local.
- Hakob_Arzumanyan (AMD Developer Community thread #505) replied with two
  open questions: (Q1) "30 tok/s at 8K feels slow — did you try vLLM
  tuning?" and (Q2) "concurrency at 8K-32K where most users live?"
- Decision: spin up second MI300X session, answer both empirically before
  recording demo + final lablab submit.
- Slides v1 (10 slides), POSTS_DRAFTS, SPEAKER_NOTES, DEMO_FLOW,
  LABLAB_STEP2_TEXT all drafted with session-1 numbers.

### What landed by end of session

**Session-2 droplet** (134.199.195.198, ATL1, fresh vLLM 0.17.1 + ROCm 7.2):
- 27 min wall clock, $0.90 incremental
- Two-phase benchmark suite via `run_extended.sh`:
  - PHASE 1: default Triton backend → 12 new concurrency cells (8K/16K/64K
    × {1,8,16,31}) + 3 hot throughput points
  - PHASE 2: `--attention-backend ROCM_AITER_FA` → same 12 cells + 32K
    A/B comparison at N={1,8,16}

**PHASE 1 — Extended default Triton**:
| Context | N=1 | N=8 | N=16 | N=31 success |
|---|---|---|---|---|
| 8K | 36.5 | 69.4 | 75.2 | 78.5 (31/31 ✅) |
| 16K | 21.2 | 30.2 | 30.9 | 31.4 (31/31 ✅) |
| 64K | 3.41 | 3.57 | 3.60 | 3.61 (31/31 ✅) |

Combined with session-1: **31/31 success at 8K, 16K, 32K, 64K** —
every realistic-developer context. Clean 24-cell matrix (144/144
outputs OK).

**PHASE 2 — AITER backend tuning attempt → measured regression**:
- Throughput 2-4× higher than default Triton (8K×31: 168 vs 78.5;
  64K×31: 18.5 vs 3.61)
- TTFT 2.8× faster at 64K hot (3.54s vs 10.01s)
- BUT **137 of 144 cells produced broken output** (repeating punctuation
  tokens, e.g. `!!!!!!!!!!`)
- Default Triton on same configuration: **0/144 broken**
- vLLM startup logs flag `q_scale` and `prob_scale` as uncalibrated
  for FP8 attention — likely the underlying cause
- **Conclusion: default Triton stays production-safe; AITER filed for
  AMD upstream investigation**

**Files added**:
```
benchmarks/2026-05-05-mi300x-stress-test/extended/
├── SUMMARY.md                                     full PHASE 1+2 narrative
└── benchmarks/results/
    ├── bench_throughput_hot_extended.json         PHASE 1 hot
    ├── bench_throughput_hot_aiter.json            PHASE 2 hot
    ├── bench_concurrency_realistic_extended.json  PHASE 1 concurrency
    ├── bench_concurrency_realistic_aiter.json     PHASE 2 same matrix
    ├── bench_concurrency_32k_aiter_compare.json   PHASE 2 32K A/B
    ├── rocm_smi_extended.txt + rocm_smi_aiter.txt
    └── run_extended.log + run_extended_aiter.log
```

**Local artifacts updated** (NOT pushed — pre-submission embargo holds):
- `slides/SLIDE_DECK.md` — added slide 7 "Tuning attempt: AITER regression",
  expanded slide 5 (throughput) and slide 6 (concurrency) tables to 6 contexts
- `slides/SLIDE_DECK.pdf|html|pptx` — re-rendered (now 11 slides)
- `slides/SPEAKER_NOTES.md` — re-numbered, added slide 7 narration (~30s)
- `slides/DEMO_FLOW.md` — added rollback-to-default-Triton step before recording
- `slides/POSTS_DRAFTS.md` — added AITER finding to X thread + LinkedIn + AMD Forum
- `slides/LABLAB_STEP2_TEXT.md` — long description updated with extended findings
- `slides/HAKOB_FOLLOWUP_REPLY.md` — new file, full data-rich follow-up reply ready
- `README.md` — extended throughput + concurrency tables, added AITER section
- (pending) plots refresh, hf_space/app.py Verified evidence tab,
  memory + knowledge files

### Key decisions / hard-won lessons
- **Tuning attempts are findings, not failures**: AITER regression is the
  most useful piece of session-2 data — it shows engineering discipline
  and gives AMD a concrete bug report. Worth a dedicated slide.
- **Conservative output validation**: every concurrency cell now checks
  output content shape (broken vs OK) in addition to HTTP success status.
  144 cells × character-set test caught the AITER regression that pure
  throughput numbers would have hidden.
- **SSH disconnect resilience**: `nohup bash ... & disown` + redirect to
  `/tmp/vllm.log` prevents losing the vLLM process when the SSH tunnel
  times out (which it did once during PHASE 1). Lesson applied for
  PHASE 2 from the start.
- **Demo prep matters**: discovered that the droplet must be ROLLED
  BACK to default Triton before recording, otherwise the live demo
  would produce `!!!!!!!!`. Added explicit rollback section to
  DEMO_FLOW.md with smoke-test curl.

### Cost so far
$3.22 (session 1) + $0.90 (session 2) = **$4.12 of $100 credits**.
$95.88 remaining for demo recording + optional LoRA + buffer.

### Public state at end of day-3 morning
- HF org Space: still `f81271c` (pre-stress-test)
- HF personal Space: still `53f2b06` (conservative wording)
- GitHub: still unchanged (locally updated, not yet pushed)
- AMD Forum: initial brief reply to Hakob already posted; full
  data-rich follow-up drafted in HAKOB_FOLLOWUP_REPLY.md, scheduled
  for after final submit lands
- Discord: quiet, no new posts (post-submission wave)
- X / LinkedIn: still on Day-1 posts (post-submission wave)

---

## What's next (post Day-3 plan)

### 2026-05-06 (later) to 2026-05-10 — Day 3-7

1. **Restart vLLM on droplet with default Triton** (rollback from AITER,
   ~3 min)
2. **Demo video recording** (3-5 min) against live MI300X backend with
   real Qwen3-Coder-Next inference + clean default-Triton output
   (~30-60 min, ~$2)
3. **Destroy droplet** after recording (5 min, $0)
4. **Re-render plots** with combined PHASE 1 + PHASE 2 data (local, free)
5. **Lablab Step 2 + 3 final submit** BEFORE 2026-05-11 00:00 Tashkent
6. **Post-submission ONE big push**: scripts + verified data + updated
   READMEs + plots → GitHub + both HF Spaces
7. **Build-in-public posts wave**: X + LinkedIn + AMD Forum thread #505
   (Hakob follow-up) + HF Discussions thread, all referencing verified
   numbers
8. **Optional**: LoRA fine-tune for Track 2 bonus (~$10 of remaining
   $95.88 credits)
9. **Optional**: file AITER regression upstream as vLLM/ROCm issue
   with full evidence pack attached

### 2026-05-11 00:00 Tashkent — DEADLINE

Final submission lands. Public reveal of verified evidence pack
synchronized with submission. Build-in-public wave amplifies.

### 2026-05-11 02:00+ Tashkent — Live judging

Pitch presentations on Twitch. If Sardor advances, present REPOMIND with
the verified evidence pack live.

---

## 2026-05-06 (Wed evening) — Day 3 evening: investor narrative + outreach playbook + judge-as-messenger pivot

### State at start of evening
- Day 3 morning: extended PHASE 1 + PHASE 2 stress test done, all 5 source-of-truth docs in place
  (MASTER_PITCH, MARKET_RESEARCH, IMPACT_RECALCULATIONS), 16 SVG slides + 6 banners (light theme,
  embedded base64 logos), Cap recordings (2 takes), screenshots captured (13 manual)
- vLLM logs pulled (3 files), droplet destroyed at $4.12 spend
- All ready for video edit + lablab final submit

### What landed by end of evening

**Strategic pivot — user revealed actual end goal:**
> "my aim is not just 1st place, is to make this project resonate in media globally so giants will
> try to buy me like Alexander Wang"

This reframed every artifact priority for Day 4-7. Not "winning the hackathon" → **"acqui-hire /
strategic talent positioning, with hackathon as the trigger event"**.

**New documents (positioned as Series-A grade):**
- **`INVESTOR_NARRATIVE.md`** — Wang/Suleyman/Shazeer comparable deal positioning. Pre-funding talent+IP+community range $10M-$100M, strategic acquirer (Meta/AMD/Anthropic/sovereign) range $100M-$500M. Comp deals: Wang $14.3B, Suleyman $650M, Shazeer $2.7B, Luan $400M+, Cursor $9B, Anthropic $40B, OpenAI $500B. 60-sec elevator pitch + email-to-a16z-partner template.
- **`OUTREACH_PLAYBOOK.md`** — 12 Tier-1 decision-makers with ready DM templates (Elon, Dario,
  Sam, Lisa Su, Mark Z, Sundar, Demis, Satya, Karpathy, Mira, Cursor founders, Junyang).
  5-tier execution ladder T+0 through T+2 months. Master X thread (6 tweets, pinned). Show HN
  submission. Press tip lines (TechCrunch, Information, Tom's, Phoronix, banking trades, defense
  trades, China/Asia tech press). Daily scoreboard with 20+ rows.

**Strategic frame established for slide redesign:**
Hackathon judges (Mahati Kumar Meta, Pavan Gondhi JPM, Mallika Rao Netflix, Suneeth Maraboina
Apple, Vasu Raj Jain Amazon, Ramine Roane AMD) are **not the final decision-makers** — they are
**forwarding agents to their own CEO/leadership**. Slides should be optimized for **fwd-ability**:
every slide gives the judge a 1-sentence headline they can text to their VP / CEO.

This is breakthrough #12 in memory/breakthroughs.md. Pattern is repeatable for any future
hackathon with big-company judges.

### Files added this session
- `INVESTOR_NARRATIVE.md` (~600 lines)
- `OUTREACH_PLAYBOOK.md` (~750 lines)
- (pending) `slide-17-judges-call-to-action.svg` — judges-as-messengers slide with per-judge fwd-able sound-bites

### Memory + knowledge updates this session
- `memory/competition_repomind.md` — added Day 3 evening narrative pivot section
- `memory/breakthroughs.md` — added #12 (judges as conduits), #13 (locked sub-market frame), #14 (solo founder + ship-in-days = acqui-hire magnet)
- `memory/feedback_lessons.md` — added 5 new rules (fwd-ability optimization, end-goal-reveal-early, ship-receipts-over-feature-lists, locked-sub-market positioning, demo recording smoke test)

### Cost so far
$4.12 spent of $100 credits. Day 3 evening session was 100% local document work — zero
incremental cost. Final spend trajectory: well under $20 of $100 by hackathon end.

### What's next (Day 4-7 plan, post-pivot)

1. **Demo video editing in CapCut** — assemble 16 SVG slides + 6 banners + 2 Cap recordings + voice-over from INVESTOR_NARRATIVE §9 60-sec pitch
2. **Build slide-17-judges-call-to-action.svg** — direct address to judges with per-judge fwd-able sound-bites
3. **Lablab Step 2/3 final submit** before 2026-05-11 00:00 Tashkent
4. **Step 3 confirmation = T+0** — trigger OUTREACH_PLAYBOOK execution
5. **Tier 1-2-3 outreach push** per OUTREACH_PLAYBOOK schedule
6. **Track success metrics** in daily scoreboard (X impressions, HN front page, DM reply rate, press coverage, GitHub stars)

### Public state at end of Day 3 evening
- All 5 source-of-truth docs locally written, embargoed until T+0
- 16 SVG slides + 6 banners locally rendered, ready for CapCut import
- Cap recordings (2 takes) saved in Cap library
- HF org Space + personal Space still on pre-stress-test commits (`f81271c` / `53f2b06`)
- GitHub: unchanged, all updates locally batched for one big post-submit push
- AMD Forum thread #505: Hakob's initial reply still standing, full data-rich follow-up drafted in `slides/HAKOB_FOLLOWUP_REPLY.md`
- X / LinkedIn: still on Day-1 posts; Day-3 evening narrative materials drafted but not published

---

## Total spend so far
$4.12 / $100 credits (4.1% used). Plenty of headroom for:
- Demo recording redo if needed (~$2)
- Optional LoRA fine-tune (~$10)
- Optional live MI300X during judging window (variable)

Total expected end-of-hackathon spend: $15-30 of $100. Stays well within budget.

---

## 2026-05-06 (late evening) — Day 3 → final asset bundle ready for submission

### State at start

- 19 SVG slides + 6 banners rendered, 1.36-min CapCut timeline shaping up
- VOICEOVER_SCRIPT.md still in 4:30 form
- captions.srt still in 4:40 form (75 captions)
- README.md / MASTER_PITCH.md / OUTREACH_PLAYBOOK.md had latest tech numbers but no fit-map / compliance keywords / new alt-email + LinkedIn

### What landed by end of evening

- **REPOMIND logo redesigned** — DAG mark (root + 3 children, one red active path). Semantics: code repo file-tree + neural graph + focused chunk. Replaces earlier bookmark-icon design.
- **All "JUDGES — forward to X" callouts removed** from slide-02 / 03 / 06 / 10 / 11a (replaced with neutral fact-only framing — readers connect dots themselves).
- **Slide-12 fully rebuilt** (header was truncated "6.49× faster on 8K context (78.5 tok"; metric values overlapped section labels). New: 3 sections × 4 metrics each, no overlap.
- **Slide-16 fully rebuilt** ("TIFT" visual / TTFT confusion + truncated descriptions). New: "TIME-TO-FIRST-TOKEN SCALING" header + descriptions wrap cleanly.
- **Slide-06 right column tightened** (red-badge approach reverted to clean text-only with proper vertical spacing — user read the badge background as "covering" text).
- **Slide-10 middle Claude screenshot fixed** (was letterboxed because portrait-aspect screenshot in landscape card with `xMidYMid meet`. Switched to `slice` for all 3 pricing cards, restored AMD logo to `meet`).
- **Closing-slide availability strip** — 3-line footer: availability statement / both emails + LinkedIn / handles. Same applied to slide-18-final-trigger and banner_closing.
- **CapCut bundle built** — `capcut_video/` folder with 23 numbered PNGs (`01_title.png` → `23_closing_banner.png`) + `CAPCUT_ORDER.md` with timeline timing.
- **VOICEOVER_SCRIPT.md compressed to 1:36** (5 segments, ~205 words at 140 wpm) for actual edited timeline. Original 4:30 version kept below for reference.
- **captions_1m36s.srt generated** — 32 captions synced to compressed voice-over.
- **REPOMIND_presentation.pdf** built (4.7 MB, 23 pages, 1920×1080) for lablab attachment / email decks.
- **BUILD_IN_PUBLIC_DRAFTS.md** drafted — 8 platform-specific copy blocks (X / LinkedIn / Show HN / r/LocalLLaMA / AMD Forum #505 reply / 3 Discord servers / 4 Tier-1 cold DMs) + cadence table (T+0 to T+72h).
- **README.md, MASTER_PITCH.md, OUTREACH_PLAYBOOK.md, INVESTOR_NARRATIVE.md** updated with full contact set (both emails + LinkedIn + availability statement). README also gained a "Where REPOMIND fits" section (6 enterprise contexts) + compliance keywords block (SR 11-7 / OCC / on-prem / air-gapped / audit-able).

### Memory updates

- `feedback_external_actions_permission.md` (NEW) — never push / post / DM / submit without explicit per-action permission. Local file ops are fine.

### Public state at end of Day 3 (late evening)

- GitHub `SRKRZ23/repomind` still **private** (will go public T+0 after lablab submission lands)
- HF Space not yet created
- YouTube not yet uploaded
- All build-in-public copy drafted but **nothing posted**
- Ready: video bundle (CapCut), PDF deck, contact-complete docs, 8 platform-specific posts queued behind explicit go-ahead

### What's next (Day 4-7)

1. CapCut export → 1080p MP4
2. YouTube upload (unlisted)
3. GitHub repo polish + go public
4. HuggingFace Space create + go public
5. lablab Step 3 submission (deadline 2026-05-11 00:00 Tashkent)
6. After submission lands: execute build-in-public cadence per BUILD_IN_PUBLIC_DRAFTS.md section H
