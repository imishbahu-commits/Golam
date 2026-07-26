# OpenManus + Persistent Storage Setup

## Quick Start

```bash
# Run the setup script
bash setup-openmanus.sh

# Or with Docker (persistent storage)
docker-compose -f docker-compose.openmanus.yml up -d
```

## Persistent Storage Options

### Option 1: MCP Memory Server (Recommended)
Configured in `kilo.json` - gives you 500 free memories, 3 agents on Kronvex free tier.
- No credit card required
- Sign up at kronvex.io/dashboard

### Option 2: Git Auto-Commit
Kilo Cloud Agent already auto-commits to a unique branch on every message.
Merge to main branch to keep work:
```bash
git checkout feature/kilo-agent-session && git merge main
```

### Option 3: Local Mount Persistence
Docker setup mounts `/workspace/openmanus-persistent` to host filesystem.
Files survive container restarts.

## Free Models Configured
- `laguna-m-1-free` (Poolside) - KiloBench 25.4%
- `hy3-free` (Tencent) - KiloBench 47.6%
- Routes through Kilo Gateway with `$0` token cost

## Dashboard Access
- Kilo Mobile app: kilocode.onelink.me/ZzZZ/07005hzt
- Docker: http://localhost:8080
- CLI: `python run_mcp.py`