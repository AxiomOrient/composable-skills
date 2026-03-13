---
name: workflow-check-with-checklist
description: "Workflow skill that combines `workflow-review-change` with the full 9-item `review-quality` checklist pass. Use when the user explicitly wants both narrow review scans and checklist coverage."
---

# Workflow / Check + Checklist

## Purpose
Compose narrow review scans and the full quality checklist into one explicit project review workflow.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{tests,security,perf,compat,style},deterministic-output | lens: kahneman-tversky | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kahneman-tversky` because it keeps the work aligned with: Separate observed evidence from inferred risk, expose uncertainty, and resist conclusion-first bias.

## Use When
- Need both explicit narrow review scans and the full 9-item checklist.
- Need a named workflow instead of repeatedly typing `$workflow-review-change + $review-quality`.
- Need checklist-backed review output for a bounded project or module scope.

## Do Not Use When
- Need only the narrower `workflow-review-change` workflow.
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
- Preserve the neutrality rules of `workflow-review-change` and `review-quality`.
- Do not invent findings when both underlying workflows return no issue.
- Keep checklist coverage explicit rather than hiding it inside the base review workflow.

## Execution Constraints
- Do not use this workflow as a shortcut for implementation or release rollout judgement.
- If checklist coverage cannot be completed, keep that gap explicit in CHECKLIST_TABLE or accompanying notes.
- Preserve the named combination of narrow review plus checklist instead of hiding one side.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Lead with verdict: **병합 가능** or **보류**.

Checklist summary (9 items):
| # | Item | pass / risk / unknown | Key evidence |

긴급/중요 findings that block merge:
- 긴급 `file:line` — [issue]
- Risk item #N — [finding] → [required action]

On 보류: "Fix [top finding] first — or want all risk items listed?"
On step failure: name the step and ask what blocked it.

## Mandatory Rules
- Keep the base review workflow narrow and the checklist workflow explicit.
- Expose the combined workflow as a named convenience layer only.

## Expansion
- `$workflow-review-change`
- `$review-quality`

## Example Invocation
```text
$workflow-check-with-checklist
TARGET_SCOPE: src/auth
REVIEW_FOCUS: mixed
```
