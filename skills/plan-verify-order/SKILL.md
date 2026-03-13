---
name: plan-verify-order
description: "Define the narrow-to-broad verification map before changing code. Use when the immediate job is to decide how success will be verified, not to implement the change yet."
---

# Plan / Verify Order

## Purpose
Lock a concrete verification path before implementation work starts.

## Default Program
```text
[stages: preflight>detect>plan>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{tests},deterministic-output | lens: kent-beck | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kent-beck` because it keeps the work aligned with: Small safe iterations with explicit Red-Green-Refactor rhythm.

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
- `why`: Verification mapping should stage narrow checks before broader gates to keep feedback fast and safe.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: verification-map.v1

## Neutrality Rules
- Do not mark a check sufficient if it does not cover the claimed change risk.
- Separate required checks from optional confidence checks.
- Keep verification steps executable and bounded.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Show verification in order:
1. Narrow check — [command or test] — pass signal: [what to look for]
2. Broader check — [command or test] — pass signal: [what to look for]

List stop conditions explicitly:
- [condition] — blocks claiming success because: [why]

Ask: "Run narrow checks first? Or is [specific risk area] the higher priority?"

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
