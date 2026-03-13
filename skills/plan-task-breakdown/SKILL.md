---
name: plan-task-breakdown
description: "Planning-only skill. Generate or update implementation plan and tasks documents. Do not implement or review code here. Do not use when a plan already exists and only execution is needed."
---

# Plan / Task Breakdown

## Purpose
Create execution-ready plan and task artifacts with stable task ids and explicit verification paths.

## Default Program
```text
[stages: preflight>detect>analyze@panel(3)>plan>review>reflect>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat},deterministic-output |
 lens: eisenhower |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `eisenhower` because it keeps the work aligned with: Prioritize by urgency and importance while keeping the critical path explicit.

## Use When
- Need implementation-ready plan and task documents.
- Need execution phases, decision gates, and verification strategy before coding.
- Need to update existing plan/task artifacts in place.

## Do Not Use When
- Need direct code changes.
- Need only scope normalization before planning.
- Need review verdicts or release judgement.
- Need product framing, information architecture, feature specification, or technical design as the primary artifact.

## Required Inputs
- `PLANNING_GOAL` (string; required): What the work must deliver.
- `TARGET_SCOPE` (path|module|folder|repo|artifact; required): Bounded scope of the planned work.
- `DONE_CONDITION` (list; required; shape: {CONDITION}): Observable completion contract.
- `PLAN_OUTPUT_PATH` (path; optional): Path where the implementation plan must be created or updated. Defaults to `plans/IMPLEMENTATION-PLAN.md` when omitted. The `plans/` directory is created automatically if it does not exist.
- `TASKS_OUTPUT_PATH` (path; optional): Path where the task table must be created or updated. Defaults to `plans/TASKS.md` when omitted. The `plans/` directory is created automatically if it does not exist.
- `ARTIFACT_MODE` (create|update; optional; allowed: create|update): Whether the planning artifacts are being created from scratch or updated in place. Defaults to `create` when omitted.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Compatibility, rollout, time, safety, and non-goal constraints.
- `EXISTING_ARTIFACTS` (list; optional; required when ARTIFACT_MODE=update; shape: {PATH, ROLE}): Existing planning docs that must be updated in place.

## Input Contract Notes
- PLANNING_GOAL should describe one bounded delivery target, not a mixed roadmap.
- DONE_CONDITION should contain observable completion checks rather than implementation ideas.
- When PLAN_OUTPUT_PATH or TASKS_OUTPUT_PATH is omitted, default to `plans/IMPLEMENTATION-PLAN.md` and `plans/TASKS.md`. Create the `plans/` directory if it does not exist before writing.
- When ARTIFACT_MODE is omitted, default to `create` unless EXISTING_ARTIFACTS clearly indicates update-in-place work.
- When ARTIFACT_MODE=update, EXISTING_ARTIFACTS should point to the exact plan or task files that must be edited in place.
- DONE_CONDITION should reflect the core user-visible or contract-visible outcome, not optional polish or aesthetic cleanup.
- Use planner for execution artifacts only; if the primary missing artifact is a brief, IA map, feature spec, or technical design doc, create that upstream document first.

## Structured Outputs
- `IMPLEMENTATION_PLAN_PATH` (string; required): Saved path to the implementation plan.
- `TASKS_ARTIFACT_PATH` (string; required): Saved path to the task artifact.
- `TASK_ROWS` (list; required; shape: {TASK_ID, ACTION, DONE_WHEN, EVIDENCE_REQUIRED, DEPENDS_ON}): Stable task rows with done criteria and evidence expectations.
- `DECISION_GATES` (list; required; shape: {GATE_NAME, CHECK, PASS_CONDITION, ON_FAIL}): Decision points and verification gates for the work.

## Output Contract Notes
- TASK_ROWS should remain stable enough that downstream execution can refer to TASK_ID without renumbering during one delivery cycle.
- DECISION_GATES should mark only true go/no-go checks, not generic reminders.
- IMPLEMENTATION_PLAN_PATH must match the actual saved artifact path used by the planning run.
- TASKS_ARTIFACT_PATH must match the actual saved task artifact path used by the planning run.
- TASK_ROWS should prioritize the shortest path to DONE_CONDITION and push non-essential cleanup out of the critical path unless it is required for correctness or clarity.

## Primary Lens
- `primary_lens`: `eisenhower`
- `why`: Planning should expose priority, critical path, and decision gates before execution.

## Artifacts
- `artifacts_in`: scope-contract.v1
- `artifacts_out`: implementation-plan.md.v1, tasks.md.v1

## Neutrality Rules
- Separate explicit requirements from planning assumptions.
- If scope or done condition is unresolved, keep it as an open edge instead of guessing.
- Keep task breakdown bounded to the stated goal and constraints.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Show the key decisions made in the plan:
- Critical path: [first task → ... → final task]
- Decision gates: [gate name] — passes when: [condition]

List task rows as a compact table: TASK-ID | action | done when | depends on.

Flag any open edges: "Scope of [task] is still unresolved — need: [what info]"

Ask about the one decision that most affects the critical path if any remains open.

## Execution Constraints
- Do not implement code or issue review verdicts from this skill; planning artifacts only.
- If scope, done condition, or constraints are unresolved, leave an explicit open edge instead of smoothing it away.
- Keep the task table bounded to the supplied goal and constraints rather than expanding into adjacent backlog.
- Prefer the simplest plan that satisfies the explicit goal and core user outcome; avoid adding tasks that improve taste but not the delivery contract.
