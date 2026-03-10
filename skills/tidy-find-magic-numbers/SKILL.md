---
name: tidy-find-magic-numbers
description: "Find repeated literals, configuration-like values, and policy constants that should be centralized into constants, config, or shared definitions. Use when a bounded module, folder, or repo needs explicit constant/common extraction analysis."
---

# Tidy / Find Magic Numbers

## Purpose
Identify exact literal values and policy constants that can be centralized without changing behavior.

## Default Program
```text
[stages: preflight>detect>analyze>review>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Use When
- Need to find extractable constants in a module, folder, or repo.
- Need to reduce repeated literals and policy drift.
- Need evidence-backed commonization candidates before refactoring.

## Do Not Use When
- Need a general bug review.
- Need to implement the refactor immediately without first identifying candidates.
- The target contains no meaningful repeated literals or config-like values.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Where to scan for extractable constants.
- `EXTRACTION_POLICY` (constants|config|shared-definition; required): Preferred extraction destination style.

## Structured Outputs
- `EXTRACTABLE_CONSTANTS` (list; required): Concrete literal values or policy constants that should be extracted.
- `REUSE_OPPORTUNITIES` (list; required): Places where the same value or policy recurs.
- `EXTRACTION_BLOCKERS` (list; required): Reasons some values should remain local.

## Procedure
1. Scan the target for repeated literals, thresholds, enum-like strings, and policy values.
2. Group candidates by semantic role rather than raw textual equality alone.
3. Recommend the narrowest centralization target for each candidate.
4. List blockers for candidates that should stay local.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Constant extraction should prefer explicit reusable data over repeated magic literals.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: constant-extraction-report.v1

## Neutrality Rules
- Recommend extraction only when reuse or policy consistency is evidenced.
- Do not force extraction for values that are local and semantically unique.
- Separate extraction candidates from blockers and uncertainty.

## Mandatory Rules
- Name the exact literal or value family being recommended.
- Include evidence locations for each extraction recommendation.

## Example Invocation
```text
$tidy-find-magic-numbers
TARGET_SCOPE: src/auth
EXTRACTION_POLICY: constants
```
