---
name: check-merge-ready
description: "Neutral review-only verdict skill. Produce findings-first PR/code review with severity, confidence, file/line evidence, testing gaps, and integrate/hold judgement. Use for general review, PR review, and /review-style checks. For mandatory 9-item checklist evaluation, compose with check-quality-scan; for gate-centric release risk judgement, compose with audit. Do not edit code or create implementation plans here. English triggers: review, code review, PR review, /review, review verdict."
---

# Review

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
- `frame_name`: Bias-Aware Evidence Judge
- `why`: Review verdicts should separate observed defects from inferred impact and mark uncertainty explicitly.
- `summary`: Separate observed evidence from inferred risk, expose uncertainty, and resist conclusion-first bias.
- `thesis`: Good judgement is not strong opinion; it is disciplined separation between what is observed, what is inferred, and what still needs checking.
- `decision_rules`:
  - Separate observed evidence from interpretation before assigning impact.
  - Mark uncertainty explicitly instead of smoothing it away into confident prose.
  - Check whether the current conclusion is driven by vivid anecdotes, availability bias, or conclusion-first framing.
  - Prefer the cheapest discriminating next check when evidence is incomplete.
- `anti_patterns`:
  - Severity inflation without evidence
  - Confusing likelihood with impact
  - Treating first-pass intuition as verdict
- `good_for`:
  - neutral analysis
  - review
  - audit
  - risk judgement
  - quality checklists
- `not_for`:
  - step-by-step debugging
  - incremental refactor design
  - information architecture work
- `required_artifacts`:
  - Observed Evidence
  - Risk Inference
  - Uncertainty Note
  - Cheapest Verification Step
- `references`:
  - https://www.nobelprize.org/prizes/economic-sciences/2002/kahneman/facts/

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

## Output Discipline
- `response_profile=review_findings`
- User-facing rendering is delegated to `respond`.
