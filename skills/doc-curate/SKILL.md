---
name: doc-curate
description: "Govern the documentation surface by classifying docs as keep, update, deprecate, or delete, while preserving durable knowledge and explicit replacement paths. Use when repository docs need lifecycle decisions before rewriting or removal. Do not modify runtime code."
---

# Doc / Curate

## Purpose
Reclassify and clean the documentation surface with explicit lifecycle decisions grounded in current reader need, current role, migration need, and durable-knowledge retention.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat},deterministic-output |
 lens: nielsen-norman |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `nielsen-norman` because it keeps the work aligned with: Usability-first decisions, information scent, navigation clarity, and explicit ownership of each maintained doc.

## Use When
- Need to decide whether each doc should be kept, updated, deprecated, or deleted.
- Need to preserve durable knowledge before deleting delivery-only docs.
- Need to separate canonical docs from stale, superseded, or migration-only docs.
- Need explicit cleanup actions without touching runtime code.

## Do Not Use When
- Need repo root README authoring or multilingual publishing.
- Need a recursive folder docset with parent README-style summaries; use doc-build-index.
- Need release notes, upgrade notes, or migration docs for a specific release; use doc-write-release-docs.
- Need only a fresh inventory with no lifecycle judgement.

## Required Inputs
- `CURATION_GOAL` (lifecycle-governance|cleanup|surface-sync|mixed; required): Primary curation objective.
- `TARGET_SCOPE` (docs-folder|repo|subtree; required): Doc scope to govern.
- `INVENTORY_SCOPE` (folder-tree|repo-wide|release-surface; required): How broad the lifecycle inventory and cleanup judgement should be.
- `DECISION_MODE` (conservative|balanced|aggressive; optional): How readily delete or deprecate actions may be recommended. Defaults to `conservative` when omitted.
- `CANONICAL_SURFACES` (list; optional; shape: {PATH, WHY_CANONICAL}): Docs that define the maintained public surface and should be favored when deduplicating or redirecting content.

## Input Contract Notes
- This skill owns lifecycle judgement for documentation, not README publication or runtime code edits.
- Use `conservative` when migration uncertainty is high or historical docs might still have readers.
- Put current public entry docs, current architecture docs, and current contributor workflow docs into CANONICAL_SURFACES when the repository has explicit maintainership rules.

## Structured Outputs
- `DOC_LIFECYCLE_MAP` (list; required; shape: {PATH, DECISION, CURRENT_READER, CURRENT_ROLE, EVIDENCE}): Keep/update/deprecate/delete judgement for each doc.
- `DURABLE_KNOWLEDGE_TRANSFERS` (list; required; shape: {FROM, TO, WHAT, WHY}): Knowledge that must move into maintained docs before any deletion.
- `DEPRECATION_ACTIONS` (list; required; shape: {PATH, REPLACEMENT, REMOVE_CONDITION, EVIDENCE}): Docs that should remain temporarily with explicit replacement and removal conditions.
- `DELETE_CANDIDATES` (list; required; shape: {PATH, WHY_SAFE, PRECONDITION}): Docs that are safe to delete after required knowledge transfer or replacement checks.
- `UPDATE_TARGETS` (list; required; shape: {PATH, WHY_UPDATE}): Docs whose topic still matters but whose names, paths, examples, procedures, or surface references are stale.

## Output Contract Notes
- Keep docs that explain the current public surface, current architecture, or current contributor workflow unless explicit evidence proves they are superseded.
- Update docs whose subject still matters but whose procedures, names, examples, or paths are stale.
- Deprecate docs when readers or migration paths still exist; include replacement and removal conditions, plus version or date when known.
- Delete docs only when no current reader remains, a canonical replacement exists or migration is unnecessary, and any durable knowledge has already moved.

## Primary Lens
- `primary_lens`: `nielsen-norman`
- `why`: Documentation curation succeeds when reader tasks, navigation clarity, and maintained ownership are explicit.

## Artifacts
- `artifacts_in`: doc-inventory.v2
- `artifacts_out`: doc-curation-report.v2

## Neutrality Rules
- Do not recommend delete simply because a doc is old.
- Do not hide migration needs inside a vague "cleanup" label.
- Separate lifecycle judgement from content-writing recommendations.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Show lifecycle decisions first:
- keep/update/deprecate/delete — file — why

Then show required follow-up:
- durable knowledge move — from → to — what moves
- deprecation notice — file — replacement / remove when
- delete candidate — file — why safe / what must happen first

Flag any boundary call that needs a human decision:
"Left [file] as update instead of delete — current reader need is still ambiguous."

## Execution Constraints
- Do not author the repo root README from this skill.
- Do not delete unfinished plan or task docs while TODO / DOING / BLOCKED work remains.
- Treat completed delivery-only artifacts as delete candidates only after durable knowledge is promoted into maintained docs.
- Prefer explicit canonical targets over broad merge-everything cleanup.
