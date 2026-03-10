---
name: check-module-walls
description: "Check whether module, API, or layer boundaries expose unclear contracts, hidden assumptions, or leaking responsibilities. Use when the goal is to verify boundaries rather than perform broad review."
---

# Boundary Contract Check

## Purpose
Verify that a bounded interface or module boundary has explicit contracts and does not leak hidden assumptions.

## Default Program
```text
[stages: preflight>detect>analyze>review>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: uncle-bob | output: md(contract=v1)]
```

## Use When
- Need to check whether a module or API boundary is explicit enough.
- Need to verify ownership and responsibility separation across layers.
- Need evidence of contract leaks before refactoring or review.

## Do Not Use When
- Need a broad code review across unrelated concerns.
- Need direct implementation rather than contract analysis.
- Have no bounded interface or module boundary to inspect.

## Required Inputs
- `TARGET_SCOPE` (path|module|api; required): Boundary to inspect.
- `BOUNDARY_KIND` (module|api|service|layer; required): Kind of boundary being checked.

## Input Contract Notes
- TARGET_SCOPE should identify one concrete interface, module, or boundary slice rather than a broad subsystem.
- BOUNDARY_KIND should describe the actual contract surface being inspected, not the desired architecture outcome.

## Structured Outputs
- `BOUNDARY_CONTRACTS` (list; required; shape: {CONTRACT, STATUS, EVIDENCE}): Current explicit or implicit contracts found at the boundary.
- `LEAKED_ASSUMPTIONS` (list; required; shape: {ASSUMPTION, LOCATION, WHY_LEAKING}): Assumptions or responsibilities leaking across the boundary.
- `HARDENING_ACTIONS` (list; required; shape: {ACTION, TARGET, WHY}): Specific actions to make the contract more explicit.

## Output Contract Notes
- Describe the current boundary contract before calling it weak or ambiguous.
- LEAKED_ASSUMPTIONS may be empty when the inspected boundary is already explicit enough.
- HARDENING_ACTIONS should stay local to the boundary instead of expanding into a whole-system redesign.

## Procedure
1. List the explicit inputs, outputs, and invariants at the target boundary.
2. Identify hidden assumptions, side-channel coupling, or leaked ownership.
3. Return concrete hardening actions that clarify the contract without redesigning the whole system.

## Primary Lens
- `primary_lens`: `uncle-bob`
- `frame_name`: Boundary-and-Dependency Steward
- `why`: Boundary checks should focus on dependency direction, contract clarity, and leak prevention.
- `summary`: Strong boundaries and maintainable architecture with explicit dependency direction.
- `thesis`: When modules are hard to change safely, first make dependency direction and contract boundaries visible, then remove leaks and forbidden couplings.
- `decision_rules`:
  - State boundary type and dependency direction explicitly.
  - Check whether policy depends on detail or detail depends on policy.
  - Treat leaked assumptions across layers as contract defects.
  - Prefer hardening the boundary before adding new behavior.
- `anti_patterns`:
  - Ambiguous layer ownership
  - Cross-boundary knowledge leaks
  - Dependency plans that omit forbidden coupling
- `good_for`:
  - boundary checks
  - dependency rule planning
  - architectural hygiene
- `not_for`:
  - user-facing document curation
  - answer forecasting
  - throughput baselining
- `required_artifacts`:
  - Boundary Map
  - Dependency Direction
  - Contract Hardening Actions
- `references`:
  - https://blog.cleancoder.com/

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: boundary-contract-report.v1

## Neutrality Rules
- Describe the current contract before judging it weak or unclear.
- Separate proven contract leaks from speculative design concerns.
- Recommend only the hardening needed to clarify the boundary.

## Execution Constraints
- Keep the check bounded to the named boundary and its immediate callers or callees.
- Do not turn general naming or style preferences into boundary defects without contract evidence.
- Prefer explicit contract hardening over architectural expansion.

## Mandatory Rules
- Do not label a boundary broken without evidence of leakage or ambiguity.
- Keep recommendations bounded to the inspected contract.

## Example Invocation
```text
$check-module-walls
TARGET_SCOPE: src/api/user-service.ts
BOUNDARY_KIND: service
```

## Output Discipline
- `response_profile=review_findings`
- User-facing rendering is delegated to `respond`.
