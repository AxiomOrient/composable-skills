---
name: workflow-scout-structure
description: "Workflow skill that clarifies the scope boundary first, then maps the current structure inside that scope. Use when the user needs one default scout entrypoint to understand how a bounded system is shaped now."
---

# Workflow / Scout Structure

## Purpose
Compose scope clarification and current-state structure mapping into one default scout workflow.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs,tests,security},deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need one default scout entrypoint for understanding current structure.
- Need to lock scope before mapping boundaries and responsibilities.
- Need a scout workflow that stays descriptive instead of slipping into redesign.

## Do Not Use When
- Need option comparison rather than structure mapping.
- Need evidence-gap analysis rather than current-state mapping.
- Need direct implementation or review verdicts.

## Required Inputs
- `REQUEST` (string; required): Original request or analysis intent.
- `TARGET_SCOPE` (file|module|folder|repo|artifact; required): Bounded area to analyze.
- `QUESTION` (string; required): Exact structure question to resolve.
- `MAP_FOCUS` (boundaries|responsibilities|interactions|mixed; optional): Primary structure lens for the map.
- `KNOWN_CONSTRAINTS` (list; optional): Explicit constraints or non-goals already known.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Files, docs, commands, or notes already known.

## Input Contract Notes
- REQUEST should describe the work item or uncertainty before the scope is clarified.
- QUESTION should stay structure-focused rather than solution-focused.
- MAP_FOCUS narrows the map view but should not preload a redesign recommendation.

## Structured Outputs
- `DRAFT_SCOPE_CONTRACT` (object; required): Goal, scope, constraints, and acceptance boundary draft.
- `BOUNDARY_MAP` (list; required; shape: {BOUNDARY, RESPONSIBILITY, INTERACTION}): Current boundaries and their ownership split.
- `OPEN_STRUCTURE_QUESTIONS` (list; required; shape: {QUESTION, CHEAPEST_NEXT_CHECK}): Remaining structure questions after the mapping pass.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Actual atomic path executed by the workflow.

## Output Contract Notes
- DRAFT_SCOPE_CONTRACT should remain the boundary artifact rather than a plan.
- BOUNDARY_MAP should describe the current system, not a proposed target state.
- EXPANDED_ATOMIC_PATH must preserve execution order explicitly.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: clarify-contract.v1, structure-map.v1

## Neutrality Rules
- Preserve the neutrality rules of clarify-scope and analyze-structure.
- Do not smuggle redesign, implementation, or review judgement into the workflow.
- Keep the workflow explicit enough that users can drop to the narrower atomic skill when needed.

## Execution Constraints
- Do not hide the scope-contract step when the request is still broad.
- Keep the workflow focused on current-state understanding.
- When the source material is long, keep scope clarification and structure mapping as two explicit passes instead of collapsing them into one skimmed summary.
- Final handoff should carry anchor evidence from the scope pass and the structure pass, and leave unresolved verification questions visible instead of smoothing them over.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Show per-step outcome (step → result):
- clarify-scope → scope contract: goal + acceptance boundary
- analyze-structure → boundary map + open structure questions

On failure at any step: stop and ask what blocked it.

On success: show the boundary map and list remaining structure questions with cheapest checks.

Ask: "Want to go deeper on [most interesting or uncertain boundary]?"

## Mandatory Rules
- Expose the expanded atomic path explicitly.
- Keep structure mapping visible instead of folding it into generic analysis prose.
- Do not claim the workflow is done if either atomic pass skipped its anchor-and-verification step on a long context.

## Expansion
- `$clarify-scope`
- `$analyze-structure`

## Example Invocation
```text
$workflow-scout-structure
REQUEST: understand the current auth structure before deciding where to change it
TARGET_SCOPE: src/auth
QUESTION: which module boundaries and responsibility splits matter most right now
```
