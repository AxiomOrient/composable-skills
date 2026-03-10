---
name: scout-facts
description: "Neutral analysis-only skill. Produce evidence-based findings and option comparison reports only. Do not plan, implement, or review code here. English triggers: analysis report, cause analysis, option analysis."
---

# Scout Facts

## Purpose
Produce an evidence-first analysis without implementation or verdict work.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,quality-gates{tests,security},deterministic-output |
 lens: kahneman-tversky |
 output: md(contract=v1)]
```

## Use When
- Need evidence-first analysis before implementation.
- Need root-cause analysis, option comparison, structure mapping, or evidence-gap analysis.
- Need a recommendation that remains explicitly separated from evidence.

## Do Not Use When
- Need direct code changes.
- Need immediate incident recovery or debugging.
- Need final review or release judgement.

## Required Inputs
- `ANALYSIS_GOAL` (root-cause|option-compare|structure-map|evidence-gap; required; allowed: root-cause|option-compare|structure-map|evidence-gap): Exact analysis job.
- `TARGET_SCOPE` (file|module|folder|repo|artifact; required): Bounded target scope.
- `QUESTION` (string; required): Uncertainty or decision to resolve.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Known files, logs, commands, or measurements.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Time, scope, or non-goal constraints.

## Input Contract Notes
- TARGET_SCOPE must stay bounded enough that every major claim can cite concrete evidence from within scope.
- QUESTION should be one decision or uncertainty, not a broad brainstorming topic.
- KNOWN_EVIDENCE should point to existing artifacts only; do not preload conclusions into the evidence list.
- If simplicity, core-user impact, or non-essential work reduction matters to the decision, state it explicitly in CONSTRAINTS instead of assuming it by default.

## Structured Outputs
- `OBSERVED_EVIDENCE` (list; required; shape: {OBSERVATION, LOCATION, EVIDENCE}): Observed facts grounded in files, logs, commands, or measurements.
- `INFERRED_FINDINGS` (list; required; shape: {FINDING, BASED_ON, CONFIDENCE}): Interpretations derived from observed evidence, kept separate from raw observation.
- `OPTION_SET` (list; optional; required when ANALYSIS_GOAL=option-compare; shape: {OPTION, UPSIDE, DOWNSIDE, RECOMMENDED}): Compared options with trade-offs.
- `RECOMMENDATION` (string; required): Selected recommendation.
- `NEXT_VERIFICATION_STEPS` (list; required; shape: {STEP, PURPOSE, EXPECTED_SIGNAL}): Cheapest next checks when evidence is incomplete.

## Output Contract Notes
- Keep OBSERVED_EVIDENCE and INFERRED_FINDINGS separate; every inference should point back to cited evidence.
- OPTION_SET is required only for option-compare runs; omit it for other analysis goals instead of filling placeholders.
- RECOMMENDATION may explicitly be hold or inconclusive when evidence is insufficient.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `frame_name`: Bias-Aware Evidence Judge
- `why`: Use a bias-aware evidence lens so analysis stays neutral, separates observation from inference, and marks uncertainty before recommendation.
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
- `artifacts_out`: analysis-report.v1

## Neutrality Rules
- Separate observation, evidence, inference, and recommendation.
- Do not invent defects or implementation direction without evidence.
- Return no-finding or inconclusive when evidence is insufficient.

## Execution Constraints
- Do not patch code, generate implementation plans, or deliver review verdicts from this skill.
- Prefer the cheapest discriminating next check over broad speculative follow-up work.
- If the evidence cannot support a claim, say inconclusive instead of smoothing the gap away.

## Output Discipline
- `response_profile=analysis_report`
- User-facing rendering is delegated to `respond`.
