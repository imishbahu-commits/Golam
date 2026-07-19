#!/bin/bash
# save.sh - Persist key files (configs, scripts, data) to GitHub
# Run this before session ends to save your work
# Usage: ./save.sh "commit message"
SESSION_DIR="/workspace/3687d744-ed12-49a6-a5a1-d31c2e560a56/sessions/agent_962408fb-3d44-43a6-b282-2cdcc3bc435e"
cd "$SESSION_DIR"
MSG="${1:-Update files: $(date -u +%Y-%m-%dT%H:%M:%SZ)}"
git add -A
git commit -m "$MSG" 2>&1 || true
git push origin HEAD:refs/heads/session/agent_962408fb-3d44-43a6-b282-2cdcc3bc435e 2>&1
echo "Files persisted to GitHub"
