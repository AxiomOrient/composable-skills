---
name: build-write-code
description: "Implementation-only skill. Apply code changes and produce verification-backed implementation evidence. Do not own orchestration, plan/task synchronization, architecture analysis reports, or code-review verdicts here. English triggers: implement, code change, feature build, bug fix."
---

# Write Code

## Purpose

Apply code changes for explicit task ids and produce verification-backed implementation evidence.

## Default Program

```text
[stages: preflight>detect>implement>verify>review>audit |
 scope: diff |
 policy: evidence,correctness-first,safety-gates,approval-gates{explicit,no-fallback},deterministic-output |
 lens: hickey-carmack |
 output: md(contract=v1)]
```

## Use When

- Need to apply real code changes for a bounded task.
- Need to emit implementation evidence that downstream delivery flow can synchronize with plan/task artifacts.
- Need explicit verification evidence after code changes.

## Do Not Use When

- Need only analysis or review output.
- Need only verification-map design before patching.
- Need release-only or review-only judgement.

## Required Inputs

- `CHANGE_GOAL` (string; required): Exact behavior or structure to change.
- `TARGET_SCOPE` (path|module|folder|repo; required): Scope of the code changes.
- `TASK_IDS` (list; required; shape: {TASK_ID}): Selected task ids from docs/TASKS.md.
- `TASK_SOURCE` (tasks-md|explicit-user|adhoc; optional; allowed: tasks-md|explicit-user|adhoc): Where TASK_IDS came from. Use `adhoc` only when no task ledger exists and keep ids stable for this run.
- `VERIFICATION_MAP` (list; required; shape: {CHECK, ORDER, PASS_CONDITION}): Narrow-to-broad verification steps.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Safety, rollout, compatibility, or non-goal constraints.

## Input Contract Notes

- CHANGE_GOAL should describe one bounded implementation target, not a mixed backlog.
- TASK_IDS must be stable ids. If docs/TASKS.md is absent, use TASK_SOURCE=`adhoc` with ids like `adhoc/skill-contract-sync`.
- VERIFICATION_MAP must be ordered narrow-to-broad so the skill can stop claiming success when early checks fail.
- CHANGE_GOAL should name the core user-visible or contract-visible effect to achieve, not bundle optional polish, speculative abstraction, or unrelated cleanup.
- If simplicity or scope discipline matters, state it explicitly in CONSTRAINTS so the implementation can reject non-essential cleanup and incidental expansion.

## Structured Outputs

- `CHANGED_ARTIFACTS` (list; required; shape: {PATH, CHANGE_KIND, WHY}): Files or artifacts changed by the implementation.
- `VERIFICATION_RESULTS` (list; required; shape: {CHECK, RESULT, EVIDENCE}): Executed checks and outcomes.
- `VERIFICATION_GAPS` (list; required; shape: {PATH_OR_CHECK, GAP, CHEAPEST_NEXT_CHECK}): Explicit verification gaps when a changed artifact or planned check could not be fully verified.
- `IMPLEMENTATION_EVIDENCE_NOTES` (list; required; shape: {TASK_ID, NOTE, EVIDENCE}): Implementation-local evidence notes that downstream delivery utilities can attach to task artifacts.

## Output Contract Notes

- Each CHANGED_ARTIFACTS item must be justified by at least one VERIFICATION_RESULTS or VERIFICATION_GAPS row.
- Use VERIFICATION_GAPS instead of burying incomplete checks inside prose.
- IMPLEMENTATION_EVIDENCE_NOTES must reference the same TASK_IDS provided in the input.
- Keep CHANGED_ARTIFACTS proportional to the stated CHANGE_GOAL; broader cleanup needs an explicit correctness, clarity, or maintenance justification.

## Primary Lens

- `primary_lens`: `hickey-carmack`
- `frame_name`: Data-First Systems Pragmatist
- `why`: Implementation should make data models, side effects, and cost visible, then choose the simplest change that satisfies the core user outcome and explicit contract. Simplicity and focus on the essential behavior matter more than decorative structure.
- `summary`: Simplicity first, explicit side effects, and a visible cost model.
- `thesis`: Start from the essential outcome, not file size. A long file is not automatically a God Object; split when responsibilities, cohesion, or reasons to change diverge.
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
  - Treat line count as a warning signal only; judge God Object risk by multiple responsibilities, low cohesion, and too many reasons to change.
  - If a change would push one module into unrelated responsibilities, extract or split by responsibility before adding more branches, state, or helpers.
  - Call out allocation, ownership, latency, and complexity characteristics when they matter to the decision.
- `anti_patterns`:
  - Decorative abstraction without a real invariant
  - Hidden state or hidden side effects
  - One module accumulating unrelated responsibilities because "it is already the place that does this kind of thing"
  - LOC-only panic refactors with no responsibility boundary
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
  - Reason to Change Boundary

## Artifacts

- `artifacts_in`: verification-map.v1, implementation-plan.md.v1, tasks.md.v1
- `artifacts_out`: implementation-delta.v1

## Neutrality Rules

- Do not claim success without verification evidence.
- Separate implemented change from deferred improvement.
- If verification is incomplete, mark the gap explicitly.

## Execution Constraints

- Do not synchronize plan/task markdown from this skill; emit implementation evidence only.
- Keep edits inside TARGET_SCOPE unless a narrowly justified support change is required for correctness or verification.
- Do not mark the change complete while VERIFICATION_GAPS still contain core contract failures.
- Prefer the simplest change that satisfies the explicit contract and core user outcome; avoid decorative abstraction, speculative structure, or non-essential side work.
- Focus on the essential behavior first. Only include extra cleanup when it directly improves correctness, clarity, or maintainability for the same contract.
- If implementation would turn a file into a multi-responsibility sink, split by responsibility instead of extending a growing God Object.
- Do not call something a God Object from LOC alone; use single-responsibility, cohesion, and reason-to-change signals.

## Mandatory Rules

- Do not synchronize plan/task markdown here; emit implementation evidence only.
- Every changed artifact must be paired with at least one verification result or an explicit verification gap.

## Output Discipline

- `response_profile=implementation_delta`
- User-facing rendering is delegated to `respond`.
