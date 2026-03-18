---
name: review-quality
description: "Checklist-only quality review for changed code. Verify the fixed 9-item quality table and surface pass, risk, or unknown rows with evidence."
---

# Review / Quality

## Purpose
Check code quality against a fixed checklist without replacing verdict review.

## Fixed Checklist
The following 9 items are always evaluated. CHECKLIST_TABLE must contain exactly these rows:

| # | Item | What to Check |
|---|------|---------------|
| 1 | Correctness | Does the code behave correctly without obvious logic errors? |
| 2 | Clarity | Is the code readable enough for the next maintainer? |
| 3 | Simplicity | Does it solve the problem without unnecessary layers or indirection? |
| 4 | Boundary Respect | Are module and interface boundaries kept intact? |
| 5 | Error Handling | Are failure cases handled clearly and safely? |
| 6 | Security | Are secrets, auth, input trust, and exposure risks handled safely? |
| 7 | Testability | Can the critical behavior be verified and is coverage obviously missing? |
| 8 | Performance | Are there unnecessary allocations, repeated work, or hot-path problems? |
| 9 | Goal Fit | Does the change actually match the stated goal without scope drift? |

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,quality-gates{tests,security,perf,compat,style},deterministic-output |
 lens: kahneman-tversky |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kahneman-tversky` because it keeps the work aligned with: Separate observed evidence from inferred risk, expose uncertainty, and resist conclusion-first bias.

## Use When
- Need the mandatory 9-item checklist evaluated.
- Need explicit pass, risk, or unknown output across fixed quality dimensions.
- Need checklist evidence before a final review or audit.

## Do Not Use When
- Need direct code implementation.
- Need a single narrow scan instead of the full checklist.
- Need final integrate or hold verdict only.

## Required Inputs
- `SCOPE` (diff|file|module|folder|repo; required): Scope to inspect.
- `GOAL` (string; required): Intended behavior or maintenance goal.
- `FOCUS_ITEMS` (list; optional; shape: {ITEM}): Optional checklist item numbers to emphasize. The full table still stays required.
- `EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Tests, benchmarks, issue context, or supporting evidence.

## Input Contract Notes
- GOAL should describe the intended behavior or maintenance result, not the checklist verdict you want.
- FOCUS_ITEMS narrows emphasis only; it does not remove the obligation to report the full fixed checklist.
- EVIDENCE should cite existing tests, benchmarks, or artifacts rather than conclusions.

## Structured Outputs
- `CHECKLIST_TABLE` (list; required; shape: {ITEM, STATUS, EVIDENCE, ACTION}): Checklist rows with item, status, evidence, and action.
- `FINDINGS_SUMMARY` (list; required; shape: {ISSUE, ITEM, EVIDENCE, IMPACT}): Material risks surfaced by the checklist.
- `UNKNOWN_ITEMS` (list; required; shape: {ITEM, CHEAPEST_CHECK}): Unknown items plus cheapest verification steps.
- `CHECKLIST_STATUS` (pass|risk|unknown; required; allowed: pass|risk|unknown): Overall checklist state.

## Output Contract Notes
- CHECKLIST_TABLE should cover the fixed checklist even when FOCUS_ITEMS narrows emphasis for deeper commentary.
- Use FINDINGS_SUMMARY only for material risks supported by evidence; do not restate every checklist row there.
- Use UNKNOWN_ITEMS when evidence is missing instead of forcing a pass or risk label.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `why`: Checklist review should resist conclusion-first bias and keep risk claims evidence-backed.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: quality-checklist-report.v1

## Neutrality Rules
- Use pass, risk, or unknown only; do not force a negative finding.
- If evidence is insufficient for a checklist item, mark it unknown with the cheapest verification step.
- Do not elevate style preference above behavior, safety, or performance evidence.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

9개 항목 표:
- # | Item | pass / risk / unknown | 핵심 근거

중요 위험만 아래에 한 줄씩:
- 항목 번호 → 발견사항 → 영향

모르는 항목은 가장 빠른 확인 방법과 함께 따로 적기.

끝에: 병합 전 꼭 처리할 risk 항목만 짧게.

## Execution Constraints
- Do not collapse the checklist into a generic review verdict from this skill.
- Keep each item scoped to observable evidence rather than taste-only commentary.
- If multiple items point to the same issue, record the issue once in FINDINGS_SUMMARY and keep row-by-row detail in CHECKLIST_TABLE.

## Example Invocation
```text
$review-quality
SCOPE: src/payment
GOAL: payment flow refactor
FOCUS_ITEMS:
  - {ITEM: 5}
  - {ITEM: 8}
```
