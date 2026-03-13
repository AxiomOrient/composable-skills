---
name: tidy-remove-legacy
description: "Use when a bounded scope contains unnecessary files, stale docs, completed planning artifacts, deprecated aliases, or obsolete glue that should be removed without widening into broad refactor work. Execute the cleanup, update direct references, and verify that no required surface was deleted by mistake."
---

# Tidy / Remove Legacy

## Purpose
Remove unnecessary legacy surface in a bounded scope, relink surviving references, and verify that the remaining public or runtime surface still matches the intended contract.

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

## Response Format

Show what was removed or collapsed:
- [path or surface] — action: [deleted/collapsed/relinked] — why: [legacy reason]

Show reference updates: [file] — change: [what was updated]

Show verification results: [check] — result: PASS / FAIL

Flag any gaps: "[path or check] could not be fully verified — need: [cheapest next check]"

Ask about any boundary decision if cleanup scope was deliberately constrained.

## Execution Constraints
- Delete or collapse only the legacy surface named in LEGACY_TARGETS unless a directly dependent reference must change for correctness.
- Prefer removing the smallest obsolete surface that restores clarity; do not widen into unrelated renames or reshaping.
- If cleanup reveals a larger architectural problem, stop at the bounded cleanup and record the next structural step separately.
