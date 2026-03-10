#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from build_state_report import STATE_REPORT_PATH, render_state_report


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "atomic": {
        "name", "layer", "family", "job_type", "description", "purpose",
        "when_to_use", "do_not_use", "required_inputs", "structured_outputs",
        "artifacts_in", "artifacts_out", "neutrality_rules", "primary_lens",
        "lens_rationale", "response_profile",
        "default_prompt", "default_program", "explicit_only"
    },
    "utility": {
        "name", "layer", "family", "job_type", "description", "purpose",
        "when_to_use", "do_not_use", "required_inputs", "structured_outputs",
        "artifacts_in", "artifacts_out", "neutrality_rules", "response_profile",
        "default_prompt", "default_program", "explicit_only"
    },
    "workflow": {
        "name", "layer", "family", "job_type", "description", "purpose",
        "when_to_use", "do_not_use", "required_inputs", "structured_outputs",
        "artifacts_in", "artifacts_out", "neutrality_rules", "response_profile",
        "default_prompt", "default_program", "explicit_only", "expands_to"
    },
}


def load_valid_lenses() -> tuple[dict[str, dict], dict[str, object], list[str]]:
    lens_file = ROOT.parent / "_core" / "lenses.json"
    errors: list[str] = []
    try:
        raw = json.loads(lens_file.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, {}, [f"{lens_file}: missing lenses.json"]
    except json.JSONDecodeError as exc:
        return {}, {}, [f"{lens_file}: invalid json ({exc})"]

    lenses = raw.get("lenses")
    if not isinstance(lenses, list):
        return {}, {}, [f"{lens_file}: `lenses` must be a list"]

    catalog = raw.get("catalog")
    if not isinstance(catalog, dict):
        errors.append(f"{lens_file}: `catalog` must be an object")
        catalog = {}

    out: dict[str, dict] = {}
    for idx, item in enumerate(lenses):
        if not isinstance(item, dict):
            errors.append(f"{lens_file}: lenses[{idx}] must be an object")
            continue
        lens_id = item.get("id")
        if not isinstance(lens_id, str) or not lens_id:
            errors.append(f"{lens_file}: lenses[{idx}] missing valid `id`")
            continue
        status = item.get("status")
        if status not in {"active", "reserve", "alias"}:
            errors.append(f"{lens_file}: lenses[{idx}] has invalid `status`")
        for key in ("display_name", "category", "summary", "required_artifacts", "keywords"):
            if key not in item:
                errors.append(f"{lens_file}: lenses[{idx}] missing `{key}`")
        if status == "alias":
            alias_of = item.get("alias_of")
            if not isinstance(alias_of, str) or not alias_of:
                errors.append(f"{lens_file}: lenses[{idx}] alias lens missing valid `alias_of`")
        else:
            for key in ("frame_name", "thesis", "decision_rules", "anti_patterns", "good_for", "not_for", "references"):
                if key not in item:
                    errors.append(f"{lens_file}: lenses[{idx}] missing `{key}`")
        out[lens_id] = item

    active = catalog.get("active_lenses", [])
    reserve = catalog.get("reserve_lenses", [])
    public_aliases = catalog.get("public_aliases", {})
    if not isinstance(active, list):
        errors.append(f"{lens_file}: catalog.active_lenses must be a list")
        active = []
    if not isinstance(reserve, list):
        errors.append(f"{lens_file}: catalog.reserve_lenses must be a list")
        reserve = []
    if not isinstance(public_aliases, dict):
        errors.append(f"{lens_file}: catalog.public_aliases must be an object")
        public_aliases = {}
    for lens_id in active:
        item = out.get(lens_id)
        if not item:
            errors.append(f"{lens_file}: active lens `{lens_id}` is not defined")
        elif item.get("status") != "active":
            errors.append(f"{lens_file}: active lens `{lens_id}` must have status `active`")
    for lens_id in reserve:
        item = out.get(lens_id)
        if not item:
            errors.append(f"{lens_file}: reserve lens `{lens_id}` is not defined")
        elif item.get("status") != "reserve":
            errors.append(f"{lens_file}: reserve lens `{lens_id}` must have status `reserve`")
    for alias_id, target in public_aliases.items():
        alias_item = out.get(alias_id)
        if not alias_item:
            errors.append(f"{lens_file}: public alias `{alias_id}` is not defined")
            continue
        if alias_item.get("status") != "alias":
            errors.append(f"{lens_file}: public alias `{alias_id}` must have status `alias`")
        if alias_item.get("alias_of") != target:
            errors.append(f"{lens_file}: public alias `{alias_id}` must target `{target}`")
        if target not in out:
            errors.append(f"{lens_file}: public alias `{alias_id}` points to undefined lens `{target}`")
        elif out[target].get("status") != "active":
            errors.append(f"{lens_file}: public alias `{alias_id}` must point to an active lens")
    return out, catalog, errors


def load_entries() -> tuple[dict[str, dict], list[str]]:
    entries: dict[str, dict] = {}
    errors: list[str] = []
    for layer in ("atomic", "utility", "workflow"):
        layer_dir = ROOT / layer
        if not layer_dir.exists():
            continue
        for entry_path in sorted(layer_dir.glob("*.json")):
            try:
                data = json.loads(entry_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{entry_path}: invalid json ({exc})")
                continue
            name = data.get("name")
            if not isinstance(name, str) or not name:
                errors.append(f"{entry_path}: missing or invalid `name`")
                continue
            if name in entries:
                errors.append(f"{entry_path}: duplicate registry name `{name}`")
                continue
            entries[name] = {"data": data, "path": entry_path, "layer": layer}
    return entries, errors


def validate_field_objects(name: str, data: list, errors: list[str]) -> None:
    if not isinstance(data, list) or not data:
        errors.append(f"{name} must be a non-empty list")
        return
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            errors.append(f"{name}[{idx}] must be an object")
            continue
        for key in ("name", "type", "required", "description"):
            if key not in item:
                errors.append(f"{name}[{idx}] missing `{key}`")
        required_when = item.get("required_when")
        if required_when is not None and not isinstance(required_when, str):
            errors.append(f"{name}[{idx}] `required_when` must be a string when present")
        allowed_values = item.get("allowed_values")
        if allowed_values is not None:
            if not isinstance(allowed_values, list) or not allowed_values or not all(isinstance(v, str) and v for v in allowed_values):
                errors.append(f"{name}[{idx}] `allowed_values` must be a non-empty list of strings when present")
        exclusive_with = item.get("exclusive_with")
        if exclusive_with is not None:
            valid_list = isinstance(exclusive_with, list) and exclusive_with and all(isinstance(v, str) and v for v in exclusive_with)
            valid_str = isinstance(exclusive_with, str) and bool(exclusive_with)
            if not (valid_str or valid_list):
                errors.append(f"{name}[{idx}] `exclusive_with` must be a string or non-empty list of strings when present")
        shape = item.get("shape")
        if shape is not None and not isinstance(shape, str):
            errors.append(f"{name}[{idx}] `shape` must be a string when present")


def validate_string_list(name: str, data: object, errors: list[str]) -> None:
    if data is None:
        return
    if not isinstance(data, list) or not all(isinstance(item, str) and item for item in data):
        errors.append(f"{name} must be a list of non-empty strings when present")


def validate_entry(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    layer = path.parent.name
    errors: list[str] = []
    missing = sorted(REQUIRED[layer] - set(data.keys()))
    if missing:
        errors.append(f"missing keys: {', '.join(missing)}")
    if data.get("layer") != layer:
        errors.append(f"layer mismatch: expected {layer}, got {data.get('layer')}")
    if data.get("name") != path.stem:
        errors.append(f"name mismatch: file stem `{path.stem}` != entry name `{data.get('name')}`")
    validate_field_objects("required_inputs", data.get("required_inputs"), errors)
    validate_field_objects("structured_outputs", data.get("structured_outputs"), errors)
    validate_string_list("input_contract_notes", data.get("input_contract_notes"), errors)
    validate_string_list("output_contract_notes", data.get("output_contract_notes"), errors)
    validate_string_list("execution_constraints", data.get("execution_constraints"), errors)
    neutrality = data.get("neutrality_rules")
    if not isinstance(neutrality, list) or not neutrality:
        errors.append("neutrality_rules must be a non-empty list")
    if layer == "atomic":
        if not isinstance(data.get("primary_lens"), str) or not data.get("primary_lens"):
            errors.append("primary_lens must be a non-empty string")
        if not isinstance(data.get("lens_rationale"), str) or not data.get("lens_rationale"):
            errors.append("lens_rationale must be a non-empty string")
    if layer == "workflow":
        expands_to = data.get("expands_to")
        if not isinstance(expands_to, list) or not expands_to:
            errors.append("expands_to must be a non-empty list")
        if not data.get("name", "").startswith("wf-"):
            errors.append("workflow names must use the `wf-` prefix")
    return errors


def validate_workflow_graph(entries: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    workflow_graph: dict[str, list[str]] = {}

    for name, info in entries.items():
        data = info["data"]
        if info["layer"] != "workflow":
            continue
        expanded_names: list[str] = []
        for raw in data.get("expands_to", []):
            if not isinstance(raw, str) or not raw.startswith("$"):
                errors.append(f"{info['path']}: invalid expands_to token `{raw}`")
                continue
            target = raw[1:]
            expanded_names.append(target)
            if target not in entries:
                errors.append(f"{info['path']}: expands_to references unknown skill `{target}`")
        workflow_graph[name] = expanded_names

    visited: set[str] = set()
    stack: list[str] = []
    active: set[str] = set()

    def dfs(node: str) -> None:
        visited.add(node)
        stack.append(node)
        active.add(node)
        for target in workflow_graph.get(node, []):
            if target not in workflow_graph:
                continue
            if target in active:
                cycle = " -> ".join(stack + [target])
                errors.append(f"workflow cycle detected: {cycle}")
                continue
            if target not in visited:
                dfs(target)
        stack.pop()
        active.remove(node)

    for node in sorted(workflow_graph):
        if node not in visited:
            dfs(node)

    return errors


def validate_index(entries: dict[str, dict]) -> list[str]:
    index_path = ROOT / "index.json"
    if not index_path.exists():
        return [f"{index_path}: missing index.json"]
    try:
        current = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{index_path}: invalid json ({exc})"]

    expected = {
        layer: sorted(name for name, info in entries.items() if info["layer"] == layer)
        for layer in ("atomic", "utility", "workflow")
    }
    errors: list[str] = []
    for layer, names in expected.items():
        indexed = sorted(current.get(layer, []))
        if indexed != names:
            errors.append(
                f"{index_path}: {layer} index mismatch (expected {names}, got {indexed})"
            )
    return errors


def validate_generated_state_report() -> list[str]:
    expected = render_state_report()
    if not STATE_REPORT_PATH.exists():
        return [f"{STATE_REPORT_PATH}: missing generated state report"]
    current = STATE_REPORT_PATH.read_text(encoding="utf-8")
    if current != expected:
        return [f"{STATE_REPORT_PATH}: generated content drift detected; run build_state_report.py"]
    return []


def validate_skill_surface_sync(entries: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    skills_root = ROOT.parent
    program_pattern = re.compile(r"##\s+Default\s+Program\s*\n```text\n(.*?)\n```", flags=re.S)
    section_pattern = re.compile(r"##\s+([^\n]+)\n(.*?)(?=\n##\s+|\Z)", flags=re.S)
    output_discipline_pattern = re.compile(r"`response_profile=([^`]+)`")

    for name, info in entries.items():
        skill_md = skills_root / name / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{skill_md}: missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        match = program_pattern.search(text)
        if not match:
            errors.append(f"{skill_md}: missing Default Program block")
            continue
        current_program = match.group(1).strip()
        expected_program = info["data"].get("default_program", "[orchestration-only]").strip()
        if current_program != expected_program:
            errors.append(
                f"{skill_md}: Default Program drift detected (registry `{expected_program}` != SKILL.md `{current_program}`)"
            )
        sections = {title.strip(): body for title, body in section_pattern.findall(text)}
        required_inputs_body = sections.get("Required Inputs")
        structured_outputs_body = sections.get("Structured Outputs")
        if required_inputs_body is None:
            errors.append(f"{skill_md}: missing Required Inputs section")
        else:
            current_inputs = re.findall(r"- `([^`]+)` \(", required_inputs_body)
            expected_inputs = [field["name"] for field in info["data"].get("required_inputs", [])]
            if current_inputs != expected_inputs:
                errors.append(
                    f"{skill_md}: Required Inputs drift detected (registry {expected_inputs} != SKILL.md {current_inputs})"
                )
        if structured_outputs_body is None:
            errors.append(f"{skill_md}: missing Structured Outputs section")
        else:
            current_outputs = re.findall(r"- `([^`]+)` \(", structured_outputs_body)
            expected_outputs = [field["name"] for field in info["data"].get("structured_outputs", [])]
            if current_outputs != expected_outputs:
                errors.append(
                    f"{skill_md}: Structured Outputs drift detected (registry {expected_outputs} != SKILL.md {current_outputs})"
                )
        output_match = output_discipline_pattern.search(text)
        expected_profile = info["data"].get("response_profile")
        current_profile = output_match.group(1).strip() if output_match else None
        if current_profile != expected_profile:
            errors.append(
                f"{skill_md}: Output Discipline drift detected (registry `{expected_profile}` != SKILL.md `{current_profile}`)"
            )
        for registry_key, section_name in (
            ("input_contract_notes", "Input Contract Notes"),
            ("output_contract_notes", "Output Contract Notes"),
            ("execution_constraints", "Execution Constraints"),
        ):
            expected_items = info["data"].get(registry_key)
            if not expected_items:
                continue
            current_body = sections.get(section_name)
            if current_body is None:
                errors.append(f"{skill_md}: missing {section_name} section")
                continue
            current_items = [item.strip() for item in re.findall(r"- (.+)", current_body)]
            if current_items != expected_items:
                errors.append(
                    f"{skill_md}: {section_name} drift detected (registry {expected_items} != SKILL.md {current_items})"
                )
    return errors


def main() -> int:
    errors: list[str] = []
    entries, load_errors = load_entries()
    errors.extend(load_errors)
    lens_catalog, lens_meta, lens_errors = load_valid_lenses()
    errors.extend(lens_errors)
    for info in entries.values():
        entry = info["path"]
        entry_errors = validate_entry(entry)
        for err in entry_errors:
            errors.append(f"{entry}: {err}")
        if info["layer"] == "atomic" and lens_catalog:
            primary_lens = info["data"].get("primary_lens")
            if primary_lens not in lens_catalog:
                errors.append(f"{entry}: primary_lens `{primary_lens}` is not defined in _core/lenses.json")
            elif lens_catalog[primary_lens].get("status") != "active":
                errors.append(f"{entry}: primary_lens `{primary_lens}` must point to an active lens")
    errors.extend(validate_workflow_graph(entries))
    errors.extend(validate_index(entries))
    errors.extend(validate_generated_state_report())
    errors.extend(validate_skill_surface_sync(entries))
    if errors:
        print("FAIL")
        for err in errors:
            print("-", err)
        return 1
    print("PASS: registry entries are structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
