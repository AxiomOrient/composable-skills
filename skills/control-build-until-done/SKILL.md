---
name: control-build-until-done
description: "Plan-free autonomous build loop. Drives a bounded code mission to completion without requiring plan or task documents. Evaluates current state, picks the smallest next code action, executes it, and loops until the done contract is proven or a real blocker stops progress. For document-driven execution with a TASKS.md ledger, use workflow-build-execute-plan instead."
---

# Control / Build Until Done

## Purpose
Autonomously drive a bounded code mission to completion without plan documents. Reads current code state, evaluates it against the done contract, picks the smallest useful next action, executes it, and loops immediately. No manual stepping. No stopping between passes — done or blocked is the only exit.

## Default Program
```text
[stages: evaluate>select>implement>verify>loop>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,correctness-first,loop-until-done,approval-gates{blockers-only} |
 lens: contract-evidence-verifier |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `contract-evidence-verifier` because it keeps the work aligned with: Check explicit contracts against fresh evidence, separate blockers from gaps, and do not claim pass without proof.

## Use When
- Need to drive a code mission to completion without any plan or task documents.
- DONE_CONDITION is clear but the implementation path is not fully mapped upfront.
- Need ralph-mode execution: evaluate → act → verify → repeat until provably done.
- A pass fails mid-loop — debug and retry within the same loop instead of stopping.

## Do Not Use When
- Have a plans/TASKS.md ledger — use `workflow-build-execute-plan` for document-driven execution.
- Need only a single-pass implementation — use `build-write-code` directly.
- Need non-code work (docs, review) — use `control-finish-until-done` instead.

## Required Inputs
- `MISSION_GOAL` (string; required): One bounded mission to execute until the done contract is proven or a real blocker stops progress.
- `TARGET_SCOPE` (path|module|folder|repo; required): Exact scope the mission is allowed to touch.
- `DONE_CONDITION` (list; required; shape: {CONDITION, PROOF_REQUIRED}): Explicit completion contract. Each condition must be externally checkable — no vibe-based success language.
- `CURRENT_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Observations, test results, or notes from any prior pass. When absent, reads TARGET_SCOPE to build initial evidence.
- `MAX_PASSES` (integer; optional): Safety ceiling for passes within one turn. Default: 5.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Safety, scope, or non-goal constraints.

## Input Contract Notes
- DONE_CONDITION must be externally checkable: test passing, file existing, behavior observable. "Looks good" is not valid.
- When CURRENT_EVIDENCE is absent, read TARGET_SCOPE first to establish the baseline state.
- If the mission goal is ambiguous, emit blocked immediately and ask for clarification. Do not guess.

## Execution Loop

Run this loop within a single turn until MISSION_STATUS=done or blocked:

```
1. Read current code state at TARGET_SCOPE
2. Check each DONE_CONDITION against current evidence
3. All conditions have proof → done, stop
4. A real blocker exists → blocked, ask the user
5. Pick the smallest action that advances the weakest done condition
6. Execute: implement (build-write-code), verify (run tests), or debug (root cause)
7. Update evidence with results
8. Go back to step 2 immediately
```

**Do not stop between passes.** Each pass completes and immediately triggers the next evaluation.

## Structured Outputs
- `MISSION_STATUS` (done|blocked; required; allowed: done|blocked): Loop outcome. No `continue` output — if not done, keep looping.
- `DONE_CONDITION_STATUS` (list; required; shape: {CONDITION, STATUS, EVIDENCE}): Evidence status for each condition.
- `PASSES_COMPLETED` (integer; required): Number of implementation/verification passes executed.
- `BLOCKERS` (list; optional; required when MISSION_STATUS=blocked; shape: {ISSUE, LOCATION, UNBLOCKING_CHECK}): What stopped progress and what would unblock it.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Output one line per pass as it executes, then immediately continue.

```
Pass 1 → build-write-code: `session.ts:42` fix refreshToken expiry
Pass 2 → verify: `npm test -- session` → ✓ 3/3
Pass 3 → build-write-code: `token.ts:18` add auto-renewal on expiry
Pass 4 → verify: `npm test` → ✓ 12/12
```

On loop exit:
- **Done**: `Done ✓ (N passes)` — one line of evidence per condition
- **Blocked**: `Blocked: [issue]` — ask immediately: "How should we unblock this?"

## Primary Lens
- `primary_lens`: `contract-evidence-verifier`
- `why`: Each pass must narrow the gap between current state and the done contract. Stop only when every condition has proof — not when momentum runs out.

## Artifacts
- `artifacts_in`: none (plan-free — reads current code state directly)
- `artifacts_out`: completion-evidence.v1

## Neutrality Rules
- Do not declare done from partial progress or intent. Every DONE_CONDITION row needs proof.
- If a pass fails, debug and retry within the same loop. Only emit blocked when genuinely unresolvable.
- Prefer the smallest discriminating next action over broad cleanup.

## Execution Constraints
- Run the full loop within a single turn. Do not pause between passes for user confirmation unless a genuine blocker appears.
- If a test fails, attempt to fix it within the same loop before declaring blocked.
- Keep each pass bounded to the smallest action that advances the weakest done condition.
- Do not drift into adjacent cleanup not in DONE_CONDITION.

## Mandatory Rules
- Never emit MISSION_STATUS=done while any DONE_CONDITION row lacks proof.
- Do not stop after one pass when the mission is not done. Continue immediately.
- Stop and ask only when a genuine blocker exists. Do not guess or fabricate a workaround.

## Example Invocation

```text
$control-build-until-done
GOAL: Keep the session alive after browser refresh
SCOPE: src/auth
DONE:
  - session refresh test passes
  - login state persists after browser refresh
```

> Have a TASKS.md plan? Use `workflow-build-execute-plan` for document-driven execution.
