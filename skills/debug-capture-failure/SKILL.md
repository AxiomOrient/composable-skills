---
name: debug-capture-failure
description: "Turn a failure symptom into a repeatable failing recipe. Use when a bug report is real but the failure steps are still missing, unstable, or too hand-wavy for deeper debugging."
---

# Debug / Capture Failure

## Purpose
Convert a reported failure into concrete reproduction steps and explicit missing repro inputs.

## Default Program
```text
[stages: preflight>detect>analyze>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: feynman | output: md(contract=v1)]
```

## Use When
- Need a stable repro recipe before deeper debugging.
- Need to turn a vague failure report into actionable reproduction steps.
- Need to separate missing repro data from root-cause hypotheses.

## Do Not Use When
- Already have a stable repro recipe.
- Need confirmed root cause rather than repro capture.
- Need direct implementation or broad review work.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Scope in which the failure appears.
- `FAILURE_SYMPTOM` (string; required): Observed failure symptom.
- `EXPECTED_BEHAVIOR` (string; required): Expected behavior instead of the failure.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Logs, failing commands, traces, or notes already known.

## Input Contract Notes
- FAILURE_SYMPTOM should describe the observed failure, not a guessed cause.
- EXPECTED_BEHAVIOR should be specific enough to distinguish pass from fail.
- KNOWN_EVIDENCE should contain current traces or commands, not fix proposals.

## Structured Outputs
- `REPRO_STEPS` (list; required; shape: {STEP, PURPOSE, EXPECTED_SIGNAL}): Concrete reproduction steps.
- `REPRO_STATUS` (stable|partial|missing; required; allowed: stable|partial|missing): Whether the repro is fully captured, partial, or still missing.
- `MISSING_REPRO_INPUTS` (list; required; shape: {INPUT, WHY_NEEDED}): Missing data or environment details needed to make the repro stable.

## Output Contract Notes
- REPRO_STEPS should be executable and concrete rather than a vague narrative.
- REPRO_STATUS=stable should mean another maintainer could plausibly rerun the failure from the provided steps.
- MISSING_REPRO_INPUTS may be empty when the repro is already stable.

## Primary Lens
- `primary_lens`: `feynman`
- `why`: Reproduction should become concrete and rerunnable before deeper debugging tries to explain the failure.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: debug-capture-failure.v1

## Neutrality Rules
- Capture reproduction without claiming root cause.
- Separate missing repro data from debugging hypotheses.
- Do not invent stable repro steps when evidence is incomplete.

## Execution Constraints
- Do not jump to fix advice from this skill.
- Prefer the smallest stable repro over a long environment dump.
- Keep the output focused on reproducing the failure.
