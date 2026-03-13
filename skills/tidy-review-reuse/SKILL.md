---
name: tidy-review-reuse
description: "Read-only review skill that inspects a bounded change scope for missed reuse opportunities. Find newly written logic that should call existing helpers, utilities, shared modules, or adjacent abstractions instead."
---
# Tidy / Review Reuse

## Purpose
Review a bounded scope for new logic that should reuse existing code instead of reimplementing it.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: diff|repo|paths(glob,...) | policy: evidence,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Required Inputs
- `REVIEW_SCOPE` (diff|recent-files|path-set; required; allowed: diff|recent-files|path-set): How to choose the files to review.
- `TARGET_SCOPE` (path|module|folder|repo; optional): Explicit path boundary when REVIEW_SCOPE is path-set, or a narrowing filter over a diff.
- `FOCUS_HINTS` (list; optional; shape: {AREA, WHY}): Optional focus areas such as parsing helpers, type guards, or path handling.

## Structured Outputs
- `REUSE_FINDINGS` (list; required; shape: {ISSUE, LOCATION, EXISTING_ASSET, WHY_REUSE, RECOMMENDED_CHANGE}): Actionable reuse findings tied to a concrete existing asset.
- `SEARCH_EVIDENCE` (list; required; shape: {PATTERN, MATCH, WHY_RELEVANT}): Searches or codebase matches that justify each finding.
- `REVIEW_STATUS` (clean|findings|inconclusive; required; allowed: clean|findings|inconclusive): Whether the scope is clean, has findings, or lacks enough evidence.
