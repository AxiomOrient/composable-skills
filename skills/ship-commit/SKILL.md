---
name: ship-commit
description: "Use when generating Conventional Commit message candidates from an existing diff or change summary. Do not use when implementation, debugging, or review analysis is requested. English triggers: commit message, conventional commit, commit title."
---

# Commit

## Purpose
Generate precise Conventional Commit proposals from an existing diff or structured change summary.

## Default Program
```text
[stages: preflight>detect>analyze>handoff>audit |
 scope: diff |
 policy: evidence,deterministic-output |
 lens: minto-pyramid |
 output: md(contract=v1)]
```

## Use When
- Need commit message candidates after the implementation is already done.
- Need commit type, scope, and breaking-change status inferred from evidence.
- Need 3-5 stable commit candidates with rationale.

## Do Not Use When
- Need implementation, debugging, or review work.
- Need release decision rather than commit wording.
- There is no diff or change summary to summarize.

## Required Inputs
- `DIFF_SUMMARY` (diff|change-summary; required): Diff or structured summary of the completed changes.
- `CHANGE_INTENT` (string; required): What the change was meant to accomplish.
- `SCOPE_HINT` (string; optional): Optional conventional-commit scope hint.
- `BREAKING_CHANGE` (yes|no|uncertain; optional): Breaking-change status if already known.

## Input Contract Notes
- DIFF_SUMMARY should reflect completed changes only; this skill does not invent intent that is absent from the diff.
- CHANGE_INTENT should describe the actual purpose of the change, not the commit wording you hope to get.
- Use SCOPE_HINT only when it clarifies the conventional-commit scope rather than forcing a misleading one.

## Structured Outputs
- `TOP_CANDIDATE` (string; required): Best commit candidate.
- `ALTERNATIVES` (list; required; shape: {MESSAGE, WHY}): Alternative commit candidates.
- `BODY_FOOTER_NOTES` (list; required; shape: {NOTE, WHEN_TO_USE}): Optional body/footer notes such as BREAKING CHANGE.

## Output Contract Notes
- TOP_CANDIDATE should be the shortest accurate Conventional Commit message that fits the evidenced change.
- Use ALTERNATIVES when type, scope, or emphasis is genuinely ambiguous instead of pretending there is only one valid message.
- BODY_FOOTER_NOTES should stay empty when no justified footer is needed.

## Primary Lens
- `primary_lens`: `minto-pyramid`
- `frame_name`: Answer-First Structurer
- `why`: Commit messages should compress change logic into a short ordered argument with minimal noise.
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
- `artifacts_out`: commit-proposal.v1

## Neutrality Rules
- Infer commit type from the diff, not from wishful framing.
- If type or scope is ambiguous, surface alternatives explicitly.
- Do not invent breaking-change claims without evidence.

## Execution Constraints
- Do not perform git mutations from this skill; message generation only.
- Prefer accurate compression over marketing language or changelog prose.
- If the diff does not support a confident single message, return stable alternatives rather than overcommitting.

## Output Discipline
- `response_profile=commit_proposal`
- User-facing rendering is delegated to `respond`.
