<div align="center">
  <img src="assets/banner.png" alt="Digital Asset Forge — Sovereign Architecture Banner" width="100%" />
</div>

<br />

<div align="center">
  <a href="https://zoth.nullai.tech/tools/digital-asset-forge"><img src="https://img.shields.io/badge/Zoth_Studio_v2-Workspace-D4AF37?style=for-the-badge&logo=sparkles&logoColor=black" alt="Zoth Studio Workspace" /></a>
  <a href="http://127.0.0.1:8118"><img src="https://img.shields.io/badge/ZothOS_v3.3-Port_:8118-38BDF8?style=for-the-badge&logo=linux&logoColor=black" alt="Port :8118" /></a>
  <a href="https://nullai.tech"><img src="https://img.shields.io/badge/Security-100%25_Zero--Egress-10B981?style=for-the-badge&logo=shield&logoColor=black" alt="Zero Egress" /></a>
  <a href="https://buy.stripe.com/3cIfZg27PdKo2D64Ocfw40X"><img src="https://img.shields.io/badge/☕_Buy_Us_a_Coffee-Stripe-D4AF37?style=for-the-badge" alt="Buy Us a Coffee" /></a>
</div>

# ⚡ Digital Asset Forge (v2.5.0)

> **High-Res 300 DPI multi-ratio wall art pack generator (2:3, 3:4, 4:5, 11:14, ISO) for Etsy & Shopify digital downloads (98% margin) with 20MB multi-zip splitting.**

---

## 🏛️ Architectural Overview

**Digital Asset Forge** is a sovereign digital commerce powerhouse in the **[Zoth Studio v2](https://zoth.nullai.tech)** arsenal and **[ZothOS Linux 3.3](https://zothos.nullai.tech)** ecosystem, engineered by **Neal Frazier Tech ([@1nc0gn30](https://github.com/1nc0gn30))**.

| Property | Specification |
| :--- | :--- |
| **Tool ID** | `digital-asset-forge` |
| **Category** | `Commerce & MCP` |
| **Local Port** | `http://127.0.0.1:8118` |
| **Execution Mode** | Native Python Daemon & Browser Client |
| **Zoth Studio Route** | `http://127.0.0.1:3000/tools/digital-asset-forge` |
| **License** | 100% Free & Open Access (Zero Paywalls) |

---

## 💎 What It Does & How It Works

- **Standard 5-Ratio Wall Art Architecture**: Automatically calculates master 300 DPI pixel dimensions across the five standard art download ratio families:
  - `2:3 Ratio`: 24"x36" (7200x10800px) — scales to 4x6, 6x9, 8x12, 10x15, 12x18, 16x24, 20x30, 24x36.
  - `3:4 Ratio`: 18"x24" (5400x7200px) — scales to 6x8, 9x12, 12x16, 15x20, 18x24.
  - `4:5 Ratio`: 16"x20" (4800x6000px) — scales to 4x5, 8x10, 12x15, 16x20.
  - `11:14 Ratio`: 11"x14" (3300x4200px) — standard home photo frame.
  - `ISO Metric`: A1 (7016x9933px) — scales to A5, A4, A3, A2, A1.
- **Etsy 20MB Multi-Zip Splitting**: Calculates exact compression splits to ensure digital download ZIP archives comply with Etsy's strict 20MB per-file upload limit.
- **Automated Customer Printing Guide**: Generates comprehensive PDF/TXT printing instructions explaining paper finishes (matte vs semi-gloss), DPI requirements, and local print labs (Costco, Walgreens, local print shops).
- **SEO & Copywriting Engine**: Generates high-converting title, 13 algorithmic search tags, and formatted product descriptions optimized for Etsy and Shopify search rank.

---

## 🚀 Quick Start

```bash
# Clone and launch the standalone daemon on port 8118
git clone https://github.com/1nc0gn30/digital-asset-forge.git
cd digital-asset-forge
python3 server.py --port 8118

# In another terminal, inspect ratio specifications:
curl -s http://127.0.0.1:8118/health
curl -s http://127.0.0.1:8118/api/ratios
```

---

## 💻 ZothOS CLI & MCP Commands

The sovereign binary `digital-asset-forge` is pre-installed in `/usr/local/bin` and `~/.local/bin`:

```bash
# Verify installation & status
digital-asset-forge --version
digital-asset-forge --status
digital-asset-forge --json

# Validate pixel dimensions against physical print size
digital-asset-forge dpi --width 7200 --height 10800 --target-w 24 --target-h 36

# Generate digital download pack manifest
digital-asset-forge manifest --title "Celestial Merkaba" --artist "Neal Frazier"
digital-asset-forge manifest --title "Celestial Merkaba" --json

# Generate printing guide for customers
digital-asset-forge guide --title "Celestial Merkaba" --shop "Neal Frazier Atelier"

# Generate Etsy SEO title and 13 tags
digital-asset-forge etsy --title "Celestial Merkaba" --niche geometric --price 7.50

# Launch server daemon
digital-asset-forge server --port 8118
```

---

## ☕ 100% Free & Open-Access Support Architecture

Every tool engineered by Neal Frazier Tech is **100% free, open, and unlocked by default**. There are zero paywalls, zero license locks, and zero feature gates.

If this tool empowers your business or automates your art downloads, consider supporting development:

- **☕ Buy Us a Coffee (Stripe)**: [https://buy.stripe.com/3cIfZg27PdKo2D64Ocfw40X](https://buy.stripe.com/3cIfZg27PdKo2D64Ocfw40X)
- **◎ Solana Tip Address**: `GG2eQbVh8ut1BK6j1A2tz7pSySdLpD38BgyEhGcxdXoK`

---

<div align="center">
  <sub>Engineered by <b>Neal Frazier Tech</b> (<a href="https://github.com/1nc0gn30">@1nc0gn30</a>) &bull; <a href="https://nullai.tech">NullAI Platform</a> &bull; <a href="https://zoth.nullai.tech">Zoth Studio v2</a></sub>
</div>
