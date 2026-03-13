---
name: tidy-why-complex
description: "Inventory essential versus accidental complexity in a bounded scope before simplification. Use when the immediate job is to identify complexity sources, not to plan the entire simplification yet."
---

# Tidy / Why Complex

## Purpose
Map complexity sources and classify them as essential or accidental before simplification work.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need a bounded complexity inventory before simplification.
- Need to know whether complexity comes from domain rules or accidental structure.
- Need to identify which complexity clusters are worth removing first.

## Do Not Use When
- Need a full simplification plan already.
- Need direct implementation work.
- The target scope is not bounded.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Where to inspect complexity.
- `SIMPLIFICATION_GOAL` (naming|structure|side-effects|mixed; required): Complexity dimension to prioritize.

## Structured Outputs
- `ESSENTIAL_COMPLEXITY` (list; required): Complexity that is inherent to the domain.
- `ACCIDENTAL_COMPLEXITY` (list; required): Complexity created by incidental structure or naming.
- `SIMPLIFICATION_CANDIDATES` (list; required): Candidates worth simplifying first.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Complexity inventory should separate essential structure from accidental abstraction and hidden state.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: tidy-why-complex.v1

## Response Format

Show the complexity inventory as two lists:
- Essential: [complexity] — reason: [why the domain requires it]
- Accidental: [complexity] — cause: [indirection / naming / hidden state]

Show simplification candidates ordered by removal value:
1. [candidate] — what it would remove

Ask: "Start with [top candidate], or want the full complexity map before deciding?"

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
