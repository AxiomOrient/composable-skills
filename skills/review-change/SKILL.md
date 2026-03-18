---
name: review-change
description: "Review changed code with prioritized findings, testing gaps, and an integrate or hold verdict. Use when you need a findings-first merge judgement rather than implementation work."
---

# Review / Change

## Purpose
Issue a findings-first review verdict with concrete evidence.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,quality-gates{tests,security,compat,style},deterministic-output |
 lens: kahneman-tversky |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kahneman-tversky` because it keeps the work aligned with: Separate observed evidence from inferred risk, expose uncertainty, and resist conclusion-first bias.

## Use When
- Need a final findings-first review verdict.
- Need prioritized review findings with file and line evidence.
- Need integrate or hold judgement after reviewing changed code.

## Do Not Use When
- Need direct code implementation.
- Need only the 9-item checklist without verdict synthesis.
- Need a narrow single-concern scan instead of a broad review verdict.

## Required Inputs
- `REVIEW_GOAL` (general-verdict|regression-risk|change-intent-check|narrow-focus; required): Type of review verdict needed.
- `TARGET_SCOPE` (diff|file|module|folder|repo; required): Scope to review.
- `CHANGE_INTENT` (string; required): Claimed purpose of the change.
- `KNOWN_TEST_SIGNAL` (list; optional; shape: {SIGNAL, STATUS, SOURCE}): Executed tests, missing tests, or known verification state.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Security-only, perf-only, compat-only, or other focus constraints.

## Input Contract Notes
- CHANGE_INTENT should summarize the claimed purpose of the change, not the reviewer verdict.
- KNOWN_TEST_SIGNAL should distinguish executed evidence from missing or assumed coverage.
- Use REVIEW_GOAL=`narrow-focus` only when constraints clearly bound the inspection surface.

## Structured Outputs
- `FINDINGS` (list; required; shape: {SEVERITY, SUMMARY, LOCATION, EVIDENCE, CONFIDENCE}): Concrete findings with severity, confidence, and evidence.
- `TESTING_GAPS` (list; required; shape: {GAP, IMPACT, CHEAPEST_CHECK}): Testing gaps plus cheapest verification steps.
- `VERDICT` (integrate|hold; required; allowed: integrate|hold): Integrate or hold verdict with rationale.

## Output Contract Notes
- Each FINDINGS row should cite concrete evidence and keep severity separate from confidence.
- Use TESTING_GAPS for missing verification coverage even when no code defect is proven.
- VERDICT should summarize the practical merge stance after findings and testing gaps are considered.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `why`: Review verdicts should separate observed defects from inferred impact and mark uncertainty explicitly.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: review-report.v1

## Neutrality Rules
- Do not assume a finding exists; return no findings when evidence does not support one.
- Separate observed behavior from inferred impact.
- Do not convert maintainability preference into a blocker unless a concrete regression or risk exists.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

결론부터: **병합 가능** / **보류**

발견사항은 심각도 순서:
- 긴급 / 중요 / 참고 — `file:line` — [문제] (confidence: high/medium/low)

테스트 빈틈은 따로:
- [빈틈] — 가장 빠른 확인 방법: [command or test]

끝에: "긴급부터 고칠까요, 아니면 전체 목록을 먼저 볼까요?"

## Execution Constraints
- Review is read-and-judge only; do not patch code or rewrite planning artifacts here.
- If evidence is insufficient to support a finding, downgrade it to a testing gap or inconclusive note instead of overstating impact.
- Keep the verdict tied to the supplied scope and change intent rather than repo-wide preference debates.

## Example Invocation
```text
$review-change
REVIEW_GOAL: general-verdict
TARGET_SCOPE: diff
CHANGE_INTENT: replace payment provider A with B
KNOWN_TEST_SIGNAL:
  - {SIGNAL: unit tests, STATUS: pass, SOURCE: local}
```
