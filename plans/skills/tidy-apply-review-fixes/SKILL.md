---
name: tidy-apply-review-fixes
description: "Implementation skill that takes bounded cleanup findings and applies the smallest safe fixes while preserving current behavior. Designed to consume review outputs such as reuse, quality, and efficiency findings. Do not use for net-new feature work or broad refactors."
---
# Tidy / Apply Review Fixes

## Purpose
Aggregate bounded cleanup findings, apply the smallest safe fixes, and verify that behavior still holds.

## Default Program
```text
[stages: preflight>detect>analyze>implement>verify>review>audit | scope: diff|recent-files|paths(glob,...) | policy: evidence,correctness-first,quality-gates{tests,compat,style},deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because cleanup fixes should preserve the contract while removing accidental complexity and wasted work with the smallest explicit change.

## Use When
- Need to turn bounded review findings into actual code changes.
- Need a post-review cleanup pass that preserves current behavior.
- Need one implementation step that deduplicates overlapping cleanup findings before editing code.

## Do Not Use When
- Need net-new feature work.
- Need broad architectural refactor planning.
- Need to edit code without concrete upstream findings.

## Required Inputs
- `TARGET_SCOPE` (path|module|folder|diff; required): Bounded scope where the fixes may be applied.
- `REVIEW_FINDINGS` (list; required; shape: {SOURCE_SKILL, ISSUE, LOCATION, RECOMMENDED_FIX, EVIDENCE}): Cleanup findings to normalize and fix.
- `FUNCTIONAL_EQUIVALENCE` (yes|preserve-current-behavior; required; allowed: yes|preserve-current-behavior): Explicit contract that behavior must stay the same.
- `APPLY_POLICY` (fix-high-signal|fix-all-safe; optional; allowed: fix-high-signal|fix-all-safe): How aggressively to apply the findings.

## Input Contract Notes
- `REVIEW_FINDINGS` should already be bounded and actionable; this skill is not responsible for inventing new review categories.
- `TARGET_SCOPE` must be small enough that focused verification can still prove behavior holds.
- Use `fix-high-signal` when the diff is risky or the review findings include larger refactor ideas.

## Structured Outputs
- `FIXED_FINDINGS` (list; required; shape: {SOURCE_SKILL, ISSUE, LOCATION, CHANGE, STATUS}): Findings that were actually fixed and the change made.
- `SKIPPED_FINDINGS` (list; required; shape: {SOURCE_SKILL, ISSUE, LOCATION, REASON}): Findings intentionally skipped because they were false positives, too risky, or out of scope.
- `CHANGED_ARTIFACTS` (list; required; shape: {PATH, WHY}): Files changed during the cleanup pass.
- `VERIFICATION_RESULTS` (list; required; shape: {CHECK, RESULT, COMMAND_OR_TEST, EVIDENCE}): Checks run after edits.

## Output Contract Notes
- Every `FIXED_FINDINGS` row must map to at least one `CHANGED_ARTIFACTS` row.
- Every changed file must be covered by at least one verification result or an explicit verification-gap note inside `SKIPPED_FINDINGS`.
- A finding may be skipped without argument when it is a false positive or exceeds the bounded scope.

## Artifacts
- `artifacts_in`: review-report.v1
- `artifacts_out`: implementation-delta.v1

## Neutrality Rules
- Prefer the smallest explicit fix that resolves the finding.
- Do not expand the cleanup pass into unrelated refactoring.
- Skip speculative or boundary-breaking findings instead of forcing them in.

## Execution Constraints
- Edit only inside TARGET_SCOPE.
- Deduplicate overlapping findings before changing code.
- Preserve current behavior and rerun the narrowest relevant checks after each cluster of changes.
- If a finding requires a broader refactor than the scope can verify, skip it and record why.

## Response Format
Lead with what was fixed and what was skipped.

Fixed:
- [source] [issue] — `file:line` — changed: [what]

Skipped:
- [source] [issue] — `file:line` — reason: [why skipped]

Verification:
- [command or test] — PASS / FAIL — [key signal]

## Mandatory Rules
- Preserve behavior.
- Keep the cleanup bounded.
- Do not claim success without verification evidence.

## Example Invocation
```text
$tidy-apply-review-fixes TARGET_SCOPE: diff FUNCTIONAL_EQUIVALENCE: yes APPLY_POLICY: fix-high-signal REVIEW_FINDINGS:
- SOURCE_SKILL: tidy-review-reuse
  ISSUE: duplicated path normalization
  LOCATION: src/router/path.ts:44
  RECOMMENDED_FIX: replace inline normalization with normalizePath()
  EVIDENCE: src/shared/path.ts:12 already provides normalizePath
```
