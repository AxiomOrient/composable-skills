---
name: ask-flip-assumption
description: "Challenge the default framing by listing assumptions, reversing them, and generating a small set of perspective-shifting questions. Use when the question is stuck, too feature-centric, or needs a sharper angle."
---

# Question Reframe

## Purpose
Break question deadlock by exposing assumptions and generating a few high-value reframed questions.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: popper-falsification | output: md(contract=v1)]
```

## Use When
- Need to break a question deadlock or escape one habitual framing.
- Need to challenge hidden assumptions before asking the final question.
- Need a sharper angle than a feature-centric or default-solution question.

## Do Not Use When
- Need raw clarification because the problem statement is still too vague.
- Need repository work or code changes.
- Need a full answer instead of better question framing.

## Required Inputs
- `CORE_QUESTION` (string; required): Current main question to challenge.
- `ASSUMPTIONS` (list; optional; shape: {ASSUMPTION}): Assumptions already identified by the user.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Known scope, evidence, or domain limits.

## Input Contract Notes
- If ASSUMPTIONS are not given, infer only the few assumptions that most constrain the question.
- Reframing should challenge the question angle, not invent a new unrelated topic.
- Use biological or system metaphors only if they sharpen the question instead of adding ornament.

## Structured Outputs
- `ASSUMPTION_LIST` (list; required; shape: {ASSUMPTION}): Three assumptions currently shaping the question.
- `REVERSAL_TESTS` (list; required; shape: {ASSUMPTION, REVERSAL}): Reversal tests that challenge each assumption.
- `CHALLENGE_QUESTIONS` (list; required; shape: {QUESTION, WHY_IT_CHANGES_THE_VIEW}): Two perspective-shifting questions.
- `EXPECTED_FEEDBACK` (list; required; shape: {QUESTION, EXPECTED_SIGNAL}): What kind of new information each challenge question is likely to unlock.
- `NEXT_RECOMMENDED_SKILL` (string; required): Smallest useful next step after reframing.

## Output Contract Notes
- CHALLENGE_QUESTIONS should contain exactly two questions.
- Each reversal should directly challenge one assumption from ASSUMPTION_LIST.
- EXPECTED_FEEDBACK should describe what new signal the reframe would reveal, not a full answer.

## Primary Lens
- `primary_lens`: `popper-falsification`
- `frame_name`: Disconfirming Question Designer
- `why`: Question reframing should break confirmation bias, expose hidden assumptions, and generate challenge questions that can actually change the downstream answer.
- `summary`: Prefer questions that expose testable claims, disconfirming edges, and evidence burdens.
- `thesis`: A strong question is not merely broad or clever; it creates a surface where claims can fail, evidence can discriminate, and weak answers become obvious.
- `decision_rules`:
  - Rewrite vague prompts into claim-bearing questions with observable failure conditions.
  - Name the evidence burden required for a strong answer.
  - Expose disconfirming edges instead of prompting only for confirmation.
  - Penalize question forms that permit high-fluency but low-testability answers.
- `anti_patterns`:
  - Open-ended prompts with no failure condition
  - Questions that reward rhetoric over evidence
  - Forecasts with no explicit claim surface
- `good_for`:
  - question forging
  - question evaluation
  - answer forecasting
- `not_for`:
  - documentation structure
  - dependency planning
  - release gate review
- `required_artifacts`:
  - Claim Surface
  - Disconfirming Edge
  - Evidence Burden
  - Failure Condition
- `references`:
  - https://www.britannica.com/biography/Karl-Popper

## Artifacts
- `artifacts_in`: question-stack.v1
- `artifacts_out`: ask-flip-assumption.v1

## Neutrality Rules
- Do not smuggle a preferred answer into the reframed questions.
- Challenge assumptions, not the user.
- Keep the reframe anchored to the original decision or problem.

## Execution Constraints
- List only the assumptions that materially shape the current question.
- Prefer one strong reversal over many decorative what-if prompts.
- Keep the challenge questions short, specific, and usable.

## Mandatory Rules
- Return exactly two CHALLENGE_QUESTIONS.
- Each CHALLENGE_QUESTIONS item must connect to an explicit reversal test.

## Output Discipline
- `response_profile=analysis_report`
- User-facing rendering is delegated to `respond`.
