---
name: test-run-user-scenarios
description: "Test-category scenario validation skill. Simulate realistic users and agents running the framework through happy, failure, and weird cases, then report where the skill surface is confusing, brittle, or missing guardrails."
---

# Test Run User Scenarios

## Purpose
Simulate real user and agent usage with concrete inputs and expected outputs, then expose where the framework breaks, confuses, or under-specifies behavior.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: repo|paths(glob,...) |
 policy: evidence,deterministic-output |
 lens: kahneman-tversky |
 output: md(contract=v1)]
```

## Use When
- Need to validate the framework against realistic use cases instead of only happy-path examples.
- Need concrete user and agent scenarios with varied inputs, expected outputs, and observable pass/fail signals.
- Need to include success cases, failure cases, and weird-but-plausible misuse cases before release or major refactors.

## Do Not Use When
- Need unit or integration test code written directly.
- Need only narrow test-gap analysis for one code path.
- Need final contract verification after the work is already complete.

## Required Inputs
- `SYSTEM_UNDER_TEST` (skill|workflow|macro-surface|skill-pack; required): Which framework surface is being exercised.
- `TARGET_SCOPE` (path|folder|repo|artifact; required): Exact area under test.
- `PRIMARY_USERS` (list; required; shape: {ROLE, GOAL, CONTEXT}): Realistic user or agent personas and the job each one is trying to finish.
- `SCENARIO_COUNT` (integer; optional): Target number of scenarios to generate and run. Default to 6 when omitted.
- `FAILURE_CLASSES` (list; optional; shape: {CLASS}): Failure or misuse classes to force into the scenario set, such as ambiguous input, missing context, wrong-skill pick, legacy name, or contradictory goal.
- `KNOWN_CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Scope, release, or realism constraints for the scenario run.

## Input Contract Notes
- PRIMARY_USERS should be grounded in plausible roles and goals, not fictional filler personas with no concrete job.
- SCENARIO_COUNT should stay small enough that each scenario can actually be exercised and observed.
- FAILURE_CLASSES should force meaningful breakage or misuse paths, not random nonsense with no learning value.

## Structured Outputs
- `USE_CASE_MATRIX` (list; required; shape: {SCENARIO, USER_ROLE, GOAL, INPUTS, EXPECTED_OUTPUT_SIGNAL}): Concrete happy-path use cases with explicit inputs and expected signals.
- `FAILURE_CASES` (list; required; shape: {SCENARIO, BAD_INPUT_OR_CONTEXT, EXPECTED_BREAKPOINT}): Realistic failure or misuse scenarios that should reveal brittle behavior or bad affordances.
- `ODD_CASES` (list; required; shape: {SCENARIO, WHY_PLAUSIBLE, WHAT_MIGHT_GO_WRONG}): Weird but plausible scenarios worth exercising.
- `EXECUTION_LOG` (list; required; shape: {SCENARIO, ACTION_TAKEN, OBSERVED_RESULT, STATUS}): What was actually exercised and what happened.
- `USABILITY_FINDINGS` (list; required; shape: {ISSUE, LOCATION, WHY_IT_CONFUSES_OR_FAILS}): Framework surface problems found through scenario execution.
- `NEXT_FIXES` (list; required; shape: {FIX, WHY_NOW, SMALLEST_CHECK_AFTER_FIX}): Smallest fixes or follow-up checks that improve real-world usability.

## Output Contract Notes
- USE_CASE_MATRIX should use concrete prompts, macros, or inputs that a real caller could plausibly produce.
- EXECUTION_LOG must separate observed results from expected results; do not backfill success without an actual run or observable signal.
- FAILURE_CASES and ODD_CASES should exist even when the happy path passes.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `frame_name`: Bias-Aware Evidence Judge
- `why`: Scenario testing should resist idealized happy-path bias and instead check what real callers are actually likely to do.
- `summary`: Use realistic scenarios, separate observed results from expectations, and value failure discovery over demo polish.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: scenario-test-report.v1

## Neutrality Rules
- Do not invent passing outcomes for scenarios that were not actually exercised.
- Prefer plausible misuse and ambiguity over theatrical nonsense.
- Separate framework confusion, skill-contract ambiguity, and parser/runtime failure.

## Execution Constraints
- Act as both caller and agent when constructing and exercising scenarios.
- Include at least one happy-path, one failure-path, and one weird-but-plausible case in every run.
- Prefer realistic prompts and inputs that a maintainer, contributor, or first-time user would actually type.

## Required References
- `references/scenario-patterns.md`

## Example Invocation
```text
$compose + $test-run-user-scenarios + @skills + [Simulate a first-time maintainer, a rushed releaser, and a confused docs contributor choosing skills for real work. Include happy, failure, and weird cases.]
```

## Output Discipline
- `response_profile=analysis_report`
- User-facing rendering is delegated to `respond`.
