---
name: plan-dependency-rules
description: "Define target dependency rules and allowed module directions before bounded refactoring. Use when the immediate job is to make dependency rules explicit, not to plan the full refactor yet."
---

# Plan / Dependency Rules

## Purpose
Make target dependency rules explicit before structural cleanup.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{compat},deterministic-output | lens: uncle-bob | output: md(contract=v1)]
```

## Use When
- Need explicit dependency rules before refactoring.
- Need to clarify allowed versus forbidden imports or calls.
- Need a target boundary map for a bounded structural cleanup.

## Do Not Use When
- Need a broad architecture redesign.
- Need direct implementation or code changes.
- There is no bounded module or layer boundary to define.
- Need only current-state boundary diagnosis without target dependency rules.

## Required Inputs
- `TARGET_SCOPE` (path|module|layer; required): Boundary whose dependency rules will be defined.
- `CURRENT_BOUNDARY_NOTES` (list; optional; shape: {NOTE, EVIDENCE}): Known dependency problems or leaks.

## Input Contract Notes
- TARGET_SCOPE should point to one bounded module, layer, or path where dependency rules can be stated concretely.
- CURRENT_BOUNDARY_NOTES should cite observed leaks or coupling rather than aspirational architecture slogans.

## Structured Outputs
- `ALLOWED_DEPENDENCIES` (list; required; shape: {FROM, TO, WHY_ALLOWED}): Permitted dependency directions.
- `FORBIDDEN_DEPENDENCIES` (list; required; shape: {FROM, TO, WHY_FORBIDDEN}): Dependency directions or couplings to remove.
- `TRANSITION_STEPS` (list; required; shape: {STEP, WHY}): Bounded steps to reach the target dependency rules.

## Output Contract Notes
- ALLOWED_DEPENDENCIES and FORBIDDEN_DEPENDENCIES should describe concrete directional rules, not vague layering principles.
- TRANSITION_STEPS should stay bounded to the rule change rather than expanding into a full refactor plan.

## Primary Lens
- `primary_lens`: `uncle-bob`
- `why`: Dependency planning should make boundary direction and forbidden couplings explicit.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: plan-dependency-rules.v1

## Neutrality Rules
- Describe the current dependency reality before prescribing rules.
- Keep target rules bounded to the inspected scope.
- Do not propose new abstraction layers without evidence they reduce coupling.

## Execution Constraints
- Do not turn this skill into a broad technical design or whole-system architecture rewrite.
- Prefer the smallest rule set that removes the observed coupling problem.
- Keep target rules explicit enough that later refactor work can check compliance.

## Example Invocation
```text
$plan-dependency-rules
TARGET_SCOPE: src/domain
CURRENT_BOUNDARY_NOTES: ui imports domain internals
```
