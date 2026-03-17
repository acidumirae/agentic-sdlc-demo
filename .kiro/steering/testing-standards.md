---
inclusion: fileMatch
fileMatchPattern: "tests/**/*,src/**/*.test.*,src/**/*.spec.*"
---

# Testing Agent — Standards

Activated when test files or spec files are in context.

## Test Hierarchy

1. Unit tests — every function with logic, mocked dependencies
2. Integration tests — service boundaries, DB interactions, API contracts
3. E2E tests — critical user journeys from user stories
4. Security tests — auth bypass, injection, boundary inputs

## Coverage Requirements

- New features: minimum 90% line coverage
- Security-critical paths (auth, payments, data access): 100%
- Bug fixes: must include a regression test that fails before the fix

## Test Structure (AAA Pattern)

```
// Arrange — set up state and inputs
// Act — invoke the unit under test  
// Assert — verify outcomes and side effects
```

## Edge Cases — Always Test

- Null / undefined / empty inputs
- Boundary values (0, -1, MAX_INT)
- Concurrent/race conditions on shared state
- Network timeouts and partial failures
- Unauthenticated and unauthorized access attempts

## Bug Fix Protocol

1. Write a failing test that reproduces the bug
2. Confirm it fails on current code
3. Implement the fix
4. Confirm the test now passes
5. Check no existing tests regressed
