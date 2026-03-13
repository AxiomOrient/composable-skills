---
name: scout-evidence-gap
description: "Identify what evidence is missing before a claim or decision can be trusted. Use when the main job is to map uncertainty and the cheapest next checks, not to compare options or debug a failure."
---

# Scout / Evidence Gap

## Purpose
Turn a shaky claim into an explicit list of confidence limits and cheapest next checks.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: kahneman-tversky | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kahneman-tversky` because it keeps the work aligned with: Separate observed evidence from inferred risk, expose uncertainty, and resist conclusion-first bias.

## Use When
- Need to know what evidence is still missing before deciding.
- Need to separate current proof from missing proof.
- Need the cheapest next checks rather than a broad investigation plan.

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
- Use CONSTRAINTS to explain why some high-value checks may still be deferred.

## Structured Outputs
- `CURRENT_EVIDENCE` (list; required; shape: {OBSERVATION, LOCATION, EVIDENCE}): Current evidence that does exist.
- `EVIDENCE_GAPS` (list; required; shape: {GAP, WHY_IT_BLOCKS}): Missing proof that limits confidence.
- `CONFIDENCE_LIMITS` (list; required; shape: {LIMIT, WHY}): What cannot be concluded yet and why.
- `NEXT_CHECKS` (list; required; shape: {CHECK, PURPOSE, EXPECTED_SIGNAL}): Cheapest next checks to reduce uncertainty.

## Output Contract Notes
- CURRENT_EVIDENCE should not overstate what the available proof establishes.
- EVIDENCE_GAPS may be empty only when the claim is already adequately supported for the stated scope.
- NEXT_CHECKS should be small, discriminating, and ordered by information value.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `why`: Evidence-gap mapping should mark uncertainty explicitly, separate current proof from missing proof, and point to the cheapest next signal.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: evidence-gap.v1

## Neutrality Rules
- Separate current proof from missing proof.
- Do not invent confidence where the evidence is thin.
- Prefer the cheapest discriminating next check over broad speculative work.

## Execution Constraints
- Do not turn evidence-gap mapping into review verdicts or implementation advice.
- Keep the result bounded to the stated claim and scope.
- Explain why the gap matters instead of listing generic unknowns.
- If the evidence surface is long, extract 3-7 anchor facts first and include at least one anchor from the middle when it matters to the claim.
- Before calling the claim supported or under-supported, ask 2-4 verification questions that force a fresh rescan against the current evidence.
- If the first pass produces generic gaps or limits, rewrite once so the missing entities, signals, or checks become explicit without expanding into a plan.

## Response Format

Think and operate in English, but deliver the final response in Korean.

State the current confidence level for the claim in one line: supported / under-supported / unsupported.

List what exists as evidence: [observation] — [location]

List what is missing: [gap] — why it blocks confidence

Show the next checks ordered by information value:
- [check] — expected signal: [what it would confirm or falsify]

Didn't check: [explicitly out of scope areas]

Ask: "Want to go deeper on [most informative gap]?"

## Mandatory Rules
- Do not treat the claim as adequately supported unless the anchor facts and verification pass both support that conclusion for the stated scope.
