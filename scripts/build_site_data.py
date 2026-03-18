#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
README_PATH = SKILLS_ROOT / "README.md"
OUTPUT_PATH = REPO_ROOT / "docs" / "data" / "skills.json"

LAYER_ORDER = {"workflow": 0, "atomic": 1, "control": 2}
FAMILY_ORDER = {
    "workflow": 0,
    "ask": 1,
    "clarify": 2,
    "analyze": 3,
    "plan": 4,
    "build": 5,
    "debug": 6,
    "test": 7,
    "review": 8,
    "tidy": 9,
    "doc": 10,
    "release": 11,
    "control": 12,
    "compose": 13,
    "commit": 14,
    "gemini": 15,
    "misc": 99,
}
LAYER_LABELS = {
    "workflow": {"en": "Workflow", "ko": "워크플로"},
    "atomic": {"en": "Atomic", "ko": "원자 스킬"},
    "control": {"en": "Control", "ko": "제어 스킬"},
}
FAMILY_INFO = {
    "workflow": {
        "label_en": "Workflow",
        "label_ko": "워크플로",
        "value_ko": "처음부터 끝까지 한 흐름으로 묶어 시작 비용을 줄인다.",
        "summary_ko": "한 번에 맡길 수 있는 기본 진입점이다.",
    },
    "ask": {
        "label_en": "Ask",
        "label_ko": "질문 설계",
        "value_ko": "흐린 생각을 바로 물을 수 있는 질문으로 바꾼다.",
        "summary_ko": "좋은 답을 얻기 전에, 좋은 질문부터 만든다.",
    },
    "clarify": {
        "label_en": "Clarify",
        "label_ko": "요구 명확화",
        "value_ko": "범위와 경계를 계약처럼 또렷하게 만든다.",
        "summary_ko": "어디까지가 이번 일인지 먼저 분명하게 만든다.",
    },
    "analyze": {
        "label_en": "Analyze",
        "label_ko": "분석",
        "value_ko": "판정 전에 구조와 근거를 먼저 드러낸다.",
        "summary_ko": "무엇이 있는지 지도로 펼쳐 본다.",
    },
    "plan": {
        "label_en": "Plan",
        "label_ko": "계획",
        "value_ko": "만들기 전에 구조와 검증 순서를 고정한다.",
        "summary_ko": "바로 손대지 않고 먼저 설계를 세운다.",
    },
    "build": {
        "label_en": "Build",
        "label_ko": "구현",
        "value_ko": "실제 변경을 만들고 검증 근거까지 남긴다.",
        "summary_ko": "생각이 아니라 실행을 담당한다.",
    },
    "debug": {
        "label_en": "Debug",
        "label_ko": "디버그",
        "value_ko": "현상에서 원인까지 좁혀 재현 가능한 수정으로 바꾼다.",
        "summary_ko": "느낌이 아니라 재현 가능한 실패로 다룬다.",
    },
    "test": {
        "label_en": "Test",
        "label_ko": "테스트",
        "value_ko": "다음 번 같은 문제를 막는 보호막을 만든다.",
        "summary_ko": "무엇을 지켜야 하는지부터 설계한다.",
    },
    "review": {
        "label_en": "Review",
        "label_ko": "리뷰",
        "value_ko": "좋아 보인다가 아니라 통과/보류 판단을 만든다.",
        "summary_ko": "위험과 품질을 명시적으로 판정한다.",
    },
    "tidy": {
        "label_en": "Tidy",
        "label_ko": "정리",
        "value_ko": "복잡함과 레거시를 덜어 같은 일을 더 단순하게 만든다.",
        "summary_ko": "군살을 줄여 이해와 유지 비용을 낮춘다.",
    },
    "doc": {
        "label_en": "Doc",
        "label_ko": "문서",
        "value_ko": "지식을 흩어 놓지 않고 구조화해 남긴다.",
        "summary_ko": "문서 표면과 수명주기를 함께 다룬다.",
    },
    "release": {
        "label_en": "Release",
        "label_ko": "릴리즈",
        "value_ko": "내보내도 되는지 근거로 점검한다.",
        "summary_ko": "출고 전 마지막 검증을 맡는다.",
    },
    "control": {
        "label_en": "Control",
        "label_ko": "제어",
        "value_ko": "반복과 종료 조건을 자동으로 밀어준다.",
        "summary_ko": "한 번이 아니라 끝날 때까지 실행한다.",
    },
    "compose": {
        "label_en": "Compose",
        "label_ko": "조립",
        "value_ko": "여러 스킬을 숨김 없이 한 체인으로 엮는다.",
        "summary_ko": "다중 스킬 실행 순서를 명시적으로 만든다.",
    },
    "commit": {
        "label_en": "Commit",
        "label_ko": "커밋",
        "value_ko": "끝난 변경의 의도를 짧고 정확하게 남긴다.",
        "summary_ko": "코드가 아니라 변경 설명을 다룬다.",
    },
    "gemini": {
        "label_en": "Gemini",
        "label_ko": "외부 조사",
        "value_ko": "외부 분석을 붙이되 로컬 근거와 분리해 비교한다.",
        "summary_ko": "명시 요청이 있을 때만 외부 분석을 붙인다.",
    },
    "misc": {
        "label_en": "Misc",
        "label_ko": "기타",
        "value_ko": "작은 보조 역할을 맡아 전체 흐름을 돕는다.",
        "summary_ko": "좁은 목적의 보조 스킬이다.",
    },
}


