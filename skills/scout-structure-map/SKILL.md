---
name: scout-structure-map
description: "Map the current structure, boundaries, and responsibility splits inside a bounded scope. Use when the main job is to understand how the system is shaped now, not to compare options or design a new solution."
---

# Scout / Structure Map

## Purpose
Produce a structure-first map of the current system without turning the result into design or verdict work.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need to understand the current structure before planning or refactoring.
- Need to map boundaries, responsibilities, or key interactions inside a bounded scope.
- Need structure observations without slipping into implementation advice or verdict work.

## Do Not Use When
- Need option comparison rather than current-state mapping.
- Need evidence-gap analysis rather than structure explanation.
- Need debugging, implementation, or review verdicts.

## Required Inputs
- `TARGET_SCOPE` (file|module|folder|repo|artifact; required): Bounded scope to map.
- `STRUCTURE_QUESTION` (string; optional): Exact structure uncertainty to resolve. Default to the main current-state structure question when omitted.
- `MAP_FOCUS` (boundaries|responsibilities|interactions|mixed; optional; allowed: boundaries|responsibilities|interactions|mixed): Primary structure lens for the map.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Files, docs, traces, or notes already known.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Scope or interpretation limits.

## Input Contract Notes
- STRUCTURE_QUESTION should ask about the current shape of the system, not about the preferred future design.
- If STRUCTURE_QUESTION is omitted, use the default question: what are the main current boundaries, responsibilities, and interactions inside this scope.
- MAP_FOCUS narrows how the structure is described; it should not preload a verdict.
- KNOWN_EVIDENCE should point to real artifacts only.

## Structured Outputs
- `BOUNDARY_MAP` (list; required; shape: {BOUNDARY, RESPONSIBILITY, INTERACTION}): Main boundaries and what each one owns.
- `STRUCTURE_NOTES` (list; required; shape: {OBSERVATION, LOCATION, WHY_IT_MATTERS}): Observed structure facts that explain the current shape.
- `OPEN_STRUCTURE_QUESTIONS` (list; required; shape: {QUESTION, CHEAPEST_NEXT_CHECK}): Remaining structure questions that still need evidence.

## Output Contract Notes
- BOUNDARY_MAP should describe the current ownership split, not a proposed redesign.
- STRUCTURE_NOTES should stay grounded in observed artifacts.
- OPEN_STRUCTURE_QUESTIONS may be empty when the current structure is sufficiently explained for the stated question.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Current-state structure mapping should expose boundaries, responsibilities, and explicit interactions without skipping straight to redesign.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: structure-map.v1

## Neutrality Rules
- Map the current structure before suggesting improvements.
- Separate observed boundaries from inferred responsibilities.
- Do not invent design recommendations when the job is current-state mapping only.

## Execution Constraints
- Do not collapse the map into vague architecture prose.
- Keep the output bounded to the stated structure question.
- Prefer a small explicit map over a broad narrative dump.
- If the source material is long, extract 3-7 anchor facts first and include at least one anchor from the middle when it changes the shape of the map.
- Before finalizing the map, ask 2-4 verification questions about potentially missing boundaries, responsibilities, or interactions and rescan the evidence against them.
- If the first pass misses a salient boundary or edge already named by the anchors, rewrite once with higher density instead of widening the scope.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Show the boundary map as a compact list:
- [boundary] — owns: [responsibility] — interacts with: [other boundary]

Follow with structure notes that explain any non-obvious shapes.

Flag open questions: "Didn't check: [areas not covered by evidence]"

Ask: "Want to go deeper on [most interesting or uncertain boundary]?"

## Mandatory Rules
- Do not finalize `BOUNDARY_MAP` until the anchor facts and verification pass agree that the main current boundaries and interactions were actually covered.
