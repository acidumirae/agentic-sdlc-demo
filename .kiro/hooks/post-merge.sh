#!/usr/bin/env bash
# Hook: post-merge
# Agent: deployment-agent
# Triggered after a merge to main. Runs predictive deployment risk analysis.
# Install: ln -sf ../../.kiro/hooks/post-merge.sh .git/hooks/post-merge

set -euo pipefail

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Kiro SDLC — Post-Merge Deployment Analysis"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
COMMIT_HASH=$(git rev-parse HEAD)

echo "Branch : $CURRENT_BRANCH"
echo "Commit : $COMMIT_HASH"
echo ""

# Only run full deployment prediction on main
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "[SKIP] Not on main branch. Skipping deployment prediction."
  exit 0
fi

# Verify test and security reports exist before deploying
if [ ! -f "docs/reports/coverage-report.md" ]; then
  echo "❌ DEPLOY BLOCKED — No coverage report found."
  echo "   Run the Testing Agent (synthesize_tests.py) first."
  exit 1
fi

if [ ! -f "docs/reports/security-report.md" ]; then
  echo "❌ DEPLOY BLOCKED — No security report found."
  echo "   Run the Security Agent (static_scanner.py) first."
  exit 1
fi

# Run deployment risk predictor
python3 .kiro/skills/deployment_predictor.py "$COMMIT_HASH" canary

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo ""
  echo "✅ Deployment approved. Canary rollout initiated."
  echo "   Monitor: error_rate, latency_p99, saturation"
else
  echo ""
  echo "❌ DEPLOY HALTED — Risk score exceeds threshold."
  echo "   Notifying development-agent and testing-agent to remediate."
  echo "   See docs/reports/deployment-runbook.md for details."
  exit 1
fi
