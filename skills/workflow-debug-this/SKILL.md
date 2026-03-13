---
name: workflow-debug-this
description: "Workflow skill that captures the repro, narrows the failure surface, performs root-cause debugging, and checks regression protection. Use when the user wants one default debug entrypoint instead of a broad 'fix the bug' instruction."
---

# Workflow / Debug This

## Purpose
Compose repro capture, failure-surface reduction, debugging, and test-gap awareness into one explicit debug workflow.

## Default Program
```text
[stages: preflight>detect>analyze>implement>verify>review>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{tests},deterministic-output | lens: feynman | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `feynman` because it keeps the work aligned with: Reproduce first, use disprovable hypotheses, and explain the result plainly.

## Use When
- Need a bounded debug loop for a concrete failure.
- Need to capture the repro and reduce failure surface before root-cause work.
- Need debug output tied to follow-up regression protection.

## Do Not Use When
- Need a first-pass implementation with no concrete failure.
- Need only a failure-surface map without deeper debugging.
- Need a broad project review instead of a debug loop.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Scope where the failure occurs.
- `FAILURE_SYMPTOM` (string; required): Observed failure symptom.
- `EXPECTED_BEHAVIOR` (string; required): Expected behavior.

## Input Contract Notes
- FAILURE_SYMPTOM should describe the observable failure, not a guessed root cause.
- EXPECTED_BEHAVIOR should be specific enough to distinguish pass from fail during debugging.
- TARGET_SCOPE should bound where evidence is gathered before the workflow widens the search.

## Structured Outputs
- `REPRO_CAPTURE` (debug-capture-failure.v1; required): Reproduction recipe and missing repro inputs.
- `FAILURE_SURFACE_MAP` (debug-map-impact.v1; required): Reduced failing surface and entry points.
- `DEBUG_REPORT` (debug-report.v1; required): Root-cause analysis and fix direction.
- `TEST_GAP_REPORT` (test-gap-report.v1; required): Regression protection gaps to close after the fix.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Actual atomic path executed by the workflow.

## Output Contract Notes
- REPRO_CAPTURE should stay focused on making the failure rerunnable, not on explaining the cause.
- FAILURE_SURFACE_MAP should remain a map of likely surface and entry points, not a confirmed root cause.
- DEBUG_REPORT should explicitly separate confirmed cause from still-open hypotheses.
- TEST_GAP_REPORT should focus on regression protection to add after the concrete fix.
- EXPANDED_ATOMIC_PATH must preserve execution order explicitly.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: debug-capture-failure.v1, debug-map-impact.v1, debug-report.v1, test-gap-report.v1

## Neutrality Rules
- Keep repro capture, surface mapping, root cause, and test gaps as distinct outputs.
- Do not treat suspicion from the surface map as confirmed cause.
- Keep the workflow explicit and inspectable.

## Execution Constraints
- Do not collapse mapped surface, root cause, and regression gaps into one blob report.
- If reproduction or evidence is incomplete, keep the debug result inconclusive instead of overstating confidence.
- Preserve the explicit expanded workflow path in the final output.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

원인을 한 줄로 — 아직 확인 못 했으면 "미확인: [후보들]"

```
원인: [무엇이 왜 망가졌는지]
근거: [로그, 추적, 테스트 등]
수정: `파일:줄` — [변경 내용]
```

회귀 테스트 빈틈: [추가해야 할 테스트]

미확인일 때: "후보 [N]개로 좁혔습니다 — 가장 빠른 다음 확인: [X]. 실행할까요?"
단계 막힐 때: "[단계]에서 막힘 — [계속하려면 무엇이 필요한지]"

## Mandatory Rules
- Preserve the separation between mapped surface and confirmed cause.
- Expose the expanded atomic path explicitly.

## Expansion
- `$debug-capture-failure`
- `$debug-map-impact`
- `$debug-find-root-cause`
- `$test-find-gaps`

## Example Invocation
```text
$workflow-debug-this
TARGET_SCOPE: src/session
FAILURE_SYMPTOM: session disappears after refresh
EXPECTED_BEHAVIOR: session persists after refresh
```

## Eval Cases

| Prompt | Should Trigger | Key Output Check |
|--------|---------------|-----------------|
| 새로고침하면 세션이 사라지는데 원인 찾고 수정까지 해줘. | YES | REPRO_CAPTURE 존재 |
| 로그 보니까 에러 나는데, 어디서 터지는지 좁혀서 고쳐봐. | YES | DEBUG_REPORT 존재 |
| 전반적인 코드 리뷰 좀 해줘. | NO | 버그 수정 전용 — workflow-review-change 권장 |
