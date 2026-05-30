#!/usr/bin/env python3.11
"""Build REPOMIND LinkedIn cover image v3 — uniform logo sizing + real REPOMIND brand mark.

Changes from v2:
- Replaced "RM" circle with REAL REPOMIND brand logo (assets/logo.png)
- All 7 attribution logos now uniform 55px height with consistent vertical baseline
- Better horizontal spacing in the credits strip
- Real official logos: REPOMIND (assets), Zenodo, ORCID, AMD, Qwen
- Stylized text-brand (also 55px height): OpenAIRE, lablab.ai, Hugging Face
"""

import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOGOS = HERE / "logos"


def datauri(path: Path) -> str:
    data = path.read_bytes()
    mime = {
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }[path.suffix.lower()]
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


# Real logo files we have authoritative versions of
logos = {}
for name in ["amd.svg", "orcid.svg", "zenodo.png", "qwen_real.png", "repomind.png"]:
    p = LOGOS / name
    if p.exists() and p.stat().st_size > 200:
        key = name.rsplit(".", 1)[0].replace("_real", "")
        logos[key] = datauri(p)


# Logo strip layout — single row, all 55px tall, evenly spaced
# Container starts at x=60, total width 1080, contains 7 logos
# Logo height: 55px, vertical center at y_row = 510 (so y top = 482)
LOGO_ROW_Y = 482   # top of logo container
LOGO_H = 55        # uniform logo height
LABEL_Y = 565      # text labels below logos

