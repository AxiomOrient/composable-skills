---
name: doc-build-index
description: "Build recursive folder docsets where each parent folder gets a README-style overview and each child folder or project gets a focused project-info doc with explicit links. Use when the target is a folder tree or module tree and readers need summary-at-parent plus detail-at-child navigation. Do not modify the repo root README."
---

# Doc / Build Index

## Purpose
Build hierarchical folder docsets with parent overview pages and child detail pages, while keeping the hierarchy MECE and easy to navigate.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat},deterministic-output |
 lens: nielsen-norman |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `nielsen-norman` because it keeps the work aligned with: Reader-first hierarchy, scanning behavior, information scent, and navigable landing pages.

## Use When
- Need a folder tree or module tree documented as parent overview pages plus child project or module info pages.
- Need README-style summaries at folder boundaries without touching the repo root README.
- Need one docset whose parent pages summarize and link while child pages hold focused project information.

## Do Not Use When
- Need only a single guide page with no hierarchy.
- Need repo root README authoring or multilingual publishing.
- Need lifecycle governance only.
- Need release notes, changelog entries, or migration docs for a release.

## Required Inputs
- `DOCSET_KIND` (folder-tree|module-tree|project-tree; required): Primary hierarchy being documented.
- `TREE_SCOPE` (folder|subtree; required): Exact hierarchy to document.
- `INDEX_DEPTH` (one-level|recursive; required): How deep the parent/child docset should go.
- `INDEX_LAYOUT` (docs-mirror|in-place-readme; optional): Where the overview pages should live. Defaults to `in-place-readme` when omitted.
- `PARENT_ENTRY_STYLE` (readme-overview|index-page; optional): Parent-page style. Defaults to `readme-overview` when omitted.
- `CHILD_DOC_STYLE` (project-info|module-info|mixed; optional): Child-page style. Defaults to `project-info` when omitted.
- `AUDIENCE` (general|developer|maintainer|mixed; required): Primary audience for the resulting docset.
- `AUDIENCE_LEVEL` (general|intermediate|expert; optional): Difficulty level. Default is general-reader language when omitted.
- `EVIDENCE_LINKS` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Extra files or sources that must be cited beyond the repo tree itself.

## Input Contract Notes
- Use `in-place-readme` when the folder itself should expose the overview page as its entrypoint.
- Each parent page should summarize only the scope it owns and link downward; it should not absorb every child detail.
- Child pages should hold detailed project information without reintroducing the global overview verbatim.
- If AUDIENCE_LEVEL is omitted, explain the hierarchy and key terms for a general reader first.

## Structured Outputs
- `PARENT_ENTRY_DOCS` (list; required; shape: {PATH, COVERS, LINKS_TO}): Parent overview pages or local README files that summarize and link child docs.
- `CHILD_INFO_DOCS` (list; required; shape: {PATH, TARGET, SUMMARY, EVIDENCE_REF}): Child project or module docs created or updated under the hierarchy.
- `DOCSET_NAV_MAP` (list; required; shape: {FROM, TO, PURPOSE}): Navigation graph across parent pages and child detail pages.
- `COVERAGE_GAPS` (list; required; shape: {TARGET, GAP, NEXT_SOURCE}): Missing evidence or unsupported targets that prevent complete child coverage.

## Output Contract Notes
- PARENT_ENTRY_DOCS should read like overview pages: summary, key facts, and explicit links.
- CHILD_INFO_DOCS should stay MECE relative to siblings and inherit shared context from the parent page instead of duplicating it.
- DOCSET_NAV_MAP should show upward and downward navigation, not just a flat link list.
- COVERAGE_GAPS should be used instead of inventing a child summary when evidence is weak.

## Primary Lens
- `primary_lens`: `nielsen-norman`
- `why`: Hierarchical docsets succeed when each landing page provides context, each child page has a distinct role, and navigation stays explicit.

## Artifacts
- `artifacts_in`: doc-inventory.v2
- `artifacts_out`: knowledge-index-docset.v2

## Neutrality Rules
- Write only claims grounded in the actual files or cited supporting sources.
- If a folder has many children, group them in reader-meaningful clusters rather than an undifferentiated long list.
- Keep parent overview text distinct from child detail text.

## Execution Constraints
1. If a folder has child folders, the parent gets a README-style overview or index page with summary, scope, key facts, and child links.
2. Each child folder or project gets a focused info doc that covers only its own responsibility, interfaces, dependencies, commands, and related docs as supported by evidence.
3. Keep sibling child docs MECE; move shared context upward to the parent overview page.
4. Do not modify the repo root README from this skill.
5. Prefer stable hierarchy: parent overview -> child project info -> deeper evidence links.

## Response Format

Think and operate in English, but deliver the final response in Korean.

List what was written, grouped by level:
- Parent overview: file — covers — key links
- Child info: file — target — main scope

Flag coverage gaps:
"Couldn't verify: [target] — missing: [source]"

Ask:
"Want to recurse one level deeper, or is this hierarchy the right stop point?"
