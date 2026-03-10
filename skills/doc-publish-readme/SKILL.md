---
name: doc-publish-readme
description: "Create or refresh the repo root README as a GitHub-friendly project entrypoint, then publish easy-to-read localized entry docs under docs/i18n/<lang>/. Use when the target is a project repo and readers need a root landing doc plus language-specific entrypoints."
---

# Project Readme Localize

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
- `TARGET_LANGUAGES` (list; optional; shape: {LANG}): Languages to publish under docs/i18n/<lang>/. Default localized set is ko, es, zh when omitted.
- `SOURCE_DOCS` (list; required; shape: {PATH, ROLE}): Docs or evidence-backed pages that the root README and localized entry docs must summarize and link.

## Input Contract Notes
- This skill owns the repo root README and the docs/i18n/<lang>/ publishing surface.
- If AUDIENCE_LEVEL is omitted, explain the project as if the reader is a general but capable newcomer.
- PRIMARY_LANGUAGE defaults to en when omitted.
- TARGET_LANGUAGES defaults to ko, es, zh when omitted, and user-requested extra languages should be appended unless the user explicitly narrows the language set.

## Structured Outputs
- `ROOT_README_PATH` (string; required): Root README path created or updated by this skill.
- `LANGUAGE_DOCS` (list; required; shape: {LANG, PATH, SOURCE_REF, COVERAGE}): Localized docs created or updated under docs/i18n/<lang>/.
- `LANGUAGE_SELECTOR_LINKS` (list; required; shape: {LANG, TARGET}): Language selector links exposed from the root README.
- `DOC_PORTAL_MAP` (list; required; shape: {ENTRY, LINKS_TO}): How the root README and localized entry docs connect to deeper guides.

## Output Contract Notes
- ROOT_README_PATH should stay GitHub-first: fast overview, quickstart, and links to deeper docs before detailed internals.
- LANGUAGE_DOCS should live under docs/i18n/<lang>/ so readers can switch languages predictably.
- LANGUAGE_SELECTOR_LINKS should let readers choose their language from the root README without searching.
- The root README should be authored in English by default unless PRIMARY_LANGUAGE explicitly overrides it.

## Primary Lens
- `primary_lens`: `feynman-teaching`
- `frame_name`: Plain-Language Concept Teacher
- `why`: Project entry docs should explain the project plainly first, then layer detail and language variants without losing accuracy.
- `summary`: Start from the simplest correct mental model, translate jargon into plain words, and add concrete examples before deeper detail.
- `thesis`: If a general reader cannot follow the core idea in plain language, the explanation is not ready; define the idea simply first, then layer technical detail only as needed.
- `core_philosophy`: Make the main idea easy without making it wrong, and let the reader climb from simple words to technical precision step by step.
- `mental_model`:
  - Name the main idea in one plain sentence before using technical framing.
  - Translate unfamiliar terms into everyday language before reintroducing the formal term.
  - Use one concrete example to anchor the explanation before discussing edge cases.
  - Add detail only when it changes the reader's understanding or next action.
- `decision_rules`:
  - Prefer plain language over jargon when both are accurate.
  - Define unavoidable technical terms the first time they appear.
  - Choose examples that match the reader's likely mental model or workflow.
  - Keep explanations short enough that a non-expert can retain the thread.
- `anti_patterns`:
  - Dense jargon before first principles
  - Correct but unreadable expert shorthand
  - Example-free explanation of an abstract concept
- `good_for`:
  - beginner documentation
  - README writing
  - concept guides
  - multilingual explanation
- `not_for`:
  - root-cause debugging
  - threat modelling
  - performance bottleneck analysis
- `required_artifacts`:
  - Core Idea
  - Plain-Language Definition
  - Concrete Example
  - Term Translation
- `references`:
  - https://www.feynmanlectures.caltech.edu/
  - https://fs.blog/feynman-learning-technique/

## Artifacts
- `artifacts_in`: documentation-report.v1, knowledge-index-docset.v1
- `artifacts_out`: project-readme-portal.v1

## Neutrality Rules
- Do not claim capabilities or workflows that the source docs and repository evidence do not support.
- If a source doc is incomplete, preserve that gap instead of fabricating localized content.
- Keep translation and simplification faithful to the source meaning.

## Execution Constraints
- Author the root README in English by default unless PRIMARY_LANGUAGE explicitly overrides it.
- Always place localized entry docs under docs/i18n/<lang>/.
- Default localized entry docs to ko, es, zh and append extra user-requested languages when provided.
- Keep the root README readable on GitHub with a short first scan path before deeper details.
- Define technical terms in plain words before using jargon when AUDIENCE_LEVEL is general or omitted.
- Link the root README to language-specific entry docs and link those entry docs back to the root README or portal.

## Mandatory Rules
- Only this skill should modify the repo root README in the documentation pack.
- Publish ko, es, and zh entry docs by default unless the user explicitly narrows the language set.
- Every target language must receive at least one entry doc under docs/i18n/<lang>/.

## Example Invocation
```text
$doc-publish-readme
PROJECT_SCOPE: repo
README_GOAL: github-overview
AUDIENCE: general
PRIMARY_LANGUAGE: en
TARGET_LANGUAGES: ko, es, zh
```

## Output Discipline
- `response_profile=documentation_report`
- User-facing rendering is delegated to `respond`.
