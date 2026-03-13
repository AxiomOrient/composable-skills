---
name: tidy-simplify
description: "Behavior-preserving code simplification skill for one bounded scope after the target has already been identified. Applies the four-step cognitive-load reduction sequence: Intent Extraction, Abstraction Cost, Collapse & Merge, and Immutability Check. For recent-diff cleanup across reuse, quality, and efficiency, use workflow-tidy-simplify-this instead."
---

# Tidy / Simplify

## Purpose
Apply the four-step cognitive-load reduction sequence to a bounded code scope while preserving functional equivalence.

## Default Program
```text
[stages: preflight>detect>analyze>implement>verify>review>audit |
 scope: diff|paths(glob,...) |
 policy: evidence,correctness-first,quality-gates{tests,compat,style},deterministic-output |
 lens: hickey-carmack |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need to apply actual code changes that reduce cognitive load in a concrete, bounded scope.
- Need to remove indirection, nested branching, one-use helpers, or mutable state churn after the scope is clearly defined.
- Need a dedicated simplification implementation pass before broader refactoring or review.
- tidy-cut-fat produced a simplification blueprint and now the actual reduction moves must be applied.

## Do Not Use When
- Need net-new feature work or behavior changes.
- Need only analysis, inventory, or a simplification plan — use tidy-cut-fat or tidy-analyze instead.
- Need recent-diff cleanup across reuse, quality, and efficiency — use workflow-tidy-simplify-this.
- Need only checklist review or final delivery verification.
- The target scope is too broad to verify functional equivalence after simplification.

## Required Inputs
- `TARGET_SCOPE` (path|module|folder|diff; required): Bounded scope to simplify. Must be small enough to verify equivalence with focused checks.
- `FUNCTIONAL_EQUIVALENCE` (yes; required): Explicit confirmation that this pass must preserve functional equivalence. Must be `yes`; this skill does not proceed without this confirmation.
- `SIMPLIFY_GOAL` (control-flow|data-flow|indirection|immutability|mixed; required; allowed: control-flow|data-flow|indirection|immutability|mixed): Primary simplification dimension matching the four-step algorithm. Identify the dominant cognitive load source.
- `KNOWN_PAIN` (list; optional; shape: {SYMPTOM, LOCATION, WHY_RELEVANT}): Known complexity hotspots to prioritize in the simplification pass.

## Input Contract Notes
- TARGET_SCOPE should be small enough that functional equivalence can be confirmed with focused tests or behavior checks.
- FUNCTIONAL_EQUIVALENCE must be `yes`; this skill does not proceed without this confirmation.
- SIMPLIFY_GOAL should identify the dominant cognitive load source, not a vague desire such as 'cleaner'.
- If the scope is still unclear, run tidy-cut-fat first to produce an analysis, then use this skill for the implementation pass.

## Structured Outputs
- `INTENT_STATEMENT` (string; required): Step 1 — Intent Extraction: one sentence naming the core value, behavior, or guarantee that must survive simplification.
- `ABSTRACTION_COSTS` (list; required; shape: {STRUCTURE, COST, KEEP_OR_COLLAPSE, EVIDENCE}): Step 2 — Abstraction Cost: each layer, helper, and wrapper priced by cognitive cost. Collapse candidates marked.
- `SIMPLIFICATION_MOVES` (list; required; shape: {MOVE, TARGET, WHY, STATUS}): Steps 3 and 4 — Collapse & Merge and Immutability Check: actual reduction moves applied (guard clause, merge, inline, immutability refactor).
- `BEHAVIOR_GUARDS` (list; required; shape: {GUARD, CHECK}): Explicit behavior guards confirming each simplification move preserved functional equivalence.
- `VERIFICATION_RESULTS` (list; required; shape: {CHECK, RESULT, COMMAND_OR_TEST, EVIDENCE}): Evidence that the scope still behaves correctly after all simplification moves, including the exact command or test used.

## Output Contract Notes
- INTENT_STATEMENT must be written before any abstraction cost judgement — it anchors what must be preserved.
- ABSTRACTION_COSTS drives reasoning about what to collapse; SIMPLIFICATION_MOVES records the actual reduction actions.
- Every SIMPLIFICATION_MOVES entry must map to at least one BEHAVIOR_GUARDS or VERIFICATION_RESULTS entry.
- VERIFICATION_RESULTS should name the exact command, test, or check instead of summarizing proof narratively.
- Stop and narrow the scope if VERIFICATION_RESULTS cannot confirm functional equivalence.

## Procedure
1. Step 1 — Intent Extraction: Read the entire TARGET_SCOPE. Write INTENT_STATEMENT as one sentence naming the final value, behavior, or guarantee the code must preserve. If the intent cannot be named clearly, do not proceed.
2. Step 2 — Abstraction Cost: Inspect all interfaces, wrappers, helper chains, and transformation hops. Price each by its cognitive cost. Mark one-use helpers, pass-through wrappers, and decorative layers as collapse candidates in ABSTRACTION_COSTS.
3. Step 3 — Collapse & Merge: Replace nested branching with guard clauses or early returns. Merge multi-hop data transformations into one explicit pipeline. Prefer standard-library operations over bespoke logic. Record each move in SIMPLIFICATION_MOVES.
4. Step 4 — Immutability Check: Reduce mutable temporary state. Prefer derived values, one-way data flow, and explicit transformation over stateful bookkeeping. Add immutability moves to SIMPLIFICATION_MOVES.
5. Verify: Run the narrowest checks that confirm functional equivalence still holds. Record in BEHAVIOR_GUARDS and VERIFICATION_RESULTS. Stop at any verification gap rather than claiming success.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Simplification must start from the core outcome, price each abstraction against its cognitive cost, and choose the smallest explicit mechanism that preserves correctness — the Hickey-Carmack data-first, explicit-control frame enforces exactly this discipline.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: implementation-delta.v1

## Neutrality Rules
- Do not call a move simpler unless cognitive path, hidden state, or indirection is observably reduced.
- Do not remove structure that carries a real invariant, public contract, or boundary check.
- If functional equivalence cannot be evidenced, stop at the verification gap instead of claiming success.
- Stop when the improvement is aesthetic only and does not reduce cognitive steps.

## Execution Constraints
- Apply code changes only within TARGET_SCOPE; do not expand into unrelated cleanup.
- Prefer guard clauses, single explicit data pipelines, and standard-library replacements when behavior stays equivalent.
- Reduce mutable state and one-use indirection before proposing new abstractions.
- Keep the verification surface narrow and behavior-focused.
- Do not turn this into a broad refactor or architecture rewrite.

## Response Format

Think and operate in English, but deliver the final response in Korean.

State the intent: what the code must preserve after simplification.

Show what changed and what was left alone:
- Simplified: [move] — removed: [what abstraction or state]
- Left alone: [structure] — reason: [carries real invariant]

Show verification: [command or test] — result: PASS / FAIL

If scope was constrained: "Stopped at [boundary] — [rest] would require a separate pass."

Ask about any move where functional equivalence is uncertain.

## Mandatory Rules
- Preserve functional equivalence — write INTENT_STATEMENT first, verify last.
- Do not skip ABSTRACTION_COSTS — every collapse move must be priced before applied.
- Do not claim the pass is complete without verification evidence.

## Required References
- `references/simplify-algorithm.md`
- `references/structural-simplicity-rubric.md`

## Example Invocation
```text
$tidy-simplify
TARGET_SCOPE: src/auth/session.ts
FUNCTIONAL_EQUIVALENCE: yes
SIMPLIFY_GOAL: indirection
KNOWN_PAIN:
- nested branching hides refresh intent
- one-use helper chain obscures data flow
```