def normalize_remote_url(url: str) -> str:
    if url.startswith("git@github.com:"):
        return "https://github.com/" + url.removeprefix("git@github.com:").removesuffix(".git")
    if url.startswith("https://github.com/"):
        return url.removesuffix(".git")
    return "https://github.com/AxiomOrient/composable-skills"


def get_repo_url() -> str:
    try:
        raw = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
    except Exception:
        return "https://github.com/AxiomOrient/composable-skills"
    return normalize_remote_url(raw)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    marker = "\n---\n"
    end = text.find(marker, 4)
    if end == -1:
        return {}, text
    block = text[4:end]
    body = text[end + len(marker) :]
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta, body


def parse_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^## (.+)$", text, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[title] = text[start:end].strip()
    return sections


def parse_bullets(block: str) -> list[str]:
    bullets: list[str] = []
    current: list[str] = []
    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("- "):
            if current:
                bullets.append(" ".join(current).strip())
            current = [stripped[2:].strip()]
            continue
        if current and (line.startswith("  ") or line.startswith("\t")):
            current.append(stripped)
            continue
        if current and not stripped:
            bullets.append(" ".join(current).strip())
            current = []
    if current:
        bullets.append(" ".join(current).strip())
    return [clean_inline_markup(item) for item in bullets if item.strip()]


def clean_inline_markup(text: str) -> str:
    cleaned = re.sub(r"`([^`]+)`", r"\1", text)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def compact_paragraph(block: str) -> str:
    paragraph_lines: list[str] = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped:
            if paragraph_lines:
                break
            continue
        if stripped.startswith("- ") or stripped.startswith("```"):
            break
        paragraph_lines.append(stripped)
    return clean_inline_markup(" ".join(paragraph_lines))


def detect_layer(name: str) -> str:
    if name.startswith("workflow-"):
        return "workflow"
    if name.startswith("control-"):
        return "control"
    return "atomic"


def detect_family(name: str, layer: str) -> str:
    if layer == "workflow":
        return "workflow"
    if layer == "control":
        return "control"
    prefix = name.split("-", 1)[0]
    if prefix in FAMILY_INFO:
        return prefix
    return "misc"


def parse_readme_summaries() -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    text = README_PATH.read_text(encoding="utf-8")
    summary_map: dict[str, str] = {}
    quick_pick_map: dict[str, dict[str, str]] = {}

    bullet_pattern = re.compile(
        r"^- \[`(?P<name>[^`]+)`\]\(\./[^)]+\): (?P<summary>.+)$",
        flags=re.MULTILINE,
    )
    for match in bullet_pattern.finditer(text):
        summary_map[match.group("name")] = match.group("summary").strip()

    table_pattern = re.compile(
        r"^\| (?P<need>[^|]+?) \| \[`(?P<name>[^`]+)`\]\(\./[^)]+\) \| (?P<why>[^|]+?) \|$",
        flags=re.MULTILINE,
    )
    for match in table_pattern.finditer(text):
        quick_pick_map[match.group("name")] = {
            "need": match.group("need").strip(),
            "why": match.group("why").strip(),
        }
        summary_map.setdefault(match.group("name"), match.group("why").strip())

    inline_table_pattern = re.compile(
        r"^\| (?P<need>[^|]+?) \| `(?P<name>[^`]+)` \| (?P<required>[^|]+?) \| (?P<scope>[^|]+?) \| (?P<done>[^|]+?) \|$",
        flags=re.MULTILINE,
    )
    for match in inline_table_pattern.finditer(text):
        quick_pick_map.setdefault(
            match.group("name"),
            {"need": match.group("need").strip(), "why": match.group("done").strip()},
        )

    return summary_map, quick_pick_map


