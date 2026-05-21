#!/usr/bin/env python3.11
"""Build REPOMIND LinkedIn cover image with REAL embedded logos.

Approach:
- Real official logos (downloaded from Wikipedia Commons / official brand sites):
  - AMD (SVG)
  - ORCID (SVG)
  - Zenodo (PNG, gradient logo from about.zenodo.org)
  - Qwen / Alibaba Cloud (JPEG)
- Stylized text-brand representations for orgs where authoritative logos weren't reachable:
  - Hugging Face: 🤗 emoji + text (their official brand mark)
  - lablab.ai: stylized typography
  - OpenAIRE: stylized typography

The logos are embedded as base64 data URIs so the output SVG is self-contained.
Renders to PNG via rsvg-convert at 1200×630 (LinkedIn optimal).
"""

import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOGOS = HERE / "logos"


def datauri(path: Path) -> str:
    """Return data: URI for a logo file."""
    data = path.read_bytes()
    mime = {
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }[path.suffix.lower()]
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


# Load logos as data URIs (only the ones we have as real files)
logos = {}
# Use qwen_real.png (PNG-converted from JPEG) for better SVG embedding compatibility
for name in ["amd.svg", "orcid.svg", "zenodo.png", "qwen_real.png"]:
    p = LOGOS / name
    if p.exists() and p.stat().st_size > 200:  # filter out HTML error pages
        key = name.rsplit(".", 1)[0].replace("_real", "")
        logos[key] = datauri(p)


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

  <!-- Left AMD-red accent stripe -->
  <rect x="0" y="0" width="14" height="630" fill="#ED1C24"/>
  <rect x="0" y="0" width="1200" height="3" fill="#ED1C24"/>

  <!-- ========== TOP ZONE (title + DOI) ========== -->

  <!-- Label -->
  <text x="60" y="55" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="12" font-weight="700" fill="#ED1C24" letter-spacing="3">
    METHODOLOGY PREPRINT  ·  PUBLISHED 2026-05-21  ·  CC-BY-4.0
  </text>

  <!-- Title -->
  <text x="60" y="135" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="72" font-weight="900" fill="#000000" letter-spacing="-2">REPOMIND</text>

  <!-- Subtitle -->
  <text x="60" y="180" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="20" font-weight="500" fill="#444444" letter-spacing="-0.3">
    Reproducing 256K-context repository-scale code understanding
  </text>
  <text x="60" y="208" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="20" font-weight="500" fill="#444444" letter-spacing="-0.3">
    on a single AMD MI300X with FP8 KV cache
  </text>

  <!-- Red divider -->
  <line x1="60" y1="240" x2="220" y2="240" stroke="#ED1C24" stroke-width="3"/>

  <!-- "RM" brand mark right top -->
  <g transform="translate(1100, 75)">
    <circle cx="0" cy="0" r="34" fill="none" stroke="#ED1C24" stroke-width="2.5"/>
    <text x="0" y="8" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
          font-size="24" font-weight="900" text-anchor="middle" fill="#ED1C24">RM</text>
  </g>

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

  <!-- ========== LOGOS ZONE — REAL OFFICIAL LOGOS ========== -->

  <text x="60" y="450" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="10" font-weight="700" fill="#666666" letter-spacing="2.5">
    HOSTED BY  ·  INDEXED IN  ·  BUILT ON  ·  POWERED BY
  </text>

  <!-- Logo strip — row 1 (publishers + indexers) -->
  <g transform="translate(60, 470)">
    <!-- Zenodo — real PNG logo -->
    <image x="0" y="10" width="125" height="50"
           xlink:href="{logos.get('zenodo', '')}"
           preserveAspectRatio="xMidYMid meet"/>

    <!-- ORCID — real SVG logo (small) -->
    <image x="160" y="10" width="50" height="50"
           xlink:href="{logos.get('orcid', '')}"
           preserveAspectRatio="xMidYMid meet"/>
    <text x="218" y="42" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
          font-size="14" font-weight="600" fill="#000000">ORCID</text>

    <!-- OpenAIRE — text-styled brand -->
    <g transform="translate(310, 30)">
      <text font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
            font-size="22" font-weight="800" fill="#3F9BD8" letter-spacing="-0.5">Open</text>
      <text x="55" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
            font-size="22" font-weight="400" fill="#444444" letter-spacing="-0.5">AIRE</text>
    </g>

    <!-- AMD — real SVG logo -->
    <image x="490" y="6" width="135" height="58"
           xlink:href="{logos.get('amd', '')}"
           preserveAspectRatio="xMidYMid meet"/>

    <!-- lablab.ai — text-styled brand -->
    <g transform="translate(660, 35)">
      <text font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
            font-size="22" font-weight="900" fill="#000000" letter-spacing="-1">lablab</text>
      <text x="80" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
            font-size="22" font-weight="400" fill="#ED1C24" letter-spacing="-0.5">.ai</text>
    </g>

    <!-- Hugging Face — emoji + text -->
    <g transform="translate(810, 35)">
      <text font-family="'Apple Color Emoji', 'Segoe UI Emoji', sans-serif"
            font-size="26" fill="#FFD21E">🤗</text>
      <text x="36" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
            font-size="16" font-weight="700" fill="#000000">Hugging Face</text>
    </g>

    <!-- Qwen / Alibaba Cloud — real JPEG -->
    <image x="985" y="0" width="155" height="70"
           xlink:href="{logos.get('qwen', '')}"
           preserveAspectRatio="xMidYMid meet"/>
  </g>

  <!-- ========== FOOTER ========== -->

  <!-- Divider -->
  <line x1="60" y1="560" x2="1140" y2="560" stroke="#E5E5E5" stroke-width="1"/>

  <!-- Author line -->
  <text x="60" y="585" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="14" font-weight="700" fill="#000000">Sardor Razikov</text>
  <text x="155" y="585" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="12" font-weight="400" fill="#666666">
    Independent ML Engineer, Tashkent, Uzbekistan
  </text>

  <!-- Right footer -->
  <text x="1140" y="585" text-anchor="end"
        font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="12" font-weight="500" fill="#666666">
    ORCID 0009-0007-0731-4247
  </text>

  <!-- Bottom mini-info -->
  <text x="60" y="610" font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="10" font-weight="400" fill="#666666" letter-spacing="0.5">
    23 pages · 6,000 words · 62 measured data points · MIT-licensed code · CC-BY-4.0 preprint
  </text>
  <text x="1140" y="610" text-anchor="end"
        font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="10" font-weight="400" fill="#666666" letter-spacing="0.5">
    AMD Developer Hackathon 2026 · May 4–11, 2026
  </text>

</svg>
"""

out = HERE / "linkedin_cover_v2.svg"
out.write_text(COVER_SVG)
print(f"Wrote {out}")
print(f"Embedded {len(logos)} real logos as base64 data URIs: {list(logos.keys())}")
