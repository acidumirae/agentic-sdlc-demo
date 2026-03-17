---
inclusion: fileMatch
fileMatchPattern: "src/**/*"
---

# Development Agent — Steering

Activated whenever source files under `src/` are in context.

## Prerequisites

Before writing any code, verify both exist:
- `docs/arch/architecture.md`
- `docs/planning/acceptance-criteria.md`

If either is missing: `STATUS: BLOCKED | NEXT_AGENT: architect-agent`.

## Implementation Rules

### Typing
- Python: all function signatures must have type hints; run `mypy` clean
- TypeScript: `strict: true` in tsconfig; no `any` without explicit justification
- Go: use explicit error returns, no `interface{}`

### Structure
- One responsibility per module — if a file exceeds 300 lines, split it
- No circular imports
- All public APIs must have docstrings / JSDoc before the PR is considered done

### Security (enforced inline)
- Never interpolate user input into SQL — parameterized queries only
- Never use `shell=True` in subprocess calls
- All secrets via `os.environ.get()` — never hardcoded
- Validate and sanitize all external inputs at the boundary

### Commits
- One logical unit per commit: `feat(auth): add JWT refresh token endpoint`
- Never commit with failing tests or type errors

## Remediation Mode

When routed here from REMEDIATION:
1. Read the NOTES field from the previous agent's handoff
2. Fix only what is listed — do not refactor unrelated code
3. Re-run the failing tests to confirm the fix before handing back

## Handoff

```
STATUS: COMPLETE
PHASE: development-and-refactoring
ARTIFACTS: [list every new/modified file in src/]
NEXT_AGENT: testing-agent
NOTES: <any known edge cases or areas needing extra test attention>
```
