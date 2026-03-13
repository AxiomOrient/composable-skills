---
name: workflow-doc-systemize
description: "Workflow skill that inventories docs, curates the non-root doc surface, and writes the needed documentation artifacts. Use when the user needs one default documentation entrypoint instead of manually chaining inventory, curation, and writing."
---

# Workflow / Doc Systemize

## Purpose
Compose documentation inventory, curation, and writing into one default docs workflow.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs,compat},deterministic-output | lens: nielsen-norman | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `nielsen-norman` because it keeps the work aligned with: Usability-first decisions based on explicit heuristics, scanning behavior, and information scent.

## Use When
- Need one default docs entrypoint for a repo or docs subtree.
- Need inventory, curation, and writing to stay connected in one path.
- Need documentation work without runtime code changes.

## Do Not Use When
- Need only root README publishing.
- Need only one narrow documentation concern.
- Need runtime code changes.

## Required Inputs
- `TARGET_SCOPE` (path|docs-folder|repo|subtree; required): Documentation scope to systemize.
- `INVENTORY_GOAL` (cleanup|navigation|coverage|mixed; optional): Why the inventory is being created. Defaults to `mixed` when omitted.
- `DOC_GOAL` (concept-guide|architecture-guide|usage-guide|api-guide|module-note|mixed; required): Documentation objective for the writing stage.
- `AUDIENCE` (general|developer|operator|maintainer|mixed; required): Primary audience.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Documentation constraints or non-goals.

## Input Contract Notes
- TARGET_SCOPE should be a real documentation surface, not a generic code subtree.
- DOC_GOAL and INVENTORY_GOAL can differ; one guides cleanup while the other guides writing.
- Use doc-publish-readme separately when the root README or publish surface must change.
- When INVENTORY_GOAL is omitted, default to `mixed`.

## Structured Outputs
- `DOC_INVENTORY` (list; required; shape: {PATH, STATUS, EVIDENCE}): Documentation inventory.
- `DOC_NAVIGATION_MAP` (list; required; shape: {FROM, TO, PURPOSE}): Navigation map for the curated docs surface.
- `WRITTEN_DOCS` (list; required; shape: {PATH, CHANGE_KIND, AUDIENCE, FORM}): Docs created or updated.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Actual atomic path executed by the workflow.

## Output Contract Notes
- DOC_INVENTORY should stay evidence based.
- WRITTEN_DOCS should reflect the final writing work instead of only the cleanup plan.
- EXPANDED_ATOMIC_PATH must preserve execution order explicitly.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: doc-inventory.v1, doc-curation-report.v1, documentation-report.v1

## Neutrality Rules
- Preserve the neutrality rules of the underlying docs skills.
- Do not imply runtime code changes from a docs-only workflow.
- Keep inventory, curation, and writing outputs distinct.

## Execution Constraints
- Do not widen this workflow into root README publishing.
- Prefer the smallest doc surface that improves findability and usefulness for the stated audience.

## Response Format

Show what was written and what's still missing — no chain commentary.

```
updated: `file` — [what changed and why]
written: `file` — [new content added]
```

Gaps (couldn't verify or write):
- `file` — [why — e.g., no source content, ambiguous scope]

Ask: "Anything important missing in [section with lowest confidence]?"

## Mandatory Rules
- Expose the expanded atomic path explicitly.
- Keep root README publication outside this workflow.

## Expansion
- `$doc-find-all`
- `$doc-curate`
- `$doc-write`

## Example Invocation
```text
$workflow-doc-systemize
TARGET_SCOPE: docs
INVENTORY_GOAL: cleanup
DOC_GOAL: usage-guide
AUDIENCE: maintainer
```
