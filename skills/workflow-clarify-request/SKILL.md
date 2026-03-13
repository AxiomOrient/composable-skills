---
name: workflow-clarify-request
description: "Workflow skill that turns a fuzzy topic into a clear problem statement, a usable question stack, and challenge questions. Use when the user wants a question that is actually worth asking, not just a longer prompt."
---

# Workflow / Clarify Request

## Purpose
Compose the core question-design path into one explicit ready-to-ask workflow.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: popper-falsification | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `popper-falsification` because it keeps the work aligned with: Prefer questions that expose testable claims, disconfirming edges, and evidence burdens.

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
- `artifacts_out`: ask-clarify-question.v1, question-stack.v1, ask-flip-assumption.v1

## Neutrality Rules
- Preserve the neutrality rules of each underlying atomic skill.
- Do not present the question as answer-worthy if the workflow still exposes major framing confusion.
- Keep workflow output explicit enough for downstream repair loops.

## Execution Constraints
- Keep the final question set short enough that a user can ask it immediately.
- Prefer challenge questions that materially change the answer over stylistic rewording.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Output the sharpened result directly — no chain detail, no preamble.

**Sharpened:** [the reframed question in plain language]

Challenge questions:
1. [assumption reversal]
2. [perspective shift that changes what "good answer" means]

If any step failed, name it and ask: "Which constraint should we relax?"

## Mandatory Rules
- Expose the expanded atomic path explicitly.
- Keep the final output askable without requiring another redesign pass.

## Expansion
- `$ask-clarify-question`
- `$ask-break-it-down`
- `$ask-flip-assumption`

## Example Invocation
```text
$workflow-clarify-request
TOPIC: Would introducing an AI code review tool actually improve productivity for our team?
AUDIENCE: engineering manager
```

## Eval Cases

| Prompt | Should Trigger | Key Output Check |
|--------|---------------|-----------------|
| 내가 질문하려는 내용이 좀 모호한데, 날카롭게 다듬어서 질문 리스트 좀 뽑아줘. | YES | CORE_QUESTION 존재 |
| 이 주제로 관리자한테 물어보려는데, 놓치고 있는 반대 관점 질문도 같이 만들어봐. | YES | CHALLENGE_QUESTIONS 존재 |
| 이미 답이 틀렸는데 질문을 어떻게 고칠까? | NO | 첫 질문 설계 단계 — ask-fix-prompt 권장 |
