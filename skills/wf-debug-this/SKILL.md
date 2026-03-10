---
name: wf-debug-this
description: "Workflow skill that narrows a failure surface, performs root-cause debugging, and checks regression protection. Use when the user wants an explicit debug loop rather than a broad 'fix the bug' instruction."
---

# Debug Workflow

## Purpose
Compose failure-surface reduction, debugging, and test-gap awareness into one explicit debug workflow.

## Default Program
```text
[stages: preflight>detect>analyze>implement>verify>review>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{tests},deterministic-output | lens: feynman | output: md(contract=v1)]
```

## Use When
- Need a bounded debug loop for a concrete failure.
- Need to reduce failure surface before root-cause work.
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
- `FAILURE_SURFACE_MAP` (debug-map-blast-radius.v1; required): Reduced failing surface and entry points.
- `DEBUG_REPORT` (debug-report.v1; required): Root-cause analysis and fix direction.
- `TEST_GAP_REPORT` (test-gap-report.v1; required): Regression protection gaps to close after the fix.

## Output Contract Notes
- FAILURE_SURFACE_MAP should remain a map of likely surface and entry points, not a confirmed root cause.
- DEBUG_REPORT should explicitly separate confirmed cause from still-open hypotheses.
- TEST_GAP_REPORT should focus on regression protection to add after the concrete fix.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: debug-map-blast-radius.v1, debug-report.v1, test-gap-report.v1

## Neutrality Rules
- Keep surface mapping, root cause, and test gaps as distinct outputs.
- Do not treat suspicion from the surface map as confirmed cause.
- Keep the workflow explicit and inspectable.

## Execution Constraints
- Do not collapse mapped surface, root cause, and regression gaps into one blob report.
- If reproduction or evidence is incomplete, keep the debug result inconclusive instead of overstating confidence.
- Preserve the explicit expanded workflow path in the final output.

## Mandatory Rules
- Preserve the separation between mapped surface and confirmed cause.
- Expose the expanded atomic path explicitly.

## Expansion
- `$debug-map-blast-radius`
- `$debug-find-root-cause`
- `$test-find-gaps`

## Example Invocation
```text
$wf-debug-this
TARGET_SCOPE: src/session
FAILURE_SYMPTOM: session disappears after refresh
EXPECTED_BEHAVIOR: session persists after refresh
```

## Output Discipline
- `response_profile=debug_report`
- User-facing rendering is delegated to `respond`.
