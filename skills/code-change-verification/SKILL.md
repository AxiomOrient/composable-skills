---
name: code-change-verification
description: "Run the smallest credible verification stack after runtime, test, or build changes. Use when code, tests, or build behavior changed and you need explicit verify commands, fail-fast execution, and root-cause grouped failure reporting."
---
# Code Change Verification

## Purpose
Prove that a code or build change is actually safe enough to hand off by selecting the smallest relevant verification stack, running it in a deliberate order, and reporting failures by root cause instead of raw log order.

## Default Program
```text
[stages: preflight>detect>plan>verify>review>handoff>audit |
 scope: diff|repo|paths(glob,...) |
 policy: evidence,quality-gates{format,lint,typecheck,tests},deterministic-output |
 lens: kent-beck |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kent-beck` because it keeps the work aligned with: the smallest useful feedback loop, direct evidence, and immediate repair after a broken check.

## Use When
- Need the mandatory verification path after code, tests, or build behavior changed.
- Need to decide which format, lint, typecheck, and test commands are actually relevant.
- Need one concise verification report instead of scattered shell output.

## Do Not Use When
- Only docs, comments, or non-runtime metadata changed.
- Need test-gap discovery rather than command execution.
- Need a final merge verdict that also weighs design or product fit.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo|diff; required): Where the change lives.
- `CHANGE_TYPE` (runtime|tests|build|mixed; required): What kind of change was made.
- `VERIFICATION_POLICY` (smallest-relevant|required-full-stack; optional): Whether to run the minimum credible stack or the full repository stack.
- `KNOWN_COMMAND_SOURCES` (list; optional; shape: {REF, WHY_RELEVANT}): AGENTS, WORKFLOW, Makefile, package scripts, CI workflows, or repo scripts that define the verification order.

## Input Contract Notes
- `CHANGE_TYPE` should describe what changed, not whether the change is believed to be safe.
- `KNOWN_COMMAND_SOURCES` should point to repository-owned command definitions before inventing ad-hoc commands.
- When `VERIFICATION_POLICY` is omitted, default to the smallest credible stack that still checks the changed surface.

## Structured Outputs
- `VERIFICATION_PLAN` (list; required; shape: {STEP, COMMAND, WHY}): Ordered commands and why each command is required.
- `VERIFICATION_RESULTS` (list; required; shape: {STEP, STATUS, EVIDENCE}): Pass, fail, or blocked status with evidence.
- `FAILURE_SUMMARY` (list; required; shape: {ROOT_CAUSE, IMPACT, NEXT_ACTION}): Failures grouped by root cause rather than command order.
- `UNCHECKED_RISK` (list; required; shape: {RISK, WHY_NOT_CHECKED, CHEAPEST_NEXT_CHECK}): Any relevant check that was not run.

## Output Contract Notes
- `VERIFICATION_PLAN` should stay executable and ordered.
- `VERIFICATION_RESULTS` should cite the command or artifact that produced the evidence.
- `FAILURE_SUMMARY` should merge duplicate symptoms that point to the same root cause.
- `UNCHECKED_RISK` must be explicit when the repo cannot support a required check.

## Primary Lens
- `primary_lens`: `kent-beck`
- `why`: Verification should stay fast, factual, and immediately repair-oriented.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: verification-report.v1

## Response Format
Think and operate in English, but deliver the final response in Korean.
Lead with one line:
`Verification: pass|fail|partial — scope: [TARGET_SCOPE] — stack: [N] step(s)`

Then show:
- Plan: ordered verification commands with one-line purpose.
- Result: each command → pass/fail/blocked → key evidence.
- Root-cause summary: merged by underlying cause, not log order.
- Unchecked risk: only what materially remains outside the executed stack.

If blocked, end with:
`Blocked by: [missing dependency or environment] — cheapest next check: [X]`

## Neutrality Rules
- Do not declare success when a materially relevant check was skipped without being surfaced.
- Do not confuse command failure order with causal priority.
- Prefer repository-defined verify commands over hand-assembled alternatives.

## Execution Constraints
- Do not edit generated files directly as a way to silence verification drift unless the generating source also changed.
- Prefer the repository's smallest credible verification path before escalating to the full stack.
- Re-run the failed command after a fix before declaring the root cause resolved.

## References
- `references/command-discovery-order.md`
- `references/verification-report-template.md`

## Example Invocation
```text
$code-change-verification TARGET_SCOPE: src/auth CHANGE_TYPE: runtime VERIFICATION_POLICY: smallest-relevant KNOWN_COMMAND_SOURCES:
- REF: AGENTS.md
  WHY_RELEVANT: repository rules say which checks are mandatory
- REF: Makefile
  WHY_RELEVANT: defines format, lint, typecheck, and tests entrypoints
```
