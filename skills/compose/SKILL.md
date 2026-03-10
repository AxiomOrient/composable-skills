---
name: compose
description: "Single entrypoint for deterministic orchestration with Stage x Policy x Lens from explicit macro syntax. English triggers: compose, composition, orchestration, workflow fusion."
---

# Compose

## Purpose
Parse explicit skill macros into one deterministic execution program without adding hidden domain logic.

## Default Program
```text
[orchestration-only]
```

## Use When
- Need to normalize a multi-skill macro into one deterministic execution plan.
- Need workflow expansion from registry-backed workflow skills.
- Need stage, lens, scope, or output overrides resolved before domain execution.

## Do Not Use When
- Need domain analysis, implementation, review, or debugging by itself.
- Need shorthand or non-canonical names instead of explicit workflows or explicit skills.
- Need to infer missing domain skills without an explicit macro or workflow skill.
- Need direct PROGRAM DSL input parsing as a public entry mode.

## Required Inputs
- `MACRO_EXPRESSION` (string; required; shape: $skill + $wf-workflow + @path + [prompt]): Explicit macro text such as $wf-check-full-review + @src/auth + $check-delivered.
- `LENS_OVERRIDE` (string; optional): Optional explicit lens override token.
- `SCOPE_OVERRIDE` (string|list; optional): Optional explicit scope tokens such as @src or scope:paths(src/auth).

## Input Contract Notes
- Public compose entry is macro-only. Direct PROGRAM DSL parsing is internal and not part of the public skill contract.
- Bracket payloads `[ ... ]` are appended to prompt tail in encounter order and are treated as explicit prompt text.
- Scope can come from `@path`, markdown doc tokens, or explicit `scope:...`; compose only normalizes what is explicitly present.

## Structured Outputs
- `INPUT_MODE` (macro; required; allowed: macro): Public input mode used for the current parse.
- `PARSED_SKILLS` (list; required; shape: {EXPLICIT_SKILL}): Explicit skills parsed from the macro before workflow expansion.
- `EFFECTIVE_SKILLS` (list; required; shape: {EXPLICIT_OR_WORKFLOW_SKILL}): Explicit skills after internal response-layer normalization but before workflow flattening.
- `EXPANDED_SKILLS` (list; required; shape: {EXPANDED_SKILL}): Deterministically flattened skill list after workflow expansion.
- `PARSED_DOC_INPUTS` (list; optional; shape: {DOC_OR_PATH}): Document or path tokens parsed from the macro.
- `PROMPT_TAIL` (string; optional): Concatenated explicit prompt payload parsed from free text and bracket blocks.
- `NORMALIZED_SCOPE` (string; required): Resolved scope after macro tokens and skill defaults are merged.
- `LENS_SOURCE` (explicit-override|workflow-default|atomic-default|fallback-default; required; allowed: explicit-override|workflow-default|atomic-default|fallback-default): Where the final lens came from.
- `PROGRAM` (string; required): Normalized execution program.
- `RESPONSE_PROFILE` (object; required): Resolved response profile metadata for the final render.
- `STRUCTURAL_WARNINGS` (list; optional; shape: {WARNING}): Non-blocking orchestration warnings such as duplicate collapse or implicit response-layer append.
- `STRUCTURAL_ERRORS` (list; optional; shape: {ERROR}): Blocking parse or expansion errors returned when macro normalization fails.

## Output Contract Notes
- PROGRAM is the normalized one-line DSL string; the parser may also emit an auxiliary structured program breakdown.
- PARSED_SKILLS preserves the user macro surface, while EFFECTIVE_SKILLS includes internal response-layer normalization and EXPANDED_SKILLS removes workflow names.
- When normalization fails, STRUCTURAL_ERRORS should explain the blocking reason instead of guessing hidden fallback behavior.

## Artifacts
- `artifacts_in`: macro-expression.v1
- `artifacts_out`: compose-program.v2

## Neutrality Rules
- Parse only explicit macro, registry, and override inputs.
- Do not invent domain conclusions, findings, or hidden stage logic during orchestration.
- If a workflow expansion is invalid or cyclic, return the structural error instead of guessing a fallback.

## Execution Constraints
- Do not perform domain analysis, implementation, or verification inside compose.
- Collapse duplicate skills only after workflow expansion and report the collapse as a warning.
- If two or more explicit skills remain in the macro, final response profile resolves to the generic composite profile.

## Mandatory Rules
- Require MACRO_EXPRESSION.
- Prefer canonical wf-* workflow names in new macros.

## Required References
- `../_core/SKILL-FUSION-CONTRACT-v1.2.md`
- `../_core/MICRO-MODULES-v1.md`
- `../_core/RESPONSE-CONTRACT-v1.md`
- `../_core/lenses.json`

## Example Invocation
```text
$compose + $wf-check-full-review + @src/auth + $check-delivered
```

## Output Discipline
- `response_profile=generic`
- User-facing rendering is delegated to `respond`.
