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

---

## 2026-05-06 (night) — Day 4: lablab submission landed + Phase C launch wave

### Submission landed at T+0

- Lablab project page live: https://lablab.ai/ai-hackathons/amd-developer/repomind/repomind
- Submitted 5 days before deadline (deadline 2026-05-11 00:00 Tashkent)
- Step 1 (Basic Info): final Short Description (236 chars) + Long Description (1978 chars), 4 build-in-public link slots filled (X status URL + LinkedIn post URL + AMD Forum #505 + HF Discussion #5), AMD Cloud feedback section filled with WINS / FRICTION / OVERALL structure
- Step 3 (Application): GitHub MIT repo + HF Space (org-judged for HF Special Prize) + Demo Application Platform = Hugging Face + Additional Information field with full evidence-pack pointers (demo video + presentation PDF + benchmarks tree + key metrics + author bio + contact set)

### YouTube channel + video assets
- Channel **@REPOMIND_SR** customized: banner 2048×1152, profile 800×800, watermark 150×150 (transparent + outlined), name REPOMIND, description (English + 6 inline links), 5 channel-level Links (GitHub / HF Live Demo / AMD Hackathon / LinkedIn / X), business email `razikovsardor1@gmail.com`
- Video **REPOMIND: 256K-context coding agent on a single AMD MI300X (open source, MIT)** — 1:38 length, 88-char title, custom thumbnail 1280×720 (REPOMIND wordmark + "256K context · FP8" red headline + open-source/MIT/github footer), category Science & Technology, allow embedding ✓, public visibility, Content ID claim noted (CapCut "Final Chance For Glory" track — informational only, no restrictions)
- URL: https://youtu.be/BvSBR1QazLU

### Phase C posting log (T+0 → T+3 hours)

| T+ | Platform | Status / URL |
|---|---|---|
| T+0 | Lablab Step 3 final submit | Live ✅ — https://lablab.ai/ai-hackathons/amd-developer/repomind/repomind |
| T+0 | YouTube video Public | Live ✅ — https://youtu.be/BvSBR1QazLU |
| T+0 | X main thread (10 tweets) | Live ✅ |
| T+1 | LinkedIn long-form launch post | Live ✅ — https://www.linkedin.com/posts/sardor-razikov-569a5327b_repomind-256k-context-coding-agent-on-a-share-7457817182069096449-GAP0 |
| T+2 | AMD Developer Community Forum thread #505 reply to Hakob_Arzumanyan | Live ✅ — `HAKOB_FOLLOWUP_REPLY.md` content posted verbatim. Thread state at posting: 16 views, 4-min read time. Forum auto-embedded GitHub stress-test folder URL as rich card. |
| T+3 | HuggingFace Discussion #5 (Qwen3-Coder-Next-FP8 page) follow-up | Live ✅ — final "submission landed" reply with full verified results + Qwen team thanks |

### Discord status: 🔴 lablab Discord re-muted (2026-05-06 ~22:23 Tashkent)

Posting REPOMIND submission announcement to lablab.ai Discord `#general-chat-amd-hackathon` triggered auto-mod (4 URLs in single message: lablab + HF + YouTube + GitHub). Message blocked (visible only to author with red ⛔ banner) and 7-day timeout applied — second time this happened (first was 4 May, lifted by Steve Kimoi via email on 5 May).

Mitigation in progress: email Steve Kimoi again requesting unmute. New skill saved to memory: `feedback_lablab_discord_automod.md` — split posts into text-only + links-reply to avoid threshold.

### Pending Phase C (T+4 onward)

- AMD ROCm Discord post (independent of lablab unmute)
- HuggingFace Discord #showcase post
- Anthropic Builders Discord #projects post
- Telegram Stories RU + EN (3 slides each, bio updated to HF Space URL)
- Facebook RU + EN long-form posts
- Hacker News Show HN (target peak Tuesday 9 AM EST = ~22:00 Tashkent)
- Reddit r/LocalLLaMA submission
- Tier-1 cold DMs (12 decision-makers + 5 lablab judges + 2 HF leadership) — order: Junyang Lin → Lisa Su → Karpathy → Mahati Kumar → Mira Murati → Cursor founders → Demis → Sundar → Sam → Satya → Mark Z → Elon → Dario. Pacing: 1-2 per hour, watch read receipts, escalate only on positive signal.

### New skills saved to memory (this session)

- `feedback_phase_c_outreach.md` — Build-in-public launch playbook (T+0 to T+72h cadence + community-thread-reply > broadcast + pace Tier-1 DMs)
- `feedback_lablab_discord_automod.md` — lablab Discord auto-mod 3+ URL spam threshold + workaround
- `feedback_hf_space_iframe_links.md` — HF Space Gradio iframe sandbox breaks markdown links; fix with gr.HTML + `<a target="_blank" rel="noopener noreferrer">`

### Public state at end of Day 4 (night)

- All major artifacts public and submitted
- 6 of ~14 Phase C platforms posted with measured cadence
- AMD Forum thread #505 = highest-leverage single act, awaiting Hakob_Arzumanyan re-engagement signal
- Tier-1 outreach queued, paced sequentially starting Day 5

---

## 2026-05-07 (Day 5) — Plan re-sequenced + first inbound traction signals

### Why a new plan was written

Original OUTREACH_PLAYBOOK assumed 72h of continuous focus from T+0. Reality at T+30h: PlantCLEF 2026 Kaggle parallel deadline (2026-05-08 02:59 Tashkent), missed HN-Tuesday window, lablab Discord still muted. Original cadence collapsed.

New plan saved at `/Users/sardorrazikov1/.claude/plans/while-we-wait-lets-spicy-wombat.md`:
- Phase 1 (now → T+55h): light touch only (X tweet #11 self-reply with traction metrics), then silent during PlantCLEF crunch
- Phase 2 (T+55h → T+101h): sleep, README polish, **Show HN at Friday 2026-05-08 17:00 Tashkent** (= 09:00 EDT, 2nd-best HN window after Tuesday), Reddit r/LocalLLaMA, **Tier-1 DM batch #1 at T+85h** (Junyang Lin → Karpathy → Lisa Su via LinkedIn, sequential 2h gaps), Phoronix tip, 3 safe Discords (skip lablab Discord — still muted)
- Phase 3 (T+96h → T+1week): decision-gated, see 3 measurable checkpoints in plan file

OUTREACH_PLAYBOOK.md was edited inline to add HOLD/GO/SKIP markers per Tier-1 entry (prevents accidental fire-DMs-tonight while sleep-deprived).

### Inbound traction signals (T+30h → T+38h)

- **lablab.ai (15,381 LinkedIn followers, OFFICIAL account)** publicly commented on Sardor's launch post: "REPOMIND isn't just a hackathon project - it's a serious technical argument for a $30B market that SaaS AI coding tools legally cannot touch... **One of the standout submissions of this hackathon. Sardor, the community needs to see this!**" — strongest tier of lablab comment (with explicit amplification ask)
- **Stephen Kimoi (lablab DevRel)**: "All the best 🙌 Sardor Razikov" — same Stephen who lifted Sardor's Discord mute twice; real ally
- **Kevin Brkal (3rd-degree, marketing builder)**: "this is legitimately impressive work under those constraints"
- **X comment from anonymous user** asking technical question: "MI300X for repo-scale at $4 of compute hits a real gap. What inference framework underneath - vLLM, SGLang, or custom?"

Sardor replied to all 4 (lablab.ai with thoughtful "Zenodo preprint coming" hook, Kevin warmly, Stephen with Discord-unmute gratitude, X comment with vLLM 0.17.1 + ROCm 7.2 + AITER A/B + benchmarks repro link).

### Strategic implications

- **Tier-1 DM HOLD gate partially open** — lablab official endorsement = traction signal for Friday HN opener and DM social proof
- **HN Friday opener** can lead with lablab quote: "Lablab.ai (the hackathon host) just publicly called this 'one of the standout submissions ... the community needs to see this' — sharing here for the HN crowd."
- **Junyang/Karpathy/Lisa Su DMs** can use lablab quote as warm-context opener (3-5× higher reply rate than cold)
- Must **calibrate**: lablab.ai gives substantive comments to multiple good projects, not just standout ones (saw evidence on Anum's project, AeroFlux, etc.). REPOMIND comment is in the strongest tier but not cosmically unique. Use as +1 amplification, not as singling-out.

### Memory updates from this day

5 new feedback files saved:
- `feedback_kaggle_new_token_system.md` — Kaggle deprecated kaggle.json; use `~/.kaggle/access_token` (KGAT_*) instead. Old format = silent 401.
- `feedback_macro_f1_per_sample.md` — In multi-label F1-per-sample with sparse GT, precision >> recall. Validate prediction count distribution before submit. (PlantCLEF v2 validated this at -0.077 F1 cost.)
- `feedback_amd_droplet_scratch_wipe.md` — DigitalOcean MI300X 1-Click /scratch (5 TB) wipes on reboot. Plan re-setup each session.
- `feedback_csv_ensemble_diminishing_returns.md` — CSV blending of similar pipelines (same backbone) doesn't improve F1. Real diversity = different models or score-level fusion of cached scores.
- `feedback_lablab_endorsement_calibration.md` — Lablab.ai LinkedIn comments substantive but not unique. +1 amplification voice, not magic ticket.

`competition_repomind.md` and `competition_plantclef2026.md` memory entries updated with current state.

### Public state at end of Day 5 (early morning Tashkent, before sleep)

- ✅ X tweet #11 self-reply posted with 24h metrics + Zenodo preprint plant
- ✅ X reply to vLLM technical question with version specifics + AITER A/B
- ✅ LinkedIn replies to lablab.ai + Stephen Kimoi + Kevin Brkal
- ✅ X main thread pinned to profile
- ✅ Calendar reminder set for 2026-05-08 14:00 Tashkent (REPOMIND HN re-launch prep)
- ✅ AMD MI300X droplet destroyed (saving ~$12 of credits during 6h sleep)
- 🛌 Sleep window 2026-05-07 ~02:30 Tashkent → ~08:30 Tashkent
- 🌅 Tomorrow morning: PlantCLEF 5/5 fresh submits sprint until 02:59 Tashkent deadline, then REPOMIND HN at 17:00 Tashkent

### What's next (Day 6, 2026-05-07/08)

1. ~05:00 Tashkent: PlantCLEF Kaggle reset → fresh 5 submits available
2. Re-launch MI300X droplet (~10 min setup, /scratch wiped from yesterday)
3. Re-run v3 inference (~30 min, regenerates cache for instant threshold sweeps)
4. Run v4 (only_classifier model variant, ~17 min, real architectural diversity)
5. Recompute v3 with looser threshold from cache (~1 min) — multiple variants
6. Build score-level ensembles using cached pipeline outputs (NOT CSV-level)
7. Submit best 3-5 by 02:00 May 8 Tashkent
8. Final 5 selection at 02:59 deadline
9. 14:00 Tashkent: README polish for HN
10. 17:00 Tashkent: Show HN goes live with lablab quote opener
11. Sequential Tier-1 DM batch #1 at 17:00 + 2h + 4h (Junyang → Karpathy → Lisa Su)

---

## 2026-05-08 (Day 6) — Hakob 3rd reply + PlantCLEF finals locked + CITADEL pivot

### Hakob 3rd reply on AMD Forum #505 (~00:00 Tashkent)

After Sardor's data-rich reply on 2026-05-06 with verified stress-test numbers, Hakob_Arzumanyan returned for the third time in 2 days:

> "Hi, thanks alot for your answer, i appreciate the time you have put into getting those numbers out. These totally answer my questions. I am amazed to see 31/31 success at 8k. Also on full 24-cell matrix it is pretty good results, thanks alot for sharing with us."

Tone: warm, satisfied, natural close-out. Specific praise for 8K all-pass and 24-cell matrix. AMD relationship visibly warming.

### Sardor's 4th-turn reply posted ~01:00 Tashkent

Crafted to: (a) acknowledge Hakob's specific points (8K all-pass, marginal cells 32K+), (b) demonstrate research integrity by flagging where rigor is still owed, (c) seed next direction without ask, (d) plant ECB Zenodo DOI as authority signal.

Reply text posted verbatim:
```
Thanks Hakob — glad the data closed the loop. The 8K all-pass was the
cleanest signal; on the 24-cell matrix the marginal cells (32K+ at high
concurrency) are where I want to do more rigorous evaluation next.

Next direction I'm exploring: public benchmarking on MI300X comparing
frontier models (Gemma 4, Llama 4, Qwen3 family) on calibration and
multilingual fairness, using the methodology I published at
https://doi.org/10.5281/zenodo.19791329 (Epistemic Curie Benchmark).
MI300X 192GB makes single-node multi-model comparison tractable in a
way H100 80GB can't — that's the angle I find most useful for the
ROCm ecosystem story.

Will share concrete results when ready.

— Sardor
```

This reply functions as **soft preview of CITADEL** without naming it. When CITADEL launches ~2026-05-19, Hakob will not be surprised — he's already seen the direction signaled.

### PlantCLEF 2026 finals locked (~01:00 Tashkent, T-2h to deadline)

After exhausted reality check at 00:30+ Tashkent, decision made: do NOT relaunch droplet for Day 2 sprint. Lock finals from Day 1 results:

✅ submission_v3.csv (0.31580 public) — best, anchor
✅ submission_v1.csv (0.30305 public) — architectural diversity hedge

Reasoning: 2.5h budget to deadline insufficient for safe MI300X relaunch + reliable submit cycle; sleep-deprived founder (30+h) = poor quality decisions; v3 strongest already verified; CSV ensembles validated as diminishing returns Day 1 (E3 0.305 < v3 0.315). Per `feedback_kaggle_imbalance.md`: 11% public sample = high private LB volatility, v1+v3 hedge mathematically sound.

Public rank at deadline: #34. Private LB reveal expected ~05:00-08:00 Tashkent on 2026-05-08.

### Gemma 4 Good Hackathon strategy session (~22:00 May 7 → 01:30 May 8)

3.5h strategic planning session for next hackathon (Gemma 4 Good, deadline 2026-05-19, $200K prize pool). Generated 35+ project concepts across multiple iterations. Final concept selected: **CITADEL** — open eval infrastructure extending ECB methodology to canonical multi-model, multi-task, multi-lingual, multi-hardware framework.

Key strategic insights captured to memory:

1. **Positive-sum infrastructure beats zero-sum competition** for billion-dollar acquirer trigger (`feedback_positive_sum_acquirer_pattern.md`). Stripe/Plaid/Cloudflare model: every player benefits, none threatened, multiple acquirers compete defensively. Mapped 15 acquirer scenarios for CITADEL: HuggingFace, Scale AI, AMD, NVIDIA, Anthropic, Google DeepMind, OpenAI, Microsoft, Meta, Cohere, Datadog, Mistral, Snowflake, Databricks, Oracle. Realistic ceiling 12-18 months: $500M-2B acquihire.

2. **Brainstorm diminishing returns past ~30 concepts** (`feedback_brainstorm_diminishing_returns.md`). Top-3 candidates emerged after round 2; rounds 3-4 produced reskins that didn't beat top-3. User asked verbatim brainstorm prompt 4 times — wingman should detect this and redirect to decision/criteria, not generate round 5.

3. **Solo + 11d hackathon submission ≠ $1B trigger.** Realistic max from hackathon alone: $5-50M acquihire signal in 30-90 days. $500M+ requires 12-18 months focused post-hackathon execution. Don't promise unrealistic timelines; design for trajectory.

4. **AMD compounding strategy:** Hakob warming + AMD Forum thread momentum + soft CITADEL preview seeded = AMD CES 2027 case study mention path = high probability. Lisa Su keynote-quotable: "indie founder built canonical AI eval on MI300X."

### Memory writes (this day)

New files:
- `competition_gemma4good.md` — full CITADEL strategic playbook (12-layer architecture vision, 11-day MVP scope, 15 acquirer scenarios, hero video script outline, AMD compounding plan, backup pool of 35+ alternatives)
- `feedback_positive_sum_acquirer_pattern.md` — Stripe/Plaid/Cloudflare neutral infrastructure framework
- `feedback_brainstorm_diminishing_returns.md` — wingman detection + redirect rule

Updates:
- `competition_repomind.md` — Day 6 status, Hakob 3rd reply context, CITADEL pivot for Phase D
- `competition_plantclef2026.md` — Day 2 superseded (no relaunch), finals locked, awaiting private LB
- `MEMORY.md` — index updated with 3 new entries

### Tonight (2026-05-08 ~01:30 Tashkent)

Sleep window opens. PlantCLEF deadline auto-passes 02:59 Tashkent (no action needed). Wake target: ~07:30-08:00 Tashkent.

### Tomorrow (2026-05-08 8 AM onward)

| Time Tashkent | Activity |
|---|---|
| 07:30-08:00 | Wake |
| 08:00-09:00 | Coffee + check PlantCLEF private LB |
| 09:00-10:00 | Pin Hakob reply timing (post Hakob reply at 17:00 alongside HN — already posted, this is monitoring) |
| 10:00-13:00 | README polish + HN copy final pass + draft 5 likely HN comment responses |
| 13:00-16:30 | Light recovery + final HN prep |
| **17:00** | **REPOMIND Show HN goes LIVE** with lablab quote opener |
| 17:00-21:00 | Founder-on-keyboard for HN — every comment <5 min response |
| 21:00 | Sleep |

### What's next (Day 7+, 2026-05-09 onward)

1. 2026-05-09 morning: assess HN outcome (Gate 2 per spicy-wombat plan)
2. 2026-05-09 ~09:00 Tashkent: Tier-1 DM batch #1 (Junyang Lin → Karpathy → Lisa Su, sequential 2h gaps)
3. 2026-05-09 afternoon: REPOMIND aftermath monitoring + light CITADEL architecture sketch (paper only, no code)
4. 2026-05-10: CITADEL Day 1 of 11-day build — repo setup, AMD MI300X compute access, architecture commit
5. 2026-05-11 to 2026-05-19: CITADEL execution per day-by-day plan in `competition_gemma4good.md`
6. 2026-05-19 04:59 GMT+5: CITADEL submit

---

## 2026-05-08 17:00-17:50 Tashkent — HN launch outcome

### Submission landed but flagged

**HN URL:** https://news.ycombinator.com/item?id=48061853

Show HN was restricted ("temporarily restricting Show HNs because of a massive influx") for new account `sardor_r1`. Pivoted to regular submission — accepted.

**Title posted:** "Repomind – 256K context coding agent on a single AMD MI300X (FP8)"

**First comment (T+0)** included lablab endorsement quote + bullet-stat walls + "happy to answer" closer. Got **[flagged]** within 30 minutes. Edit to cleaner technical version did not remove flag (HN flags are sticky once applied).

**Second comment (T+44 min)** with technical AITER regression question — clean, not flagged, no organic responses yet.

**Final state at T+48 min:** 2 points, 2 comments (both Sardor's), buried on page 2-3 of /newest. **Front page not reached.**

### Channel post-mortem

| Channel | Result | Time invested |
|---|---|---|
| HN | ⚠️ Flagged, 2 points | 5 min submit + 10 min monitoring |
| Reddit r/LocalLLaMA | 💀 Auto-filtered (new account + multi-link) | 10 min including modmail consideration |
| AMD Discord #project-showcase | 💀 Role-gated (AI Developer Program role required, multi-day approval) | 5 min navigation |
| AMD Discord #ai-dev-general | 💀 Same role gate | 1 min |
| Lablab Discord | 💀 Server-wide mute (5d 4h remaining) | 0 min (skipped per memory) |
| HF Discord, Anthropic Builders | 💀 Not pre-joined; can't post in launch window | 0 min (skipped) |
| X (own pinned thread reply) | ✅ Posted | 1 min |
| LinkedIn (under launch post) | ✅ Posted | 1 min |

**Net:** 3 channels truly active (HN + X + LinkedIn), 5 channels blocked, ~30 min total launch window spent including channel-blocked exploration time.

### PlantCLEF final result (parallel)

Private LB: **#33 of 371** (improved 1 position from #34 public). Methodology (v3 vegetation mask + KMeans cluster priors) validated; no shake-up.

### Lessons saved to memory

Two new feedback files:
- `feedback_hn_launch_traps.md` — name-dropping endorsements, bullet-stat walls, founder bio openers, "happy to answer" closers all trigger HN flags. Technical question opener + bug-story angle + in-narrative numbers survive.
- `feedback_launch_channel_constraints.md` — new accounts blocked on Reddit (auto-filter), Discord (role-gates), HN (low karma). Pre-audit channels 1+ week before launch; expect 50% of cold channels to block first post.

Updates:
- `competition_repomind.md` — Day 6 final state (HN flagged, plan B for Tuesday)
- `competition_plantclef2026.md` — private LB #33 final, competition closed
- `MEMORY.md` — index with 2 new feedback entries

### Plan B — Tuesday 2026-05-12 19:00 Tashkent (09:00 EDT)

HN re-submission with bug-story angle:
- New title: "AITER FP8 attention backend regression on MI300X: 2-4x throughput, 137/144 broken outputs"
- Same URL: github.com/SRKRZ23/repomind
- Pure technical bug-story = HN-bait, no marketing tone
- Tuesday 09:00 EDT = best HN window of the week

### Sardor's energy state

After this launch attempt + 30+h sleep deprivation prior days + no front-page outcome — high risk of burnout if pushes into CITADEL build tonight. Memory plan is: rest tonight, recovery Saturday, Tier-1 DMs Saturday afternoon (Junyang/Karpathy/Lisa Su), Tuesday HN Plan B, Sunday-Monday architecture sketch on paper, Wednesday-following Sunday CITADEL code build.

---

## Project rename: PROMETHEUS → CITADEL (2026-05-08)

The next-hackathon concept (open eval infrastructure for AI ecosystem, extension of ECB methodology) was named **PROMETHEUS** throughout 2026-05-07/08 brainstorm sessions. On 2026-05-08, Sardor renamed it to **CITADEL** — concept unchanged, name preferred.

All references in this file (above) were retroactively updated to use **CITADEL** in place of **PROMETHEUS**.

A separate, earlier-explored concept called "CITADEL ULTRA" (12-layer sovereign-AI-deployment infrastructure) was rejected during brainstorm and is no longer active. The CITADEL name now refers exclusively to the eval-framework project being built for Gemma 4 Good Hackathon.

See `competition_gemma4good.md` for full CITADEL strategic playbook.

---

## 2026-05-08 ~18:00 Tashkent — CITADEL scope decision: full 12-layer unified vision

After memory rename PROMETHEUS → CITADEL, Sardor made strategic decision: **merge eval-framework concept with original sovereign-deployment 12-layer vision**. Ship all 12 layers fully built, tested, benchmarked.

Combined positioning: **"open infrastructure for AI ecosystem trust — deploy anywhere, benchmark transparently, audit cryptographically, prove compliance."**

12-layer architecture:
- Layers 0-1: Network/security + hardware abstraction (foundation)
- Layers 2-4: Task suites + model adapters + metrics (eval core)
- Layers 5-7: Eval infrastructure + dashboard + cryptographic audit (eval shipping surface)
- Layers 8-9: Multi-cloud arbitrage + federated learning (deployment expansion)
- Layers 10-12: Regulatory translator + intelligent router + AI marketplace (ecosystem)

11-day shipping plan (per `competition_gemma4good.md`):
- Layers 0-7 production-grade with integration tests
- Layers 8-12 stub-quality with reference implementations / detailed RFCs
- Hero video showcases full vision, demos Layers 1-7 working

Acquihire ceiling lifted: $500M-2B (eval-only) → $1-3B realistic / $5B moonshot (full 12-layer vision).

Sardor confirmed: build, test, benchmark all 12 layers — full vision, not narrow MVP.

After this scope decision, Sardor announced new fast task to follow (TBD).
