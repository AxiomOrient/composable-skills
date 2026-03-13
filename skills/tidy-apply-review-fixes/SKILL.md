---
name: tidy-apply-review-fixes
description: "Implementation skill that takes bounded cleanup findings and applies the smallest safe fixes while preserving current behavior. Designed to consume review outputs such as reuse, quality, and efficiency findings."
---
# Tidy / Apply Review Fixes

## Purpose
Aggregate bounded cleanup findings, apply the smallest safe fixes, and verify that behavior still holds.

## Default Program
```text
[stages: preflight>detect>analyze>implement>verify>review>audit | scope: diff|repo|paths(glob,...) | policy: evidence,correctness-first,quality-gates{tests,compat,style},deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Required Inputs
- `TARGET_SCOPE` (path|module|folder|diff; required): Bounded scope where the fixes may be applied.
- `REVIEW_FINDINGS` (list; required; shape: {SOURCE_SKILL, ISSUE, LOCATION, RECOMMENDED_FIX, EVIDENCE}): Cleanup findings to normalize and fix.
- `FUNCTIONAL_EQUIVALENCE` (yes|preserve-current-behavior; required; allowed: yes|preserve-current-behavior): Explicit contract that behavior must stay the same.
- `APPLY_POLICY` (fix-high-signal|fix-all-safe; optional; allowed: fix-high-signal|fix-all-safe): How aggressively to apply the findings.

## Structured Outputs
- `FIXED_FINDINGS` (list; required; shape: {SOURCE_SKILL, ISSUE, LOCATION, CHANGE, STATUS}): Findings that were actually fixed and the change made.
- `SKIPPED_FINDINGS` (list; required; shape: {SOURCE_SKILL, ISSUE, LOCATION, REASON}): Findings intentionally skipped because they were false positives, too risky, or out of scope.
- `CHANGED_ARTIFACTS` (list; required; shape: {PATH, WHY}): Files changed during the cleanup pass.
- `VERIFICATION_RESULTS` (list; required; shape: {CHECK, RESULT, COMMAND_OR_TEST, EVIDENCE}): Checks run after edits.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

수정한 항목:
- [항목] — `file:line` — [어떻게 수정했는지]

건너뛴 항목:
- [항목] — [이유]

검증 결과: [명령어] — result: PASS / FAIL

미확인 항목이 있으면 가장 빠른 다음 확인 방법과 함께 나열.
