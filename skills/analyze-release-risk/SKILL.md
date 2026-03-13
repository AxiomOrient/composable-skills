---
name: analyze-release-risk
description: "Analyze release or quality-gate risk with explicit evidence and gate status mapping. Use when you need a neutral risk analysis before merge or release, not a full GO/NO-GO verdict."
---

# Analyze / Release Risk

## Purpose
Assess release or quality-gate risk with explicit evidence — gate status mapping, risk classification, and gap identification — without issuing a final GO/NO-GO verdict.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: diff | policy: evidence,quality-gates{tests,security,compat,style},deterministic-output | lens: kahneman-tversky | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kahneman-tversky` because it keeps the work aligned with: Separate observed evidence from inferred risk, expose uncertainty, and resist conclusion-first bias.

## Use When
- Need regression, gate, or release-adjacent risk analysis.
- Need explicit gate status (pass/fail/unverified) before merge or release.
- Need audit evidence without a hard GO/NO-GO verdict.

## Do Not Use When
- Need a general review verdict — use `review-change` instead.
- Need vulnerability analysis only — use `review-security` instead.
- Need full GO/NO-GO release judgment — use `release-verdict` instead.

## Required Inputs
- `TARGET_SCOPE` (diff|file|module|folder|repo; required): Scope to analyze.
- `RISK_FOCUS` (regression|compatibility|security|performance|mixed; required): Primary risk dimension.
- `CHANGE_INTENT` (string; required): Claimed purpose of the change.
- `KNOWN_GATE_SIGNAL` (list; optional; shape: {SIGNAL, STATUS, SOURCE}): Known test, security, compat, or CI signals.

## Input Contract Notes
- CHANGE_INTENT should describe the claimed purpose of the change, not the analysis verdict expected.
- KNOWN_GATE_SIGNAL should distinguish observed gate evidence from assumed or stale status.
- Use RISK_FOCUS to narrow the primary gate lens, not to preload a conclusion.

## Structured Outputs
- `GATE_STATUS_MAP` (list; required; shape: {GATE, STATUS, EVIDENCE, COVERAGE}): Status of each relevant gate with coverage assessment.
- `RISK_FINDINGS` (list; required; shape: {RISK, GATE, SEVERITY, EVIDENCE, CONFIDENCE}): Risk findings with severity and confidence.
- `UNVERIFIED_GATES` (list; required; shape: {GATE, WHY_UNVERIFIED, CHEAPEST_CHECK}): Gates that could not be verified with cheapest check.
- `RISK_SUMMARY` (string; required): Evidence-backed risk characterization — not a GO/NO-GO verdict.

## Output Contract Notes
- RISK_FINDINGS may be empty when the gate evidence is clean.
- UNVERIFIED_GATES should identify the cheapest check for each gap.
- RISK_SUMMARY should characterize risk level without prescribing a release decision.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `why`: Risk analysis must separate observed gate signals from inferred risk and mark uncertainty explicitly.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: release-risk-analysis.v1

## Neutrality Rules
- Separate gate evidence from risk characterization.
- If a gate is unverified, mark it as a gap instead of assuming pass or fail.
- Do not inflate style preference into a blocker without regression or release impact.

## Execution Constraints
- Do not issue a GO/NO-GO verdict — risk analysis only.
- Do not manufacture blockers because the prompt asks for a risk analysis.
- Mark unverified gates explicitly rather than assuming clean.
- Keep analysis tied to concrete gate signals.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

게이트 상태:
| 게이트 | 상태 (통과/실패/미확인) | 근거 | 커버리지 |
|--------|----------------------|------|---------|

위험 발견사항:
- [게이트] — 위치: [파일:줄] — 위험: [무엇이 문제] — 심각도: [높음/중간/낮음] — 신뢰도: [높음/중간/낮음]

미확인 게이트:
- [게이트] — 왜 못 확인했는지 — 가장 빠른 확인 방법: [명령어/테스트]

전체 위험 수준: [한 문장 — GO/NO-GO 아님]

마지막에: "릴리즈 결정이 필요하면 release-verdict로 넘어갈까요?"

## Mandatory Rules
- Do not issue a GO/NO-GO verdict.
- Return empty RISK_FINDINGS when gate evidence does not support a finding.

## Example Invocation
```text
$analyze-release-risk
SCOPE: diff
RISK_FOCUS: regression
CHANGE_INTENT: "Adding pagination to the users list API"
```
