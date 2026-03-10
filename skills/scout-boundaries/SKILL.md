---
name: scout-boundaries
description: "Define the exact goal, scope boundary, constraints, and done condition before planning or specification work. Use when the request is still too broad to turn directly into a plan or spec."
---

# Scope Contract Map

## Purpose
Reduce a broad request to an explicit scope contract that downstream planning or spec skills can consume.

## Default Program
```text
[stages: preflight>detect>analyze>plan>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: minto-pyramid | output: md(contract=v1)]
```

## Use When
- Need to lock goal, scope, constraints, and done condition before planning.
- Need to separate in-scope, out-of-scope, and acceptance boundary.
- Need a bounded contract before writing specs or tasks.

## Do Not Use When
- Already have a precise scope contract.
- Need direct implementation or review work.
- Need full planning artifacts rather than scope normalization only.

## Required Inputs
- `REQUEST` (string, required): Original user request or work item.
- `TARGET_SCOPE` (path|module|repo|artifact, required): Bounded area under discussion.
- `KNOWN_CONSTRAINTS` (list, optional): Explicit constraints or non-goals already known.

## Structured Outputs
- `GOAL` (string, required): Normalized goal statement.
- `IN_SCOPE` (list, required): Items or paths inside the scope boundary.
- `OUT_OF_SCOPE` (list, required): Items explicitly excluded.
- `DONE_CONDITION` (list, required): Completion contract for downstream work.

## Procedure
1. Normalize the request into one clear goal statement.
2. Draw the in-scope and out-of-scope boundary explicitly.
3. Convert constraints into a concrete done condition.
4. Return a stable scope contract for planner or spec.

## Primary Lens
- `primary_lens`: `minto-pyramid`
- `frame_name`: Answer-First Structurer
- `why`: Scope contracts should state the answer first, then bound in-scope, out-of-scope, and done criteria.
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
- `artifacts_out`: scope-contract.v1

## Neutrality Rules
- Separate explicit constraints from inferred assumptions.
- Mark unresolved scope edges instead of silently deciding them.
- Do not turn preference into scope without evidence.

## Mandatory Rules
- Keep the output contract-first and compact.
- Do not emit a full implementation plan here.

## Example Invocation
```text
$scout-boundaries
REQUEST: simplify the auth module without behavior change
TARGET_SCOPE: src/auth
```

## Output Discipline
- `response_profile=planning_doc`
- User-facing rendering is delegated to `respond`.

