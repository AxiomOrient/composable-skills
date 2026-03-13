---
name: ask-fix-prompt
description: "Diagnose why an answer was wrong, shallow, or structurally weak, then produce the minimum prompt repair. Use only after a failed answer, not for first-pass question design, repository work, or coding."
---

# Ask / Fix Prompt

## Purpose
Turn a failed answer into a controlled repair loop that explains the failure and proposes the smallest useful question change.

## Default Program
```text
[stages: preflight>detect>analyze>review>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: feynman | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `feynman` because it keeps the work aligned with: Reproduce first, use disprovable hypotheses, and explain the result plainly.

## Use When
- Already received a weak, wrong, or structurally off-target answer.
- Need to explain what was missing before retrying.
- Need the minimum question or prompt delta instead of a full redesign.

## Do Not Use When
- Have not yet asked the original question.
- Need code editing, repository analysis, or implementation.
- Need a first-pass question design rather than repair.

## Required Inputs
- `TOPIC` (string; required): Original topic.
- `QUESTION_OR_STACK` (string|question-stack.v1; required): Original question or question stack.
- `BAD_ANSWER` (string; required): Answer that failed.

## Input Contract Notes
- BAD_ANSWER should contain the actual failed answer, not only a complaint about it.
- QUESTION_OR_STACK should preserve the original ask so the repair can stay minimal.
- This skill is already fixed to repair-after-failure; do not overload it with broader redesign intent.

## Structured Outputs
- `FAILURE_CLASS` (scope-miss|evidence-gap|format-mismatch|reasoning-gap|inconclusive; required; allowed: scope-miss|evidence-gap|format-mismatch|reasoning-gap|inconclusive): Failure class from the repair playbook.
- `WHY_WRONG` (string; required): Why the answer failed.
- `WHAT_WAS_MISSING` (list; required; shape: {MISSING, WHY_IT_MATTERS}): Missing terms, disagreements, evidence, or output constraints.
- `MINIMAL_QUESTION_DELTA` (list; required; shape: {CHANGE, WHY}): Smallest question-level changes likely to fix the failure.
- `REPAIRED_PROMPT` (string; required): Repaired prompt or repaired question stack.
- `RE_RUN_RECOMMENDATION` (string; required): Whether to re-run ask, map, or broader question redesign.

## Output Contract Notes
- Use FAILURE_CLASS=inconclusive when the supplied BAD_ANSWER does not provide enough evidence to diagnose a specific failure mode.
- MINIMAL_QUESTION_DELTA may be an empty list when the original question is still sound and the failure came from answer execution rather than prompt shape.
- REPAIRED_PROMPT should preserve useful parts of the original question instead of rewriting everything by default.

## Procedure
1. Classify the failure using the repair playbook.
2. State why the answer failed and what was missing.
3. Produce the minimum question change likely to fix the failure.
4. Emit a repaired prompt only if a minimal delta is insufficient by itself.
5. Recommend the narrowest upstream step that should be re-run.

## Primary Lens
- `primary_lens`: `feynman`
- `why`: Repair by explaining plainly why the answer failed and what minimum corrective question delta is needed.

## Artifacts
- `artifacts_in`: question-stack.v1
- `artifacts_out`: repair-playbook.v2

## Neutrality Rules
- Explain the failure before proposing a fix.
- Prefer the smallest prompt delta that addresses the failure.
- Preserve useful parts of the original question instead of redesigning by default.
- If the failure evidence is weak, say inconclusive instead of inventing missing requirements.

## Execution Constraints
- Do not escalate to a broader redesign unless the failure is clearly structural.
- Keep the repair delta narrowly tied to the observed failure mode.
- Do not smuggle a new preferred answer into the repaired prompt.

## Response Format

Lead with the failure class and one sentence on why the answer failed.

Then show the minimal repair:
- What was missing
- The smallest question change that would fix it
- The repaired prompt (only if a delta alone is insufficient)

Close with: "Re-run with the repaired prompt, or is the failure class wrong?"

## Mandatory Rules
- Always explain why the answer failed before proposing a fix.
- Keep the repair delta as small as possible.
- Re-run broader question design only when the failure is structural.

## Required References
- `references/repair-playbook.md`
- `references/question-quality-rubric.md`

## Example Invocation
```text
$ask-fix-prompt
TOPIC: RAG vs long context
QUESTION_OR_STACK: <previous prompt>
BAD_ANSWER: <model answer>
```
