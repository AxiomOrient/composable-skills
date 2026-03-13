---
name: test-write-guards
description: "Test-category execution skill. Add or strengthen automated tests that act as real regression guards. Do not use for direct feature implementation, fake CI-only coverage, or diagnosing failures without a test-design intent."
---

# Test / Write Guards

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

## Lens Rationale
This skill uses `kent-beck` because it keeps the work aligned with: Small safe iterations with explicit Red-Green-Refactor rhythm.

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
- `TEST_GOAL` (regression|edge-case|failure-path|mixed; required): Primary testing objective.
- `TEST_LAYER` (unit|integration|contract|scenario; optional; allowed: unit|integration|contract|scenario): Where the regression guard should live. Default to the cheapest layer that still protects the stated behavior.
- `TARGET_SCOPE` (path|module|folder|repo; required): Scope under test.
- `TARGET_BEHAVIORS` (list; required): Behaviors or scenarios to protect.
- `FAILURE_PATHS` (list; optional): Known unhappy paths to include.

## Input Contract Notes
- TARGET_BEHAVIORS should describe observable behavior, not helper calls, private methods, or implementation structure.
- TEST_LAYER chooses the guard layer, not the behavior under test.
- FAILURE_PATHS should name user-visible or contract-visible failures when they matter.
- If the target behaviors are still fuzzy, use `test-design-cases` first instead of guessing test shapes.

## Structured Outputs
- `TEST_MATRIX` (object; required; shape: {HAPPY_PATH, EDGE_CASES, FAILURE_CASES}): Happy, edge, and failure-path scenario matrix with one list per category.
- `ADDED_TESTS` (list; required; shape: {TEST_NAME, BEHAVIOR_COVERED, LAYER, FILE}): Added or updated tests with the behavior each one guards.
- `VERIFICATION_RESULTS` (list; required; shape: {CHECK, RESULT, COMMAND_OR_TEST, EVIDENCE}): Executed test commands and observed pass/fail signals.

## Output Contract Notes
- TEST_MATRIX should stay minimal and behavior-oriented; do not inflate it with low-value cases just to raise test count.
- ADDED_TESTS should map back to explicit target behaviors or failure paths.
- VERIFICATION_RESULTS should cite executed commands and observed pass/fail signals, not unrun claims.

## Primary Lens
- `primary_lens`: `kent-beck`
- `why`: Test design should prefer small safe tests tied to explicit behavior and refactor confidence.

## Artifacts
- `artifacts_in`: test-design-cases.v1, test-gap-report.v1
- `artifacts_out`: test-report.v1

## Neutrality Rules
- Prefer observable behavior over implementation-detail coupling.
- If a case is speculative, mark it optional instead of mandatory.
- Do not imply coverage the suite does not provide.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Show added tests as a compact list:
- [test name] — behavior covered: [what it guards] — layer: [unit/integration/contract] — file

Show verification results:
- [command or test] — result: PASS / FAIL — [key signal]

List any gaps not yet covered by the new guards.

Ask: "Cover [specific remaining gap] now?"

## Execution Constraints
- Do not write tests only to satisfy the current implementation details, mock call counts, or branch shape unless the contract explicitly requires that level.
- Do not add duplicate tests that restate already-proven behavior at the same layer.
- If the code has no clean seam for a valuable test, surface that seam problem instead of hiding it behind a brittle test.
