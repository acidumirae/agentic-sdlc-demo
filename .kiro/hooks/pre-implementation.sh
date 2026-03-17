#!/bin/bash
# Hook: pre-implementation.sh
# Purpose: Ensures that a developer agent cannot start writing code without a valid spec and architecture.

echo "[Kiro Hook] Verifying SDLC phase prerequisites..."

if [ ! -d "docs/specs" ] || [ -z "$(ls -A docs/specs/*.md 2>/dev/null)" ]; then
    echo "❌ SDLC Violation: No specifications found in docs/specs/."
    echo "Action required: Run the Product Manager agent to generate specs."
    exit 1
fi

if [ ! -d "docs/arch" ] || [ -z "$(ls -A docs/arch/*.md 2>/dev/null)" ]; then
    echo "❌ SDLC Violation: No architecture documents found in docs/arch/."
    echo "Action required: Run the Architect agent to design the system."
    exit 1
fi

echo "✅ Prerequisites met. Proceeding to implementation..."
exit 0
