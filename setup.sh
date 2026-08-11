#!/bin/bash
# setup.sh - Complete environment bootstrap for new sessions
# Clones all repos, creates venvs, installs dependencies
set -e

export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$HOME/.deno/bin:$PATH"

SESSION_DIR="/workspace/3687d744-ed12-49a6-a5a1-d31c2e560a56/sessions/agent_962408fb-3d44-43a6-b282-2cdcc3bc435e"
cd "$SESSION_DIR"

echo "=== Restoring session files from GitHub ==="
git fetch origin
git reset --hard origin/session/$(basename "$SESSION_DIR")

echo "=== Installing uv ==="
if ! command -v uv &> /dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"

echo "=== Installing Rust (for OpenCut) ==="
if ! command -v cargo &> /dev/null; then
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
  . "$HOME/.cargo/env"
fi
export PATH="$HOME/.cargo/bin:$PATH"

echo "=== Installing Deno (for YouTube downloads) ==="
if ! command -v deno &> /dev/null; then
  curl -fsSL https://deno.land/install.sh | sh
fi
export PATH="$HOME/.deno/bin:$PATH"

echo "=== Setting up Agent-Reach ==="
if [ ! -d "agent-reach/.git" ]; then
  git clone https://github.com/Panniantong/Agent-Reach.git agent-reach
fi
cd agent-reach
if [ ! -d ".venv" ]; then uv venv .venv; fi
uv pip install -e ".[all]" --python .venv/bin/python 2>&1 | tail -3
[ -f ".env.example" ] && [ ! -f ".env" ] && cp .env.example .env
cd "$SESSION_DIR"

echo "=== Setting up MoneyPrinterTurbo ==="
if [ ! -d "moneyprinter-turbo/.git" ]; then
  git clone https://github.com/harry0703/MoneyPrinterTurbo.git moneyprinter-turbo
fi
cd moneyprinter-turbo
if [ ! -d ".venv" ]; then uv venv .venv; fi
uv pip install -r requirements.txt --python .venv/bin/python 2>&1 | tail -3
[ -f "config.example.toml" ] && [ ! -f "config.toml" ] && cp config.example.toml config.toml
cd "$SESSION_DIR"

echo "=== Setting up Voicebox (TTS) ==="
if [ ! -d "voicebox/.git" ]; then
  git clone https://github.com/jamiepine/voicebox.git voicebox
fi
cd voicebox/backend
if [ ! -d ".venv" ]; then uv venv .venv --python 3.12; fi
uv pip install -r requirements.txt --python .venv/bin/python 2>&1 | tail -5
cd "$SESSION_DIR"

echo "=== Setting up OpenCut (Video Editor) ==="
if [ ! -d "opencut/.git" ]; then
  git clone https://github.com/OpenCut-app/OpenCut.git opencut
fi
if ! command -v bun &> /dev/null; then
  curl -LsSf https://bun.sh/install | sh
fi
export PATH="$HOME/.bun/bin:$PATH"
cd opencut
[ ! -d "node_modules" ] && bun install 2>&1 | tail -3
cd "$SESSION_DIR"

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
echo "  cd moneyprinter-turbo && source .venv/bin/activate"
echo "  python cli.py --help"
echo ""
echo "Voicebox (TTS):"
echo "  cd voicebox/backend && source .venv/bin/activate"
echo "  python voicebox-server.py"
echo ""
echo "OpenCut (video editing):"
echo "  cd opencut && bun run dev"
echo ""
echo "Save before exit: ./save.sh 'Your message'"
echo "=============================================="
