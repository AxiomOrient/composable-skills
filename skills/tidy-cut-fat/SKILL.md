---
name: tidy-cut-fat
description: "Use when complexity must be reduced without changing core behavior: oversized objects, unclear architecture, noisy folder trees, weak naming, hidden side effects, or accidental abstraction. Produce a minimal simplification blueprint focused on essentials only. Allow large structural change when it clearly removes accidental complexity. Do not use for net-new feature work or incident firefighting. English triggers: simplify architecture, simplify refactor, reduce complexity, remove indirection."
---

# Simplifier

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

## Use When
- Need a simplification blueprint for a bounded scope.
- Need to distinguish essential complexity from accidental complexity.
- Need to reduce structural or naming noise before implementation.

## Do Not Use When
- Need direct code changes.
- Need security or release review rather than simplification planning.
- Need a dependency-rule refactor plan rather than broad simplification.

## Required Inputs
- `TARGET_SCOPE` (path|module|folder|repo, required): Scope to simplify.
- `SIMPLIFICATION_GOAL` (naming|structure|side-effects|mixed, required): Dimension of simplification to prioritize.
- `PRESERVE_BEHAVIOR` (yes|no-change-intent, required): Behavior-preservation contract.
- `KNOWN_PAIN` (list, optional): Known hotspots or complexity symptoms.

## Structured Outputs
- `COMPLEXITY_INVENTORY` (list, required): Essential versus accidental complexity findings.
- `SIMPLIFICATION_PLAN` (list, required): Atomic simplification steps.
- `BEHAVIOR_GUARDS` (list, required): Checks that preserve intended behavior.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `frame_name`: Data-First Systems Pragmatist
- `why`: Simplification should remove hidden indirection and preserve only essential structure.
- `summary`: Data model first, explicit side effects, and explicit performance characteristics.
- `thesis`: Make the structure and cost of the system visible first, then prefer the simplest explicit mechanism that preserves correctness.
- `decision_rules`:
  - Model the system in data before proposing structure or abstraction.
  - Separate transformations from side effects and name the boundary explicitly.
  - Prefer concrete mechanisms over clever indirection unless the abstraction removes real duplication or sharpens invariants.
  - Call out allocation, ownership, latency, and complexity characteristics when they matter to the decision.
- `anti_patterns`:
  - Decorative abstraction without a real invariant
  - Hidden state or hidden side effects
  - Recommendation without a visible cost model
- `good_for`:
  - implementation
  - simplification
  - duplication analysis
  - constant extraction
  - structure-heavy analysis
- `not_for`:
  - open-ended product messaging
  - user-empathy discovery
  - security governance by itself
- `required_artifacts`:
  - Data Model
  - Transformations vs Side Effects
  - Cost or Perf Notes
- `references`:
  - https://www.infoq.com/presentations/Simple-Made-Easy/
  - https://www.gdcvault.com/play/1022186/Keynote-Approaching-Zero-Driver

## Artifacts
- `artifacts_in`: tidy-why-complex.v1
- `artifacts_out`: simplification-plan.v1

## Neutrality Rules
- Separate essential complexity from accidental complexity.
- Do not recommend abstraction unless it removes a proven complexity source.
- Keep uncertain complexity causes as candidates, not conclusions.

## Output Discipline
- `response_profile=implementation_delta`
- User-facing rendering is delegated to `respond`.

