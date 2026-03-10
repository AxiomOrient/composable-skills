---
name: check-security-holes
description: "Use when running security audits, threat modeling, or vulnerability verification with prioritized findings. Do not use when non-security implementation, generic debugging, or pure performance analysis is the primary task. English triggers: security audit, vulnerability check, threat model."
---

# Security

## Purpose
Surface security issues and threat-relevant risks.

## Default Program
```text
[stages: preflight>detect>analyze>plan>verify>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,safety-gates,quality-gates{security,tests},deterministic-output |
 lens: nist-rmf |
 output: md(contract=v1)]
```

## Use When
- Need vulnerability, threat-model, or mitigation-verification output.
- Need security-specific review with prioritized findings.
- Need exploitability or mitigation evidence before merge or release.

## Do Not Use When
- Need general debugging or performance analysis.
- Need direct implementation.
- Need broad review or release judgement instead of security-specific output.

## Required Inputs
- `SECURITY_GOAL` (audit|threat-model|mitigation-verify; required): Security objective.
- `TARGET_SCOPE` (file|module|service|repo|diff; required): Scope to inspect.
- `ASSETS_OR_BOUNDARIES` (list; required; shape: {ASSET_OR_BOUNDARY, WHY_RELEVANT}): Assets, trust boundaries, or entrypoints to prioritize.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Scans, prior findings, logs, or threat notes.

## Input Contract Notes
- ASSETS_OR_BOUNDARIES should anchor the review to real assets, trust boundaries, or entrypoints rather than broad fear-driven scanning.
- KNOWN_EVIDENCE should cite existing scans, logs, or prior findings only; do not preload vulnerability conclusions into the evidence list.
- Use SECURITY_GOAL to choose the review mode, not to imply that a vulnerability must be found.

## Structured Outputs
- `THREAT_MODEL` (object; required): Assets, attacker model, boundaries, and entrypoints.
- `SECURITY_FINDINGS` (list; required; shape: {SEVERITY, ISSUE, LOCATION, EVIDENCE, EXPLOITABILITY}): Prioritized vulnerability findings.
- `MITIGATION_VERIFICATION` (list; required; shape: {CONTROL_OR_MITIGATION, STATUS, EVIDENCE}): Mitigation checks or verification results.

## Output Contract Notes
- SECURITY_FINDINGS may be empty when the threat model and available evidence do not support a concrete vulnerability claim.
- Use MITIGATION_VERIFICATION for hardening checks or control status instead of presenting every improvement idea as a vulnerability.
- If exploitability is uncertain, record that uncertainty explicitly instead of smoothing it into a confirmed finding.

## Primary Lens
- `primary_lens`: `nist-rmf`
- `frame_name`: Control-and-Monitor Risk Framer
- `why`: Security review should frame assets, controls, and monitoring needs systematically.
- `summary`: Systematic risk framing with controls and continuous monitoring lifecycle.
- `thesis`: Security review should move from assets and boundaries to controls, residual risk, and monitoring, rather than stopping at vulnerability spotting alone.
- `decision_rules`:
  - Frame the system boundary, asset class, and threat-relevant context first.
  - Map findings to missing, weak, or unverified controls.
  - Separate immediate mitigation from ongoing monitoring needs.
  - State residual risk after controls, not only raw issue count.
- `anti_patterns`:
  - Issue lists with no system context
  - Threat claims without control mapping
  - Mitigation advice without monitoring or verification
- `good_for`:
  - security review
  - control assessment
  - risk framing
- `not_for`:
  - UI structure review
  - performance optimization
  - message architecture
- `required_artifacts`:
  - System Categorization
  - Control Selection or Status
  - Continuous Monitoring Plan
- `references`:
  - https://csrc.nist.gov/projects/risk-management/about-rmf

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: security-report.v1

## Neutrality Rules
- Build the threat model before asserting vulnerability impact.
- If exploitability is uncertain, mark it as unverified rather than overstating certainty.
- Separate discovered vulnerabilities from hardening suggestions.

## Execution Constraints
- Do not invent vulnerabilities to satisfy a security-audit request; return an empty SECURITY_FINDINGS list when evidence does not support a finding.
- Keep the report anchored to the stated assets and boundaries instead of broad speculative fear scanning.
- Treat missing proof as unverified exploitability, not as a confirmed issue.

## Output Discipline
- `response_profile=security_report`
- User-facing rendering is delegated to `respond`.
