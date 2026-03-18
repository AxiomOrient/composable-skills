# Doc scope checklist

Check these sources in order when relevant:

1. Root instructions: `AGENTS.md`, `WORKFLOW.md`, `ARCHITECTURE.md`, `PRODUCT_SENSE.md`.
2. Structured docs: `docs/`, especially specs, design docs, plans, and generated references.
3. Runtime/config surface: CLI flags, env vars, config files, build scripts, example commands.
4. Current change boundary: changed files, plan artifacts, migration notes, release notes.

Minimal rules:
- Compare user-visible behavior first.
- Compare operator-facing commands and configuration second.
- Prefer the smallest patch that restores truth.
