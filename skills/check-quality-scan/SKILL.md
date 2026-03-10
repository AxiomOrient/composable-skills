---
name: check-quality-scan
description: "Neutral checklist-only quality inspection skill for changed code. Use when you must explicitly verify design elegance, code conciseness, latent bug risk, goal achievement, security issues, duplicate code, performance risk, constant/common extraction opportunities, and unnecessary code. Do not replace review verdict skills; compose with review or audit when final go/no-go judgement is required. Korean triggers: 설계는 우아해?, 코드는 간결해?, 잠재적인 버그는 없어?, 목적은 달성했어?, 보안 문제 없어?, 중복 코드 제거했어?, 성능 문제는 없어?, 상수화/공통화 가능해?, 불필요한 코드 없어?."
---

# Quality Checklist

## Purpose
Check code quality against a fixed checklist without replacing verdict review.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: diff |
 policy: evidence,quality-gates{tests,security,perf,compat,style},deterministic-output |
 lens: kahneman-tversky |
 output: md(contract=v1)]
```

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
- `frame_name`: Bias-Aware Evidence Judge
- `why`: Checklist review should resist conclusion-first bias and keep risk claims evidence-backed.
- `summary`: Separate observed evidence from inferred risk, expose uncertainty, and resist conclusion-first bias.
- `thesis`: Good judgement is not strong opinion; it is disciplined separation between what is observed, what is inferred, and what still needs checking.
- `decision_rules`:
  - Separate observed evidence from interpretation before assigning impact.
  - Mark uncertainty explicitly instead of smoothing it away into confident prose.
  - Check whether the current conclusion is driven by vivid anecdotes, availability bias, or conclusion-first framing.
  - Prefer the cheapest discriminating next check when evidence is incomplete.
- `anti_patterns`:
  - Severity inflation without evidence
  - Confusing likelihood with impact
  - Treating first-pass intuition as verdict
- `good_for`:
  - neutral analysis
  - review
  - audit
  - risk judgement
  - quality checklists
- `not_for`:
  - step-by-step debugging
  - incremental refactor design
  - information architecture work
- `required_artifacts`:
  - Observed Evidence
  - Risk Inference
  - Uncertainty Note
  - Cheapest Verification Step
- `references`:
  - https://www.nobelprize.org/prizes/economic-sciences/2002/kahneman/facts/

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: quality-checklist-report.v1

## Neutrality Rules
- Use pass, risk, or unknown only; do not force a negative finding.
- If evidence is insufficient for a checklist item, mark it unknown with the cheapest verification step.
- Do not elevate style preference above behavior, safety, or performance evidence.

## Execution Constraints
- Do not collapse the checklist into a generic review verdict from this skill.
- Keep each item scoped to observable evidence rather than taste-only commentary.
- If multiple items point to the same issue, record the issue once in FINDINGS_SUMMARY and keep the row-by-row detail in CHECKLIST_TABLE.

## Output Discipline
- `response_profile=review_findings`
- User-facing rendering is delegated to `respond`.
