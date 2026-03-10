#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PARSER="$REPO_ROOT/skills/compose/scripts/parse_macro.py"

run_case() {
  local name="$1"
  local macro="$2"
  local mode="${3:-success}"
  local py_check="$4"

  local tmp
  tmp="$(mktemp)"
  if python3 "$PARSER" --macro "$macro" --format json >"$tmp" 2>"$tmp.err"; then
    if [[ "$mode" == "failure" ]]; then
      echo "expected failure for $name" >&2
      cat "$tmp" >&2
      rm -f "$tmp" "$tmp.err"
      return 1
    fi
  else
    if [[ "$mode" == "failure" ]]; then
      python3 - "$tmp" "$tmp.err" <<'PY'
from pathlib import Path
import json
import sys
stdout = Path(sys.argv[1]).read_text()
stderr = Path(sys.argv[2]).read_text()
errors = []
if stdout.strip():
    try:
        payload = json.loads(stdout)
        errors.extend(payload.get("errors", []))
    except Exception:
        pass
errors.append(stderr)
joined = "\n".join(part for part in errors if part)
if "Unknown skill" not in joined:
    raise SystemExit(f"unexpected error text: {joined}")
PY
      rm -f "$tmp" "$tmp.err"
      return 0
    fi
    cat "$tmp.err" >&2
    rm -f "$tmp" "$tmp.err"
    return 1
  fi

  python3 - "$tmp" <<PY
import json, sys
payload = json.loads(open(sys.argv[1]).read())
$py_check
PY
  rm -f "$tmp" "$tmp.err"
}

run_case \
  "docs-maintainer-happy-path" \
  '$compose + $finish-until-done + $doc-write + $check-delivered + @docs + [Keep iterating until a first-time maintainer can follow the docs.]' \
  success \
  'assert "finish-until-done" in payload["parsed"]["expanded_skills"]; assert "doc-write" in payload["parsed"]["expanded_skills"]'

run_case \
  "framework-scenario-skill" \
  '$compose + $test-run-user-scenarios + @skills + [Simulate a first-time maintainer, a rushed releaser, and a confused docs contributor. Include happy, failure, and weird cases.]' \
  success \
  'assert payload["response_profile"]["primary_skill"] == "test-run-user-scenarios"; assert "test-run-user-scenarios" in payload["parsed"]["expanded_skills"]'

run_case \
  "duplicate-test-gap-collapse" \
  '$compose + $test-find-gaps + $test-find-gaps + @src/auth + [Check repeated gap scan input.]' \
  success \
  'assert payload["parsed"]["expanded_skills"].count("test-find-gaps") == 1; assert any("Collapsed duplicate skill `$test-find-gaps`" in w for w in payload.get("warnings", []))'

run_case \
  "legacy-test-skill-name-rejected" \
  '$compose + $plan-test-cases + @src/auth + [legacy name should fail]' \
  failure \
  'pass'

run_case \
  "release-review-user-flow" \
  '$compose + $wf-ship-ready-check + $check-delivered + @skills + [I am about to release this pack today. Tell me what blocks me.]' \
  success \
  'expanded = payload["parsed"]["expanded_skills"]; assert "ship-check-repo" in expanded and "ship-check-hygiene" in expanded and "ship-go-nogo" in expanded'

echo "framework user scenario test passed"
