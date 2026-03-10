---
name: build-make-faster
description: "Use when performance bottlenecks require measurement, optimization, and before/after verification. Do not use when the task is general feature implementation or optimization guesses without measurement. English triggers: performance optimization, profiling, latency, memory optimization."
---

# Performance Optimizer

## Purpose
Measure and improve a bounded performance bottleneck with comparable before/after evidence.

## Default Program
```text
[stages: preflight>detect>analyze>plan>implement>verify>review>reflect>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,correctness-first,quality-gates{tests,security},perf-aware,safety-gates,deterministic-output |
 lens: goldratt-toc |
 output: md(contract=v1)]
```

## Use When
- Need measured performance optimization.
- Need baseline, bottleneck evidence, and after-result in one path.
- Need to optimize a bounded hot path or memory issue.

## Do Not Use When
- Need general feature implementation.
- Need only baseline capture before optimization.
- Need performance review without applying changes.

## Required Inputs
- `TARGET_SCOPE` (path|module|route|repo, required): Optimization target.
- `METRIC_NAME` (latency|throughput|memory|custom, required): Primary metric.
- `PERFORMANCE_BUDGET` (string, required): Target threshold or expected improvement.
- `BASELINE_EVIDENCE` (list, required): Benchmark, profile, or measurement inputs.

## Structured Outputs
- `METRIC_BASELINE` (object, required): Baseline metric snapshot.
- `BOTTLENECK_EVIDENCE` (list, required): Evidence of the bottleneck and chosen fix.
- `BEFORE_AFTER_RESULTS` (object, required): Comparable before/after measurement results.

## Primary Lens
- `primary_lens`: `goldratt-toc`
- `frame_name`: Constraint-First Optimizer
- `why`: Performance work should identify the bottleneck, measure it, and optimize the real constraint first.
- `summary`: Find the system constraint and optimize end-to-end throughput.
- `thesis`: Performance work improves when the real bottleneck is identified first and local optimizations are judged by system throughput, not by isolated micro-metrics.
- `decision_rules`:
  - Identify the constraint before proposing optimization work.
  - Measure throughput or end-to-end effect, not just local speedups.
  - Explain whether the change exploits, subordinates to, or elevates the constraint.
  - Reject optimizations that do not move the real bottleneck.
- `anti_patterns`:
  - Optimizing a non-constraint
  - Benchmarking without a throughput story
  - Perf work that omits the baseline
- `good_for`:
  - performance baselines
  - bottleneck analysis
  - throughput optimization
- `not_for`:
  - security control review
  - question engineering
  - README structure
- `required_artifacts`:
  - Constraint Identification
  - Baseline Throughput
  - Exploit, Subordinate, or Elevate Plan
- `references`:
  - https://www.toc-goldratt.com/en/about-toc

## Artifacts
- `artifacts_in`: perf-baseline.v1
- `artifacts_out`: performance-report.v1

## Neutrality Rules
- No optimization claim without comparable before/after evidence.
- Separate baseline capture from optimization ideas.
- If measurements are noisy or incompatible, mark them insufficient.

## Output Discipline
- `response_profile=performance_report`
- User-facing rendering is delegated to `respond`.
