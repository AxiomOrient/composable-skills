#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_DIR="$REPO_ROOT/scripts"
RUNTIME="${1:-codex}"

usage() {
  echo "Usage: ./scripts/sync.sh [codex|claude] [target-root]" >&2
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "$RUNTIME" == "codex" || "$RUNTIME" == "claude" ]]; then
  shift || true
else
  RUNTIME="codex"
fi

case "$RUNTIME" in
  codex)
    bash "$SCRIPT_DIR/sync_codex.sh" "${1:-$HOME/.codex}"
    ;;
  claude)
    bash "$SCRIPT_DIR/sync_claude.sh" "${1:-$HOME/.claude}"
    ;;
  *)
    echo "Unsupported runtime: $RUNTIME" >&2
    usage
    exit 1
    ;;
esac
