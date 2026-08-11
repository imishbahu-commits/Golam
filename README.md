# AI Video Automation Environment

## Overview
Complete pipeline for scraping content, generating AI voiceovers, and creating YouTube-ready ranking/commentary videos.

## Installed Tools

| Tool | Purpose | Activate |
|---|---|---|
| **Agent-Reach** | Web scraper for 13 platforms (Bilibili, XiaoHongshu, Twitter/X, YouTube) | `source agent-reach/.venv/bin/activate` |
| **MoneyPrinterTurbo** | AI video generation with TTS + Whisper subtitles | `cd moneyprinter-turbo && source .venv/bin/activate` |
| **Voicebox** | TTS voice generation (82M param model) | `cd voicebox/backend && source .venv/bin/activate` |
| **OpenCut** | Browser-based video editor (Rust/Tauri) | `cd opencut && bun run dev` |

## Ranking Video Format (Researched)
Based on analysis of YouTube ranking video tutorials:

- **Duration**: 45-75 seconds (ideal for Shorts/feed)
- **Format**: 9:16 vertical (1080x1920)
- **Structure**: 8-10 items, tier list (S/A/B/C/D/F)
- **Hook**: First 2-3 seconds teasing controversial #1
- **Sequence**: Consensus items → mid-list hot take → defensible #1 → "tell me where I'm wrong"
- **Engagement**: Pattern interrupts every 2-3 items, controversy budget = 1 hot take

## Generated Video: "Ranking Every Social Media App"
- **File**: `ranking_video.mp4` (4.9 MB)
- **Duration**: 1m20s
- **Voice**: gTTS (Google Text-to-Speech, used because Edge TTS is blocked in sandbox)
- **Subtitles**: Hardcoded captions in English
- **Content**: 10 social media platforms ranked by monetization potential

## Session Persistence
- `./setup.sh` — Restore all files + reinstall dependencies
- `./save.sh "message"` — Persist work to GitHub before session ends

## Quick Start
```bash
# Start new session
./setup.sh

# Generate a new ranking video
python generate_ranking_video.py --topic "top 10 fastest animals" --count 10

# Manual workflow
source agent-reach/.venv/bin/activate
python -m agent_reach.cli read "https://www.bilibili.com/video/BV..."

cd moneyprinter-turbo
source .venv/bin/activate
python cli.py --video-subject "ranking fast animals"
```
