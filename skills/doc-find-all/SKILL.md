---
name: doc-find-all
description: "Inventory documentation files, classify their status, and expose orphan, duplicate, or stale docs before curation. Use when the immediate job is inventory, not rewriting docs yet."
---

# Doc / Find All

## Purpose
Create an evidence-backed documentation inventory before curation or refresh work.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: nielsen-norman | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `nielsen-norman` because it keeps the work aligned with: Usability-first decisions based on explicit heuristics, scanning behavior, and information scent.

## Use When
- Need to know which docs are active, stale, duplicate, or orphaned.
- Need a bounded documentation inventory before curation — run this before doc-curate.
- Need evidence before recommending merges, moves, or deletes.

## Do Not Use When
- Need to write the README or guide content directly.
- Need runtime code changes.
- The target scope contains no documentation set to inventory.

## Required Inputs
- `TARGET_SCOPE` (path|docs-folder|repo; required): Documentation scope to inventory.
- `INVENTORY_GOAL` (cleanup|navigation|coverage|mixed; optional): Why the inventory is being created. Defaults to `mixed` when omitted.

## Input Contract Notes
- TARGET_SCOPE should be a real documentation set, not a broad repo area with no docs boundary.
- INVENTORY_GOAL should explain why the inventory is being created so stale, duplicate, and coverage signals can be prioritized correctly.
- When INVENTORY_GOAL is omitted, default to `mixed`.

## Structured Outputs
- `DOC_INVENTORY` (list; required; shape: {PATH, STATUS, EVIDENCE}): Document records with status and evidence.
- `ORPHAN_OR_DUPLICATE_SET` (list; required; shape: {PATH, ISSUE, EVIDENCE}): Docs that appear stale, orphaned, or duplicated.
- `NEXT_CURATION_TARGETS` (list; required; shape: {PATH, WHY_NEXT}): Highest-value docs to curate next.

## Output Contract Notes
- DOC_INVENTORY should distinguish observed status from inferred cleanup priority.
- ORPHAN_OR_DUPLICATE_SET may be empty when the current doc set is clean enough.
- NEXT_CURATION_TARGETS should stay bounded to the immediate next doc work instead of a generic backlog.

## Primary Lens
- `primary_lens`: `nielsen-norman`
- `why`: Doc inventory should focus on discoverability, duplication, and navigation gaps.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: doc-inventory.v1

## Neutrality Rules
- Read docs before classifying them stale or duplicate.
- Keep delete or archive conclusions tentative until evidence is explicit.
- Separate navigation problems from content-quality problems.

## Response Format

Show the inventory as a compact list:
- file — status (active/stale/orphaned/duplicate) — reason

List the highest-value curation targets next: file — why now.

Flag gaps: "Didn't check: [paths or areas outside scope]"

Ask: "Want to curate [top target] first, or need to widen the inventory scope?"

## Execution Constraints
- Do not rewrite docs from this skill; inventory only.
- Keep stale or duplicate classifications tied to explicit evidence such as overlap, missing links, or outdated references.
- Prefer the smallest useful inventory that supports the stated inventory goal.

## Example Invocation
```text
$doc-find-all
TARGET_SCOPE: docs
INVENTORY_GOAL: cleanup
```
