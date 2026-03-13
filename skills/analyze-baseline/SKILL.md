---
name: analyze-baseline
description: "Capture a statistically valid performance baseline with variance analysis and budget determination before optimization. Use when you need a reproducible before-measurement, not when optimization work has already started."
---

# Analyze / Baseline

## Purpose
Lock a measurable, reproducible baseline before optimization — including variance analysis, confidence intervals, and an evidence-backed budget.

## Default Program
```text
[stages: preflight>detect>analyze>verify>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,perf-aware,deterministic-output | lens: goldratt-toc | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `goldratt-toc` because it keeps the work aligned with: Find the system constraint and optimize end-to-end throughput — baseline first, constraint identified.

## Use When
- Need to capture a statistically valid performance baseline before optimization.
- Need variance analysis to determine whether a measurement is stable enough to compare.
- Need an evidence-backed budget tied to a concrete constraint.

## Do Not Use When
- Optimization is already measured and only code changes remain.
- Need general performance review rather than baseline capture.
- There is no concrete metric to optimize.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Optimization target.
- `METRIC_NAME` (latency|throughput|memory|cpu|custom; required): Primary performance metric.
- `MEASUREMENT_METHOD` (command|benchmark|profile|custom; required): How the baseline will be captured.
- `SAMPLE_SIZE` (number; optional): Number of samples for statistical confidence. Defaults to minimum needed for 95% confidence.
- `BUDGET_HINT` (string; optional): Known target budget or threshold if one already exists.

## Input Contract Notes
- METRIC_NAME should identify one primary metric so the baseline is comparable later.
- MEASUREMENT_METHOD should be reproducible enough that before-and-after comparison is meaningful.
- If no explicit budget exists yet, BUDGET_HINT may be omitted and the output budget will be marked provisional.

## Structured Outputs
- `METRIC_DEFINITION` (string; required): Exact metric definition — what is measured and under which conditions.
- `BASELINE_RESULT` (object; required; shape: {VALUE, UNIT, VARIANCE, P50, P95, P99, METHOD, ENVIRONMENT}): Baseline result with statistical distribution.
- `STABILITY_ASSESSMENT` (object; required; shape: {IS_STABLE, VARIANCE_PCT, RECOMMENDATION}): Whether the baseline is stable enough for comparison.
- `SYSTEM_CONSTRAINT` (string; required): Identified bottleneck based on the measurement.
- `PERFORMANCE_BUDGET` (string; required): Target budget with basis stated. Marked provisional when no explicit budget was given.

## Output Contract Notes
- BASELINE_RESULT must include variance so later comparisons can be statistically valid.
- STABILITY_ASSESSMENT should flag when variance is too high for reliable comparison.
- SYSTEM_CONSTRAINT identifies where the measured bottleneck lives, not a redesign recommendation.
- PERFORMANCE_BUDGET may be provisional but must state its basis.

## Primary Lens
- `primary_lens`: `goldratt-toc`
- `why`: Capture the current constraint and throughput baseline before optimizing; stability matters more than a single data point.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: perf-baseline.v1

## Neutrality Rules
- Keep metric definition and baseline separate from optimization ideas.
- Mark noisy or unstable baseline measurements explicitly.
- Do not compare incompatible metrics or environments.

## Execution Constraints
- Do not turn this skill into optimization planning or code change work.
- Prefer one stable metric and one reproducible capture path over multiple loosely comparable numbers.
- If measurement is noisy, report instability instead of pretending the baseline is precise.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

기준값: [메트릭] = [값] [단위] — 측정 방법: [어떻게] — 환경: [어디서]

분포: p50=[값] / p95=[값] / p99=[값] — 변동성: [안정/불안정 (변동률%)]

불안정하면: "기준값 불안정 — 변동률 [N]% — 비교에 쓰기 위험함"

병목: [어디서 제약이 생기는지]

목표값: [목표] — 근거: [어디서 나온 숫자인지, 또는 "잠정값"]

마지막에: "목표값 맞나요? 맞으면 최적화로 넘어갑니다."

## Execution Constraints
- Do not turn this skill into optimization planning or code change work.
- If the measurement is noisy, report instability instead of pretending the baseline is precise.

## Example Invocation
```text
$analyze-baseline
SCOPE: src/search
METRIC: latency
METHOD: benchmark
SAMPLE_SIZE: 100
```
