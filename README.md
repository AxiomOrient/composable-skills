# Composable Skill Packs

Portable release repository for composable Codex and Claude Code skill packs.

Version: `1.0.0`

## Requirements

- `bash`
- `python3`
- `rsync`

## What This Repo Contains

- `skills/`: runtime skill surface
- `skills/packs/README.md`: category/domain pack index
- `docs/SKILL-SYSTEM.md`: architecture and admission guide
- `docs/SKILL-STATE-REPORT.md`: generated skill inventory
- `scripts/install.sh`: install into a Codex or Claude Code home
- `scripts/sync.sh`: update an existing install
- `scripts/validate.sh`: run release validation

This repo ships the public skill surface only.
Internal `.system` skills are not part of this release package.

## Install

Clone the repo, then install into your runtime home.

```bash
git clone git@github.com:AxiomOrient/composable-skill-packs.git
cd composable-skill-packs
./scripts/install.sh codex ~/.codex
./scripts/install.sh claude ~/.claude
```

Restart the target runtime after installation.

### Claude Code

Claude Code installs the public skill surface into `~/.claude/skills` and syncs supporting docs into `~/.claude/docs`.

```bash
./scripts/install.sh claude ~/.claude
```

To update an existing Claude Code install:

```bash
./scripts/sync.sh claude ~/.claude
```

Usage:

- Local combo guide: [`skills/SKILL-COMBOS.md`](./skills/SKILL-COMBOS.md)
- Local atomic reference: [`skills/ATOMIC-SKILLS.md`](./skills/ATOMIC-SKILLS.md)
- Pack index: [`skills/packs/README.md`](./skills/packs/README.md)
- Official Claude Code skills and slash commands: [code.claude.com/docs/en/slash-commands](https://code.claude.com/docs/en/slash-commands)
- Official Claude Code subagents: [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

## Update

```bash
git pull --ff-only
./scripts/sync.sh codex ~/.codex
./scripts/sync.sh claude ~/.claude
```

## Validate

```bash
./scripts/validate.sh
```

`validate.sh` regenerates the state report before running registry, parser, sync, and scenario checks.

## Structure

- Runtime discovery source: [`skills/_registry/index.json`](./skills/_registry/index.json)
- User guide: [`skills/README.md`](./skills/README.md)
- Beginner combos: [`skills/SKILL-COMBOS.md`](./skills/SKILL-COMBOS.md)
- Pack index: [`skills/packs/README.md`](./skills/packs/README.md)
- System rules: [`docs/SKILL-SYSTEM.md`](./docs/SKILL-SYSTEM.md)

## Release Rules

- Public workflows use `wf-*` only.
- `compose` is the engine.
- Packs are catalog/install units, not runtime execution nodes.
- Every public skill must keep explicit inputs, outputs, neutrality rules, and response profile.
