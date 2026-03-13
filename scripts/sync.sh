#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  echo "Usage: ./scripts/sync.sh [local] [profile] [target-agents-root]" >&2
  echo "Profiles: core | docs-release | extras | all" >&2
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

MODE="${1:-global}"
PROFILE="core"
TARGET_ROOT_ARG=""
is_profile() {
  [[ "$1" == "core" || "$1" == "docs-release" || "$1" == "extras" || "$1" == "all" ]]
}
if [[ "$MODE" == "local" ]]; then
  shift || true
  if [[ -n "${1:-}" ]] && is_profile "${1:-}"; then
    PROFILE="$1"
    shift || true
  fi
  TARGET_ROOT_ARG="${1:-}"
else
  MODE="global"
  if [[ -n "${1:-}" ]] && is_profile "${1:-}"; then
    PROFILE="$1"
    shift || true
  fi
  TARGET_ROOT_ARG="${1:-}"
fi

resolve_local_root() {
  local explicit_root="${1:-}"
  if [[ -n "$explicit_root" ]]; then
    printf '%s\n' "$explicit_root"
    return 0
  fi
  printf '%s\n' "$PWD/.agents"
}

resolve_global_root() {
  local explicit_root="${1:-}"
  if [[ -n "$explicit_root" ]]; then
    printf '%s\n' "$explicit_root"
    return 0
  fi
  printf '%s\n' "$HOME/.agents"
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

need_cmd python3

if [[ "$MODE" == "local" ]]; then
  python3 "$REPO_ROOT/scripts/skills.py" sync --profile "$PROFILE" "$(resolve_local_root "$TARGET_ROOT_ARG")"
else
  python3 "$REPO_ROOT/scripts/skills.py" sync --profile "$PROFILE" "$(resolve_global_root "$TARGET_ROOT_ARG")"
fi
