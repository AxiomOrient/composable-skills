---
name: review-final-verify
description: "Final verification skill for explicit done criteria after work output is complete. Use when delivery needs a last read-and-check pass, not new implementation."
---

# Review / Final Verify

## Purpose
Perform final contract and evidence verification.

## Default Program
```text
[stages: review>audit |
 scope: diff |
 policy: evidence,quality-gates{tests,security},deterministic-output |
 lens: contract-evidence-verifier |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `contract-evidence-verifier` because it keeps the work aligned with: Check explicit contracts against fresh evidence, separate blockers from gaps, and do not claim pass without proof.

## Use When
- Need explicit final checks before delivering an answer.
- Need final verification of docs, outputs, tests, or task sync.
- Need a separate validation gate after implementation or review.

## Do Not Use When
- Need feature implementation.
- Need broad analysis instead of final verification.
- Need a domain-specific review rather than final validation.

## Required Inputs
- `VERIFY_TARGETS` (list; required; shape: {TARGET, TYPE}): Files, docs, outputs, or artifacts to validate.
- `DONE_CRITERIA` (list; required; shape: {CONTRACT, SOURCE}): Sections, schemas, or invariants that must hold.
- `VERIFY_SCOPE` (diff|docs|path-set; required): Verification scope.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Tests, logs, or prior review outputs.

## Input Contract Notes
- VERIFY_TARGETS should be explicit artifacts or paths, not vague module names.
- DONE_CRITERIA must be checkable invariants with a visible source of truth.
- KNOWN_EVIDENCE can seed the check list, but stale evidence should be rerun when feasible.
- If simplicity, user-focus, or scope-discipline must be verified, include them as explicit observable DONE_CRITERIA instead of taste-based expectations.

## Structured Outputs
- `BLOCKERS` (list; required; shape: {ISSUE, LOCATION, WHY_BLOCKING}): Blocking contract violations or evidence failures that prevent a pass.
- `VERIFIED_CHECKS` (list; required; shape: {CHECK, RESULT, EVIDENCE}): Checks actually run against the explicit contract.
- `EVIDENCE_GAPS` (list; required; shape: {GAP, CHEAPEST_NEXT_CHECK}): Missing evidence that keeps the result from becoming fully conclusive.
- `P2_RESIDUALS` (list; required; shape: {ISSUE, LOCATION, NEXT_CHECK}): Residual non-blocking items not fixed.
- `FINAL_VERIFICATION_STATUS` (pass|blocked|inconclusive; required; allowed: pass|blocked|inconclusive): Pass, blocked, or inconclusive final status.

## Output Contract Notes
- Use `blocked` when an explicit contract is violated and delivery should stop.
- Use `inconclusive` when the contract could not be fully checked because evidence is missing.
- Mark `pass` only when each expected contract has at least one VERIFIED_CHECKS entry and both BLOCKERS and EVIDENCE_GAPS are empty.

## Primary Lens
- `primary_lens`: `contract-evidence-verifier`
- `why`: Final verification should check explicit contracts against fresh evidence, separate blockers from gaps, and surface the cheapest next check.

## Artifacts
- `artifacts_in`: implementation-delta.v1, review-report.v1, audit-report.v1
- `artifacts_out`: final-verification-report.v1

## Neutrality Rules
- Verify only against explicit contracts and evidence; do not invent defects.
- If evidence is insufficient, mark the conclusion as inconclusive and state the cheapest next check.
- Separate structural violation, evidence gap, and residual polish.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

결과부터: **통과** / **중단** / **미확인**

중단이거나 미확인이면 문제 먼저:
- [문제] — [어디서] — [왜 문제인지]

확인한 항목:
- 항목 | 결과 | 근거

확인 못 한 것이 있으면 가장 빠른 다음 확인 방법과 함께 적기.

## Execution Constraints
- Verification is read-and-check only; do not modify files from this skill.
- Prefer rerunning the cheapest relevant check over trusting stale success claims.
- Keep blockers, evidence gaps, and residual polish items in separate buckets.

## Example Invocation
```text
$review-final-verify
VERIFY_TARGETS:
  - {TARGET: src/auth/session.ts, TYPE: code}
DONE_CRITERIA:
  - {CONTRACT: session refresh test passes, SOURCE: tests/auth}
VERIFY_SCOPE: path-set
```
