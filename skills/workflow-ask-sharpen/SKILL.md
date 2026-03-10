---
name: workflow-ask-sharpen
description: "Workflow skill that turns a fuzzy topic into a clear problem statement, a usable question stack, and two challenge questions. Use when the user wants a question that is actually worth asking, not just a longer prompt."
---

# Workflow / Ask Sharpen

## Purpose
Compose the core question-design path into one explicit ready-to-ask workflow.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: popper-falsification | output: md(contract=v1)]
```

## Use When
- Need a question that is ready to ask, not just a rough draft.
- Need assumption-challenging reframing after the first question stack is built.
- Need a stable named workflow for practical question design.

## Do Not Use When
- Already have a clear question and only need repair after a failed answer.
- Need repair-after-failure rather than first-pass question preparation.
- Need code or repository work.

## Required Inputs
- `TOPIC` (string; required): Raw topic or rough thought to prepare into a strong question.
- `AUDIENCE` (string; optional): Target reader or decision-maker for the future answer.
- `CONSTRAINTS` (list; optional): Scope, evidence, time, or deliverable constraints.

## Input Contract Notes
- TOPIC can be rough; this workflow exists to turn it into a sharper ask.
- CONSTRAINTS should be real limits that change the shape of the question, not a long wishlist.
- AUDIENCE is optional because many first-pass question-shaping requests do not need a named reader yet.

## Structured Outputs
- `PROBLEM_STATEMENT` (string; required): Single clear problem-definition sentence.
- `CORE_QUESTION` (string; required): Main question to ask first.
- `CHALLENGE_QUESTIONS` (list; required; shape: {QUESTION, WHY_IT_CHANGES_THE_VIEW}): Two challenge questions that test or widen the framing.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Expanded atomic path used by the workflow.

## Output Contract Notes
- CHALLENGE_QUESTIONS should force the user to test assumptions rather than decorate the prompt.
- EXPANDED_ATOMIC_PATH must preserve the real execution order.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: ask-form-question.v1, question-stack.v1, ask-flip-assumption.v1

## Neutrality Rules
- Preserve the neutrality rules of each underlying atomic skill.
- Do not present the question as answer-worthy if the workflow still exposes major framing confusion.
- Keep workflow output explicit enough for downstream repair loops.

## Execution Constraints
- Keep the final question set short enough that a user can ask it immediately.
- Prefer challenge questions that materially change the answer over stylistic rewording.

## Mandatory Rules
- Expose the expanded atomic path explicitly.
- Keep the final output askable without requiring another redesign pass.

## Expansion
- `$ask-form-question`
- `$ask-break-it-down`
- `$ask-flip-assumption`

## Example Invocation
```text
$workflow-ask-sharpen
TOPIC: Would introducing an AI code review tool actually improve productivity for our team?
AUDIENCE: engineering manager
```
