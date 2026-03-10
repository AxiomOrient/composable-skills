#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REGISTRY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REGISTRY_ROOT.parent
LENS_FILE = SKILLS_ROOT / "_core" / "lenses.json"


def load_lens_catalog() -> dict[str, dict]:
    try:
        raw = json.loads(LENS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}
    items = raw.get("lenses", [])
    out: dict[str, dict] = {}
    if not isinstance(items, list):
        return out
    for item in items:
        if not isinstance(item, dict):
            continue
        lens_id = item.get("id")
        if isinstance(lens_id, str) and lens_id:
            out[lens_id] = item
    return out


def append_bullet_list(lines: list[str], label: str, items: object) -> None:
    if isinstance(items, list) and items:
        lines.append(f"- `{label}`:")
        for item in items:
            lines.append(f"  - {item}")


def format_field(field: dict) -> str:
    parts = [field["type"], "required" if field.get("required") else "optional"]
    allowed_values = field.get("allowed_values")
    if isinstance(allowed_values, list) and allowed_values:
        parts.append(f"allowed: {'|'.join(str(v) for v in allowed_values)}")
    required_when = field.get("required_when")
    if isinstance(required_when, str) and required_when:
        parts.append(f"required when {required_when}")
    exclusive_with = field.get("exclusive_with")
    if isinstance(exclusive_with, str) and exclusive_with:
        parts.append(f"exclusive with {exclusive_with}")
    elif isinstance(exclusive_with, list) and exclusive_with:
        parts.append(f"exclusive with {', '.join(str(v) for v in exclusive_with)}")
    shape = field.get("shape")
    if isinstance(shape, str) and shape:
        parts.append(f"shape: {shape}")
    return f"- `{field['name']}` ({'; '.join(parts)}): {field['description']}"


def append_section(lines: list[str], title: str, items: object) -> None:
    if isinstance(items, list) and items:
        lines += ["", f"## {title}"]
        for item in items:
            lines.append(f"- {item}")


def build_skill_md(entry: dict) -> str:
    lens_catalog = load_lens_catalog()
    title = entry.get("title") or entry["name"].replace("-", " ").title()
    lines: list[str] = [
        "---",
        f"name: {entry['name']}",
        f"description: \"{entry['description']}\"",
        "---",
        "",
        f"# {title}",
        "",
        "## Purpose",
        entry["purpose"],
        "",
        "## Default Program",
        "```text",
        entry.get("default_program", "[orchestration-only]"),
        "```",
        "",
        "## Use When",
    ]
    for item in entry["when_to_use"]:
        lines.append(f"- {item}")
    lines += ["", "## Do Not Use When"]
    for item in entry["do_not_use"]:
        lines.append(f"- {item}")
    lines += ["", "## Required Inputs"]
    for field in entry["required_inputs"]:
        lines.append(format_field(field))
    append_section(lines, "Input Contract Notes", entry.get("input_contract_notes"))
    lines += ["", "## Structured Outputs"]
    for field in entry["structured_outputs"]:
        lines.append(format_field(field))
    append_section(lines, "Output Contract Notes", entry.get("output_contract_notes"))
    if entry.get("procedure"):
        lines += ["", "## Procedure"]
        for idx, step in enumerate(entry["procedure"], start=1):
            lines.append(f"{idx}. {step}")
    primary_lens = entry.get("primary_lens")
    if isinstance(primary_lens, str) and primary_lens:
        lens_info = lens_catalog.get(primary_lens, {})
        lines += ["", "## Primary Lens", f"- `primary_lens`: `{primary_lens}`"]
        frame_name = lens_info.get("frame_name")
        if isinstance(frame_name, str) and frame_name:
            lines.append(f"- `frame_name`: {frame_name}")
        if entry.get("lens_rationale"):
            lines.append(f"- `why`: {entry['lens_rationale']}")
        summary = lens_info.get("summary")
        if isinstance(summary, str) and summary:
            lines.append(f"- `summary`: {summary}")
        thesis = lens_info.get("thesis")
        if isinstance(thesis, str) and thesis:
            lines.append(f"- `thesis`: {thesis}")
        core_philosophy = lens_info.get("core_philosophy")
        if isinstance(core_philosophy, str) and core_philosophy:
            lines.append(f"- `core_philosophy`: {core_philosophy}")
        append_bullet_list(lines, "mental_model", lens_info.get("mental_model"))
        append_bullet_list(lines, "decision_rules", lens_info.get("decision_rules"))
        append_bullet_list(lines, "anti_patterns", lens_info.get("anti_patterns"))
        append_bullet_list(lines, "good_for", lens_info.get("good_for"))
        append_bullet_list(lines, "not_for", lens_info.get("not_for"))
        append_bullet_list(lines, "required_artifacts", lens_info.get("required_artifacts"))
        append_bullet_list(lines, "references", lens_info.get("references"))
    lines += ["", "## Artifacts", f"- `artifacts_in`: {', '.join(entry.get('artifacts_in', [])) or 'none'}", f"- `artifacts_out`: {', '.join(entry.get('artifacts_out', [])) or 'none'}", "", "## Neutrality Rules"]
    for rule in entry["neutrality_rules"]:
        lines.append(f"- {rule}")
    append_section(lines, "Execution Constraints", entry.get("execution_constraints"))
    if entry.get("mandatory_rules"):
        lines += ["", "## Mandatory Rules"]
        for rule in entry["mandatory_rules"]:
            lines.append(f"- {rule}")
    if entry.get("expands_to"):
        lines += ["", "## Expansion"]
        for token in entry["expands_to"]:
            lines.append(f"- `{token}`")
    if entry.get("required_refs"):
        lines += ["", "## Required References"]
        for ref in entry["required_refs"]:
            lines.append(f"- `{ref}`")
    if entry.get("example_invocation"):
        lines += ["", "## Example Invocation", "```text", entry["example_invocation"].strip(), "```"]
    lines += ["", "## Output Discipline", f"- `response_profile={entry['response_profile']}`", "- User-facing rendering is delegated to `respond`."]
    return "\n".join(lines).rstrip() + "\n"


def build_openai_yaml(entry: dict) -> str:
    allow = "false" if entry.get("explicit_only", False) else "true"
    display_name = entry.get("display_name") or entry.get("title") or entry["name"].replace("-", " ").title()
    return (
        "interface:\n"
        f"  display_name: \"{display_name}\"\n"
        f"  short_description: \"{entry['description']}\"\n"
        f"  default_prompt: \"{entry['default_prompt']}\"\n"
        "policy:\n"
        f"  allow_implicit_invocation: {allow}\n"
    )


def materialize(entry_path: Path) -> None:
    entry = json.loads(entry_path.read_text(encoding="utf-8"))
    skill_dir = SKILLS_ROOT / entry["name"]
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(build_skill_md(entry), encoding="utf-8")
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / "openai.yaml").write_text(build_openai_yaml(entry), encoding="utf-8")
    if entry.get("asset_template"):
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        (assets_dir / "request-template.txt").write_text(entry["asset_template"], encoding="utf-8")
    for ref in entry.get("required_refs", []):
        ref_path = skill_dir / ref
        if not ref_path.exists():
            ref_path.parent.mkdir(parents=True, exist_ok=True)
            ref_path.write_text(f"# {ref_path.name}\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("entry", help="Registry entry path, relative to skills/_registry")
    args = ap.parse_args()
    materialize(REGISTRY_ROOT / args.entry)
    print(f"Materialized {args.entry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
