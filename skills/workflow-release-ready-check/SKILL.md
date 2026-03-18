---
name: workflow-release-ready-check
description: "Workflow skill that verifies repository reality, release hygiene, and final release readiness before publication. Use when the user wants a transparent release review instead of a single vague 'can we ship?' prompt."
---

# Workflow / Release Ready Check

## Purpose

Compose repository prechecks, release hygiene gates, security preflight, and GO/NO-GO release judgement into one explicit release review workflow.

## Default Program

```text
[stages: preflight>detect>analyze>plan>review>handoff>audit | scope: repo|diff | policy: evidence,safety-gates,quality-gates{docs,release,tests,security},deterministic-output | lens: release-gatekeeper | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `release-gatekeeper` because it keeps the work aligned with: Treat release as a sequence of explicit gates and judge only the gate in scope with concrete evidence.

## Use When

- Need release review built from explicit repository, hygiene, and readiness subchecks.
- Need repo-exposure and secret-leak gates checked before shipping.
- Need document-upgrade and legacy-removal gates checked before shipping.
- Need a named release-review workflow that can still be extended with review-final-verify or release-publish.
- Need release judgement only, while keeping branch, tag, and publish mutation outside the current run.

## Do Not Use When

- Need direct branch, tag, or GitHub release mutation; use release-publish instead.
- Need the default review-plus-publish release flow; use control-release-publish-flow instead.
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

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Lead with release decision: 출시 가능 / 출시 불가 / 중단.

Show per-step outcome (step → result):
- release-check-repo → 준비됨 / 중단
- release-check-hygiene → doc gate + surface sync
- review-security → 통과 / 중단
- release-verdict → 출시 가능 / 출시 불가 / 중단

List any blockers with severity and what resolves each.

On GO: "All gates passed — ready to publish." No further question needed.

## Mandatory Rules

- Expose repository, hygiene, and readiness subchecks explicitly.
- Treat missing release docs as a real gate when REQUIRED_DOCS says they are blocking.
- Treat security-preflight blockers as real release blockers when the repo is about to ship.

## Expansion

- `$release-check-repo`
- `$release-check-hygiene`
- `$review-security`
- `$release-verdict`

## Example Invocation

```text
$workflow-release-ready-check
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

## Eval Cases

| Prompt | Should Trigger | Key Output Check |
|--------|---------------|-----------------|
| 배포하기 전에 보안이나 문서, 레포 상태 다 괜찮은지 최종 확인해줘. | YES | RELEASE_DECISION 존재 |
| 출시해도 될지 GO/NO-GO 판정 좀 내려봐. | YES | HYGIENE_SUMMARY 존재 |
| 태그 달고 릴리즈 생성해줘. | NO | 판정 전용 워크플로우 — release-publish 권장 |
