# AI Video Automation Environment

## Overview
Complete pipeline for scraping content, generating AI voiceovers, and creating YouTube-ready ranking/commentary videos.

## Components

| Tool | Purpose | Activation |
|---|---|---|
| **Agent-Reach** | Scrape videos/clips from 13 platforms (YouTube, Bilibili, Xiaohongshu, Twitter) | `source agent-reach/.venv/bin/activate` |
| **MoneyPrinterTurbo** | AI video generation with Edge TTS, Whisper subtitles | `cd moneyprinter-turbo && source .venv/bin/activate` |
| **Voicebox** | TTS voice generation (82M param model) | `cd voicebox/backend && source .venv/bin/activate` |
| **OpenCut** | Browser-based video editor (Rust/Tauri) | `cd opencut && bun run dev` |
| **generate_ranking_video.py** | Orchestration script for full pipeline | `python generate_ranking_video.py --topic "top 10 X"` |

## Ranking Video Format (from analysis)

Based on research, the proven formula:
- **45-75 seconds**, 8-10 items, 9:16 vertical (1080x1920)
- Hook in first 2-3 seconds teasing controversial #1
- Two consensus items to establish credibility
- One debatable hot-take at #3 or #5
- Strongest defensible spicy placement at #1
- "Tell me where I'm wrong" outro

## Quick Start
```bash
# Start session
./setup.sh

# Generate a ranking video
python generate_ranking_video.py --topic "top 10 fastest animals" --count 10

# Manual workflow
source agent-reach/.venv/bin/activate
python -m agent_reach.cli read "https://www.bilibili.com/video/BV..."

cd moneyprinter-turbo
source .venv/bin/activate
python cli.py --video-subject "ranking fast animals" --voice-name "en-US-AriaNeural"
```

## Session Persistence
- `./setup.sh` - Restore all files + reinstall dependencies
- `./save.sh "message"` - Persist work to GitHub before session ends
