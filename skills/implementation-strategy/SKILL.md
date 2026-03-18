---
name: implementation-strategy
description: "Decide the simplest safe implementation path before editing compatibility-sensitive code. Use when a task may affect APIs, config, schemas, durable state, or migration boundaries and you need an explicit rewrite-vs-shim decision."
---
# Implementation Strategy

## Purpose
Choose the smallest implementation that satisfies the current task while protecting real released boundaries and calling out the cases that need migration or explicit confirmation.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{compat,docs},deterministic-output |
 lens: hickey-carmack |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: visible contracts, explicit side effects, and the simplest mechanism that preserves correctness.

## Use When
- Need to decide whether a change can be rewritten directly or needs compatibility handling.
- Need to judge a proposed change against the latest real release boundary instead of branch churn.
- Need to make migration, rollback, or durable-state risk explicit before coding.

## Do Not Use When
- Need only a product brief or feature spec.
- The change is obviously internal and has no meaningful compatibility surface.
- The work is already implemented and you only need verification or PR summary.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Where the change will land.
- `CHANGE_INTENT` (string; required): The behavior or interface that is about to change.
- `CHANGE_SURFACE` (public-api|runtime|schema|protocol|cli|config|internal|mixed; required): What boundary the change touches.
- `RELEASE_BOUNDARY_HINT` (tag|commit|none; optional): Known latest release boundary when already established.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Compatibility, rollout, migration, or user constraints.

## Input Contract Notes
- `CHANGE_SURFACE` should classify the boundary being changed, not the preferred solution.
- `RELEASE_BOUNDARY_HINT` is only a hint; verify the real release boundary from the repo when possible.
- `CONSTRAINTS` should call out non-negotiables such as stable config names, persisted data, or zero-downtime rollout.

## Structured Outputs
- `COMPATIBILITY_BOUNDARY` (list; required; shape: {BOUNDARY, BASIS, RISK_LEVEL}): What must remain stable and why.
- `IMPLEMENTATION_STANCE` (list; required; shape: {DECISION, WHY, WHAT_TO_UPDATE_DIRECTLY}): Direct rewrite vs shim/migration decision.
- `MIGRATION_REQUIREMENTS` (list; required; shape: {STEP, WHY, CAN_SKIP_IF}): Migrations or adapters that are truly required.
- `STOP_AND_CONFIRM` (list; required; shape: {TRIGGER, WHY_CONFIRMATION_IS_NEEDED}): Cases that require explicit user confirmation before editing.

## Output Contract Notes
- `COMPATIBILITY_BOUNDARY` should be judged against a real release boundary whenever possible.
- `IMPLEMENTATION_STANCE` should prefer direct rewrite when the old shape is unreleased or internal.
- `MIGRATION_REQUIREMENTS` should only exist when there is a real durable or released boundary to protect.
- `STOP_AND_CONFIRM` should stay narrow and concrete.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Strategy should favor explicit contracts and the simplest safe mechanism.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: implementation-strategy.v1

## Response Format
Think and operate in English, but deliver the final response in Korean.
Lead with one line:
`Implementation stance: direct-rewrite|compat-layer|migration-needed — boundary: [released|branch-local|mixed]`

Then show:
- Compatibility boundary.
- Decision and rationale.
- Required migrations or adapters, if any.
- Stop-and-confirm triggers.

If no compatibility-sensitive boundary exists, say:
`No released compatibility boundary found in the stated scope; direct rewrite is preferred.`

## Neutrality Rules
- Do not preserve an unreleased abstraction just because it already exists on the branch.
- Do not call a change breaking without tying it to a real released or durable external boundary.
- Prefer deletion or replacement over aliases, shims, and dual-write logic when the old shape is not actually owed support.

## Execution Constraints
- Judge risk against the latest meaningful release boundary, not against unreleased main-branch churn.
- Update callers, tests, docs, and examples directly when a direct rewrite is justified.
- Escalate only when the change touches a released API, durable external data, or a user explicitly asks for backward compatibility.

## References
- `references/compatibility-boundary-checklist.md`
- `references/migration-decision-rules.md`

## Example Invocation
```text
$implementation-strategy TARGET_SCOPE: src/session CHANGE_INTENT: rename session persistence fields and simplify restore logic CHANGE_SURFACE: schema CONSTRAINTS:
- CONSTRAINT: existing serialized session files may already exist in user environments
```
