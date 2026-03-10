---
name: plan-verify-order
description: "Define the narrow-to-broad verification map before changing code. Use when the immediate job is to decide how success will be verified, not to implement the change yet."
---

# Verification Map Plan

## Purpose
Lock a concrete verification path before implementation work starts.

## Default Program
```text
[stages: preflight>detect>plan>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{tests},deterministic-output | lens: kent-beck | output: md(contract=v1)]
```

## Use When
- Need to define how a code change will be verified before patching.
- Need narrow-to-broad verification steps for a bounded task.
- Need to separate smoke checks from broader quality gates.

## Do Not Use When
- Implementation is already complete and only execution evidence is needed.
- Need a general plan rather than verification design.
- There is no bounded target change yet.
- Need an exhaustive happy, edge, and failure case inventory rather than verification order and stop conditions.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Scope of the planned change.
- `CHANGE_GOAL` (string; required): Behavior or structure that will change.
- `RISK_AREAS` (list; optional; shape: {RISK, WHY_IT_MATTERS}): Known regression or safety concerns.

## Input Contract Notes
- CHANGE_GOAL should describe the bounded change being prepared, not the implementation method.
- RISK_AREAS should identify concrete regression or safety concerns instead of broad anxiety terms such as `quality`.

## Structured Outputs
- `NARROW_CHECKS` (list; required; shape: {CHECK, PURPOSE, PASS_SIGNAL}): Cheapest local checks that confirm the change.
- `BROADER_CHECKS` (list; required; shape: {CHECK, PURPOSE, PASS_SIGNAL}): Broader tests or validations to run after local checks.
- `STOP_CONDITIONS` (list; required; shape: {CONDITION, WHY_BLOCKING}): Conditions that should block claiming success.

## Output Contract Notes
- NARROW_CHECKS should come first in execution order and should be the cheapest checks that can falsify the planned change quickly.
- BROADER_CHECKS should cover wider confidence only after the narrow checks pass.
- Use STOP_CONDITIONS for explicit block claims, not for generic caution notes.

## Primary Lens
- `primary_lens`: `kent-beck`
- `frame_name`: Small-Safe Feedback Driver
- `why`: Verification mapping should stage narrow checks before broader gates to keep feedback fast and safe.
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
- `artifacts_out`: verification-map.v1

## Neutrality Rules
- Do not mark a check sufficient if it does not cover the claimed change risk.
- Separate required checks from optional confidence checks.
- Keep verification steps executable and bounded.

## Execution Constraints
- Do not turn this skill into a full regression test inventory; focus on ordered verification path and stop conditions.
- Prefer the smallest discriminating checks before broad suites or manual confidence work.
- Keep each check directly tied to the stated change goal or risk area.

## Example Invocation
```text
$plan-verify-order
TARGET_SCOPE: src/auth
CHANGE_GOAL: persist session across refresh
```

## Output Discipline
- `response_profile=planning_doc`
- User-facing rendering is delegated to `respond`.
