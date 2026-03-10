---
name: debug-map-blast-radius
description: "Map a concrete failure into reproduction scope, impacted paths, and observed-versus-expected boundaries before deeper debugging. Use when a bug exists but the failing surface is still diffuse."
---

# Failure Surface Map

## Purpose
Reduce a broad bug report to a bounded reproduction window and impacted code surface before root-cause work.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: feynman | output: md(contract=v1)]
```

## Use When
- A failure is reported but the affected modules or boundaries are still unclear.
- Need to map observed versus expected behavior before debugging deeper.
- Need a reproducible scope window for a bug hunt.

## Do Not Use When
- Need the final code fix directly.
- Need general repository analysis without a concrete failure symptom.
- Already have a confirmed root cause.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo, required): Scope in which the failure appears.
- `FAILURE_SYMPTOM` (string, required): Observed failure symptom.
- `EXPECTED_BEHAVIOR` (string, required): Expected behavior instead of the failure.
- `REPRO_HINTS` (list, optional): Known triggering inputs, timing, or environment hints.

## Structured Outputs
- `REPRO_WINDOW` (object, required): Minimal reproduction scope and trigger conditions.
- `IMPACTED_PATHS` (list, required): Files, modules, or boundaries most likely involved.
- `OBSERVED_VS_EXPECTED` (object, required): Observed behavior versus expected behavior.
- `NEXT_DEBUG_ENTRY_POINTS` (list, required): Cheapest next entry points for debugging.

## Procedure
1. Normalize the failure symptom and expected behavior into one comparison table.
2. Derive the smallest reproduction window from the given evidence.
3. Identify the most likely impacted paths and system boundaries.
4. Return the cheapest next debugging entry points without claiming root cause.

## Primary Lens
- `primary_lens`: `feynman`
- `frame_name`: Reproduce-and-Explain Investigator
- `why`: Failure mapping should shrink the problem space using observable repro evidence.
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
- `artifacts_in`: none
- `artifacts_out`: debug-map-blast-radius.v1

## Neutrality Rules
- Map the failing surface without asserting a root cause.
- Keep suspected modules tentative until evidence confirms them.
- If reproduction remains unclear, state the smallest missing condition explicitly.

## Mandatory Rules
- Do not jump directly to the fix.
- Keep the output focused on scope reduction and entry-point selection.

## Example Invocation
```text
$debug-map-blast-radius
TARGET_SCOPE: src/auth
FAILURE_SYMPTOM: login succeeds but session is lost after refresh
EXPECTED_BEHAVIOR: session persists after refresh
```

## Output Discipline
- `response_profile=analysis_report`
- User-facing rendering is delegated to `respond`.
