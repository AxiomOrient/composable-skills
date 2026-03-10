---
name: build-until-done
description: "Atomic completion-control skill for code-changing work. Keep a bounded implementation mission moving until its explicit done contract is satisfied or a real blocker stops progress. Compose with narrow code-path companion skills such as build-write-code, test-write-guards, debug-find-root-cause, or check-delivered when the task must finish instead of stopping at a partial pass."
---

# Completion Contract Loop

## Purpose
Check a bounded code-changing mission against explicit done conditions and decide whether to stop, block, or run one smallest next pass.

## Default Program
```text
[stages: preflight>detect>analyze>plan>handoff>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,deterministic-output |
 lens: contract-evidence-verifier |
 output: md(contract=v1)]
```

## Use When
- Need to keep one bounded code-changing mission moving until explicit done conditions are satisfied.
- Need a disciplined continue/done/blocked decision after a partial implementation, test, debug, or verification pass.
- Need to compose with narrow code-path companion skills so the task finishes instead of stopping at a partial result.

## Do Not Use When
- Need broad multi-project orchestration or hidden retry automation.
- Need only final read-only validation after work is already complete.
- Need a documentation, review, planning, or release-prep loop with no code changes; use `finish-until-done` instead.

## Required Inputs
- `MISSION_GOAL` (string; required): One bounded mission that should either finish or stop with a real blocker.
- `TARGET_SCOPE` (path|module|folder|repo|artifact; required): Exact scope the mission is allowed to touch.
- `DONE_CONDITION` (list; required; shape: {CONDITION, PROOF_REQUIRED}): Explicit completion contract and the evidence required for each condition.
- `CURRENT_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Current outputs, tests, notes, or observations from prior passes.
- `COMPANION_SKILLS` (list; optional; allowed: build-write-code|test-write-guards|build-make-faster|debug-find-root-cause|check-delivered; shape: {SKILL}): Narrow code-path companion skills allowed for the next pass.
- `MAX_PASSES` (integer; optional): Safety budget for same-turn iteration. Default to 3 when omitted.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Time, safety, approval, or non-goal constraints that limit the loop.

## Input Contract Notes
- DONE_CONDITION should contain externally checkable conditions, not vibe-based success language.
- DONE_CONDITION should prioritize the core user-visible or contract-visible outcome before secondary polish or optional cleanup.
- COMPANION_SKILLS should stay narrow and code-path only. If the mission does not require code changes, use `finish-until-done` instead.
- MAX_PASSES is a safety ceiling for one turn, not a quality score. If omitted, use 3 as the default ceiling.

## Structured Outputs
- `MISSION_STATUS` (continue|done|blocked; required; allowed: continue|done|blocked): Whether the mission needs another pass, is complete, or is blocked.
- `DONE_CONDITION_STATUS` (list; required; shape: {CONDITION, STATUS, EVIDENCE_OR_GAP}): Per-condition check status against the explicit completion contract.
- `NEXT_PASS` (list; optional; required when MISSION_STATUS=continue; shape: {GOAL, RECOMMENDED_SKILL, PASS_CONDITION, WHY_THIS_FIRST}): Exactly one smallest next pass when the mission should continue.
- `BLOCKERS` (list; optional; required when MISSION_STATUS=blocked; shape: {ISSUE, LOCATION, UNBLOCKING_CHECK}): Real blockers that stop progress and what would unblock them.
- `LOOP_EXIT_REASON` (string; required): Why the loop stopped on done, blocked, or continue-for-another-pass.

## Output Contract Notes
- Emit `done` only when every DONE_CONDITION row has evidence, not just partial progress.
- Emit `continue` only with one smallest next pass; do not return a backlog disguised as a next step.
- Emit `blocked` only when an external dependency, missing input, approval gate, or pass-budget stop prevents the next pass.

## Primary Lens
- `primary_lens`: `contract-evidence-verifier`
- `frame_name`: Contract-and-Evidence Verifier
- `why`: Code completion looping should compare explicit done conditions against fresh evidence, force one smallest next code pass, and stop cleanly on real blockers instead of vibe-based progress claims.
- `summary`: Check explicit contracts against fresh evidence, separate blockers from gaps, and do not claim pass without proof.
- `thesis`: Final verification is not another review; it is a disciplined check that each explicit contract has evidence, each blocker is isolated, and each missing proof becomes a next check.
- `decision_rules`:
  - Verify every expected contract against concrete evidence before concluding pass.
  - Separate blocker, evidence gap, and residual polish instead of mixing them in one bucket.
  - Prefer rerunning the cheapest relevant check over trusting stale success claims.
  - If a contract cannot be checked fully, mark inconclusive and name the next check.
- `anti_patterns`:
  - Pass claim with no evidence trail
  - Mixing blocker and polish in the same verdict bucket
  - Trusting stale success claims without rerun or citation
- `good_for`:
  - final verification
  - delivery gates
  - artifact validation
  - task sync checks
- `not_for`:
  - root-cause debugging
  - broad review verdicts
  - architecture ideation
- `required_artifacts`:
  - Checked Contract
  - Evidence Trail
  - Blocker
  - Next Check
- `references`:
  - https://csrc.nist.gov/glossary/term/verification
  - https://csrc.nist.gov/glossary/term/validation

## Artifacts
- `artifacts_in`: implementation-delta.v1, test-report.v1, debug-report.v1, review-report.v1, self-verify-report.v1
- `artifacts_out`: completion-contract-loop-report.v1

## Neutrality Rules
- Do not declare the mission complete from momentum, partial progress, or intent.
- Prefer the smallest discriminating next pass over a broad cleanup list.
- If the done contract is ambiguous, surface the ambiguity as a blocker instead of guessing success.

## Execution Constraints
- This skill is decision-and-control only; do not patch files, rewrite plans, or hide orchestration logic here.
- When composed with allowed companion skills in the same turn, rerun the completion check after each material code pass and stop only on done, blocked, or MAX_PASSES exhaustion.
- Keep companion skills narrow and code-path only. If the mission requires broad cross-domain decomposition, hand off to `plan-task-breakdown` or a workflow instead of stretching this skill.
- Do not keep the mission in `continue` for non-essential cleanup once the core done contract is already proven unless that cleanup was explicitly included in DONE_CONDITION.

## Mandatory Rules
- Never emit `MISSION_STATUS=done` while any DONE_CONDITION row lacks proof.
- When `MISSION_STATUS=continue`, NEXT_PASS must contain exactly one row.

## Example Invocation
```text
$compose + $build-until-done + $build-write-code + $check-delivered + @src/auth + [Keep iterating until refresh no longer drops the session and targeted checks pass.]
```

## Output Discipline
- `response_profile=analysis_report`
- User-facing rendering is delegated to `respond`.
