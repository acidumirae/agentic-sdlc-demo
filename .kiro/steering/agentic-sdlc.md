---
inclusion: always
---

# Agentic SDLC — Global Steering Rules

This workspace implements a fully autonomous multi-agent Software Development Life Cycle. All agents must adhere to these rules at all times.

## Phase Gate Enforcement

Agents MUST NOT proceed to a downstream phase without verified artifacts from the upstream phase:

| Phase | Required Input Artifact | Output Artifact |
|---|---|---|
| Requirements & Planning | Business goal / user prompt | `docs/planning/planning.md`, user stories |
| Design & Prototyping | `docs/planning/planning.md` | `docs/design/`, UI components |
| Development & Refactoring | `docs/arch/architecture.md` | `src/` implementation |
| Testing & Debugging | `src/` implementation | `tests/`, coverage report |
| Security Review | `src/` + `tests/` | Security report, patched code |
| Deployment & Operations | Passing tests + security clearance | Deployed artifact, runbook |

## Agent Handoff Protocol

When completing a phase, always:
1. Write the output artifact to disk at the documented path
2. Summarize what was produced and what the next agent needs
3. Tag the handoff with `[HANDOFF: <next-agent>]` in your response

## Orchestration Agent Authority

The Orchestration Agent has override authority. If it issues a directive, all other agents must comply immediately and halt current work.

## Coding Standards (enforced by Development Agent)

- Strict typing in all languages (TypeScript strict mode, Python type hints)
- SOLID principles, no god classes
- Every public function must have a docstring/JSDoc
- No hardcoded secrets — use environment variables
- Atomic commits per logical unit of work

## Security Baseline (enforced by Security Agent)

- OWASP Top 10 must be checked on every PR
- No known CVEs in direct dependencies
- Secrets scanning on every commit
- Least-privilege access in all infrastructure configs

## Test Coverage Baseline (enforced by Testing Agent)

- Minimum 90% line coverage for new code
- 100% coverage for security-critical paths
- All edge cases from user stories must have corresponding tests
