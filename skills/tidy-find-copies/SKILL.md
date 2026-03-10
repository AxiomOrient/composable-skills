---
name: tidy-find-copies
description: "Find behavior-level, structure-level, or logic-level duplication in a bounded scope. Use when a module, folder, or repo needs explicit duplication analysis before simplification or refactoring."
---

# Duplication Scan

## Purpose
Identify duplicated logic or structure that can be consolidated without changing behavior.

## Default Program
```text
[stages: preflight>detect>analyze>review>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Use When
- Need evidence-backed duplication findings before simplification or refactoring.
- Need to know whether similar code is accidental copy-paste or justified variation.
- Need a bounded duplication report for one module, folder, or repo.

## Do Not Use When
- Need a general review without duplication focus.
- Need to implement refactoring immediately without first identifying duplication boundaries.
- The target scope is too broad to compare meaningfully without narrowing.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo, required): Where to scan for duplication.
- `DUPLICATION_KIND` (logic|structure|flow|mixed, required): Which kind of duplication to prioritize.

## Structured Outputs
- `DUPLICATION_CLUSTERS` (list, required): Grouped duplication candidates with evidence locations.
- `SAFE_MERGE_OPPORTUNITIES` (list, required): Clusters likely safe to consolidate.
- `KEEP_SEPARATE_REASONS` (list, required): Reasons similar-looking code should remain separate.

## Procedure
1. Identify repeated flows, logic blocks, or structurally parallel modules in the target scope.
2. Group them into duplication clusters based on behavior, not only syntax.
3. Separate clusters that are safe to consolidate from cases where domain differences matter.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `frame_name`: Data-First Systems Pragmatist
- `why`: Duplication scanning should distinguish real duplication from justified variation.
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
- `artifacts_out`: duplication-report.v1

## Neutrality Rules
- Treat similar code as duplication only when behavior or structure truly overlaps.
- Separate safe merge opportunities from look-alike but justified variation.
- Do not recommend abstraction when it would hide useful domain differences.

## Mandatory Rules
- Report evidence locations for every duplication cluster.
- Do not call parallel structure a bug by default.

## Example Invocation
```text
$tidy-find-copies
TARGET_SCOPE: src/payments
DUPLICATION_KIND: flow
```

## Output Discipline
- `response_profile=review_findings`
- User-facing rendering is delegated to `respond`.

