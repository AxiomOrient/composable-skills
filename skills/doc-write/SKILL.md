---
name: doc-write
description: "Documentation-only skill. Produce or refresh non-root, non-release documentation such as concept guides, architecture notes, usage docs, module docs, redirects, and deprecation notices from evidence. Root README publishing belongs to doc-publish-readme. Recursive folder docsets belong to doc-build-index. Release-facing docs belong to doc-write-release-docs. Do not implement code or perform review verdicts."
---

# Doc / Write

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

## Lens Rationale
This skill uses `feynman-teaching` because it keeps the work aligned with: Start from the simplest correct mental model, translate jargon into plain words, and add concrete examples before deeper detail.

## Use When
- Need to create or refresh non-root guides, architecture docs, usage docs, module notes, redirect notes, or deprecation notices.
- Need to turn upstream stage payloads into documentation artifacts.
- Need documentation changes without runtime code changes.

## Do Not Use When
- Need runtime code changes.
- Need documentation inventory or lifecycle governance only.
- Need repo root README, GitHub landing docs, or multilingual publishing.
- Need recursive parent/child folder docsets.
- Need release notes, changelog entries, migration docs, or rollback notes.
- Need review verdicts rather than docs.

## Required Inputs
- `DOC_GOAL` (refresh|concept-guide|architecture-guide|usage-guide|api-guide|module-note|deprecation-note|redirect-note|mixed; required): Documentation objective.
- `DOC_FORM` (guide|tutorial|reference|concept-note|redirect|deprecation-note|mixed; optional): Document form. Default is guide when omitted.
- `TARGET_SCOPE` (folder|module|artifact|docs-subtree; required): Scope to document.
- `AUDIENCE` (general|developer|operator|maintainer|mixed; required): Primary audience.
- `AUDIENCE_LEVEL` (general|intermediate|expert; optional): Difficulty level. Default is general-reader language when omitted.
- `EVIDENCE_LINKS` (list; required; shape: {TYPE, REF, WHY_RELEVANT}): Files, commands, logs, or upstream payloads supporting the docs.

## Input Contract Notes
- AUDIENCE should identify the primary reader who must act on the document, not every possible reader at once.
- DOC_GOAL should describe the reader's main task or decision, not a grab-bag of optional sections.
- Use `deprecation-note` or `redirect-note` when lifecycle governance has already decided the target doc should remain temporarily as a bridge.
- This skill does not modify the repo root README; use doc-publish-readme when the root entry doc or multilingual publish surface must change.

## Structured Outputs
- `DOC_PLAN` (list; required; shape: {SECTION, READER_NEED, EVIDENCE_REF}): Sections or docs that will be written.
- `WRITTEN_DOCS` (list; required; shape: {PATH, CHANGE_KIND, AUDIENCE, FORM}): Docs created or updated.
- `EVIDENCE_MAP` (list; required; shape: {SECTION, CLAIM, EVIDENCE}): Evidence supporting each section.

## Output Contract Notes
- DOC_PLAN should prioritize the shortest path to the audience's primary question or task before secondary context.
- WRITTEN_DOCS should stay proportional to DOC_GOAL; omit decorative sections that do not help the stated audience.
- Redirect or deprecation docs should point clearly to the canonical replacement instead of duplicating the replacement content.

## Primary Lens
- `primary_lens`: `feynman-teaching`
- `why`: Non-root docs often fail because they jump into local jargon too early instead of leading readers from problem to answer.

## Artifacts
- `artifacts_in`: doc-curation-report.v2, knowledge-index-docset.v2
- `artifacts_out`: documentation-report.v2

## Neutrality Rules
- Write only what the evidence supports.
- Keep transitional docs shorter than canonical docs.
- Do not imply runtime behavior or release guarantees that were not verified.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Show what was written:
- updated: `file` — [what changed and why]
- written: `file` — [new content added]

Flag gaps:
- `file` — [why not written or why low confidence]
