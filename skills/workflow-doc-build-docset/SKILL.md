---
name: workflow-doc-build-docset
description: "Workflow skill that inventories a folder tree and builds parent README-style overview pages plus child project-info docs. Use when the user wants one default docset builder instead of manually chaining inventory and hierarchy-writing skills."
---

# Workflow / Doc Build Docset

## Purpose
Compose documentation inventory and hierarchical docset writing into one default workflow for folder-tree documentation.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat},deterministic-output |
 lens: nielsen-norman |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `nielsen-norman` because hierarchical docsets work only when landing pages, summaries, and links support quick scanning and clear navigation.

## Use When
- Need a folder tree documented as parent README-style summaries and child detail docs.
- Need one workflow that inventories the current surface before generating hierarchy docs.
- Need recursive, MECE-friendly docs for modules, projects, or subtrees.

## Do Not Use When
- Need only lifecycle governance for existing docs.
- Need repo root README publication.
- Need release notes, changelog entries, or migration docs.
- Need only one narrow page rather than a hierarchy.

## Required Inputs
- `TREE_SCOPE` (folder|subtree; required): Folder tree to document.
- `DOCSET_KIND` (folder-tree|module-tree|project-tree; required): Kind of hierarchy being documented.
- `AUDIENCE` (general|developer|maintainer|mixed; required): Primary audience for the hierarchy.
- `INDEX_DEPTH` (one-level|recursive; optional): How deep the hierarchy should be. Defaults to `recursive` when omitted.
- `INDEX_LAYOUT` (docs-mirror|in-place-readme; optional): Where parent overview pages should live. Defaults to `in-place-readme` when omitted.

## Structured Outputs
- `PARENT_ENTRY_DOCS` (list; required; shape: {PATH, COVERS, LINKS_TO}): Parent overview pages or local README files.
- `CHILD_INFO_DOCS` (list; required; shape: {PATH, TARGET, SUMMARY, EVIDENCE_REF}): Child project or module docs.
- `DOCSET_NAV_MAP` (list; required; shape: {FROM, TO, PURPOSE}): Navigation graph across the hierarchy.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Atomic path executed by the workflow.

## Execution Constraints
- Inventory first so existing docs and ownership are not overwritten blindly.
- Keep the hierarchy reader-first: parent summary, child detail, explicit links.
- Do not widen this workflow into repo root README publication.

## Expansion
- `$doc-find-all`
- `$doc-build-index`
