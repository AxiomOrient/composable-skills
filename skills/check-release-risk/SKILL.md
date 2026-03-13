---
name: check-release-risk
description: "Review-only skill. Evaluate existing diff/PR risks and quality gates before merge or release. Do not edit code or create implementation plans here. For full GO/NO-GO release judgment with rollout and rollback strategy, use release-verdict instead."
---

# Check / Release Risk

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

## Lens Rationale
This skill uses `kahneman-tversky` because it keeps the work aligned with: Separate observed evidence from inferred risk, expose uncertainty, and resist conclusion-first bias.

## Use When
- Need regression, gate, or release-adjacent audit output.
- Need explicit pass/fail or gap status for tests, security, and compatibility gates.
- Need audit evidence before merge or release.

## Do Not Use When
- Need direct code implementation.
- Need a general review verdict rather than gate audit — use check-merge-ready instead.
- Need vulnerability analysis only — use check-security-holes instead.
- Need full GO/NO-GO release judgment with rollout plan and rollback strategy — use release-verdict instead.

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
- `why`: Audit should separate observed gate signals from inferred risk and mark uncertainty explicitly.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: audit-report.v1

## Neutrality Rules
- Separate gate evidence from recommendation.
- If a gate is unverified, mark it as a gap instead of assuming pass or fail.
- Do not inflate style preference into a blocker without release or regression impact.

## Response Format

Show gate status as a compact table:
- Gate | Status (pass/fail/unverified) | Evidence

List blocking findings first:
- [gate] — file:line — [issue] — impact: [what breaks if shipped]

Follow with the RISK_RECOMMENDATION in one sentence.

If gates are unverified, list the cheapest check for each.

## Execution Constraints
- Do not manufacture audit blockers because the prompt asks for an audit; return an empty AUDIT_FINDINGS list when gate evidence is clean.
- If evidence is incomplete, mark the gate unverified and keep the recommendation proportional to that gap.
- Keep audit output tied to concrete gate signals rather than broad suspicion or preference debates.
