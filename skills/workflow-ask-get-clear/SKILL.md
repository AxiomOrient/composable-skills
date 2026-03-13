---
name: workflow-ask-get-clear
description: "Workflow skill that turns a fuzzy topic into one clear problem statement and a usable question stack. Use when the user needs help getting clear before deeper reframing or before asking for the answer."
---

# Workflow / Ask Get Clear

## Purpose
Compose question clarification and scaffolding into one reusable question-design workflow.

## Default Program
```text
[stages: preflight>detect>analyze>plan>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: inversion-focus | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `inversion-focus` because it keeps the work aligned with: Reduce cognitive load, define by exclusions and one dominant constraint, then state the problem plainly.

## Use When
- Need a clear problem statement and question stack in one pass.
- Need a reusable workflow entrypoint before deeper challenge or answer work.
- Need a named composition rather than manually listing clarify plus scaffold each time.

## Do Not Use When
- Need assumption-challenging reframing in the same workflow.
- Need the final answer directly.
- Need repository or implementation work.

## Required Inputs
- `TOPIC` (string; required): Raw topic or rough thought to clarify into a question.
- `AUDIENCE` (string; optional): Target reader or decision-maker for the future answer.
- `CONSTRAINTS` (list; optional): Scope, evidence, time, or deliverable constraints.

## Input Contract Notes
- TOPIC can be rough or messy; this workflow exists to turn that into a usable question handle.
- Keep CONSTRAINTS short and concrete; the workflow will surface the dominant one.
- AUDIENCE is optional because many first-pass question-shaping requests do not need a named reader yet.

## Structured Outputs
- `PROBLEM_STATEMENT` (string; required): Single clear problem-definition sentence.
- `QUESTION_STACK` (question-stack.v1; required): Prioritized stack of askable questions.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Expanded atomic path used by the workflow.

## Output Contract Notes
- QUESTION_STACK should stay short enough to act on immediately.
- EXPANDED_ATOMIC_PATH must preserve the real execution order.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: ask-form-question.v1, question-stack.v1

## Neutrality Rules
- Preserve the neutrality rules of each underlying atomic skill.
- Do not expand into answer content while shaping the question.
- Keep the workflow transparent by exposing the expanded skill list.

## Execution Constraints
- Prefer one usable problem statement over multiple half-bounded prompts.
- Keep the stack focused on the core decision the audience actually needs.

## Response Format

Output the result directly — no preamble, no chain commentary.

**CORE_QUESTION:** [one sentence, plain language]

If a question stack was produced, show it:
1. [most important] — why this matters
2. [next]

If a step failed, say which and ask: "Want to try a different angle?"

## Mandatory Rules
- Expose the expanded atomic path explicitly.
- Keep the workflow output short enough that the user can ask or refine the question immediately.

## Expansion
- `$ask-form-question`
- `$ask-break-it-down`

## Example Invocation
```text
$workflow-ask-get-clear
TOPIC: Would adopting an AI code review tool actually improve team productivity?
AUDIENCE: engineering manager
```
