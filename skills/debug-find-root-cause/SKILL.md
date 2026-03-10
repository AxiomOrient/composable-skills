---
name: debug-find-root-cause
description: "Neutral debugging skill for concrete failures. Use when a concrete failure, bug, or crash requires reproducible debugging and root-cause analysis. Do not use when feature implementation, broad design planning, or non-failure analysis is the primary intent. English triggers: debug, crash analysis, root-cause."
---

# Debug

## Purpose
Reproduce a concrete failure, confirm root cause, and isolate the minimal fix path.

## Default Program
```text
[stages: preflight>detect>analyze>implement>verify>audit |
 scope: diff |
 lens: feynman |
 output: md(contract=v1)]
```

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
- `frame_name`: Reproduce-and-Explain Investigator
- `why`: Debugging should reproduce first, test hypotheses, and explain the confirmed cause plainly.
- `summary`: Reproduce first, use disprovable hypotheses, and explain the result plainly.
- `thesis`: If you cannot reproduce the phenomenon, isolate the variables, and explain it in plain language, you do not understand it well enough to trust the fix.
- `decision_rules`:
  - Reduce the failure to the cheapest reproducible case before proposing a fix.
  - Prefer hypotheses that can be disproved quickly by observation, logs, or tests.
  - State observed versus expected behavior explicitly before naming root cause.
  - Leave behind a regression guard when the cause becomes clear.
- `anti_patterns`:
  - Patch-first debugging
  - Stack-trace worship without a repro path
  - Cause claims that skip observed-versus-expected framing
- `good_for`:
  - debugging
  - answer repair
  - failure-surface mapping
  - final verification
- `not_for`:
  - broad risk prioritization
  - navigation or UX review
  - high-level strategic planning
- `required_artifacts`:
  - Repro Steps
  - Observed vs Expected
  - Falsification or Evidence Trail
  - Regression Guard
- `references`:
  - https://www.feynmanlectures.caltech.edu/
  - https://www.nobelprize.org/prizes/physics/1965/feynman/biographical/

## Artifacts
- `artifacts_in`: debug-map-blast-radius.v1
- `artifacts_out`: debug-report.v1

## Neutrality Rules
- Do not assume the first plausible cause is the root cause.
- If reproduction is missing, say repro-missing rather than guessing the fix.
- Separate symptom, cause hypothesis, and confirmed cause.

## Execution Constraints
- Do not claim a confirmed cause until the observed evidence discriminates it from plausible alternatives.
- If the evidence cannot isolate the cause, keep the result inconclusive and return the cheapest next discriminating check.
- Do not implement or recommend a confident fix path solely to satisfy a bug-fix request when the root cause is still unconfirmed.

## Output Discipline
- `response_profile=debug_report`
- User-facing rendering is delegated to `respond`.
