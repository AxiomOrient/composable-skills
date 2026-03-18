---
name: docs-sync
description: "Compare repository behavior, configuration, and plans against the docs surface to find missing, stale, or wrong documentation. Use when code changed and you need a doc audit, patch plan, or approval-ready doc sync report."
---
# Docs Sync

## Purpose
Keep repository knowledge legible by comparing the real code, config, and execution artifacts against the current documentation surface, then reporting or applying only the doc changes that are actually warranted.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{docs,links},deterministic-output |
 lens: craft-clarity |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `craft-clarity` because it keeps the work aligned with: reader-usable documentation, explicit stale points, and the smallest revision that restores clarity.

## Use When
- Need a docs audit after code, configuration, CLI, or workflow changes.
- Need to compare `AGENTS.md`, architecture notes, plans, and docs against the actual repository.
- Need an approval-ready docs sync report before editing documentation.

## Do Not Use When
- Need feature design before implementation.
- Need a release-only checklist with no doc comparison.
- Need to rewrite documentation style without checking implementation truth first.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo|diff; required): Scope whose documentation may now be stale.
- `DOC_SURFACE` (path|repo-docs; required): Docs surface to inspect, such as `docs/`, root design notes, or architecture files.
- `SYNC_MODE` (audit-only|propose-edits|apply-approved; required): Whether to only audit, propose changes, or apply already-approved edits.
- `REFERENCE_ARTIFACTS` (list; optional; shape: {REF, WHY_RELEVANT}): Plans, specs, generated schema docs, or workflow files that define the source of truth.

## Input Contract Notes
- `DOC_SURFACE` should include both root guidance files and deeper docs when both matter.
- `SYNC_MODE` should reflect editing authority explicitly; do not assume edits are approved.
- `REFERENCE_ARTIFACTS` should name the artifacts that now define truth after the latest change.

## Structured Outputs
- `DOC_SYNC_REPORT` (list; required; shape: {DOC_FILE, STATUS, ISSUE, EVIDENCE, PROPOSED_CHANGE}): Page-by-page findings.
- `MISSING_DOCS` (list; required; shape: {TOPIC, EVIDENCE, SUGGESTED_LOCATION}): Important topics missing from the docs surface.
- `STALE_DOCS` (list; required; shape: {DOC_FILE, STALE_CLAIM, CORRECT_INFO, EVIDENCE}): Existing docs that drifted from reality.
- `PATCH_PLAN` (list; required; shape: {FILE, CHANGE, WHY}): Minimal doc edits required to restore alignment.

## Output Contract Notes
- `DOC_SYNC_REPORT` should separate missing, stale, and structurally misplaced documentation.
- `MISSING_DOCS` should point to the best insertion point instead of only naming the topic.
- `STALE_DOCS` should quote the outdated claim in a paraphrased form precise enough to patch.
- `PATCH_PLAN` should stay minimal and executable.

## Primary Lens
- `primary_lens`: `craft-clarity`
- `why`: Documentation sync should optimize for reader-usable truth, not volume.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: docs-sync-report.v1

## Response Format
Think and operate in English, but deliver the final response in Korean.
Lead with one line:
`Docs sync: aligned|drifted|partial — scope: [TARGET_SCOPE]`

Then show:
- Doc-first findings: file → issue → evidence.
- Code-first gaps: topic → evidence → best doc location.
- Patch plan: smallest file-level edits that restore accuracy.
- Approval note: only when `SYNC_MODE` is `audit-only` or `propose-edits`.

If no material drift exists, say:
`No material doc drift found in the stated scope.`

## Neutrality Rules
- Do not equate documentation presence with documentation correctness.
- Keep source-of-truth evidence explicit; never patch docs from memory alone.
- Do not expand the patch plan into a style rewrite unless the stale state requires it.

## Execution Constraints
- Prefer repo-owned docs and plans over external memory or chat context.
- When `SYNC_MODE` is not `apply-approved`, stop at the audit plus patch plan.
- Generated reference docs should be fixed at the generating source when possible instead of hand-editing generated output.

## References
- `references/docs-sync-report-template.md`
- `references/doc-scope-checklist.md`

## Example Invocation
```text
$docs-sync TARGET_SCOPE: src/session DOC_SURFACE: docs/ SYNC_MODE: propose-edits REFERENCE_ARTIFACTS:
- REF: AGENTS.md
  WHY_RELEVANT: project-level operating rules live here
- REF: docs/exec-plans/active/session-refresh.md
  WHY_RELEVANT: current source of truth for the in-flight change
```
