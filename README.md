# Composable Skills

Portable Codex skill repository with one direct source model:

- human contract: `skills/<name>/SKILL.md`
- machine contract: `skills/<name>/skill.json`
- shared metadata: `skills/_meta/*.json`

The repo keeps only the direct runtime skill surface and the minimal install/sync tooling needed to use it.

## Requirements

- `bash`
- `python3`

## What This Repo Contains

- `skills/`: runtime skill surface
- `skills/_meta/`: shared machine-readable metadata
- `scripts/sync.sh`: update an existing `.agents` install
- `scripts/skills.py`: minimal CLI for direct metadata validation and sync

Internal `.system` skills are not part of the public release package.

## Sync

```bash
git clone git@github.com:AxiomOrient/composable-skills.git
cd composable-skills
./scripts/sync.sh
```

For project-local install:

```bash
./scripts/sync.sh local
```

If the target ends with `/skills`, the scripts normalize it back to the `.agents` root automatically.

## Runtime Model

- Public entry surface: `workflow-*`
- Expert building blocks: atomic skills
- Internal control surface: `compose`, `respond`, `plan-sync-tasks`, `build-until-done`, `finish-until-done`, `release-publish`

The runtime reads direct skill metadata from skill folders.
It does not require `_registry`, `_core`, generated guides, a committed `catalog.json`, or a separate docs package.

## Start Here

- Runtime guide: [`skills/README.md`](./skills/README.md)

## Release Rules

- Public entry skills use `workflow-*` only.
- `compose` stays an internal control engine, not a default discovery target.
- Every shipped skill keeps explicit inputs, outputs, neutrality rules, and response profile.
- Temporary implementation docs such as `plans/IMPLEMENTATION-PLAN.md` and `plans/TASKS.md` do not ship in release commits.
