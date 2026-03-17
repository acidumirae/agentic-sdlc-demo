#!/usr/bin/env bash
# Hook: pre-implementation
# Agent: orchestration-agent
# Phase gate: blocks development unless planning and architecture artifacts exist.
# Run manually or wire into your IDE's pre-task hook.

set -euo pipefail

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Kiro SDLC — Pre-Implementation Phase Gate"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ERRORS=0

# Check planning artifacts
for artifact in "docs/planning/planning.md" "docs/planning/user-stories.md" "docs/planning/acceptance-criteria.md"; do
  if [ ! -f "$artifact" ]; then
    echo "❌ Missing: $artifact"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ Found:   $artifact"
  fi
done

# Check architecture artifact
if [ ! -f "docs/arch/architecture.md" ]; then
  echo "❌ Missing: docs/arch/architecture.md"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ Found:   docs/arch/architecture.md"
fi

echo ""

if [ $ERRORS -gt 0 ]; then
  echo "❌ SDLC VIOLATION — $ERRORS required artifact(s) missing."
  echo ""
  echo "Required actions:"
  echo "  1. Run planning-agent  → generates docs/planning/"
  echo "  2. Run architect-agent → generates docs/arch/architecture.md"
  echo ""
  echo "See .kiro/specifications/sdlc-workflow.yaml for phase dependencies."
  exit 1
fi

echo "✅ All phase prerequisites met. Development Agent may proceed."
exit 0
