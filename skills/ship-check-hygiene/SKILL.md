---
name: ship-check-hygiene
description: "Use when release readiness depends on legacy removal, document freshness, and public-surface sync. Do not use for branch mutation or rollout-risk judgement."
---

# Ship / Check Hygiene

## Purpose

Verify release hygiene gates such as required docs, stale or legacy surface removal, and skill-metadata-to-doc sync before release judgement or publication.

## Default Program

```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: diff|repo |
 policy: evidence,safety-gates,quality-gates{docs,release,surface-sync},deterministic-output |
 lens: release-gatekeeper |
 output: md(contract=v1)]
```

## Use When

- Need to confirm required release docs are upgraded and delivery-only implementation docs are removed before shipping.
- Need to check that legacy files, stale docs, or removed public skills are actually cleaned up.
- Need explicit evidence that skill metadata, user docs, and public surface still agree.

## Do Not Use When

- Need git branch, tag, or remote state only; use ship-check-repo instead.
- Need rollout risk or rollback judgement; use ship-release-verdict instead.
- Need to rewrite docs directly; use doc-write, doc-curate, or doc-publish-readme instead.

## Required Inputs

- `HYGIENE_SCOPE` (diff|repo; required; allowed: diff|repo): Release hygiene scope under inspection.
- `REQUIRED_DOCS` (list; optional; shape: {PATH, WHY_REQUIRED}): Docs that must be updated or present before release and are expected to remain public after the release.
- `SURFACE_CONTRACTS` (list; optional; shape: {CONTRACT, SOURCE}): Public-surface contracts such as skill-metadata/docs parity or required path ownership.
- `LEGACY_PATTERNS` (list; optional; shape: {PATTERN, WHY_BLOCKING}): Names, files, or patterns that must not survive the release, including delivery-only implementation docs.

## Input Contract Notes

- REQUIRED_DOCS should list only release-blocking docs, not every nice-to-have document in the repository.
- SURFACE_CONTRACTS should be observable contracts, such as skill-metadata/docs parity or root README ownership, not abstract taste rules.
- LEGACY_PATTERNS is for concrete legacy removal checks, not for broad cleanup brainstorming.
- Delivery-only planning docs such as `plans/IMPLEMENTATION-PLAN.md` and `plans/TASKS.md` belong in LEGACY_PATTERNS so the hygiene gate can require their deletion before release.
- Prefer exact skill names, file paths, or anchored patterns over broad words such as 'release' that would match unrelated content.

## Structured Outputs

- `HYGIENE_FINDINGS` (list; required; shape: {ISSUE, LOCATION, EVIDENCE, BLOCKS_RELEASE}): Concrete hygiene problems such as stale docs, leftover legacy surface, or unsynced public references.
- `DOC_GATE_STATUS` (pass|blocked|inconclusive; required; allowed: pass|blocked|inconclusive): Whether required release docs are ready.
- `SURFACE_SYNC_STATUS` (pass|blocked|inconclusive; required; allowed: pass|blocked|inconclusive): Whether skill metadata, skill docs, and user-facing docs stay in sync.
- `REQUIRED_CLEANUPS` (list; required; shape: {ACTION, WHY}): Bounded cleanup actions required before release.

## Output Contract Notes

- If required release docs are missing or stale, DOC_GATE_STATUS should be blocked instead of buried in a note.
- SURFACE_SYNC_STATUS should reflect observable mismatches only, such as skill-metadata/doc drift or surviving legacy names.
- REQUIRED_CLEANUPS should stay bounded and release-relevant rather than turning into a generic improvement backlog.
- HYGIENE_FINDINGS and REQUIRED_CLEANUPS may both be empty when docs and public surface are already clean.

## Primary Lens

- `primary_lens`: `release-gatekeeper`
- `why`: Release hygiene should be judged as delivery safety, not as optional cleanup, because stale docs and legacy public surface create real rollout risk.

## Artifacts

- `artifacts_in`: none
- `artifacts_out`: release-hygiene-report.v1

## Neutrality Rules

- Do not invent hygiene blockers when docs and public surface evidence is clean.
- Treat missing release docs or stale public references as release risk, not as optional polish.
- Keep release-blocking hygiene issues separate from non-blocking cleanup ideas.

## Execution Constraints

- Do not edit files from this skill; it is a check-only release gate.
- If docs upgrade is required and not evidenced, block release instead of assuming the docs will catch up later.
- Treat delivery-only implementation docs as stale release surface unless they were explicitly promoted into maintained public docs.
- Keep findings traceable to concrete files, paths, or public-surface contracts.
