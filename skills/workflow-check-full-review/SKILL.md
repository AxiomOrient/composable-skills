---
name: workflow-check-full-review
description: "Workflow skill that composes current-state structure mapping and bounded review scans for a project, folder, or module. Use when the user wants a review built from explicit subchecks instead of a single broad 'find bugs' instruction."
---

# Workflow / Check Full Review

## Purpose
Compose specific analysis and review scans into one explicit project review workflow.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{tests,security},deterministic-output | lens: kahneman-tversky | output: md(contract=v1)]
```

## Use When
- Need a project, folder, or module reviewed through explicit subchecks.
- Need review output grounded in current-state structure, duplication, boundary, error-path, and test-gap evidence.
- Need a named workflow that can still be extended with additional skills.

## Do Not Use When
- Need direct code implementation without review.
- Need a narrow single-concern scan rather than a combined review workflow.
- Need release-only gating without structural review.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Project, folder, or module to review.
- `REVIEW_FOCUS` (maintainability|risk|mixed; optional; allowed: maintainability|risk|mixed): Optional emphasis for the combined review.

## Input Contract Notes
- TARGET_SCOPE should stay bounded enough that the subchecks can cite concrete files or folders.
- REVIEW_FOCUS narrows emphasis only; it should not remove mandatory evidence from the underlying review workflow.
- Use this workflow when the user wants explicit composed subchecks, not a hidden all-purpose review.

## Structured Outputs
- `REVIEW_FINDINGS` (list; required; shape: {FINDING, SOURCE_CHECK, LOCATION, EVIDENCE, SEVERITY}): Combined evidence-backed review findings.
- `CHECK_REPORTS` (list; required; shape: {CHECK, SUMMARY, OUTPUT_REF}): Underlying scan reports that support the review.
- `INTEGRATE_OR_HOLD` (integrate|hold; required; allowed: integrate|hold): Final review stance.

## Output Contract Notes
- REVIEW_FINDINGS should stay traceable to one or more CHECK_REPORTS rows.
- CHECK_REPORTS should expose the underlying subcheck identity rather than hiding it behind summary prose.
- INTEGRATE_OR_HOLD should reflect the composed evidence, not a new independent verdict logic.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: review-findings.v2

## Neutrality Rules
- Preserve the neutrality rules of each underlying scan skill.
- Do not invent defects when underlying scans return no findings.
- Expose the combined review as the sum of explicit subchecks.

## Execution Constraints
- Do not patch code from this workflow; it is analysis and review composition only.
- If a required subcheck cannot run, surface that gap in CHECK_REPORTS rather than pretending full coverage.
- Keep workflow output inspectable by preserving the explicit subcheck trail.

## Mandatory Rules
- Keep findings tied to explicit subcheck evidence.
- Use the workflow only as a transparent composition, not a hidden mega-review.

## Expansion
- `$scout-structure-map`
- `$tidy-find-magic-numbers`
- `$tidy-find-copies`
- `$check-module-bounds`
- `$check-failure-paths`
- `$test-find-gaps`
- `$check-merge-ready`

## Example Invocation
```text
$workflow-check-full-review
TARGET_SCOPE: src/auth
REVIEW_FOCUS: maintainability
```
