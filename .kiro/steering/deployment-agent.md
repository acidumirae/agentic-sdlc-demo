---
inclusion: fileMatch
fileMatchPattern: "infra/**/*,k8s/**/*,deploy/**/*,.github/workflows/**/*,Dockerfile*,docker-compose*"
---

# Deployment Agent — Steering

Activated when infrastructure, CI/CD, or container files are in context.

## Prerequisites (hard gates — do not proceed without both)

- `docs/reports/coverage-report.md` must exist and show coverage >= 90%
- `docs/reports/security-report.md` must exist and show zero critical findings

If either gate fails: `STATUS: BLOCKED | NEXT_AGENT: <testing-agent|security-agent>`.

## Deployment Strategy

Default: canary rollout
```
10% → 30% → 50% → 80% → 100%
interval: 5 minutes between increments
```

Rollback triggers (automatic):
- `error_rate > 1%` over any 1-minute window
- `latency_p99 > 500ms` sustained for 2 minutes
- Any unhandled exception spike > baseline + 3σ

## Infrastructure Rules

- All IaC (Terraform, CloudFormation, Pulumi) must pass `tfsec` / `checkov` before apply
- No wildcard IAM — every policy scoped to minimum required actions
- All secrets injected via secrets manager (Vault, AWS SSM, GCP Secret Manager)
- TLS required on all external-facing endpoints
- Enable access logging on all load balancers and API gateways

## CI/CD Pipeline Integration

Before triggering deployment:
1. Run `deployment_predictor.py <commit_hash>` — halt if risk_score > 0.5
2. Confirm both test and security sign-offs are present in `docs/reports/`
3. Write `docs/reports/deployment-runbook.md` with rollout plan and rollback procedure

## Incident Response

If post-deployment metrics breach rollback triggers:
1. Immediately execute rollback to previous stable release
2. Write incident report to `docs/reports/incident-<timestamp>.md`
3. Route `STATUS: FAIL` back to development-agent with root cause notes
