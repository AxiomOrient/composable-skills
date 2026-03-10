---
name: tidy-reorganize
description: "Use when planning behavior-preserving structural refactoring, module-boundary cleanup, or dependency hygiene in a bounded scope. For broad complexity reduction (data model reshaping, naming/tree simplification, side-effect isolation), use simplifier instead. Do not use when adding new features or fixing production incidents. English triggers: refactor plan, structural cleanup, dependency hygiene."
---

# Structure Refactor

## Purpose
Plan structure-preserving cleanup with explicit invariants, dependency rules, and rollback paths.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>reflect>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,correctness-first,quality-gates{tests,compat,style},deterministic-output |
 lens: fowler-strangler |
 output: md(contract=v1)]
```

## Use When
- Need a behavior-preserving refactor plan.
- Need dependency hygiene or module-boundary cleanup in a bounded scope.
- Need atomic refactor steps with rollback paths.

## Do Not Use When
- Need direct code changes.
- Need broad simplification rather than bounded refactor planning.
- Need new feature design or incident debugging.

## Required Inputs
- `TARGET_SCOPE` (path|module|folder|repo, required): Scope to refactor.
- `REFACTOR_BOUNDARY` (module-boundary|dependency-hygiene|structure-preserving-cleanup, required): Type of refactor being planned.
- `BEHAVIOR_INVARIANTS` (list, required): What must remain unchanged.
- `CONSTRAINTS` (list, optional): Rollout, compatibility, and testing constraints.

## Structured Outputs
- `TARGET_DEPENDENCY_RULES` (list, required): Allowed and forbidden dependency directions.
- `ATOMIC_REFACTOR_STEPS` (list, required): Bounded refactor steps.
- `ROLLBACK_PATH` (list, required): Rollback or stop conditions.

## Primary Lens
- `primary_lens`: `fowler-strangler`
- `frame_name`: Seam-First Migrator
- `why`: Refactoring should prefer staged structural change with rollback-friendly seams.
- `summary`: Use seams and staged cutovers for structural change.
- `thesis`: Structural change is safer when it proceeds through explicit seams, staged replacement, and rollback-friendly cutovers rather than big-bang rewrites.
- `decision_rules`:
  - Identify seams before identifying target architecture steps.
  - Prefer small reversible cutovers over wide rewrites.
  - Specify rollback or coexistence strategy alongside each step.
  - Treat structural isolation as progress, even before feature payoff.
- `anti_patterns`:
  - Big-bang refactor plan
  - Cutover steps with no rollback path
  - Refactor goals that mix behavior change with structural isolation
- `good_for`:
  - refactor planning
  - staged modernization
  - rollback-friendly structural change
- `not_for`:
  - test case enumeration
  - UX navigation review
  - neutral bug triage
- `required_artifacts`:
  - Seam Plan
  - Incremental Cutover Steps
  - Rollback Path
- `references`:
  - https://martinfowler.com/bliki/StranglerFigApplication.html

## Artifacts
- `artifacts_in`: plan-dependency-rules.v1, boundary-contract-report.v1
- `artifacts_out`: refactor-plan.v1

## Neutrality Rules
- Keep behavior-preserving invariants explicit before proposing steps.
- Do not smuggle feature work into refactor steps.
- If the cleanup boundary is unclear, mark it as an open edge instead of widening scope silently.

## Output Discipline
- `response_profile=implementation_delta`
- User-facing rendering is delegated to `respond`.
