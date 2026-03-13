---
name: analyze-options
description: "Compare explicit options with evidence-backed trade-offs and a weighted decision matrix. Use when the main job is to choose between named alternatives with analytical rigor."
---

# Analyze / Options

## Purpose
Turn a decision question and explicit option set into a disciplined, scored, evidence-backed comparison.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: kahneman-tversky | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kahneman-tversky` because it keeps the work aligned with: Separate observed evidence from inferred risk, apply explicit weights, expose uncertainty, and resist conclusion-first bias.

## Use When
- Need a rigorous, scored comparison of explicit options before planning or implementation.
- Need quantitative trade-off weighting, not just qualitative impressions.
- Need one recommendation tied to bounded evidence and explicit scoring.

## Do Not Use When
- Need current-state structure mapping rather than decision comparison.
- Need evidence-gap analysis without a concrete option set.
- Need debugging, implementation, or review verdicts.

## Required Inputs
- `TARGET_SCOPE` (file|module|folder|repo|artifact; required): Bounded scope the decision applies to.
- `DECISION_QUESTION` (string; required): Exact choice to resolve.
- `OPTION_SET` (list; required; shape: {OPTION, DESCRIPTION}): Explicit options to compare.
- `DECISION_CRITERIA` (list; optional; shape: {CRITERION, WEIGHT}): Criteria and relative weights for scoring.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Files, docs, measurements, or prior notes.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Hard limits that change the trade-off.

## Input Contract Notes
- OPTION_SET should contain real candidate options, not vague directions like "better architecture".
- DECISION_QUESTION should identify one choice, not a bundle of decisions.
- DECISION_CRITERIA enables weighted scoring; omit to derive criteria from the decision context.
- Use CONSTRAINTS for hard limits that rule out options, not general preferences.

## Structured Outputs
- `OBSERVED_EVIDENCE` (list; required; shape: {OBSERVATION, LOCATION, EVIDENCE}): Observed facts relevant to the choice.
- `SCORING_MATRIX` (object; required; shape: {CRITERIA, OPTION_SCORES}): Scored comparison per criterion per option.
- `OPTION_COMPARISON` (list; required; shape: {OPTION, UPSIDE, DOWNSIDE, SCORE, FIT}): Trade-off comparison with score and constraint fit.
- `RECOMMENDATION` (string; required): Recommended option or inconclusive result with rationale.
- `CHEAPEST_NEXT_CHECK` (string; required): Next check that would most reduce remaining uncertainty.

## Output Contract Notes
- SCORING_MATRIX should show numerical or ranked scores per criterion.
- OPTION_COMPARISON should compare only the supplied options.
- RECOMMENDATION may be inconclusive when evidence cannot discriminate strongly enough.
- CHEAPEST_NEXT_CHECK should identify one high-value next signal.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `why`: Option comparison must separate observed evidence from trade-off judgement, apply explicit weights, and mark uncertainty before recommending.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: option-analysis.v1

## Neutrality Rules
- Compare the explicit options instead of inventing a preferred hidden third path.
- Separate observed evidence from trade-off interpretation.
- Return inconclusive when evidence cannot justify a recommendation.

## Execution Constraints
- Do not turn option comparison into implementation planning.
- Keep the comparison proportional to the stated decision question.
- Extract 3-7 anchor facts before comparing options.
- Before final recommendation, ask 2-4 verification questions that could overturn the leading option.
- If first pass omits a salient counter-signal, rewrite with higher density instead of adding length.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

결론부터: [선택지] 추천 — 또는 "증거 부족으로 결론 없음"

점수 비교:
| 기준 | 비중 | [옵션A] | [옵션B] |
|------|-----|---------|---------|
| [기준] | [높음/중간/낮음] | [점수] | [점수] |

장단점:
- [옵션] — 장점: [무엇이 좋은지] — 단점: [무엇이 나쁜지]

불확실하면: "다음으로 줄일 수 있음 — [가장 빠른 확인 방법]"

마지막에: "[추천 옵션의 가장 큰 단점]이 결정을 바꾸나요?"

## Mandatory Rules
- Do not emit RECOMMENDATION until anchor facts and verification pass either support it or force an explicit inconclusive result.

## Example Invocation
```text
$analyze-options
SCOPE: src/cache
QUESTION: Redis vs in-memory cache for session data
OPTIONS:
  - Redis: distributed, persistent
  - In-memory: fast, ephemeral
CRITERIA:
  - latency (high)
  - operational cost (medium)
  - failure safety (high)
```
