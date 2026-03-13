---
name: control-improve-loop
description: "Atomic self-feedback refinement loop. Review one bounded work product, extract the highest-value improvement, run the smallest fix, and repeat until the explicit quality bar is satisfied or a real blocker stops progress."
---

# Control / Improve Loop

## Purpose
Drive bounded self-critique and improvement loops toward a simpler, higher-quality result without drifting into over-engineering.

## Default Program
```text
[stages: preflight>detect>analyze>review>reflect>plan>handoff>audit | scope: diff|repo|paths(glob,...) | policy: evidence,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, smallest high-value fix over decorative polish.

## Use When
- Need iterative self-critique and improvement for one bounded artifact or scope.
- Need to keep refining until the core quality bar is met while rejecting over-engineering.
- Need one explicit skill that can critique current work, choose the smallest high-value fix, and rerun the loop.

## Do Not Use When
- Need only final read-only delivery verification — use `review-final-verify` instead.
- Need broad multi-track planning or orchestration across unrelated scopes.
- Need net-new feature ideation rather than refinement of existing work.

## Required Inputs
- `MISSION_GOAL` (string; required): One bounded mission that should improve through self-critique until done or blocked.
- `TARGET_SCOPE` (path|artifact|module|folder|repo|diff; required): Exact scope the loop is allowed to inspect or improve.
- `DONE_CONDITION` (list; required; shape: {CONDITION, PROOF_REQUIRED}): Explicit quality bar and proof required per condition.
- `CURRENT_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Current evidence, review notes, tests, or docs from prior passes.
- `COMPANION_SKILLS` (list; optional; allowed: build-write-code|doc-write|tidy-simplify|test-write-guards|review-change|review-final-verify|plan-task-breakdown; shape: {SKILL}): Narrow companion skills allowed for the next improvement pass.
- `MAX_PASSES` (integer; optional): Safety ceiling for same-turn refinement passes. Default 3.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Non-goals, simplicity limits, or quality boundaries.

## Input Contract Notes
- DONE_CONDITION should contain checkable quality conditions, not vibe-based success language.
- CURRENT_EVIDENCE should describe the current state honestly.
- COMPANION_SKILLS should stay narrow. If the mission requires broad decomposition, use plan-task-breakdown first.
- State simplicity in CONSTRAINTS so the loop can stop when remaining changes are decorative.

## Structured Outputs
- `MISSION_STATUS` (continue|done|blocked; required): Whether the mission needs another pass, is complete, or is blocked.
- `SELF_FEEDBACK` (list; required; shape: {ISSUE, WHY_IT_MATTERS, SMALLEST_FIX}): Highest-value critique items from the current work.
- `APPLIED_IMPROVEMENTS` (list; required; shape: {ACTION, TARGET, EVIDENCE}): Improvements already applied during the current loop.
- `DONE_CONDITION_STATUS` (list; required; shape: {CONDITION, STATUS, EVIDENCE_OR_GAP}): Per-condition status against the done contract.
- `NEXT_PASS` (list; optional; required when MISSION_STATUS=continue; shape: {GOAL, RECOMMENDED_SKILL, PASS_CONDITION, WHY_THIS_FIRST}): Exactly one smallest next pass.
- `BLOCKERS` (list; optional; required when MISSION_STATUS=blocked; shape: {ISSUE, LOCATION, UNBLOCKING_CHECK}): Real blockers and cheapest check to unblock.
- `LOOP_EXIT_REASON` (string; required): Why the loop stopped.

## Output Contract Notes
- Emit `done` only when every DONE_CONDITION row has proof and remaining improvements are non-essential.
- Emit `continue` only when the next pass is known but cannot be safely executed within the current turn.
- SELF_FEEDBACK should rank the smallest change that materially improves the result.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Self-verification should keep only the smallest high-value improvement, reject decorative over-engineering, and stop when the essence-first quality bar is proven.

## Artifacts
- `artifacts_in`: implementation-delta.v1, documentation-report.v1, review-report.v1
- `artifacts_out`: improve-loop-report.v1

## Neutrality Rules
- Do not invent flaws just to keep the loop moving.
- Do not keep iterating after the explicit quality bar is already proven.
- Prefer the smallest high-value fix over ambitious cleanup.

## Execution Constraints
- Stop when the best remaining change is decorative, speculative, or outside TARGET_SCOPE.
- Keep simplicity and essence-first judgement above ornamental polish.
- Do not convert an implicit backlog into mandatory work unless DONE_CONDITION makes it critical.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

루프 상태: **완료** / **계속** / **중단**

완료라면: 각 완료 기준과 근거 목록. 끝.

계속이라면: 다음 패스 하나 — 목표, 쓸 스킬, 통과 조건. 왜 이것인지.

중단이라면: 막힌 것과 가장 빠른 해결 방법.

자기 피드백: 이슈 → 왜 중요한지 → 가장 작은 수정.

## Mandatory Rules
- Never emit `MISSION_STATUS=done` while any DONE_CONDITION row lacks proof.
- When `MISSION_STATUS=continue`, NEXT_PASS must contain exactly one row.

## Example Invocation
```text
$compose + $control-improve-loop + $build-write-code + $review-final-verify + @src/auth + [Keep reviewing and tightening the refresh flow until the simplest correct shape is proven.]
```
