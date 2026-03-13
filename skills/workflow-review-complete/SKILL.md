---
name: workflow-review-complete
description: "Workflow skill that chains structure analysis, quality scan, security review, failure-path review, and a final change verdict into one complete review session. Use when you need the most thorough review coverage in one pass."
---

# Workflow / Review Complete

## Purpose
Compose structure analysis, quality checklist, security review, failure-path review, and final change verdict into one complete, evidence-backed review workflow.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{tests,security},deterministic-output | lens: kahneman-tversky | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kahneman-tversky` because it keeps the work aligned with: Separate observed evidence from inferred risk, expose uncertainty, and resist conclusion-first bias.

## Use When
- Need the most complete review coverage: structure, quality, security, failure paths, and final verdict.
- Need a review workflow where each dimension is explicitly traced.
- Need a final integrate/hold decision backed by multiple review dimensions.

## Do Not Use When
- Need only one specific review dimension — use the individual `review-*` or `analyze-*` skill.
- Need direct code implementation.
- Need release gating rather than code review — use `workflow-release-ready-check` instead.

## Required Inputs
- `TARGET_SCOPE` (path|module|diff|repo; required): Code to review.
- `CHANGE_INTENT` (string; required): Claimed purpose of the change.
- `REVIEW_DEPTH` (full|security-focus|quality-focus; optional): Which dimensions to emphasize. Defaults to `full`.

## Input Contract Notes
- TARGET_SCOPE should be bounded enough that each review dimension can cite concrete files.
- CHANGE_INTENT should describe the actual purpose of the change, not the expected verdict.
- REVIEW_DEPTH narrows emphasis but does not skip safety-critical dimensions.

## Structured Outputs
- `STRUCTURE_FINDINGS` (structure-analysis.v1; required): Current-state structure, coupling, and boundary map.
- `QUALITY_RESULTS` (checklist-results.v1; required): 9-item quality checklist results.
- `SECURITY_FINDINGS` (review-report.v1; required): Security vulnerabilities and verdict.
- `FAILURE_PATH_FINDINGS` (review-report.v1; required): Failure path gaps and recovery coverage.
- `FINAL_VERDICT` (integrate|hold; required): Synthesized integrate/hold decision.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Actual atomic path executed by the workflow.

## Output Contract Notes
- FINAL_VERDICT should synthesize across all review dimensions, not just the last step.
- Each sub-report should remain independently inspectable.
- EXPANDED_ATOMIC_PATH must preserve execution order.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: structure-analysis.v1, review-report.v1

## Neutrality Rules
- Preserve the neutrality rules of each underlying review skill.
- Do not invent defects when underlying scans return no findings.
- Keep workflow output inspectable by preserving the explicit subcheck trail.

## Execution Constraints
- Do not patch code from this workflow — review and analysis only.
- If a required review step cannot run, surface that gap in EXPANDED_ATOMIC_PATH.
- Keep the final verdict tied to the composed evidence, not invented independently.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

최종 결론: **병합 가능** / **보류**

단계별 결과:
- analyze-structure → 주요 구조/결합 이슈
- review-quality → 품질 체크리스트 결과
- review-security → 보안 발견사항
- review-failure-paths → 실패 경로 빈틈
- review-change → 최종 판정 근거

전체 발견사항 (심각도 순):
- 긴급 `file:line` — [무슨 문제]
- 중요 `file:line` — [무슨 문제]

보류라면: "긴급 [N]개 수정 후 재검토 — 목록 볼까요?"
단계 실패 시: "[단계]에서 중단 — [계속하려면 무엇이 필요한지]"

## Mandatory Rules
- Keep findings tied to explicit subcheck evidence.
- Do not synthesize a verdict that contradicts the underlying subcheck results.

## Expansion
- `$analyze-structure`
- `$review-quality`
- `$review-security`
- `$review-failure-paths`
- `$review-change`

## Example Invocation
```text
$workflow-review-complete
SCOPE: src/auth
CHANGE: "Refactor auth middleware to use JWT"
DEPTH: full
```
