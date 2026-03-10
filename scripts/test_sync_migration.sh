#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_ROOT="$(mktemp -d)"
TARGET_ROOT="$TMP_ROOT/codex-home"

cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT

# Legacy fixture: keep one removed workflow name here so sync pruning stays covered.
mkdir -p "$TARGET_ROOT/skills/wf-question-repair" "$TARGET_ROOT/docs"
cat > "$TARGET_ROOT/.codex-skills-manifest.txt" <<'EOF'
scout-facts
wf-question-repair
EOF

printf 'legacy-skill\n' > "$TARGET_ROOT/skills/wf-question-repair/marker.txt"

"$REPO_ROOT/scripts/sync.sh" "$TARGET_ROOT" >/dev/null

if [[ -d "$TARGET_ROOT/skills/wf-question-repair" ]]; then
  echo "expected removed legacy skill directory to be pruned" >&2
  exit 1
fi

if [[ ! -f "$TARGET_ROOT/.composable-skill-packs-manifest.txt" ]]; then
  echo "expected new manifest file to be written" >&2
  exit 1
fi

if [[ -f "$TARGET_ROOT/.codex-skills-manifest.txt" ]]; then
  echo "expected legacy manifest file to be removed after migration" >&2
  exit 1
fi

if grep -Fxq "wf-question-repair" "$TARGET_ROOT/.composable-skill-packs-manifest.txt"; then
  echo "expected removed skill to stay out of migrated manifest" >&2
  exit 1
fi

if [[ ! -d "$TARGET_ROOT/skills/scout-facts" ]]; then
  echo "expected current skills to be installed during sync" >&2
  exit 1
fi

if [[ ! -f "$TARGET_ROOT/docs/AGENT-SKILL-GUIDE.md" ]]; then
  echo "expected docs sync to include AGENT-SKILL-GUIDE.md" >&2
  exit 1
fi

echo "sync migration test passed"
