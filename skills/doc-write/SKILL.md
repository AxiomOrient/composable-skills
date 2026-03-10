---
name: doc-write
description: "Documentation-only skill. Produce or refresh non-root documentation such as concept guides, architecture notes, usage docs, and module docs from evidence. Root README, GitHub-style onboarding, and multilingual publishing belong to doc-publish-readme. Do not implement code or perform review verdicts. English triggers: documentation, guide writing, architecture docs, docs generation."
---

# Write Docs

## Purpose
Write or refresh non-root documentation from repository evidence with audience-aware difficulty control.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat},deterministic-output |
 lens: feynman-teaching |
 output: md(contract=v1)]
```

## Use When
- Need to create or refresh non-root guides, architecture docs, usage docs, or module notes.
- Need to turn upstream stage payloads into documentation artifacts.
- Need documentation changes without runtime code changes.

## Do Not Use When
- Need runtime code changes.
- Need documentation inventory or cleanup only.
- Need repo root README, GitHub landing docs, or multilingual publishing.
- Need review verdicts rather than docs.

## Required Inputs
- `DOC_GOAL` (concept-guide|architecture-guide|usage-guide|api-guide|module-note|mixed; required): Documentation objective.
- `DOC_FORM` (guide|tutorial|reference|concept-note|paper-summary|survey|mixed; optional): Document form. Default is guide when omitted.
- `TARGET_SCOPE` (folder|module|artifact|docs-subtree; required): Scope to document.
- `AUDIENCE` (general|developer|operator|maintainer|mixed; required): Primary audience.
- `AUDIENCE_LEVEL` (general|intermediate|expert; optional): Difficulty level. Default is general-reader language when omitted.
- `EVIDENCE_LINKS` (list; required; shape: {TYPE, REF, WHY_RELEVANT}): Files, commands, logs, or upstream payloads supporting the docs.

## Input Contract Notes
- AUDIENCE should identify the primary reader who must act on the document, not every possible reader at once.
- DOC_GOAL should describe the reader's main task or decision, not a grab-bag of optional sections.
- DOC_FORM controls the document genre such as guide versus paper-summary; use lens override only when the mental model must change, not as a substitute for genre selection.
- When DOC_FORM is `guide` or `tutorial`, optimize for a newcomer who wants to know when to use the doc, what they will get from it, and what to do next.
- When DOC_FORM is `reference`, `survey`, or `paper-summary`, optimize for scanability and lookup speed rather than tutorial-style narration.
- EVIDENCE_LINKS should point only to real sources that support the written claims.
- This skill does not modify the repo root README; use doc-publish-readme when the root entry doc or multilingual publish surface must change.
- If AUDIENCE_LEVEL is omitted, explain terms for a general reader first and introduce jargon only after a plain-language definition.

## Structured Outputs
- `DOC_PLAN` (list; required; shape: {SECTION, READER_NEED, EVIDENCE_REF}): Sections or docs that will be written.
- `WRITTEN_DOCS` (list; required; shape: {PATH, CHANGE_KIND, AUDIENCE, FORM}): Docs created or updated.
- `EVIDENCE_MAP` (list; required; shape: {SECTION, CLAIM, EVIDENCE}): Evidence supporting each section.

## Output Contract Notes
- DOC_PLAN should prioritize the shortest path to the audience's primary question or task before secondary context.
- WRITTEN_DOCS should stay proportional to DOC_GOAL; omit decorative sections that do not help the stated audience.
- WRITTEN_DOCS and DOC_PLAN should reflect DOC_FORM explicitly when a paper-summary, survey, tutorial, or reference structure is requested.
- For `guide` or `tutorial`, the first scan path should answer three things quickly: what this is, when to read it, and what action the reader can take next.
- For `reference`, `survey`, or `paper-summary`, prefer tables, bullets, and compact lookup blocks over long tutorial-style prose.
- EVIDENCE_MAP should let a reader trace each major claim back to a concrete source.
- WRITTEN_DOCS should exclude the repo root README.

## Primary Lens
- `primary_lens`: `feynman-teaching`
- `frame_name`: Plain-Language Concept Teacher
- `why`: General documentation should explain the core idea plainly first, then layer detail only as needed for the reader level.
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
- `artifacts_in`: doc-curation-report.v1
- `artifacts_out`: documentation-report.v1

## Neutrality Rules
- Write only claims grounded in repository evidence or upstream payloads.
- If a section lacks support, mark it as needing confirmation instead of guessing.
- Keep documentation structure separate from implementation or review advice.

## Execution Constraints
- Prefer the minimum useful document structure that helps the stated audience understand, use, or operate the target.
- Do not add sections for completeness theater when they do not change the reader's decision or next action.
- Keep the document focused on the explicit scope and audience instead of mixing multiple doc goals into one artifact.
- For guide-like docs, open with a plain-language orientation path before deeper explanation.
- For reference-like docs, compress aggressively and bias toward scanable structure instead of narrative completeness.
- Define technical terms in plain words before using shorthand or deeper jargon when AUDIENCE_LEVEL is general or omitted.
- Do not modify the repo root README from this skill.

## Output Discipline
- `response_profile=documentation_report`
- User-facing rendering is delegated to `respond`.
