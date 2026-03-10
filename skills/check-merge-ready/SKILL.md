---
name: check-merge-ready
description: "Neutral review-only verdict skill. Produce findings-first PR/code review with severity, confidence, file/line evidence, testing gaps, and integrate/hold judgement. Do not edit code or create implementation plans here. Compose with check-quality-scan for 9-item checklist coverage, or with check-ship-risk for release risk context."
---

# Check / Merge Ready

## Purpose
Issue a findings-first review verdict with evidence.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: diff |
 policy: evidence,quality-gates{tests,security,compat,style},deterministic-output |
 lens: kahneman-tversky |
 output: md(contract=v1)]
```

## Use When
- Need a final findings-first review verdict.
- Need prioritized review findings with file/line evidence.
- Need integrate/hold judgement after reviewing changed code.

## Do Not Use When
- Need direct code implementation.
- Need only the 9-item checklist without verdict synthesis.
- Need a narrow single-concern scan instead of a broad review verdict.

## Required Inputs
- `REVIEW_GOAL` (general-verdict|regression-risk|change-intent-check|narrow-focus; required; allowed: general-verdict|regression-risk|change-intent-check|narrow-focus): Type of review verdict needed.
- `TARGET_SCOPE` (diff|file|module|folder|repo; required): Scope to review.
- `CHANGE_INTENT` (string; required): Claimed purpose of the change.
- `KNOWN_TEST_SIGNAL` (list; optional; shape: {SIGNAL, STATUS, SOURCE}): Executed tests, missing tests, or CI status.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Security-only, perf-only, compat-only, or other focused constraints.

## Input Contract Notes
- CHANGE_INTENT should summarize the claimed purpose of the change, not the reviewer verdict.
- KNOWN_TEST_SIGNAL should distinguish executed evidence from missing or assumed coverage.
- Use REVIEW_GOAL=narrow-focus only when constraints clearly bound the inspection surface.

## Structured Outputs
- `FINDINGS` (list; required; shape: {SEVERITY, SUMMARY, LOCATION, EVIDENCE, CONFIDENCE}): Concrete findings with severity, confidence, and evidence.
- `TESTING_GAPS` (list; required; shape: {GAP, IMPACT, CHEAPEST_CHECK}): Testing gaps plus cheapest verification steps.
- `VERDICT` (integrate|hold; required; allowed: integrate|hold): Integrate or hold verdict with rationale.

## Output Contract Notes
- Each FINDINGS row should cite concrete evidence and keep severity separate from confidence.
- Use TESTING_GAPS for missing verification coverage even when no code defect is proven.
- VERDICT should summarize the practical merge stance after findings and testing gaps are considered.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `why`: Review verdicts should separate observed defects from inferred impact and mark uncertainty explicitly.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: review-report.v1

## Neutrality Rules
- Do not assume a finding exists; return no findings when evidence does not support one.
- Separate observed behavior from inferred impact.
- Do not convert maintainability preference into a blocker unless a concrete regression or risk exists.

## Execution Constraints
- Review is read-and-judge only; do not patch code or rewrite planning artifacts here.
- If evidence is insufficient to support a finding, downgrade it to a testing gap or inconclusive note instead of overstating impact.
- Keep the verdict tied to the supplied scope and change intent rather than repo-wide preference debates.
