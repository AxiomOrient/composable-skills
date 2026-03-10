---
name: test-find-gaps
description: "Test-category gap-analysis skill. Review whether a bounded scope is missing regression tests for core behavior, failure paths, or boundary contracts. Use when the goal is test-gap analysis rather than writing tests immediately."
---

# Test Gap Review

## Purpose
Identify exact regression-prevention gaps in a bounded target before test implementation.

## Default Program
```text
[stages: preflight>detect>analyze>review>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: kent-beck | output: md(contract=v1)]
```

## Use When
- Need to know what is not covered by current tests.
- Need to review test gaps for core behavior, edge cases, or failure paths.
- Need evidence-backed test priorities before adding tests.

## Do Not Use When
- Need to write the tests immediately without first reviewing gaps.
- Need a broad code review unrelated to test coverage.
- There is no bounded target scope.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Scope to inspect for missing tests.
- `TEST_FOCUS` (core-behavior|edge-cases|failure-paths|boundary-contracts|mixed; required): Which test gap category to prioritize.

## Input Contract Notes
- TARGET_SCOPE should point to a bounded behavior surface, not the whole repo unless the repo is the real unit under test.
- TEST_FOCUS should guide prioritization, not preload the claim that missing tests definitely exist in that category.
- Do not assume a gap just because a nearby file lacks tests; use observable current coverage as the baseline.

## Structured Outputs
- `MISSING_TEST_SCENARIOS` (list; required; shape: {SCENARIO, RISK, CHEAPEST_TEST}): Important scenarios that lack regression protection.
- `CURRENT_COVERAGE_NOTES` (list; required; shape: {COVERED_BEHAVIOR, EVIDENCE}): What the current test suite does cover.
- `TEST_PRIORITY_ORDER` (list; required; shape: {TEST, WHY_NOW}): Ordered list of the cheapest high-value tests to add.

## Output Contract Notes
- CURRENT_COVERAGE_NOTES should describe observable coverage before declaring gaps.
- MISSING_TEST_SCENARIOS may be empty when current regression protection is already sufficient for the stated focus.
- TEST_PRIORITY_ORDER should rank by regression value and cheapest signal, not by raw scenario count.

## Procedure
1. Inspect the target behavior and the current tests that cover it.
2. List missing high-value regression scenarios by focus category.
3. Return a priority order for the cheapest useful tests to add.

## Primary Lens
- `primary_lens`: `kent-beck`
- `frame_name`: Small-Safe Feedback Driver
- `why`: Test-gap review should identify the smallest missing checks that guard real behavior.
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
- `artifacts_in`: none
- `artifacts_out`: test-gap-report.v1

## Neutrality Rules
- Describe current coverage before declaring a gap.
- Prioritize missing tests by risk and regression value, not by raw count.
- Separate missing tests from cases that are already covered indirectly.

## Execution Constraints
- Do not confuse low-level coverage metrics with meaningful behavioral gaps unless the missing behavior is explicit.
- Keep the report focused on regression protection rather than general code quality.
- Prefer the smallest useful next test over broad speculative test suites.
- Do not recommend tests whose only purpose is to satisfy CI or assert implementation trivia.

## Mandatory Rules
- Do not equate low line coverage with a meaningful test gap automatically.
- Keep the output scoped to missing regression protection.

## Example Invocation
```text
$test-find-gaps
TARGET_SCOPE: src/auth
TEST_FOCUS: failure-paths
```

## Output Discipline
- `response_profile=review_findings`
- User-facing rendering is delegated to `respond`.
