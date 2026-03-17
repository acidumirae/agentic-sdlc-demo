#!/usr/bin/env bash

# .kerio/hooks/pre-commit.sh
# Trigger the Security Reviewer Agent before allowing local commits.

echo "Kerio SDLC: Triggering pre-commit security analysis..."

# Simulate the agent call
python3 .kerio/skills/static_scanner.py --diff HEAD

if [ $? -ne 0 ]; then
    echo "[!] Security vulnerabilities found. The Security Agent has blocked this commit."
    echo "[!] Refer to '.cursor/rules/05-security-agent.mdc' for auto-remediation steps."
    exit 1
fi

echo "[✔] Security check passed. Proceeding with commit."
exit 0
