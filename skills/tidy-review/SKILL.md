---
name: tidy-review
description: "Read-only cleanup review skill. Inspect a bounded scope for missed reuse opportunities, code-quality issues, and efficiency problems. Produces structured findings that feed into tidy-apply-review-fixes. Use before applying cleanup edits."
---

# Tidy / Review

## Purpose
Inspect a bounded scope through up to three cleanup lenses — reuse, quality, and efficiency — and produce structured findings without touching any code.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: diff|repo|paths(glob,...) | policy: evidence,correctness-first,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because cleanup review should keep data flow and side effects explicit, distinguish essential from accidental complexity, and prefer the smallest justified finding.

## Use When
- Need read-only inspection for reuse, quality, or efficiency opportunities before editing code.
- Need structured findings to feed into `tidy-apply-review-fixes`.
- Composing `workflow-tidy-simplify-this` and need the review phase before the apply phase.

## Do Not Use When
- Need to apply the fixes — use `tidy-apply-review-fixes` after this skill.
- Need deep complexity inventory — use `tidy-analyze` instead.
- Need duplication analysis only — use `tidy-find-copies` instead.

## Required Inputs
- `TARGET_SCOPE` (path|module|folder|diff; required): Bounded scope to inspect.
- `FOCUS` (reuse|quality|efficiency|all; optional; allowed: reuse|quality|efficiency|all): Which cleanup lens to apply. Defaults to `all`.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF}): Existing test results, benchmarks, or prior review notes.

## Input Contract Notes
- FOCUS=reuse: finds newly written logic that should call existing helpers/utilities.
- FOCUS=quality: finds redundant state, parameter sprawl, leaky abstractions, unclear naming.
- FOCUS=efficiency: finds unnecessary work, missed concurrency, hot-path bloat, memory waste.
- FOCUS=all: runs all three lenses and deduplicates overlapping findings.

## Structured Outputs
- `REVIEW_FINDINGS` (list; required; shape: {LENS, ISSUE, LOCATION, RECOMMENDED_FIX, EVIDENCE}): Structured findings per lens. May be empty when scope is clean.
- `SKIPPED_AREAS` (list; required; shape: {AREA, WHY_SKIPPED}): Areas not inspected due to scope boundaries or missing evidence.
- `REVIEW_SUMMARY` (string; required): One-line characterization of the finding set — not a verdict.

## Output Contract Notes
- REVIEW_FINDINGS may be empty when the scope is already clean.
- Do not manufacture findings to justify the review pass.
- Keep findings concrete and locally actionable — no architectural redesign suggestions.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: cleanup-review-findings.v1

## Neutrality Rules
- This skill only reads. No code changes.
- Do not issue an integrate/hold verdict — findings only.
- Do not inflate style preference into a blocking finding.

## Execution Constraints
- Inspect only the declared scope.
- Deduplicate findings that appear across multiple lenses.
- Return empty REVIEW_FINDINGS when no concrete issues are found.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

발견사항 목록 (렌즈별):
- [렌즈: 재사용/품질/효율] — 위치: `파일:줄` — 문제: [무엇이 문제] — 제안: [구체적 수정 방법]

발견사항이 없으면: "이 범위는 깨끗합니다."

마지막에 한 줄 요약: 발견사항 수, 주요 영역.

## Mandatory Rules
- Return empty findings when scope is clean.
- No code edits in this skill.

## Example Invocation
```text
$tidy-review
TARGET_SCOPE: diff
FOCUS: all
```
