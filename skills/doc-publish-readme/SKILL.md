---
name: doc-publish-readme
description: "Create or refresh the repo root README as a GitHub-friendly project entrypoint, then publish easy-to-read localized entry docs under /i18n/<lang>/. Use when the target is a project repo and readers need a root landing doc plus language-specific entrypoints."
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
- Need only hierarchical module, library, or paper index docs.
- Need documentation inventory or cleanup without publishing the root entry docs.

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
- If AUDIENCE_LEVEL is omitted, explain the project as if the reader is a general but capable newcomer.
- PRIMARY_LANGUAGE defaults to en when omitted.
- TARGET_LANGUAGES defaults to ko, es, zh when omitted, and user-requested extra languages should be appended unless the user explicitly narrows the language set.

## Structured Outputs

- `ROOT_README_PATH` (string; required): Root README path created or updated by this skill.
- `LANGUAGE_DOCS` (list; required; shape: {LANG, PATH, SOURCE_REF, COVERAGE}): Localized docs created or updated under /i18n/<lang>/.
- `LANGUAGE_SELECTOR_LINKS` (list; required; shape: {LANG, TARGET}): Language selector links exposed from the root README.
- `DOC_PORTAL_MAP` (list; required; shape: {ENTRY, LINKS_TO}): How the root README and localized entry docs connect to deeper guides.

## Output Contract Notes

- ROOT_README_PATH should stay GitHub-first: fast overview, quickstart, and links to deeper docs before detailed internals.
- LANGUAGE_DOCS should live under /i18n/<lang>/ so readers can switch languages predictably.
- LANGUAGE_SELECTOR_LINKS should let readers choose their language from the root README without searching.
- The root README should be authored in English by default unless PRIMARY_LANGUAGE explicitly overrides it.

## Primary Lens

- `primary_lens`: `feynman-teaching`
- `why`: Project entry docs should explain the project plainly first, then layer detail and language variants without losing accuracy.

## Artifacts

- `artifacts_in`: documentation-report.v1, knowledge-index-docset.v1
- `artifacts_out`: project-readme-portal.v1

## Neutrality Rules

- Do not claim capabilities or workflows that the source docs and repository evidence do not support.
- If a source doc is incomplete, preserve that gap instead of fabricating localized content.
- Keep translation and simplification faithful to the source meaning.

## Execution Constraints

- Author the root README in English by default unless PRIMARY_LANGUAGE explicitly overrides it.
- Always place localized entry docs under /i18n/<lang>/.
- Default localized entry docs to ko, es, zh and append extra user-requested languages when provided.
- Keep the root README readable on GitHub with a short first scan path before deeper details.
- Define technical terms in plain words before using jargon when AUDIENCE_LEVEL is general or omitted.
- Link the root README to language-specific entry docs and link those entry docs back to the root README or portal.

## Response Format

Show what was written or updated:

- README.md — [change kind]
- /i18n/[lang]/ — [lang] entry doc — [coverage notes]

Flag content gaps: "Couldn't verify: [section] — source doc was incomplete"

Ask about audience or tone if the source docs were ambiguous on either.

## Mandatory Rules

- Only this skill should modify the repo root README in the documentation surface.
- Publish ko, es, and zh entry docs by default unless the user explicitly narrows the language set.
- Every target language must receive at least one entry doc under /i18n/<lang>/.

## Example Invocation

```text
$doc-publish-readme
PROJECT_SCOPE: repo
README_GOAL: github-overview
AUDIENCE: general
PRIMARY_LANGUAGE: en
TARGET_LANGUAGES: ko, es, zh
```
