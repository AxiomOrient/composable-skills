---
name: review-security
description: "Run a bounded security review for repo exposure, vulnerability risk, or mitigation verification with prioritized findings. Use when security-specific judgement is needed."
---

# Review / Security

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

## Do Not Use When
- Need always-on development policing or a broad hardening backlog.
- Need general debugging or performance analysis.
- Need direct implementation.
- Need broad review or release judgement instead of security-specific output.

## Required Inputs
- `SECURITY_GOAL` (audit|repo-exposure-review|threat-model|mitigation-verify; required): Security objective.
- `TARGET_SCOPE` (file|module|service|repo|diff; required): Scope to inspect.
- `REVIEW_STAGE` (github-commit|release|general; optional; allowed: github-commit|release|general): Delivery stage that triggered the review.
- `SENSITIVE_SURFACES` (list; optional; shape: {SURFACE, WHY_RELEVANT}): Assets, trust boundaries, config files, ignore targets, or entrypoints to prioritize.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Scans, prior findings, logs, or threat notes.

## Input Contract Notes
- Use `repo-exposure-review` for lightweight commit or release gating rather than full threat modelling.
- SENSITIVE_SURFACES can name assets, trust boundaries, config files, ignore targets, or suspected leak surfaces.
- KNOWN_EVIDENCE should cite existing scans, logs, or prior findings only; do not preload vulnerability conclusions.
- When a file format is vendor-specific or its sensitivity is ambiguous, confirm against official docs before calling it a leak.

## Structured Outputs
- `THREAT_MODEL` (object; required): Assets, attacker model, boundaries, and entrypoints.
- `SECURITY_FINDINGS` (list; required; shape: {SEVERITY, ISSUE, LOCATION, EVIDENCE, EXPLOITABILITY, ACTION}): Prioritized vulnerability or exposure findings.
- `MITIGATION_VERIFICATION` (list; required; shape: {CONTROL_OR_MITIGATION, STATUS, EVIDENCE}): Mitigation checks or verification results.
- `EXPOSURE_DECISIONS` (list; required; shape: {ITEM, CLASSIFICATION, EVIDENCE, ACTION}): Classification of reviewed files or tokens.
- `SECURITY_STATUS` (safe|at-risk|blocked; required; allowed: safe|at-risk|blocked): Overall security review state.

## Output Contract Notes
- SECURITY_FINDINGS may be empty when the threat model and available evidence do not support a concrete vulnerability claim.
- Use MITIGATION_VERIFICATION for hardening checks or control status instead of presenting every improvement idea as a vulnerability.
- Use EXPOSURE_DECISIONS to separate actual secret leaks from intentionally tracked public config or false positives.
- If exploitability or sensitivity is uncertain, record that uncertainty explicitly instead of smoothing it into a confirmed finding.

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

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

위험 표면 한 줄:
- 자산 / 공격자 / 신뢰 경계

발견사항은 심각도 순서:
- 긴급 / 중요 / 참고 — `file:line` — [문제] — exploitability: [confirmed/unverified]

노출 분류는 따로:
- [file or token] → [secret / public-client-config / allowlisted / unverified] — [근거]

끝에: "긴급부터 막을까요, 아니면 전체 대응 순서를 먼저 볼까요?"

## Execution Constraints
- Do not invent vulnerabilities to satisfy a security-audit request; return an empty SECURITY_FINDINGS list when evidence does not support a finding.
- For `repo-exposure-review`, always inspect tracked sensitive paths, ignore drift, and diff-added credential material before suggesting broader hardening work.
- Do not treat public client config as a confirmed secret leak without evidence that it contains non-public credentials or violates explicit repo policy.

## Example Invocation
```text
$review-security
SECURITY_GOAL: repo-exposure-review
TARGET_SCOPE: ./
REVIEW_STAGE: release
```
