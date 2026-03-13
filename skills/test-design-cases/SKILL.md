---
name: test-design-cases
description: "Test-category design skill. Define the exact happy-path, edge-case, and failure-path matrix before or alongside test writing. Use when the immediate job is to map what must be tested, not to write all tests yet."
---

# Test / Design Cases

## Purpose
Make regression test coverage explicit before test implementation.

## Default Program
```text
[stages: preflight>detect>analyze>plan>handoff>audit | scope: diff|paths(glob,...) | policy: evidence,quality-gates{tests},deterministic-output | lens: kent-beck | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kent-beck` because it keeps the work aligned with: Small safe iterations with explicit Red-Green-Refactor rhythm.

## Use When
- Need a test matrix before writing or extending tests.
- Need to prioritize happy, edge, and failure-path scenarios.
- Need to map missing regression protection precisely.

## Do Not Use When
- Tests are already written and only execution evidence is needed.
- Need a broad review rather than test-design output.
- There is no bounded behavior or change target.
- Need ordered verification steps and stop conditions rather than a case inventory.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Behavior or module under test.
- `TEST_GOAL` (regression|edge-case|failure-path|mixed; required): Primary testing objective.
- `TARGET_BEHAVIORS` (list; required; shape: {BEHAVIOR, WHY_IT_MATTERS}): Behaviors or cases that must be covered.

## Input Contract Notes
- TARGET_BEHAVIORS should describe observable behavior rather than implementation internals.
- TEST_GOAL prioritizes the matrix focus but should not suppress other high-risk cases that are explicitly in scope.
- Do not treat raw coverage percentage as a substitute for naming the exact behavior that must stay protected.

## Structured Outputs
- `HAPPY_PATH_CASES` (list; required; shape: {CASE, EXPECTED_SIGNAL}): Core success scenarios.
- `EDGE_CASES` (list; required; shape: {CASE, EXPECTED_SIGNAL}): Boundary conditions and atypical inputs.
- `FAILURE_CASES` (list; required; shape: {CASE, EXPECTED_SIGNAL}): Failure-path or error-handling scenarios.

## Output Contract Notes
- Use HAPPY_PATH_CASES, EDGE_CASES, and FAILURE_CASES to inventory the behavior matrix, not to prescribe execution order.
- Cases may be empty in one bucket when the target behavior genuinely does not require that category.
- Keep each case externally observable and suitable for regression protection.
- Do not turn the matrix into an exhaustive cartesian product when risk does not justify it.

## Primary Lens
- `primary_lens`: `kent-beck`
- `why`: Regression planning should enumerate small safe cases that protect behavior during change.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: test-design-cases.v1

## Neutrality Rules
- List observable behavior, not implementation-detail assertions.
- Do not inflate speculative cases into mandatory tests without risk evidence.
- Keep the matrix bounded and actionable.

## Response Format

Show the case matrix grouped by bucket:

Happy path:
- [case] — expected signal: [observable pass condition]

Edge cases:
- [case] — expected signal: [what distinguishes this from the happy path]

Failure cases:
- [case] — expected signal: [what the code should do instead of silently failing]

Ask: "Cover [highest-risk gap case] now, or want full matrix written first?"

## Execution Constraints
- Do not turn this skill into a verification-sequencing plan; it owns case inventory only.
- Prefer the smallest set of cases that protects real behavior under change.
- Keep bucket labels honest rather than forcing every case into every category.
- Do not prescribe framework-specific assertions or mock strategy here; that belongs to `test-write-guards`.

## Example Invocation
```text
$test-design-cases
TARGET_SCOPE: src/auth
TEST_GOAL: mixed
TARGET_BEHAVIORS: login success, invalid token, session refresh
```
