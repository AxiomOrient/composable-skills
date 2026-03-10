---
name: plan-how-to-build
description: "Use when turning approved requirements into a buildable technical design with explicit boundaries, data and control flow, decisions, trade-offs, and verification paths. Do not use for product briefs, IA maps, or pure feature requirements."
---

# Technical Design Doc

## Purpose
Translate approved product and feature intent into a buildable technical design that makes boundaries, flows, decisions, and verification explicit.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: repo|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat},deterministic-output |
 lens: hickey-carmack |
 output: md(contract=v1)]
```

## Use When
- Need a technical design before implementation starts.
- Need to make component boundaries, data flow, and trade-offs explicit.
- Need one design document that engineers can implement against and review.

## Do Not Use When
- Need only high-level product framing or user problem definition.
- Need only feature behavior, scope, and acceptance scenarios.
- Need only information hierarchy or navigation structure.
- Need only bounded dependency direction rules without a broader technical mechanism.

## Required Inputs
- `DESIGN_SCOPE` (feature|service|module|system; required): Boundary the technical design governs.
- `IMPLEMENTATION_GOAL` (string; required): Core behavior or capability the design must enable.
- `REQUIREMENT_SOURCES` (list; required; shape: {REF, WHY_RELEVANT}): Briefs, specs, or contracts that the design must satisfy.
- `SYSTEM_BOUNDARIES` (list; optional; shape: {BOUNDARY, RESPONSIBILITY}): Known components or boundaries that must appear in the design.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Compatibility, performance, migration, policy, or operational constraints.
- `ROLLBACK_OR_MIGRATION` (list; optional; shape: {STEP, WHY}): Rollback, migration, or rollout-sensitive steps that affect the design.

## Input Contract Notes
- REQUIREMENT_SOURCES should point to explicit upstream artifacts instead of relying on memory or broad verbal summaries.
- SYSTEM_BOUNDARIES may be partial, but the final design must still surface the real responsibilities it introduces or touches.
- CONSTRAINTS should name non-negotiable realities such as latency budgets, compatibility rules, or migration limits.
- Use ROLLBACK_OR_MIGRATION only when it materially shapes the design, not as a catch-all implementation checklist.

## Structured Outputs
- `DESIGN_SUMMARY` (string; required): One concise summary of the proposed design and its central trade-off.
- `BOUNDARY_MAP` (list; required; shape: {BOUNDARY, RESPONSIBILITY}): Components or boundaries and the responsibility each one owns.
- `DATA_AND_CONTROL_FLOW` (list; required; shape: {FLOW, INPUT, OUTPUT}): Important data or control flows that make the design understandable.
- `DECISIONS_AND_TRADEOFFS` (list; required; shape: {DECISION, CHOSEN_OPTION, TRADEOFF}): Key design decisions and what each decision costs or protects.
- `RISKS_AND_VERIFICATION` (list; required; shape: {RISK, CHECK}): Main implementation or rollout risks and the check that reduces each one.
- `MIGRATION_AND_ROLLBACK` (list; required; shape: {STEP, WHY}): Migration or rollback-sensitive steps that the design must respect.

## Output Contract Notes
- BOUNDARY_MAP should identify real ownership boundaries rather than generic layer names with no responsibilities.
- DATA_AND_CONTROL_FLOW should make the main mechanism visible enough that reviewers can reason about correctness and cost.
- DECISIONS_AND_TRADEOFFS should describe what was chosen and what was given up, not just restate the happy path.
- RISKS_AND_VERIFICATION should connect each risk to the cheapest meaningful check.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `frame_name`: Data-First Systems Pragmatist
- `why`: Technical design docs should make boundaries, data flow, side effects, and trade-offs explicit enough that implementation can stay simple and reviewable.
- `summary`: Data model first, explicit side effects, and explicit performance characteristics.
- `thesis`: Make the structure and cost of the system visible first, then prefer the simplest explicit mechanism that preserves correctness.
- `core_philosophy`: Start from the essential user-visible or contract-visible outcome, keep the mechanism explicit, and remove accidental complexity before adding more structure.
- `mental_model`:
  - Name the core outcome and invariant before changing code.
  - Make data shape, side effects, and cost visible enough to reason about.
  - Choose the smallest explicit change that satisfies the contract.
  - Add abstraction only when it removes proven duplication or protects a real invariant.
- `decision_rules`:
  - Model the system in data before proposing structure or abstraction.
  - Separate transformations from side effects and name the boundary explicitly.
  - Prefer concrete mechanisms over clever indirection unless the abstraction removes real duplication or sharpens invariants.
  - Call out allocation, ownership, latency, and complexity characteristics when they matter to the decision.
- `anti_patterns`:
  - Decorative abstraction without a real invariant
  - Hidden state or hidden side effects
  - Recommendation without a visible cost model
- `good_for`:
  - implementation
  - simplification
  - duplication analysis
  - constant extraction
  - structure-heavy analysis
- `not_for`:
  - open-ended product messaging
  - user-empathy discovery
  - security governance by itself
- `required_artifacts`:
  - Data Model
  - Transformations vs Side Effects
  - Cost or Perf Notes
- `references`:
  - https://www.infoq.com/presentations/Simple-Made-Easy/
  - https://www.gdcvault.com/play/1022186/Keynote-Approaching-Zero-Driver

## Artifacts
- `artifacts_in`: plan-why-build-this.v1, spec-contract.v1, ia-map.v1
- `artifacts_out`: plan-how-to-build.v1

## Neutrality Rules
- Separate upstream requirements from the chosen solution mechanism.
- Do not invent architectural complexity when a simpler mechanism satisfies the stated constraints.
- If a design decision cannot be justified from the sources and constraints, mark it as an open decision instead of pretending it is settled.

## Execution Constraints
- Do not restate the entire product brief or feature spec; focus on how the system will satisfy the approved contract.
- Do not reduce this skill to a dependency-rule checklist when the only missing artifact is target dependency direction.
- Prefer the smallest design that satisfies the requirement sources and explicit constraints.
- Keep boundaries, side effects, and trade-offs explicit instead of hiding them in polished prose.

## Example Invocation
```text
$plan-how-to-build
DESIGN_SCOPE: feature
IMPLEMENTATION_GOAL: 비밀번호 재설정 토큰 검증과 새 비밀번호 저장을 안전하게 처리한다
REQUIREMENT_SOURCES:
  - REF: docs/specs/password-reset.md
    WHY_RELEVANT: 기능 요구사항과 예외 조건의 기준
CONSTRAINTS:
  - CONSTRAINT: 기존 사용자 테이블 스키마는 유지한다
```

## Output Discipline
- `response_profile=design_contract`
- User-facing rendering is delegated to `respond`.
