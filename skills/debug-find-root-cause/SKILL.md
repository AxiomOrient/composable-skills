---
name: debug-find-root-cause
description: "Neutral debugging skill for concrete failures. Use when a concrete failure, bug, or crash requires reproducible debugging and root-cause analysis after the repro is already stable or close to stable. Do not use when the main missing artifact is the repro recipe itself."
---

# Debug / Find Root Cause

## Purpose
Reproduce a concrete failure, confirm root cause, and isolate the minimal fix path.

## Default Program
```text
[stages: preflight>detect>analyze>implement>verify>audit |
 scope: diff|repo |
 lens: feynman |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `feynman` because it keeps the work aligned with: Reproduce first, use disprovable hypotheses, and explain the result plainly.

## Use When
- A concrete failure exists and reproducible RCA is required.
- Need to move from symptom to confirmed cause and minimal fix direction.
- Need regression guard planning after a real bug fix.

## Do Not Use When
- The request is exploratory with no concrete failure.
- The request is feature implementation.
- The immediate job is only to reduce failure surface.

## Required Inputs
- `FAILURE_SYMPTOM` (string; required): Observed failure symptom.
- `TARGET_SCOPE` (file|module|command|test|repo; required): Scope in which the failure appears.
- `EXPECTED_BEHAVIOR` (string; required): What should have happened.
- `REPRO_STATUS` (yes|no|partial; required): Whether a reproduction already exists.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Stack traces, logs, failing tests, or repro commands.

## Input Contract Notes
- FAILURE_SYMPTOM should describe the observed failure, not a guessed cause.
- EXPECTED_BEHAVIOR should be concrete enough to distinguish pass from fail during reproduction.
- KNOWN_EVIDENCE should cite observed traces, logs, or failing checks only; do not preload a root-cause conclusion into the evidence list.
- If the repro recipe is still missing, use `debug-capture-failure` first.

## Structured Outputs
- `REPRO_STEPS` (list; required; shape: {STEP, PURPOSE, EXPECTED_SIGNAL}): Cheapest reproduction steps.
- `OBSERVED_VS_EXPECTED` (object; required): Observed behavior versus expected behavior.
- `CONFIRMED_CAUSE` (string; required): Confirmed root cause or inconclusive result.
- `MINIMAL_FIX_DIRECTION` (string; required): Narrow fix path.
- `REGRESSION_GUARD` (list; required; shape: {GUARD, PURPOSE, STATUS}): Regression guard or repro harness to leave behind.

## Output Contract Notes
- CONFIRMED_CAUSE may explicitly be `inconclusive` when reproduction or evidence cannot isolate the cause.
- MINIMAL_FIX_DIRECTION should become a next-investigation direction rather than a guessed patch when the cause is still unconfirmed.
- REPRO_STEPS and OBSERVED_VS_EXPECTED should stay grounded in concrete signals, not retrospective theory.

## Primary Lens
- `primary_lens`: `feynman`
- `why`: Debugging should reproduce first, test hypotheses, and explain the confirmed cause plainly.

## Artifacts
- `artifacts_in`: debug-map-impact.v1
- `artifacts_out`: debug-report.v1

## Neutrality Rules
- Do not assume the first plausible cause is the root cause.
- If reproduction is missing, say repro-missing rather than guessing the fix.
- Separate symptom, cause hypothesis, and confirmed cause.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Lead with root cause in one line — or "inconclusive" if not yet confirmed.

Then show:
- Cause: [what is broken and why]
- Evidence: [specific trace, log line, or test that confirms it]
- Fix applied: [the minimal change made]

List any regression guards added or recommended.

Ask: "Reproduced the fix? Want regression test added?"

## Execution Constraints
- Do not claim a confirmed cause until the observed evidence discriminates it from plausible alternatives.
- If the evidence cannot isolate the cause, keep the result inconclusive and return the cheapest next discriminating check.
- Do not implement or recommend a confident fix path solely to satisfy a bug-fix request when the root cause is still unconfirmed.
