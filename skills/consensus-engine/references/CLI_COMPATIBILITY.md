# CLI Compatibility

## Runtime Surface

Within this repository, the runtime source of truth is:

- `skills/consensus-engine` - internal script-backed engine
- `skills/workflow-consensus-engine` - public entrypoint that first locks boundaries

Sync installs into `.agents/skills/` through `./scripts/sync.sh`.

## Adapter Discovery Rule

The orchestrator does not hard-code undocumented flags blindly.

Before running any model CLI, it probes:

- `codex exec --help`
- `claude --help`
- `gemini --help`

The command adapter then enables only the flags confirmed by the local binary.

## Expected CLI Commands

### Codex

Observed locally on 2026-03-18:

Pattern:

```bash
codex exec --sandbox read-only --ask-for-approval never \
  --output-schema assets/agent-response.schema.json \
  --output-last-message /tmp/codex.json \
  "<prompt>"
```

### Claude Code

Observed locally on 2026-03-18:

Pattern:

```bash
claude -p "<prompt>" \
  --disable-slash-commands \
  --no-session-persistence \
  --permission-mode plan \
  --output-format json \
  --json-schema '<schema-json>'
```

### Gemini CLI

Observed locally on 2026-03-18:

Pattern:

```bash
gemini -p "<prompt>" \
  --output-format json \
  --approval-mode plan
```

## Required Runtime Conditions

- all three CLIs must be installed and authenticated
- the task must be safe to send to external model CLIs
- read-only / plan-style operation is the default
- this skill does not assume any MCP dependency
- if a preferred flag is unavailable, the adapter must fall back to a validated parse-from-stdout path instead of guessing