COVER_SVG = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 1200 630" width="1200" height="630">

  <defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F5F5F5"/>
    </linearGradient>
    <pattern id="dots" x="0" y="0" width="32" height="32" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="0.8" fill="#E5E5E5"/>
    </pattern>
  </defs>

  <!-- Background -->
  <rect width="1200" height="630" fill="url(#bg-grad)"/>
  <rect width="1200" height="630" fill="url(#dots)" opacity="0.35"/>

  <!-- AMD-red accent stripes -->
  <rect x="0" y="0" width="14" height="630" fill="#ED1C24"/>
  <rect x="0" y="0" width="1200" height="3" fill="#ED1C24"/>

  <!-- ========== TOP ZONE ========== -->

  <text x="60" y="55" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="12" font-weight="700" fill="#ED1C24" letter-spacing="3">
    METHODOLOGY PREPRINT  ·  PUBLISHED 2026-05-21  ·  CC-BY-4.0
  </text>

  <text x="60" y="135" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="72" font-weight="900" fill="#000000" letter-spacing="-2">REPOMIND</text>

  <text x="60" y="180" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="20" font-weight="500" fill="#444444" letter-spacing="-0.3">
    Reproducing 256K-context repository-scale code understanding
  </text>
  <text x="60" y="208" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="20" font-weight="500" fill="#444444" letter-spacing="-0.3">
    on a single AMD MI300X with FP8 KV cache
  </text>

  <line x1="60" y1="240" x2="220" y2="240" stroke="#ED1C24" stroke-width="3"/>

  <!-- REAL REPOMIND brand logo (replaces "RM" placeholder) -->
  <image x="1090" y="35" width="80" height="80"
         xlink:href="{logos.get('repomind', '')}"
         preserveAspectRatio="xMidYMid meet"/>

  <!-- ========== STATS ZONE ========== -->

  <g font-family="'Helvetica Neue', Helvetica, Arial, sans-serif">
    <g transform="translate(60, 260)">
      <rect x="0" y="0" width="245" height="86" fill="#FFFFFF" stroke="#E5E5E5" stroke-width="1.2"/>
      <rect x="0" y="0" width="245" height="4" fill="#ED1C24"/>
      <text x="18" y="44" font-size="32" font-weight="900" fill="#000000" letter-spacing="-1">31/31</text>
      <text x="18" y="65" font-size="10" font-weight="700" fill="#666666" letter-spacing="1.5">PARALLEL USERS @ 8K-64K</text>
      <text x="18" y="78" font-size="9" font-weight="400" fill="#666666">144/144 clean · default Triton</text>
    </g>

    <g transform="translate(325, 260)">
      <rect x="0" y="0" width="245" height="86" fill="#FFFFFF" stroke="#E5E5E5" stroke-width="1.2"/>
      <rect x="0" y="0" width="245" height="4" fill="#ED1C24"/>
      <text x="18" y="44" font-size="32" font-weight="900" fill="#000000" letter-spacing="-1">137/144</text>
      <text x="18" y="65" font-size="10" font-weight="700" fill="#666666" letter-spacing="1.5">AITER × FP8 BROKEN CELLS</text>
      <text x="18" y="78" font-size="9" font-weight="400" fill="#666666">Open regression report · filed upstream</text>
    </g>

    <g transform="translate(590, 260)">
      <rect x="0" y="0" width="245" height="86" fill="#FFFFFF" stroke="#E5E5E5" stroke-width="1.2"/>
      <rect x="0" y="0" width="245" height="4" fill="#ED1C24"/>
      <text x="18" y="44" font-size="32" font-weight="900" fill="#000000" letter-spacing="-1">3/3</text>
      <text x="18" y="65" font-size="10" font-weight="700" fill="#666666" letter-spacing="1.5">NEEDLE PASS AT 200K</text>
      <text x="18" y="78" font-size="9" font-weight="400" fill="#666666">9/9 e2e Q&amp;A · pytorch/vision 1.3M tok</text>
    </g>

    <g transform="translate(855, 260)">
      <rect x="0" y="0" width="285" height="86" fill="#FFFFFF" stroke="#E5E5E5" stroke-width="1.2"/>
      <rect x="0" y="0" width="285" height="4" fill="#ED1C24"/>
      <text x="18" y="44" font-size="32" font-weight="900" fill="#000000" letter-spacing="-1">$4.12</text>
      <text x="18" y="65" font-size="10" font-weight="700" fill="#666666" letter-spacing="1.5">TOTAL COMPUTE COST</text>
      <text x="18" y="78" font-size="9" font-weight="400" fill="#666666">2 sessions · 124 min · AMD Developer Cloud</text>
    </g>
  </g>

  <!-- ========== DOI CALLOUT ========== -->

  <g transform="translate(60, 370)">
    <rect x="0" y="0" width="1080" height="44" fill="#FFE5E5" rx="3"/>
    <rect x="0" y="0" width="6" height="44" fill="#ED1C24"/>
    <text x="22" y="19" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
          font-size="10" font-weight="700" fill="#ED1C24" letter-spacing="2.5">DOI</text>
    <text x="22" y="37" font-family="'Menlo', 'Monaco', 'Courier New', monospace"
          font-size="15" font-weight="700" fill="#000000">10.5281/zenodo.20330468</text>
    <text x="310" y="37" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
          font-size="13" font-weight="500" fill="#444444">→ https://doi.org/10.5281/zenodo.20330468</text>
  </g>

  <!-- ========== LOGO STRIP — UNIFORM 55px HEIGHT, ALIGNED ========== -->

  <text x="60" y="450" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="10" font-weight="700" fill="#666666" letter-spacing="2.5">
    HOSTED BY  ·  INDEXED IN  ·  BUILT ON  ·  POWERED BY
  </text>

  <!-- All logos in container y=482 to y=537 (55px tall), uniform vertical center -->

  <!-- 1. Zenodo (real PNG logo, ~2.5:1 aspect ratio) -->
  <image x="60" y="{LOGO_ROW_Y}" width="138" height="{LOGO_H}"
         xlink:href="{logos.get('zenodo', '')}"
         preserveAspectRatio="xMidYMid meet"/>
  <text x="129" y="{LABEL_Y}" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="10" font-weight="500" fill="#666666" text-anchor="middle">Hosted</text>

  <!-- 2. ORCID (real SVG iD logo — square, plus text) -->
  <image x="220" y="{LOGO_ROW_Y}" width="55" height="{LOGO_H}"
         xlink:href="{logos.get('orcid', '')}"
         preserveAspectRatio="xMidYMid meet"/>
  <text x="285" y="{LOGO_ROW_Y + 35}" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="16" font-weight="700" fill="#A6CE39">ORCID</text>
  <text x="265" y="{LABEL_Y}" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="10" font-weight="500" fill="#666666" text-anchor="middle">Author iD</text>

  <!-- 3. OpenAIRE (text brand — sized to match 55px visual height) -->
  <g transform="translate(372, {LOGO_ROW_Y})">
    <text y="40" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
          font-size="22" font-weight="800" fill="#3F9BD8" letter-spacing="-0.5">Open</text>
    <text x="58" y="40" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
          font-size="22" font-weight="400" fill="#222222" letter-spacing="-0.5">AIRE</text>
  </g>
  <text x="427" y="{LABEL_Y}" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="10" font-weight="500" fill="#666666" text-anchor="middle">Indexed in</text>

  <!-- 4. AMD (real SVG logo, ~3.5:1 aspect ratio) -->
  <image x="535" y="{LOGO_ROW_Y}" width="155" height="{LOGO_H}"
         xlink:href="{logos.get('amd', '')}"
         preserveAspectRatio="xMidYMid meet"/>
  <text x="612" y="{LABEL_Y}" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="10" font-weight="500" fill="#666666" text-anchor="middle">Built on MI300X</text>

  <!-- 5. lablab.ai (text brand — matches 55px height) -->
  <g transform="translate(720, {LOGO_ROW_Y})">
    <text y="40" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
          font-size="22" font-weight="900" fill="#000000" letter-spacing="-1">lablab</text>
    <text x="78" y="40" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
          font-size="22" font-weight="500" fill="#ED1C24" letter-spacing="-0.5">.ai</text>
  </g>
  <text x="775" y="{LABEL_Y}" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="10" font-weight="500" fill="#666666" text-anchor="middle">Hackathon host</text>

  <!-- 6. Hugging Face (emoji + text — matches 55px height) -->
  <g transform="translate(848, {LOGO_ROW_Y})">
    <text y="40" font-family="'Apple Color Emoji', 'Segoe UI Emoji', sans-serif"
          font-size="32" fill="#FFD21E">🤗</text>
    <text x="42" y="38" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
          font-size="15" font-weight="700" fill="#000000">Hugging Face</text>
  </g>
  <text x="930" y="{LABEL_Y}" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="10" font-weight="500" fill="#666666" text-anchor="middle">HF Space host</text>

  <!-- 7. Qwen (real PNG logo, ~3.3:1 aspect ratio) -->
  <image x="1000" y="{LOGO_ROW_Y}" width="140" height="{LOGO_H}"
         xlink:href="{logos.get('qwen', '')}"
         preserveAspectRatio="xMidYMid meet"/>
  <text x="1070" y="{LABEL_Y}" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="10" font-weight="500" fill="#666666" text-anchor="middle">Model maker</text>

  <!-- ========== FOOTER ========== -->

  <line x1="60" y1="582" x2="1140" y2="582" stroke="#E5E5E5" stroke-width="1"/>

  <text x="60" y="603" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="13" font-weight="700" fill="#000000">Sardor Razikov</text>
  <text x="155" y="603" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="11" font-weight="400" fill="#666666">
    Independent ML Engineer  ·  ORCID 0009-0007-0731-4247
  </text>

  <text x="1140" y="603" text-anchor="end"
        font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="11" font-weight="500" fill="#666666">
    23 pages · 6,000 words · CC-BY-4.0 · AMD Developer Hackathon 2026
  </text>

  <text x="60" y="622" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="9" font-weight="400" fill="#666666" letter-spacing="0.3">
    Logos shown are factual attribution to organizations involved in this work (nominative fair use). All trademarks property of their respective owners.
  </text>

</svg>
"""

out = HERE / "linkedin_cover_v2.svg"
out.write_text(COVER_SVG)
print(f"Wrote {out}")
print(f"Embedded {len(logos)} real logos: {list(logos.keys())}")
