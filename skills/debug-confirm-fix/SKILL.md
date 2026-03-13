---
name: debug-confirm-fix
description: "Verify that a chosen fix actually removes the bug and leaves behind meaningful regression protection. Use after a concrete fix candidate exists, not during the initial root-cause search."
---

# Debug / Confirm Fix

## Purpose
Check whether a fix candidate removes the failure and whether the regression guard is real.

## Default Program
```text
[stages: preflight>detect>verify>review>audit | scope: diff|repo|paths(glob,...) | policy: evidence,quality-gates{tests},deterministic-output | lens: contract-evidence-verifier | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `contract-evidence-verifier` because it keeps the work aligned with: Check explicit contracts against fresh evidence, separate blockers from gaps, and do not claim pass without proof.

## Use When
- Need to verify a fix candidate after root cause is already known.
- Need to confirm the bug is gone and the guard is meaningful.
- Need a narrow post-fix validation step rather than another broad debug pass.

## Do Not Use When
- Still lack a stable repro or fix candidate.
- Need first-pass root-cause debugging.
- Need direct implementation work rather than post-fix confirmation.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Scope where the fix applies.
- `FIX_CANDIDATE` (string; required): Fix or change being verified.
- `EXPECTED_BEHAVIOR` (string; required): Expected behavior after the fix.
- `REPRO_STEPS` (list; required; shape: {STEP, PURPOSE, EXPECTED_SIGNAL}): Repro steps used to confirm the fix.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Tests, logs, or prior debug evidence already known.

## Input Contract Notes
- FIX_CANDIDATE should describe the actual fix being checked, not a vague intention to fix later.
- REPRO_STEPS should be concrete enough to rerun the original failure.
- KNOWN_EVIDENCE should contain current proof only; stale success claims should be rerun when feasible.

## Structured Outputs
- `FIX_CONFIRMATION_STATUS` (pass|blocked|inconclusive; required; allowed: pass|blocked|inconclusive): Whether the fix is confirmed, blocked, or still inconclusive.
- `VERIFIED_BEHAVIORS` (list; required; shape: {BEHAVIOR, RESULT, EVIDENCE}): Behaviors rechecked after the fix.
- `REGRESSION_GUARD_STATUS` (list; required; shape: {GUARD, STATUS, EVIDENCE}): Whether the regression guard exists and actually protects the fixed behavior.

## Output Contract Notes
- FIX_CONFIRMATION_STATUS=pass requires both behavior confirmation and guard confirmation.
- VERIFIED_BEHAVIORS should cite rerun evidence rather than relying on memory.
- REGRESSION_GUARD_STATUS may be incomplete when the behavior is fixed but the protection is still weak.

## Primary Lens
- `primary_lens`: `contract-evidence-verifier`
- `why`: Post-fix confirmation should verify the explicit contract against fresh repro and guard evidence before claiming the bug is really gone.

## Artifacts
- `artifacts_in`: debug-report.v1, test-report.v1
- `artifacts_out`: debug-fix-confirmation.v1

## Neutrality Rules
- Do not call the fix confirmed without rerun evidence.
- Separate fixed behavior from guard quality.
- Mark inconclusive when the fix cannot be fully rechecked.

## Response Format

Lead with fix status: PASS / BLOCKED / INCONCLUSIVE.

Show what was verified:
- [behavior] → [result] — evidence: [test or command]

Show guard status:
- [guard] → [exists / weak / missing] — [why it matters]

Ask: "Guard in place? Want regression test strengthened?"

## Execution Constraints
- Do not turn this skill into another full root-cause report.
- Prefer rerunning the smallest relevant repro and guard checks first.
- Keep the output focused on post-fix confirmation.
