# consensus-engine

A portable Codex skill package for three-way consensus across:

- Codex CLI
- Claude Code CLI
- Gemini CLI

## What It Does

1. builds one bounded request packet
2. runs an **independent** first round across the three CLIs
3. extracts `must_keep` / `must_avoid` decisions
4. builds an anonymized disagreement packet
5. runs a rebuttal round
6. writes a deterministic consensus result and markdown report

## Install

### Current Codex

Copy this folder to either:

- `.agents/skills/consensus-engine`
- `~/.agents/skills/consensus-engine`

### Legacy / AxiomMd style

Copy this folder to:

- `.codex/skills/consensus-engine`

## Validate

```bash
python3 scripts/validate_skill.py
```

## Run

```bash
python3 scripts/run_consensus.py \
  --task "Decide the best auth refresh design for this repository" \
  --mode analysis \
  --constraint "Do not edit files" \
  --done-signal "Return one recommendation plus open risks" \
  --context-file ./notes.txt
```

Outputs are written under `assets/runs/<timestamp>/` unless `--out-dir` is set.
