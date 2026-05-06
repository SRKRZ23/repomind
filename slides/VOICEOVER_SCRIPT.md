# REPOMIND — Voice-Over Script

> **TL;DR — Use the COMPRESSED 1:36 version below.** The original 4:30 version is kept further down for reference.

**Recommended TTS:** ttsmaker.com → English (US) — voice "Davis" (Male) or "Roger" (Male). Speed 1.0. Generate per segment, drop into CapCut audio track, align with corresponding video clip start.

---

## ⚡ COMPRESSED 1:36 VERSION — for the actual edited timeline

Total: **~96 seconds**, ~205 words at 140 wpm.

Five segments only. Generate one MP3 per segment. Align each MP3's start with the start of the matching video segment in the CapCut timeline.

### SEG 1 — Hook + locked market (≈15 sec) [0:00 → 0:15]

```
REPOMIND. Open-source repo-scale coding agent. Single AMD MI300X. Six and a half days. Four dollars of compute. Cursor, Claude, Copilot — all banned at JPMorgan, Apple, and the Department of Defense. Three million developers locked out.
```

### SEG 2 — Architectural moat + verified (≈18 sec) [0:15 → 0:33]

```
AMD's blog said two-fifty-six K context, single GPU, FP8 — possible. NVIDIA H100 cannot fit. AMD MI300X has the headroom. We shipped the open-source proof. Sixty-two verified data points across one hundred twenty-four minutes of stress testing. Ninety-two percent peak VRAM.
```

### SEG 3 — Hakob 6.49× + AITER honesty (≈22 sec) [0:33 → 0:55]

```
An AMD engineer asked publicly about concurrency. We measured. Six-point-four-nine times faster on eight K context than on thirty-two K. Then we tried AMD's AITER backend — throughput jumped four times, but output broke on FP8 KV cache. We filed the regression upstream. Default Triton stays production-safe. This is honest physics.
```

### SEG 4 — Live demo narration (≈28 sec) [0:55 → 1:23]

```
Watch live. Real MI300X. Real model. Real agent. I paste pallets-flask. Click ingest. Two seconds. Four hundred thousand tokens fitted to the window. Where is the WSGI request entry point? The agent reasons. Three grep calls. One read with explicit line range. It identifies __call__ at line one-six-one-eight, wsgi-app at one-five-six-six. Real multi-step reasoning on real hardware.
```

### SEG 5 — Business + availability close (≈13 sec) [1:23 → 1:36]

```
Cursor: forty dollars per seat per month, banned. REPOMIND: zero per-seat licensing. Eighteen-thousand-dollar MI300X capex pays back in three months at one hundred developers. I am Sardor Razikov. From Tashkent. Open to acquisition, founding-team, and strategic-partnership conversations.
```

---

## TTSmaker generation steps

1. Open https://ttsmaker.com
2. Language: English (US)
3. Voice: **Davis (Male)** — clean, tech-demo. Or **Roger (Male)** — deeper, more authoritative. Pick one and stay consistent.
4. Speed: **1.0** (or 1.05 if any segment runs ~1 sec long)
5. Paste SEG 1 → click "Convert to Speech" → "Download MP3" → save as `seg1.mp3`
6. Repeat for SEG 2, 3, 4, 5
7. In CapCut: drag all 5 MP3s onto an audio track (separate from the music track). Move each MP3 so its **start** aligns with the start of its target video clip.
8. Music bed (Action Music): keep it at **−25 dB** under voice. CapCut → select music clip → "Auto-duck under voice" if available, otherwise manual key-frame ducking.

## If a segment runs over its budget

- Don't speed up the voice (sounds robotic). Instead: trim the visible video clip to match, OR cut one sentence from the segment.
- Easiest cut targets: SEG 2 ("Ninety-two percent peak VRAM" → drop), SEG 3 ("This is honest physics" → drop), SEG 4 ("Real multi-step reasoning on real hardware" → drop).

---

## ORIGINAL 4:30 VERSION (reference only)

Below is the longer 15-segment version designed for a 4:30 video. Use only if you re-extend the timeline.

**Recommended CapCut AI voice:** "Cody" or "Liam" (clear US English, energetic-but-credible). Pace: 140 wpm. Slight pause after each sentence for SRT subtitle readability.

---

## SEGMENT-BY-SEGMENT SCRIPT

Copy each segment block into CapCut AI Voice. Generate audio per segment, then align on timeline.

### SEGMENT 0 — Disclaimer (5 sec) [0:00-0:05]

```
Disclaimer. This video uses real screen recording with mouse click and typing sounds added in editing. All numbers are verified. All sources are public.
```

---

### SEGMENT 1 — Opening hook (10 sec) [0:05-0:15]

```
REPOMIND. Open-source repo-scale coding agent. On a single AMD MI300X. Built solo, in six and a half days, for four dollars of compute.
```

---

### SEGMENT 2 — The locked market (20 sec) [0:15-0:35]

