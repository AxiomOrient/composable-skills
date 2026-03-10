---
name: ship-check-hygiene
description: "Use when release readiness depends on legacy removal, document freshness, and public-surface sync. Do not use for branch mutation or rollout-risk judgement."
---

# Release Hygiene Check

## Purpose
Verify release hygiene gates such as required docs, stale or legacy surface removal, and registry-to-doc sync before release judgement or publication.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: diff|repo |
 policy: evidence,safety-gates,quality-gates{docs,release,registry},deterministic-output |
 lens: release-gatekeeper |
 output: md(contract=v1)]
```

## Use When
- Need to confirm required release docs are upgraded before shipping.
- Need to check that legacy files, stale docs, or removed public skills are actually cleaned up.
- Need explicit evidence that registry, user docs, and public surface still agree.

## Do Not Use When
- Need git branch, tag, or remote state only; use ship-check-repo instead.
- Need rollout risk or rollback judgement; use ship-go-nogo instead.
- Need to rewrite docs directly; use doc-write, doc-curate, or doc-publish-readme instead.

## Required Inputs
- `HYGIENE_SCOPE` (diff|repo; required; allowed: diff|repo): Release hygiene scope under inspection.
- `REQUIRED_DOCS` (list; optional; shape: {PATH, WHY_REQUIRED}): Docs that must be updated or present before release.
- `SURFACE_CONTRACTS` (list; optional; shape: {CONTRACT, SOURCE}): Public-surface contracts such as registry/docs parity or required path ownership.
- `LEGACY_PATTERNS` (list; optional; shape: {PATTERN, WHY_BLOCKING}): Names, files, or patterns that must not survive the release.

## Input Contract Notes
- REQUIRED_DOCS should list only release-blocking docs, not every nice-to-have document in the repository.
- SURFACE_CONTRACTS should be observable contracts, such as registry/docs parity or root README ownership, not abstract taste rules.
- LEGACY_PATTERNS is for concrete legacy removal checks, not for broad cleanup brainstorming.
- Prefer exact skill names, file paths, or anchored patterns over broad words such as 'release' that would match unrelated content.

## Structured Outputs
- `HYGIENE_FINDINGS` (list; required; shape: {ISSUE, LOCATION, EVIDENCE, BLOCKS_RELEASE}): Concrete hygiene problems such as stale docs, leftover legacy surface, or unsynced public references.
- `DOC_GATE_STATUS` (pass|blocked|inconclusive; required; allowed: pass|blocked|inconclusive): Whether required release docs are ready.
- `SURFACE_SYNC_STATUS` (pass|blocked|inconclusive; required; allowed: pass|blocked|inconclusive): Whether registry, skill docs, and user-facing docs stay in sync.
- `REQUIRED_CLEANUPS` (list; required; shape: {ACTION, WHY}): Bounded cleanup actions required before release.

## Output Contract Notes
- If required release docs are missing or stale, DOC_GATE_STATUS should be blocked instead of buried in a note.
- SURFACE_SYNC_STATUS should reflect observable mismatches only, such as registry/doc drift or surviving legacy names.
- REQUIRED_CLEANUPS should stay bounded and release-relevant rather than turning into a generic improvement backlog.
- HYGIENE_FINDINGS and REQUIRED_CLEANUPS may both be empty when docs and public surface are already clean.

## Primary Lens
- `primary_lens`: `release-gatekeeper`
- `frame_name`: Repo-to-Release Gatekeeper
- `why`: Release hygiene should be judged as delivery safety, not as optional cleanup, because stale docs and legacy public surface create real rollout risk.
- `summary`: Treat release as a sequence of explicit gates and judge only the gate in scope with concrete evidence.
- `thesis`: Release work becomes unsafe when repository facts, hygiene, readiness, and publication are collapsed into one blurry judgement. Name the gate in scope, verify it directly, and hand off unresolved gates explicitly.
- `core_philosophy`: Treat release as a chain of explicit gates. Check only the current gate, block on missing proof, and do not borrow confidence from adjacent gates.
- `mental_model`:
  - Name the exact release gate in scope before making any judgement.
  - Check only gate-specific evidence instead of mixing repository, hygiene, readiness, and publish signals together.
  - Use blocked or inconclusive when the current gate lacks proof instead of assuming a later gate will absorb the risk.
  - Hand off the next required release gate explicitly once the current gate is resolved.
- `decision_rules`:
  - Keep repository reality, hygiene, readiness, and publication in separate verdict buckets.
  - Judge the gate in scope from concrete evidence only.
  - Escalate missing required proof to blocked or inconclusive instead of optimistic release language.
  - Record the cheapest next gate or action rather than assuming downstream cleanup.
- `anti_patterns`:
  - Repository, docs, rollout, and publish claims merged into one verdict
  - Optimistic release language with unresolved gate evidence
  - Assuming success in one gate because a neighboring gate looks healthy
- `good_for`:
  - release repo checks
  - release hygiene gates
  - release readiness
  - release publication
- `not_for`:
  - feature implementation
  - broad product ideation
  - architecture cleanup unrelated to shipping
- `required_artifacts`:
  - Gate In Scope
  - Gate Evidence
  - Blocking Gap or Status
  - Next Gate or Action
- `references`:
  - https://dora.dev/
  - https://sre.google/sre-book/table-of-contents/

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
- Keep findings traceable to concrete files, paths, or public-surface contracts.

## Output Discipline
- `response_profile=analysis_report`
- User-facing rendering is delegated to `respond`.
