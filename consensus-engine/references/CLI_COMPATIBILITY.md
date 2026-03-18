# CLI Compatibility

## Skill Installation Paths

This package is path-portable.

Use the same `consensus-engine/` folder in one of these locations depending on your runtime:

- current Codex installs: `.agents/skills/consensus-engine` or `~/.agents/skills/consensus-engine`
- legacy AxiomMd-style installs: `.codex/skills/consensus-engine`

The internal file layout stays the same.

## Expected CLI Commands

### Codex

The orchestrator uses non-interactive Codex with schema-constrained output.

Pattern:

```bash
codex exec --sandbox read-only --ask-for-approval never \
  --output-schema assets/agent-response.schema.json \
  --output-last-message /tmp/codex.json \
  "<prompt>"
```

### Claude Code

The orchestrator uses print mode with JSON schema output.

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

The orchestrator uses headless JSON output and local validation.

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
