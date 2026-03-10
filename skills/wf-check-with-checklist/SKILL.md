---
name: wf-check-with-checklist
description: "Workflow skill that combines `wf-check-full-review` with the full 9-item `check-quality-scan` pass. Use when the user explicitly wants both narrow review scans and checklist coverage."
---

# Review Checklist Workflow

## Purpose
Compose narrow review scans and the full quality checklist into one explicit project review workflow.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{tests,security,perf,compat,style},deterministic-output | lens: kahneman-tversky | output: md(contract=v1)]
```

## Use When
- Need both explicit narrow review scans and the full 9-item checklist.
- Need a named workflow instead of repeatedly typing `$wf-check-full-review + $check-quality-scan`.
- Need checklist-backed review output for a bounded project or module scope.

## Do Not Use When
- Need only the narrower `wf-check-full-review` workflow.
- Need only the checklist without narrow review scans.
- Need release-only gating without structural review.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Project, folder, or module to review.
- `REVIEW_FOCUS` (maintainability|risk|mixed; optional; allowed: maintainability|risk|mixed): Optional emphasis for the combined review.

## Input Contract Notes
- Use this workflow only when both narrow review scans and the 9-item checklist are explicitly wanted.
- TARGET_SCOPE should stay bounded enough that checklist rows and review findings can still point to concrete evidence.
- REVIEW_FOCUS changes emphasis but should not suppress checklist categories.

## Structured Outputs
- `REVIEW_FINDINGS` (list; required; shape: {FINDING, SOURCE_CHECK, LOCATION, EVIDENCE, SEVERITY}): Combined evidence-backed review findings.
- `CHECKLIST_TABLE` (list; required; shape: {CHECK_ITEM, STATUS, EVIDENCE, NOTE}): Checklist rows produced by the 9-item quality checklist.
- `INTEGRATE_OR_HOLD` (integrate|hold; required; allowed: integrate|hold): Final review stance.

## Output Contract Notes
- REVIEW_FINDINGS should remain traceable to the underlying narrow review workflow.
- CHECKLIST_TABLE should expose each checklist item explicitly rather than collapsing the 9-item pass into prose.
- INTEGRATE_OR_HOLD should reflect both the narrow review evidence and the checklist outcome.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: review-findings.v2, quality-checklist-report.v1

## Neutrality Rules
- Preserve the neutrality rules of `wf-check-full-review` and `check-quality-scan`.
- Do not invent findings when both underlying workflows return no issue.
- Keep checklist coverage explicit rather than hiding it inside the base review workflow.

## Execution Constraints
- Do not use this workflow as a shortcut for implementation or release rollout judgement.
- If checklist coverage cannot be completed, keep that gap explicit in CHECKLIST_TABLE or accompanying notes.
- Preserve the named combination of narrow review plus checklist instead of hiding one side.

## Mandatory Rules
- Keep the base review workflow narrow and the checklist workflow explicit.
- Expose the combined workflow as a named convenience layer only.

## Expansion
- `$wf-check-full-review`
- `$check-quality-scan`

## Example Invocation
```text
$wf-check-with-checklist
TARGET_SCOPE: src/auth
REVIEW_FOCUS: mixed
```

## Output Discipline
- `response_profile=review_findings`
- User-facing rendering is delegated to `respond`.
