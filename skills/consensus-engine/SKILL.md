---
name: consensus-engine
description: "Run a script-backed three-agent consensus pass for one bounded decision or one explicit compose execution contract. Use when Codex, Claude Code, and Gemini CLI should work independently, challenge only the disagreement surface, and converge on the strongest recommendation or work product instead of naive majority vote."
---

# Consensus Engine

## Purpose
Produce one auditable consensus artifact set from Codex, Claude Code, and Gemini CLI without collapsing disagreement into fake certainty.

The default job is not "analysis only." The engine can either:
- arbitrate one bounded decision, or
- run one shared `compose` execution contract in parallel and converge on the strongest work product.

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
- Need one explicit `compose` macro executed in parallel for docs, implementation proposals, PRD drafts, or research reports.

## Do Not Use When
- One model is enough.
- The task is deterministic and debate adds no value.
- Required CLIs are unavailable, unauthenticated, or forbidden in the environment.
- The prompt contains secrets or regulated data that must not be sent to external model CLIs.
- The main job is direct shared-workspace mutation instead of parallel draft/proposal convergence.

## Required Inputs
- `MISSION_TASK` (string; required): One bounded decision or analysis question.
- `CONSENSUS_MODE` (execute|analysis|plan|implement-review; optional): Output mode. Defaults to `execute`.
- `CONSTRAINTS` (list; optional; shape: `{CONSTRAINT}`): Hard limits, non-goals, or compatibility boundaries.
- `DONE_SIGNALS` (list; required; shape: `{DONE_SIGNAL}`): What a valid final recommendation must contain.
- `CONTEXT_FILES` (list; optional; shape: `{PATH}`): Local files to embed as bounded evidence.
- `LOCAL_EVIDENCE` (list; optional; shape: `{FACT}`): Already verified facts that should anchor the run.
- `MACRO_EXPRESSION` (string; optional): Explicit `compose` macro that defines the shared execution contract for all three agents.

## Input Contract Notes
- `MISSION_TASK` must describe one mission, not a bundle of unrelated choices.
- `DONE_SIGNALS` should be externally checkable answer requirements such as "recommend one path and list remaining risks."
- `CONTEXT_FILES` should stay bounded and local; large repositories still need an explicit question surface.
- When `MACRO_EXPRESSION` is present, the engine first normalizes it through the local compose parser and shares the same program and response profile with every agent.
- If the compose contract still has missing required inputs after normalization, stop instead of letting providers guess.
- When information is missing, record open questions instead of guessing.

## Core Workflow
1. Normalize one bounded request packet with task, scope assumptions, constraints, done signals, and local evidence.
2. If `MACRO_EXPRESSION` is present, parse it into one shared `compose` execution contract before any provider runs.
3. If the shared compose contract still reports missing required inputs, stop and emit blockers instead of running providers.
4. Run round 1 independently across Codex, Claude Code, and Gemini CLI.
5. Normalize decisions as positive action phrases so polarity stays in `must_keep` / `must_avoid`, then cluster the disagreement surface.
6. Build an anonymized disagreement packet that shows only proposal summaries, work summaries, and collision points.
7. Run round 2 rebuttal only when disagreement or divergent work products justify it.
8. Apply deterministic arbitration rules:
   - `3 keep / 0 avoid` => accepted keep
   - `0 keep / 3 avoid` => accepted avoid
   - `2 keep / 0 avoid` with stronger evidence => provisional keep
   - `0 keep / 2 avoid` with stronger evidence => provisional avoid
   - any keep/avoid collision => unresolved
   - aligned votes without enough concrete anchors => needs-more-evidence
9. Select the strongest work product only when the run reaches at least provisional consensus and the chosen draft satisfies the compose response profile.
10. Write request, round outputs, disagreement packet, selected work product, final result JSON, and markdown report under `assets/runs/<timestamp>/`.

