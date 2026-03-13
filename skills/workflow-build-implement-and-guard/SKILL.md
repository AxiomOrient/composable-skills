---
name: workflow-build-implement-and-guard
description: "Workflow skill that implements a bounded change and immediately follows with regression-guard work. Use when the user needs one default build entrypoint instead of separately invoking implementation and test-guard skills."
---

# Workflow / Build & Guard

## Purpose
Compose implementation and regression-guard writing into one default build workflow.

## Default Program
```text
[stages: preflight>detect>implement>verify>review>audit | scope: diff|paths(glob,...) | policy: evidence,correctness-first,quality-gates{tests,security},deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need to implement a bounded change and leave regression guards in the same run.
- Need one default build entrypoint for category-first discovery.
- Need implementation evidence plus concrete follow-up test protection.

## Do Not Use When
- Need planning or scope clarification before coding.
- Need only test-gap analysis without changing code.
- Need only direct implementation without test guard follow-up.

## Required Inputs
- `CHANGE_GOAL` (string; required): Core behavior or structure to change.
- `IMPLEMENTATION_MODE` (bugfix|feature|refactor|integration|cleanup; optional): Implementation mode. Defaults to the narrowest mode implied by the change goal.
- `TARGET_SCOPE` (path|module|folder|repo; required): Scope of the code changes.
- `TASK_IDS` (list; optional; shape: {TASK_ID}): Task ids to implement or synthesized adhoc ids when no task ledger exists.
- `VERIFICATION_MAP` (list; required; shape: {CHECK, ORDER, PASS_CONDITION}): Narrow-to-broad verification steps.
- `TARGET_BEHAVIORS` (list; required): Behaviors that the guard tests must protect.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Safety, rollout, compatibility, or non-goal constraints.

## Input Contract Notes
- TARGET_BEHAVIORS should describe observable behavior rather than implementation detail.
- Use this workflow when code and tests should move together, not when the only goal is green CI.
- TASK_IDS should remain stable enough that execution evidence can point back to the task ledger when one exists. If omitted, synthesize one stable `adhoc/...` id for this run.

## Structured Outputs
- `CHANGED_ARTIFACTS` (list; required; shape: {PATH, CHANGE_KIND, WHY}): Files changed by implementation or guard writing.
- `VERIFICATION_RESULTS` (list; required; shape: {CHECK, RESULT, EVIDENCE}): Executed verification checks.
- `ADDED_TESTS` (list; required): Guard tests added or updated.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Actual atomic path executed by the workflow.

## Output Contract Notes
- CHANGED_ARTIFACTS should include both code and test changes when both happen.
- VERIFICATION_RESULTS should stay grounded in executed checks.
- EXPANDED_ATOMIC_PATH must preserve execution order explicitly.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: implementation-delta.v1, test-report.v1

## Neutrality Rules
- Preserve the neutrality rules of build-write-code and test-write-guards.
- Do not report regression protection that was not actually added or verified.
- Keep code change evidence separate from future cleanup ideas.

## Execution Constraints
- Do not inflate the workflow into a planning or architecture pass.
- Keep the test guard work bounded to the same contract as the code change.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

구현과 테스트를 함께 출력.

```
변경: `파일:줄` — 설명
테스트: `테스트명` → ✓
```

테스트 실패 시 즉시:
> "테스트 실패: [이유] — 계속 진행할까요?"

## Mandatory Rules
- Expose the expanded atomic path explicitly.
- Keep the workflow bounded to one implementation contract.

## Expansion
- `$build-write-code`
- `$test-write-guards`

## Example Invocation
```text
$workflow-build-implement-and-guard
CHANGE_GOAL: keep the session after refresh
TARGET_SCOPE: src/session
TASK_IDS:
  - TASK_ID: auth/session-refresh
VERIFICATION_MAP:
  - CHECK: session refresh test
    ORDER: 1
    PASS_CONDITION: stay signed in after refresh
TARGET_BEHAVIORS:
  - keep the session after refresh during an active login
```
