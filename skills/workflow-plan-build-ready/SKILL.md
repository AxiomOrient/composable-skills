---
name: workflow-plan-build-ready
description: "Workflow skill that turns a broad request into a bounded scope contract, a buildable spec/design path, and execution-ready task artifacts. Use when the user needs one default planning entrypoint before implementation."
---

# Workflow / Plan Build Ready

## Purpose
Compose scope normalization, spec/design shaping, and task breakdown into one default planning workflow.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs,compat},deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need one planning workflow before writing code.
- Need scope, design, and task artifacts to stay aligned in one path.
- Need a category-default planning entrypoint instead of manually chaining multiple planning skills.

## Do Not Use When
- Need direct implementation right now.
- Need only one narrow planning artifact such as a feature spec or dependency rules.
- Already have stable plan/task artifacts and only need plan-driven execution.

## Required Inputs
- `REQUEST` (string; required): Original request or delivery target.
- `TARGET_SCOPE` (path|module|folder|repo|artifact; required): Bounded scope of the work.
- `DONE_CONDITION` (list; required; shape: {CONDITION}): Observable completion contract.
- `PLAN_OUTPUT_PATH` (path; optional): Path where the implementation plan will be written. Defaults to `plans/IMPLEMENTATION-PLAN.md` when omitted.
- `TASKS_OUTPUT_PATH` (path; optional): Path where the task table will be written. Defaults to `plans/TASKS.md` when omitted.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Compatibility, rollout, time, or non-goal constraints.

## Input Contract Notes
- REQUEST should describe the delivery target in plain language before planning expands it.
- DONE_CONDITION should stay externally checkable rather than implementation-specific.
- Use this workflow when the main missing artifact is the plan path itself, not the final code.
- When PLAN_OUTPUT_PATH or TASKS_OUTPUT_PATH is omitted, default to `plans/IMPLEMENTATION-PLAN.md` and `plans/TASKS.md`.

## Structured Outputs
- `SCOPE_CONTRACT` (scope-contract.v1; required): Bounded scope contract for the planned work.
- `DESIGN_SUMMARY` (string; required): Condensed build-ready design summary.
- `TASK_ROWS` (list; required; shape: {TASK_ID, ACTION, DONE_WHEN, EVIDENCE_REQUIRED, DEPENDS_ON}): Execution-ready task rows.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Actual atomic path executed by the workflow.

## Output Contract Notes
- TASK_ROWS should be stable enough for downstream execution and verification.
- DESIGN_SUMMARY should be buildable, not a product brief restatement.
- EXPANDED_ATOMIC_PATH must preserve execution order explicitly.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: scope-contract.v1, spec-contract.v1, plan-how-to-build.v1, implementation-plan.md.v1, tasks.md.v1

## Neutrality Rules
- Preserve the neutrality rules of the underlying planning skills.
- Do not imply code implementation progress from this workflow.
- Keep planning artifacts bounded to the stated request and done condition.

## Execution Constraints
- Do not collapse planning artifacts into one prose blob.
- Prefer the minimum plan surface that makes the work implementable and verifiable.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Output the task table and open decisions — no chain commentary.

Tasks:
| ID | Goal | Scope | Verification |
|----|----|----|----|

Open decisions that must be resolved before building:
- [decision] — options: [A] vs [B] — "Which approach?"

If a step produced a blocker: name it and ask what needs clarifying before continuing.

## Mandatory Rules
- Expose the expanded atomic path explicitly.
- Keep the plan output bounded enough that build-write-code can execute against it.

## Expansion
- `$clarify-boundaries`
- `$plan-what-it-does`
- `$plan-how-to-build`
- `$plan-task-breakdown`

## Example Invocation
```text
$workflow-plan-build-ready
REQUEST: simplify the auth module without changing behavior
TARGET_SCOPE: src/auth
DONE_CONDITION:
  - CONDITION: a structure-improvement report and task rows are created
PLAN_OUTPUT_PATH: plans/IMPLEMENTATION-PLAN.md
TASKS_OUTPUT_PATH: plans/TASKS.md
```
