---
name: test-write-guards
description: "Test-category execution skill. Add or strengthen automated tests that act as real regression guards. Do not use for direct feature implementation, fake CI-only coverage, or diagnosing failures without a test-design intent."
---

# Test Guards

## Purpose
Add or improve regression-prevention tests with an explicit scenario matrix and execution evidence.

## Default Program
```text
[stages: preflight>detect>analyze>plan>implement>verify>review>handoff>audit |
 scope: diff|paths(glob,...) |
 policy: evidence,correctness-first,quality-gates{tests,security},deterministic-output |
 lens: kent-beck |
 output: md(contract=v1)]
```

## Use When
- Need to add or strengthen automated tests.
- Need to convert a regression risk into concrete test protection.
- Need a bounded test matrix plus implemented tests.

## Do Not Use When
- Need only to analyze missing test gaps.
- Need direct feature implementation unrelated to tests.
- Need only the scenario matrix before writing tests.
- Need to make CI green with low-value tests that do not protect real behavior.

## Required Inputs
- `TEST_GOAL` (regression|edge-case|failure-path|mixed, required): Primary testing objective.
- `TARGET_SCOPE` (path|module|folder|repo, required): Scope under test.
- `TARGET_BEHAVIORS` (list, required): Behaviors or scenarios to protect.
- `FAILURE_PATHS` (list, optional): Known unhappy paths to include.

## Input Contract Notes
- TARGET_BEHAVIORS should describe observable behavior, not helper calls, private methods, or implementation structure.
- FAILURE_PATHS should name user-visible or contract-visible failures when they matter.
- If the target behaviors are still fuzzy, use `test-design-cases` first instead of guessing test shapes.

## Structured Outputs
- `TEST_MATRIX` (object, required): Happy, edge, and failure-path scenario matrix.
- `ADDED_TESTS` (list, required): Added or updated tests.
- `VERIFICATION_RESULTS` (list, required): Executed test evidence.

## Output Contract Notes
- TEST_MATRIX should stay minimal and behavior-oriented; do not inflate it with low-value cases just to raise test count.
- ADDED_TESTS should map back to explicit target behaviors or failure paths.
- VERIFICATION_RESULTS should cite executed commands and observed pass/fail signals, not unrun claims.

## Primary Lens
- `primary_lens`: `kent-beck`
- `frame_name`: Small-Safe Feedback Driver
- `why`: Test design should prefer small safe tests tied to explicit behavior and refactor confidence.
- `summary`: Small safe iterations with explicit Red-Green-Refactor rhythm.
- `thesis`: When behavior must stay trustworthy during change, shorten the feedback loop, make the smallest useful check first, and let tests document intent.
- `decision_rules`:
  - Design the smallest test that discriminates the target behavior.
  - Sequence checks from narrow and cheap to broader and slower.
  - Prefer tests that protect behavior under change rather than mirror implementation details.
  - Use explicit behavior buckets: happy path, edge case, failure case.
- `anti_patterns`:
  - Large speculative test plans before identifying the core behavior
  - Tests coupled to implementation internals
  - Broad integration checks as the only guard
- `good_for`:
  - test design
  - regression planning
  - verification mapping
  - test-gap review
- `not_for`:
  - portfolio-level risk judgement
  - documentation navigation
  - architecture modernization strategy
- `required_artifacts`:
  - Behavior Under Test
  - Small Safe Steps
  - Happy, Edge, and Failure Cases
- `references`:
  - https://kentbeck.com/

## Artifacts
- `artifacts_in`: test-design-cases.v1, test-gap-report.v1
- `artifacts_out`: test-report.v1

## Neutrality Rules
- Prefer observable behavior over implementation-detail coupling.
- If a case is speculative, mark it optional instead of mandatory.
- Do not imply coverage the suite does not provide.

## Execution Constraints
- Do not write tests only to satisfy the current implementation details, mock call counts, or branch shape unless the contract explicitly requires that level.
- Do not add duplicate tests that restate already-proven behavior at the same layer.
- If the code has no clean seam for a valuable test, surface that seam problem instead of hiding it behind a brittle test.

## Output Discipline
- `response_profile=test_report`
- User-facing rendering is delegated to `respond`.
