---
name: control-finish-until-done
description: "Plan-free autonomous loop for non-code work. Drives bounded documentation, review, planning, or release-prep missions to completion without requiring task documents. Reads current artifact state, evaluates it against the done contract, applies the smallest content improvement, and loops until the contract is proven or a real blocker stops progress. For code-changing missions, use control-build-until-done instead."
---

# Control / Finish Until Done

## Purpose
Autonomously drive a bounded non-code mission to completion without plan documents. Reads current artifact state, evaluates it against the done contract, picks the smallest useful improvement, applies it, and loops immediately. No manual stepping — done or blocked is the only exit.

Works across: documentation, code review, planning artifacts, release prep, content revision.

## Default Program
```text
[stages: evaluate>read>improve>verify>loop>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,craft-clarity,loop-until-done,approval-gates{blockers-only} |
 lens: craft-clarity |
 output: md(contract=v1)]
```

## Lens: craft-clarity
Each pass must make the artifact **clearer, more complete, or more accurate** for its intended reader. "Technically present" is not the same as done. A section that would confuse its reader is not finished. Keep going until the content stands on its own.

## Lens Rationale
This skill uses `craft-clarity` because it keeps the work aligned with: Treat clear, complete, reader-usable output as the real done condition, then keep iterating until the artifact stands on its own.

## Use When
- Need to drive documentation, review, planning, or release-prep to completion without any task documents.
- DONE_CONDITION is clear but the path to get there is not fully mapped upfront.
- Need to keep iterating on content — write → read → revise → verify — until the quality bar is provably met.
- A pass reveals a new gap — incorporate it into the loop instead of stopping.

## Do Not Use When
- Need code implementation, tests, or performance fixes — use `control-build-until-done` instead.
- Have a TASKS.md plan and need ledger-driven execution — use `workflow-build-execute-plan` instead.
- Need only final validation after work is already complete.

## Required Inputs
- `MISSION_GOAL` (string; required): One bounded non-code mission to drive to completion.
- `TARGET_SCOPE` (path|artifact|folder; required): Exact scope the mission is allowed to touch.
- `DONE_CONDITION` (list; required; shape: {CONDITION, PROOF_REQUIRED}): Explicit completion contract. Each condition must be reader-verifiable — no "looks good" or "seems complete."
- `CURRENT_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Observations, review notes, or prior pass results. When absent, reads TARGET_SCOPE to build initial state.
- `MAX_PASSES` (integer; optional): Safety ceiling for passes in one turn. Default: 5.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Scope, audience, tone, or non-goal constraints.

## Input Contract Notes
- DONE_CONDITION must be reader-checkable: "beginner can follow without prior context", "all links verified", "no undefined terms in section 2". "Looks complete" is not valid.
- When CURRENT_EVIDENCE is absent, read TARGET_SCOPE first to establish baseline content state.
- If the mission goal is ambiguous (e.g., "write the docs" with no audience defined), emit blocked immediately and ask for clarification.

## Execution Loop

Run this loop within a single turn until MISSION_STATUS=done or blocked:

```
1. Read current artifact state at TARGET_SCOPE
2. Check each DONE_CONDITION against current content evidence
3. All conditions met with reader-verifiable proof → done
4. A real blocker exists (missing source, unclear audience, approval needed) → blocked, ask
5. Pick smallest improvement that advances the weakest done condition
6. Execute: write/revise content (doc-write), review (check-quality-scan / check-change-review),
            structure (plan-task-breakdown), or verify (check-final-verify)
7. Update evidence with results
8. Go back to step 2 immediately
```

**Do not stop between passes.** Each pass completes and immediately triggers the next evaluation.

## Structured Outputs
- `MISSION_STATUS` (done|blocked; required; allowed: done|blocked): Loop outcome. No `continue` — if not done, keep looping.
- `DONE_CONDITION_STATUS` (list; required; shape: {CONDITION, STATUS, EVIDENCE}): Reader-verifiable evidence for each condition.
- `PASSES_COMPLETED` (integer; required): Number of content improvement passes executed.
- `BLOCKERS` (list; optional; required when MISSION_STATUS=blocked; shape: {ISSUE, LOCATION, UNBLOCKING_CHECK}): What stopped progress and what would unblock it.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Do not summarize the process. Output one line per pass as it executes, then keep going.

```
Pass 1 → doc-write: `docs/auth.md §session` — added refresh flow explanation
Pass 2 → check-quality-scan: clarity P1 in intro — revised lead sentence
Pass 3 → check-final-verify: ✓ all conditions met
```

On done:
```
Done ✓ (N passes)
- [condition]: ✓ [proof]
- [condition]: ✓ [proof]
```

On blocked — ask directly, one sentence:
> "`docs/api-spec.md` missing — can you share it, or should I draft a placeholder?"

No "work complete" line. No summary of what each pass did. Let the pass log speak.

## Primary Lens
- `primary_lens`: `craft-clarity`
- `why`: Non-code work is done when its intended reader can use it — not when it's technically present. Each pass must advance clarity, completeness, or accuracy. "Written" and "finished" are not the same thing.

## Artifacts
- `artifacts_in`: none (plan-free — reads current artifact state directly)
- `artifacts_out`: completion-evidence.v1

## Neutrality Rules
- Do not declare done from partial progress, word count, or intent. Every DONE_CONDITION row needs reader-verifiable evidence.
- If a pass reveals a new gap, add it to the loop — do not stop and report it as a blocker unless it's genuinely unresolvable.
- Prefer the smallest improvement that advances the weakest condition. Do not rewrite everything when one section needs a fix.

## Execution Constraints
- Run the full loop within a single turn. Do not pause between passes for user confirmation unless a genuine blocker appears.
- If a review pass finds issues, fix them within the same loop before declaring done.
- Keep each pass bounded to the smallest action that advances the weakest done condition.
- Do not drift into adjacent content not in DONE_CONDITION.

## Mandatory Rules
- Never emit MISSION_STATUS=done while any DONE_CONDITION row lacks reader-verifiable proof.
- Do not stop after one pass when the mission is not done. Continue immediately.
- Stop and ask only when a genuine blocker exists. Do not guess or fabricate missing content.

## Symmetry with control-build-until-done

| | control-build-until-done | control-finish-until-done |
|--|--|--|
| Domain | Code | Docs / reviews / plans |
| Drives by | DONE_CONDITION + tests | DONE_CONDITION + reader evidence |
| Pass types | implement, run tests, debug | write, review, revise, verify |
| Lens | contract-evidence-verifier | craft-clarity |
| Plan docs | Not needed | Not needed |
| Exit | done ✓ or blocked | done ✓ or blocked |

## Example Invocation

```text
$control-finish-until-done
GOAL: Make the session auth guide beginner-readable and complete
SCOPE: docs/auth/
DONE:
  - A developer new to the project can follow the guide without external help
  - All code examples are verified against the current API
  - No section ends with a placeholder or TODO
```

> Have a TASKS.md plan? Use `workflow-build-execute-plan` for document-driven execution.
> Need code changes too? Switch to `control-build-until-done` for that part.
