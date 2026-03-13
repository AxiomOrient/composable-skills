---
name: tidy-review-reuse
description: "Read-only review skill that inspects a bounded change scope for missed reuse opportunities. Find newly written logic that should call existing helpers, utilities, shared modules, or adjacent abstractions instead. Do not use for direct code edits or broad architecture planning."
---
# Tidy / Review Reuse

## Purpose
Review a bounded scope for new logic that should reuse existing code instead of reimplementing it.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: diff|recent-files|paths(glob,...) | policy: evidence,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because reuse judgements should start from explicit data flow and real invariants, not decorative abstraction.

## Use When
- Need to review a recent diff or bounded file set for duplicated logic.
- Need to search the codebase for existing helpers that could replace new hand-rolled code.
- Need one specialized review pass before deciding what cleanup to implement.

## Do Not Use When
- Need direct code changes.
- Need broad architecture or module-boundary refactor planning.
- Need to speculate about reusable abstractions that do not already exist.

## Required Inputs
- `REVIEW_SCOPE` (diff|recent-files|path-set; required; allowed: diff|recent-files|path-set): How to choose the files to review.
- `TARGET_SCOPE` (path|module|folder|repo; optional): Explicit path boundary when REVIEW_SCOPE is `path-set`, or a narrowing filter over a diff.
- `FOCUS_HINTS` (list; optional; shape: {AREA, WHY}): Optional focus areas such as parsing helpers, type guards, or path handling.

## Input Contract Notes
- Use `diff` first when git changes exist. Use `recent-files` only when there is no useful diff boundary.
- A valid reuse finding must point to a concrete existing asset, not a hypothetical helper that should be created later.
- If the scope is large, limit the review to the files actually changed or the smallest explicit folder boundary.

## Structured Outputs
- `REUSE_FINDINGS` (list; required; shape: {ISSUE, LOCATION, EXISTING_ASSET, WHY_REUSE, RECOMMENDED_CHANGE}): Actionable reuse findings tied to a concrete existing asset.
- `SEARCH_EVIDENCE` (list; required; shape: {PATTERN, MATCH, WHY_RELEVANT}): Searches or codebase matches that justify each finding.
- `REVIEW_STATUS` (clean|findings|inconclusive; required; allowed: clean|findings|inconclusive): Whether the scope is clean, has findings, or lacks enough evidence.

## Output Contract Notes
- Return `clean` when no concrete existing asset beats the new code.
- Return `inconclusive` when the scope cannot be inspected confidently or the codebase search is incomplete.
- Every `REUSE_FINDINGS` row must cite the existing asset that should be reused.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: review-report.v1

## Neutrality Rules
- Do not invent a reuse finding without a concrete existing implementation.
- Prefer local or adjacent utilities over larger shared abstractions when both satisfy the same contract.
- Leave intentionally local code alone when reuse would increase coupling or hide a real invariant.

## Execution Constraints
- This skill is read-and-review only; do not edit files.
- Search common utility directories, shared modules, and files adjacent to the changed code.
- Flag inline logic only when the existing asset is truly equivalent or can be used with a small safe adaptation.

## Response Format
Lead with `CLEAN`, `FINDINGS`, or `INCONCLUSIVE`.

For each finding:
- [issue] — `file:line` → reuse `[existing asset]` — why: [why the existing code is better]

If clean:
- "No concrete reuse win found in the reviewed scope."

## Mandatory Rules
- Point to a concrete existing asset for every finding.
- Keep this skill read-only.
- Separate proven reuse wins from speculative refactor ideas.

## Example Invocation
```text
$tidy-review-reuse REVIEW_SCOPE: diff FOCUS_HINTS:
- AREA: type guards
  WHY: several new inline checks were added
```
