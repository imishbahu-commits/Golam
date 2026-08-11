# AI Video Automation Environment

## Overview
A complete pipeline for scraping videos from the web, generating AI voiceovers, and creating YouTube-ready commentary videos.

## Components

| Tool | Purpose | Activate |
|---|---|---|
| **Agent-Reach** | Web scraper for 13 platforms (Bilibili, XiaoHongShu, Twitter/X, YouTube, Reddit...) | `source agent-reach/.venv/bin/activate` |
| **MoneyPrinterTurbo** | AI video generation with TTS (Edge TTS default) | `source moneyprinter-turbo/.venv/bin/activate` |
| **Kokoro 82M** | 82M parameter TTS model (English/Zh multi-speaker) | `cd kokoro-82m && source .venv/bin/activate` |

## Session Persistence
All configs and scripts are tracked on GitHub. At the start of each session, run `./setup.sh` to restore everything.

## Quick Start
```bash
# 1. Start new session
source agent-reach/.venv/bin/activate
source moneyprinter-turbo/.venv/bin/activate  # optional: switch to MPT env

# 2. Scrape video clips (Agent-Reach)
python -m agent_reach.cli read "https://www.bilibili.com/video/BV..."

# 3. Generate voiceover (MoneyPrinterTurbo or Kokoro)
python moneyprinter-turbo/cli.py --prompt "..." --voice-name "en-US-AriaNeural"

# 4. Save your progress before session ends
./save.sh "Work completed"
```
