#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


REGISTRY_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = REGISTRY_ROOT.parent.parent / "docs"
STATE_REPORT_PATH = DOCS_ROOT / "SKILL-STATE-REPORT.md"


STATE_LABELS = {
    "atomic-stable": "하나의 문제와 하나의 산출물에 집중된 atomic skill",
    "broad-entrypoint": "direct entry는 허용하지만 더 좁은 skill이 있으면 우선 대체해야 하는 skill",
    "utility-stable": "orchestration/rendering/execution-governance 전용 utility",
    "workflow-stable": "explicit `expands_to`를 가진 named workflow",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry() -> tuple[dict[str, list[str]], dict[str, dict]]:
    index = load_json(REGISTRY_ROOT / "index.json")
    entries: dict[str, dict] = {}
    for layer, names in index.items():
        for name in names:
            entries[name] = load_json(REGISTRY_ROOT / layer / f"{name}.json")
    return index, entries


def derive_state(entry: dict) -> str:
    layer = entry["layer"]
    if layer == "utility":
        return "utility-stable"
    if layer == "workflow":
        return "workflow-stable"
    split_candidates = entry.get("split_candidates") or []
    if isinstance(split_candidates, list) and split_candidates:
        return "broad-entrypoint"
    return "atomic-stable"


def current_state_text(entry: dict, state: str) -> str:
    if state == "atomic-stable":
        return "Single-problem atomic skill."
    if state == "broad-entrypoint":
        split_candidates = entry.get("split_candidates") or []
        joined = ", ".join(f"`{name}`" for name in split_candidates)
        return f"Direct entrypoint. Prefer {joined} when scope is narrower." if joined else "Direct entrypoint."
    if state == "utility-stable":
        return "Utility-only skill."
    if state == "workflow-stable":
        return "Canonical workflow."
    return "Canonical workflow."


def field_names(fields: list[dict]) -> str:
    return ", ".join(f"`{field['name']}`" for field in fields)


def rows_for_layer(layer: str, names: list[str], entries: dict[str, dict]) -> list[str]:
    rows = []
    for name in names:
        entry = entries[name]
        state = derive_state(entry)
        rows.append(
            "| {name} | {family} | {job} | {state} | {inputs} | {outputs} | {current} |".format(
                name=entry["name"],
                family=entry["family"],
                job=entry["job_type"],
                state=state,
                inputs=field_names(entry["required_inputs"]),
                outputs=field_names(entry["structured_outputs"]),
                current=current_state_text(entry, state),
            )
        )
    return rows


def render_state_report() -> str:
    index, entries = load_registry()
    atomic_count = len(index["atomic"])
    utility_count = len(index["utility"])
    workflow_count = len(index["workflow"])
    total = atomic_count + utility_count + workflow_count

    lines = [
        "# Skill State Report",
        "",
        "> Generated from `skills/_registry/index.json` and registry entries. Do not edit manually.",
        "",
        "## Summary",
        "",
        f"- registry 기준 현재 구성: `atomic {atomic_count} / utility {utility_count} / workflow {workflow_count} / total {total}`",
        "- `State` 열은 registry field가 아니라 generated classification이다.",
        "- classification rule:",
        "  - atomic + `split_candidates` 있음 -> `broad-entrypoint`",
        "  - atomic + `split_candidates` 없음 -> `atomic-stable`",
        "  - utility -> `utility-stable`",
        "  - workflow -> `workflow-stable`",
        "",
        "## State Labels",
        "",
    ]
    for key, desc in STATE_LABELS.items():
        lines.append(f"- `{key}`: {desc}")

    lines += [
        "",
        "## Atomic Skills",
        "",
        "| Skill | Family | Job | State | Required Inputs | Structured Outputs | Current State |",
        "|---|---|---|---|---|---|---|",
    ]
    lines.extend(rows_for_layer("atomic", index["atomic"], entries))

    lines += [
        "",
        "## Utility Skills",
        "",
        "| Skill | Family | Job | State | Required Inputs | Structured Outputs | Current State |",
        "|---|---|---|---|---|---|---|",
    ]
    lines.extend(rows_for_layer("utility", index["utility"], entries))

    lines += [
        "",
        "## Workflow Skills",
        "",
        "| Skill | Family | Job | State | Required Inputs | Structured Outputs | Current State |",
        "|---|---|---|---|---|---|---|",
    ]
    lines.extend(rows_for_layer("workflow", index["workflow"], entries))
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    STATE_REPORT_PATH.write_text(render_state_report(), encoding="utf-8")
    print(f"Wrote {STATE_REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
