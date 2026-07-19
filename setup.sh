#!/bin/bash
# setup.sh - Complete environment bootstrap for new sessions
# Clones all repos, creates venvs, installs dependencies, restores configs
set -e

SESSION_DIR="/workspace/3687d744-ed12-49a6-a5a1-d31c2e560a56/sessions/agent_962408fb-3d44-43a6-b282-2cdcc3bc435e"
export PATH="$HOME/.local/bin:$PATH"

cd "$SESSION_DIR"

echo "=== Fetching latest session files from GitHub ==="
git fetch origin
git reset --hard origin/session/$(basename "$SESSION_DIR")

echo "=== Installing uv (Python package manager) ==="
if ! command -v uv &> /dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "=== Cloning Agent-Reach ==="
if [ ! -d "agent-reach/.git" ]; then
  git clone https://github.com/Panniantong/Agent-Reach.git agent-reach
fi
cd agent-reach
uv venv .venv
uv pip install -e ".[all]" --python .venv/bin/python
cd "$SESSION_DIR"

echo "=== Cloning MoneyPrinterTurbo ==="
if [ ! -d "moneyprinter-turbo/.git" ]; then
  git clone https://github.com/harry0703/MoneyPrinterTurbo.git moneyprinter-turbo
fi
cd moneyprinter-turbo
uv venv .venv
uv pip install -r requirements.txt --python .venv/bin/python
# Copy config if it exists, create if not
if [ -f "$SESSION_DIR/moneyprinter-turbo/config.toml" ]; then
  cp "$SESSION_DIR/moneyprinter-turbo/config.toml" .
elif [ -f config.example.toml ] && [ ! -f config.toml ]; then
  cp config.example.toml config.toml
fi
cd "$SESSION_DIR"

echo "=== Cloning Kokoro 82M ==="
if [ ! -d "kokoro-82m/.git" ]; then
  git clone https://github.com/hexgrad/kokoro.git kokoro-82m
fi

echo ""
echo "=== Setup complete! ==="
echo "Activate Agent-Reach:  source agent-reach/.venv/bin/activate"
echo "Activate MPT:          source moneyprinter-turbo/.venv/bin/activate"
echo "Kokoro:                cd kokoro-82m && uv run python -m kokoro"
echo ""
echo "Run ./save.sh to persist any changes to GitHub."
