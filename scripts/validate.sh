#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export PYTHONDONTWRITEBYTECODE=1

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

need_cmd python3
need_cmd bash
need_cmd rsync

python3 "$REPO_ROOT/skills/_registry/scripts/build_state_report.py"
python3 "$REPO_ROOT/skills/_registry/scripts/validate_registry.py"
python3 "$REPO_ROOT/skills/compose/scripts/parse_macro_golden_test.py"
bash "$REPO_ROOT/scripts/test_framework_user_scenarios.sh"
bash "$REPO_ROOT/scripts/test_sync_migration.sh"
bash "$REPO_ROOT/scripts/test_sync_claude.sh"
