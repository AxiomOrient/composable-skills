---
name: plan-driven-delivery
description: "Use when enforcing markdown-first planning and synchronized implementation execution. Treat implementation-plan and tasks documents as primary data artifacts. This skill does not create the plan; it synchronizes execution against an existing plan. English triggers: plan-driven, markdown-first delivery, plan-task synchronization."
---

# Plan Driven Delivery

## Purpose
Synchronize planning artifacts, task lifecycle, and implementation evidence in one run without replacing the task-breakdown planner.

## Default Program
```text
[stages: preflight>detect>plan>review>audit |
 scope: paths(docs/IMPLEMENTATION-PLAN.md,docs/TASKS.md) |
 policy: evidence,correctness-first,quality-gates{tests,docs,security},safety-gates,approval-gates{explicit,no-fallback},deterministic-output |
 lens: hickey-carmack |
 output: md(contract=v1)]
```

## Use When
- Need execution governed by docs/IMPLEMENTATION-PLAN.md and docs/TASKS.md.
- Need task selection and status changes tied to explicit TASK-ID rows.
- Need implementation and plan/task document updates kept in sync.

## Do Not Use When
- Need to create the plan or task breakdown from scratch; use plan-task-breakdown instead.
- Need a standalone domain analysis or review without task tracking.
- Have no plan/task artifacts and do not want markdown-first execution control.
- Need implicit next actions not linked to explicit TASK-ID rows.

## Required Inputs
- `IMPLEMENTATION_PLAN_PATH` (path; required): Path to docs/IMPLEMENTATION-PLAN.md.
- `TASKS_PATH` (path; required): Path to docs/TASKS.md.
- `SELECTED_TASK_IDS` (list; optional; shape: {TASK_ID}): Explicit task ids selected for the current run.
- `KNOWN_EVIDENCE` (list; optional; shape: {SOURCE, NOTE}): Tests, logs, diffs, or prior outputs that support task progress.
- `IMPLEMENTATION_EVIDENCE_NOTES` (list; optional; shape: {TASK_ID, NOTE, EVIDENCE}): Implementation-local evidence notes emitted by $build-write-code before markdown synchronization.

## Input Contract Notes
- IMPLEMENTATION_PLAN_PATH and TASKS_PATH should point to the source-of-truth markdown artifacts for the current delivery run.
- SELECTED_TASK_IDS should be omitted only when the utility is expected to infer the active task set from explicit evidence in the docs.
- IMPLEMENTATION_EVIDENCE_NOTES must already reference stable TASK_ID rows before synchronization starts.

## Structured Outputs
- `TASK_LINK_MAP` (list; required; shape: {TASK_ID, LINKED_EVIDENCE, LINK_STATUS}): Mapping from selected work items to TASK-ID rows.
- `TASK_STATUS_UPDATES` (list; required; shape: {TASK_ID, FROM, TO, EVIDENCE}): Explicit task status transitions and evidence.
- `SYNC_STATUS` (synced|blocked|partial; required; allowed: synced|blocked|partial): Overall synchronization state such as synced or blocked.

## Output Contract Notes
- TASK_LINK_MAP should make missing or ambiguous task linkage explicit instead of silently guessing matches.
- TASK_STATUS_UPDATES should describe only actual markdown truth changes, not proposed future transitions.
- SYNC_STATUS=`partial` is for mixed outcomes where some task links succeeded and some remained blocked.

## Artifacts
- `artifacts_in`: implementation-plan.v1, tasks-table.v1, implementation-delta.v1
- `artifacts_out`: task-sync-report.v1

## Neutrality Rules
- Treat plan and task documents as the source of execution truth.
- If task linkage is missing, report blocked instead of guessing mappings.
- Keep document truth separate from AI-proposed next actions or interpretations.

## Execution Constraints
- Do not create new tasks or rewrite plan strategy here; synchronize only against existing markdown truth.
- If evidence cannot be linked to an explicit task row, keep the sync blocked or partial instead of inventing a mapping.
- Keep runtime code untouched from this utility.

## Mandatory Rules
- Do not create new project plans here; plan-task-breakdown owns plan creation.
- Only synchronize work that can be linked to explicit task rows or explicit evidence.
- Do not change runtime code here; synchronize markdown truth only.

## Output Discipline
- `response_profile=implementation_delta`
- User-facing rendering is delegated to `respond`.
