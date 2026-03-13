---
name: workflow-build-execute-plan
description: "Plan-document-driven build pipeline. Requires plans/TASKS.md (and optionally plans/IMPLEMENTATION-PLAN.md). Reads each incomplete task row, implements it, self-critiques, syncs the ledger, verifies, and loops until all tasks are done or a real blocker stops progress. For plan-free autonomous execution without task documents, use control-build-until-done instead."
---

# Workflow / Build Execute Plan

## Purpose
Execute a TASKS.md ledger to completion. Reads task rows as work orders, runs the full implement → critique → sync → verify cycle per task, and loops until every row is done or a real blocker stops progress. Does not stop between cycles — keeps going within the same turn.

## Default Program
```text
[stages: preflight>detect>select>implement>critique>sync>verify>loop>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,correctness-first,quality-gates{tests,security},deterministic-output |
 lens: contract-evidence-verifier |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `contract-evidence-verifier` because it keeps the work aligned with: Check explicit contracts against fresh evidence, separate blockers from gaps, and do not claim pass without proof.

## Use When
- Have a plans/TASKS.md ledger and need end-to-end automated execution of all task rows.
- Need each implementation pass followed by self-critique before moving to the next task.
- Need the task ledger kept in sync automatically after each pass.
- Need a structured execution record of what was implemented and why.

## Do Not Use When
- Have no plan or task documents — use `control-build-until-done` for plan-free autonomous execution.
- Need only a single-pass implementation — use `build-write-code` directly.
- Need planning first — use `workflow-plan-build-ready` to create the plan, then return here.
- Need non-code work (docs, review, release) — use `control-finish-until-done` instead.

## Required Inputs
- `MISSION_GOAL` (string; required): One bounded mission to execute until all task rows are done or a real blocker stops progress.
- `TARGET_SCOPE` (path|module|folder|repo; required): Scope the loop is allowed to touch.
- `DONE_CONDITION` (list; required; shape: {CONDITION, PROOF_REQUIRED}): Explicit completion contract. Typically: all tasks complete + core tests pass.
- `PLAN_ARTIFACTS` (list; **required**; shape: {PATH, ROLE}): Plan and task ledger documents to execute. **This workflow does not operate without plan documents.** Defaults to `plans/IMPLEMENTATION-PLAN.md` + `plans/TASKS.md`.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Safety, rollout, compatibility, or non-goal constraints.

## Input Contract Notes
- PLAN_ARTIFACTS is required. If called without plan documents, immediately emit blocked and direct the user to `control-build-until-done`.
- Treat every incomplete task row as active work to consume, not passive reference material.
- DONE_CONDITION must be externally checkable. No vibe-based success language.
- CONSTRAINTS should name non-goals explicitly so the loop does not drift into adjacent cleanup.

## Execution Flow (per task cycle)

Run all task cycles within a single turn. Do not stop between cycles — continue until MISSION_STATUS=done or blocked:

```
1. Select     — Read TASKS.md, pick the next incomplete task row
2. Implement  — build-write-code applies the code change for that task
3. Critique   — check-improve-loop reviews the implementation and applies the highest-value fix
4. Sync       — plan-sync-tasks marks the task row done and records evidence in the ledger
5. Verify     — Confirm the per-task done condition has evidence
6. Loop       — More tasks remain → go to step 1 immediately
              — No tasks remain → check overall DONE_CONDITION → done or blocked
```

**Do not pause between cycles.** Each cycle completes and immediately starts the next.

## Structured Outputs
- `MISSION_STATUS` (done|blocked; required; allowed: done|blocked): Final loop outcome. No `continue` — if not done, keep looping.
- `TASK_EXECUTION_LOG` (list; required; shape: {TASK_ID, IMPLEMENTATION_SUMMARY, CRITIQUE_APPLIED, SYNC_STATUS, VERIFY_RESULT}): Per-task execution record.
- `DONE_CONDITION_STATUS` (list; required; shape: {CONDITION, STATUS, EVIDENCE_OR_GAP}): Per-condition check against the done contract.
- `BLOCKERS` (list; optional): Real blockers that stopped the loop and what would unblock them.
- `LOOP_EXIT_REASON` (string; required): Why the loop exited.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Output one line per task cycle in real time, then immediately start the next cycle.

```
Task [1/5] `auth/session-refresh` → ✓ done
Task [2/5] `auth/token-rotate` → ✓ done
Task [3/5] `auth/logout-cleanup` → ✗ test failed: [reason]
```

If a task fails, stop and ask immediately:
> "Task `[id]` failed — debug and continue, or skip?"

On loop exit:
- **Done**: `All tasks complete (N)` — list any failures separately
- **Blocked**: `Blocked: [reason]` — suggest how to unblock

## Primary Lens
- `primary_lens`: `contract-evidence-verifier`
- `why`: Each cycle must produce evidence before advancing. Progress is not assumed from momentum.

## Artifacts
- `artifacts_in`: plans/IMPLEMENTATION-PLAN.md (**required**), plans/TASKS.md (**required**)
- `artifacts_out`: completion-contract-loop-report.v1, task-sync-report.v1

## Neutrality Rules
- Do not mark a task done without per-task done condition evidence.
- Do not skip the self-critique pass for speed.
- If plan documents are absent, do not invent task rows — emit blocked and direct to `control-build-until-done`.

## Execution Loop Rules
- Execute all cycles in a single turn. Do not treat one-cycle output as a final result.
- Output one progress line per cycle, not an interim report.
- If a task fails mid-loop, stop and ask the user before continuing.

## Expansion
- `$build-write-code`
- `$check-improve-loop`
- `$plan-sync-tasks`
- `$check-final-verify`

## Mandatory Rules
- If PLAN_ARTIFACTS is absent, emit blocked immediately and direct to `control-build-until-done`.
- Never emit MISSION_STATUS=done while any task row or DONE_CONDITION lacks evidence.
- Never stop after one cycle when tasks remain.

## Example Invocation

```text
$workflow-build-execute-plan
GOAL: Fix session refresh bug
SCOPE: src/auth
DONE: All tasks complete and core session tests pass
PLAN: plans/IMPLEMENTATION-PLAN.md, plans/TASKS.md
```

> No plan documents? Use `control-build-until-done` for plan-free autonomous execution.
