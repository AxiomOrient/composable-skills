---
name: check-quality-scan
description: "Checklist-only quality inspection for changed code. Verify 9 fixed items: design elegance, conciseness, latent bugs, goal achievement, security, duplicate code, performance, constant extraction, and unnecessary code. Do not use as a standalone verdict; compose with check-merge-ready when integrate/hold judgement is needed."
---

# Check / Quality Scan

## Purpose
Check code quality against a fixed checklist without replacing verdict review.

## Fixed Checklist
The following 9 items are always evaluated. CHECKLIST_TABLE must contain exactly these rows:

| # | Item | What to Check |
|---|------|---------------|
| 1 | Design Elegance | Does the design solve the problem without unnecessary layers, indirection, or abstraction? |
| 2 | Conciseness | Is the implementation as short as it can be while remaining readable? |
| 3 | Latent Bugs | Are there off-by-one errors, null dereferences, race conditions, or unchecked error paths? |
| 4 | Goal Achievement | Does the change actually accomplish the stated CHANGE_GOAL without scope creep? |
| 5 | Security | Are there injection risks, unsafe deserialization, exposed secrets, or broken auth paths? |
| 6 | Duplicate Code | Is behavior that already exists elsewhere being re-implemented? |
| 7 | Performance | Are there unnecessary allocations, N+1 queries, blocking calls, or quadratic paths? |
| 8 | Constant Extraction | Are magic numbers, repeated strings, or configuration values inlined instead of named? |
| 9 | Unnecessary Code | Does the diff include dead code, unreachable branches, or unused variables? |

TARGET_AREA maps emphasis to these items: `security` → item 5; `perf` → item 7; `duplication` → item 6; `constants` → item 8; `general-quality` → items 1, 2, 4, 9.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: diff |
 policy: evidence,quality-gates{tests,security,perf,compat,style},deterministic-output |
 lens: kahneman-tversky |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kahneman-tversky` because it keeps the work aligned with: Separate observed evidence from inferred risk, expose uncertainty, and resist conclusion-first bias.

## Use When
- Need the mandatory 9-item checklist evaluated.
- Need explicit pass/risk/unknown output across fixed quality dimensions.
- Need checklist evidence before a final review or audit.

## Do Not Use When
- Need direct code implementation.
- Need a single narrow scan instead of the full checklist.
- Need final integrate/hold verdict only.

## Required Inputs
- `CHECK_SCOPE` (diff|file|module|folder; required): Scope to inspect.
- `CHANGE_GOAL` (string; required): Intended behavior or maintenance goal.
- `TARGET_AREA` (security|perf|duplication|constants|general-quality; optional): Optional emphasis area.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Tests, benchmarks, issue context, or supporting evidence.

## Input Contract Notes
- CHANGE_GOAL should describe the intended behavior or maintenance result, not the checklist verdict you want to receive.
- TARGET_AREA narrows emphasis only; it does not remove the obligation to report the full fixed checklist.
- KNOWN_EVIDENCE should cite existing tests, benchmarks, or artifacts rather than conclusions.

## Structured Outputs
- `CHECKLIST_TABLE` (list; required; shape: {ITEM, STATUS, EVIDENCE, ACTION}): Checklist rows with item, status, evidence, and action.
- `FINDINGS_SUMMARY` (list; required; shape: {ISSUE, ITEM, EVIDENCE, IMPACT}): Material risks surfaced by the checklist.
- `UNKNOWN_ITEMS` (list; required; shape: {ITEM, CHEAPEST_CHECK}): Unknown items plus cheapest verification steps.

## Output Contract Notes
- CHECKLIST_TABLE should cover the fixed checklist even when TARGET_AREA narrows emphasis for deeper commentary.
- Use FINDINGS_SUMMARY only for material risks supported by evidence; do not restate every checklist row there.
- Use UNKNOWN_ITEMS when evidence is missing instead of forcing a pass or risk label.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `why`: Checklist review should resist conclusion-first bias and keep risk claims evidence-backed.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: quality-checklist-report.v1

## Neutrality Rules
- Use pass, risk, or unknown only; do not force a negative finding.
- If evidence is insufficient for a checklist item, mark it unknown with the cheapest verification step.
- Do not elevate style preference above behavior, safety, or performance evidence.

## Response Format

Show the 9-item checklist as a compact table:
- # | Item | Status (pass/risk/unknown) | Key evidence

List material risks below the table, one line each: item number → finding → impact.

List unknown items with cheapest verification step.

End with any risk items that need action before merge.

## Execution Constraints
- Do not collapse the checklist into a generic review verdict from this skill.
- Keep each item scoped to observable evidence rather than taste-only commentary.
- If multiple items point to the same issue, record the issue once in FINDINGS_SUMMARY and keep the row-by-row detail in CHECKLIST_TABLE.
