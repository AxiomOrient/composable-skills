---
name: build-until-done
description: "Atomic loop control primitive for code-changing work. Tracks done conditions against current evidence, selects the one concrete next pass, and keeps the mission moving until the explicit contract is proven or a real blocker stops progress. Use when you want direct control over which companion skills run in a compose chain. For fully automated plan-ledger execution with a fixed pipeline, use workflow-build-execute-loop instead."
---

# Build / Until Done

## Purpose
Own the loop control layer for a bounded code-changing mission: analyze current evidence against the done contract, decide continue/done/blocked, and produce exactly one concrete next pass when continuing. It is the control brain — the companion skills are the execution body.

## Default Program
```text
[stages: preflight>detect>analyze>evaluate>handoff>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,deterministic-output |
 lens: contract-evidence-verifier |
 output: md(contract=v1)]
```

## Use When
- Need to drive one bounded code-changing mission to completion within a compose chain.
- Need a disciplined continue/done/blocked decision after a partial implementation, test, debug, or verification pass.
- Need manual control over which companion skills execute each pass.
- Need a plan or task document treated as a live execution ledger with per-task progress tracking.

## Do Not Use When
- Need fully automated end-to-end execution: write code → critique → sync → verify → repeat, driven by a plans/ task ledger. Use `workflow-build-execute-loop` instead.
- Need broad multi-project orchestration or hidden retry automation.
- Need only final read-only validation after work is already complete.
- Need a documentation, review, planning, or release-prep loop with no code changes; use `finish-until-done` instead.

