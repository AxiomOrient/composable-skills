---
name: release-publish
description: "Use when a validated change set must be cleaned up, merged into the release branch as a release-only commit, tagged, and optionally published as a GitHub release. Do not use for release-risk judgement only; use ship-go-nogo or wf-ship-ready-check for GO/NO-GO analysis."
---

# Release Publish

## Purpose
Execute release preparation and publication with explicit cleanup, branch, tag, and publish evidence while keeping main release-only.

## Default Program
```text
[stages: preflight>detect>plan>review>handoff>audit |
 scope: repo |
 policy: evidence,safety-gates,quality-gates{docs,tests,registry,release},approval-gates{explicit,no-fallback},deterministic-output |
 lens: release-gatekeeper |
 output: md(contract=v1)]
```

## Use When
- Need to turn a validated dev branch into a release-only commit on the target branch.
- Need legacy removal, doc pruning, tag creation, and GitHub release publication handled as one explicit release run.
- Need the exact release evidence such as cleanup actions, commit refs, tag refs, and publish status recorded.
- Need low-level control over the publish stage after review has already been resolved elsewhere.

## Do Not Use When
- Need only release safety or rollout judgement; use ship-go-nogo or wf-ship-ready-check instead.
- Need the default end-to-end release flow; use wf-ship-it instead.
- Need normal implementation, debugging, or documentation authoring work.
- Cannot tolerate branch, tag, or remote mutation in the current run.

## Required Inputs
- `SOURCE_BRANCH` (string; required): Branch that holds the validated release candidate changes.
- `TARGET_BRANCH` (string; required): Branch that should receive the release-only commit.
- `RELEASE_BUMP` (patch|minor|explicit-tag; required; allowed: patch|minor|explicit-tag): Requested version bump policy.
- `RELEASE_TAG` (string; optional; required when RELEASE_BUMP=explicit-tag): Explicit tag to publish, such as v1.2.0.
- `REQUIRED_CHECKS` (list; optional; shape: {NAME, COMMAND, REQUIRED}): Checks that must pass before the release branch and tag are mutated.
- `PUBLISH_TARGET` (github|tag-only|local-only; optional; allowed: github|tag-only|local-only): Whether to stop at a local tag, push a tag only, or publish a GitHub release.
- `REMOTE_NAME` (string; optional): Remote to push the release branch and tag to. Default is origin.
- `LEGACY_CLEANUP_SCOPE` (list; optional; shape: {AREA, RULE}): Optional cleanup expectations such as removed legacy skills, deleted stale docs, or registry sync.
- `RELEASE_NOTES_SOURCE` (generate|path|string; optional; allowed: generate|path|string): How release notes should be sourced.
- `RELEASE_NOTES_PATH` (path; optional; required when RELEASE_NOTES_SOURCE=path): Path to release notes when using path mode.

## Input Contract Notes
- SOURCE_BRANCH should already contain all intended release content and a clean validation result before publication starts.
- TARGET_BRANCH is usually main when the project policy requires release-only commits on the primary branch.
- LEGACY_CLEANUP_SCOPE is for bounded release hygiene checks, not for open-ended product backlog cleanup.
- Release publication should start only after repository prechecks, docs gate, and ship-go-nogo judgement have already returned ready/pass/go.

## Structured Outputs
- `CLEANUP_REPORT` (list; required; shape: {AREA, ACTION, STATUS, EVIDENCE}): Release-hygiene actions such as legacy removal, stale-doc deletion, or registry synchronization.
- `RELEASE_COMMITS` (list; required; shape: {BRANCH, COMMIT, ROLE}): Recorded commits for the source branch and the release-only target branch commit.
- `PUBLISH_RESULTS` (list; required; shape: {TARGET, STATUS, REF}): Tag, push, and GitHub release outcomes.
- `RELEASE_STATUS` (prepared|published|blocked; required; allowed: prepared|published|blocked): Overall execution state after cleanup, branch sync, tag, and publish attempts.

## Output Contract Notes
- CLEANUP_REPORT should include explicit no-op entries when a release hygiene area was checked and nothing needed removal.
- RELEASE_COMMITS must distinguish the source-branch preparation commit from the target-branch release-only commit.
- PUBLISH_RESULTS must report partial completion honestly, such as local tag created but remote release blocked.

