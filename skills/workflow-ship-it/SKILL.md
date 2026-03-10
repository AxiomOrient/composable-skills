---
name: workflow-ship-it
description: "Workflow skill that runs repository checks, release hygiene, release readiness, and then the release-only commit/tag/publish flow as one explicit control workflow. Use when the user wants release preparation and publication without manually chaining review and publish skills."
---

# Workflow / Ship It

## Purpose

Compose repository prechecks, release hygiene, security preflight, release judgement, and release publication into one explicit release control workflow.

## Default Program

```text
[stages: preflight>detect>analyze>plan>review>handoff>audit | scope: repo | policy: evidence,safety-gates,quality-gates{docs,release,tests,security},approval-gates{explicit,no-fallback},deterministic-output | lens: release-gatekeeper | output: md(contract=v1)]
```

## Use When

- Need one explicit release control flow instead of manually chaining `workflow-ship-ready-check` and `release-publish`.
- Need repo checks, hygiene gates, release-only commit policy, tag creation, and publish status handled as one explicit flow.
- Need security preflight to run before the release decision and publication steps.
- Need `TARGET_BRANCHES` to be the single branch source of truth for both review and publish phases.

## Do Not Use When

- Need only release judgement without any branch or tag mutation; use `workflow-ship-ready-check` instead.
- Need only low-level publish execution after some other gate system already ran; use `release-publish` instead.
- Cannot tolerate branch, tag, or remote mutation in the current run.

## Required Inputs

- `TARGET_BRANCHES` (list; required; shape: {BRANCH, ROLE}): Branches involved in the release, such as source/dev and target/main.
- `ROLLOUT_PLAN` (string; required): Intended rollout path.
- `ROLLBACK_PATH` (string; required): Rollback or stop strategy.
- `RELEASE_BUMP` (patch|minor|explicit-tag; required; allowed: patch|minor|explicit-tag): Requested version bump policy.
- `RELEASE_TAG` (string; optional; required when RELEASE_BUMP=explicit-tag): Explicit tag to publish, such as `v1.0.0`.
- `RELEASE_SCOPE` (diff|repo|deployment-slice; optional; allowed: diff|repo|deployment-slice): Release slice to judge. Defaults to `repo`.
- `HYGIENE_SCOPE` (diff|repo; optional; allowed: diff|repo): Scope for release hygiene checks. Defaults to `repo`.
- `REQUIRED_DOCS` (list; optional; shape: {PATH, WHY_REQUIRED}): Release-blocking docs that must be upgraded and kept public after the release.
- `LEGACY_PATTERNS` (list; optional; shape: {PATTERN, WHY_BLOCKING}): Legacy names or files that must not survive the release, including temporary implementation docs when they are delivery-only artifacts.
- `SURFACE_CONTRACTS` (list; optional; shape: {CONTRACT, SOURCE}): Public-surface contracts such as skill-metadata/docs parity or root README ownership.
- `KNOWN_GATES` (list; optional; shape: {GATE, STATUS, EVIDENCE}): Known release gate signals.
- `REQUIRED_CHECKS` (list; optional; shape: {NAME, COMMAND, REQUIRED}): Checks that must pass before the release branch and tag are mutated.
- `PUBLISH_TARGET` (github|tag-only|local-only; optional; allowed: github|tag-only|local-only): Whether to stop at a local tag, push a tag only, or publish a GitHub release.
- `REMOTE_NAME` (string; optional): Remote expected to receive release refs. Default is origin.
- `RELEASE_NOTES_SOURCE` (generate|path|string; optional; allowed: generate|path|string): How release notes should be sourced.
- `RELEASE_NOTES_PATH` (path; optional; required when RELEASE_NOTES_SOURCE=path): Path to release notes when using path mode.

## Input Contract Notes

- `TARGET_BRANCHES` must include one `{ROLE: source}` and one `{ROLE: target}`. The workflow derives `SOURCE_BRANCH` and `TARGET_BRANCH` for the publish phase from that one input.
- `RELEASE_SCOPE` and `HYGIENE_SCOPE` default to `repo` when omitted because this workflow is meant to be the simplest explicit end-to-end release control flow.
- Use this workflow when the public branch policy matters. It keeps `main` release-only by routing publication through `release-publish`.
- If only the candidate tag is fixed and the rest should stay standard, prefer `RELEASE_BUMP=explicit-tag` with `RELEASE_TAG` rather than bypassing the workflow.
- Keep temporary implementation docs such as `plans/IMPLEMENTATION-PLAN.md` and `plans/TASKS.md` out of `REQUIRED_DOCS`; model them under `LEGACY_PATTERNS` so the release stays explicit about deleting them.