```
Three million developers locked out of AI coding tools. JP Morgan banned ChatGPT in 2023. Apple banned ChatGPT and Copilot. The Department of Defense needs AI coding for tens of thousands of developers, on-premise only. Cursor, nine billion. Anthropic, forty billion. OpenAI, five hundred billion. All blocked. That's a thirty billion dollar a year market that nobody currently serves.
```

---

### SEGMENT 3 — Architectural moat (20 sec) [0:35-0:55]

```
AMD's own February 2026 blog said the configuration exists. Two hundred fifty-six K context, single GPU, FP8 precision. NVIDIA H100, eighty gigabytes, cannot fit. AMD MI300X, one hundred ninety-two gigabytes, has the headroom. We shipped the open-source proof.
```

---

### SEGMENT 4 — Verified numbers (15 sec) [0:55-1:10]

```
Verified results. Seventy-seven gigabytes of model weights. Ninety-four gigabytes of KV cache. Ninety-two percent peak VRAM. Cold start in three minutes thirty seconds. vLLM startup in forty-two seconds. Sixty-two verified data points across one hundred twenty-four minutes of stress testing.
```

---

### SEGMENT 5 — Throughput physics (15 sec) [1:10-1:25]

```
Throughput across six contexts. TTFT linear in prompt size, exactly as theory predicts. Eight kilo: half a second. Sixty-four kilo: ten seconds. Two-fifty-six kilo: one minute fifty-eight. Honest physics. Honest numbers.
```

---

### SEGMENT 6 — The 6.49× hero (20 sec) [1:25-1:45]

```
This is the number nobody else had. An AMD engineer named Hakob asked publicly what concurrency looks like at eight K to thirty-two K. We measured. Six point four nine times faster on eight K context than on thirty-two K. Thirty-one of thirty-one users succeed at every realistic context. One hundred forty-four of one hundred forty-four outputs clean.
```

---

### SEGMENT 7 — AITER honesty (20 sec) [1:45-2:05]

```
We tried AMD's own AITER attention backend. Throughput went up two to four times. But output degraded to gibberish on one hundred thirty-seven of one hundred forty-four cells with FP8 KV cache. We filed it for AMD's ROCm team upstream. Default Triton stays production-safe. This is engineering honesty.
```

---

### SEGMENT 8 — 200K needle (15 sec) [2:05-2:20]

```
The two hundred fifty-six K window is usable, not just allocated. Three of three needle pass at two hundred thousand tokens. Model recovers planted facts from the deep middle of the prompt. Most claims are memory allocation. We proved attention.
```

---

### SEGMENT 9 — End-to-end Q&A (15 sec) [2:20-2:35]

```
Nine of nine repository questions answered correctly across three real repos. Including pytorch slash vision at one point three million tokens. Five times larger than the context window. Priority chunker fits to one hundred eighty K. Cursor sends fragments. We construct the right window.
```

---

### SEGMENT 10 — LIVE DEMO with screen recording (35 sec) [2:35-3:10]

**This segment narrates over the screen recording (28.15 sec) + screenshot overlay (6.86 sec).**

```
Let me show you live. Real MI300X. Real model. Real agent. I paste pallets slash flask. Click ingest. Two seconds, two thousand chunks, four hundred thousand tokens fitted to the window. Switch to ask. Where is the WSGI request entry point? Click ask. The agent reasons. Three grep calls. One read file with explicit line range. Five tool calls total in the first run, four in the second. Both runs identify the same code: __call__ method at line one six one eight, wsgi_app at one five six six. Real multi-step reasoning on real hardware. The screenshot you see now is from the alternate run. Both verified.
```

---

### SEGMENT 11 — Business case (20 sec) [3:10-3:30]

```
Real pricing, captured today. Cursor: forty dollars per seat per month. Claude: one hundred. Copilot: nineteen to thirty-nine. REPOMIND: zero per-seat licensing. Eighteen thousand dollar one-time MI300X capex breaks even versus Cursor in three to six months at one hundred developers. Code never leaves your VPC.
```

---

### SEGMENT 12 — Meta deal validation (15 sec) [3:30-3:45]

```
Mark Zuckerberg already signed six billion dollars with AMD in February twenty twenty-six. REPOMIND is the open-source proof he was missing. Fifty-eight million per year saved at thirty thousand Meta developers. Six hundred seventy-five million in productivity unlock at high end.
```

---

### SEGMENT 13 — Per-judge call (20 sec) [3:45-4:05]

```
Each judge sees a different REPOMIND. For AMD: the Lisa Su CES proof. For Meta: the six billion dollar deal validation. For JP Morgan: the LLM Suite next layer. For Apple iOS: the Copilot ban resolved. For Netflix: idle GPU hours turned into developer productivity. Be the one who flags this upstream first.
```

---

### SEGMENT 14 — The pattern (15 sec) [4:05-4:20]

```
Wang sold Scale AI to Meta for fourteen point three billion. Suleyman to Microsoft for six hundred fifty million. Shazeer to Google for two point seven billion. Solo founder plus strategic AI infrastructure equals multi-billion-dollar exits. The pattern moves fast.
```

---

### SEGMENT 15 — Closing (10 sec) [4:20-4:30]

