---
name: review-failure-paths
description: "Review only the failure paths, exception handling, fallback logic, and cleanup behavior of a bounded scope. Use when the goal is unhappy-path inspection rather than a broad review."
---

# Review / Failure Paths

## Purpose
Find missing, inconsistent, or unsafe error-handling paths in a bounded target.

## Default Program
```text
[stages: preflight>detect>analyze>review>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: feynman | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `feynman` because it keeps the work aligned with: Reproduce first, use disprovable hypotheses, and explain the result plainly.

## Use When
- Need to inspect only failure paths and cleanup behavior.
- Need to verify exception, fallback, timeout, or recovery handling.
- Need a bounded review focused on unhappy-path behavior.

## Do Not Use When
- Need a broad review across all concerns.
- Need to implement the fix immediately without first checking error-path coverage.
- The target has no relevant failure or cleanup paths.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Where to inspect failure paths.
- `FAILURE_FOCUS` (exceptions|fallbacks|recovery|all; optional; allowed: exceptions|fallbacks|recovery|all): Which unhappy-path slice to emphasize. Defaults to `all`.
- `FAILURE_MODES` (list; optional; shape: {MODE, WHY_RELEVANT}): Known failure modes to prioritize.

## Input Contract Notes
- TARGET_SCOPE should stay bounded to the component or path where failure handling is actually implemented.
- FAILURE_MODES should name concrete failure conditions rather than broad worries such as `robustness`.
- FAILURE_FOCUS narrows emphasis only; it should not hide other clearly evidenced failure-path bugs.

## Structured Outputs
- `ERROR_PATH_FINDINGS` (list; required; shape: {ISSUE, FAILURE_MODE, LOCATION, EVIDENCE}): Failure-path findings with evidence.
- `MISSING_GUARDS` (list; required; shape: {GUARD, LOCATION, WHY_NEEDED}): Guards, cleanup steps, or fallback behaviors missing from the code.
- `RECOVERY_GAPS` (list; required; shape: {GAP, LOCATION, IMPACT}): Places where the code fails unsafely or recovers inconsistently.
- `FAILURE_PATH_STATUS` (clean|needs-fix|inconclusive; required; allowed: clean|needs-fix|inconclusive): Overall unhappy-path review state.

## Output Contract Notes
- Tie each ERROR_PATH_FINDINGS entry to a concrete failure mode or cleanup path.
- Use MISSING_GUARDS for absent checks and RECOVERY_GAPS for unsafe or inconsistent recovery behavior.
- If a suspected failure path cannot be evidenced, keep it out of findings and record it as an inconclusive note instead.

## Primary Lens
- `primary_lens`: `feynman`
- `why`: Error-path review should compare observed failure behavior against expected recovery behavior.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: failure-path-review.v1

## Neutrality Rules
- Review only failure paths and do not inflate normal-path style issues into defects.
- Separate proven missing guards from speculative robustness ideas.
- If a failure mode is untested or unreachable from current evidence, mark it inconclusive rather than as a bug.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

심각도별로:

긴급 — `file:line` — [어떤 오류] — [어떻게 망가지는지]
중요 — `file:line` — [빠진 처리] — [무엇이 무방비인지]
참고 — `file:line` — [복구 불일치]

복구 후에도 시스템이 나쁜 상태로 남으면 따로 표시.

끝에: "긴급부터 처리할까요, 아니면 전체 목록을 먼저 볼까요?"

## Execution Constraints
- Stay on unhappy-path behavior and cleanup logic only.
- Do not rewrite the review into a general correctness or style pass.
- Prefer concrete failure-mode traces over hypothetical robustness brainstorming.

## Example Invocation
```text
$review-failure-paths
TARGET_SCOPE: src/queue
FAILURE_FOCUS: exceptions
FAILURE_MODES:
  - {MODE: timeout, WHY_RELEVANT: external API can hang}
```
