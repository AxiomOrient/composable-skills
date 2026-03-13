---
name: gemini
description: "Use when the user explicitly requests Gemini CLI as a sub-agent for large-context analysis or web research, including session resume. Do not run Gemini implicitly. English triggers: gemini, gemini cli, external research delegation."
---

# Gemini

## Purpose
Run an explicitly requested Gemini CLI delegation and keep its output separated from local evidence.

## Default Program
```text
[stages: preflight>detect>analyze>verify>review>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,safety-gates,deterministic-output |
 lens: feynman |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `feynman` because it keeps the work aligned with: Reproduce first, use disprovable hypotheses, and explain the result plainly.

## Use When
- The user explicitly invokes gemini or $gemini.
- Need large-context external analysis, web research, or session resume through Gemini CLI.
- Need Gemini output compared against local evidence instead of replacing it.

## Do Not Use When
- Gemini was not explicitly requested.
- Need ordinary local repository analysis that can be completed without external delegation.
- Need automatic file edits unless the user explicitly requested apply mode.

## Required Inputs
- `GEMINI_MODE` (new|resume|apply; required): Execution mode for Gemini CLI.
- `GEMINI_GOAL` (string; required): Exact analysis or verification goal for Gemini.
- `TARGET_SCOPE` (file|module|folder|repo; required): Bounded target scope for Gemini.
- `SESSION_ID` (string; optional): Explicit Gemini session id for resume mode.

## Input Contract Notes
- Prefer `GEMINI_MODE=new` when the job is a fresh analysis; use `resume` only when the prior Gemini session context is part of the task.
- `SESSION_ID` should be supplied for `resume` runs and omitted for fresh runs unless the user explicitly wants a specific session reused.
- Use `apply` only when the user explicitly wants Gemini to propose or make concrete changes rather than analysis-only delegation.

## Structured Outputs
- `GEMINI_FINDINGS` (list; required): Summarized Gemini claims or findings.
- `LOCAL_COMPARISON` (list; required): Local evidence comparison against Gemini output.
- `CONFLICTS` (list; required): Explicit conflicts between Gemini and local evidence.
- `EVIDENCE_GAPS` (list; required; shape: {STEP_OR_CLAIM, GAP, CHEAPEST_NEXT_CHECK}): Claims or side effects that were not executed or could not be proven in the current run.

## Output Contract Notes
- `GEMINI_FINDINGS` should summarize Gemini output as reported, not silently merge it into the local conclusion.
- `LOCAL_COMPARISON` should state where local evidence agrees, disagrees, or remains insufficient.
- `CONFLICTS` may be empty when Gemini and local evidence align; do not invent disagreement just to fill the section.
- `EVIDENCE_GAPS` should make non-executed external steps explicit instead of implying live evidence.

## Artifacts
- `artifacts_in`: gemini-request.v1
- `artifacts_out`: external-verification-report.v1

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Show Gemini's output directly, attributed: "Gemini says: [finding or claim]"

Then compare against local evidence: "Local evidence: [agrees / disagrees / insufficient]"

List conflicts explicitly: "Gemini vs local: [what they disagree on]"

Flag confidence: "Gemini confidence is low on [claim] — local evidence does not confirm."

## Neutrality Rules
- Report Gemini output and local analysis separately.
- Do not promote Gemini claims above local evidence without comparison.
- If Gemini and local evidence conflict, surface the conflict explicitly.
- If Gemini execution or comparison evidence is missing, report the gap instead of implying completion.

## Example Invocation
```text
$compose + $gemini + $check-final-verify

GEMINI_MODE: new
GEMINI_GOAL: Compare the current auth token refresh flow against official provider docs.
TARGET_SCOPE: src/auth
```
