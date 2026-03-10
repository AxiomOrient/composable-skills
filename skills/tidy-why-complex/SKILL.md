---
name: tidy-why-complex
description: "Inventory essential versus accidental complexity in a bounded scope before simplification. Use when the immediate job is to identify complexity sources, not to plan the entire simplification yet."
---

# Complexity Inventory

## Purpose
Map complexity sources and classify them as essential or accidental before simplification work.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Use When
- Need a bounded complexity inventory before simplification.
- Need to know whether complexity comes from domain rules or accidental structure.
- Need to identify which complexity clusters are worth removing first.

## Do Not Use When
- Need a full simplification plan already.
- Need direct implementation work.
- The target scope is not bounded.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo, required): Where to inspect complexity.
- `SIMPLIFICATION_GOAL` (naming|structure|side-effects|mixed, required): Complexity dimension to prioritize.

## Structured Outputs
- `ESSENTIAL_COMPLEXITY` (list, required): Complexity that is inherent to the domain.
- `ACCIDENTAL_COMPLEXITY` (list, required): Complexity created by incidental structure or naming.
- `SIMPLIFICATION_CANDIDATES` (list, required): Candidates worth simplifying first.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `frame_name`: Data-First Systems Pragmatist
- `why`: Complexity inventory should separate essential structure from accidental abstraction and hidden state.
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
- `artifacts_in`: none
- `artifacts_out`: tidy-why-complex.v1

## Neutrality Rules
- Do not label domain-required complexity as accidental without evidence.
- Separate pain points from actual simplification candidates.
- Keep the inventory descriptive before recommending changes.

## Example Invocation
```text
$tidy-why-complex
TARGET_SCOPE: src/auth
SIMPLIFICATION_GOAL: structure
```

## Output Discipline
- `response_profile=analysis_report`
- User-facing rendering is delegated to `respond`.

