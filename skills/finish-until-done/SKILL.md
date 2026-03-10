---
name: finish-until-done
description: "Atomic completion-control skill for bounded non-code work. Own the loop for one explicit mission until its done contract is proven or a real blocker stops progress. Use prompt criteria and fresh evidence to keep going until the issue is actually resolved."
---

# Finish / Until Done

## Purpose
Own a bounded non-code loop, execute the next required pass, and keep going until the explicit contract is proven or a real blocker stops progress.

## Default Program
```text
[stages: preflight>detect>analyze>plan>handoff>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,deterministic-output |
 lens: contract-evidence-verifier |
 output: md(contract=v1)]
```

## Use When
- Need to keep one bounded non-code mission moving until explicit done conditions are satisfied.
- Need a disciplined continue/done/blocked decision after a documentation, review, planning, or release-prep pass.
- Need to compose with narrow non-code companion skills so the task finishes instead of stopping at a partial result.
- Need the stopping condition to come from the prompt and fresh evidence rather than from a prewritten task ledger.

## Do Not Use When
- Need code implementation, test-writing, performance tuning, or patch-and-rerun loops.
- Need only final read-only validation after work is already complete.
- Need broad multi-project orchestration or hidden retry automation.

## Required Inputs
- `MISSION_GOAL` (string; required): One bounded mission that should either finish or stop with a real blocker.
- `TARGET_SCOPE` (path|module|folder|repo|artifact; required): Exact scope the mission is allowed to touch.
- `DONE_CONDITION` (list; required; shape: {CONDITION, PROOF_REQUIRED}): Explicit completion contract and the evidence required for each condition.
- `CURRENT_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Current outputs, notes, review results, docs, or observations from prior passes.
- `COMPANION_SKILLS` (list; optional; allowed: plan-sync-tasks|scout-structure-map|doc-write|check-merge-ready|check-quality-scan|plan-task-breakdown|check-final-verify; shape: {SKILL}): Narrow non-code companion skills allowed for the next pass.
- `MAX_PASSES` (integer; optional): Safety budget for same-turn iteration. Default to 3 when omitted.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Time, safety, approval, or non-goal constraints that limit the loop.

## Input Contract Notes
- DONE_CONDITION should contain externally checkable conditions, not vibe-based success language.
- DONE_CONDITION should prioritize the core user-visible or contract-visible outcome before secondary polish or optional cleanup.
- COMPANION_SKILLS should stay non-code and narrow. If the mission requires code changes or test loops, use `build-until-done` instead.
- DONE_CONDITION should be derived from the prompt or explicit contract in front of the skill, not assumed from a hidden task list.
- MAX_PASSES is a safety ceiling for one turn, not a quality score. If omitted, use 3 as the default ceiling.

## Structured Outputs
- `MISSION_STATUS` (continue|done|blocked; required; allowed: continue|done|blocked): Whether the mission needs another pass, is complete, or is blocked.
- `DONE_CONDITION_STATUS` (list; required; shape: {CONDITION, STATUS, EVIDENCE_OR_GAP}): Per-condition check status against the explicit completion contract.
- `NEXT_PASS` (list; optional; required when MISSION_STATUS=continue; shape: {GOAL, RECOMMENDED_SKILL, PASS_CONDITION, WHY_THIS_FIRST}): Exactly one smallest next pass when the mission should continue.
- `BLOCKERS` (list; optional; required when MISSION_STATUS=blocked; shape: {ISSUE, LOCATION, UNBLOCKING_CHECK}): Real blockers that stop progress and what would unblock them.
- `LOOP_EXIT_REASON` (string; required): Why the loop stopped on done, blocked, or continue-for-another-pass.

## Output Contract Notes
- Emit `done` only when every DONE_CONDITION row has evidence, not just partial progress.
- Emit `continue` only when the next pass is known but cannot be safely executed within the current turn because of MAX_PASSES, a blocker, or missing proof. Do not return a backlog disguised as a next step.
- Emit `blocked` only when an external dependency, missing input, approval gate, or pass-budget stop prevents the next pass.

## Primary Lens
- `primary_lens`: `contract-evidence-verifier`
- `why`: Non-code completion looping should compare explicit done conditions against fresh evidence, force one smallest next pass, and stop cleanly on real blockers instead of vibe-based progress claims.

## Artifacts
- `artifacts_in`: analysis-report.v1, documentation-report.v1, planning-doc.v1, review-report.v1, release-decision.v1, self-verify-report.v1
- `artifacts_out`: completion-contract-loop-report.v1

## Neutrality Rules
- Do not declare the mission complete from momentum, partial progress, or intent.
- Prefer the smallest discriminating next pass over a broad cleanup list.
- If the done contract is ambiguous, surface the ambiguity as a blocker instead of guessing success.

## Execution Constraints
- This skill owns pass selection and stop conditions. It may invoke allowed companion skills, absorb fresh evidence, and resume control within the same turn.
- When composed with allowed companion skills in the same turn, execute the next required pass, rerun the completion check, and keep going until done, blocked, or MAX_PASSES exhaustion.
- Derive the next stopping test from the prompt, DONE_CONDITION, and fresh evidence rather than from an external plan ledger.
- Keep companion skills narrow. If the mission requires broad cross-domain decomposition, hand off to `plan-task-breakdown` or a workflow instead of stretching this skill.
- Do not keep the mission in `continue` for non-essential cleanup once the core done contract is already proven unless that cleanup was explicitly included in DONE_CONDITION.

## Mandatory Rules
- Never emit `MISSION_STATUS=done` while any DONE_CONDITION row lacks proof.
- When `MISSION_STATUS=continue`, NEXT_PASS must contain exactly one row.

## Example Invocation
```text
$compose + $finish-until-done + $doc-write + $check-final-verify + @docs + [Keep iterating until the guide is beginner-readable, linked correctly, and contract sections are complete.]
```
