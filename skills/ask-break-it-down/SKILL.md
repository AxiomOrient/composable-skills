---
name: ask-break-it-down
description: "Break one bounded question into a prioritized question stack using first principles and explicit data/control framing. Use when the main question is clear enough to ask about, but still too large to answer well in one step."
---

# Ask / Break It Down

## Purpose
Turn one broad problem statement into a small, prioritized stack of askable subquestions.

## Default Program
```text
[stages: preflight>detect>analyze>plan>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need to split one large question into smaller askable units.
- Need to separate business, technical, and user layers instead of mixing them.
- Need a first-principles and data/control view before asking the final question.

## Do Not Use When
- Need to clarify the raw problem first because the topic is still foggy.
- Need a final answer rather than question design.
- Need repository work or implementation.

## Required Inputs
- `PROBLEM_STATEMENT` (string; required): Bounded problem sentence to decompose.
- `AUDIENCE` (string; optional): Who the future answer is meant to help.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Known business, technical, or evidence constraints.

## Input Contract Notes
- PROBLEM_STATEMENT should contain one bounded direction, not a bundle of unrelated asks.
- If multiple purposes are mixed together, separate them into business, technical, and user-experience layers first.
- Use first principles only to remove confusion, not to expand into theoretical essay writing.

## Structured Outputs
- `QUESTION_LAYERS` (list; required; shape: {LAYER, QUESTION, PRIORITY}): Prioritized subquestions grouped by layer.
- `FIRST_PRINCIPLES` (list; required; shape: {PRINCIPLE, WHY_IT_HOLDS}): Domain principles that should stay stable while the question is reframed.
- `DATA_CONTROL_VIEW` (string; required): Data-first and explicit-control framing of the question.
- `CORE_QUESTION` (string; required): Single main question to ask first.
- `NEXT_RECOMMENDED_SKILL` (string; required): Smallest useful next question-design step.

## Output Contract Notes
- QUESTION_LAYERS should contain only 3 to 5 questions in total.
- CORE_QUESTION should be the smallest question that unlocks the rest of the stack.
- DATA_CONTROL_VIEW should make the flow or control boundary more concrete, not more abstract.

## Primary Lens
- `primary_lens`: `eisenhower`
- `why`: Breaking one question into a prioritized stack requires separating what must be answered first (critical path) from what can wait, and pushing nice-to-have sub-questions out of the main layer so the core question stays reachable.

## Artifacts
- `artifacts_in`: ask-clarify-question.v1
- `artifacts_out`: question-stack.v1

## Neutrality Rules
- Do not answer the question while scaffolding it.
- Prefer one prioritized stack over many equal-weight branches.
- If a layer does not materially change the decision, omit it.

## Execution Constraints
- Separate business purpose, technical implementation, and user experience when the prompt mixes them.
- Use Hickey-Carmack style data-first and explicit-control framing to remove hidden complexity.
- Keep the stack minimal and focused on the core question.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

State the CORE_QUESTION first, one sentence.

Then show the question stack:
- Layer | Question | Priority

Follow with the DATA_CONTROL_VIEW in one short paragraph.

Close with: "Start with [CORE_QUESTION], or want to reframe a different layer first?"

## Mandatory Rules
- Return 3 to 5 QUESTION_LAYERS items total.
- Always emit exactly one CORE_QUESTION.
