---
name: workflow-test-close-gaps
description: "Workflow skill that identifies missing regression protection, turns it into a behavior matrix, and writes guard tests. Use when the user needs one default test entrypoint instead of manually chaining gap review, test design, and test writing."
---

# Workflow / Test Close Gaps

## Purpose
Compose test-gap review, test-case design, and guard writing into one default test workflow.

## Default Program
```text
[stages: preflight>detect>analyze>plan>implement>verify>handoff>audit | scope: diff|paths(glob,...) | policy: evidence,quality-gates{tests,security},deterministic-output | lens: kent-beck | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kent-beck` because it keeps the work aligned with: Small safe iterations with explicit Red-Green-Refactor rhythm.

## Use When
- Need one default test entrypoint to close meaningful regression gaps.
- Need missing-test analysis, case design, and guard writing in one path.
- Need test work that stays tied to explicit behaviors.

## Do Not Use When
- Need only to inventory gaps without writing tests.
- Need direct feature implementation unrelated to tests.
- Need only a broad review rather than test-specific follow-up.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Scope under test.
- `TEST_GOAL` (regression|edge-case|failure-path|mixed; required): Primary testing objective.
- `TEST_LAYER` (unit|integration|contract|scenario; optional): Preferred layer for the written guard tests.
- `TARGET_BEHAVIORS` (list; required): Behaviors that must be protected.
- `FAILURE_PATHS` (list; optional): Known unhappy paths to include.

## Input Contract Notes
- TARGET_BEHAVIORS should be observable, contract-visible behavior.
- Use this workflow when the outcome should be actual guard tests, not only analysis.
- TEST_GOAL should prioritize the matrix focus but not hide explicit high-risk cases.
- TEST_LAYER is optional because the workflow can choose the cheapest effective layer when the request does not specify one.

## Structured Outputs
- `MISSING_TEST_SCENARIOS` (list; required; shape: {SCENARIO, RISK, CHEAPEST_TEST}): Regression scenarios that were missing before the workflow.
- `TEST_MATRIX` (object; required): Happy, edge, and failure-path case matrix.
- `ADDED_TESTS` (list; required): Guard tests added or updated.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Actual atomic path executed by the workflow.

## Output Contract Notes
- MISSING_TEST_SCENARIOS should reflect the pre-fix gap inventory rather than the final guard list only.
- TEST_MATRIX should remain behavior oriented.
- EXPANDED_ATOMIC_PATH must preserve execution order explicitly.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: test-gap-report.v1, test-design-cases.v1, test-report.v1

## Neutrality Rules
- Preserve the neutrality rules of the underlying test skills.
- Do not imply coverage for behavior the workflow did not actually guard.
- Keep behavior under test visible instead of hiding it behind framework details.

## Execution Constraints
- Do not widen the workflow into a generic code review.
- Prefer the smallest guard set that closes the meaningful regression gap.

## Response Format

Show per-step outcome (step → result):
- test-find-gaps → missing scenarios list
- test-design-cases → case matrix (happy / edge / failure)
- test-write-guards → tests added + verification results

On failure at any step: stop and ask what is blocking.

On success: show added tests and any remaining gaps.

Ask: "Cover [specific remaining gap] now?"

## Mandatory Rules
- Expose the expanded atomic path explicitly.
- Keep the workflow tied to observable behavior rather than implementation trivia.

## Expansion
- `$test-find-gaps`
- `$test-design-cases`
- `$test-write-guards`

## Example Invocation
```text
$workflow-test-close-gaps
TARGET_SCOPE: src/auth
TEST_GOAL: mixed
TARGET_BEHAVIORS:
  - password reset token validation
  - session persistence after login
```
