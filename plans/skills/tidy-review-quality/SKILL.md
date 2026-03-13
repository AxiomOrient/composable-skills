---
name: tidy-review-quality
description: "Read-only review skill that inspects a bounded change scope for code-quality cleanup opportunities: redundant state, parameter sprawl, near-duplicate branches, leaky abstractions, and stringly-typed logic. Do not use for direct code edits or broad product planning."
---
# Tidy / Review Quality

## Purpose
Review a bounded scope for structural code-quality issues that should be cleaned up after the main implementation is complete.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: diff|recent-files|paths(glob,...) | policy: evidence,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because code quality judgments should reward explicit data flow, sharp invariants, and the smallest clear mechanism.

## Use When
- Need a focused post-change review for structural quality issues.
- Need to catch hacky cleanup debt before merging or shipping.
- Need one specialized review pass whose output can feed a later fix step.

## Do Not Use When
- Need direct file edits.
- Need risk scoring for release or security judgement.
- Need speculative architecture advice outside the reviewed scope.

## Required Inputs
- `REVIEW_SCOPE` (diff|recent-files|path-set; required; allowed: diff|recent-files|path-set): How to choose the files to review.
- `TARGET_SCOPE` (path|module|folder|repo; optional): Explicit path boundary when REVIEW_SCOPE is `path-set`, or a narrowing filter over a diff.
- `FOCUS_HINTS` (list; optional; shape: {AREA, WHY}): Optional quality concerns to prioritize.

## Input Contract Notes
- A quality finding must name the concrete smell and the local code that shows it.
- Prefer observable structural problems over taste-based style comments.
- When the same underlying issue appears several times, group it into one finding with multiple locations.

## Structured Outputs
- `QUALITY_FINDINGS` (list; required; shape: {ISSUE, LOCATION, SIGNAL, WHY_IT_HURTS, RECOMMENDED_FIX}): Actionable structural quality findings.
- `QUALITY_HOLDS` (list; required; shape: {LOCATION, WHY_OK}): Areas reviewed and intentionally left alone because the structure carries a real invariant or boundary.
- `REVIEW_STATUS` (clean|findings|inconclusive; required; allowed: clean|findings|inconclusive): Whether the scope is clean, has findings, or lacks enough evidence.

## Output Contract Notes
- Use `QUALITY_HOLDS` to explain false positives that should not be “cleaned up.”
- Return `clean` only when no structural quality issue is justified by the observed code.
- Return `inconclusive` when the relevant boundary cannot be inspected confidently.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: review-report.v1

## Neutrality Rules
- Focus on structure that increases cognitive load or weakens invariants.
- Do not report pure formatting or naming preferences as findings unless they break a real contract.
- Do not push new abstractions unless they remove a proven local smell.

## Execution Constraints
- This skill is read-and-review only; do not edit files.
- Review at least these classes of issues when present: redundant state, parameter sprawl, copy-paste with slight variation, leaky abstractions, and stringly-typed logic.
- Tie every recommendation back to the local code path, not generic best practice prose.

## Response Format
Lead with `CLEAN`, `FINDINGS`, or `INCONCLUSIVE`.

For each finding:
- [issue] — `file:line` — why it hurts: [reason] — fix: [smallest useful change]

For each hold:
- left alone: `file:line` — [why the structure is justified]

## Mandatory Rules
- Keep this skill read-only.
- Separate real findings from justified structure.
- Do not turn taste into defect claims.

## Example Invocation
```text
$tidy-review-quality REVIEW_SCOPE: diff FOCUS_HINTS:
- AREA: abstraction boundaries
  WHY: a new service layer was added in this diff
```
