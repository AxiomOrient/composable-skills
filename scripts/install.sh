#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNTIME="${1:-codex}"

usage() {
  echo "Usage: ./scripts/install.sh [codex|claude] [target-root]" >&2
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
    "$SCRIPT_DIR/sync.sh" codex "${1:-$HOME/.codex}"
    ;;
  claude)
    "$SCRIPT_DIR/sync.sh" claude "${1:-$HOME/.claude}"
    ;;
  *)
    echo "Unsupported runtime: $RUNTIME" >&2
    usage
    exit 1
    ;;
esac
