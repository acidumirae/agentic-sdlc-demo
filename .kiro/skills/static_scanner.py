#!/usr/bin/env python3
"""
Skill: static_scanner
Agent: security-agent
Phase: security-review

Performs SAST, secret detection, dependency CVE scanning, and
IaC misconfiguration checks. Blocks pipeline on critical findings.
"""

import sys
import os
import re
import subprocess
from pathlib import Path
from typing import Any


# Patterns from .kiro/specifications/security-patterns.yaml
SECURITY_PATTERNS: list[dict[str, Any]] = [
    {
        "id": "SEC-001", "severity": "critical", "name": "SQL Injection",
        "pattern": re.compile(r'(f"|f\').*?(WHERE|SELECT|INSERT|UPDATE|DELETE)', re.IGNORECASE),
        "remediation": "Use parameterized queries or ORM query builders",
    },
    {
        "id": "SEC-002", "severity": "critical", "name": "Hardcoded Secret",
        "pattern": re.compile(r'(api_key|password|secret|token)\s*=\s*["\'][^"\']{8,}', re.IGNORECASE),
        "remediation": "Move to environment variables or a secrets manager",
    },
    {
        "id": "SEC-003", "severity": "high", "name": "Dangerous HTML Injection",
        "pattern": re.compile(r'innerHTML|dangerouslySetInnerHTML|document\.write', re.IGNORECASE),
        "remediation": "Use textContent or a sanitization library (DOMPurify)",
    },
    {
        "id": "SEC-004", "severity": "high", "name": "Wildcard IAM Policy",
        "pattern": re.compile(r'"Action"\s*:\s*"\*"|"Resource"\s*:\s*"\*"'),
        "remediation": "Scope IAM policies to minimum required actions and resources",
    },
    {
        "id": "SEC-005", "severity": "critical", "name": "Shell Injection",
        "pattern": re.compile(r'subprocess\.(call|run|Popen)\(.*shell\s*=\s*True'),
        "remediation": "Pass command as a list, never use shell=True with user input",
    },
]

SCANNABLE_EXTENSIONS = {".py", ".ts", ".js", ".tsx", ".jsx", ".tf", ".yaml", ".yml", ".json"}


def scan_file(file_path: str) -> list[dict[str, Any]]:
    """Scan a single file for known vulnerability patterns."""
    findings: list[dict[str, Any]] = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except OSError:
        return findings

    for lineno, line in enumerate(lines, start=1):
        for pattern in SECURITY_PATTERNS:
            if pattern["pattern"].search(line):
                findings.append({
                    "file": file_path,
                    "line": lineno,
                    "rule": pattern["id"],
                    "severity": pattern["severity"],
                    "name": pattern["name"],
                    "snippet": line.strip(),
                    "remediation": pattern["remediation"],
                })
    return findings


def scan_directory(src_path: str) -> list[dict[str, Any]]:
    """Recursively scan all source files in a directory."""
    all_findings: list[dict[str, Any]] = []
    for root, _, files in os.walk(src_path):
        # Skip node_modules, .git, venv
        if any(skip in root for skip in ["node_modules", ".git", "venv", "__pycache__"]):
            continue
        for fname in files:
            if Path(fname).suffix in SCANNABLE_EXTENSIONS:
                all_findings.extend(scan_file(os.path.join(root, fname)))
    return all_findings


def run_dependency_audit() -> list[dict[str, Any]]:
    """
    Run dependency vulnerability audit using available package managers.
    Supports: pip-audit, npm audit, yarn audit.
    """
    findings: list[dict[str, Any]] = []

    # pip-audit
    if os.path.exists("requirements.txt") or os.path.exists("pyproject.toml"):
        result = subprocess.run(["pip-audit", "--format=json"], capture_output=True, text=True)
        if result.returncode != 0:
            findings.append({
                "rule": "SEC-DEP", "severity": "high",
                "name": "Vulnerable Python Dependency",
                "snippet": result.stdout[:200],
                "remediation": "Run `pip-audit --fix` or upgrade affected packages",
            })

    # npm audit
    if os.path.exists("package.json"):
        result = subprocess.run(["npm", "audit", "--json"], capture_output=True, text=True)
        if result.returncode != 0:
            findings.append({
                "rule": "SEC-DEP", "severity": "high",
                "name": "Vulnerable NPM Dependency",
                "snippet": "Run `npm audit` for details",
                "remediation": "Run `npm audit fix` or upgrade affected packages",
            })

    return findings


def write_security_report(findings: list[dict[str, Any]], output_path: str) -> None:
    """Write a structured security report to docs/reports/security-report.md."""
    Path(os.path.dirname(output_path)).mkdir(parents=True, exist_ok=True)
    critical = [f for f in findings if f.get("severity") == "critical"]
    high = [f for f in findings if f.get("severity") == "high"]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Security Review Report\n\n")
        f.write(f"**Total findings:** {len(findings)}  \n")
        f.write(f"**Critical:** {len(critical)}  \n")
        f.write(f"**High:** {len(high)}  \n\n")

        if not findings:
            f.write("✅ No vulnerabilities detected.\n")
            return

        f.write("## Findings\n\n")
        for finding in findings:
            f.write(f"### [{finding.get('severity', 'unknown').upper()}] {finding.get('name', 'Unknown')}\n\n")
            if "file" in finding:
                f.write(f"- **File:** `{finding['file']}` (line {finding.get('line', '?')})\n")
            f.write(f"- **Rule:** {finding.get('rule', 'N/A')}\n")
            f.write(f"- **Snippet:** `{finding.get('snippet', '')}`\n")
            f.write(f"- **Remediation:** {finding.get('remediation', '')}\n\n")


def main() -> int:
    """Entry point for the Security Agent skill."""
    scan_path = sys.argv[1] if len(sys.argv) > 1 else "src"
    report_path = sys.argv[2] if len(sys.argv) > 2 else "docs/reports/security-report.md"

    # Handle --diff flag for pre-commit hook usage
    if "--diff" in sys.argv:
        diff_result = subprocess.run(["git", "diff", "--cached", "--name-only"],
                                     capture_output=True, text=True)
        changed_files = [f for f in diff_result.stdout.splitlines()
                         if Path(f).suffix in SCANNABLE_EXTENSIONS]
        findings = []
        for f in changed_files:
            if os.path.exists(f):
                findings.extend(scan_file(f))
    else:
        print(f"[Security Agent] Scanning {scan_path}/")
        findings = scan_directory(scan_path)
        print(f"[Security Agent] Running dependency audit...")
        findings.extend(run_dependency_audit())

    critical = [f for f in findings if f.get("severity") == "critical"]

    print(f"[Security Agent] Found {len(findings)} issue(s) ({len(critical)} critical)")
    for f in findings:
        tag = "[SECURITY-BLOCK]" if f.get("severity") == "critical" else "[SECURITY-WARN]"
        loc = f"  {f.get('file', '')}:{f.get('line', '')}" if "file" in f else ""
        print(f"  {tag} {f.get('name')}{loc}")
        print(f"    → {f.get('remediation')}")

    write_security_report(findings, report_path)
    print(f"\n[Security Agent] Report written to {report_path}")

    if critical:
        print("\nSTATUS: FAIL | PHASE: security-review | NEXT_AGENT: development-agent (remediation)")
        return 1

    print("\nSTATUS: COMPLETE | PHASE: security-review | NEXT_AGENT: deployment-agent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
