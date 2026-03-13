---
name: scout-scope
description: "Use when requirements are vague and must be clarified into precise goal, scope, constraints, and acceptance criteria. Do not use when the primary task is implementation, debugging, or deep repository analysis. If scope direction is known and only boundary formalization is needed, use scout-boundaries instead."
---

# Scout / Scope

## Purpose
Turn vague requests into concrete goal, scope, constraints, and acceptance criteria.

## Default Program
```text
[stages: preflight>detect>analyze>plan>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{docs},deterministic-output |
 lens: minto-pyramid |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `minto-pyramid` because it keeps the work aligned with: Lead with the answer, group supporting points logically, and make scope and evidence hierarchy explicit.

## Use When
- Requirements are ambiguous.
- Completion criteria are missing or conflicting.
- Need clarification questions before planning or implementation.

## Do Not Use When
- Need direct implementation.
- Need deep repository analysis rather than requirement clarification.
- The immediate job is only to formalize an already-understood boundary into a scope contract — use scout-boundaries instead.

## Required Inputs
- `REQUEST` (string; required): Ambiguous request or work item.
- `TARGET_SCOPE` (file|module|folder|repo|artifact; required): Target scope under discussion.
- `KNOWN_CONSTRAINTS` (list; optional): Explicit constraints, non-goals, or deadlines.
- `KNOWN_DONE_CONDITION` (list; optional): Any existing completion rule.

## Input Contract Notes
- REQUEST should describe the work item in its original ambiguous form, not pre-interpreted or pre-scoped.
- TARGET_SCOPE should identify the bounded area under discussion, not the entire repo unless the real uncertainty spans the full codebase.
- KNOWN_CONSTRAINTS should contain stated limits only; do not infer constraints from context or prior conversation.
- If the scope direction is already clear and only boundary formalization is needed, use `scout-boundaries` instead.

## Structured Outputs
- `CLARIFYING_QUESTIONS` (list; required; shape: {QUESTION, WHY_BLOCKING}): Ordered clarification questions if needed, most blocking first.
- `DRAFT_SCOPE_CONTRACT` (object; required; shape: {GOAL, SCOPE, CONSTRAINTS, ACCEPTANCE_BOUNDARY}): Goal, scope, constraints, and acceptance boundary draft.
- `OUT_OF_SCOPE` (list; required): Explicit out-of-scope items.

## Output Contract Notes
- CLARIFYING_QUESTIONS may be empty when the requirement is specific enough to produce a complete DRAFT_SCOPE_CONTRACT without guessing.
- DRAFT_SCOPE_CONTRACT should state the goal, constraints, and acceptance boundary; do not conflate it with an implementation plan.
- OUT_OF_SCOPE must name explicit exclusions; do not leave the out-of-scope boundary implicit.

## Primary Lens
- `primary_lens`: `minto-pyramid`
- `why`: Clarification should turn a vague request into an answer-first scope contract with grouped questions.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: clarify-contract.v1

## Neutrality Rules
- Separate explicit user constraints from inferred assumptions.
- If scope or done condition is unresolved, surface it as a question instead of deciding silently.
- Keep clarification bounded to goal, scope, constraints, and acceptance boundary.

## Execution Constraints
- Do not turn scope clarification into implementation planning or architecture advice.
- Order CLARIFYING_QUESTIONS by blocking priority — lead with the most critical ambiguity first.
- Stop when the goal, scope, and acceptance criteria can be stated without guessing.
- If the request context is long or noisy, recite 3-5 explicit goal, constraint, or done-condition anchors before drafting the scope contract.
- Ask 2-4 verification questions that distinguish explicit user facts from your own assumptions, then rescan before finalizing the contract.
- If the first draft omits a salient anchor, rewrite once with higher information density instead of adding broader speculation.

## Response Format

Show the draft scope contract:
- Goal: [one sentence]
- In scope: [list]
- Out of scope: [list]
- Acceptance boundary: [done when ...]

List clarifying questions ordered by how much they block the contract, most blocking first.

Didn't lock: [any edge that is still an assumption rather than an explicit fact].

Ask the most blocking clarification if any remain open.

## Mandatory Rules
- Do not finalize `DRAFT_SCOPE_CONTRACT` while a key goal, constraint, or acceptance condition appears only as an unstated assumption rather than an anchored fact or an explicit open question.