def build_skill_record(skill_path: Path, repo_url: str, summaries: dict[str, str], quick_picks: dict[str, dict[str, str]]) -> dict[str, object]:
    text = skill_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    sections = parse_sections(body)
    name = meta.get("name", skill_path.parent.name)
    layer = detect_layer(name)
    family = detect_family(name, layer)
    family_info = FAMILY_INFO[family]
    layer_info = LAYER_LABELS[layer]
    purpose = compact_paragraph(sections.get("Purpose", ""))
    use_when = parse_bullets(sections.get("Use When", ""))
    do_not_use_when = parse_bullets(sections.get("Do Not Use When", ""))
    expansion = [item.lstrip("$") for item in parse_bullets(sections.get("Expansion", ""))]
    summary_ko = summaries.get(name, "")
    quick_pick = quick_picks.get(name)
    source_path = skill_path.relative_to(REPO_ROOT).as_posix()
    return {
        "name": name,
        "description": meta.get("description", ""),
        "summaryKo": summary_ko,
        "purpose": purpose,
        "useWhen": use_when,
        "doNotUseWhen": do_not_use_when,
        "expansion": expansion,
        "layer": layer,
        "layerLabel": layer_info,
        "family": family,
        "familyInfo": family_info,
        "quickPick": quick_pick,
        "sourcePath": source_path,
        "sourceUrl": f"{repo_url}/blob/main/{source_path}",
        "missingContract": False,
        "sortKey": [LAYER_ORDER.get(layer, 99), FAMILY_ORDER.get(family, 99), name],
    }


def build_placeholder_record(skill_dir: Path, repo_url: str, summaries: dict[str, str], quick_picks: dict[str, dict[str, str]]) -> dict[str, object]:
    name = skill_dir.name
    layer = detect_layer(name)
    family = detect_family(name, layer)
    family_info = FAMILY_INFO[family]
    layer_info = LAYER_LABELS[layer]
    quick_pick = quick_picks.get(name)
    source_path = skill_dir.relative_to(REPO_ROOT).as_posix()
    return {
        "name": name,
        "description": "Contract file missing in repository snapshot.",
        "summaryKo": summaries.get(name, "현재 저장소 스냅샷에는 상세 계약 파일이 없다."),
        "purpose": "Contract file is missing in this repository snapshot.",
        "useWhen": [],
        "doNotUseWhen": [],
        "expansion": [],
        "layer": layer,
        "layerLabel": layer_info,
        "family": family,
        "familyInfo": family_info,
        "quickPick": quick_pick,
        "sourcePath": source_path,
        "sourceUrl": f"{repo_url}/tree/main/{source_path}",
        "missingContract": True,
        "sortKey": [LAYER_ORDER.get(layer, 99), FAMILY_ORDER.get(family, 99), name],
    }


def make_stats(skills: list[dict[str, object]]) -> dict[str, object]:
    by_layer: dict[str, int] = {}
    by_family: dict[str, int] = {}
    for skill in skills:
        by_layer[skill["layer"]] = by_layer.get(skill["layer"], 0) + 1
        by_family[skill["family"]] = by_family.get(skill["family"], 0) + 1

    family_cards = []
    for family, count in sorted(by_family.items(), key=lambda item: (FAMILY_ORDER.get(item[0], 99), item[0])):
        info = FAMILY_INFO.get(family, FAMILY_INFO["misc"])
        family_cards.append(
            {
                "family": family,
                "count": count,
                "labelEn": info["label_en"],
                "labelKo": info["label_ko"],
                "summaryKo": info["summary_ko"],
            }
        )

    return {
        "skillsCount": len(skills),
        "workflowCount": by_layer.get("workflow", 0),
        "atomicCount": by_layer.get("atomic", 0),
        "controlCount": by_layer.get("control", 0),
        "familyCards": family_cards,
    }


def main() -> None:
    repo_url = get_repo_url()
    summaries, quick_picks = parse_readme_summaries()
    skill_dirs = sorted(
        path
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and path.name not in {".system", "_meta"}
    )
    skills = []
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            skills.append(build_skill_record(skill_file, repo_url, summaries, quick_picks))
        else:
            skills.append(build_placeholder_record(skill_dir, repo_url, summaries, quick_picks))
    skills.sort(key=lambda item: item["sortKey"])
    for skill in skills:
        skill.pop("sortKey", None)

    payload = {
        "generatedFrom": "skills/*/SKILL.md + skills/README.md",
        "repoUrl": repo_url,
        "stats": make_stats(skills),
        "skills": skills,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)} ({len(skills)} skills)")


if __name__ == "__main__":
    main()
