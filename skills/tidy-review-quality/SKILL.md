---
name: tidy-review-quality
description: "Read-only review skill that inspects a bounded change scope for code-quality cleanup opportunities: redundant state, parameter sprawl, near-duplicate branches, leaky abstractions, and stringly-typed logic."
---
# Tidy / Review Quality

## Purpose
Review a bounded scope for structural code-quality issues that should be cleaned up after the main implementation is complete.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: diff|repo|paths(glob,...) | policy: evidence,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Required Inputs
- `REVIEW_SCOPE` (diff|recent-files|path-set; required; allowed: diff|recent-files|path-set): How to choose the files to review.
- `TARGET_SCOPE` (path|module|folder|repo; optional): Explicit path boundary when REVIEW_SCOPE is path-set, or a narrowing filter over a diff.
- `FOCUS_HINTS` (list; optional; shape: {AREA, WHY}): Optional quality concerns to prioritize.

## Structured Outputs
- `QUALITY_FINDINGS` (list; required; shape: {ISSUE, LOCATION, SIGNAL, WHY_IT_HURTS, RECOMMENDED_FIX}): Actionable structural quality findings.
- `QUALITY_HOLDS` (list; required; shape: {LOCATION, WHY_OK}): Areas reviewed and intentionally left alone because the structure carries a real invariant or boundary.
- `REVIEW_STATUS` (clean|findings|inconclusive; required; allowed: clean|findings|inconclusive): Whether the scope is clean, has findings, or lacks enough evidence.
