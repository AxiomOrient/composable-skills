---
name: plan-why-build-this
description: "Use when turning a rough idea into a short product brief that names the user, problem, intended outcome, success signals, and non-goals before writing specs or design docs. Do not use for detailed feature requirements or technical solution design."
---

# Plan / Why Build This

## Purpose
Capture why the work matters, for whom it matters, and what success looks like before deeper specification begins.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: repo|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat},deterministic-output |
 lens: christensen-jtbd |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `christensen-jtbd` because it keeps the work aligned with: Define customer progress as job-to-be-done and map competing alternatives.

## Use When
- Need a high-level brief before feature spec or design work.
- Need to make audience, problem, success signals, and non-goals explicit.
- Need one short alignment document that prevents premature solution design.

## Do Not Use When
- Need detailed functional requirements or edge-case behavior.
- Need navigation structure or information hierarchy.
- Need technical boundaries, data flow, or implementation trade-offs.

## Required Inputs
- `BRIEF_SCOPE` (feature|initiative|product|project; required): Boundary the brief governs.
- `PROBLEM_STATEMENT` (string; required): Plain-language statement of the problem worth solving.
- `TARGET_AUDIENCE` (list; required; shape: {USER, CONTEXT}): Primary users or stakeholder groups and the context they are in.
- `DESIRED_OUTCOMES` (list; required; shape: {OUTCOME, WHY_IT_MATTERS}): Intended outcomes and why each one matters.
- `SUCCESS_SIGNALS` (list; required; shape: {SIGNAL, HOW_MEASURED}): Observable signals or metrics that indicate the brief succeeded.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Explicit time, policy, compatibility, resource, or non-goal constraints.
- `KNOWN_NON_GOALS` (list; optional; shape: {NON_GOAL, WHY_OUT}): Items that should stay out of scope even if adjacent to the problem.

## Input Contract Notes
- PROBLEM_STATEMENT should stay problem-first and avoid embedding a preferred solution.
- TARGET_AUDIENCE should be specific enough that a later spec can make trade-offs for real users rather than a generic 'everyone'.
- SUCCESS_SIGNALS should be observable. If exact metrics are unknown, use proxy signals rather than aspirational language.
- KNOWN_NON_GOALS should be explicit when adjacent asks are likely to create scope creep.

## Structured Outputs
- `BRIEF_SUMMARY` (string; required): One short summary of the problem, target user, and intended outcome.
- `USER_JOBS` (list; required; shape: {USER, JOB, PAIN}): User jobs and pain points implied by the brief.
- `OUTCOME_PRIORITIES` (list; required; shape: {OUTCOME, SIGNAL, PRIORITY}): Ranked outcomes and the signal that will show whether each one improved.
- `NON_GOALS` (list; required; shape: {NON_GOAL, WHY_OUT}): Explicitly excluded work or expectations.
- `OPEN_ASSUMPTIONS` (list; required; shape: {ASSUMPTION, WHY_IT_MATTERS}): Assumptions that later spec or validation work must confirm.

## Output Contract Notes
- BRIEF_SUMMARY should stay short enough that it can anchor later spec work without becoming a long concept document.
- USER_JOBS should describe user needs, not solution ideas dressed up as needs.
- OUTCOME_PRIORITIES should rank what matters most instead of treating every goal as equally critical.
- OPEN_ASSUMPTIONS should stay explicit rather than being buried in prose.

## Primary Lens
- `primary_lens`: `christensen-jtbd`
- `why`: A product brief should clarify the user job, pain, and desired progress before the team writes detailed requirements or solution documents.

## Artifacts
- `artifacts_in`: scope-contract.v1
- `artifacts_out`: plan-why-build-this.v1

## Neutrality Rules
- Separate user problem from preferred solution.
- Do not invent business impact or certainty that the inputs do not support.
- Keep non-goals and open assumptions visible instead of implying universal buy-in.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Lead with the brief summary in two sentences: who, what problem, what outcome.

Show ranked outcomes and their success signals:
- [outcome] → signal: [how measured] — priority: [1/2/3]

List non-goals explicitly — what is deliberately out of scope.

Flag open assumptions that later spec work must confirm.

Ask: "Is the success signal for [highest-priority outcome] measurable, or is it still a proxy?"

## Execution Constraints
- Do not turn this skill into a detailed feature spec or technical design document.
- Prefer the smallest brief that still makes user, outcome, and scope boundaries explicit.
- If the audience or success signal is unclear, surface it as an assumption rather than guessing silently.

## Example Invocation
```text
$plan-why-build-this
BRIEF_SCOPE: feature
PROBLEM_STATEMENT: new users get lost on the setup screen after first login
TARGET_AUDIENCE:
  - USER: new administrator
    CONTEXT: right after the first workspace setup
DESIRED_OUTCOMES:
  - OUTCOME: reduce time to complete the first setup
    WHY_IT_MATTERS: reducing early drop-off matters
SUCCESS_SIGNALS:
  - SIGNAL: increase first-setup completion rate
    HOW_MEASURED: 7-day cohort completion rate
```
