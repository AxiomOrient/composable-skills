#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_ROOT="$(mktemp -d)"
TARGET_ROOT="$TMP_ROOT/claude-home"

cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT

# Legacy fixture: keep one removed workflow name here so Claude sync pruning stays covered.
mkdir -p "$TARGET_ROOT/skills/wf-question-repair"
cat > "$TARGET_ROOT/.composable-skill-packs-claude-manifest.txt" <<'EOF'
scout-facts
ask-fix-prompt
wf-question-repair
EOF

printf 'legacy-skill\n' > "$TARGET_ROOT/skills/wf-question-repair/marker.txt"

"$REPO_ROOT/scripts/sync.sh" claude "$TARGET_ROOT" >/dev/null

if [[ -d "$TARGET_ROOT/skills/wf-question-repair" ]]; then
  echo "expected removed legacy Claude skill directory to be pruned" >&2
  exit 1
fi

if [[ ! -f "$TARGET_ROOT/.composable-skill-packs-claude-manifest.txt" ]]; then
  echo "expected Claude manifest file to be written" >&2
  exit 1
fi

if [[ ! -f "$TARGET_ROOT/skills/scout-facts/SKILL.md" ]]; then
  echo "expected scout-facts skill to be installed for Claude" >&2
  exit 1
fi

if [[ ! -f "$TARGET_ROOT/skills/README.md" ]]; then
  echo "expected shared skill README to be synced for Claude" >&2
  exit 1
fi

if [[ ! -f "$TARGET_ROOT/skills/packs/README.md" ]]; then
  echo "expected pack index docs to be synced for Claude" >&2
  exit 1
fi

if [[ ! -f "$TARGET_ROOT/docs/SKILL-SYSTEM.md" ]]; then
  echo "expected docs to be synced for Claude" >&2
  exit 1
fi

if [[ -d "$TARGET_ROOT/skills/scout-facts/agents" ]]; then
  echo "expected Codex-only agents metadata to stay out of Claude sync" >&2
  exit 1
fi

if [[ ! -f "$TARGET_ROOT/skills/ask-fix-prompt/references/repair-playbook.md" ]]; then
  echo "expected shared references to be preserved for Claude" >&2
  exit 1
fi

echo "claude sync test passed"
