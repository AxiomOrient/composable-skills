---
name: doc-find-all
description: "Inventory documentation files, infer their likely reader and role, and expose orphan, duplicate, time-sensitive, or delivery-only docs before curation. Use when the immediate job is evidence-backed inventory, not rewriting docs yet."
---

# Doc / Find All

## Purpose
Create an evidence-backed documentation inventory before lifecycle curation, docset building, or release-doc work.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{docs},deterministic-output |
 lens: nielsen-norman |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `nielsen-norman` because it keeps the work aligned with: Usability-first decisions based on explicit heuristics, scanning behavior, information scent, and reader-task alignment.

## Use When
- Need to know which docs are active, stale, duplicate, orphaned, delivery-only, or time-sensitive.
- Need a bounded documentation inventory before lifecycle decisions or rewrite work.
- Need reader-role evidence before recommending keep, update, deprecate, or delete.

## Do Not Use When
- Need to write the README, release notes, or guide content directly.
- Need runtime code changes.
- The target scope contains no documentation boundary worth inventorying.

## Required Inputs
- `TARGET_SCOPE` (path|docs-folder|repo; required): Documentation scope to inventory.
- `INVENTORY_GOAL` (cleanup|navigation|coverage|lifecycle|mixed; optional): Why the inventory is being created. Defaults to `mixed` when omitted.

## Input Contract Notes
- TARGET_SCOPE should be a real documentation set, not a broad repo area with no docs boundary.
- INVENTORY_GOAL should explain whether lifecycle judgement, navigation, or coverage matters most so the inventory can surface the right signals first.
- When INVENTORY_GOAL is omitted, default to `mixed`.

## Structured Outputs
- `DOC_INVENTORY` (list; required; shape: {PATH, DOC_KIND, STATUS, ROLE_HINT, AUDIENCE_HINT, EVIDENCE}): Document records with inferred role, likely reader, and evidence-backed status.
- `ORPHAN_OR_DUPLICATE_SET` (list; required; shape: {PATH, ISSUE, EVIDENCE}): Docs that appear orphaned, duplicated, or disconnected from the current surface.
- `TEMPORAL_RISK_SET` (list; required; shape: {PATH, RISK, EVIDENCE}): Docs whose wording, path references, version references, or procedures appear time-sensitive or stale.
- `NEXT_CURATION_TARGETS` (list; required; shape: {PATH, WHY_NEXT}): Highest-value docs to govern, rewrite, or prune next.

## Output Contract Notes
- DOC_INVENTORY should distinguish observed file state from inferred lifecycle risk.
- ROLE_HINT and AUDIENCE_HINT should stay explicitly tentative when the reader or role is not obvious.
- NEXT_CURATION_TARGETS should stay bounded to the immediate next doc work instead of a generic backlog.

## Primary Lens
- `primary_lens`: `nielsen-norman`
- `why`: Good doc inventory should reveal findability, duplication, reader fit, and stale-surface risk before cleanup begins.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: doc-inventory.v2

## Neutrality Rules
- Read docs before classifying them stale, duplicate, delivery-only, or unneeded.
- Keep delete or archive conclusions tentative until explicit lifecycle evidence exists.
- Separate navigation problems, content-quality problems, and lifecycle problems.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Show the inventory as a compact list:
- file — kind/status — likely reader/role — reason

Then list the highest-value curation targets:
- file — why now

Flag inventory gaps:
"Didn't check: [paths or areas outside scope]"

Ask:
"Want to govern lifecycle for [top target] first, build a folder docset, or prepare release docs?"

## Execution Constraints
- Do not rewrite docs from this skill; inventory only.
- Keep stale, duplicate, or delivery-only classifications tied to explicit evidence such as overlap, broken ownership, outdated references, or completed one-off delivery purpose.
- Prefer the smallest useful inventory that supports the stated inventory goal.

## Example Invocation
```text
$doc-find-all
TARGET_SCOPE: docs
INVENTORY_GOAL: lifecycle
```
