---
name: check-ship-risk
description: "Review-only skill. Evaluate existing diff/PR risks and quality gates. Do not edit code or create implementation plans here. English triggers: code review, diff review, regression audit."
---

# Ship Risk Check

## Purpose
Assess release or quality-gate risk with explicit evidence.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: diff |
 policy: evidence,quality-gates{tests,security,compat,style},deterministic-output |
 lens: kahneman-tversky |
 output: md(contract=v1)]
```

## Use When
- Need regression, gate, or release-adjacent audit output.
- Need explicit pass/fail or gap status for tests, security, and compatibility gates.
- Need audit evidence before merge or release.

## Do Not Use When
- Need direct code implementation.
- Need a general review verdict rather than gate audit.
- Need vulnerability analysis only.

## Required Inputs
- `AUDIT_GOAL` (regression-gate|release-risk|quality-gate-check; required): Type of audit judgement required.
- `TARGET_SCOPE` (diff|file|module|folder|repo; required): Scope to audit.
- `CHANGE_INTENT` (string; required): Claimed purpose of the change.
- `KNOWN_GATE_SIGNAL` (list; optional; shape: {SIGNAL, STATUS, SOURCE}): Known test, security, compat, or CI signals.

## Input Contract Notes
- CHANGE_INTENT should describe the claimed purpose of the change, not the audit verdict you expect to receive.
- KNOWN_GATE_SIGNAL should distinguish observed gate evidence from assumed or stale status.
- Use AUDIT_GOAL to choose the gate lens, not to preload the conclusion that a blocker must exist.

## Structured Outputs
- `GATE_STATUS` (list; required; shape: {GATE, STATUS, EVIDENCE}): Status of each relevant gate.
- `AUDIT_FINDINGS` (list; required; shape: {ISSUE, GATE, EVIDENCE, IMPACT}): Blocking or risky audit findings.
- `RISK_RECOMMENDATION` (string; required): Audit recommendation based on the gate evidence.

## Output Contract Notes
- AUDIT_FINDINGS may be empty when the observed gate evidence does not support a blocker or material risk.
- Use GATE_STATUS to record unverified or missing gate evidence instead of inventing a finding to fill the list.
- RISK_RECOMMENDATION should follow the cited gate evidence, including `pass-with-known-gaps` or equivalent inconclusive outcomes when needed.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `frame_name`: Bias-Aware Evidence Judge
- `why`: Audit should separate observed gate signals from inferred risk and mark uncertainty explicitly.
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
- `artifacts_out`: audit-report.v1

## Neutrality Rules
- Separate gate evidence from recommendation.
- If a gate is unverified, mark it as a gap instead of assuming pass or fail.
- Do not inflate style preference into a blocker without release or regression impact.

## Execution Constraints
- Do not manufacture audit blockers because the prompt asks for an audit; return an empty AUDIT_FINDINGS list when gate evidence is clean.
- If evidence is incomplete, mark the gate unverified and keep the recommendation proportional to that gap.
- Keep audit output tied to concrete gate signals rather than broad suspicion or preference debates.

## Output Discipline
- `response_profile=review_findings`
- User-facing rendering is delegated to `respond`.
