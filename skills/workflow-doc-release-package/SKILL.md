---
name: workflow-doc-release-package
description: "Workflow skill that inventories the current docs surface and writes or refreshes release-facing docs such as release notes, changelog entries, upgrade notes, and migration guides. Use when the user wants one release-doc entrypoint instead of manually chaining inventory and release-doc writing."
---

# Workflow / Doc Release Package

## Purpose
Compose documentation inventory and release-doc writing into one default workflow for release-facing documentation.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat,release},deterministic-output |
 lens: release-gatekeeper |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `release-gatekeeper` because release docs should cover only the verified release slice, its impact, and any required action.

## Use When
- Need release notes, changelog entries, upgrade docs, migration docs, compatibility notes, or rollback summaries.
- Need one workflow that checks the current docs surface before authoring release docs.
- Need release documentation without mutating git refs or publishing releases.

## Do Not Use When
- Need rollout GO/NO-GO judgement or release publication.
- Need generic non-release documentation.
- Need repo root README publication.
- Need lifecycle governance of the entire docs surface.

## Required Inputs
- `RELEASE_SCOPE` (diff|tag|version|repo|deployment-slice; required): Release slice being documented.
- `RELEASE_DOC_GOAL` (release-note|changelog-entry|upgrade-note|migration-guide|compatibility-note|rollback-note|mixed; required): Release documentation objective.
- `AUDIENCE` (user|developer|operator|maintainer|mixed; required): Primary release-doc audience.
- `RELEASE_VERSION` (string; optional): Version, tag, or release label to name in the docs when known.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Constraints such as required doc paths, excluded audiences, or exact sections.

## Structured Outputs
- `RELEASE_DOCS` (list; required; shape: {PATH, KIND, AUDIENCE, COVERAGE}): Release-facing docs created or updated.
- `CHANGE_SUMMARY` (list; required; shape: {CHANGE, IMPACT, EVIDENCE}): Verified changes included in the docs.
- `BREAKING_CHANGE_SET` (list; required; shape: {CHANGE, USER_IMPACT, REQUIRED_ACTION}): Breaking or migration-relevant changes.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Atomic path executed by the workflow.

## Execution Constraints
- Inventory first so existing release docs and canonical release surfaces are not overwritten blindly.
- Keep unsupported release claims out; record doc gaps instead.
- Do not widen this workflow into release publication or rollout judgement.

## Expansion
- `$doc-find-all`
- `$doc-write-release-docs`
