---
name: check-improve-loop
description: "Atomic self-feedback refinement skill. Review one bounded work product, extract the highest-value improvement, run the smallest improvement pass, and repeat until the explicit quality bar is satisfied or a real blocker stops progress. Use prompt criteria and fresh evidence to keep fixing only critical problems."
---

# Check / Improve Loop

## Purpose
Drive bounded self-critique and improvement loops toward a simpler, higher-quality result without drifting into over-engineering.

## Default Program
```text
[stages: preflight>detect>analyze>review>reflect>plan>handoff>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,deterministic-output |
 lens: hickey-carmack |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need iterative self-critique and improvement for one bounded artifact or scope.
- Need to keep refining until the core quality bar is met while rejecting decorative over-engineering.
- Need one explicit skill that can critique current work, choose the smallest high-value fix, and rerun the loop.
- Need the loop to keep fixing only critical issues named by the prompt or proven by fresh evidence.

## Do Not Use When
- Need only final read-only delivery verification; use check-final-verify instead.
- Need broad multi-track planning, backlog slicing, or hidden orchestration across unrelated scopes.
- Need net-new feature ideation rather than refinement of an existing work product.

## Required Inputs
- `MISSION_GOAL` (string; required): One bounded mission that should improve through self-critique until done or blocked.
- `TARGET_SCOPE` (path|artifact|module|folder|repo|diff; required): Exact scope the self-verify loop is allowed to inspect or improve.
- `DONE_CONDITION` (list; required; shape: {CONDITION, PROOF_REQUIRED}): Explicit quality bar and the proof required for each condition.
- `CURRENT_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Current implementation evidence, review notes, tests, or docs from prior passes.
- `COMPANION_SKILLS` (list; optional; allowed: build-write-code|doc-write|tidy-simplify|test-write-guards|check-change-review|check-final-verify|plan-sync-tasks; shape: {SKILL}): Narrow companion skills allowed for the next improvement pass.
- `MAX_PASSES` (integer; optional): Safety ceiling for same-turn refinement passes. Default to 3 when omitted.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Non-goals, simplicity limits, approval gates, or quality boundaries.

## Input Contract Notes
- DONE_CONDITION should contain checkable quality conditions, not vibe-based success language.
- CURRENT_EVIDENCE should describe the current state honestly; this skill is not allowed to assume improvement where none is proven.
- COMPANION_SKILLS should stay narrow. If the mission requires broad decomposition, use plan-task-breakdown or a workflow first.
- If simplicity matters, state it in CONSTRAINTS so the loop can stop when remaining changes are decorative.
- DONE_CONDITION should come from the prompt and explicit quality bar in front of the skill, not from an implicit task ledger.

## Structured Outputs
- `MISSION_STATUS` (continue|done|blocked; required; allowed: continue|done|blocked): Whether the mission needs another improvement pass, is complete, or is blocked.
- `SELF_FEEDBACK` (list; required; shape: {ISSUE, WHY_IT_MATTERS, SMALLEST_FIX}): Highest-value critique items derived from the current work.
- `APPLIED_IMPROVEMENTS` (list; required; shape: {ACTION, TARGET, EVIDENCE}): Improvements already applied during the current loop.
- `DONE_CONDITION_STATUS` (list; required; shape: {CONDITION, STATUS, EVIDENCE_OR_GAP}): Per-condition status against the explicit done contract.
- `NEXT_PASS` (list; optional; required when MISSION_STATUS=continue; shape: {GOAL, RECOMMENDED_SKILL, PASS_CONDITION, WHY_THIS_FIRST}): Exactly one smallest next pass when the loop should continue.
- `BLOCKERS` (list; optional; required when MISSION_STATUS=blocked; shape: {ISSUE, LOCATION, UNBLOCKING_CHECK}): Real blockers and the cheapest check that would unblock them.
- `LOOP_EXIT_REASON` (string; required): Why the loop stopped on done, blocked, or continue.

## Output Contract Notes
- Emit `done` only when every DONE_CONDITION row has proof and remaining improvements are non-essential.
- Emit `continue` only when the next pass is known but cannot be safely executed within the current turn because of MAX_PASSES, a blocker, or missing proof. Do not return a backlog disguised as guidance.
- SELF_FEEDBACK should rank the smallest change that materially improves the result before larger cleanup ideas.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Self-verification should keep only the smallest high-value improvement, reject decorative over-engineering, and stop when the essence-first quality bar is already proven.

## Artifacts
- `artifacts_in`: implementation-delta.v1, documentation-report.v1, review-report.v1, self-verify-report.v1
- `artifacts_out`: self-refine-loop-report.v1

## Neutrality Rules
- Do not invent flaws just to keep the loop moving.
- Do not keep iterating after the explicit quality bar is already proven unless a remaining issue materially affects the core outcome.
- Prefer the smallest high-value fix over ambitious cleanup.

## Execution Constraints
- This skill owns pass selection and stop conditions. It may invoke allowed companion skills, absorb fresh evidence, and resume control within the same turn.
- Stop when the best remaining change is decorative, speculative, or outside TARGET_SCOPE.
- Keep simplicity and essence-first judgement above ornamental polish.
- Do not convert an implicit backlog into mandatory work unless the prompt or DONE_CONDITION makes it critical.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Lead with the loop status: DONE / CONTINUE / BLOCKED.

If DONE: list each done condition with its proof evidence. Stop there.

If CONTINUE: show the one next pass — goal, skill, pass condition. Say why this and not something else.

If BLOCKED: name the blocker and the cheapest check to unblock it.

Keep the self-feedback list tight: issue → why it matters → smallest fix.

## Mandatory Rules
- Never emit `MISSION_STATUS=done` while any DONE_CONDITION row lacks proof.
- When `MISSION_STATUS=continue`, NEXT_PASS must contain exactly one row.

## Example Invocation
```text
$compose + $check-improve-loop + $build-write-code + $check-final-verify + @src/auth + [Keep reviewing and tightening the refresh flow until the simplest correct shape is proven.]
```
