#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_ROOT="${1:-$HOME/.codex}"
SKILLS_SRC="$REPO_ROOT/skills"
DOCS_SRC="$REPO_ROOT/docs"
SKILLS_DEST="$TARGET_ROOT/skills"
DOCS_DEST="$TARGET_ROOT/docs"
MANIFEST_PATH="$TARGET_ROOT/.composable-skill-packs-manifest.txt"
LEGACY_MANIFEST_PATH="$TARGET_ROOT/.codex-skills-manifest.txt"
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

EXISTING_MANIFEST_PATH="$MANIFEST_PATH"
if [[ ! -f "$EXISTING_MANIFEST_PATH" && -f "$LEGACY_MANIFEST_PATH" ]]; then
  EXISTING_MANIFEST_PATH="$LEGACY_MANIFEST_PATH"
fi

if [[ -f "$EXISTING_MANIFEST_PATH" ]]; then
  while IFS= read -r old_skill; do
    [[ -z "$old_skill" ]] && continue
    if ! grep -Fxq "$old_skill" "$TMP_MANIFEST"; then
      rm -rf "$SKILLS_DEST/$old_skill"
    fi
  done < "$EXISTING_MANIFEST_PATH"
fi

rsync -a --delete "$SKILLS_SRC/_core/" "$SKILLS_DEST/_core/"
rsync -a --delete "$SKILLS_SRC/_registry/" "$SKILLS_DEST/_registry/"
cp "$SKILLS_SRC/README.md" "$SKILLS_DEST/README.md"
cp "$SKILLS_SRC/SKILL-COMBOS.md" "$SKILLS_DEST/SKILL-COMBOS.md"
cp "$SKILLS_SRC/ATOMIC-SKILLS.md" "$SKILLS_DEST/ATOMIC-SKILLS.md"
if [[ -d "$SKILLS_SRC/packs" ]]; then
  rsync -a --delete "$SKILLS_SRC/packs/" "$SKILLS_DEST/packs/"
fi

while IFS= read -r skill_name; do
  [[ -z "$skill_name" ]] && continue
  rsync -a --delete "$SKILLS_SRC/$skill_name/" "$SKILLS_DEST/$skill_name/"
done < "$TMP_MANIFEST"

rsync -a --delete "$DOCS_SRC/" "$DOCS_DEST/"

mv "$TMP_MANIFEST" "$MANIFEST_PATH"
rm -f "$LEGACY_MANIFEST_PATH"

echo "Synced composable-skill-packs into $TARGET_ROOT"
echo "Restart Codex to pick up updated skills."
