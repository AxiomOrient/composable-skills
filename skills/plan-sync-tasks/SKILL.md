---
name: plan-sync-tasks
description: "Use when synchronizing markdown-first execution against existing implementation-plan and tasks artifacts. Treat those documents as primary data artifacts. This skill does not create the plan; it synchronizes execution against the existing task ledger."
---

# Plan / Sync Tasks

## Purpose
Synchronize planning artifacts, task lifecycle, and implementation evidence in one run without replacing plan-task-breakdown.

## Default Program
```text
[stages: preflight>detect>plan>review>audit |
 scope: paths(plans/IMPLEMENTATION-PLAN.md,plans/TASKS.md) |
 policy: evidence,correctness-first,quality-gates{tests,docs,security},safety-gates,approval-gates{explicit,no-fallback},deterministic-output |
 lens: hickey-carmack |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need execution governed by plans/IMPLEMENTATION-PLAN.md and plans/TASKS.md.
- Need task selection and status changes tied to explicit TASK-ID rows.
- Need implementation and plan/task document updates kept in sync.

## Do Not Use When
- Need to create the plan or task breakdown from scratch; use plan-task-breakdown instead.
- Need a standalone domain analysis or review without task tracking.
- Have no plan/task artifacts and do not want markdown-first execution control.
- Need implicit next actions not linked to explicit TASK-ID rows.

## Required Inputs
- `IMPLEMENTATION_PLAN_PATH` (path; required): Path to plans/IMPLEMENTATION-PLAN.md.
- `TASKS_PATH` (path; required): Path to plans/TASKS.md.
- `SELECTED_TASK_IDS` (list; optional; shape: {TASK_ID}): Explicit task ids selected for the current run.
- `KNOWN_EVIDENCE` (list; optional; shape: {SOURCE, NOTE}): Tests, logs, diffs, or prior outputs that support task progress.
- `IMPLEMENTATION_EVIDENCE_NOTES` (list; optional; shape: {TASK_ID, NOTE, EVIDENCE}): Implementation-local evidence notes emitted by $build-write-code before markdown synchronization.

## Input Contract Notes
- IMPLEMENTATION_PLAN_PATH and TASKS_PATH should point to the source-of-truth markdown artifacts for the current delivery run.
- SELECTED_TASK_IDS should be omitted only when the utility is expected to infer the active task set from explicit evidence in the docs.
- IMPLEMENTATION_EVIDENCE_NOTES must already reference stable TASK_ID rows before synchronization starts.
- When task ids or verification steps must be inferred from a markdown backlog, use `scripts/task_ledger.py` before synchronization instead of hand-parsing tables ad hoc.

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

## Bundled Scripts
- `scripts/task_ledger.py next --tasks <tasks-path> [--plan <plan-path>]`
  - Emits the next actionable task id, task row, and derived verification map.
- `scripts/task_ledger.py summary --tasks <tasks-path> [--plan <plan-path>]`
  - Emits open/done/blocked counts and the first open task in file order.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Show which task rows were updated:
- TASK-ID | from: [status] → to: [status] | evidence: [what proved it]

Flag any rows that couldn't be resolved:
- TASK-ID — blocked: [why linkage failed or evidence was missing]

State the overall sync status: synced / blocked / partial.

## Mandatory Rules
- Do not create new project plans here; plan-task-breakdown owns plan creation.
- Only synchronize work that can be linked to explicit task rows or explicit evidence.
- Do not change runtime code here; synchronize markdown truth only.
