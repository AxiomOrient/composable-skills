---
name: analyze-evidence-gap
description: "Identify missing evidence, score confidence levels, and rank the cheapest next checks before a claim can be trusted. Use when the main job is to map uncertainty with explicit confidence scoring."
---

# Analyze / Evidence Gap

## Purpose
Turn a shaky claim into an explicit confidence map — scored evidence levels, classified gaps, and information-value-ranked next checks.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: kahneman-tversky | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kahneman-tversky` because it keeps the work aligned with: Separate observed evidence from inferred risk, quantify confidence, and resist conclusion-first bias.

## Use When
- Need to know what evidence is still missing before a claim can be trusted.
- Need explicit confidence scoring, not just a vague "we're not sure".
- Need the cheapest next checks ranked by information value.

## Do Not Use When
- Need current-state structure mapping rather than uncertainty mapping.
- Need option comparison rather than evidence sufficiency checking.
- Need debugging, implementation, or review verdicts.

## Required Inputs
- `TARGET_SCOPE` (file|module|folder|repo|artifact; required): Bounded scope the claim depends on.
- `CLAIM_UNDER_CHECK` (string; required): Claim, assumption, or conclusion that may lack enough evidence.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Current evidence already available.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Time, scope, or cost limits for additional checking.

## Input Contract Notes
- CLAIM_UNDER_CHECK should name the exact belief or conclusion whose evidence is still uncertain.
- KNOWN_EVIDENCE should include only current artifacts, not planned checks.
- Use CONSTRAINTS to explain why some high-value checks may be deferred.

## Structured Outputs
- `CONFIDENCE_SCORE` (object; required; shape: {LEVEL, SCORE_0_100, RATIONALE}): Overall confidence with 0-100 score and rationale.
- `CURRENT_EVIDENCE` (list; required; shape: {OBSERVATION, LOCATION, EVIDENCE_TYPE, STRENGTH}): Current evidence with type classification (direct/indirect/circumstantial) and strength.
- `EVIDENCE_GAPS` (list; required; shape: {GAP, GAP_TYPE, CONFIDENCE_IMPACT, WHY_IT_BLOCKS}): Missing proof with gap type and quantified confidence impact.
- `CONFIDENCE_LIMITS` (list; required; shape: {LIMIT, WHY}): What cannot be concluded yet and why.
- `NEXT_CHECKS` (list; required; shape: {CHECK, INFORMATION_VALUE, EXPECTED_SIGNAL}): Cheapest next checks ranked by information value.

## Output Contract Notes
- CONFIDENCE_SCORE should distinguish total lack of evidence from partial but weak evidence.
- CURRENT_EVIDENCE should classify each piece as direct, indirect, or circumstantial.
- EVIDENCE_GAPS should estimate how much each gap reduces confidence.
- NEXT_CHECKS should be small, discriminating, and ordered by information value descending.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `why`: Evidence-gap analysis must score confidence explicitly, classify evidence strength, and rank next checks by information value.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: evidence-gap-analysis.v1

## Neutrality Rules
- Separate current proof from missing proof.
- Do not invent confidence where evidence is thin.
- Prefer the cheapest discriminating next check over broad speculative work.

## Execution Constraints
- Do not turn evidence-gap analysis into review verdicts or implementation advice.
- Keep the result bounded to the stated claim and scope.
- Explain why each gap matters instead of listing generic unknowns.
- Extract 3-7 anchor facts first; include at least one from the middle.
- Ask 2-4 verification questions that force a fresh rescan against current evidence.
- If first pass produces generic gaps, rewrite so missing entities become explicit.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

신뢰도: [지지됨/불충분/지지안됨] — 점수: [0-100] — 이유: [한 줄]

현재 근거:
- [관찰 내용] — 위치: [파일/문서] — 종류: [직접/간접/정황] — 강도: [강/중/약]

부족한 근거:
- [무엇이 없는지] — 신뢰도 영향: [얼마나 줄이는지]

다음 확인 (정보 가치 높은 것부터):
1. [확인 방법] — 알 수 있는 것: [무엇]

미확인: "[범위 밖이어서 확인 못 한 부분]"

마지막에: "[가장 정보가치 높은 확인] 먼저 해볼까요?"

## Mandatory Rules
- Do not treat the claim as adequately supported unless anchor facts and verification pass both support that conclusion.

## Example Invocation
```text
$analyze-evidence-gap
SCOPE: src/auth
CLAIM: "JWT token validation is secure against replay attacks"
```
