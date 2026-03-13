---
name: tidy-review-efficiency
description: "Read-only review skill that inspects a bounded change scope for efficiency cleanup opportunities: unnecessary work, missed concurrency, hot-path bloat, TOCTOU-style existence checks, memory growth, and overly broad operations. Do not use for benchmark-driven optimization implementation itself."
---
# Tidy / Review Efficiency

## Purpose
Review a bounded scope for safe efficiency improvements that should be cleaned up after the main implementation.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: diff|recent-files|paths(glob,...) | policy: evidence,deterministic-output | lens: goldratt-toc | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `goldratt-toc` because efficiency review should identify the real local bottleneck or wasted work, not cargo-cult micro-optimizations.

## Use When
- Need a focused pass for wasted work in recent changes.
- Need to review a diff for hot-path bloat, repeated I/O, or missed parallelism.
- Need one specialized efficiency review before deciding what cleanup to implement.

## Do Not Use When
- Need to implement benchmark-driven performance changes across a large scope.
- Need direct code edits.
- Need broad system profiling instead of bounded review.

## Required Inputs
- `REVIEW_SCOPE` (diff|recent-files|path-set; required; allowed: diff|recent-files|path-set): How to choose the files to review.
- `TARGET_SCOPE` (path|module|folder|repo; optional): Explicit path boundary when REVIEW_SCOPE is `path-set`, or a narrowing filter over a diff.
- `FOCUS_HINTS` (list; optional; shape: {AREA, WHY}): Optional efficiency concerns to prioritize, such as memory pressure or startup latency.

## Input Contract Notes
- This is a bounded review skill, not a full benchmarking workflow.
- Efficiency findings should name the wasted work, the likely cost model, and the smallest safe improvement.
- Prefer obvious unnecessary work over speculative future bottlenecks.

## Structured Outputs
- `EFFICIENCY_FINDINGS` (list; required; shape: {ISSUE, LOCATION, COST_MODEL, RECOMMENDED_FIX, RISK}): Actionable efficiency findings with a visible cost model.
- `HOT_PATH_NOTES` (list; required; shape: {LOCATION, WHY_HOT}): Hot-path or repeated-path notes that justify why a finding matters.
- `REVIEW_STATUS` (clean|findings|inconclusive; required; allowed: clean|findings|inconclusive): Whether the scope is clean, has findings, or lacks enough evidence.

## Output Contract Notes
- Use `RISK` to call out behavior or readability tradeoffs when an efficiency fix is not obviously safe.
- Return `clean` when no concrete wasted work is visible in scope.
- Return `inconclusive` when the likely cost model depends on evidence that is unavailable.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: review-report.v1

## Neutrality Rules
- Do not optimize by folklore; every finding needs an observed local cost model.
- Prefer removing obvious wasted work before proposing deeper rewrites.
- Call out when a potential efficiency win would materially worsen readability or contract clarity.

## Execution Constraints
- This skill is read-and-review only; do not edit files.
- Review at least these classes of issues when present: unnecessary work, missed concurrency, hot-path bloat, pre-checking existence before operation, memory growth, and overly broad operations.
- Keep the review bounded to the supplied scope.

## Response Format
Lead with `CLEAN`, `FINDINGS`, or `INCONCLUSIVE`.

For each finding:
- [issue] — `file:line` — cost: [cost model] — fix: [smallest safe improvement]

If a hot path matters:
- hot path: `file:line` — [why this path is likely hot or repeated]

## Mandatory Rules
- Keep this skill read-only.
- Name the local cost model for every finding.
- Avoid speculative optimization advice with no scope evidence.

## Example Invocation
```text
$tidy-review-efficiency REVIEW_SCOPE: diff FOCUS_HINTS:
- AREA: memory efficiency
  WHY: the change added a new cache-like structure
```
