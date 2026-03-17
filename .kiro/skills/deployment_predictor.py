#!/usr/bin/env python3
"""
Skill: deployment_predictor
Agent: deployment-agent
Phase: deployment-and-operations

Evaluates CI/CD telemetry and test/security reports to produce a
risk score, then executes a canary rollout or halts the pipeline.
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Any


def load_report(path: str) -> dict[str, Any]:
    """Load a JSON or markdown report file, returning parsed content."""
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Attempt JSON parse; fall back to raw text dict
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"raw": content}


def calculate_risk_score(
    coverage: int,
    critical_vulns: int,
    high_vulns: int,
    test_pass_rate: float,
    recent_rollback_count: int,
) -> float:
    """
    Compute a 0.0–1.0 deployment risk score.
    Higher = more risky. Score > 0.5 halts deployment.
    """
    score = 0.0
    if coverage < 90:
        score += (90 - coverage) / 100
    score += critical_vulns * 0.30
    score += high_vulns * 0.10
    score += (1.0 - test_pass_rate) * 0.25
    score += min(recent_rollback_count * 0.05, 0.20)
    return min(round(score, 3), 1.0)


def parse_telemetry(commit_hash: str) -> dict[str, Any]:
    """
    Pull CI/CD telemetry for the given commit.
    In production: query your CI API (GitHub Actions, Jenkins, etc.)
    """
    # Mock telemetry — replace with real API calls
    return {
        "commit": commit_hash,
        "test_pass_rate": 0.97,
        "coverage": 93,
        "critical_vulns": 0,
        "high_vulns": 1,
        "recent_rollback_count": 0,
        "avg_build_time_seconds": 142,
        "flaky_test_count": 2,
    }


def write_runbook(
    commit_hash: str,
    risk_score: float,
    telemetry: dict[str, Any],
    strategy: str,
    output_path: str,
) -> None:
    """Write a deployment runbook to docs/reports/deployment-runbook.md."""
    Path(os.path.dirname(output_path)).mkdir(parents=True, exist_ok=True)
    decision = "APPROVED" if risk_score <= 0.5 else "HALTED"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Deployment Runbook — {commit_hash}\n\n")
        f.write(f"**Decision:** {decision}  \n")
        f.write(f"**Risk Score:** {risk_score}  \n")
        f.write(f"**Strategy:** {strategy}  \n\n")
        f.write("## Telemetry Summary\n\n")
        for key, val in telemetry.items():
            f.write(f"- **{key}:** {val}\n")
        f.write("\n## Rollout Plan\n\n")
        if decision == "APPROVED":
            f.write("1. Deploy 10% canary — monitor error rate and p99 latency for 5 min\n")
            f.write("2. Increment to 30%, 50%, 80%, 100% at 5-minute intervals\n")
            f.write("3. Rollback trigger: error_rate > 1% OR latency_p99 > 500ms\n")
        else:
            f.write("Pipeline halted. Notify development-agent and testing-agent to remediate.\n")
            f.write(f"Blocking factors: risk_score={risk_score} exceeds threshold of 0.5\n")


def trigger_canary_deploy(commit_hash: str) -> bool:
    """
    Trigger canary deployment via CI/CD API.
    In production: call GitHub Actions workflow_dispatch, ArgoCD, or Spinnaker.
    """
    print(f"  [✔] Canary rollout initiated for {commit_hash} (10% traffic)")
    print("  [✔] Monitoring: error_rate, latency_p99, saturation")
    return True


def main() -> int:
    """Entry point for the Deployment Agent skill."""
    commit_hash = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    strategy = sys.argv[2] if len(sys.argv) > 2 else "canary"
    runbook_path = "docs/reports/deployment-runbook.md"

    print(f"[Deployment Agent] Analyzing telemetry for commit: {commit_hash}")
    telemetry = parse_telemetry(commit_hash)

    risk_score = calculate_risk_score(
        coverage=telemetry.get("coverage", 0),
        critical_vulns=telemetry.get("critical_vulns", 99),
        high_vulns=telemetry.get("high_vulns", 0),
        test_pass_rate=telemetry.get("test_pass_rate", 0.0),
        recent_rollback_count=telemetry.get("recent_rollback_count", 0),
    )

    print(f"[Deployment Agent] Risk score: {risk_score} (threshold: 0.5)")
    write_runbook(commit_hash, risk_score, telemetry, strategy, runbook_path)
    print(f"[Deployment Agent] Runbook written to {runbook_path}")

    if risk_score > 0.5:
        print("[!] High failure probability. Halting deployment pipeline.")
        print("\nSTATUS: FAIL | PHASE: deployment-and-operations | NEXT_AGENT: development-agent")
        return 1

    print(f"[✔] Deployment approved. Initiating {strategy} rollout...")
    trigger_canary_deploy(commit_hash)
    print("\nSTATUS: COMPLETE | PHASE: deployment-and-operations | NEXT_AGENT: none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
