---
name: pr-draft-summary
description: "Generate a review-ready branch suggestion, PR title, and concise draft description after substantive work is complete. Use when code, tests, build config, or behavior-relevant docs changed and you need a tight summary block for handoff or review."
---
# PR Draft Summary

## Purpose
Turn a real repository diff into a review-ready summary block that a human can paste into a PR without rewriting the change story from scratch.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: diff|branch|repo |
 policy: evidence,review-ready,deterministic-output |
 lens: minto-pyramid |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `minto-pyramid` because it keeps the work aligned with: lead with the core change, then support it with the minimum structure reviewers need.

## Use When
- Substantive work is done and ready for review or handoff.
- Need a branch suggestion, title, and concise PR description derived from the actual diff.
- Need risk and rollback notes without bloated prose.

## Do Not Use When
- No meaningful code or behavior-relevant diff exists.
- Need release notes rather than a review-ready PR block.
- Need a final merge verdict instead of a summary artifact.

## Required Inputs
- `REVIEW_SCOPE` (diff|branch|repo; required): What body of changes to summarize.
- `CHANGE_INTENT` (string; required): What the change set was trying to accomplish.
- `BASE_REF_HINT` (git-ref|none; optional): Expected comparison base when not using the default upstream.
- `NOTES_POLICY` (minimal|include-risk-and-rollback; optional): How much operational context to include.

## Input Contract Notes
- `REVIEW_SCOPE` should point to the actual change boundary, not the desired PR outcome.
- `CHANGE_INTENT` should reflect the main outcome, not every file touched.
- `BASE_REF_HINT` is a hint only; prefer the real upstream or merge base when available.

## Structured Outputs
- `CHANGE_SUMMARY` (list; required; shape: {POINT, EVIDENCE}): The smallest set of points that explains the diff.
- `PR_TITLE` (string; required): Concise review-ready title.
- `PR_DESCRIPTION` (string; required): Tight draft description starting from the core outcome.
- `RISK_AND_ROLLBACK` (list; required; shape: {RISK, IMPACT, ROLLBACK_POINT}): Material operational notes when relevant.

## Output Contract Notes
- `CHANGE_SUMMARY` should be derived from the real diff, not from intent alone.
- `PR_TITLE` should fit the primary change, not a laundry list.
- `PR_DESCRIPTION` should stay paste-ready and avoid repeated detail.
- `RISK_AND_ROLLBACK` should be omitted only when there is truly nothing material to say.

## Primary Lens
- `primary_lens`: `minto-pyramid`
- `why`: PR summaries should lead with the answer and keep supporting detail minimal.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: pr-draft-summary.v1

## Response Format
Think and operate in English, but deliver the final response in Korean.
Output a concise Markdown block:

```md
# Pull Request Draft
## Branch name suggestion
git checkout -b [name]

## Title
[title]

## Description
[short description]
```

When material, append:
- Risks: one line each.
- Rollback: one line each.

If no substantive changes are detected, say so directly and do not emit a fake PR block.

## Neutrality Rules
- Do not inflate the summary to sound more important than the diff warrants.
- Do not list every touched file when a smaller change story explains the work.
- Do not omit material risk just to keep the summary polished.

## Execution Constraints
- Prefer the actual diff, status, and merge-base context over memory.
- Keep the title and description tight enough for a human reviewer to scan quickly.
- Surface untracked but relevant work when it materially changes the review story.

## References
- `references/pr-draft-template.md`
- `references/change-bucketing.md`

## Example Invocation
```text
$pr-draft-summary REVIEW_SCOPE: branch CHANGE_INTENT: simplify session restore and add regression protection NOTES_POLICY: include-risk-and-rollback
```
