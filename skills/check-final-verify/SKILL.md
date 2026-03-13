---
name: check-final-verify
description: "Neutral final verification skill. Use when explicit final verification is required after work output is complete. Do not use for feature implementation, broad analysis, or as a substitute for a full review."
---

# Check / Final Verify

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
- `EXPECTED_CONTRACTS` (list; required; shape: {CONTRACT, SOURCE}): Sections, schemas, or invariants that must hold.
- `VERIFY_SCOPE` (diff|docs|path-set; required): Verification scope.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Tests, logs, or prior checklist/review outputs.

## Input Contract Notes
- VERIFY_TARGETS should be explicit artifacts or paths, not vague module names.
- EXPECTED_CONTRACTS must be checkable invariants with a visible source of truth.
- KNOWN_EVIDENCE can seed the check list, but stale evidence should be rerun when feasible.
- If simplicity, user-focus, or scope-discipline must be verified, include them as explicit and observable EXPECTED_CONTRACTS rather than as taste-based expectations.
- If test quality matters, include the exact required behaviors, required checks, or explicit coverage threshold in EXPECTED_CONTRACTS instead of assuming a generic quality bar.

## Structured Outputs
- `BLOCKERS` (list; required; shape: {ISSUE, LOCATION, WHY_BLOCKING}): Blocking contract violations or evidence failures that prevent a pass.
- `VERIFIED_CHECKS` (list; required; shape: {CHECK, RESULT, EVIDENCE}): Checks that were actually run against the explicit contract.
- `EVIDENCE_GAPS` (list; required; shape: {GAP, CHEAPEST_NEXT_CHECK}): Missing evidence that keeps the result from becoming fully conclusive.
- `P2_RESIDUALS` (list; required; shape: {ISSUE, LOCATION, NEXT_CHECK}): Residual P2 items not fixed.
- `FINAL_VERIFICATION_STATUS` (pass|blocked|inconclusive; required): Pass, blocked, or inconclusive final status.

## Output Contract Notes
- Use `blocked` when an explicit contract is violated and delivery should stop.
- Use `inconclusive` when the contract could not be fully checked because evidence is missing.
- Mark `pass` only when each expected contract has at least one VERIFIED_CHECKS entry and both BLOCKERS and EVIDENCE_GAPS are empty.
- Do not fail work on an arbitrary test-count or coverage preference unless that threshold was explicitly part of the contract.

## Primary Lens
- `primary_lens`: `contract-evidence-verifier`
- `why`: Final verification should check explicit contracts against fresh evidence, separate blockers from gaps, and surface the cheapest next check.

## Artifacts
- `artifacts_in`: implementation-delta.v1, review-report.v1, audit-report.v1
- `artifacts_out`: self-verify-report.v1

## Neutrality Rules
- Verify only against explicit contracts and evidence; do not invent defects.
- If evidence is insufficient, mark the conclusion as inconclusive and state the cheapest next check.
- Separate structural violation, evidence gap, and style issue.

## Execution Constraints
- Verification is read-and-check only; do not modify files from this skill.
- Prefer rerunning the cheapest relevant check over trusting stale success claims.
- Keep blockers, evidence gaps, and residual polish items in separate buckets.
- Do not escalate aesthetic preference into a blocker unless it violates an explicit contract or creates a concrete correctness, usability, or maintenance risk.
- For test-related verification, prefer rerunning the smallest relevant behavior check over relying on broad `all green` summaries.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Lead with the status: PASS / BLOCKED / INCONCLUSIVE.

If BLOCKED or INCONCLUSIVE, list blockers first:
- [contract violated or gap] — file:section — [why it blocks delivery]

Then show verified checks as a compact table:
- Contract | Result | Evidence

If any EVIDENCE_GAPS remain, list them with cheapest next check.

## Mandatory Rules
- Do not modify files here; verification is read-and-check only.
- Mark `FINAL_VERIFICATION_STATUS=pass` only when every explicit contract has evidence.
