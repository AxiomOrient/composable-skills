---
name: tidy-remove-legacy
description: "Use when a bounded scope contains unnecessary files, stale docs, completed planning artifacts, deprecated aliases, or obsolete glue that should be removed without widening into broad refactor work. Execute the cleanup, update direct references, and verify that no required surface was deleted by mistake."
---

# Tidy / Remove Legacy

## Purpose
Remove unnecessary legacy surface in a bounded scope, relink surviving references, and verify that the remaining public or runtime surface still matches the intended contract.

For documentation, do not treat "old" as a synonym for "delete". First classify each doc as `keep`, `update`, `deprecate`, or `delete`, then act only on the classes that justify removal.

## Default Program
```text
[stages: preflight>detect>implement>verify>review>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,correctness-first,quality-gates{tests,docs,compat},deterministic-output |
 lens: hickey-carmack |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need to delete unnecessary files, stale docs, completed planning artifacts, deprecated aliases, or obsolete glue in a bounded scope.
- Need direct references updated as part of the same cleanup pass.
- Need explicit verification that required surface still exists after the cleanup.

## Do Not Use When
- Need release-only hygiene review rather than file changes; use `release-check-hygiene`.
- Need a broad structural refactor plan rather than bounded cleanup execution; use `tidy-reorganize`.
- Need speculative simplification with no concrete legacy targets.

## Required Inputs
- `TARGET_SCOPE` (path|module|folder|repo; required): Bounded scope allowed for the cleanup.
- `LEGACY_TARGETS` (list; required; shape: {PATH_OR_PATTERN, WHY_LEGACY}): Concrete unnecessary files, stale docs, completed plan artifacts, aliases, patterns, or surfaces to remove or collapse.
- `CLEANUP_MODE` (delete-only|delete-and-relink|collapse-alias|mixed; required): Type of legacy cleanup to execute.
- `PRESERVE_SURFACE` (list; optional; shape: {PATH_OR_CONTRACT, WHY_MUST_SURVIVE}): Files, interfaces, or public surfaces that must remain intact.
- `VERIFICATION_MAP` (list; required; shape: {CHECK, ORDER, PASS_CONDITION}): Narrow-to-broad verification steps after cleanup.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Non-goals, compatibility rules, or rollout constraints.

## Input Contract Notes
- LEGACY_TARGETS must be concrete enough to verify removal or collapse without guessing.
- Completed implementation plans or task ledgers count as legacy only when the user or repository contract says they should no longer ship or remain in the working surface.
- PRESERVE_SURFACE should name the surfaces that would be expensive or dangerous to delete by mistake.
- Keep the cleanup bounded. If multiple unrelated legacy themes appear, split them into separate runs.

## Documentation Decision Ladder

Before deleting any documentation, classify it with this order of precedence:

1. `keep`
   - Keep docs that describe the current public surface, current runtime behavior, current architecture, or current contributor workflow.
   - Keep entry docs that help readers discover the project, such as root `README.md`, runtime `skills/README.md`, support docs, contribution docs, and docs that explain the project's core artifact.
   - In a repository whose product is "skills", documentation that explains those skills is product documentation by default, not legacy.
2. `update`
   - Update docs that still serve a current audience but contain stale names, stale paths, stale examples, or outdated workflow details.
   - Prefer update over delete when the topic is still valid but the wording is behind the code.
3. `deprecate`
   - Deprecate docs when the thing they describe is still temporarily supported, still needed for migration, or still relevant to users on a supported older path.
   - Mark deprecation explicitly with replacement path, removal condition, and if possible a target version or milestone.
4. `delete`
   - Delete only when the content has no current audience, duplicates another source of truth, describes removed and unsupported behavior with no migration need, or is a delivery-only artifact the repo contract says must not ship.

## Documentation-Specific Rules

- Wrong docs are worse than missing docs. If a doc is inaccurate but still covers a live topic, prefer `update` or temporary `deprecate`, not silent retention.
- Keep one source of truth per topic. If two docs say the same thing, keep the discoverable canonical one and delete or redirect the duplicate.
- Preserve discoverability. If a doc is the shortest path for a user to understand what the project is, how it is used, or where deeper docs live, do not delete it without a replacement path.
- Preserve documentation mode boundaries. Reference, explanation, how-to, and tutorial content should be separated by purpose; mixed docs should usually be split or rewritten before deletion is considered.

## Planning Artifact Rules

- Keep plan docs such as `plans/IMPLEMENTATION-PLAN.md` and `plans/TASKS.md` while the work is active, queued, blocked, or still used by execution workflows.
- Do not delete plan docs when any task row is still `TODO`, `DOING`, or `BLOCKED`, or when an execution workflow like `workflow-build-execute-plan` still depends on them.
- Delete delivery-only planning docs only after all tasks are done and the repository contract says they must not ship in release commits.
- If a completed plan still contains reusable project knowledge, convert that durable knowledge into a permanent doc first, then delete the delivery-only artifact.

## Evidence Requirements For Doc Deletion

Do not delete a doc unless you can point to at least one of:

- a newer canonical doc that supersedes it
- repository policy that says the artifact is temporary and must not ship
- code or surface removal that makes the doc factually dead
- absence of active workflow or user path that still needs it

If those checks are incomplete, mark a verification gap instead of deleting.

## Structured Outputs
- `CLEANUP_CHANGES` (list; required; shape: {PATH, ACTION, WHY}): Files or surfaces removed, collapsed, or updated.
- `REFERENCE_UPDATES` (list; required; shape: {PATH, CHANGE, WHY}): Direct references updated because of the cleanup.
- `VERIFICATION_RESULTS` (list; required; shape: {CHECK, RESULT, EVIDENCE}): Executed checks and outcomes.
- `VERIFICATION_GAPS` (list; required; shape: {PATH_OR_CHECK, GAP, CHEAPEST_NEXT_CHECK}): Anything that could not be fully verified after cleanup.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Legacy cleanup should remove dead surface with the smallest explicit change set, keep surviving contracts visible, and avoid turning cleanup into a disguised refactor spree.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: implementation-delta.v1

## Neutrality Rules
- Do not label something legacy without file, reference, or contract evidence.
- Keep removed surface separate from follow-up improvement ideas.
- If a target might still be live, record the verification gap instead of deleting on assumption.
- For docs, prefer `update` over `delete` unless deletion has stronger evidence than preservation.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Show what was removed or collapsed:
- [path or surface] — action: [deleted/collapsed/relinked] — why: [legacy reason]

Show reference updates: [file] — change: [what was updated]

Show verification results: [check] — result: PASS / FAIL

Flag any gaps: "[path or check] could not be fully verified — need: [가장 빠른 다음 확인 방법]"

Ask about any boundary decision if cleanup scope was deliberately constrained.

## Execution Constraints
- Delete or collapse only the legacy surface named in LEGACY_TARGETS unless a directly dependent reference must change for correctness.
- Prefer removing the smallest obsolete surface that restores clarity; do not widen into unrelated renames or reshaping.
- If cleanup reveals a larger architectural problem, stop at the bounded cleanup and record the next structural step separately.
- When the target is documentation, run the decision ladder explicitly and state the chosen class (`keep`, `update`, `deprecate`, or `delete`) before editing files.
