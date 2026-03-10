---
name: workflow-ship-ready-check
description: "Workflow skill that verifies repository reality, release hygiene, and final release readiness before publication. Use when the user wants a transparent release review instead of a single vague 'can we ship?' prompt."
---

# Workflow / Ship Ready Check

## Purpose

Compose repository prechecks, release hygiene gates, security preflight, and GO/NO-GO release judgement into one explicit release review workflow.

## Default Program

```text
[stages: preflight>detect>analyze>plan>review>handoff>audit | scope: repo|diff | policy: evidence,safety-gates,quality-gates{docs,release,tests,security},deterministic-output | lens: release-gatekeeper | output: md(contract=v1)]
```

## Use When

- Need release review built from explicit repository, hygiene, and readiness subchecks.
- Need repo-exposure and secret-leak gates checked before shipping.
- Need document-upgrade and legacy-removal gates checked before shipping.
- Need a named release-review workflow that can still be extended with check-final-verify or release-publish.
- Need release judgement only, while keeping branch, tag, and publish mutation outside the current run.

## Do Not Use When

- Need direct branch, tag, or GitHub release mutation; use release-publish instead.
- Need the default review-plus-publish release flow; use workflow-ship-it instead.
- Need only one narrow release concern rather than a combined release review.
- Need runtime implementation or debugging rather than release gating.

## Required Inputs

- `RELEASE_SCOPE` (diff|repo|deployment-slice; optional; allowed: diff|repo|deployment-slice): Release slice to judge after repository and hygiene gates are checked. Defaults to `repo` when omitted.
- `TARGET_BRANCHES` (list; required; shape: {BRANCH, ROLE}): Branches involved in the release, such as source/dev and target/main.
- `HYGIENE_SCOPE` (diff|repo; optional; allowed: diff|repo): Scope for release hygiene checks. Defaults to `repo` when omitted.
- `ROLLOUT_PLAN` (string; required): Intended rollout path.
- `ROLLBACK_PATH` (string; required): Rollback or stop strategy.
- `REQUIRED_DOCS` (list; optional; shape: {PATH, WHY_REQUIRED}): Release-blocking docs that must be upgraded and kept public after the release.
- `LEGACY_PATTERNS` (list; optional; shape: {PATTERN, WHY_BLOCKING}): Legacy names or files that must not survive the release, including temporary implementation docs when they are delivery-only artifacts.
- `REMOTE_NAME` (string; optional): Remote expected to receive release refs when publish is likely to follow.
- `TAG_INTENT` (string; optional): Candidate version tag to check during repo and release review.
- `KNOWN_GATES` (list; optional; shape: {GATE, STATUS, EVIDENCE}): Known release gate signals.
- `SURFACE_CONTRACTS` (list; optional; shape: {CONTRACT, SOURCE}): Public-surface contracts such as registry/docs parity or root README ownership.

## Input Contract Notes

- TARGET_BRANCHES should identify real release branch roles before the workflow runs.
- RELEASE_SCOPE should match the actual candidate being judged; do not overload HYGIENE_SCOPE to imply rollout scope.
- When RELEASE_SCOPE or HYGIENE_SCOPE is omitted, default to `repo`.
- Use REQUIRED_DOCS only for docs that block shipping when stale or missing.
- Put delivery-only planning docs such as `plans/IMPLEMENTATION-PLAN.md` and `plans/TASKS.md` in `LEGACY_PATTERNS`, not `REQUIRED_DOCS`, so the review can block on deleting them before release.
- Use SURFACE_CONTRACTS when release hygiene depends on explicit public-surface rules instead of implicit taste.
- This workflow composes explicit release subchecks; it should not hide them behind a single opaque verdict.

## Structured Outputs

- `REPO_RELEASE_STATUS` (ready|blocked|inconclusive; required; allowed: ready|blocked|inconclusive): Repository precondition status.
- `HYGIENE_SUMMARY` (list; required; shape: {AREA, STATUS, EVIDENCE}): Release hygiene summary including docs and public-surface sync.
- `CHECK_REPORTS` (list; required; shape: {CHECK, SUMMARY, OUTPUT_REF}): Underlying repo, hygiene, security, and readiness subcheck reports that support the final release decision.
- `RELEASE_DECISION` (go|no-go|blocked; required; allowed: go|no-go|blocked): Final release judgement.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Actual atomic path executed by the workflow.

## Output Contract Notes

- HYGIENE_SUMMARY should expose docs and public-surface gate status explicitly instead of hiding them inside prose.
- CHECK_REPORTS should preserve the underlying repo, hygiene, and readiness subcheck identities.
- RELEASE_DECISION should remain traceable to both readiness evidence and the explicit subchecks.
- EXPANDED_ATOMIC_PATH must preserve actual workflow order.

## Artifacts

- `artifacts_in`: none
- `artifacts_out`: release-review-report.v1

## Neutrality Rules

- Preserve the neutrality rules of the underlying repository, hygiene, security, and readiness checks.
- Do not invent blockers when underlying subchecks are clean.
- Expose release review as the sum of explicit subchecks.

## Execution Constraints

- Do not mutate branches, tags, remotes, or release hosts from this workflow.
- If a required subcheck cannot be verified, surface that gap instead of pretending full release coverage.
- Keep document gate status explicit because stale docs can block release.

## Mandatory Rules

- Expose repository, hygiene, and readiness subchecks explicitly.
- Treat missing release docs as a real gate when REQUIRED_DOCS says they are blocking.
- Treat security-preflight blockers as real release blockers when the repo is about to ship.

## Expansion

- `$ship-check-repo`
- `$ship-check-hygiene`
- `$workflow-security-preflight`
- `$ship-release-verdict`

## Example Invocation

```text
$workflow-ship-ready-check
RELEASE_SCOPE: repo
TARGET_BRANCHES:
  - {BRANCH: codex/dev, ROLE: source}
  - {BRANCH: main, ROLE: target}
HYGIENE_SCOPE: repo
ROLLOUT_PLAN: verify in staging, then roll out to production
ROLLBACK_PATH: git revert and redeploy
LEGACY_PATTERNS:
  - {PATTERN: ^plans/IMPLEMENTATION-PLAN\\.md$, WHY_BLOCKING: delivery-only implementation docs must not ship}
  - {PATTERN: ^plans/TASKS\\.md$, WHY_BLOCKING: delivery-only task ledgers must not ship}
```
