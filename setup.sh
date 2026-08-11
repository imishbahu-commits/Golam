#!/bin/bash
# setup.sh - Complete environment bootstrap for new sessions
# Clones all repos, creates venvs, installs dependencies, restores configs
set -e

SESSION_DIR="/workspace/3687d744-ed12-49a6-a5a1-d31c2e560a56/sessions/agent_962408fb-3d44-43a6-b282-2cdcc3bc435e"
export PATH="$HOME/.local/bin:$PATH"

cd "$SESSION_DIR"

echo "=== Restoring session files from GitHub ==="
git fetch origin
git reset --hard origin/session/$(basename "$SESSION_DIR")

echo "=== Installing uv ==="
if ! command -v uv &> /dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"

echo "=== Setting up Agent-Reach (scraping) ==="
if [ ! -d "agent-reach/.git" ]; then
  git clone https://github.com/Panniantong/Agent-Reach.git agent-reach
fi
cd agent-reach
if [ ! -d ".venv" ]; then
  uv venv .venv
fi
uv pip install -e ".[all]" --python .venv/bin/python 2>&1 | tail -3
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
  cp .env.example .env
fi
cd "$SESSION_DIR"

echo "=== Setting up MoneyPrinterTurbo (video gen) ==="
if [ ! -d "moneyprinter-turbo/.git" ]; then
  git clone https://github.com/harry0703/MoneyPrinterTurbo.git moneyprinter-turbo
fi
cd moneyprinter-turbo
if [ ! -d ".venv" ]; then
  uv venv .venv
fi
uv pip install -r requirements.txt --python .venv/bin/python 2>&1 | tail -3
if [ -f "config.example.toml" ] && [ ! -f "config.toml" ]; then
  cp config.example.toml config.toml
fi
cd "$SESSION_DIR"

echo "=== Setting up Kokoro 82M (TTS) ==="
if [ ! -d "kokoro-82m/.git" ]; then
  git clone https://github.com/hexgrad/kokoro.git kokoro-82m
fi
if [ ! -d "kokoro-82m/.venv" ]; then
  cd kokoro-82m
  uv venv .venv
  uv pip install -e . --python .venv/bin/python 2>&1 | tail -3
  cd "$SESSION_DIR"
fi

echo ""
echo "=============================================="
echo "  ENVIRONMENT READY!"
echo "=============================================="
echo ""
echo "Agent-Reach (scraping):"
echo "  source agent-reach/.venv/bin/activate"
echo "  python -m agent_reach.cli doctor"
echo ""
echo "MoneyPrinterTurbo (video gen):"
echo "  source moneyprinter-turbo/.venv/bin/activate"
echo "  python moneyprinter-turbo/cli.py --help"
echo ""
echo "Kokoro 82M (voice):"
echo "  cd kokoro-82m"
echo "  source .venv/bin/activate"
echo ""
echo "Save before exit: ./save.sh 'Your message'"
echo "=============================================="
