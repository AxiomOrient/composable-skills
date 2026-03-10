---
name: respond
description: "Final-output only skill. Render the final user-facing response in plain, short, easy, concrete language using skill-specific response profiles. Do not analyze, plan, implement, or review here."
---

# Respond

## Purpose
Render one final user-facing response from upstream stage payloads and the resolved response profile using simple, concrete language that a beginner can follow.

## Default Program
```text
[stages: handoff |
 scope: diff |
 policy: evidence,deterministic-output,response-contract{plain-korean,feynman-clear,actionable,core-first,short-sentences,plain-words,concrete-details} |
 output: md(contract=v1)]
```

## Use When
- Need the final user-facing response rendered from completed upstream work.
- Need standalone or composed response sections selected from the resolved response profile.
- Need one deterministic exit point after multi-skill execution.

## Do Not Use When
- Need new analysis, implementation, debugging, or review work.
- Need to create findings that upstream stages did not establish.
- Need to infer missing sections from unstated evidence.

## Required Inputs
- `RESPONSE_PROFILE` (response-profile.v1; required): Resolved response profile with primary skill, profile id, and required sections.
- `STAGE_PAYLOADS` (list(stage-payload.v1); required): Finalized upstream payloads accumulated before rendering. Use only established facts from these payloads.
- `LANGUAGE_PREFERENCE` (ko|match-user|en; optional): Optional output language. Default is `ko`.

## Structured Outputs
- `FINAL_RESPONSE` (markdown.v1; required): Single final response rendered for the user in plain, short, concrete language.
- `RENDERED_SECTIONS` (list; required): Sections actually rendered from the response profile.

## Artifacts
- `artifacts_in`: stage-payloads.v1, response-profile.v1
- `artifacts_out`: final-response.v1

## Neutrality Rules
- Render only what upstream stages established.
- Do not add new findings, verdicts, or recommendations during rendering.
- If required support is missing, omit the unsupported claim instead of fabricating content.

## Mandatory Rules
- Start with the answer, not the process.
- Explain technical terms in plain words the first time they appear.
- Prefer short sentences and common words over internal jargon.
- Prefer file names, line numbers, function names, and measurements over abstract labels.
- Prefer a short paragraph that explains meaning and next action over a taxonomy of labels.
- If there is no finding or evidence is incomplete, say that plainly.
