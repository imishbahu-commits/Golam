#!/bin/bash
# restore.sh - Restores files from GitHub at the start/end of a session
# Usage: ./restore.sh
cd /workspace/3687d744-ed12-49a6-a5a1-d31c2e560a56/sessions/agent_962408fb-3d44-43a6-b282-2cdcc3bc435e
git fetch origin
git reset --hard origin/session/agent_962408fb-3d44-43a6-b282-2cdcc3bc435e
echo "Files restored from GitHub"
