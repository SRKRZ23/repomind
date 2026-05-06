# CAPCUT IMPORT ORDER — REPOMIND video assembly

23 numbered PNGs are in this folder. Drag them into CapCut **in numeric order** and place each on the timeline at the time shown below. The screen recording + screenshot are inserted between #13 and #14.

---

## TIMELINE (4:30 total)

| # | File                          | On screen      | Duration | Voice-over (from `slides/VOICEOVER_SCRIPT.md`)            |
|---|-------------------------------|----------------|----------|------------------------------------------------------------|
| 01 | `01_title.png`               | 0:00 → 0:15    | 15 s     | SEG 0 (disclaimer 5 s) + SEG 1 (opening hook 10 s)         |
| 02 | `02_locked_market.png`       | 0:15 → 0:35    | 20 s     | SEG 2 (3M devs locked out)                                  |
| 03 | `03_architectural_moat.png`  | 0:35 → 0:55    | 20 s     | SEG 3 (AMD blog moat)                                       |
| 04 | `04_verified_kpis.png`       | 0:55 → 1:05    | 10 s     | SEG 4 first half (62 data points)                           |
| 05 | `05_cold_start.png`          | 1:05 → 1:10    | 5 s      | SEG 4 tail (3:30 cold start)                                |
| 06 | `06_throughput_physics.png`  | 1:10 → 1:18    | 8 s      | SEG 5 first (TTFT linear)                                   |
| 07 | `07_speed_ratios.png`        | 1:18 → 1:25    | 7 s      | SEG 5 tail (8K vs 256K)                                     |
| 08 | `08_hakob_question.png`      | 1:25 → 1:43    | 18 s     | SEG 6 (Hakob asked, we answered)                            |
| 09 | `09_hakob_649x_hero.png`     | 1:43 → 1:45    | 2 s flash| SEG 6 punctuation (6.49× hero number)                       |
| 10 | `10_aiter_honesty.png`       | 1:45 → 2:03    | 18 s     | SEG 7 first (AITER tried)                                   |
| 11 | `11_aiter_regression.png`    | 2:03 → 2:05    | 2 s flash| SEG 7 tail (gibberish, filed upstream)                      |
| 12 | `12_needle_200k.png`         | 2:05 → 2:20    | 15 s     | SEG 8 (200K needle pass)                                    |
| 13 | `13_repo_qa.png`             | 2:20 → 2:35    | 15 s     | SEG 9 (9/9 across 3 repos)                                  |
| ▶  | **YOUR_SCREEN_RECORDING.mp4**| 2:35 → 3:03    | 28.15 s  | SEG 10 first half (live demo VO)                            |
| ▶  | **YOUR_SCREENSHOT_1st_result + cropped overlay** | 3:03 → 3:10 | 6.86 s   | SEG 10 tail ("screenshot from alternate run")               |
| 14 | `14_business_case.png`       | 3:10 → 3:23    | 13 s     | SEG 11 first (Cursor / Claude / Copilot pricing)            |
| 15 | `15_business_banner.png`     | 3:23 → 3:25    | 2 s flash| SEG 11 punctuation (zero per-seat)                          |
| 16 | `16_stack_comparison.png`    | 3:25 → 3:30    | 5 s      | SEG 11 tail (stack comparison)                              |
| 17 | `17_meta_6b_deal.png`        | 3:30 → 3:45    | 15 s     | SEG 12 (Meta $6 B AMD deal)                                 |
| 18 | `18_real_evidence.png`       | 3:45 → 3:52    | 7 s      | SEG 13 first (primary sources flash)                        |
| 19 | `19_velocity_honesty.png`    | 3:52 → 3:58    | 6 s      | SEG 13 mid (6.5 days, $4.12)                                |
| 20 | `20_fit_map.png`             | 3:58 → 4:08    | 10 s     | SEG 13 tail (where it fits — 6 enterprise types)            |
| 21 | `21_pattern_table.png`       | 4:08 → 4:20    | 12 s     | SEG 14 (Wang / Suleyman / Shazeer comparable deals)         |
| 22 | `22_closing.png`             | 4:20 → 4:28    | 8 s      | SEG 15 first (Lisa Su quote + REPOMIND positioning)         |
| 23 | `23_closing_banner.png`      | 4:28 → 4:30    | 2 s      | SEG 15 final beat ("Thank you")                             |

**Total: 4:30 even.** All 19 slides + 4 banner flashes + your screen recording + screenshot.

---

## STEP-BY-STEP CAPCUT BUILD

1. **Create new CapCut project** at 1920×1080, 30 fps
2. **Drag PNGs 01–13** into the timeline, set each to its duration in the table above
3. **Drop your screen recording** (`YOUR_SCREEN_RECORDING.mp4`) right after #13, lasts 28.15 s
4. **Drop your screenshot** (with the cropped-detail overlay you already prepared) right after the recording, lasts 6.86 s
5. **Drag PNGs 14–23** into the timeline after the screenshot, set durations as in table
6. **Generate audio**: open CapCut **AI Voice → Cody (or Liam)**, paste each segment from `slides/VOICEOVER_SCRIPT.md` one at a time (SEG 0 through SEG 15), generate, drop the resulting MP3 onto the audio track at the segment start time
7. **Drop captions**: import `slides/captions.srt` onto the Subtitle track — CapCut will auto-place them
8. **Sound effects** (only on the demo segment, 2:35 → 3:10):
   - CapCut → Audio → Sound Effects → search "mouse click" and "keyboard typing"
   - Sprinkle 8–12 click/type events to match the on-screen actions
9. **Music bed**: CapCut → Audio → Music → pick subtle ambient / lo-fi / tech, drop on a separate audio track, set volume to **−25 dB**, enable "Auto-duck under voice"
10. **Export**: 1080p MP4, H.264, 30 fps, high bitrate (~16 Mbps for crisp text)

---

## NOTES

- The 2-second banner flashes (#09, #11, #15, #23) act as visual punctuation — they emphasize the punch of the surrounding voice-over. If a flash feels rushed, extend to 3 s and shorten the preceding slide by 1 s.
- All slides are 1920×1080 — drag straight in, no resize needed.
- If a voice-over segment ends slightly before the slot, hold the slide on screen until the next segment starts. CapCut handles this automatically when audio is shorter than video.
- The cropped-detail overlay on the screenshot (the part you said you added in editing) should be a separate clip stacked on top of the screenshot at 3:03 → 3:10, scaled to ~50 % of frame, positioned bottom-right.
