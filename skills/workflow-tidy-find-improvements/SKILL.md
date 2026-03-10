---
name: workflow-tidy-find-improvements
description: "Workflow skill that maps concrete simplification and commonization opportunities before structural improvement work. Use when the user wants an explicit improvement map rather than a vague 'make it better' request."
---

# Workflow / Tidy Improvements

## Purpose
Compose specific improvement scans with simplification and refactor intent into one explicit improvement map.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Use When
- Need an explicit improvement map grounded in duplication and constant extraction evidence.
- Need to decide whether simplification or refactoring is justified in a bounded scope.
- Need a reusable improvement workflow that can still be extended with extra skills.

## Do Not Use When
- Need only a single narrow scan.
- Need a direct feature implementation unrelated to simplification.
- Need bug debugging rather than structure improvement.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Scope to map for improvement.
- `IMPROVEMENT_GOAL` (simplify|commonize|mixed; required; allowed: simplify|commonize|mixed): Improvement emphasis.

## Input Contract Notes
- TARGET_SCOPE should be narrow enough that duplication and constant signals can be tied to concrete files or folders.
- Use `mixed` only when the result may include both simplification and commonization opportunities.
- This workflow maps improvement opportunities; it does not directly authorize broad refactors without evidence.
- Prefer improvement opportunities that remove accidental complexity or sharpen the primary user flow over aesthetic cleanup that does not change the core outcome.

## Structured Outputs
- `IMPROVEMENT_FINDINGS` (list; required; shape: {OPPORTUNITY, LOCATION, EVIDENCE_REF, RECOMMENDED_ACTION}): Evidence-backed improvement opportunities.
- `SIMPLIFICATION_DIRECTION` (simplify|refactor|hold; required; allowed: simplify|refactor|hold): Whether simplification or refactoring is justified.
- `EVIDENCE_BASIS` (list; required; shape: {SCAN, LOCATION, SIGNAL}): Concrete duplication or constant-extraction evidence used to justify the map.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Expanded atomic path used by the workflow.
- `NEXT_IMPLEMENTATION_STEP` (string; required): Recommended next change step.

## Output Contract Notes
- IMPROVEMENT_FINDINGS should stay traceable to EVIDENCE_BASIS rows.
- EXPANDED_ATOMIC_PATH must preserve the actual execution order of the workflow expansion.
- NEXT_IMPLEMENTATION_STEP should name one bounded follow-up change, not a vague cleanup goal.
- Recommend the next step only when it improves the core user path, contract clarity, or meaningful maintenance cost.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: improvement-report.v1

## Neutrality Rules
- Base improvement recommendations on explicit duplication or constant evidence.
- Do not recommend refactoring when the scan evidence does not justify it.
- Keep the workflow transparent and composable.

## Execution Constraints
- If the scans do not show actionable duplication or commonization evidence, return `SIMPLIFICATION_DIRECTION=hold`.
- Do not hide workflow expansion behind generic prose; expose the atomic path explicitly.
- Keep recommendations bounded to the supplied TARGET_SCOPE.
- Do not turn style preference into an improvement mandate unless it removes accidental complexity or protects a meaningful user or maintenance outcome.

## Mandatory Rules
- Keep improvement findings tied to explicit scan evidence.
- Expose the expanded atomic path explicitly.

## Expansion
- `$tidy-find-copies`
- `$tidy-find-magic-numbers`
- `$tidy-cut-fat`
- `$tidy-reorganize`

## Example Invocation
```text
$workflow-tidy-find-improvements
TARGET_SCOPE: src/auth
IMPROVEMENT_GOAL: mixed
```
