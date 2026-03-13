---
name: workflow-tidy-simplify-this
description: "Workflow skill that reviews recent changes for reuse, quality, and efficiency issues, then applies bounded safe fixes. Use after implementing a feature or bug fix when you want one default cleanup entrypoint instead of manually chaining review and fix skills."
---
# Workflow / Tidy Simplify This

## Purpose
Review recent changes through specialized cleanup lenses, aggregate the findings, apply the smallest safe fixes, and verify the result.

## Default Program
```text
[stages: preflight>detect>analyze>implement>verify>review>audit | scope: diff|repo|paths(glob,...) | policy: evidence,correctness-first,quality-gates{tests,compat,style},deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This workflow uses `hickey-carmack` because post-change cleanup should preserve the contract, keep data flow and side effects explicit, and prefer the smallest justified simplification.

## Use When
- Need a default post-implementation cleanup pass over recent changes.
- Need one workflow that checks reuse, quality, and efficiency before editing code.
- Need a diff-first simplify workflow similar to a "clean up my recent changes" command.

## Do Not Use When
- Need analysis-only mapping with no code edits — use workflow-tidy-find-improvements.
- Need a broad refactor or architecture redesign.
- Need to change behavior or add net-new features.

## Required Inputs
- `TARGET_SCOPE` (diff|recent-files|path-set; optional; allowed: diff|recent-files|path-set): Scope to simplify. Defaults to current git diff, then recent files if no diff exists.
- `FOCUS_HINTS` (list; optional; shape: {AREA, WHY}): Optional concerns such as memory efficiency, utility reuse, or abstraction boundaries.
- `APPLY_POLICY` (fix-high-signal|fix-all-safe; optional; allowed: fix-high-signal|fix-all-safe): How aggressively to apply findings. Defaults to `fix-high-signal`.
- `VERIFY_HINTS` (list; optional; shape: {CHECK, PASS_CONDITION}): Extra checks to run after cleanup when the user has a known done condition.

## Structured Outputs
- `REVIEW_FINDINGS` (list; required; shape: {CATEGORY, ISSUE, LOCATION, RECOMMENDED_FIX}): Aggregated findings from reuse, quality, and efficiency review.
- `FIXED_FINDINGS` (list; required; shape: {CATEGORY, ISSUE, LOCATION, CHANGE, STATUS}): Findings that were fixed in the cleanup pass.
- `SKIPPED_FINDINGS` (list; required; shape: {CATEGORY, ISSUE, LOCATION, REASON}): Findings left alone because they were false positives, out of scope, or too risky.
- `VERIFICATION_STATUS` (pass|blocked|inconclusive; required; allowed: pass|blocked|inconclusive): Final verification verdict after cleanup.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Atomic path executed by the workflow.

## Execution Constraints
1. Determine scope from `git diff`, then recent files only if no diff boundary exists.
2. Review the same scope through reuse, quality, and efficiency lenses.
3. Deduplicate overlapping findings and keep only concrete, locally actionable items.
4. Apply the smallest safe fixes with `FUNCTIONAL_EQUIVALENCE=yes`.
5. Run focused verification and keep read-only review evidence separate from edits.

## Expansion
- `$tidy-review-reuse`
- `$tidy-review-quality`
- `$tidy-review-efficiency`
- `$tidy-apply-review-fixes`
- `$check-final-verify`

## Example Invocation
```text
$workflow-tidy-simplify-this
TARGET_SCOPE: diff
```