## Primary Lens
- `primary_lens`: `release-gatekeeper`
- `frame_name`: Repo-to-Release Gatekeeper
- `why`: Release publication should center on blast radius, rollback readiness, and truthful delivery-state evidence rather than optimistic shipping rituals.
- `summary`: Treat release as a sequence of explicit gates and judge only the gate in scope with concrete evidence.
- `thesis`: Release work becomes unsafe when repository facts, hygiene, readiness, and publication are collapsed into one blurry judgement. Name the gate in scope, verify it directly, and hand off unresolved gates explicitly.
- `core_philosophy`: Treat release as a chain of explicit gates. Check only the current gate, block on missing proof, and do not borrow confidence from adjacent gates.
- `mental_model`:
  - Name the exact release gate in scope before making any judgement.
  - Check only gate-specific evidence instead of mixing repository, hygiene, readiness, and publish signals together.
  - Use blocked or inconclusive when the current gate lacks proof instead of assuming a later gate will absorb the risk.
  - Hand off the next required release gate explicitly once the current gate is resolved.
- `decision_rules`:
  - Keep repository reality, hygiene, readiness, and publication in separate verdict buckets.
  - Judge the gate in scope from concrete evidence only.
  - Escalate missing required proof to blocked or inconclusive instead of optimistic release language.
  - Record the cheapest next gate or action rather than assuming downstream cleanup.
- `anti_patterns`:
  - Repository, docs, rollout, and publish claims merged into one verdict
  - Optimistic release language with unresolved gate evidence
  - Assuming success in one gate because a neighboring gate looks healthy
- `good_for`:
  - release repo checks
  - release hygiene gates
  - release readiness
  - release publication
- `not_for`:
  - feature implementation
  - broad product ideation
  - architecture cleanup unrelated to shipping
- `required_artifacts`:
  - Gate In Scope
  - Gate Evidence
  - Blocking Gap or Status
  - Next Gate or Action
- `references`:
  - https://dora.dev/
  - https://sre.google/sre-book/table-of-contents/

## Artifacts
- `artifacts_in`: release-repo-check-report.v1, release-hygiene-report.v1, release-decision.v1
- `artifacts_out`: release-publication-report.v1

## Neutrality Rules
- Do not report a release as published unless branch push, tag push, and release publication were actually confirmed.
- If a required check fails or branch policy cannot be satisfied, stop with blocked instead of forcing publication.
- Keep cleanup evidence separate from release safety judgement and from publish success claims.
- If docs gate or ship-go-nogo evidence says blocked, keep publication blocked.

## Execution Constraints
- Keep the target branch release-only by creating a single release commit there instead of replaying development history directly.
- Do not silently keep legacy surface, stale docs, or stale registry entries when the release explicitly aims to remove them.
- Do not publish when required docs are stale or missing.
- Prefer squash merge or equivalent single-commit release flow when the target branch policy requires a clean public release history.
- If the remote or release host is unavailable, record prepared or blocked state rather than inventing success.

## Mandatory Rules
- Run required checks before mutating the target branch or creating the final public tag.
- Record exact branch, tag, and publish refs in the final report.
- Do not use this utility as a substitute for release-risk analysis.

## Example Invocation
```text
$compose + $wf-ship-it + $check-delivered

TARGET_BRANCHES:
  - {BRANCH: codex/dev, ROLE: source}
  - {BRANCH: main, ROLE: target}
ROLLOUT_PLAN: staging 확인 후 production
ROLLBACK_PATH: git revert 후 재배포
REQUIRED_DOCS:
  - {PATH: skills/README.md, WHY_REQUIRED: user-facing release guide}
RELEASE_BUMP: explicit-tag
RELEASE_TAG: v1.0.0
REQUIRED_CHECKS:
  - {NAME: validate, COMMAND: ./scripts/validate.sh, REQUIRED: true}
  - {NAME: diff-check, COMMAND: git diff --check, REQUIRED: true}
PUBLISH_TARGET: github
RELEASE_NOTES_SOURCE: generate
```

## Output Discipline
- `response_profile=generic`
- User-facing rendering is delegated to `respond`.
