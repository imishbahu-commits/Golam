#!/bin/bash
set -e

echo "Setting up OpenManus with persistent storage and free models..."

# Clone OpenManus
if [ ! -d "OpenManus" ]; then
    git clone https://github.com/FoundationAgents/OpenManus.git
fi
cd OpenManus

# Create workspace directory with persistence
mkdir -p /workspace/openmanus-persistent
mkdir -p ~/.openmanus

# Create OpenManus config with Kilo free models
cat > config/config.toml << 'CONFIG'
# OpenManus config using free models via Kilo Gateway
[llm]
model = "laguna-m-1-free"
base_url = "https://gateway.kilo.ai/v1"
api_key = "kgw-free"
max_tokens = 4096
temperature = 0.0

[llm.vision]
model = "laguna-m-1-free"
base_url = "https://gateway.kilo.ai/v1"
api_key = "kgw-free"
max_tokens = 4096

[workspace]
root = "/workspace/openmanus-persistent"

# MCP configuration for persistent memory
[mcp_servers.memory]
command = "npx"
args = ["-y", "@kronvex/mcp-server"]
CONFIG

echo "Installation complete!"
echo "Run: cd OpenManus && python run_mcp.py"