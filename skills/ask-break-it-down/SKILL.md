---
name: ask-break-it-down
description: "Break one big question into a prioritized question stack using first principles and explicit data/control framing. Use when the scope is too broad or multiple goals are tangled together."
---

# Question Scaffold

## Purpose
Turn one broad problem statement into a small, prioritized stack of askable subquestions.

## Default Program
```text
[stages: preflight>detect>analyze>plan>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

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
- `primary_lens`: `hickey-carmack`
- `frame_name`: Data-First Systems Pragmatist
- `why`: Question scaffolding should expose the core invariant, split layers cleanly, and choose the smallest explicit question stack that preserves the real decision.
- `summary`: Data model first, explicit side effects, and explicit performance characteristics.
- `thesis`: Make the structure and cost of the system visible first, then prefer the simplest explicit mechanism that preserves correctness.
- `core_philosophy`: Start from the essential user-visible or contract-visible outcome, keep the mechanism explicit, and remove accidental complexity before adding more structure.
- `mental_model`:
  - Name the core outcome and invariant before changing code.
  - Make data shape, side effects, and cost visible enough to reason about.
  - Choose the smallest explicit change that satisfies the contract.
  - Add abstraction only when it removes proven duplication or protects a real invariant.
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
- `artifacts_in`: ask-find-question.v1
- `artifacts_out`: question-stack.v1

## Neutrality Rules
- Do not answer the question while scaffolding it.
- Prefer one prioritized stack over many equal-weight branches.
- If a layer does not materially change the decision, omit it.

## Execution Constraints
- Separate business purpose, technical implementation, and user experience when the prompt mixes them.
- Use Hickey-Carmack style data-first and explicit-control framing to remove hidden complexity.
- Keep the stack minimal and focused on the core question.

## Mandatory Rules
- Return 3 to 5 QUESTION_LAYERS items total.
- Always emit exactly one CORE_QUESTION.

## Output Discipline
- `response_profile=question_stack`
- User-facing rendering is delegated to `respond`.
