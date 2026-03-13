---
name: workflow-tidy-simplify-this
description: "Workflow skill that reviews recent changes for reuse, quality, and efficiency issues, then applies bounded safe fixes. Use after implementing a feature or bug fix when you want one default cleanup entrypoint instead of manually chaining review and fix skills."
---
# Workflow / Tidy Simplify This

## Purpose
Review recent changes through specialized cleanup lenses, aggregate the findings, apply the smallest safe fixes, and verify the result.

## Default Program
```text
[stages: preflight>detect>analyze>implement>verify>review>audit | scope: diff|recent-files|paths(glob,...) | policy: evidence,correctness-first,quality-gates{tests,compat,style},deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This workflow uses `hickey-carmack` because post-change cleanup should preserve the contract, keep data flow and side effects explicit, and prefer the smallest justified simplification.

## Use When
- Need a default post-implementation cleanup pass over recent changes.
- Need one workflow that checks reuse, quality, and efficiency before editing code.
- Need a diff-first simplify workflow similar to a “clean up my recent changes” command.

## Do Not Use When
- Need analysis-only mapping with no code edits — use workflow-tidy-find-improvements.
- Need a broad refactor or architecture redesign.
- Need to change behavior or add net-new features.

## Required Inputs
- `TARGET_SCOPE` (diff|recent-files|path-set; optional; allowed: diff|recent-files|path-set): Scope to simplify. Defaults to current git diff, then recent files if no diff exists.
- `FOCUS_HINTS` (list; optional; shape: {AREA, WHY}): Optional concerns such as memory efficiency, utility reuse, or abstraction boundaries.
- `APPLY_POLICY` (fix-high-signal|fix-all-safe; optional; allowed: fix-high-signal|fix-all-safe): How aggressively to apply findings. Defaults to `fix-high-signal`.
- `VERIFY_HINTS` (list; optional; shape: {CHECK, PASS_CONDITION}): Extra checks to run after cleanup when the user has a known done condition.

## Input Contract Notes
- Prefer `diff` whenever git changes exist because the cleanup contract is “what just changed.”
- Use `recent-files` only when no usable diff boundary exists.
- `FOCUS_HINTS` narrow prioritization; they do not replace the three default review axes.

## Structured Outputs
- `REVIEW_FINDINGS` (list; required; shape: {CATEGORY, ISSUE, LOCATION, RECOMMENDED_FIX}): Aggregated findings from reuse, quality, and efficiency review.
- `FIXED_FINDINGS` (list; required; shape: {CATEGORY, ISSUE, LOCATION, CHANGE, STATUS}): Findings that were fixed in the cleanup pass.
- `SKIPPED_FINDINGS` (list; required; shape: {CATEGORY, ISSUE, LOCATION, REASON}): Findings left alone because they were false positives, out of scope, or too risky.
- `VERIFICATION_STATUS` (pass|blocked|inconclusive; required; allowed: pass|blocked|inconclusive): Final verification verdict after cleanup.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Atomic path executed by the workflow.

## Output Contract Notes
- The aggregated review list should deduplicate overlapping findings from multiple review skills.
- If all three review passes are clean, return an empty `FIXED_FINDINGS` list and `VERIFICATION_STATUS=pass` only after confirming no code edits were needed.
- `EXPANDED_ATOMIC_PATH` must preserve the actual execution order; the first three review skills may run in parallel when the runtime supports it.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: review-report.v1, implementation-delta.v1, self-verify-report.v1

## Neutrality Rules
- Keep the workflow bounded to the reviewed scope.
- Skip findings that are false positives or that require a larger refactor than the cleanup contract allows.
- Do not turn this into a feature pass or architecture rewrite.

## Execution Constraints
1. Determine the scope. Use `git diff` or `git diff HEAD` when staged changes exist. If there is no meaningful diff, use the most recently changed or explicitly mentioned files.
2. Launch the three review atomics on the same scope. When the runtime supports parallel agents, run `tidy-review-reuse`, `tidy-review-quality`, and `tidy-review-efficiency` in parallel.
3. Aggregate and deduplicate the findings. Keep only concrete, locally actionable items.
4. Invoke `tidy-apply-review-fixes` with the bounded findings and `FUNCTIONAL_EQUIVALENCE=yes`.
5. Invoke `check-final-verify` over the changed artifacts with explicit contracts: current behavior preserved, cleanup findings resolved or justified, and focused checks passed.
6. If the best action is “do nothing,” say so plainly and stop.

## Response Format
Lead with one of:
- `CLEAN` — no worthwhile cleanup found
- `FIXED` — fixes applied and verified
- `BLOCKED` / `INCONCLUSIVE` — verification did not fully pass

Then show:
- Review findings by category
- What was fixed vs skipped
- Verification evidence

## Mandatory Rules
- Expose the expanded atomic path explicitly.
- Preserve current behavior.
- Keep review, fix, and verification evidence separate.

## Expansion
- `$tidy-review-reuse`
- `$tidy-review-quality`
- `$tidy-review-efficiency`
- `$tidy-apply-review-fixes`
- `$check-final-verify`

## Example Invocation
```text
$workflow-tidy-simplify-this TARGET_SCOPE: diff FOCUS_HINTS:
- AREA: memory efficiency
  WHY: a new cache-like branch was added
```
