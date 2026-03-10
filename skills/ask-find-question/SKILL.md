---
name: ask-find-question
description: "Turn fuzzy intent into one clear problem statement and a small question handle. Use when the user does not know how to ask yet, feels mentally foggy, or needs the question boundary tightened before deeper design."
---

# Question Clarify

## Purpose
Convert a vague thought into a bounded problem statement with a few stable question anchors.

## Default Program
```text
[stages: preflight>detect>analyze>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: inversion-focus | output: md(contract=v1)]
```

## Use When
- Need to turn a fuzzy thought into one clear question handle.
- Need to reduce mental overload before deeper question design.
- Need a bounded problem statement rather than broad ideation.

## Do Not Use When
- Already have a clear bounded question.
- Need the final answer directly.
- Need repository analysis, implementation, or review.

## Required Inputs
- `RAW_TOPIC` (string; required): Messy topic, rough thought, or problem statement draft.
- `AUDIENCE` (string; optional): Who the future answer or decision is for.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Known time, resource, domain, or evidence constraints.

## Input Contract Notes
- RAW_TOPIC can be messy; the skill should reduce ambiguity instead of demanding a polished first draft.
- If the user does not provide explicit constraints, infer only the single most limiting constraint from the prompt and mark it as inferred.
- Ask what should be avoided before expanding ideal outcomes.

## Structured Outputs
- `FOG_KEYS` (list; required; shape: {KEYWORD}): Three concrete anchor words that represent the core issue.
- `NEGATIVE_SPACE` (list; required; shape: {AVOID}): What the future question should avoid or not become.
- `PRIMARY_CONSTRAINT` (string; required): Single dominant constraint that most limits the question.
- `PROBLEM_STATEMENT` (string; required): One clear problem-definition sentence.
- `NEXT_RECOMMENDED_SKILL` (string; required): Smallest useful next question-design step.

## Output Contract Notes
- FOG_KEYS should stay short and concrete, not abstract themes.
- PROBLEM_STATEMENT should express one bounded question direction, not a list of possible asks.
- NEXT_RECOMMENDED_SKILL should usually point to ask-break-it-down unless the question is already bounded enough to ask.

## Primary Lens
- `primary_lens`: `inversion-focus`
- `frame_name`: Fog-to-Problem Definer
- `why`: Question clarification should lower cognitive load, define the negative boundary first, and collapse ambiguity into one usable problem statement.
- `summary`: Reduce cognitive load, define by exclusions and one dominant constraint, then state the problem plainly.
- `thesis`: When the question is still foggy, do not chase the perfect prompt first; anchor on a few concrete signals, ask what must not happen, identify the biggest constraint, and turn that into one clear problem statement.
- `decision_rules`:
  - Reduce the input surface to a few concrete anchors before expanding the problem.
  - Ask what must not happen before asking for the ideal outcome.
  - Identify one dominant constraint before exploring multiple options.
  - Return one clear problem statement rather than a menu of fuzzy prompts.
- `anti_patterns`:
  - Broad ideation while the problem is still blurry
  - Many possible goals with no negative boundary
  - Treating every constraint as equally important
- `good_for`:
  - question clarification
  - problem framing
  - scope narrowing
- `not_for`:
  - final answer generation
  - repository implementation
  - release judgement
- `required_artifacts`:
  - Anchor Words
  - Negative Space
  - Dominant Constraint
  - Problem Statement
- `references`:
  - https://fs.blog/inversion/
  - https://thedecisionlab.com/biases/cognitive-load

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: ask-find-question.v1

## Neutrality Rules
- Do not answer the topic while clarifying the question.
- Separate what the user wants from what the user wants to avoid.
- If the prompt stays ambiguous, narrow to one problem statement instead of inventing extra goals.

## Execution Constraints
- Reduce the thought to three anchors, one dominant constraint, and one problem statement.
- Prefer the shortest clear wording that helps the user take control of the question.
- Do not expand into solution advice or answer content.

## Mandatory Rules
- Always emit exactly one PROBLEM_STATEMENT.
- Keep FOG_KEYS to three items unless the prompt gives fewer usable anchors.

## Output Discipline
- `response_profile=clarify_question`
- User-facing rendering is delegated to `respond`.
