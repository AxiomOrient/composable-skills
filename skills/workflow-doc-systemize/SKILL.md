---
name: workflow-doc-systemize
description: "Workflow skill that inventories docs, classifies them by keep/update/deprecate/delete, and applies only the bounded doc updates or bridge docs that the lifecycle decision requires. Use when the user needs one default documentation governance entrypoint instead of manually chaining inventory, curation, and targeted writing."
---

# Workflow / Doc Systemize

## Purpose
Compose documentation inventory, lifecycle governance, and targeted doc writing into one default docs workflow.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat},deterministic-output |
 lens: nielsen-norman |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `nielsen-norman` because it keeps the work aligned with: Usability-first decisions, information scent, and explicit doc ownership before cleanup or rewriting.

## Use When
- Need one default docs entrypoint for broad documentation cleanup and governance.
- Need inventory, lifecycle judgement, and targeted updates to stay connected in one path.
- Need documentation work without runtime code changes.

## Do Not Use When
- Need only root README publishing.
- Need a recursive folder docset with parent README-style summaries and child project docs.
- Need release notes, changelog entries, or upgrade docs for a release.
- Need only one narrow documentation concern.
- Need runtime code changes.

## Required Inputs
- `TARGET_SCOPE` (path|docs-folder|repo|subtree; required): Documentation scope to systemize.
- `CURATION_GOAL` (lifecycle-governance|cleanup|surface-sync|mixed; required): Why the docs surface is being cleaned or governed.
- `AUDIENCE` (general|developer|operator|maintainer|mixed; required): Primary reader of the maintained docs surface.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Documentation constraints, non-goals, or protected surfaces.

## Input Contract Notes
- TARGET_SCOPE should be a real documentation surface, not a generic code subtree.
- Use this workflow when the main decision is "what survives and how should it be maintained".
- Use doc-publish-readme separately when the root README or publish surface must change.

## Structured Outputs
- `DOC_INVENTORY` (list; required; shape: {PATH, DOC_KIND, STATUS, ROLE_HINT, AUDIENCE_HINT, EVIDENCE}): Documentation inventory.
- `DOC_LIFECYCLE_MAP` (list; required; shape: {PATH, DECISION, CURRENT_READER, CURRENT_ROLE, EVIDENCE}): Lifecycle judgement across the docs surface.
- `WRITTEN_DOCS` (list; required; shape: {PATH, CHANGE_KIND, AUDIENCE, FORM}): Docs created or updated as part of the chosen lifecycle actions.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Atomic path executed by the workflow.

## Output Contract Notes
- DOC_INVENTORY should stay evidence based.
- DOC_LIFECYCLE_MAP should make keep/update/deprecate/delete explicit instead of burying it in prose.
- WRITTEN_DOCS should reflect only bounded follow-up docs such as refreshes, redirects, or deprecation notices.
- EXPANDED_ATOMIC_PATH must preserve execution order explicitly.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: doc-inventory.v2, doc-curation-report.v2, documentation-report.v2

## Neutrality Rules
- Preserve the neutrality rules of the underlying docs skills.
- Do not imply runtime code changes from a docs-only workflow.
- Keep inventory, lifecycle judgement, and writing outputs distinct.

## Execution Constraints
- Do not widen this workflow into root README publishing or release-doc authoring.
- Prefer explicit reader and role decisions over vague stale-doc labels.
- Apply only the bounded doc updates required by the lifecycle decision; do not turn cleanup into a generic rewrite marathon.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Show lifecycle outcome first, then writing:

```text
keep/update/deprecate/delete: `file` — [why]
updated: `file` — [what changed and why]
written: `file` — [new bridge or replacement doc added]
```

Gaps (couldn't verify or act yet):
- `file` — [why — e.g., no source content, ambiguous current reader]

Ask:
"Any doc here should be treated as canonical even if it looks stale?"

## Mandatory Rules
- Expose the expanded atomic path explicitly.
- Keep root README publication and release-doc authoring outside this workflow.

## Expansion
- `$doc-find-all`
- `$doc-curate`
- `$doc-write`

## Eval Cases

| Prompt | Should Trigger | Key Output Check |
|--------|---------------|-----------------|
| 오래된 문서들 정리하고 쓸모없는 건 지우거나 업데이트해줘. | YES | DOC_LIFECYCLE_MAP 존재 |
| 전체 문서 인벤토리 만들고 어떻게 관리할지 결정해서 수정해. | YES | DOC_INVENTORY 존재 |
| 코드랑 문서를 같이 고쳐줘. | NO | 문서 전용 워크플로우 — build-write-code 병행 권장 |
