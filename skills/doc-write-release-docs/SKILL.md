---
name: doc-write-release-docs
description: "Produce or refresh release-facing docs such as release notes, changelog entries, upgrade notes, migration guides, compatibility notes, and rollback summaries from concrete release evidence. Use when preparing or shipping a release. Do not mutate git refs, publish releases, or judge rollout GO/NO-GO."
---

# Doc / Write Release Docs

## Purpose
Write release-facing documentation that explains what changed, who is affected, what action is required, and how to move safely.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat,release},deterministic-output |
 lens: release-gatekeeper |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `release-gatekeeper` because release docs should describe only the verified release slice, its user impact, and the actions readers must take.

## Use When
- Need release notes, changelog entries, upgrade notes, migration docs, compatibility notes, or rollback summaries.
- Need one release-doc writer that can handle both user-facing and operator-facing release documents.
- Need to document the current release from concrete change evidence.

## Do Not Use When
- Need git branch, tag, or GitHub release mutation.
- Need rollout GO/NO-GO judgement.
- Need generic non-release documentation.
- Need recursive folder docsets or repo root README publication.

## Required Inputs
- `RELEASE_SCOPE` (diff|tag|version|repo|deployment-slice; required): Release slice being documented.
- `RELEASE_DOC_GOAL` (release-note|changelog-entry|upgrade-note|migration-guide|compatibility-note|rollback-note|mixed; required): Release documentation objective.
- `AUDIENCE` (user|developer|operator|maintainer|mixed; required): Primary release-doc audience.
- `RELEASE_VERSION` (string; optional): Version, tag, or release label to name in the docs when known.
- `BREAKING_CHANGE_POLICY` (highlight-all|highlight-breaking-only|none; optional): How prominently to surface compatibility-impact changes. Defaults to `highlight-all` when omitted.
- `RELEASE_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Diff, tag, issues, PRs, tests, commands, or docs supporting the release claims.

## Input Contract Notes
- RELEASE_SCOPE should stay bounded to the actual release candidate under discussion.
- Use release-note or changelog-entry for what changed, and upgrade-note or migration-guide for what the reader must do.
- Release-facing docs may include dates, versions, and current-release wording when the document is explicitly a release artifact.

## Structured Outputs
- `RELEASE_DOCS` (list; required; shape: {PATH, KIND, AUDIENCE, COVERAGE}): Release-facing docs created or updated.
- `CHANGE_SUMMARY` (list; required; shape: {CHANGE, IMPACT, EVIDENCE}): Verified changes included in the release docs.
- `BREAKING_CHANGE_SET` (list; required; shape: {CHANGE, USER_IMPACT, REQUIRED_ACTION}): Compatibility-impact changes and what readers must do.
- `DOC_GAPS` (list; required; shape: {GAP, NEEDED_SOURCE}): Missing release evidence that prevents accurate docs.

## Output Contract Notes
- CHANGE_SUMMARY should separate user-visible change, operational change, and internal-only cleanup when the audience mix requires it.
- BREAKING_CHANGE_SET may be empty when the release has no compatibility impact.
- DOC_GAPS should block unsupported claims instead of being smoothed over with vague prose.

## Primary Lens
- `primary_lens`: `release-gatekeeper`
- `why`: Release docs are safety artifacts; they must describe the real release slice, not aspirational change lists.

## Artifacts
- `artifacts_in`: doc-inventory.v2
- `artifacts_out`: release-doc-package.v1

## Neutrality Rules
- Do not invent migration steps, rollback steps, or user impact.
- Keep internal cleanup separate from user-visible changes.
- If a release has uncertain impact, say so explicitly and record a doc gap.

## Execution Constraints
- Do not mutate branches, tags, remotes, or release hosts from this skill.
- Document only the release in scope, not speculative future work.
- Make required action explicit for any breaking or migration-relevant change.
