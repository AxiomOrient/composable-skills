---
name: check-security-holes
description: "Use when running security audits, repo-exposure reviews, or vulnerability verification with prioritized findings. Good for secret leaks, ignore drift, mobile config exposure, and pre-commit/pre-release security checks. Do not use when non-security implementation, generic debugging, or pure performance analysis is the primary goal."
---

# Check / Security Exposure

## Purpose
Surface concrete security issues and repo-exposure risks without turning every hardening idea into a blocker.

## Default Program
```text
[stages: preflight>detect>analyze>plan>verify>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,safety-gates,quality-gates{security,tests},deterministic-output |
 lens: nist-rmf |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `nist-rmf` because it keeps the work aligned with: Systematic risk framing with controls and continuous monitoring lifecycle.

## Use When
- Need a pre-commit or pre-release security pass focused on secret exposure, ignore drift, or shipped credentials.
- Need vulnerability, threat-model, or mitigation-verification output.
- Need security-specific review with prioritized findings.
- Need exploitability or mitigation evidence before merge or release.
- Need to distinguish public client config such as `GoogleService-Info.plist` from actual secret material before blocking a push or release.

## Do Not Use When
- Need always-on development policing or a broad hardening backlog.
- Need general debugging or performance analysis.
- Need direct implementation.
- Need broad review or release judgement instead of security-specific output.

## Required Inputs
- `SECURITY_GOAL` (audit|repo-exposure-review|threat-model|mitigation-verify; required): Security objective.
- `TARGET_SCOPE` (file|module|service|repo|diff; required): Scope to inspect.
- `REVIEW_STAGE` (github-commit|release|general; optional; allowed: github-commit|release|general): Delivery stage that triggered the review.
- `SENSITIVE_SURFACES` (list; optional; shape: {SURFACE, WHY_RELEVANT}): Assets, trust boundaries, vendor config files, ignore targets, or entrypoints to prioritize.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Scans, prior findings, logs, or threat notes.

## Input Contract Notes
- Use `repo-exposure-review` for lightweight commit/release gating rather than full threat modelling.
- `SENSITIVE_SURFACES` can name assets, trust boundaries, vendor config files, ignore targets, or suspected leak surfaces. Omit it when the review should start from the diff or repo baseline.
- KNOWN_EVIDENCE should cite existing scans, logs, or prior findings only; do not preload vulnerability conclusions into the evidence list.
- Use SECURITY_GOAL to choose the review mode, not to imply that a vulnerability must be found.
- When a file format is vendor-specific or its sensitivity is ambiguous, confirm against current official docs before calling it a leak. Prefer official vendor docs over blogs.

## Structured Outputs
- `THREAT_MODEL` (object; required): Assets, attacker model, boundaries, and entrypoints.
- `SECURITY_FINDINGS` (list; required; shape: {SEVERITY, ISSUE, LOCATION, EVIDENCE, EXPLOITABILITY, ACTION}): Prioritized vulnerability or exposure findings.
- `MITIGATION_VERIFICATION` (list; required; shape: {CONTROL_OR_MITIGATION, STATUS, EVIDENCE}): Mitigation checks or verification results.
- `EXPOSURE_DECISIONS` (list; required; shape: {ITEM, CLASSIFICATION, EVIDENCE, ACTION}): Classification of reviewed files or tokens, such as `secret`, `public-client-config`, `allowlisted`, or `unverified`.

## Output Contract Notes
- SECURITY_FINDINGS may be empty when the threat model and available evidence do not support a concrete vulnerability claim.
- Use MITIGATION_VERIFICATION for hardening checks or control status instead of presenting every improvement idea as a vulnerability.
- Use EXPOSURE_DECISIONS to separate actual secret leaks from intentionally tracked public config or false positives.
- If exploitability or sensitivity is uncertain, record that uncertainty explicitly instead of smoothing it into a confirmed finding.

## Bundled References
- Read `references/repo-exposure-basics.md` when the request is about secrets in git, `.gitignore` gaps, mobile config files, service-account JSON, or lightweight pre-commit/pre-release gating.

## Primary Lens
- `primary_lens`: `nist-rmf`
- `why`: Security review should frame assets, controls, and monitoring needs systematically.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: security-report.v1

## Neutrality Rules
- Build the threat model before asserting vulnerability impact.
- If exploitability is uncertain, mark it as unverified rather than overstating certainty.
- Separate discovered vulnerabilities from hardening suggestions.
- Separate actual secret leaks from repo-hygiene and allowlist decisions.
- If a platform config file is often public client config, classify it from evidence rather than from filename alone.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Lead with the threat surface in one line: assets, attacker model, trust boundary.

Then list findings ordered by severity:
- P0 (critical) / P1 (high) / P2 (medium) — file:line — [issue] — exploitability: [confirmed/unverified]

Show exposure decisions separately:
- [file or token] → [secret / public-client-config / allowlisted / unverified] — [evidence]

End with: "Fix P0s before push, or need full mitigation plan?"

## Execution Constraints
- Do not invent vulnerabilities to satisfy a security-audit request; return an empty SECURITY_FINDINGS list when evidence does not support a finding.
- For `repo-exposure-review`, always inspect tracked sensitive paths, ignore drift, and diff-added credential material before suggesting broader hardening work.
- Do not treat Firebase client config files or Firebase API keys as confirmed secret leaks without evidence that they contain non-public credentials or violate explicit repo policy.
- Treat service account keys, private signing keys, long-lived access tokens, and production env files as high severity by default.
- Keep the report bounded to commit/release-relevant findings; do not turn the result into a generic security roadmap.
