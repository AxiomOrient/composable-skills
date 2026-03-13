---
name: clarify-boundaries
description: "Formalize an understood scope into an explicit in/out-of-scope boundary, done condition, and scope contract. Use when direction is clear but boundaries need to be written down before planning work starts."
---

# Clarify / Boundaries

## Purpose
Reduce a broad request to an explicit scope contract — in/out-of-scope, done condition, constraints — that downstream planning or spec skills can consume directly.

## Default Program
```text
[stages: preflight>detect>analyze>plan>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: minto-pyramid | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `minto-pyramid` because it keeps the work aligned with: Lead with the answer, group supporting points logically, and make scope and evidence hierarchy explicit.

## Use When
- Need to lock goal, scope, constraints, and done condition before planning.
- Need to separate in-scope, out-of-scope, and acceptance boundary explicitly.
- Need a scope contract before writing specs or tasks.

## Do Not Use When
- Requirements are still ambiguous and clarifying questions are needed first — use `clarify-scope` instead.
- Already have a precise scope contract.
- Need direct implementation or review work.

## Required Inputs
- `REQUEST` (string; required): Original user request or work item.
- `TARGET_SCOPE` (path|module|repo|artifact; required): Bounded area under discussion.
- `KNOWN_CONSTRAINTS` (list; optional): Explicit constraints or non-goals already known.

## Structured Outputs
- `GOAL` (string; required): Normalized goal statement.
- `IN_SCOPE` (list; required): Items or paths inside the scope boundary.
- `OUT_OF_SCOPE` (list; required): Items explicitly excluded.
- `DONE_CONDITION` (list; required): Completion contract for downstream work.
- `UNRESOLVED_EDGES` (list; required; shape: {EDGE, WHY_UNRESOLVED}): Scope edges that could not be locked without more information.

## Output Contract Notes
- GOAL should be one sentence.
- IN_SCOPE and OUT_OF_SCOPE should be explicit lists, not narrative paragraphs.
- DONE_CONDITION should translate the goal into verifiable completion checks.
- UNRESOLVED_EDGES may be empty when scope is sufficiently clear.

## Primary Lens
- `primary_lens`: `minto-pyramid`
- `why`: Scope contracts should state the answer first, then bound in-scope, out-of-scope, and done criteria.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: scope-contract.v1

## Neutrality Rules
- Separate explicit constraints from inferred assumptions.
- Mark unresolved scope edges instead of silently deciding them.
- Do not turn preference into scope without evidence.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

목표: [한 문장]

- 포함: [목록]
- 제외: [목록]
- 완료 조건: [기준 목록]

아직 못 정한 것이 있으면: "아직 열려있음: [정보 없어서 못 정한 것]"

못 정한 것 중 계획에 가장 영향 큰 것 질문.

## Mandatory Rules
- Keep the output contract-first and compact.
- Do not emit a full implementation plan here.

## Example Invocation
```text
$clarify-boundaries
REQUEST: simplify the auth module without behavior change
SCOPE: src/auth
```
