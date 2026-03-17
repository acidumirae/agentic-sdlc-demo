---
inclusion: fileMatch
fileMatchPattern: "src/**/*,tests/**/*,.github/workflows/*,docker*,k8s/**/*,infra/**/*"
---

# Security Agent — Baseline Rules

Activated whenever source, test, CI/CD, or infrastructure files are in context.

## Mandatory Checks

### Code Review
- SQL injection: all DB queries must use parameterized statements
- XSS: all user-supplied output must be escaped/sanitized
- CSRF: state-mutating endpoints must require tokens
- Auth: verify JWT/session validation on every protected route
- Secrets: no API keys, passwords, or tokens in source — use env vars

### Dependency Audit
- Flag any dependency with a known CVE (CVSS >= 7.0 = block, 4.0-6.9 = warn)
- Verify lock files are committed and match declared versions

### Infrastructure
- No wildcard IAM policies
- All storage buckets/blobs must have public access disabled by default
- TLS required on all external endpoints
- Secrets must come from a secrets manager (Vault, AWS SSM, etc.)

## Auto-Remediation Protocol

When a vulnerability is found:
1. Do NOT just warn — provide the patched code inline
2. Write a test that would have caught the vulnerability
3. Add the pattern to `.kiro/specifications/security-patterns.yaml`
4. Report: `[SECURITY-BLOCK]` if critical, `[SECURITY-WARN]` if moderate
