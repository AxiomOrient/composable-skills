---
name: plan-what-it-does
description: "Use when writing implementation-ready feature specifications with explicit scope, required behavior, acceptance scenarios, and edge cases. Do not use for high-level product briefs, information architecture, or technical solution design. English triggers: feature spec, requirements spec, functional specification."
---

# Feature Spec

## Purpose
Write feature specifications that make required behavior, non-requirements, acceptance scenarios, and edge cases explicit before implementation.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>reflect>handoff>audit |
 scope: repo|paths(glob,...) |
 policy: evidence,quality-gates{docs,compat},deterministic-output |
 lens: minto-pyramid |
 output: md(contract=v1)]
```

## Use When
- Need a build-ready feature or flow specification.
- Need explicit functional requirements, non-requirements, and acceptance scenarios.
- Need to lock edge cases and failure expectations before implementation starts.

## Do Not Use When
- Need direct code changes.
- Need only high-level problem framing before requirements are known.
- Need information architecture or technical solution design rather than feature behavior.
- Need only verification sequencing or exhaustive test case inventory.

## Required Inputs
- `FEATURE_SCOPE` (feature|screen|flow|api|module; required): Boundary the feature spec governs.
- `USER_OUTCOME` (string; required): Core user-visible or contract-visible outcome the feature must enable.
- `REQUIRED_BEHAVIORS` (list; required; shape: {ID, BEHAVIOR, WHY}): Concrete in-scope behaviors the implementation must satisfy.
- `ACCEPTANCE_SCENARIOS` (list; required; shape: {SCENARIO, EXPECTED_RESULT}): Observable acceptance scenarios and expected results.
- `OUT_OF_SCOPE` (list; optional; shape: {ITEM, WHY_OUT}): Explicit exclusions so the feature boundary stays stable.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Compatibility, rollout, performance, policy, or non-goal constraints.

## Input Contract Notes
- USER_OUTCOME should describe one core outcome, not a blended roadmap.
- REQUIRED_BEHAVIORS should stay implementation-neutral unless a contract requires a specific interface or protocol.
- ACCEPTANCE_SCENARIOS should be externally observable and testable, not vague quality wishes.
- Use OUT_OF_SCOPE to prevent adjacent nice-to-have work from silently entering the spec.

## Structured Outputs
- `SPEC_SUMMARY` (string; required): One concise summary of the feature scope, outcome, and most important constraints.
- `FUNCTIONAL_REQUIREMENTS` (list; required; shape: {ID, REQUIREMENT, WHY}): Ordered functional requirements derived from the explicit in-scope behaviors.
- `ACCEPTANCE_CRITERIA` (list; required; shape: {CHECK, SOURCE}): Concrete checks that make implementation readiness and verification explicit.
- `EDGE_CASES` (list; required; shape: {CASE, EXPECTED_BEHAVIOR}): Important exception, failure, or edge cases that must be handled.
- `NON_REQUIREMENTS` (list; required; shape: {ITEM, WHY_OUT}): Explicitly excluded work or behaviors that must not be assumed from this spec.

## Output Contract Notes
- FUNCTIONAL_REQUIREMENTS should be testable statements, not vague aspirations or design slogans.
- ACCEPTANCE_CRITERIA should map back to explicit behaviors or scenarios rather than inventing new scope.
- EDGE_CASES should capture boundary and failure behavior without drifting into full technical design.
- NON_REQUIREMENTS should stay visible so the document resists scope creep.

## Primary Lens
- `primary_lens`: `minto-pyramid`
- `frame_name`: Answer-First Structurer
- `why`: Feature specs should lead with the scope-defining answer, then group requirements, exclusions, and acceptance checks into one testable hierarchy.
- `summary`: Lead with the answer, group supporting points logically, and make scope and evidence hierarchy explicit.
- `thesis`: A useful contract starts with the answer, then groups supporting points so scope, decision logic, and acceptance boundaries are immediately visible.
- `decision_rules`:
  - State the answer or contract first before details.
  - Group supporting points into stable buckets instead of chronological narration.
  - Make in-scope, out-of-scope, and done criteria explicit.
  - Remove sections that do not change the decision or acceptance boundary.
- `anti_patterns`:
  - Context dump before conclusion
  - Checklist without grouping logic
  - Mixed scope and acceptance criteria
- `good_for`:
  - clarification
  - spec writing
  - documentation
  - scope contracts
  - commit summaries
- `not_for`:
  - root-cause debugging
  - failure-path investigation
  - throughput optimization
- `required_artifacts`:
  - Answer First
  - Grouped Arguments
  - Scope Boundary
  - Acceptance Boundary
- `references`:
  - https://barbaraminto.com/

## Artifacts
- `artifacts_in`: scope-contract.v1, plan-why-build-this.v1
- `artifacts_out`: spec-contract.v1

## Neutrality Rules
- Separate required behavior from optional design preference.
- Mark unresolved spec edges explicitly.
- Keep every requirement implementable and testable.
- Do not imply architecture, IA, or rollout decisions unless the input evidence makes them explicit.

## Execution Constraints
- Do not write technical solution design or navigation structure from this skill; keep the document centered on feature behavior and acceptance boundaries.
- Do not turn this skill into a verification-order plan or regression test matrix; reference those only when the spec requires them.
- Prefer the smallest complete requirement set that satisfies the user outcome and explicit constraints.
- If an important behavior cannot be specified precisely yet, record it as an open edge instead of smoothing it into confident prose.

## Example Invocation
```text
$plan-what-it-does
FEATURE_SCOPE: flow
USER_OUTCOME: 사용자가 이메일 링크로 비밀번호를 재설정할 수 있어야 한다
REQUIRED_BEHAVIORS:
  - ID: FR-1
    BEHAVIOR: 유효한 토큰이면 새 비밀번호 입력 화면을 보여준다
    WHY: 재설정 흐름 진입점이 필요하다
ACCEPTANCE_SCENARIOS:
  - SCENARIO: 만료되지 않은 토큰으로 접근
    EXPECTED_RESULT: 비밀번호 입력 폼이 노출된다
```

## Output Discipline
- `response_profile=spec_contract`
- User-facing rendering is delegated to `respond`.