## Structured Outputs
- `CONSENSUS_VERDICT` (strong-consensus|provisional-consensus|no-consensus; required): Final consensus strength.
- `CONSENSUS_RECOMMENDATION` (string; required): Best current recommendation consistent with the accepted and provisional decisions.
- `SELECTED_WORK_PRODUCT` (object|null; required): The highest-fit provider work product chosen after arbitration, or `null` when selection is withheld.
- `UNRESOLVED_CONFLICTS` (list; required; shape: `{DECISION, WHY_UNRESOLVED}`): Critical collisions that were not promoted to consensus.
- `NEEDS_MORE_EVIDENCE` (list; required; shape: `{DECISION, MISSING_ANCHOR}`): Aligned directions that still fail the evidence floor.
- `CHEAPEST_NEXT_CHECKS` (list; required): Lowest-cost checks that would reduce remaining uncertainty.
- `ARTIFACT_PATHS` (object; required; shape: `{OUT_DIR, REQUEST_PACKET, RESULT_JSON, REPORT_MD}`): Paths to the materialized artifacts.

## Output Contract Notes
- `CONSENSUS_RECOMMENDATION` must preserve uncertainty instead of flattening it.
- `SELECTED_WORK_PRODUCT` should point to one concrete deliverable candidate when the run is execution-oriented, and stay `null` when consensus is too weak or required sections are missing.
- `UNRESOLVED_CONFLICTS` may be empty only when no keep/avoid collision remains.
- `NEEDS_MORE_EVIDENCE` should capture weak majorities that still lack concrete anchors.
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
  --mode execute \
  --done-signal "Return one recommendation plus unresolved risks" \
  --constraint "Do not edit files" \
  --dry-run
```

Run a composed execution contract:

```bash
python3 scripts/run_consensus.py \
  --task "Produce the best bounded implementation proposal for auth refresh" \
  --mode execute \
  --macro-expression '$workflow-build-implement-and-guard + @src/auth + [GOAL: keep the session after refresh] + [DONE: session refresh test => stay signed in after refresh] + [CONTEXT: keep the session after refresh during an active login] + [CONSTRAINTS: keep public API stable]' \
  --done-signal "Return one selected work product and remaining conflicts"
```

Run the full consensus flow without compose:

```bash
python3 scripts/run_consensus.py \
  --task "Compare candidate designs for the auth refresh flow" \
  --mode implement-review \
  --constraint "Preserve the public API" \
  --done-signal "Recommend one path and list cheapest validation checks" \
  --context-file ./notes.txt
```

## Execution Constraints
- The engine may write artifacts under its own `assets/` tree but must not patch shared product files directly.
- Treat the local `--help` output of each CLI as the adapter source of truth.
- If a preferred flag is missing, fall back to validated stdout parsing instead of inventing a command shape.
- When running a compose contract, require every provider to return the concrete deliverable in `work_output` rather than only a review of the task.
- When the compose response profile lists required sections, withhold selection if no candidate draft covers all of them.
- Stop when the mission surface is no longer bounded enough for one request packet.

## Stop Conditions
- Any required CLI command is missing from `PATH`.
- CLI capability probing fails and the adapter cannot determine a safe non-interactive command shape.
- The mission is too vague to produce one bounded request packet.
- Structured output parsing or validation fails after retry.
- The compose contract still has unresolved required inputs after normalization.
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
- 선택된 산출물: [요약]
- 충돌 남음: [있으면 목록]
- 가장 싼 다음 확인: [목록]

아티팩트 경로를 마지막에 붙인다.

## Mandatory Rules
- 1차 응답에서는 서로의 출력을 보지 않는다.
- 2차에서는 익명 disagreement packet만 공유한다.
- chain-of-thought를 요구하거나 노출하지 않는다.
- unsupported majority를 합의로 승격하지 않는다.
- compose가 있으면 세 에이전트 모두 같은 실행 계약을 공유해야 한다.
- decision 문장은 긍정 행동형으로 정규화하고, keep/avoid는 필드 극성으로만 표현한다.
