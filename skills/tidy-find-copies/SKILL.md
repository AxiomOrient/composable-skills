---
name: tidy-find-copies
description: "Find behavior-level, structure-level, or logic-level duplication in a bounded scope. Use when a module, folder, or repo needs explicit duplication analysis before simplification or refactoring."
---

# Tidy / Find Copies

## Purpose
Identify duplicated logic or structure that can be consolidated without changing behavior.

## Default Program
```text
[stages: preflight>detect>analyze>review>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need evidence-backed duplication findings before simplification or refactoring.
- Need to know whether similar code is accidental copy-paste or justified variation.
- Need a bounded duplication report for one module, folder, or repo.

## Do Not Use When
- Need a general review without duplication focus.
- Need to implement refactoring immediately without first identifying duplication boundaries.
- The target scope is too broad to compare meaningfully without narrowing.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Where to scan for duplication.
- `DUPLICATION_KIND` (logic|structure|flow|mixed; required): Which kind of duplication to prioritize.

## Structured Outputs
- `DUPLICATION_CLUSTERS` (list; required): Grouped duplication candidates with evidence locations.
- `SAFE_MERGE_OPPORTUNITIES` (list; required): Clusters likely safe to consolidate.
- `KEEP_SEPARATE_REASONS` (list; required): Reasons similar-looking code should remain separate.

## Procedure
1. Identify repeated flows, logic blocks, or structurally parallel modules in the target scope.
2. Group them into duplication clusters based on behavior, not only syntax.
3. Separate clusters that are safe to consolidate from cases where domain differences matter.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Duplication scanning should distinguish real duplication from justified variation.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: duplication-report.v1

## Neutrality Rules
- Treat similar code as duplication only when behavior or structure truly overlaps.
- Separate safe merge opportunities from look-alike but justified variation.
- Do not recommend abstraction when it would hide useful domain differences.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Show duplication clusters with evidence locations:
- [cluster name] — files: [list] — kind: [logic/structure/flow]

Split into:
- Safe to merge: [cluster] — merge target: [where]
- Keep separate: [cluster] — reason: [why domain difference matters]

Ask: "Consolidate [highest-value cluster] now, or want the full list reviewed first?"

## Mandatory Rules
- Report evidence locations for every duplication cluster.
- Do not call parallel structure a bug by default.

## Example Invocation
```text
$tidy-find-copies
TARGET_SCOPE: src/payments
DUPLICATION_KIND: flow
```
