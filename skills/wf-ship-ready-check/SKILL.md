---
name: wf-ship-ready-check
description: "Workflow skill that verifies repository reality, release hygiene, and final release readiness before publication. Use when the user wants a transparent release review instead of a single vague 'can we ship?' prompt."
---

# Release Check Workflow

## Purpose
Compose repository prechecks, release hygiene gates, and GO/NO-GO release judgement into one explicit release review workflow.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit | scope: repo|diff | policy: evidence,safety-gates,quality-gates{docs,release,tests,security},deterministic-output | lens: release-gatekeeper | output: md(contract=v1)]
```

## Use When
- Need release review built from explicit repository, hygiene, and readiness subchecks.
- Need document-upgrade and legacy-removal gates checked before shipping.
- Need a named release-review workflow that can still be extended with check-delivered or release-publish.
- Need release judgement only, while keeping branch, tag, and publish mutation outside the current run.

## Do Not Use When
- Need direct branch, tag, or GitHub release mutation; use release-publish instead.
- Need the default review-plus-publish release flow; use wf-ship-it instead.
- Need only one narrow release concern rather than a combined release review.
- Need runtime implementation or debugging rather than release gating.

## Required Inputs
- `RELEASE_SCOPE` (diff|repo|deployment-slice; required; allowed: diff|repo|deployment-slice): Release slice to judge after repository and hygiene gates are checked.
- `TARGET_BRANCHES` (list; required; shape: {BRANCH, ROLE}): Branches involved in the release, such as source/dev and target/main.
- `HYGIENE_SCOPE` (diff|repo; required; allowed: diff|repo): Scope for release hygiene checks.
- `ROLLOUT_PLAN` (string; required): Intended rollout path.
- `ROLLBACK_PATH` (string; required): Rollback or stop strategy.
- `REQUIRED_DOCS` (list; optional; shape: {PATH, WHY_REQUIRED}): Release-blocking docs that must be upgraded.
- `LEGACY_PATTERNS` (list; optional; shape: {PATTERN, WHY_BLOCKING}): Legacy names or files that must not survive the release.
- `REMOTE_NAME` (string; optional): Remote expected to receive release refs when publish is likely to follow.
- `TAG_INTENT` (string; optional): Candidate version tag to check during repo and release review.
- `KNOWN_GATES` (list; optional; shape: {GATE, STATUS, EVIDENCE}): Known release gate signals.
- `SURFACE_CONTRACTS` (list; optional; shape: {CONTRACT, SOURCE}): Public-surface contracts such as registry/docs parity or root README ownership.

## Input Contract Notes
- TARGET_BRANCHES should identify real release branch roles before the workflow runs.
- RELEASE_SCOPE should match the actual candidate being judged; do not overload HYGIENE_SCOPE to imply rollout scope.
- Use REQUIRED_DOCS only for docs that block shipping when stale or missing.
- Use SURFACE_CONTRACTS when release hygiene depends on explicit public-surface rules instead of implicit taste.
- This workflow composes explicit release subchecks; it should not hide them behind a single opaque verdict.

## Structured Outputs
- `REPO_RELEASE_STATUS` (ready|blocked|inconclusive; required; allowed: ready|blocked|inconclusive): Repository precondition status.
- `HYGIENE_SUMMARY` (list; required; shape: {AREA, STATUS, EVIDENCE}): Release hygiene summary including docs and public-surface sync.
- `CHECK_REPORTS` (list; required; shape: {CHECK, SUMMARY, OUTPUT_REF}): Underlying subcheck reports that support the final release decision.
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
- Preserve the neutrality rules of the underlying repository, hygiene, and readiness checks.
- Do not invent blockers when underlying subchecks are clean.
- Expose release review as the sum of explicit subchecks.

## Execution Constraints
- Do not mutate branches, tags, remotes, or release hosts from this workflow.
- If a required subcheck cannot be verified, surface that gap instead of pretending full release coverage.
- Keep document gate status explicit because stale docs can block release.

## Mandatory Rules
- Expose repository, hygiene, and readiness subchecks explicitly.
- Treat missing release docs as a real gate when REQUIRED_DOCS says they are blocking.

## Expansion
- `$ship-check-repo`
- `$ship-check-hygiene`
- `$ship-go-nogo`

## Example Invocation
```text
$wf-ship-ready-check
RELEASE_SCOPE: repo
TARGET_BRANCHES:
  - {BRANCH: codex/dev, ROLE: source}
  - {BRANCH: main, ROLE: target}
HYGIENE_SCOPE: repo
ROLLOUT_PLAN: staging 확인 후 production
ROLLBACK_PATH: git revert 후 재배포
```

## Output Discipline
- `response_profile=release_decision`
- User-facing rendering is delegated to `respond`.
