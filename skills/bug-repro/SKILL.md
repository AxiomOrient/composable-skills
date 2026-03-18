---
name: bug-repro
description: "Turn a vague bug report into a rerunnable reproduction with explicit environment facts, minimal failing steps, and evidence. Use when the immediate job is to prove the failure and narrow missing inputs before deeper root-cause work."
---
# Bug Repro

## Purpose
Convert a symptom into a rerunnable failure description that another engineer or agent can execute without guesswork.

## Default Program
```text
[stages: preflight>detect>analyze>verify>handoff>audit |
 scope: repo|paths(glob,...) |
 policy: evidence,repro-first,deterministic-output |
 lens: popper-falsification |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `popper-falsification` because it keeps the work aligned with: observable claims, disprovable reproduction steps, and explicit separation between confirmed failure and missing evidence.

## Use When
- Need a bug report turned into a minimal, rerunnable repro.
- Need to separate observed failure from guessed cause.
- Need evidence collection before deeper debugging or fixing.

## Do Not Use When
- The failure is already reproducible and the immediate job is root-cause analysis.
- Need only a broad issue summary with no runnable failure path.
- Need regression test design after the fix rather than repro capture before the fix.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo|runtime-surface; required): Where the bug appears.
- `FAILURE_SYMPTOM` (string; required): Observable failure symptom.
- `EXPECTED_BEHAVIOR` (string; required): What should happen instead.
- `REPRO_ASSET_HINTS` (list; optional; shape: {REF, WHY_RELEVANT}): Logs, screenshots, commands, fixtures, or issue reports that may help reproduce.

## Input Contract Notes
- `FAILURE_SYMPTOM` should describe what happens, not why it happens.
- `EXPECTED_BEHAVIOR` should be concrete enough to distinguish pass from fail.
- `REPRO_ASSET_HINTS` may be partial; missing assets should be surfaced instead of guessed.

## Structured Outputs
- `REPRO_STEPS` (list; required; shape: {STEP, ACTION, EXPECTED_FAIL_SIGNAL}): Minimal rerunnable steps.
- `REPRO_ENVIRONMENT` (list; required; shape: {FACT, VALUE, WHY_IT_MATTERS}): Environment facts that materially affect reproduction.
- `EVIDENCE_PACK` (list; required; shape: {TYPE, REF, WHY_RELEVANT}): Logs, screenshots, commands, or fixtures that support the repro.
- `MISSING_INPUTS` (list; required; shape: {INPUT, WHY_NEEDED, CHEAPEST_WAY_TO_GET_IT}): Gaps that prevent a trustworthy repro.

## Output Contract Notes
- `REPRO_STEPS` should stay minimal enough that another person can run them quickly.
- `REPRO_ENVIRONMENT` should only include facts that materially affect the failure.
- `EVIDENCE_PACK` should distinguish direct evidence from contextual hints.
- `MISSING_INPUTS` should block overconfidence instead of being buried.

## Primary Lens
- `primary_lens`: `popper-falsification`
- `why`: Reproduction should turn vague claims into disprovable, rerunnable checks.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: bug-repro-capture.v1

## Response Format
Think and operate in English, but deliver the final response in Korean.
Lead with one line:
`Repro: confirmed|partial|blocked — scope: [TARGET_SCOPE]`

Then show:
- Minimal repro steps.
- Environment facts that matter.
- Evidence pack.
- Missing inputs, if any.

If the repro is still partial, end with:
`Cheapest next repro check: [X]`

## Neutrality Rules
- Never present a guessed cause as part of the repro result.
- Distinguish direct evidence from inference.
- If the failure cannot be reproduced with current evidence, report partial or blocked instead of forcing certainty.

## Execution Constraints
- Prefer the smallest failing path over a broad end-to-end scenario when both prove the same bug.
- Keep the repro independent of proposed fixes.
- Ask for or capture the one missing input that most cheaply disambiguates the repro.

## References
- `references/repro-capture-template.md`
- `references/evidence-minimum.md`

## Example Invocation
```text
$bug-repro TARGET_SCOPE: apps/web FAILURE_SYMPTOM: session disappears after refresh EXPECTED_BEHAVIOR: session persists after refresh REPRO_ASSET_HINTS:
- REF: issue-214.md
  WHY_RELEVANT: original user report with screenshots
- REF: logs/session-refresh.txt
  WHY_RELEVANT: current failing request log
```
