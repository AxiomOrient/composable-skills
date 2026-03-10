---
name: workflow-security-preflight
description: "Workflow skill that runs a lightweight security gate before a GitHub commit or release. Use when you want secret-leak, ignore-drift, or mobile-config review without broad security hardening work."
---

# Workflow / Security Preflight

## Purpose
Run a lightweight security gate before a GitHub commit or release.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: diff|repo|paths(glob,...) | policy: evidence,safety-gates,quality-gates{security,git,hygiene},deterministic-output | lens: nist-rmf | output: md(contract=v1)]
```

## Use When
- Need a quick security pass before pushing to GitHub or cutting a release.
- Need to catch secret files, ignore drift, tracked-sensitive-file mistakes, or platform config exposure with minimal development friction.
- Need a named workflow that can compose with `ship-commit`, `workflow-ship-ready-check`, or `workflow-ship-it`.

## Do Not Use When
- Need a full threat model or deep vulnerability assessment; use `check-security-holes` directly.
- Need implementation of the fixes instead of review.
- Need always-on IDE or CI policy enforcement during every development edit.

## Required Inputs
- `SECURITY_STAGE` (github-commit|release; optional; allowed: github-commit|release): When the gate runs. Defaults to `github-commit` unless release intent is explicit.
- `TARGET_SCOPE` (diff|repo; optional; allowed: diff|repo): Scope to inspect. Defaults to `diff` for commit and `repo` for release.
- `SENSITIVE_SURFACES` (list; optional; shape: {SURFACE, WHY_RELEVANT}): Files, directories, vendors, or boundaries to prioritize.
- `KNOWN_ALLOWED_PUBLIC_CONFIGS` (list; optional; shape: {PATTERN_OR_FILE, WHY_ALLOWED}): Explicit allowlist for intentionally tracked public client config such as build-required Firebase plist/json files.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Existing scan results, alerts, or prior decisions.

## Input Contract Notes
- If `TARGET_SCOPE` is omitted, default to `diff` for `github-commit` and `repo` for `release` to keep the gate lightweight.
- Use `KNOWN_ALLOWED_PUBLIC_CONFIGS` for intentional public client config only. It must not be used to wave through real secret material.
- Keep `SENSITIVE_SURFACES` focused on likely leak surfaces rather than every path in the repository.

## Structured Outputs
- `SECURITY_GATE_STATUS` (pass|blocked|inconclusive; required; allowed: pass|blocked|inconclusive): Overall gate result.
- `SECURITY_FINDINGS` (list; required; shape: {SEVERITY, ISSUE, LOCATION, EVIDENCE, ACTION}): Blocking or noteworthy exposure findings.
- `ALLOWLIST_DECISIONS` (list; required; shape: {ITEM, STATUS, REASON}): Decisions for public client config or other intentional exceptions.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Actual atomic path executed by the workflow.

## Output Contract Notes
- `SECURITY_GATE_STATUS` should be `blocked` when concrete secret exposure or tracked-sensitive-file leakage exists.
- Use `inconclusive` when vendor file sensitivity or repo policy cannot be verified from evidence.
- `ALLOWLIST_DECISIONS` should explain why a client config file is acceptable or why it still needs action.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: security-gate-report.v1

## Neutrality Rules
- Preserve the neutrality rules of `check-security-holes`.
- Prefer a small set of actionable blockers over a broad hardening backlog.
- Treat allowlist decisions as evidence-backed classification, not as wishful exceptions.

## Execution Constraints
- Keep the gate lightweight and commit/release focused.
- Check both file content patterns and repo mechanics such as `.gitignore` and tracked status before declaring the repo safe.
- If a file is build-required but usually public client config, request or infer an allowlist decision instead of auto-blocking from filename alone.

## Mandatory Rules
- Differentiate public mobile client config from server credentials.
- Block on concrete credential exposure before GitHub commit or release.

## Expansion
- `$check-security-holes`

## Example Invocation
```text
$compose + $workflow-security-preflight + $ship-commit
SECURITY_STAGE: github-commit
TARGET_SCOPE: diff
SENSITIVE_SURFACES:
  - {SURFACE: ios/App/GoogleService-Info.plist, WHY_RELEVANT: build-required Firebase config is easy to commit by accident}
  - {SURFACE: .env.production, WHY_RELEVANT: production env files can carry real credentials}
KNOWN_ALLOWED_PUBLIC_CONFIGS:
  - {PATTERN_OR_FILE: ios/App/GoogleService-Info.plist, WHY_ALLOWED: build requires a Firebase client config file and repo policy allows the non-secret version only}
```
