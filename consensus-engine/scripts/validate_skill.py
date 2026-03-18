#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


REQUIRED_SECTIONS = [
    "## Purpose",
    "## When To Use",
    "## Core Workflow",
    "## Commands",
    "## Output Contract",
    "## Stop Conditions",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the consensus-engine skill package shape.",
    )
    parser.add_argument(
        "--skill-dir",
        default=".",
        help="Path to the skill root directory (default: current directory)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON output",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(markdown: str) -> Tuple[Dict[str, str], List[str]]:
    errors: List[str] = []
    if not markdown.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter"]
    parts = markdown.split("---", 2)
    if len(parts) < 3:
        return {}, ["SKILL.md frontmatter is not properly closed with ---"]
    raw = parts[1]
    data: Dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"Invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    for required in ("name", "description"):
        if not data.get(required):
            errors.append(f"Missing frontmatter field: {required}")
    return data, errors


def parse_openai_yaml(text: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for key in ("display_name", "short_description", "default_prompt"):
        match = re.search(rf"{key}\s*:\s*\"([^\"]+)\"", text)
        if match:
            result[key] = match.group(1)
            continue
        match = re.search(rf"{key}\s*:\s*(.+)", text)
        if match:
            result[key] = match.group(1).strip()
    return result


def validate(skill_dir: Path) -> Dict[str, object]:
    errors: List[str] = []
    warnings: List[str] = []

    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"

    if not skill_md.exists():
        errors.append("Missing SKILL.md")
    if not openai_yaml.exists():
        errors.append("Missing agents/openai.yaml")

    frontmatter = {}
    if skill_md.exists():
        text = read_text(skill_md)
        frontmatter, fm_errors = parse_frontmatter(text)
        errors.extend(fm_errors)

        expected_name = skill_dir.resolve().name
        if frontmatter.get("name") and frontmatter["name"] != expected_name:
            errors.append(
                f'Frontmatter name "{frontmatter["name"]}" does not match directory "{expected_name}"'
            )

        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"Missing section: {section}")

        if "## When Not To Use" not in text:
            warnings.append("Recommended section missing: ## When Not To Use")
        if "## Input Contract" not in text:
            warnings.append("Recommended section missing: ## Input Contract")

    ui = {}
    if openai_yaml.exists():
        ui = parse_openai_yaml(read_text(openai_yaml))
        for field in ("display_name", "short_description", "default_prompt"):
            if not ui.get(field):
                errors.append(f"Missing openai.yaml field: interface.{field}")
        default_prompt = ui.get("default_prompt", "")
        if "$consensus-engine" not in default_prompt:
            warnings.append("default_prompt should explicitly reference $consensus-engine")

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.glob("*.py"):
            text = read_text(script)
            if not text.startswith("#!/usr/bin/env python3"):
                errors.append(f"{script.name} must start with #!/usr/bin/env python3")

    return {
        "status": "ok" if not errors else "error",
        "skill_dir": str(skill_dir.resolve()),
        "frontmatter": frontmatter,
        "interface": ui,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    args = parse_args()
    result = validate(Path(args.skill_dir))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[{result['status'].upper()}] {result['skill_dir']}")
        if result["errors"]:
            print("Errors:")
            for item in result["errors"]:
                print(f"  - {item}")
        if result["warnings"]:
            print("Warnings:")
            for item in result["warnings"]:
                print(f"  - {item}")

    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
