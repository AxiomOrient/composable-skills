---
name: tidy-cut-fat
description: "Use when complexity must be reduced without changing core behavior: oversized objects, unclear architecture, noisy folder trees, weak naming, hidden side effects, or accidental abstraction. Produce a minimal simplification blueprint. Do not use for net-new feature work or incident firefighting."
---

# Tidy / Cut Fat

## Purpose
Identify and propose the smallest useful complexity reduction without changing intended behavior.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>reflect>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,correctness-first,quality-gates{tests,compat,style},deterministic-output |
 lens: hickey-carmack |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need a simplification blueprint for a bounded scope.
- Need to distinguish essential complexity from accidental complexity.
- Need to reduce structural or naming noise before implementation.

## Do Not Use When
- Need direct code changes rather than a planning output.
- Need security or release review rather than simplification planning.
- Need a dependency-rule refactor plan rather than broad simplification.

## Required Inputs
- `TARGET_SCOPE` (path|module|folder|repo; required): Scope to simplify.
- `SIMPLIFICATION_GOAL` (naming|structure|side-effects|mixed; required): Dimension of simplification to prioritize.
- `PRESERVE_BEHAVIOR` (yes|no-change-intent; required): Behavior-preservation contract.
- `KNOWN_PAIN` (list; optional): Known hotspots or complexity symptoms.

## Structured Outputs
- `COMPLEXITY_INVENTORY` (list; required): Essential versus accidental complexity findings.
- `SIMPLIFICATION_PLAN` (list; required): Atomic simplification steps.
- `BEHAVIOR_GUARDS` (list; required): Checks that preserve intended behavior.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Simplification should remove hidden indirection and preserve only essential structure.

## Artifacts
- `artifacts_in`: tidy-analyze.v1
- `artifacts_out`: simplification-plan.v1

## Response Format

Think and operate in English, but deliver the final response in Korean.

Show what changed and what was left alone:
- Simplified: [what] — why: [complexity removed]
- Left alone: [what] — reason: [essential or out of scope]

List behavior guards: [check] — confirms: [what still works]

If scope was constrained, say so plainly: "Stopped at [boundary] — [rest] was out of scope."

Ask about any boundary decision that affected what got simplified.

## Neutrality Rules
- Separate essential complexity from accidental complexity.
- Do not recommend abstraction unless it removes a proven complexity source.
- Keep uncertain complexity causes as candidates, not conclusions.