## Structured Outputs

- `CHECK_REPORTS` (list; required; shape: {CHECK, SUMMARY, OUTPUT_REF}): Underlying repo, hygiene, security, readiness, and publish stage reports.
- `RELEASE_DECISION` (go|no-go|blocked; required; allowed: go|no-go|blocked): Final release judgement before publication.
- `CLEANUP_REPORT` (list; required; shape: {AREA, ACTION, STATUS, EVIDENCE}): Release-hygiene actions such as legacy removal, stale-doc deletion, or public-surface synchronization.
- `RELEASE_COMMITS` (list; required; shape: {BRANCH, COMMIT, ROLE}): Recorded commits for the source branch and the release-only target branch commit.
- `PUBLISH_RESULTS` (list; required; shape: {TARGET, STATUS, REF}): Tag, push, and GitHub release outcomes.
- `RELEASE_STATUS` (prepared|published|blocked; required; allowed: prepared|published|blocked): Overall execution state after checks, branch sync, tag, and publish attempts.
- `EXPANDED_EXECUTION_PATH` (list; required; shape: {SKILL}): Actual execution path used by the workflow.

## Output Contract Notes

- `CHECK_REPORTS` should preserve the repo, hygiene, readiness, and publish stage identities instead of collapsing them into a single paragraph.
- `RELEASE_DECISION` must stay traceable to the review stages even when publication later fails.
- `RELEASE_STATUS` must report prepared or blocked honestly when review passes but publish cannot finish.
- `EXPANDED_EXECUTION_PATH` must preserve actual workflow order and include `release-publish` at the end.

## Artifacts

- `artifacts_in`: none
- `artifacts_out`: release-ship-report.v1

## Neutrality Rules

- Preserve the neutrality rules of the underlying repository, hygiene, security, readiness, and publication skills.
- Do not bypass a blocked review gate just because publication inputs are present.
- Do not report a release as published unless branch push, tag push, and release publication were actually confirmed.

## Execution Constraints

- Derive publish branch inputs from `TARGET_BRANCHES`; do not require the user to repeat them in the same request.
- Keep the target branch release-only by delegating publication to `release-publish`.
- If repo, hygiene, or readiness gates block the release, stop before mutating branches, tags, remotes, or release hosts.
- If docs or public-surface cleanup is part of the release contract, keep publication blocked until those checks pass.

## Mandatory Rules

- Use `TARGET_BRANCHES` as the single branch source of truth for both review and publish stages.
- Run required checks before mutating the target branch or creating the final public tag.
- Record exact branch, tag, and publish refs in the final report.

## Expansion

- `$ship-check-repo`
- `$ship-check-hygiene`
- `$workflow-security-preflight`
- `$ship-release-verdict`
- `$release-publish`

## Example Invocation

```text
$compose + $workflow-ship-it + $check-final-verify

TARGET_BRANCHES:
  - {BRANCH: codex/dev, ROLE: source}
  - {BRANCH: main, ROLE: target}
ROLLOUT_PLAN: verify in staging, then roll out to production
ROLLBACK_PATH: git revert and redeploy
RELEASE_BUMP: explicit-tag
RELEASE_TAG: v1.0.0
REQUIRED_DOCS:
  - {PATH: skills/README.md, WHY_REQUIRED: user-facing release guide}
LEGACY_PATTERNS:
  - {PATTERN: ^plans/IMPLEMENTATION-PLAN\\.md$, WHY_BLOCKING: delivery-only implementation docs must not ship}
  - {PATTERN: ^plans/TASKS\\.md$, WHY_BLOCKING: delivery-only task ledgers must not ship}
REQUIRED_CHECKS:
  - {NAME: validate, COMMAND: python3 scripts/skills.py validate, REQUIRED: true}
  - {NAME: diff-check, COMMAND: git diff --check, REQUIRED: true}
PUBLISH_TARGET: github
RELEASE_NOTES_SOURCE: generate
```
