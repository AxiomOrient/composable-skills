#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, Iterable, List


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
SKILL_META_FILE = "skill.json"
TOP_LEVEL_SKILL_FILES = ["README.md"]
TOP_LEVEL_SKILL_DIRS = ["_meta"]
MANIFEST_FILE = ".composable-skills-manifest.txt"
LEGACY_MANIFEST_FILES = [".composable-skill-packs-manifest.txt"]
LEGACY_DOC_FILES = [
    "ATOMIC-SKILLS.md",
    "CODEX-SKILL-AUTHORING-GUIDE.md",
    "SKILL-COMBOS.md",
    "SKILL-SYSTEM.md",
    "UTILITY-SKILLS.md",
    "WORKFLOW-SKILLS.md",
    "AGENT-SKILL-GUIDE.md",
    "SKILL-REFACTORING-PLAN.md",
]
DOCS_MANIFEST_FILE = ".composable-skills-docs-manifest.txt"
LEGACY_DOCS_MANIFEST_FILES = [".composable-skill-packs-docs-manifest.txt"]

DEFAULT_PROGRAM_PATTERN = re.compile(r"##\s+Default\s+Program\s*\n```text\n(.*?)\n```", flags=re.S)
FRONTMATTER_DESCRIPTION_PATTERN = re.compile(r'^description:\s*"((?:\\"|[^"])*)"\s*$', flags=re.M)
FRONTMATTER_NAME_PATTERN = re.compile(r"^name:\s*(\S+)", re.MULTILINE)
SCAFFOLD_PLACEHOLDERS = (
    "TODO: replace with one-line trigger surface.",
    "TODO: state one bounded job for this skill.",
    "TODO: list concrete trigger conditions.",
    "TODO: list adjacent requests this skill should reject.",
    "None yet. Replace with explicit inputs before shipping.",
    "TODO: replace with the actual output contract.",
)


def direct_meta_dir(skills_root: Path) -> Path:
    return skills_root / "_meta"


def lenses_path(skills_root: Path) -> Path:
    return direct_meta_dir(skills_root) / "lenses.json"


def response_profiles_path(skills_root: Path) -> Path:
    return direct_meta_dir(skills_root) / "response_profiles.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def yaml_unquote(text: str) -> str:
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        text = text[1:-1]
    return text.replace("\\\\", "\\").replace('\\"', '"')


