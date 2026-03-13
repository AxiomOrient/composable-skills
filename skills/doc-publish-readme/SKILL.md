---
name: doc-publish-readme
description: "Create or refresh the repo root README as a GitHub-friendly project entrypoint, then publish easy-to-read localized entry docs under /i18n/<lang>/. Use when the target is the repository root landing page. Folder-level README or index pages below the root belong to doc-build-index. Release-facing docs belong to doc-write-release-docs."
---

# Doc / Publish README

## Purpose
Publish the project root README and localized project entry docs with audience-level, plain-language explanations.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: repo |
 policy: evidence,quality-gates{docs,compat},deterministic-output |
 lens: feynman-teaching |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `feynman-teaching` because it keeps the work aligned with: Start from the simplest correct mental model, translate jargon into plain words, and add concrete examples before deeper detail.

## Use When
- Need to create or refresh the repo root README.
- Need GitHub-style project onboarding with links to deeper docs.
- Need localized project entry docs under a stable language folder.

## Do Not Use When
- Need only non-root guide writing.
- Need folder-level README or index pages below the repo root.
- Need release notes, changelog entries, or migration docs.
- Need documentation inventory or lifecycle cleanup without publishing the root entry docs.

## Required Inputs
- `PROJECT_SCOPE` (repo; required): Project repository root to publish.
- `README_GOAL` (github-overview|onboarding|usage-entry|mixed; required): Primary goal of the root README.
- `AUDIENCE` (general|developer|operator|mixed; required): Primary audience for the root README and localized entry docs.
- `AUDIENCE_LEVEL` (general|intermediate|expert; optional): Difficulty level. Default is general-reader language when omitted.
- `PRIMARY_LANGUAGE` (string; optional): Primary authoring language for the root README and source portal. Default is en.
- `TARGET_LANGUAGES` (list; optional; shape: {LANG}): Languages to publish under /i18n/<lang>/. Default localized set is ko, es, zh when omitted.
- `SOURCE_DOCS` (list; required; shape: {PATH, ROLE}): Docs or evidence-backed pages that the root README and localized entry docs must summarize and link.

## Input Contract Notes
- This skill owns the repo root README and the /i18n/<lang>/ publishing surface.
- Folder-level README files below the repo root are outside this skill; use doc-build-index.
- If AUDIENCE_LEVEL is omitted, explain the project as if the reader is a general but capable newcomer.

## Structured Outputs
- `ROOT_README_PATH` (string; required): Root README path created or updated by this skill.
- `LANGUAGE_DOCS` (list; required; shape: {LANG, PATH, SOURCE_REF, COVERAGE}): Localized docs created or updated under /i18n/<lang>/.
- `LANGUAGE_SELECTOR_LINKS` (list; required; shape: {LANG, TARGET}): Language selector links exposed from the root README.
- `DOC_PORTAL_MAP` (list; required; shape: {ENTRY, LINKS_TO}): How the root README and localized entry docs connect to deeper guides.

## Output Contract Notes
- ROOT_README_PATH should stay GitHub-first: fast overview, quickstart, and links to deeper docs before detailed internals.
- LANGUAGE_DOCS should live under /i18n/<lang>/ so readers can switch languages predictably.
- The root README should summarize canonical docs, not duplicate them.

## Primary Lens
- `primary_lens`: `feynman-teaching`
- `why`: Project entry docs should explain the project plainly first, then layer detail and language variants without losing accuracy.

## Artifacts
- `artifacts_in`: documentation-report.v2, knowledge-index-docset.v2
- `artifacts_out`: project-readme-portal.v2

## Neutrality Rules
- Do not claim capabilities or workflows that the source docs and repository evidence do not support.
- If a source doc is incomplete, preserve that gap instead of fabricating localized content.
- Keep translation and simplification faithful to the source meaning.
