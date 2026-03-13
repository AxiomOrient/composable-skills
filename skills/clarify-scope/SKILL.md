---
name: clarify-scope
description: "Turn vague requirements into a concrete goal, scope boundary, constraints, acceptance criteria, and explicit inclusion/exclusion list. Use when requirements are ambiguous and must be sharpened before planning or implementation."
---

# Clarify / Scope

## Purpose
Turn vague requests into concrete goal, scope, constraints, and acceptance criteria — with explicit clarifying questions for anything still unresolved.

## Default Program
```text
[stages: preflight>detect>analyze>plan>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: minto-pyramid | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `minto-pyramid` because it keeps the work aligned with: Lead with the answer, group supporting points logically, and make scope and evidence hierarchy explicit.

## Use When
- Requirements are ambiguous, missing, or conflicting.
- Completion criteria are unclear.
- Need clarification questions before planning or implementation.

## Do Not Use When
- Requirements are already clear and only boundary formalization is needed — use `clarify-boundaries` instead.
- Need direct implementation.
- Need deep repository analysis rather than requirement clarification.

## Required Inputs
- `REQUEST` (string; required): Ambiguous request or work item in its original form.
- `TARGET_SCOPE` (file|module|folder|repo|artifact; required): Target scope under discussion.
- `KNOWN_CONSTRAINTS` (list; optional): Explicit constraints, non-goals, or deadlines.
- `KNOWN_DONE_CONDITION` (list; optional): Any existing completion rules.

## Input Contract Notes
- REQUEST should describe the work item in its original ambiguous form, not pre-interpreted.
- TARGET_SCOPE should identify the bounded area, not the entire repo unless uncertainty truly spans everything.
- KNOWN_CONSTRAINTS should contain stated limits only; do not infer constraints from context.
- If scope direction is already clear and only formalization is needed, use `clarify-boundaries` instead.

## Structured Outputs
- `CLARIFYING_QUESTIONS` (list; required; shape: {QUESTION, WHY_BLOCKING}): Ordered clarification questions, most blocking first.
- `DRAFT_SCOPE_CONTRACT` (object; required; shape: {GOAL, SCOPE, CONSTRAINTS, ACCEPTANCE_BOUNDARY}): Goal, scope, constraints, and acceptance boundary draft.
- `OUT_OF_SCOPE` (list; required): Explicit out-of-scope items.

## Output Contract Notes
- CLARIFYING_QUESTIONS may be empty when the requirement is specific enough to complete without guessing.
- DRAFT_SCOPE_CONTRACT should state goal, constraints, and acceptance boundary; do not conflate with an implementation plan.
- OUT_OF_SCOPE must name explicit exclusions; do not leave boundary implicit.

## Primary Lens
- `primary_lens`: `minto-pyramid`
- `why`: Clarification should turn a vague request into an answer-first scope contract with grouped questions.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: clarify-scope.v1

## Neutrality Rules
- Separate explicit user constraints from inferred assumptions.
- If scope or done condition is unresolved, surface it as a question instead of deciding silently.
- Keep clarification bounded to goal, scope, constraints, and acceptance boundary.

## Execution Constraints
- Do not turn scope clarification into implementation planning or architecture advice.
- Order CLARIFYING_QUESTIONS by blocking priority.
- Stop when goal, scope, and acceptance criteria can be stated without guessing.
- Recite 3-5 explicit goal, constraint, or done-condition anchors before drafting the contract.
- Ask 2-4 verification questions that distinguish explicit user facts from your own assumptions.
- If the first draft omits a salient anchor, rewrite once with higher information density.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

범위 계약 초안:
- 목표: [한 문장]
- 포함: [목록]
- 제외: [목록]
- 완료 조건: [완료 기준]

명확히 해야 할 것들 (막는 순서대로):
1. [질문] — 왜 막히는지: [이유]

아직 못 정한 것: "[명시된 사실이 아니라 가정으로 남아있는 것]"

마지막에: 가장 막히는 질문 하나.

## Mandatory Rules
- Do not finalize DRAFT_SCOPE_CONTRACT while a key goal, constraint, or acceptance condition appears only as an unstated assumption.

## Example Invocation
```text
$clarify-scope
REQUEST: "simplify the auth module without breaking anything"
SCOPE: src/auth
```
