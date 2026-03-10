---
name: ship-go-nogo
description: "Use when assessing release safety, rollout risk, compatibility impact, and rollback readiness. This is the renamed release judgement skill; use it for GO/NO-GO analysis, not for publication execution."
---

# Release Readiness

## Purpose
Judge release safety and rollback readiness.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: diff|repo |
 policy: evidence,safety-gates,quality-gates{compat,docs,security,tests},deterministic-output |
 lens: release-gatekeeper |
 output: md(contract=v1)]
```

## Use When
- Need rollout, blast-radius, or rollback judgement before release.
- Need GO/NO-GO decision grounded in release evidence.
- Need rollout, interface, and monitoring checks before deployment.

## Do Not Use When
- Need direct implementation or bug debugging.
- Need only repository or docs hygiene checks.
- Need actual branch, tag, or release publication execution.

## Required Inputs
- `RELEASE_SCOPE` (diff|repo|deployment-slice; required): Release scope under evaluation.
- `ROLLOUT_PLAN` (string; required): Intended rollout path.
- `ROLLBACK_PATH` (string; required): Rollback or stop strategy.
- `KNOWN_GATES` (list; optional; shape: {GATE, STATUS, EVIDENCE}): Known tests, docs, approval, compatibility, or security signals.

## Input Contract Notes
- RELEASE_SCOPE should stay bounded to the actual release candidate under consideration.
- ROLLOUT_PLAN and ROLLBACK_PATH should describe real operational paths, not aspirational placeholders.
- KNOWN_GATES should cite observable gate evidence rather than predicted success.

## Structured Outputs
- `BLAST_RADIUS` (string; required): Affected users, systems, or consumer radius.
- `ROLLBACK_CHECKLIST` (list; required; shape: {STEP, PURPOSE}): Rollback conditions and procedure.
- `RELEASE_DECISION` (go|no-go|blocked; required; allowed: go|no-go|blocked): Go, no-go, or blocked decision with rationale.

## Output Contract Notes
- RELEASE_DECISION should remain blocked when a required gate is unresolved rather than optimistic by default.
- ROLLBACK_CHECKLIST should describe actual recovery steps, not generic rollback slogans.
- BLAST_RADIUS should reflect the real release slice and consumer impact.

## Primary Lens
- `primary_lens`: `release-gatekeeper`
- `frame_name`: Repo-to-Release Gatekeeper
- `why`: Release decisions should center on blast radius, rollback readiness, and delivery stability signals.
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
- `artifacts_out`: release-decision.v1

## Neutrality Rules
- Separate observed release evidence from GO/NO-GO judgement.
- If rollback or monitoring evidence is missing, mark the decision as blocked.
- Do not imply release readiness when approval or safety gates are unresolved.

## Execution Constraints
- Do not mutate branches, tags, remotes, or release hosts from this skill.
- Keep rollout and rollback judgement explicit and evidence-backed.
- Do not convert hygiene or repository precondition gaps into hidden assumptions.

## Output Discipline
- `response_profile=release_decision`
- User-facing rendering is delegated to `respond`.
