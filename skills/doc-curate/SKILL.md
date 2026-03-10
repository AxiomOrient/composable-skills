---
name: doc-curate
description: "Use when repository docs below the repo root README must be indexed, structured, linked, de-duplicated, and stale-doc-cleaned based on actual file evidence. Build non-root entry docs and navigation with MECE structure, but leave root README authoring to doc-publish-readme. Do not modify runtime code."
---

# Doc / Curate

## Purpose
Reorganize non-root docs with explicit inventory, entry-structure planning, navigation graph, and cleanup actions.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat},deterministic-output |
 lens: nielsen-norman |
 output: md(contract=v1)]
```

## Use When
- Need documentation inventory, navigation, and cleanup planning.
- Need to reorganize folder-level entry docs and guide entrypoints below the repo root.
- Need doc curation without runtime code changes.
- Run doc-find-all first if a fresh documentation inventory is not yet available.

## Do Not Use When
- Need to write architecture or usage content only.
- Need runtime code changes.
- Need repo root README writing or multilingual publishing.
- Need only documentation inventory without curation guidance.

## Required Inputs
- `CURATION_GOAL` (cleanup|navigation|de-duplication|mixed; required): Primary curation objective.
- `TARGET_SCOPE` (docs-folder|repo|subtree; required): Doc scope to curate.
- `ENTRY_DOC_STYLE` (guide|reference|index|mixed; optional): Preferred style for non-root entry docs. Default is index when omitted.
- `INVENTORY_SCOPE` (root-only|folder-tree|repo-wide; required): How broad the inventory should be.

## Input Contract Notes
- This skill owns non-root entry structure planning and navigation cleanup.
- ENTRY_DOC_STYLE defaults to index when omitted and should describe the entry-doc role, not the prose difficulty.
- Use doc-publish-readme when the repo root README or language portal must change.

## Structured Outputs
- `DOC_INVENTORY` (list; required; shape: {PATH, STATUS, EVIDENCE}): Evidence-backed document inventory.
- `DOC_ENTRY_STRUCTURE` (list; required; shape: {ENTRY_PATH, ENTRY_KIND, COVERS, EVIDENCE_REF}): Planned non-root entry docs and the scope each one covers.
- `DOC_NAVIGATION_MAP` (list; required; shape: {FROM, TO, PURPOSE}): Navigation graph across non-root entry docs and key supporting docs.
- `CLEANUP_ACTIONS` (list; required; shape: {ACTION, TARGET, WHY, CONFIDENCE}): Keep, merge, move, archive, or delete-candidate actions.

## Output Contract Notes
- DOC_INVENTORY should reflect observed doc state before proposing cleanup.
- DOC_ENTRY_STRUCTURE should stay bounded to non-root entry docs that materially improve navigation.
- CLEANUP_ACTIONS may be empty when the current non-root doc surface is already coherent.

## Primary Lens
- `primary_lens`: `nielsen-norman`
- `why`: Doc curation should optimize findability, navigation, and information scent.

## Artifacts
- `artifacts_in`: doc-inventory.v1
- `artifacts_out`: doc-curation-report.v1

## Neutrality Rules
- Read docs before classifying them stale or duplicate.
- Keep delete recommendations tentative until evidence is explicit.
- Separate navigation issues from content duplication issues.

## Execution Constraints
- Do not author or rewrite the repo root README from this skill.
- Treat non-root entry docs generically; do not assume they must be named README unless the local structure calls for it.
- Keep cleanup actions separate from content-writing recommendations.
- Prefer stable folder and guide entrypoints over scattered cross-links.