## Required Inputs
- `MISSION_GOAL` (string; required): One bounded mission that should either finish or stop with a real blocker.
- `TARGET_SCOPE` (path|module|folder|repo|artifact; required): Exact scope the mission is allowed to touch.
- `DONE_CONDITION` (list; required; shape: {CONDITION, PROOF_REQUIRED}): Explicit completion contract and the evidence required for each condition.
- `CURRENT_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Current outputs, tests, notes, or observations from prior passes.
- `PLAN_ARTIFACTS` (list; optional; shape: {PATH, ROLE}): Implementation plan, tasks ledger, or execution docs that must be consumed and exhausted during the loop. When present, treat incomplete task rows as active work and keep consuming them until exhausted. When absent, drive iteration from DONE_CONDITION and prompt evidence.
- `COMPANION_SKILLS` (list; optional; allowed: build-write-code|test-write-guards|build-make-faster|debug-find-root-cause|check-final-verify|plan-sync-tasks|check-improve-loop|tidy-simplify; shape: {SKILL}): Narrow code-path companion skills active in this compose chain. These are declared by the caller — this skill uses them for the next pass handoff, not internal invocation.
- `MAX_PASSES` (integer; optional): Safety budget for same-turn iteration. Default to 3, or 8 when PLAN_ARTIFACTS is present.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Time, safety, approval, or non-goal constraints that limit the loop.

## Input Contract Notes
- DONE_CONDITION should contain externally checkable conditions, not vibe-based success language.
- DONE_CONDITION should prioritize the core user-visible or contract-visible outcome before secondary polish or optional cleanup.
- COMPANION_SKILLS declares what skills are available in this compose chain. The next pass handoff will route to one of these. If absent, this skill produces a NEXT_PASS recommendation for the caller to act on.
- If PLAN_ARTIFACTS is present, treat incomplete task rows or unchecked execution items as active work, not as passive reference material.
- If PLAN_ARTIFACTS is absent, iterate directly from DONE_CONDITION and fresh prompt evidence until the contract is satisfied or blocked.
- MAX_PASSES is a safety ceiling for one turn, not a quality score. If omitted, use 3 by default, or 8 when PLAN_ARTIFACTS is present.

## Structured Outputs
- `MISSION_STATUS` (continue|done|blocked; required; allowed: continue|done|blocked): Whether the mission needs another pass, is complete, or is blocked.
- `DONE_CONDITION_STATUS` (list; required; shape: {CONDITION, STATUS, EVIDENCE_OR_GAP}): Per-condition check status against the explicit completion contract.
- `PLAN_TASK_STATUS` (list; optional; shape: {PATH_OR_TASK, STATUS, EVIDENCE_OR_GAP}): Optional status for plan/task ledger rows that materially affect the done contract.
- `NEXT_PASS` (list; optional; required when MISSION_STATUS=continue; shape: {GOAL, RECOMMENDED_SKILL, PASS_CONDITION, WHY_THIS_FIRST}): Exactly one smallest next pass when the mission should continue.
- `BLOCKERS` (list; optional; required when MISSION_STATUS=blocked; shape: {ISSUE, LOCATION, UNBLOCKING_CHECK}): Real blockers that stop progress and what would unblock them.
- `LOOP_EXIT_REASON` (string; required): Why the loop stopped on done, blocked, or continue-for-another-pass.

## Output Contract Notes
- Emit `done` only when every DONE_CONDITION row has evidence, not just partial progress.
- Emit `continue` only when the next pass is known but cannot be safely executed within the current turn because of MAX_PASSES, a blocker, or missing proof. Do not return a backlog disguised as a next step.
- Emit `blocked` only when an external dependency, missing input, approval gate, or pass-budget stop prevents the next pass.

## Primary Lens
- `primary_lens`: `contract-evidence-verifier`
- `why`: Code completion looping should compare explicit done conditions against fresh evidence, force one smallest next code pass, and stop cleanly on real blockers instead of vibe-based progress claims.

## Artifacts
- `artifacts_in`: implementation-delta.v1, test-report.v1, debug-report.v1, review-report.v1, self-verify-report.v1
- `artifacts_out`: completion-contract-loop-report.v1

## Neutrality Rules
- Do not declare the mission complete from momentum, partial progress, or intent.
- Prefer the smallest discriminating next pass over a broad cleanup list.
- If the done contract is ambiguous, surface the ambiguity as a blocker instead of guessing success.

## Execution Constraints
- This skill owns pass selection and stop conditions. It is the control layer — execution happens in the companion skills declared by the caller.
- When PLAN_ARTIFACTS is present, first run `../plan-sync-tasks/scripts/task_ledger.py next --tasks <tasks-path> [--plan <plan-path>]` to extract the next actionable task id and verification map before producing the next-pass handoff.
- If PLAN_ARTIFACTS is present, read the plan/task ledger before the first pass and keep selecting relevant incomplete rows until the ledger is exhausted, the done contract is proven, or a real blocker appears.
- If `plan-sync-tasks` is present as a companion skill, synchronize plan/task artifacts after each material pass that changes task state or evidence.
- Keep companion skills narrow and code-path only. If the mission requires broad cross-domain decomposition, hand off to `plan-task-breakdown` or a workflow instead of stretching this skill.
- Do not keep the mission in `continue` for non-essential cleanup once the core done contract is already proven unless that cleanup was explicitly included in DONE_CONDITION.

## Mandatory Rules
- Never emit `MISSION_STATUS=done` while any DONE_CONDITION row lacks proof.
- If PLAN_ARTIFACTS is present, never emit `MISSION_STATUS=done` while relevant incomplete rows still block DONE_CONDITION.
- When `MISSION_STATUS=continue`, NEXT_PASS must contain exactly one row.

## Example Invocation

플랜 없이 (DONE_CONDITION 기반 반복):
```text
$compose + $build-until-done + $build-write-code + $check-improve-loop + $check-final-verify + @src/auth + [Keep implementing and self-critiquing until the done contract is proven.]
```

플랜 있을 때 (태스크 ledger 기반, 태스크별 피드백):
```text
$compose + $build-until-done + $plan-sync-tasks + $build-write-code + $check-improve-loop + $check-final-verify + @plans/IMPLEMENTATION-PLAN.md + @plans/TASKS.md + [Consume all task rows, run self-feedback after each implementation pass, and keep going until the done contract is proven.]
```

> 완전 자동화 실행이 필요하다면 `workflow-build-execute-loop`를 사용하세요. 이 스킬은 파이프라인을 직접 지정하고 싶을 때 사용합니다.
