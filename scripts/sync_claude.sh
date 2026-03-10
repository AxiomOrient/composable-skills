#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_ROOT="${1:-$HOME/.claude}"
SKILLS_SRC="$REPO_ROOT/skills"
DOCS_SRC="$REPO_ROOT/docs"
SKILLS_DEST="$TARGET_ROOT/skills"
DOCS_DEST="$TARGET_ROOT/docs"
MANIFEST_PATH="$TARGET_ROOT/.composable-skill-packs-claude-manifest.txt"
TMP_MANIFEST="$(mktemp)"

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

need_cmd python3
need_cmd rsync

mkdir -p "$SKILLS_DEST" "$DOCS_DEST"

python3 - "$SKILLS_SRC/_registry/index.json" > "$TMP_MANIFEST" <<'PY'
import json
import sys
from pathlib import Path

index = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
for group in ("atomic", "utility", "workflow"):
    for name in index[group]:
        print(name)
PY

if [[ -f "$MANIFEST_PATH" ]]; then
  while IFS= read -r old_skill; do
    [[ -z "$old_skill" ]] && continue
    if ! grep -Fxq "$old_skill" "$TMP_MANIFEST"; then
      rm -rf "$SKILLS_DEST/$old_skill"
    fi
  done < "$MANIFEST_PATH"
fi

rsync -a --delete "$SKILLS_SRC/_core/" "$SKILLS_DEST/_core/"
rsync -a --delete "$SKILLS_SRC/_registry/" "$SKILLS_DEST/_registry/"
cp "$SKILLS_SRC/README.md" "$SKILLS_DEST/README.md"
cp "$SKILLS_SRC/SKILL-COMBOS.md" "$SKILLS_DEST/SKILL-COMBOS.md"
cp "$SKILLS_SRC/ATOMIC-SKILLS.md" "$SKILLS_DEST/ATOMIC-SKILLS.md"
if [[ -d "$SKILLS_SRC/packs" ]]; then
  rsync -a --delete "$SKILLS_SRC/packs/" "$SKILLS_DEST/packs/"
fi
rsync -a --delete "$DOCS_SRC/" "$DOCS_DEST/"

while IFS= read -r skill_name; do
  [[ -z "$skill_name" ]] && continue
  rsync -a --delete --exclude 'agents/' "$SKILLS_SRC/$skill_name/" "$SKILLS_DEST/$skill_name/"
  rm -rf "$SKILLS_DEST/$skill_name/agents"
done < "$TMP_MANIFEST"

mv "$TMP_MANIFEST" "$MANIFEST_PATH"

echo "Synced composable-skill-packs for Claude Code into $TARGET_ROOT"
echo "Restart Claude Code or reopen the workspace to pick up updated skills."