def yaml_quote(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def find_scaffold_placeholders(path: Path) -> List[str]:
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")
    return [marker for marker in SCAFFOLD_PLACEHOLDERS if marker in content]


def iter_skill_dirs(skills_root: Path) -> Iterable[Path]:
    for path in sorted(skills_root.iterdir()):
        if not path.is_dir() or path.name.startswith("."):
            continue
        if path.name == "_meta":
            continue
        if (path / "SKILL.md").exists():
            yield path


def direct_skill_entries(skills_root: Path) -> Dict[str, dict]:
    entries: Dict[str, dict] = {}
    for path in iter_skill_dirs(skills_root):
        meta_path = path / SKILL_META_FILE
        if meta_path.exists():
            entries[path.name] = load_json(meta_path)
    return entries


def extract_default_program(skill_md_path: Path) -> str:
    content = skill_md_path.read_text(encoding="utf-8")
    match = DEFAULT_PROGRAM_PATTERN.search(content)
    if not match:
        raise ValueError(f"Default Program block missing in {skill_md_path}")
    return match.group(1).strip()


def extract_frontmatter_description(skill_md_path: Path) -> str:
    content = skill_md_path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError(f"Frontmatter description missing in {skill_md_path}")
    end_index = content.find("\n---", 4)
    if end_index == -1:
        raise ValueError(f"Frontmatter description missing in {skill_md_path}")
    frontmatter = content[:end_index]
    match = FRONTMATTER_DESCRIPTION_PATTERN.search(frontmatter)
    if not match:
        raise ValueError(f"Frontmatter description missing in {skill_md_path}")
    return yaml_unquote(match.group(1).strip())


def extract_frontmatter_name(skill_md_path: Path) -> str:
    content = skill_md_path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError(f"Frontmatter missing in {skill_md_path}")
    end_index = content.find("\n---", 4)
    if end_index == -1:
        raise ValueError(f"Frontmatter missing in {skill_md_path}")
    frontmatter = content[:end_index]
    match = FRONTMATTER_NAME_PATTERN.search(frontmatter)
    if not match:
        raise ValueError(f"Frontmatter name missing in {skill_md_path}")
    return match.group(1).strip()


def parse_openai_yaml(agent_yaml_path: Path) -> Dict[str, str]:
    if not agent_yaml_path.exists():
        raise ValueError(f"Missing agent metadata file: {agent_yaml_path}")

    parsed: Dict[str, str] = {}
    for line in agent_yaml_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("display_name: "):
            parsed["display_name"] = yaml_unquote(stripped.split(": ", 1)[1].strip())
        elif stripped.startswith("short_description: "):
            parsed["short_description"] = yaml_unquote(stripped.split(": ", 1)[1].strip())
        elif stripped.startswith("default_prompt: "):
            parsed["default_prompt"] = yaml_unquote(stripped.split(": ", 1)[1].strip())
        elif stripped.startswith("allow_implicit_invocation: "):
            parsed["allow_implicit_invocation"] = stripped.split(": ", 1)[1].strip()

    required_keys = {"display_name", "short_description", "default_prompt", "allow_implicit_invocation"}
    missing = sorted(required_keys - set(parsed))
    if missing:
        raise ValueError(f"{agent_yaml_path}: missing required keys {missing}")
    return parsed


def valid_lens_ids(lenses_payload: dict) -> List[str]:
    ids = set()
    raw = lenses_payload.get("valid_ids")
    if isinstance(raw, list):
        ids.update(item for item in raw if isinstance(item, str) and item)
    raw_lenses = lenses_payload.get("lenses")
    if isinstance(raw_lenses, list):
        for item in raw_lenses:
            if not isinstance(item, dict):
                continue
            lens_id = item.get("id")
            if isinstance(lens_id, str) and lens_id:
                ids.add(lens_id)
    return sorted(ids)


def expected_allow_implicit_invocation(codex_surface: str) -> bool:
    return codex_surface == "public_entry"


def render_openai_yaml(*, name: str, display_name: str, description: str, codex_surface: str) -> str:
    return (
        "interface:\n"
        f'  display_name: "{yaml_quote(display_name)}"\n'
        f'  short_description: "{yaml_quote(description)}"\n'
        f'  default_prompt: "${yaml_quote(name)}"\n'
        "policy:\n"
        f"  allow_implicit_invocation: {str(expected_allow_implicit_invocation(codex_surface)).lower()}\n"
    )


def build_expected_openai_yaml(skills_root: Path, name: str, entry: dict) -> str:
    description = extract_frontmatter_description(skills_root / name / "SKILL.md")
    return render_openai_yaml(
        name=name,
        display_name=entry["display_name"],
        description=description,
        codex_surface=entry["codex_surface"],
    )


def command_validate(skills_root: Path) -> int:
    errors: List[str] = []
    notes: List[str] = []
    response_profiles = response_profiles_path(skills_root)
    lenses = lenses_path(skills_root)
    missing_agent_yaml: List[str] = []

    direct_entries = direct_skill_entries(skills_root)
    all_skill_names = [path.name for path in iter_skill_dirs(skills_root)]
    if not direct_entries:
        errors.append(f"No direct skill metadata files found under `{skills_root}`.")
    else:
        notes.append(f"Validated {len(direct_entries)} direct skill metadata file(s).")

    missing_meta = sorted(set(all_skill_names) - set(direct_entries))
    if missing_meta:
        errors.append(f"Missing direct skill metadata for: {', '.join(missing_meta)}")

    if response_profiles.exists():
        direct_profiles = load_json(response_profiles)
        direct_required = direct_profiles.get("required_sections")
        if not isinstance(direct_required, dict) or not direct_required:
            errors.append(f"{response_profiles}: missing valid `required_sections` map.")
            direct_required = {}
        else:
            notes.append("Direct response profile metadata is present.")
    else:
        errors.append(f"Missing direct response profile metadata: {response_profiles}")
        direct_required = {}

    if lenses.exists():
        direct_lenses = valid_lens_ids(load_json(lenses))
        if not direct_lenses:
            errors.append(f"{lenses}: missing valid lens ids.")
        else:
            notes.append("Direct lens metadata is present.")
    else:
        errors.append(f"Missing direct lens metadata: {lenses}")
        direct_lenses = []

    required_keys = {
        "name",
        "layer",
        "layer_badge",
        "response_profile",
        "default_program",
        "required_inputs",
        "display_name",
        "browse_category",
        "browse_priority",
        "is_category_default",
        "codex_surface",
        "starter_inputs",
    }

    for name, entry in sorted(direct_entries.items()):
        meta_path = skills_root / name / SKILL_META_FILE
        skill_md_path = skills_root / name / "SKILL.md"
        agent_yaml_path = skills_root / name / "agents" / "openai.yaml"

        if entry.get("name") != name:
            errors.append(f"{meta_path}: name must match directory name `{name}`.")

        try:
            frontmatter_name = extract_frontmatter_name(skill_md_path)
            if frontmatter_name != name:
                errors.append(f"{skill_md_path}: frontmatter name `{frontmatter_name}` must match directory name `{name}`.")
        except ValueError as exc:
            errors.append(str(exc))

        missing_keys = sorted(required_keys - set(entry.keys()))
        if missing_keys:
            errors.append(f"{meta_path}: missing required keys {missing_keys}")

        if entry.get("layer") == "workflow" and not isinstance(entry.get("expands_to"), list):
            errors.append(f"{meta_path}: workflow metadata must define `expands_to`.")

        try:
            current_program = extract_default_program(skill_md_path)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            expected_program = entry.get("default_program")
            if current_program != expected_program:
                errors.append(f"{meta_path}: default_program drift detected against `{skill_md_path}`.")

            lens_match = re.search(r"\blens:\s*([^\s|\]]+)", current_program)
            if lens_match:
                lens_id = lens_match.group(1).strip()
                if direct_lenses and lens_id not in direct_lenses:
                    errors.append(f"{meta_path}: default program lens `{lens_id}` is not present in `{lenses}`.")

        expected_profile = entry.get("response_profile")
        if isinstance(expected_profile, str) and direct_required and expected_profile not in direct_required:
            errors.append(f"{meta_path}: response_profile `{expected_profile}` missing from `{response_profiles}`.")

        try:
            current_description = extract_frontmatter_description(skill_md_path)
        except ValueError as exc:
            errors.append(str(exc))
            current_description = None

        if agent_yaml_path.exists():
            try:
                agent_metadata = parse_openai_yaml(agent_yaml_path)
            except ValueError as exc:
                errors.append(str(exc))
            else:
                expected_prompt = f"${name}"
                if agent_metadata["display_name"] != entry.get("display_name"):
                    errors.append(f"{agent_yaml_path}: display_name drift detected against `{meta_path}`.")
                if current_description is not None and agent_metadata["short_description"] != current_description:
                    errors.append(f"{agent_yaml_path}: short_description drift detected against `{skill_md_path}`.")
                if agent_metadata["default_prompt"] != expected_prompt:
                    errors.append(f"{agent_yaml_path}: default_prompt must be `{expected_prompt}`.")
                expected_allow = str(expected_allow_implicit_invocation(entry.get("codex_surface", ""))).lower()
                if agent_metadata["allow_implicit_invocation"] != expected_allow:
                    errors.append(
                        f"{agent_yaml_path}: allow_implicit_invocation must be `{expected_allow}` for codex_surface `{entry.get('codex_surface')}`."
                    )
        else:
            missing_agent_yaml.append(name)

        skill_placeholders = find_scaffold_placeholders(skill_md_path)
        if skill_placeholders:
            errors.append(f"{skill_md_path}: unresolved scaffold placeholders present: {', '.join(skill_placeholders)}")

        agent_placeholders = find_scaffold_placeholders(agent_yaml_path)
        if agent_placeholders:
            errors.append(f"{agent_yaml_path}: unresolved scaffold placeholders present: {', '.join(agent_placeholders)}")

    if missing_agent_yaml:
        notes.append(f"Agent metadata is derivable and currently omitted for {len(missing_agent_yaml)} skill(s).")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("PASS")
    for note in notes:
        print(f"- {note}")
    return 0


def normalize_target_root(raw_target: str) -> Path:
    target = Path(raw_target.rstrip("/"))
    if target.name == "skills":
        return target.parent
    return target


def runtime_skill_names(skills_root: Path) -> List[str]:
    return [path.name for path in iter_skill_dirs(skills_root)]


def sync_named_file(src_root: Path, dest_root: Path, filename: str) -> None:
    src = src_root / filename
    dest = dest_root / filename
    if src.is_file():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    elif dest.exists():
        dest.unlink()


def sync_named_dir(src_root: Path, dest_root: Path, dirname: str) -> None:
    src = src_root / dirname
    dest = dest_root / dirname
    if src.is_dir():
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
    elif dest.exists():
        shutil.rmtree(dest)


def prune_stale_skill_dirs(skills_dest: Path, runtime_skills: List[str], keep_top_level_dirs: List[str]) -> None:
    keep = set(runtime_skills) | set(keep_top_level_dirs)
    if not skills_dest.exists():
        return
    for path in skills_dest.iterdir():
        if path.is_dir() and path.name not in keep:
            shutil.rmtree(path)


def prune_stale_top_level_skill_files(skills_dest: Path) -> None:
    keep = set(TOP_LEVEL_SKILL_FILES)
    if not skills_dest.exists():
        return
    for path in skills_dest.iterdir():
        if path.is_file() and path.name not in keep:
            path.unlink()


def write_manifest(path: Path, values: List[str]) -> None:
    path.write_text("".join(f"{value}\n" for value in values), encoding="utf-8")


def sync_rendered_agent_yaml(skills_root: Path, skills_dest: Path, name: str, entry: dict) -> None:
    rendered = build_expected_openai_yaml(skills_root, name, entry)
    agent_yaml_path = skills_dest / name / "agents" / "openai.yaml"
    agent_yaml_path.parent.mkdir(parents=True, exist_ok=True)
    agent_yaml_path.write_text(rendered, encoding="utf-8")


def command_sync(skills_root: Path, target_root: Path) -> int:
    target_root = normalize_target_root(str(target_root))
    skills_dest = target_root / "skills"
    docs_dest = target_root / "docs"
    skills_dest.mkdir(parents=True, exist_ok=True)

    direct_entries = direct_skill_entries(skills_root)
    runtime_skills = runtime_skill_names(skills_root)
    manifest_path = target_root / MANIFEST_FILE
    docs_manifest_path = target_root / DOCS_MANIFEST_FILE

    prune_stale_skill_dirs(skills_dest, runtime_skills, TOP_LEVEL_SKILL_DIRS)
    prune_stale_top_level_skill_files(skills_dest)

    for dirname in TOP_LEVEL_SKILL_DIRS:
        sync_named_dir(skills_root, skills_dest, dirname)
    for filename in TOP_LEVEL_SKILL_FILES:
        sync_named_file(skills_root, skills_dest, filename)
    for skill_name in runtime_skills:
        sync_named_dir(skills_root, skills_dest, skill_name)
        entry = direct_entries.get(skill_name)
        if entry is None:
            continue
        try:
            sync_rendered_agent_yaml(skills_root, skills_dest, skill_name, entry)
        except (KeyError, ValueError) as exc:
            print(f"Failed to render agent metadata for `{skill_name}`: {exc}", file=sys.stderr)
            return 1

    if docs_dest.exists():
        for name in LEGACY_DOC_FILES:
            stale = docs_dest / name
            if stale.exists():
                stale.unlink()
        if not any(docs_dest.iterdir()):
            docs_dest.rmdir()

    if docs_manifest_path.exists():
        docs_manifest_path.unlink()
    for legacy_manifest in LEGACY_MANIFEST_FILES:
        stale = target_root / legacy_manifest
        if stale.exists():
            stale.unlink()
    for legacy_docs_manifest in LEGACY_DOCS_MANIFEST_FILES:
        stale = target_root / legacy_docs_manifest
        if stale.exists():
            stale.unlink()

    write_manifest(manifest_path, sorted(runtime_skills))

    print(f"Synced composable-skills into {target_root}")
    print("Restart Codex to pick up updated skills.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Minimal skill runtime CLI.")
    parser.add_argument("--skills-root", default=str(SKILLS_ROOT), help="Path to skills root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="Validate direct metadata and runtime contracts.")
    sync_parser = sub.add_parser("sync", help="Sync the runtime surface to a target .agents root.")
    sync_parser.add_argument("target_root", help="Target .agents root or a path ending in /skills.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    skills_root = Path(args.skills_root).resolve()

    if args.command == "validate":
        return command_validate(skills_root)
    if args.command == "sync":
        return command_sync(skills_root, Path(args.target_root))

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
