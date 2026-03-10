---
name: doc-build-index
description: "Analyze module trees, libraries, or papers into per-artifact explanation docs, local index files, and a guide index that links them together. Use when the target has hierarchy or external knowledge sources and readers need a navigable docset. Do not modify the repo root README."
---

# Knowledge Index Docs

## Purpose
Build hierarchical analysis docs and index files from folders, modules, libraries, or papers without touching the repo root README.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat},deterministic-output |
 lens: nielsen-norman |
 output: md(contract=v1)]
```

## Use When
- Need per-folder, per-module, per-library, or per-paper explanation docs.
- Need local README or index files that link analysis docs together.
- Need one guide index that aggregates lower-level indexes without rewriting the repo root README.

## Do Not Use When
- Need only a single guide or doc page with no hierarchy.
- Need repo root README authoring or multilingual publishing.
- Need documentation inventory or cleanup only.

## Required Inputs
- `DOCSET_KIND` (module-tree|library|paper|mixed; required): Primary kind of knowledge surface being documented.
- `DOC_FORM` (guide|reference|paper-summary|survey|mixed; optional): Document form for the generated analysis docs. Default is guide for module/library trees and paper-summary for paper targets when omitted.
- `TARGET_SCOPE` (folder|module|library|paper|subtree; required): Exact hierarchy or source set to document.
- `INDEX_DEPTH` (artifact-only|folder-tree|multi-level; required): How deep the analysis and index hierarchy should go.
- `INDEX_LAYOUT` (docs-mirror|in-place-readme; optional): Where index files should live. Default is docs-mirror when omitted.
- `AUDIENCE` (general|developer|researcher|mixed; required): Primary audience for the resulting docset.
- `AUDIENCE_LEVEL` (general|intermediate|expert; optional): Difficulty level. Default is general-reader language when omitted.
- `EVIDENCE_LINKS` (list; required; shape: {TYPE, REF, WHY_RELEVANT}): Files, library docs, papers, or other sources used to support the analysis docs.

## Input Contract Notes
- Use docs-mirror when you want doc files separated from the source tree; use in-place-readme only when local README files are the intended entrypoints.
- This skill may create folder-level README or guide index files, but it must not modify the repo root README.
- DOC_FORM controls whether the resulting analysis docs read like guides, references, surveys, or paper summaries; do not use lens choice alone to encode the output genre.
- If AUDIENCE_LEVEL is omitted, explain the hierarchy and key terms for a general reader first.

## Structured Outputs
- `ANALYSIS_DOCS` (list; required; shape: {PATH, TARGET, FORM, SUMMARY, EVIDENCE_REF}): Analysis docs created or updated for specific folders, modules, libraries, or papers.
- `LOCAL_INDEX_FILES` (list; required; shape: {PATH, COVERS, LINKS_TO}): Local README or index files that organize nearby analysis docs.
- `GUIDE_INDEX_FILES` (list; required; shape: {PATH, COVERS, LINKS_TO}): Higher-level guide or index files that aggregate local indexes.
- `COVERAGE_GAPS` (list; required; shape: {TARGET, GAP, NEXT_SOURCE}): Missing evidence or unsupported targets that prevent complete coverage.

## Output Contract Notes
- ANALYSIS_DOCS should stay traceable to a specific target and evidence reference.
- ANALYSIS_DOCS should reflect DOC_FORM explicitly so readers can tell whether each file is a guide, reference, survey, or paper summary.
- LOCAL_INDEX_FILES should link readers downward to detailed docs and upward to the next guide level when both exist.
- GUIDE_INDEX_FILES should aggregate the hierarchy without acting as a replacement for the repo root README.

## Primary Lens
- `primary_lens`: `nielsen-norman`
- `frame_name`: Findability and Heuristics Reviewer
- `why`: Hierarchical docsets succeed when navigation, scanning order, and information scent stay explicit at every level.
- `summary`: Usability-first decisions based on explicit heuristics, scanning behavior, and information scent.
- `thesis`: Structures become easier to use when navigation, labeling, scanning, and information scent are treated as first-class constraints rather than afterthoughts.
- `decision_rules`:
  - Optimize the first scan path before polishing details.
  - Check whether the user can predict where to go next from labels, grouping, and information scent.
  - Prefer predictable headings, navigation, and labels over clever naming.
  - Treat duplication, orphaned nodes, and hidden paths as structure defects, not just content defects.
- `anti_patterns`:
  - Dense structures with weak labels or headings
  - Navigation that assumes insider knowledge
  - Hierarchy that mirrors implementation history instead of user intent
- `good_for`:
  - information architecture
  - README structure
  - doc inventory
  - doc curation
  - navigation review
- `not_for`:
  - root-cause debugging
  - dependency boundary design
  - security threat modelling
- `required_artifacts`:
  - Hierarchy or Navigation Map
  - Findability Risks
  - Labeling or Mitigation Notes
- `references`:
  - https://www.nngroup.com/articles/ten-usability-heuristics/

## Artifacts
- `artifacts_in`: doc-inventory.v1
- `artifacts_out`: knowledge-index-docset.v1

## Neutrality Rules
- Write only claims grounded in the actual files, library docs, papers, or other cited sources.
- If a target lacks enough evidence, record a coverage gap instead of inventing a summary.
- Separate analysis-doc writing from repo root README authoring.

## Execution Constraints
- Do not modify the repo root README from this skill.
- Prefer a stable hierarchy: analysis doc -> local index -> guide index.
- Define technical terms in plain words before using shorthand or specialist jargon when AUDIENCE_LEVEL is general or omitted.

## Mandatory Rules
- Keep every index file linked to the analysis docs it summarizes.
- Do not collapse multiple unrelated modules, libraries, or papers into one vague summary page.

## Example Invocation
```text
$doc-build-index
DOCSET_KIND: module-tree
TARGET_SCOPE: src/auth
INDEX_DEPTH: multi-level
AUDIENCE: general
```

## Output Discipline
- `response_profile=documentation_report`
- User-facing rendering is delegated to `respond`.
