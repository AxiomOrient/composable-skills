---
name: build-write-code
description: "Implementation-only skill. Apply code changes and produce verification-backed implementation evidence. Do not own orchestration, plan/task synchronization, architecture analysis reports, or code-review verdicts here."
---

# Build / Write Code

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

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

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
- `IMPLEMENTATION_MODE` (bugfix|feature|refactor|integration|cleanup; optional; allowed: bugfix|feature|refactor|integration|cleanup): Implementation mode. Defaults to the narrowest mode implied by the change goal.
- `TARGET_SCOPE` (path|module|folder|repo; required): Scope of the code changes.
- `TASK_IDS` (list; optional; shape: {TASK_ID}): Selected task ids from plans/TASKS.md or synthesized adhoc ids when no task ledger exists.
- `TASK_SOURCE` (tasks-md|explicit-user|adhoc; optional; allowed: tasks-md|explicit-user|adhoc): Where TASK_IDS came from. Use `adhoc` only when no task ledger exists and keep ids stable for this run.
- `VERIFICATION_MAP` (list; required; shape: {CHECK, ORDER, PASS_CONDITION}): Narrow-to-broad verification steps.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Safety, rollout, compatibility, or non-goal constraints.

## Input Contract Notes
- CHANGE_GOAL should describe one bounded implementation target, not a mixed backlog.
- IMPLEMENTATION_MODE should classify the kind of implementation work without changing the core output contract.
- TASK_IDS should be stable ids when a task ledger exists. If plans/TASKS.md is absent, synthesize one stable `adhoc/...` id for this run and set TASK_SOURCE=`adhoc`.
- VERIFICATION_MAP must be ordered narrow-to-broad so the skill can stop claiming success when early checks fail.
- CHANGE_GOAL should name the core user-visible or contract-visible effect to achieve, not bundle optional polish, speculative abstraction, or unrelated cleanup.
- If simplicity or scope discipline matters, state it explicitly in CONSTRAINTS so the implementation can reject non-essential cleanup and incidental expansion.

## Structured Outputs
- `CHANGED_ARTIFACTS` (list; required; shape: {PATH, CHANGE_KIND, WHY}): Files or artifacts changed by the implementation.
- `VERIFICATION_RESULTS` (list; required; shape: {CHECK, RESULT, COMMAND_OR_TEST, EVIDENCE}): Executed checks, the exact command or test that ran, and the outcome.
- `VERIFICATION_GAPS` (list; required; shape: {PATH_OR_CHECK, GAP, CHEAPEST_NEXT_CHECK}): Explicit verification gaps when a changed artifact or planned check could not be fully verified.
- `IMPLEMENTATION_EVIDENCE_NOTES` (list; required; shape: {TASK_ID, NOTE, EVIDENCE}): Implementation-local evidence notes that downstream delivery utilities can attach to task artifacts.

## Output Contract Notes
- Each CHANGED_ARTIFACTS item must be justified by at least one VERIFICATION_RESULTS or VERIFICATION_GAPS row.
- VERIFICATION_RESULTS should name the exact command, test, or file check instead of leaving proof inside generic prose.
- Use VERIFICATION_GAPS instead of burying incomplete checks inside prose.
- IMPLEMENTATION_EVIDENCE_NOTES must reference the same TASK_IDS provided in the input or the synthesized adhoc ids used for the run.
- Keep CHANGED_ARTIFACTS proportional to the stated CHANGE_GOAL; broader cleanup needs an explicit correctness, clarity, or maintenance justification.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Implementation should make data models, side effects, and cost visible, then choose the simplest change that satisfies the core user outcome and explicit contract. Simplicity and focus on the essential behavior matter more than decorative structure.

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
- Before extending a file, apply the responsibility test: does the new code share the same primary data, the same invariant, and the same reason to change as the existing code? If not, extract it into a focused module instead of extending.
- God Object signals to watch during implementation: (1) the file now imports from two or more unrelated subsystems; (2) different callers only need a different subset of its interface; (3) a change in one feature area requires touching code that belongs to a different feature area in the same file.
- Do not diagnose a God Object from LOC alone. A large file with one clear responsibility is better than three small files with entangled cross-calls.
- When a split is warranted, cut along the axis that lets each resulting module be tested and changed in isolation without importing the other.

## Response Format

Output directly after implementing.

```
changed: `file:line` — one-line description
verified: `command` → ✓ N/N passed
```

If gaps exist, ask immediately:
> "`file.ts` unverified — handle this now?"

Do not write "work complete", a list of what you did, or a closing summary.

## Mandatory Rules
- Do not synchronize plan/task markdown here; emit implementation evidence only.
- Every changed artifact must be paired with at least one verification result or an explicit verification gap.
