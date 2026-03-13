---
name: scout-option-compare
description: "Compare explicit options with evidence-backed trade-offs inside a bounded scope. Use when the main job is to choose between named alternatives, not to map structure or debug a failure."
---

# Scout / Option Compare

## Purpose
Turn a decision question and explicit option set into a disciplined evidence-backed comparison.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: kahneman-tversky | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kahneman-tversky` because it keeps the work aligned with: Separate observed evidence from inferred risk, expose uncertainty, and resist conclusion-first bias.

## Use When
- Need to compare explicit options before planning or implementation.
- Need trade-offs, not just raw observations.
- Need one recommendation tied to bounded evidence.

## Do Not Use When
- Need current-state structure mapping rather than decision comparison.
- Need evidence-gap analysis without a concrete option set.
- Need debugging, implementation, or review verdicts.

## Required Inputs
- `TARGET_SCOPE` (file|module|folder|repo|artifact; required): Bounded scope the decision applies to.
- `DECISION_QUESTION` (string; required): Exact choice to resolve.
- `OPTION_SET` (list; required; shape: {OPTION, DESCRIPTION}): Explicit options to compare.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Files, docs, measurements, or prior notes already known.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Decision constraints or non-goals.

## Input Contract Notes
- OPTION_SET should contain the real candidate options, not vague directions such as `better architecture`.
- DECISION_QUESTION should identify one choice, not a bundle of decisions.
- Use CONSTRAINTS for hard limits that change the trade-off, not general preferences.

## Structured Outputs
- `OBSERVED_EVIDENCE` (list; required; shape: {OBSERVATION, LOCATION, EVIDENCE}): Observed facts that matter to the choice.
- `OPTION_COMPARISON` (list; required; shape: {OPTION, UPSIDE, DOWNSIDE, FIT}): Trade-off comparison for each option.
- `RECOMMENDATION` (string; required): Recommended option or inconclusive result.
- `CHEAPEST_NEXT_CHECK` (string; required): Next check that would most reduce uncertainty.

## Output Contract Notes
- OPTION_COMPARISON should compare only the supplied options.
- RECOMMENDATION may be inconclusive when the evidence cannot discriminate strongly enough.
- CHEAPEST_NEXT_CHECK should identify one high-value next signal rather than a backlog.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `why`: Option comparison should separate observed evidence from trade-off judgement and mark uncertainty before recommending a path.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: option-compare.v1

## Neutrality Rules
- Compare the explicit options instead of inventing a preferred hidden third path.
- Separate observed evidence from trade-off interpretation.
- Return inconclusive when the evidence cannot justify a recommendation.

## Execution Constraints
- Do not turn option comparison into implementation planning.
- Keep the comparison proportional to the stated decision question.
- Prefer one discriminating next check over broad speculative follow-up.
- If the evidence surface is long, extract 3-7 anchor facts before comparing options and include at least one anchor from the middle when it matters.
- Before the final recommendation, ask 2-4 verification questions that could overturn the leading option and rescan the evidence against them.
- If the first pass omits a salient entity, constraint, or counter-signal already present in the anchors, rewrite once with higher density instead of adding length.

## Response Format

State the recommendation in one line — or "inconclusive" if evidence cannot discriminate.

Show the trade-off comparison:
- Option | Upside | Downside | Fit for stated constraints

Follow with the cheapest next check if the recommendation is still uncertain.

Didn't check: [anything explicitly out of scope].

Ask: "Does [downside of recommended option] change the decision?"

## Mandatory Rules
- Do not emit `RECOMMENDATION` until the anchor facts and verification pass either support it or force an explicit inconclusive result.
