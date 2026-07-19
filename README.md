# AI Video Automation Environment

## Installed Tools

| Tool | Location | Purpose |
|---|---|---|
| **Agent-Reach** | `agent-reach/` | Web scraper for 13 platforms (X/Twitter, Bilibili, Xiaohongshu, YouTube, Reddit, etc.) |
| **MoneyPrinterTurbo** | `moneyprinter-turbo/` | AI video generation with TTS (Edge TTS default) |
| **Kokoro 82M** | `kokoro-82m/` | 82M parameter TTS model from hexgrad/kokoro |

## Quick Start

### Activate environments
```bash
source agent-reach/.venv/bin/activate
# agent-reach commands available
python -m agent_reach.cli doctor
python -m agent_reach.cli install --env=auto

source ../moneyprinter-turbo/.venv/bin/activate
# moneyprinter-turbo commands available
python cli.py --help
```

### Workflow: Scrape -> Generate -> Voiceover -> Video

1. **Scrape videos/clips** from Bilibili, Xiaohongshu, X/Twitter using Agent-Reach:
   ```bash
   python -m agent_reach.cli read "https://www.bilibili.com/video/BV..."
   python -m agent_reach.cli read "https://www.xiaohongshu.com/explore/..."
   ```

2. **Generate YouTube-ready videos** with MoneyPrinterTurbo:
   ```bash
   python cli.py --prompt "A video about AI trends" --voice-name "en-US-AriaNeural" --aspect-ratio 16:9
   ```

3. **Use Kokoro 82M** for alternative TTS:
   ```bash
   cd kokoro-82m && uv run python -m kokoro --text "Hello world" --model z
   ```

## Session Persistence

All files in this directory are tracked on GitHub. Use:
- `./save.sh "message"` — persist current state to GitHub
- `./setup.sh` — restore files + reinstall dependencies at session start
