# Verification command discovery order

Use repository-owned command definitions in this order:

1. `AGENTS.md`, `WORKFLOW.md`, or equivalent repo instructions.
2. Root scripts such as `scripts/verify.sh`, `scripts/run-tests.sh`, or `make verify`.
3. Package manager scripts (`package.json`, `pyproject.toml`, `justfile`, `Makefile`, `Taskfile.yml`).
4. CI workflows (`.github/workflows/*.yml`) only to confirm the canonical order, not to replace local entrypoints.

Discovery rules:
- Prefer one canonical entrypoint if the repo already has one.
- Prefer the smallest command that still covers the changed surface.
- If a required command depends on unavailable tooling, mark the result `blocked` instead of silently skipping it.
