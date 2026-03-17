#!/usr/bin/env bash

# .kiro/hooks/post-merge.sh
# Trigger the Deployment Agent when code is merged to main.

echo "Kiro SDLC: Code merged. Initiating predictive deployment..."

# Invoke the Deployment Agent via skill
python3 .kiro/skills/deployment_predictor.py

if [ $? -eq 0 ]; then
    echo "[✔] Deployment predicted successful. Triggering CD pipeline."
    # Simulate trigger
else
    echo "[!] Deployment prediction failed. The Deployment Agent has halted the rollout."
    echo "[!] Notifying the Development and Testing agents to remediate."
fi
