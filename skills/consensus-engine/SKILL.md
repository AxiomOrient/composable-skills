---
name: consensus-engine
description: "Run a script-backed three-agent consensus pass for one bounded decision, design, debugging, or planning question. Use when Codex, Claude Code, and Gemini CLI should answer independently, challenge only the disagreement surface, and end with evidence-weighted arbitration instead of naive majority vote."
---

# Consensus Engine

## Purpose
Produce one auditable consensus artifact set from Codex, Claude Code, and Gemini CLI without collapsing disagreement into fake certainty.

This is an analysis-only skill. It writes request and result artifacts under `assets/runs/<timestamp>/` and does not edit product files.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,safety-gates,deterministic-output | lens: kahneman-tversky | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kahneman-tversky` because the main job is not "pick the most popular answer" but "separate evidence from confidence, expose collision points, and resist bandwagon bias."

## Use When
- Need one bounded recommendation for architecture, refactoring, debugging, migration, or implementation strategy.
- Need Codex, Claude Code, and Gemini CLI to answer the same mission independently before seeing disagreement only.
- Need a durable artifact set that preserves accepted decisions, provisional lean, unresolved conflicts, and cheapest next checks.
- Need deterministic orchestration through a script because the workflow depends on external CLIs and structured output collection.

## Do Not Use When
- One model is enough.
- The task is deterministic and debate adds no value.
- Required CLIs are unavailable, unauthenticated, or forbidden in the environment.
- The prompt contains secrets or regulated data that must not be sent to external model CLIs.
- The main job is direct implementation rather than analysis.

## Required Inputs
- `MISSION_TASK` (string; required): One bounded decision or analysis question.
- `CONSENSUS_MODE` (analysis|plan|implement-review; optional): Output mode. Defaults to `analysis`.
- `CONSTRAINTS` (list; optional; shape: `{CONSTRAINT}`): Hard limits, non-goals, or compatibility boundaries.
- `DONE_SIGNALS` (list; required; shape: `{DONE_SIGNAL}`): What a valid final recommendation must contain.
- `CONTEXT_FILES` (list; optional; shape: `{PATH}`): Local files to embed as bounded evidence.
- `LOCAL_EVIDENCE` (list; optional; shape: `{FACT}`): Already verified facts that should anchor the run.

## Input Contract Notes
- `MISSION_TASK` must describe one mission, not a bundle of unrelated choices.
- `DONE_SIGNALS` should be externally checkable answer requirements such as "recommend one path and list remaining risks."
- `CONTEXT_FILES` should stay bounded and local; large repositories still need an explicit question surface.
- When information is missing, record open questions instead of guessing.

## Core Workflow
1. Normalize one bounded request packet with task, scope assumptions, constraints, done signals, and local evidence.
2. Run round 1 independently across Codex, Claude Code, and Gemini CLI.
3. Extract atomic `must_keep` and `must_avoid` decisions and cluster the disagreement surface.
4. Build an anonymized disagreement packet that shows only proposal summaries and collision points.
5. Run round 2 rebuttal so each agent can update only if the disagreement evidence changes the view.
6. Apply deterministic arbitration rules:
   - `3 keep / 0 avoid` => accepted keep
   - `0 keep / 3 avoid` => accepted avoid
   - `2 keep / 0 avoid` with stronger evidence => provisional keep
   - `0 keep / 2 avoid` with stronger evidence => provisional avoid
   - any keep/avoid collision => unresolved
7. Write request, round outputs, disagreement packet, final result JSON, and markdown report under `assets/runs/<timestamp>/`.

## Structured Outputs
- `CONSENSUS_VERDICT` (strong-consensus|provisional-consensus|no-consensus; required): Final consensus strength.
- `CONSENSUS_RECOMMENDATION` (string; required): Best current recommendation consistent with the accepted and provisional decisions.
- `UNRESOLVED_CONFLICTS` (list; required; shape: `{DECISION, WHY_UNRESOLVED}`): Critical collisions that were not promoted to consensus.
- `CHEAPEST_NEXT_CHECKS` (list; required): Lowest-cost checks that would reduce remaining uncertainty.
- `ARTIFACT_PATHS` (object; required; shape: `{OUT_DIR, REQUEST_PACKET, RESULT_JSON, REPORT_MD}`): Paths to the materialized artifacts.

## Output Contract Notes
- `CONSENSUS_RECOMMENDATION` must preserve uncertainty instead of flattening it.
- `UNRESOLVED_CONFLICTS` may be empty only when no keep/avoid collision remains.
- `CHEAPEST_NEXT_CHECKS` should be actionable validation steps, not generic "do more research."
- The markdown report must preserve disagreement and evidence quality.

## Commands
Validate the skill package:

```bash
python3 scripts/validate_skill.py --skill-dir .
```

Dry-run the engine without external CLI calls:

```bash
python3 scripts/run_consensus.py \
  --task "Decide the best auth refresh redesign for this repository" \
  --mode analysis \
  --done-signal "Return one recommendation plus unresolved risks" \
  --constraint "Do not edit files" \
  --dry-run
```

Run the full two-round consensus flow:

```bash
python3 scripts/run_consensus.py \
  --task "Compare candidate designs for the auth refresh flow" \
  --mode implement-review \
  --constraint "Preserve the public API" \
  --done-signal "Recommend one path and list cheapest validation checks" \
  --context-file ./notes.txt
```

## Execution Constraints
- Keep the run analysis-only. The engine may write artifacts under its own `assets/` tree but must not patch product files.
- Treat the local `--help` output of each CLI as the adapter source of truth.
- If a preferred flag is missing, fall back to validated stdout parsing instead of inventing a command shape.
- Stop when the mission surface is no longer bounded enough for one request packet.

## Stop Conditions
- Any required CLI command is missing from `PATH`.
- CLI capability probing fails and the adapter cannot determine a safe non-interactive command shape.
- The mission is too vague to produce one bounded request packet.
- Structured output parsing or validation fails after retry.
- The task would require sending forbidden data to external CLIs.
- The final recommendation depends on unsupported claims or unresolved critical collisions.

## References
- `references/MENTAL_MODELS.md`
- `references/CONSENSUS_METHOD.md`
- `references/CLI_COMPATIBILITY.md`
- `assets/request.packet.template.yaml`
- `assets/agent-response.schema.json`
- `assets/consensus-report.template.md`

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

결론부터:
- 합의: [strong / provisional / none]
- 권고안: [한 문단]
- 충돌 남음: [있으면 목록]
- 가장 싼 다음 확인: [목록]

아티팩트 경로를 마지막에 붙인다.

## Mandatory Rules
- 1차 응답에서는 서로의 출력을 보지 않는다.
- 2차에서는 익명 disagreement packet만 공유한다.
- chain-of-thought를 요구하거나 노출하지 않는다.
- unsupported majority를 합의로 승격하지 않는다.
