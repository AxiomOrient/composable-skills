---
name: scout-scope
description: "Use when requirements are vague and must be clarified into precise goal, scope, constraints, and acceptance criteria. Do not use when the primary task is implementation, debugging, or deep repository analysis. English triggers: clarify requirements, define scope, define done criteria."
---

# Scope Clarifier

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

## Use When
- Requirements are ambiguous.
- Completion criteria are missing or conflicting.
- Need clarification questions before planning or implementation.

## Do Not Use When
- Need direct implementation.
- Need deep repository analysis rather than requirement clarification.
- The immediate job is only to normalize scope contract.

## Required Inputs
- `REQUEST` (string, required): Ambiguous request or work item.
- `TARGET_SCOPE` (file|module|folder|repo|artifact, required): Target scope under discussion.
- `KNOWN_CONSTRAINTS` (list, optional): Explicit constraints, non-goals, or deadlines.
- `KNOWN_DONE_CONDITION` (list, optional): Any existing completion rule.

## Structured Outputs
- `CLARIFYING_QUESTIONS` (list, required): Ordered clarification questions if needed.
- `DRAFT_SCOPE_CONTRACT` (object, required): Goal, scope, constraints, and acceptance boundary draft.
- `OUT_OF_SCOPE` (list, required): Explicit out-of-scope items.

## Primary Lens
- `primary_lens`: `minto-pyramid`
- `frame_name`: Answer-First Structurer
- `why`: Clarification should turn a vague request into an answer-first scope contract with grouped questions.
- `summary`: Lead with the answer, group supporting points logically, and make scope and evidence hierarchy explicit.
- `thesis`: A useful contract starts with the answer, then groups supporting points so scope, decision logic, and acceptance boundaries are immediately visible.
- `decision_rules`:
  - State the answer or contract first before details.
  - Group supporting points into stable buckets instead of chronological narration.
  - Make in-scope, out-of-scope, and done criteria explicit.
  - Remove sections that do not change the decision or acceptance boundary.
- `anti_patterns`:
  - Context dump before conclusion
  - Checklist without grouping logic
  - Mixed scope and acceptance criteria
- `good_for`:
  - clarification
  - spec writing
  - documentation
  - scope contracts
  - commit summaries
- `not_for`:
  - root-cause debugging
  - failure-path investigation
  - throughput optimization
- `required_artifacts`:
  - Answer First
  - Grouped Arguments
  - Scope Boundary
  - Acceptance Boundary
- `references`:
  - https://barbaraminto.com/

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: clarify-contract.v1

## Neutrality Rules
- Separate explicit user constraints from inferred assumptions.
- If scope or done condition is unresolved, surface it as a question instead of deciding silently.
- Keep clarification bounded to goal, scope, constraints, and acceptance boundary.

## Output Discipline
- `response_profile=clarify_question`
- User-facing rendering is delegated to `respond`.
