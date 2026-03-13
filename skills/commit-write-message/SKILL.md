---
name: commit-write-message
description: "Use when generating Conventional Commit message candidates from an existing diff or change summary. Do not use when implementation, debugging, or review analysis is requested."
---

# Commit / Write Message

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

## Lens Rationale
This skill uses `minto-pyramid` because it keeps the work aligned with: Lead with the answer, group supporting points logically, and make scope and evidence hierarchy explicit.

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
- `why`: Commit messages should compress change logic into a short ordered argument with minimal noise.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: commit-proposal.v1

## Neutrality Rules
- Infer commit type from the diff, not from wishful framing.
- If type or scope is ambiguous, surface alternatives explicitly.
- Do not invent breaking-change claims without evidence.

## Response Format

Show the top candidate first, nothing else before it:

```
[type]([scope]): [concise description]
```

Then list alternatives with rationale:
- [message] — why: [when this framing fits better]

Show BREAKING CHANGE footer only when evidence supports it.

## Execution Constraints
- Do not perform git mutations from this skill; message generation only.
- Prefer accurate compression over marketing language or changelog prose.
- If the diff does not support a confident single message, return stable alternatives rather than overcommitting.
