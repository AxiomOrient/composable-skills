---
name: tidy-review-efficiency
description: "Read-only review skill that inspects a bounded change scope for efficiency cleanup opportunities: unnecessary work, missed concurrency, hot-path bloat, TOCTOU-style existence checks, memory growth, and overly broad operations."
---
# Tidy / Review Efficiency

## Purpose
Review a bounded scope for safe efficiency improvements that should be cleaned up after the main implementation.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: diff|repo|paths(glob,...) | policy: evidence,deterministic-output | lens: goldratt-toc | output: md(contract=v1)]
```

## Required Inputs
- `REVIEW_SCOPE` (diff|recent-files|path-set; required; allowed: diff|recent-files|path-set): How to choose the files to review.
- `TARGET_SCOPE` (path|module|folder|repo; optional): Explicit path boundary when REVIEW_SCOPE is path-set, or a narrowing filter over a diff.
- `FOCUS_HINTS` (list; optional; shape: {AREA, WHY}): Optional efficiency concerns to prioritize, such as memory pressure or startup latency.

## Structured Outputs
- `EFFICIENCY_FINDINGS` (list; required; shape: {ISSUE, LOCATION, COST_MODEL, RECOMMENDED_FIX, RISK}): Actionable efficiency findings with a visible cost model.
- `HOT_PATH_NOTES` (list; required; shape: {LOCATION, WHY_HOT}): Hot-path or repeated-path notes that justify why a finding matters.
- `REVIEW_STATUS` (clean|findings|inconclusive; required; allowed: clean|findings|inconclusive): Whether the scope is clean, has findings, or lacks enough evidence.
