---
name: build-make-faster
description: "Use when performance bottlenecks require measurement, optimization, and before/after verification. Do not use when the task is general feature implementation or optimization guesswork without measurement."
---

# Build / Make Faster

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

## Lens Rationale
This skill uses `goldratt-toc` because it keeps the work aligned with: Find the system constraint and optimize end-to-end throughput.

## Use When
- Need measured performance optimization.
- Need baseline, bottleneck evidence, and after-result in one path.
- Need to optimize a bounded hot path or memory issue.

## Do Not Use When
- Need general feature implementation.
- Need only baseline capture before optimization.
- Need performance review without applying changes.

## Required Inputs
- `TARGET_SCOPE` (path|module|route|repo; required): Optimization target.
- `METRIC_NAME` (latency|throughput|memory|custom; required): Primary metric.
- `PERFORMANCE_BUDGET` (string; required): Target threshold or expected improvement.
- `BASELINE_EVIDENCE` (list; required): Benchmark, profile, or measurement inputs.

## Structured Outputs
- `METRIC_BASELINE` (object; required): Baseline metric snapshot.
- `BOTTLENECK_EVIDENCE` (list; required): Evidence of the bottleneck and chosen fix.
- `BEFORE_AFTER_RESULTS` (object; required): Comparable before/after measurement results.

## Primary Lens
- `primary_lens`: `goldratt-toc`
- `why`: Performance work should identify the bottleneck, measure it, and optimize the real constraint first.

## Artifacts
- `artifacts_in`: perf-baseline.v1
- `artifacts_out`: performance-report.v1

## Response Format

Lead with the bottleneck in one line: what it is, where it is.

Then show:
- Baseline: [metric] = [value] ([method])
- Fix applied: [what changed]
- After: [metric] = [value] — [delta vs budget]

Ask: "Measurement stable? Want a regression guard added?"

## Neutrality Rules
- No optimization claim without comparable before/after evidence.
- Separate baseline capture from optimization ideas.
- If measurements are noisy or incompatible, mark them insufficient.
