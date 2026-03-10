---
name: workflow-build-execute-loop
description: "Workflow that executes a plans/ task ledger end-to-end: implementation → per-task critique → task sync → delivery check → loop, until all tasks are done or a real blocker stops progress. Use when you have a plans/TASKS.md ledger and want zero-config full automation. For custom compose chains where you control the pipeline, use build-until-done instead."
---

# Workflow / Build Execute Loop

## Purpose
Drive plan-ledger-based implementation to full completion. This workflow IS the execution engine: it wires the complete cycle (implement → critique → sync → verify) and loops until all tasks are done. `build-until-done` serves as the oracle inside this workflow — it selects the next task and checks the overall done condition; the workflow is responsible for actually executing each step.

## Default Program
```text
[stages: preflight>detect>select>implement>critique>sync>verify>loop>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,correctness-first,quality-gates{tests,security},deterministic-output |
 lens: contract-evidence-verifier |
 output: md(contract=v1)]
```

## Use When
- Have a plans/TASKS.md ledger and want to execute all task rows without manual stepping.
- Need each implementation pass followed by a self-feedback critique before moving to the next task.
- Need the task ledger kept in sync automatically after each pass.
- Need to run until every task is done or a real blocker stops progress, not just one pass at a time.

## Do Not Use When
- Need custom control over which companion skills execute each pass — use `build-until-done` in a compose chain instead.
- Need only a single-pass implementation — use `build-write-code` directly.
- Need planning or task breakdown first — use `workflow-plan-build-ready` to create the plan, then use this workflow.
- Need non-code work (docs, review, release) — use `finish-until-done` instead.

## Required Inputs
- `MISSION_GOAL` (string; required): One bounded mission to execute until all task rows are done or a real blocker stops progress.
- `TARGET_SCOPE` (path|module|folder|repo; required): Scope the loop is allowed to touch.
- `DONE_CONDITION` (list; required; shape: {CONDITION, PROOF_REQUIRED}): Explicit completion contract and the evidence required for each condition.
- `PLAN_ARTIFACTS` (list; optional; shape: {PATH, ROLE}): Implementation plan and tasks ledger to consume. Defaults to `plans/IMPLEMENTATION-PLAN.md` and `plans/TASKS.md` when omitted. When absent, iterates from DONE_CONDITION.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Safety, rollout, compatibility, or non-goal constraints.

## Input Contract Notes
- DONE_CONDITION must contain externally checkable conditions, not vibe-based success language.
- When PLAN_ARTIFACTS is provided, treat every incomplete task row as active work to consume.
- When PLAN_ARTIFACTS is absent, drive iteration from DONE_CONDITION and fresh evidence.
- CONSTRAINTS should be explicit about non-goals so the loop does not drift into adjacent cleanup.

## Structured Outputs
- `MISSION_STATUS` (continue|done|blocked; required): Overall loop status after this run.
- `TASK_EXECUTION_LOG` (list; required; shape: {TASK_ID, IMPLEMENTATION_SUMMARY, FEEDBACK_APPLIED, SYNC_STATUS}): Per-task execution record.
- `DONE_CONDITION_STATUS` (list; required; shape: {CONDITION, STATUS, EVIDENCE_OR_GAP}): Per-condition check against the done contract.
- `BLOCKERS` (list; optional): Real blockers that stopped the loop and what would unblock them.
- `LOOP_EXIT_REASON` (string; required): Why the loop exited.

## Execution Flow (per task cycle)
1. **Select** — `build-until-done` reads the task ledger and selects the next incomplete task row.
2. **Implement** — `build-write-code` applies the code change for the selected task.
3. **Critique** — `check-improve-loop` reviews the implementation, applies the highest-value fix, and confirms the quality bar is met.
4. **Sync** — `plan-sync-tasks` marks the task row as done and records evidence in the task ledger.
5. **Verify** — `check-final-verify` confirms the done condition for the current task.
6. **Loop** — `build-until-done` checks the overall DONE_CONDITION. If more tasks remain, returns to step 1. If done or blocked, exits.

`build-until-done` is used in steps 1 and 6 as a loop oracle — task selection and exit decision only. The workflow drives execution; `build-until-done` does not.

## Primary Lens
- `primary_lens`: `contract-evidence-verifier`
- `why`: Each cycle must prove the done condition before advancing, not assume progress from momentum.

## Artifacts
- `artifacts_in`: plans/IMPLEMENTATION-PLAN.md, plans/TASKS.md (optional)
- `artifacts_out`: completion-contract-loop-report.v1, task-sync-report.v1

## Neutrality Rules
- Do not mark a task done unless the per-task done condition has evidence.
- Do not skip the self-feedback pass for speed.
- If the task ledger is absent, iterate from DONE_CONDITION without inventing task rows.

## Expansion
- `$build-write-code`
- `$check-improve-loop`
- `$plan-sync-tasks`
- `$check-final-verify`
- `$build-until-done`

## Example Invocation

플랜 있을 때 (plans/TASKS.md 기반 전체 실행):
```text
$compose + $workflow-build-execute-loop + @plans/IMPLEMENTATION-PLAN.md + @plans/TASKS.md + [모든 태스크 완료까지 실행]
GOAL: 세션 갱신 버그 수정
SCOPE: src/auth
DONE: 모든 태스크가 완료되고 핵심 테스트가 통과한다
```

플랜 없을 때 (DONE_CONDITION 기반):
```text
$compose + $workflow-build-execute-loop + @src/auth + [끝까지 실행]
GOAL: 로그인 후 새로고침해도 세션이 유지되게 정리
SCOPE: src/auth
DONE: 핵심 세션 테스트가 통과한다
```

> 파이프라인을 직접 제어하고 싶다면 `build-until-done` + compose 체인을 사용하세요.
