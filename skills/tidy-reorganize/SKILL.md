---
name: tidy-reorganize
description: "Use when planning behavior-preserving structural refactoring, module-boundary cleanup, or dependency hygiene in a bounded scope. For cognitive-load reduction with actual code changes, use tidy-simplify instead. Do not use when adding new features or fixing production incidents."
---

# Tidy / Reorganize

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

## Lens Rationale
This skill uses `fowler-strangler` because it keeps the work aligned with: Use seams and staged cutovers for structural change.

## Use When
- Need a behavior-preserving refactor plan.
- Need dependency hygiene or module-boundary cleanup in a bounded scope.
- Need atomic refactor steps with rollback paths.

## Do Not Use When
- Need direct code changes.
- Need broad simplification rather than bounded refactor planning.
- Need new feature design or incident debugging.

## Required Inputs
- `TARGET_SCOPE` (path|module|folder|repo; required): Scope to refactor.
- `REFACTOR_BOUNDARY` (module-boundary|dependency-hygiene|structure-preserving-cleanup; required): Type of refactor being planned.
- `BEHAVIOR_INVARIANTS` (list; required): What must remain unchanged.
- `CONSTRAINTS` (list; optional): Rollout, compatibility, and testing constraints.

## Structured Outputs
- `TARGET_DEPENDENCY_RULES` (list; required): Allowed and forbidden dependency directions.
- `ATOMIC_REFACTOR_STEPS` (list; required): Bounded refactor steps.
- `ROLLBACK_PATH` (list; required): Rollback or stop conditions.

## Primary Lens
- `primary_lens`: `fowler-strangler`
- `why`: Refactoring should prefer staged structural change with rollback-friendly seams.

## Artifacts
- `artifacts_in`: plan-dependency-rules.v1, boundary-contract-report.v1
- `artifacts_out`: refactor-plan.v1

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Show target dependency rules: allowed and forbidden directions.

Show atomic refactor steps:
1. [step] — why: [what coupling it removes]

Show 롤백(되돌리기) conditions: [condition] → [stop or revert action]

If scope was constrained, say so plainly: "Stopped at [boundary] — [rest] would require a separate run."

Ask about any rollout or compatibility boundary that affects step ordering.

## Neutrality Rules
- Keep behavior-preserving invariants explicit before proposing steps.
- Do not smuggle feature work into refactor steps.
- If the cleanup boundary is unclear, mark it as an open edge instead of widening scope silently.
