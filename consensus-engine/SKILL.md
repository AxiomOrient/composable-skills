---
name: consensus-engine
description: Use when you need a defensible consensus from Codex, Claude Code, and Gemini CLI for a design, debugging, implementation-plan, or decision packet. It collects independent first-pass answers, runs a disagreement and rebuttal round, and writes a consensus report with accepted decisions, weak majorities, unresolved conflicts, and cheapest next checks. Do not use for one-model quick tasks, fully deterministic computations, or when the required CLIs are unavailable.
---

## Purpose

Produce an evidence-ranked consensus from three heterogeneous CLI agents without collapsing into naive majority vote.

This is an analysis skill. It writes a request packet and consensus artifacts only. It does **not** edit product code or documents unless the user explicitly asks for a separate apply step.

## When To Use

- Need a high-confidence answer for architecture, debugging, refactoring, migration, tool selection, or implementation strategy
- Need Codex, Claude Code, and Gemini CLI to evaluate the same bounded question and then challenge each other
- Need a final output that preserves agreement, disagreement, and evidence gaps instead of flattening everything into one vague summary
- Need an auditable artifact set under `assets/runs/<timestamp>/`

## When Not To Use

- One model is enough
- The task is deterministic and does not benefit from debate
- One or more required CLIs are missing, unauthenticated, or forbidden for the current environment
- The prompt contains secrets or regulated data that must not be sent to external model CLIs
- The user wants direct implementation more than analysis

## Input Contract

Provide one bounded mission.

Minimum required input:

- one concrete task or decision question
- one explicit done condition
- any hard constraints that must not be violated

Preferred input shape:

- `task`: exact decision, design, or debugging question
- `mode`: `analysis`, `plan`, or `implement-review`
- `constraints`: safety, scope, repo, stack, cost, or latency limits
- `done_signals`: what a valid final answer must contain
- `context_files`: optional local notes, logs, specs, or diff summaries
- `local_evidence`: optional facts already verified locally

If context is incomplete, record gaps as open questions. Do not guess.

## Core Workflow

1. Read the current task, repository context, and any supplied files.
2. Restate the mission in one sentence and identify `scope.in`, `scope.out`, constraints, and done signals.
3. Create `assets/runs/<timestamp>/request.packet.yaml`. If anything is unknown, write it under `open_questions` instead of inventing it.
4. Run the orchestration script in analysis mode unless the user explicitly requested another mode.
5. Ensure round 1 is independent. Codex, Claude Code, and Gemini CLI must each answer the same packet **without** seeing peer outputs.
6. Assign the mental models exactly as follows:
   - Codex → `contract-evidence-verifier`
   - Claude Code → `craft-clarity`
   - Gemini CLI → `feynman`
   - Orchestrator → `compose`
7. Ensure each subprocess prompt explicitly forbids hidden delegation loops. Each agent must answer directly in structured JSON and must not invoke this skill again.
8. Build a disagreement matrix from round 1. Normalize atomic decisions into `must_keep` and `must_avoid` clusters.
9. Run the rebuttal round. Share only the anonymized disagreement packet and proposal summaries. Do **not** share private reasoning or chain-of-thought.
10. Apply the deterministic arbitration rules:
    - `3 keep / 0 avoid` → accepted consensus
    - `0 keep / 3 avoid` → accepted avoidance
    - `2 keep / 0 avoid` with stronger evidence than alternatives → provisional consensus
    - `0 keep / 2 avoid` with stronger evidence than alternatives → provisional avoidance
    - any `keep` vs `avoid` collision on the same decision → unresolved conflict
    - unsupported majority or low-evidence agreement → unresolved, not accepted
11. Write all artifacts under `assets/runs/<timestamp>/`.
12. Validate the report against the stop conditions. If proof is missing, stop with explicit gaps rather than pretending consensus exists.

## Commands

Validate the package shape:

```bash
python3 scripts/validate_skill.py
```

Run the consensus engine on one bounded task:

```bash
python3 scripts/run_consensus.py \
  --task "Decide the best design for X in this repository" \
  --mode analysis \
  --constraint "Do not change files" \
  --done-signal "Return one defensible recommendation plus unresolved risks" \
  --context-file ./notes.txt
```

Run with an explicit output directory:

```bash
python3 scripts/run_consensus.py \
  --task "Compare implementation options for the auth refresh flow" \
  --mode implement-review \
  --constraint "Preserve current public API" \
  --done-signal "Recommend one path and list cheapest validation checks" \
  --out-dir assets/runs/auth-refresh-consensus
```

Show script options:

```bash
python3 scripts/run_consensus.py --help
```

## Output Contract

Write paths:

- `assets/runs/<timestamp>/request.packet.yaml`
- `assets/runs/<timestamp>/codex.round1.json`
- `assets/runs/<timestamp>/claude.round1.json`
- `assets/runs/<timestamp>/gemini.round1.json`
- `assets/runs/<timestamp>/disagreement.packet.json`
- `assets/runs/<timestamp>/codex.round2.json` when `--rounds 2`
- `assets/runs/<timestamp>/claude.round2.json` when `--rounds 2`
- `assets/runs/<timestamp>/gemini.round2.json` when `--rounds 2`
- `assets/runs/<timestamp>/consensus.result.json`
- `assets/runs/<timestamp>/consensus.report.md`

`consensus.result.json` must contain at least:

- `verdict`
- `consensus_recommendation`
- `accepted_keep`
- `accepted_avoid`
- `provisional_keep`
- `provisional_avoid`
- `unresolved`
- `cheapest_next_checks`
- `agent_status`

`consensus.report.md` must preserve disagreement. Never hide unresolved items.

## Stop Conditions

Stop immediately if any of the following is true:

- `codex`, `claude`, or `gemini` CLI is missing from `PATH`
- any required CLI run fails or returns invalid structured output after retry
- the task is too vague to produce a bounded request packet
- the prompt includes data that must not be sent to external CLIs
- the requested permissions exceed the current safety mode
- the final recommendation would rely on unsupported claims, hidden assumptions, or fabricated evidence
- the rebuttal round still leaves a critical decision unresolved with no grounded way to break the tie

When stopping, write the partial artifacts and state exactly what is missing.

## References

- `references/MENTAL_MODELS.md`
- `references/CONSENSUS_METHOD.md`
- `references/CLI_COMPATIBILITY.md`
- `assets/request.packet.template.yaml`
- `assets/agent-response.schema.json`
- `assets/consensus-report.template.md`
