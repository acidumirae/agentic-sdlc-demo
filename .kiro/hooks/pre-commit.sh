#!/usr/bin/env bash
# Hook: pre-commit
# Agent: security-agent
# Runs static security scan on staged files before allowing a commit.
# Install: ln -sf ../../.kiro/hooks/pre-commit.sh .git/hooks/pre-commit

set -euo pipefail

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Kiro SDLC — Pre-Commit Security Scan"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Require Python 3
if ! command -v python3 &>/dev/null; then
  echo "[ERROR] python3 not found. Cannot run security scan."
  exit 1
fi

# Run security scanner against staged diff only
python3 .kiro/skills/static_scanner.py --diff HEAD

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo ""
  echo "❌ COMMIT BLOCKED — Critical security vulnerabilities detected."
  echo "   Review the findings above and apply the suggested remediations."
  echo "   See .cursor/rules/05-security-agent.mdc for auto-remediation guidance."
  exit 1
fi

echo ""
echo "✅ Security scan passed. Proceeding with commit."
exit 0
