# External Assets — Manual Download Checklist

What I downloaded automatically (Wikimedia Commons, CC-licensed) ✅ vs. what you need to grab manually (copyrighted news headlines, AMD press kit images, screenshots of pricing pages).

---

## ✅ Already downloaded (20 logos + 2 photos)

```
assets/external/logos/        — 20 PNG, all CC-licensed via Wikimedia Commons
  amd.png         apple.png        meta.png        netflix.png
  nvidia.png      jpm.png          huggingface.png lockheed.png
  pfizer.png      microsoft.png    google.png      openai.png
  aws.png         github.png       anthropic.png   alibabacloud.png
  chatgpt.png     cursor.png       claude.png      copilot.png

assets/external/photos/       — 2 photos, CC-licensed
  lisa_su.jpg     (Lisa Su SXSW 2024 portrait, ~88 KB)
  amd_mi325x.jpg  (AMD MI325X chip from CES reveal, ~5 MB — closest to MI300X)
```

---

## ⏳ You need to grab manually (copyrighted material — fair use for hackathon presentation OK with attribution)

### 1. News headline screenshots (4 needed)

For each: open the URL in browser → take screenshot of the headline + first paragraph → save as PNG.

| File to save as | URL to open | What to capture |
|---|---|---|
| `screenshots/cnn_jpm_ban.png` | https://www.cnn.com/2023/02/22/tech/jpmorgan-chatgpt-employees | CNN headline + dateline + lede paragraph |
| `screenshots/bloomberg_jpm_ban.png` | https://www.bloomberg.com/news/articles/2023-02-22/jpmorgan-clamps-down-on-staff-s-use-of-ai-powered-chatgpt-bot | Bloomberg headline (paywalled, may need archive.org) |
| `screenshots/macrumors_apple_ban.png` | https://www.macrumors.com/2023/05/19/apple-bans-employees-from-using-chatgpt/ | MacRumors headline + image |
| `screenshots/defensescoop_dod.png` | https://defensescoop.com/2026/02/26/dod-wants-ai-enabled-coding-tools-for-developer-workforce/ | DefenseScoop headline + first paragraph |

**Why fair use OK:** Educational / commentary / criticism use of small portions of news articles for hackathon presentation = textbook fair use under §107 of US Copyright Act. Always show source URL on screen via caption.

### 2. AMD official sources (2 needed)

| File to save as | URL to open | What to capture |
|---|---|---|
| `screenshots/amd_blog_quote.png` | https://www.amd.com/en/developer/resources/technical-articles/2026/day-0-support-for-qwen3-coder-next-on-amd-instinct-gpus.html | Top of blog page with the "Users can serve the full 256k context length on a single GPU using FP8 precision" quote highlighted |
| `screenshots/amd_meta_deal.png` | https://www.amd.com/en/newsroom/press-releases/2026-2-24-amd-and-meta-announce-expanded-strategic-partnersh.html | AMD-Meta partnership headline + Lisa Su quote |

### 3. Pricing pages (3 needed)

Open each, screenshot the relevant tier highlighted with cursor or annotation:

| File to save as | URL | Highlight |
|---|---|---|
| `screenshots/cursor_pricing.png` | https://cursor.com/pricing | Business $40/seat/mo |
| `screenshots/claude_pricing.png` | https://claude.com/pricing | Max 5x $100/mo |
| `screenshots/copilot_pricing.png` | https://github.com/features/copilot/plans | Business $19, Enterprise $39 |

### 4. Hakob's AMD Forum thread (1 needed)

| File to save as | URL | Capture |
|---|---|---|
| `screenshots/hakob_forum.png` | AMD Developer Community thread #505 (you have access) | Hakob's reply with question about "30 tok/s at 8K" + "8K-32K concurrency" |

### 5. Qwen Hugging Face model card (1 needed)

| File to save as | URL | Capture |
|---|---|---|
| `screenshots/qwen_model_card.png` | https://huggingface.co/Qwen/Qwen3-Coder-Next-FP8 | Top of model card showing 80B parameters / 3B active / 262K context |

### 6. Lisa Su CES 2026 keynote photo (optional but powerful)

If you want a more recent Lisa Su photo (the SXSW 2024 one we have is fine but CES 2026 is more on-brand):

| File to save as | Source | How |
|---|---|---|
| `photos/lisa_su_ces2026.jpg` | Google Images: search `"Lisa Su CES 2026 keynote site:reuters.com OR site:apnews.com OR site:amd.com"` | Filter by "Labeled for reuse" → save photo from AP, Reuters, or AMD official |

### 7. AMD MI300X official product photo (optional)

Wikimedia only has MI325X reveal frame. For MI300X official:

- Browse to https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html
- Right-click → Save Image → save as `photos/amd_mi300x.png`

### 8. Background music (optional, for video)

| Source | What to grab | License |
|---|---|---|
| https://studio.youtube.com/channel/UC.../music | Browse YouTube Audio Library → "Tech / Corporate / Cinematic" | Free, no attribution needed |
| https://freemusicarchive.org/genre/Electronic | Filter by Creative Commons | Attribution required (add to video credits) |
| https://incompetech.com/music/royalty-free/ | Kevin MacLeod free royalty-free | Attribution required |

Recommended track style: ambient tech / minimal piano / lo-fi electronic. NOT epic orchestral.

---

## License attribution for downloaded Wikimedia assets

When you publish the video, add a small credit line at the end (like in the closing card or video description):

> Logos and Lisa Su portrait courtesy of Wikimedia Commons (CC BY-SA / CC BY / Public Domain).
> Pricing screenshots from cursor.com / claude.com / github.com (fair use, dated 2026-05-06).
> News headlines from CNN, Bloomberg, MacRumors, DefenseScoop (fair use, original publication dates noted).

This satisfies CC license requirements + fair use disclosure.

---

## Quick all-in-one assembly tip

Once you have all assets, you can verify everything is in place:

```bash
ls -la /Users/sardorrazikov1/Alish/competitions/repomind/assets/external/{logos,photos,screenshots,audio}/
```

Expected counts:
- logos/: 20+ PNG
- photos/: 2-3 JPG
- screenshots/: 8-10 PNG (after manual capture)
- audio/: 1 MP3 (optional)

Total external assets: ~30-35 files for full polished video.

---

## Time budget

- Downloaded automatically: 0 min (already done)
- Manual headline screenshots: ~10 min (4 sites × 2-3 min each)
- AMD blog + pricing screenshots: ~10 min (5 pages)
- Hakob forum + Qwen model card: ~5 min
- Optional MI300X photo + music: ~10 min
- **Total manual time: ~30-40 min**

Then assemble in CapCut following Production Order document.
