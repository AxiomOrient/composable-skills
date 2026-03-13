---
name: check-failure-paths
description: "Review only the failure paths, exception handling, fallback logic, and cleanup behavior of a bounded scope. Use when the goal is to inspect error handling rather than run a broad review."
---

# Check / Failure Paths

## Purpose
Find missing, inconsistent, or unsafe error handling paths in a bounded target.

## Default Program
```text
[stages: preflight>detect>analyze>review>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: feynman | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `feynman` because it keeps the work aligned with: Reproduce first, use disprovable hypotheses, and explain the result plainly.

## Use When
- Need to inspect only failure paths and cleanup behavior.
- Need to verify exception, fallback, timeout, or rollback handling.
- Need a bounded review focused on unhappy-path behavior.

## Do Not Use When
- Need a broad review across all concerns.
- Need to implement the fix immediately without first checking error-path coverage.
- The target has no relevant failure or cleanup paths.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Where to inspect error paths.
- `FAILURE_MODES` (list; optional; shape: {MODE, WHY_RELEVANT}): Known failure modes to prioritize.

## Input Contract Notes
- TARGET_SCOPE should stay bounded to the component or path where the failure handling is actually implemented.
- FAILURE_MODES should name concrete failure conditions rather than broad worries such as `robustness`.

## Structured Outputs
- `ERROR_PATH_FINDINGS` (list; required; shape: {ISSUE, FAILURE_MODE, LOCATION, EVIDENCE}): Failure-path findings with evidence.
- `MISSING_GUARDS` (list; required; shape: {GUARD, LOCATION, WHY_NEEDED}): Guards, cleanup steps, or fallback behaviors missing from the code.
- `RECOVERY_GAPS` (list; required; shape: {GAP, LOCATION, IMPACT}): Places where the code fails unsafely or recovers inconsistently.

## Output Contract Notes
- Tie each ERROR_PATH_FINDINGS entry to a concrete failure mode or cleanup path.
- Use MISSING_GUARDS for absent checks and RECOVERY_GAPS for unsafe or inconsistent recovery behavior.
- If a suspected failure path cannot be evidenced, keep it out of findings and record it as a verification gap in the narrative instead.

## Procedure
1. Trace each relevant failure path through validation, cleanup, fallback, and propagation.
2. Identify missing guards, inconsistent recovery, or hidden silent-failure cases.
3. Return only failure-path findings, not general style comments.

## Primary Lens
- `primary_lens`: `feynman`
- `why`: Error-path review should compare observed failure behavior against expected recovery behavior.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: check-failure-paths.v1

## Neutrality Rules
- Review only failure paths and do not inflate normal-path style issues into defects.
- Separate proven missing guards from speculative robustness ideas.
- If a failure mode is untested or unreachable from current evidence, mark it as a gap rather than a bug.

## Execution Constraints
- Stay on unhappy-path behavior and cleanup logic only.
- Do not rewrite the review into a general correctness or style pass.
- Prefer concrete failure-mode traces over hypothetical robustness brainstorming.

## Response Format

Group findings by severity — P0 (unsafe), P1 (missing guard), P2 (inconsistent recovery):

P0 — file:line — [failure mode]: [what breaks and how badly]
P1 — file:line — [missing guard]: [what is unguarded]

List RECOVERY_GAPS separately if any paths leave the system in a bad state.

End with: "Fix P0s now, or want full gap list first?"

## Mandatory Rules
- Stay on error paths only.
- Tie every finding to a concrete failure mode or cleanup gap.

## Example Invocation
```text
$check-failure-paths
TARGET_SCOPE: src/queue
FAILURE_MODES: timeout, partial write, retry exhaustion
```