```
I am Sardor Razikov. Top one point nine percent Kaggle. Top twenty-two percent AIMO three olympiad. From Tashkent. Six and a half days to ship. AMD made the hardware. We made the open-source unlock. Thank you.
```

---

## Total runtime: 4:30 (under 5-min cap)

## CapCut AI Voice generation tips

1. **Generate per segment**, not whole script at once — keeps quality high
2. **Voice consistency**: use the same voice for all segments
3. **Pause behavior**: CapCut AI inserts natural pauses at periods/commas
4. **Numbers**: spell out big numbers ("six point four nine times" not "6.49×") — the AI voice handles it cleaner
5. **Pronunciations to verify**: "Qwen" = "kwen", "MI300X" = "M-I-three-hundred-X", "TTFT" = "T-T-F-T", "WSGI" = "wis-gee" or spell out
6. **Sound design overlay**: CapCut > Audio > Sound Effects > "click", "keyboard typing", "notification" — sprinkle during demo segment
7. **Music bed**: subtle ambient tech/lo-fi at -25dB throughout, ducks under voice automatically

## Pause markers for editing

After each segment, insert ~0.5 sec silence in CapCut for SRT subtitle readability. Total scripted runtime + pauses = ~4:30.

---

## CAPCUT TIMELINE — ALL 19 SLIDES MAPPED TO VOICEOVER

The previous mapping skipped slide-12, 13, 14, 16. New mapping uses every slide as a visual cut, even if the same VO segment plays underneath.

| Time          | Slide(s) on screen                              | VO segment            |
|---------------|--------------------------------------------------|------------------------|
| 0:00 → 0:05   | slide-01-title                                   | SEG 0 (disclaimer)    |
| 0:05 → 0:15   | slide-01-title                                   | SEG 1 (opening)       |
| 0:15 → 0:35   | slide-02-problem                                 | SEG 2 (locked market) |
| 0:35 → 0:55   | slide-03-architectural-moat                      | SEG 3 (moat)          |
| 0:55 → 1:05   | slide-04-verified                                | SEG 4 (KPIs, 1st half)|
| 1:05 → 1:10   | slide-13-time-to-workload                        | SEG 4 (KPIs, 2nd half)|
| 1:10 → 1:18   | slide-05-throughput                              | SEG 5 (TTFT physics)  |
| 1:18 → 1:25   | slide-12-x-times-faster                          | SEG 5 (compression)   |
| 1:25 → 1:45   | slide-06-concurrency (+ banner_6_5x flash 2 sec) | SEG 6 (Hakob 6.49×)   |
| 1:45 → 2:05   | slide-07-aiter-tuning (+ banner_aiter flash 2s)  | SEG 7 (AITER honesty) |
| 2:05 → 2:20   | slide-08-needle                                  | SEG 8 (200K needle)   |
| 2:20 → 2:35   | slide-09-e2e-qa                                  | SEG 9 (Q&A)           |
| 2:35 → 3:03   | screen-recording (28.15 sec, raw)                | SEG 10 (live demo)    |
| 3:03 → 3:10   | screenshot 1st-result + cropped detail (6.86 s)  | SEG 10 (alt-run note) |
| 3:10 → 3:25   | slide-10-business-case                           | SEG 11 (pricing)      |
| 3:25 → 3:30   | slide-14-stack-comparison                        | SEG 11 (stack tail)   |
| 3:30 → 3:45   | slide-11a-meta-deal                              | SEG 12 (Meta $6B)     |
| 3:45 → 3:52   | slide-15-real-evidence                           | SEG 13 (sources flash)|
| 3:52 → 3:58   | slide-16-velocity-honesty                        | SEG 13 (velocity)     |
| 3:58 → 4:08   | slide-17-judges-call-to-action (FIT MAP)         | SEG 13 (fit summary)  |
| 4:08 → 4:20   | slide-18-final-trigger (pattern table)           | SEG 14 (the pattern)  |
| 4:20 → 4:30   | slide-11-closing (Lisa Su quote)                 | SEG 15 (closing)      |

**Total runtime: 4:30**, all 19 slides used at least once.

Banners (`banner_6_5x.png`, `banner_aiter.png`, `banner_business.png`, `banner_closing.png`, `banner.png`, `cover.png`) are short 1.5–2 sec emphasis flashes — not standalone scenes. Use them as transitions or as overlays during the matching VO segment if the cut feels static. They are optional; the 19 slides above cover the full story without them.

## Asset checklist for CapCut import

- [ ] `slides/svg_slides/slide-01-title.png` … `slide-18-final-trigger.png` (19 PNGs, 1920×1080)
- [ ] `assets/banner.png` + 5 themed banners (optional flash overlays)
- [ ] Screen recording (28.15 sec) — your raw clip
- [ ] Screenshot 1st-result + cropped detail (6.86 sec) — already prepared
- [ ] 15 voice-over MP3s from CapCut AI Voice (one per segment, generated from text above)
- [ ] `slides/captions.srt` — 75 captions, drag onto Subtitle track
- [ ] Click / keyboard SFX (CapCut built-in) — only on demo segment
- [ ] Music bed at −25 dB (ambient / tech / lo-fi)
