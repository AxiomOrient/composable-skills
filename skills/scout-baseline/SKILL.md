---
name: scout-baseline
description: "Capture the exact performance metric, baseline, and budget before optimization. Use when the immediate job is to define and record the baseline, not to optimize yet."
---

# Scout / Baseline

## Purpose
Prevent measurement-free optimization by locking metric, budget, and baseline first.

## Default Program
```text
[stages: preflight>detect>analyze>verify>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,perf-aware,deterministic-output | lens: goldratt-toc | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `goldratt-toc` because it keeps the work aligned with: Find the system constraint and optimize end-to-end throughput.

## Use When
- Need to capture a performance baseline before optimization.
- Need a metric definition and budget for perf work.
- Need repeatable before/after measurement inputs.

## Do Not Use When
- Optimization is already measured and only code changes remain.
- Need general performance review rather than baseline capture.
- There is no concrete metric to optimize.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Optimization target.
- `METRIC_NAME` (latency|throughput|memory|custom; required): Primary performance metric.
- `MEASUREMENT_METHOD` (command|benchmark|profile|custom; required): How the baseline will be captured.
- `BUDGET_HINT` (string; optional): Known target budget or threshold if one already exists.

## Input Contract Notes
- METRIC_NAME should identify one primary metric so the baseline is comparable later.
- MEASUREMENT_METHOD should be reproducible enough that before-and-after comparison is meaningful.
- If no explicit budget exists yet, BUDGET_HINT may be omitted and the output budget should be marked provisional.

## Structured Outputs
- `METRIC_DEFINITION` (string; required): Exact metric definition.
- `BASELINE_RESULT` (object; required; shape: {VALUE, UNIT, METHOD, ENVIRONMENT}): Baseline measurement result.
- `PERFORMANCE_BUDGET` (string; required): Target budget or success threshold.

## Output Contract Notes
- BASELINE_RESULT should identify the environment and method so later measurements are comparable.
- PERFORMANCE_BUDGET may be provisional when no explicit budget exists yet, but the basis should be stated.
- METRIC_DEFINITION should stay specific enough that later optimization work does not quietly switch metrics.

## Primary Lens
- `primary_lens`: `goldratt-toc`
- `why`: Capture the current constraint and throughput baseline before optimizing.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: perf-baseline.v1

## Neutrality Rules
- Keep metric definition and baseline separate from optimization ideas.
- Mark noisy or unstable baseline measurements explicitly.
- Do not compare incompatible metrics or environments.

## Response Format

Think and operate in English, but deliver the final response in Korean.

Show the baseline as one line: [metric] = [value] [unit] — method: [how captured] — environment: [where]

State the performance budget: [target] — basis: [where this number came from or "provisional"]

Flag noise: "Baseline is unstable — variance [N]% — not safe for comparison yet."

Didn't check: [anything outside the stated metric or measurement path].

Ask: "Budget looks right? Want to lock this and move to optimization?"

## Execution Constraints
- Do not turn this skill into optimization planning or code change work.
- Prefer one stable metric and one reproducible capture path over multiple loosely comparable numbers.
- If the measurement is noisy, report the instability instead of pretending the baseline is precise.

## Example Invocation
```text
$scout-baseline
TARGET_SCOPE: src/search
METRIC_NAME: latency
MEASUREMENT_METHOD: benchmark
```
