#!/usr/bin/env python3
"""Macro composition parser for Fusion skills.

Converts expressions like:
  $scout-structure-map + $plan-task-breakdown + $build-write-code + $check-final-verify + [extra context] + @/abs/path/plan.md
into a normalized Fusion PROGRAM.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from difflib import get_close_matches
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

STAGE_ORDER = [
    "preflight",
    "detect",
    "analyze",
    "plan",
    "implement",
    "verify",
    "review",
    "reflect",
    "handoff",
    "audit",
]

POLICY_PRIORITY = [
    "safety-gates",
    "deterministic-output",
    "response-contract",
    "evidence",
    "approval-gates",
    "quality-gates",
    "perf-aware",
    "correctness-first",
]

COMPLETION_CONTROL_SKILLS = {"build-until-done", "finish-until-done", "check-improve-loop"}
ROUTING_SKIP_SKILLS = {"compose", "check-final-verify"}
DEFAULT_PLAN_DOC_PATHS = {"plans/IMPLEMENTATION-PLAN.md", "plans/TASKS.md"}

LEGACY_SKILL_GUIDANCE: Dict[str, str] = {}

FALLBACK_SKILL_RESPONSE_PROFILE_MAP: Dict[str, str] = {
    "compose": "generic",
    "build-until-done": "analysis_report",
    "scout-structure-map": "analysis_report",
    "finish-until-done": "analysis_report",
    "check-improve-loop": "analysis_report",
    "test-run-user-scenarios": "analysis_report",
    "debug-map-impact": "analysis_report",
    "tidy-why-complex": "analysis_report",
    "scout-scope": "clarify_question",
    "doc-write": "documentation_report",
    "doc-build-index": "documentation_report",
    "doc-publish-readme": "documentation_report",
    "doc-curate": "documentation_report",
    "doc-find-all": "documentation_report",
    "plan-task-breakdown": "planning_doc",
    "plan-why-build-this": "brief_contract",
    "plan-screen-map": "ia_contract",
    "scout-boundaries": "planning_doc",
    "plan-dependency-rules": "planning_doc",
    "plan-verify-order": "planning_doc",
    "tidy-cut-fat": "planning_doc",
    "tidy-reorganize": "planning_doc",
    "build-write-code": "implementation_delta",
    "plan-sync-tasks": "implementation_delta",
    "check-final-verify": "self_verify_report",
    "check-release-risk": "review_findings",
    "check-merge-ready": "review_findings",
    "check-quality-scan": "review_findings",
    "debug-find-root-cause": "debug_report",
    "build-make-faster": "performance_report",
    "scout-baseline": "performance_report",
    "test-write-guards": "test_report",
    "test-design-cases": "test_report",
    "check-security-holes": "security_report",
    "workflow-security-preflight": "security_report",
    "release-check-repo": "analysis_report",
    "release-check-hygiene": "analysis_report",
    "release-verdict": "release_decision",
    "release-publish": "generic",
    "tidy-find-magic-numbers": "review_findings",
    "tidy-find-copies": "review_findings",
    "check-module-bounds": "review_findings",
    "check-failure-paths": "review_findings",
    "test-find-gaps": "review_findings",
    "plan-what-it-does": "spec_contract",
    "plan-how-to-build": "design_contract",
    "commit-write-message": "commit_proposal",
    "ask-form-question": "clarify_question",
    "ask-break-it-down": "question_stack",
    "ask-flip-assumption": "analysis_report",
    "ask-fix-prompt": "repair_report",
    "workflow-ask-get-clear": "question_stack",
    "workflow-ask-sharpen": "question_stack",
    "workflow-check-full-review": "review_findings",
    "workflow-check-with-checklist": "review_findings",
    "workflow-debug-this": "debug_report",
    "workflow-scout-structure": "analysis_report",
    "workflow-plan-build-ready": "planning_doc",
    "workflow-build-implement-and-guard": "implementation_delta",
    "workflow-test-close-gaps": "test_report",
    "workflow-doc-systemize": "documentation_report",
    "workflow-tidy-find-improvements": "analysis_report",
    "workflow-security-preflight": "security_report",
    "workflow-release-publish": "generic",
    "workflow-release-ready-check": "release_decision",
    "gemini": "external_verification",
}

FALLBACK_PROFILE_REQUIRED_SECTIONS: Dict[str, List[str]] = {
    "generic": ["결과", "근거", "다음에 할 것", "질문(필요 시, 항상 맨 마지막)"],
    "analysis_report": ["결과", "핵심 발견", "옵션 비교", "근거", "다음에 할 것"],
    "question_stack": ["결과", "문제 정의", "핵심 질문", "세부 질문", "다음에 할 것"],
    "repair_report": ["결과", "실패 유형", "왜 틀렸는지", "최소 질문 수정", "다음에 할 것"],
    "self_verify_report": ["결과", "막힌 것 또는 수정 필요 항목", "검증 근거", "남은 위험", "다음에 할 것(필요 시)"],
    "documentation_report": ["결과", "프로젝트 개요", "아키텍처", "설치/실행", "사용 예시", "문서 경로", "근거"],
    "clarify_question": ["결과", "잠정 요구사항", "근거", "다음에 할 것", "확인 질문(맨 마지막)"],
    "brief_contract": ["결과", "브리프 요약", "대상 사용자와 문제", "성공 신호와 비목표", "열린 가정", "근거"],
    "ia_contract": ["결과", "구조 요약", "계층 구조", "탐색 경로와 흐름", "라벨링 메모", "근거"],
    "spec_contract": ["결과", "스펙 요약", "완료 조건 체크리스트", "근거"],
    "design_contract": ["결과", "설계 요약", "경계와 흐름", "결정과 트레이드오프", "위험과 검증", "근거"],
    "planning_doc": ["결과", "계획 요약", "할 일 목록", "문서 경로", "근거", "다음에 할 것"],
    "implementation_delta": ["결과", "변경 사항", "영향 및 위험", "검증 결과", "다음에 할 것"],
    "review_findings": ["결과", "발견된 문제", "테스트가 부족한 부분", "판정", "다음에 할 것"],
    "debug_report": ["결과", "원인 분석", "수정 내용", "재발 방지", "다음에 할 것"],
    "performance_report": ["결과", "성능 수치 (전/후)", "병목 분석 및 수정", "위험", "다음에 할 것"],
    "test_report": ["결과", "추가/수정 테스트", "커버리지 영향", "근거"],
    "security_report": ["결과", "취약점 목록", "위험도", "대응 우선순위", "다음에 할 것(발견 시에만)"],
    "release_decision": ["결과", "릴리즈 가능 여부와 이유", "위험 및 복구 방법", "승인 필요사항", "다음에 할 것(NO-GO 시에만)"],
    "commit_proposal": ["결과", "커밋 타입/메시지", "대안", "근거"],
    "external_verification": ["결과", "외부 검증 결과", "신뢰도 및 한계", "근거", "다음에 할 것"],
}

FALLBACK_VALID_LENSES: Set[str] = {
    "default",
    "debug-find-root-cause",
    "plan",
    "ux",
    "check-security-holes",
    "hickey-carmack",
    "ive",
    "feynman",
    "sinek-miller",
    "eisenhower",
    "uncle-bob",
    "karpathy",
    "kent-beck",
    "nielsen-norman",
    "wardley",
    "ries-lean",
    "christensen-jtbd",
    "shape-up",
    "sre-dora",
    "aws-well-architected",
    "nist-rmf",
    "goldratt-toc",
    "ideo-design-thinking",
    "fowler-strangler",
    "minto-pyramid",
    "kahneman-tversky",
    "kuhn-paradigm",
    "popper-falsification",
    "inversion-focus",
    "release-gatekeeper",
    "feynman-teaching",
    "contract-evidence-verifier",
}


def is_doclike_input(path: str) -> bool:
    lowered = path.strip().lower()
    return lowered.endswith(".md") or lowered == "docs" or lowered.startswith("docs/")


def infer_plan_artifact_role(path: str) -> Optional[str]:
    lowered_name = Path(path).name.lower()
    if "task" in lowered_name or "backlog" in lowered_name:
        return "tasks"
    if "plan" in lowered_name:
        return "plan"

    try:
        preview = Path(path).read_text(encoding="utf-8")[:2000].lower()
    except OSError:
        return None

    if "tasks backlog" in preview or "| id | 상태 | 작업 |" in preview:
        return "tasks"
    if "implementation master plan" in preview or "implementation plan" in preview:
        return "plan"
    return None


VALID_LENSES = set(FALLBACK_VALID_LENSES)
SKILL_RESPONSE_PROFILE_MAP = dict(FALLBACK_SKILL_RESPONSE_PROFILE_MAP)
PROFILE_REQUIRED_SECTIONS_MAP = dict(FALLBACK_PROFILE_REQUIRED_SECTIONS)
VALID_OUTPUTS = {"md(contract=v1)", "json(schema=v1)", "both"}
VALID_SCOPES = {"repo", "diff"}
PER_SKILL_META_FILE = "skill.json"
DIRECT_META_DIR = "_meta"
DIRECT_LENSES_FILE = "lenses.json"


def load_json_file(path: Path, label: str) -> Tuple[Optional[dict], List[str]]:
    if not path.exists():
        return None, []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - parser should degrade gracefully
        return None, [f"Failed to load {label} `{path}`: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{label} `{path}` must be a JSON object."]
    return data, []


def load_direct_skill_metadata(skills_root: Path) -> Tuple[Dict[str, dict], List[str]]:
    entries: Dict[str, dict] = {}
    warnings: List[str] = []
    try:
        for path in skills_root.iterdir():
            if not path.is_dir() or path.name.startswith("."):
                continue
            if path.name == DIRECT_META_DIR:
                continue
            meta_path = path / PER_SKILL_META_FILE
            if not meta_path.exists():
                continue
            data, load_warnings = load_json_file(meta_path, "Skill metadata")
            warnings.extend(load_warnings)
            if data is None:
                continue
            declared_name = data.get("name")
            if isinstance(declared_name, str) and declared_name and declared_name != path.name:
                warnings.append(
                    f"Skill metadata `{meta_path}` has name `{declared_name}` but lives under `{path.name}`; using directory name."
                )
            entry = dict(data)
            entry["name"] = path.name
            entries[path.name] = entry
    except OSError as exc:
        warnings.append(f"Failed to scan direct skill metadata under `{skills_root}`: {exc}")
    return entries, warnings


def all_skill_dirs_have_direct_metadata(skills_root: Path, direct_entries: Dict[str, dict]) -> bool:
    try:
        expected = {
            path.name
            for path in skills_root.iterdir()
            if path.is_dir()
            and not path.name.startswith(".")
            and path.name != DIRECT_META_DIR
            and (path / "SKILL.md").exists()
        }
    except OSError:
        return False
    return bool(expected) and expected == set(direct_entries)


def load_direct_lens_ids(skills_root: Path) -> Tuple[Optional[Set[str]], List[str]]:
    path = skills_root / DIRECT_META_DIR / DIRECT_LENSES_FILE
    data, warnings = load_json_file(path, "Direct lens metadata")
    if data is None:
        return None, warnings

    parsed: Set[str] = set()
    valid_ids = data.get("valid_ids")
    if isinstance(valid_ids, list):
        parsed.update(item for item in valid_ids if isinstance(item, str) and item)

    lenses = data.get("lenses")
    if isinstance(lenses, list):
        for item in lenses:
            if not isinstance(item, dict):
                continue
            lens_id = item.get("id")
            if isinstance(lens_id, str) and lens_id:
                parsed.add(lens_id)

    if not parsed:
        return None, warnings + [f"Direct lens metadata `{path}` does not contain valid lens ids."]
    return parsed, warnings


def register_skill_metadata(metadata: "RuntimeMetadata", name: str, entry: dict, *, overwrite: bool) -> None:
    if not overwrite and name in metadata.skill_metadata:
        return

    metadata.skill_names.add(name)
    metadata.skill_metadata[name] = dict(entry)

    response_profile = entry.get("response_profile")
    if isinstance(response_profile, str) and response_profile:
        metadata.skill_response_profile_map[name] = response_profile

    default_program = entry.get("default_program")
    if isinstance(default_program, str) and default_program.strip():
        metadata.default_program_map[name] = default_program.strip()

    expands_to = entry.get("expands_to")
    if entry.get("layer") == "workflow" and isinstance(expands_to, list) and expands_to:
        metadata.workflow_registry[name] = {
            "name": name,
            "expands_to": list(expands_to),
            "default_program": default_program,
        }


def build_runtime_metadata(skills_root: Path) -> RuntimeMetadata:
    metadata = RuntimeMetadata(
        valid_lenses=set(VALID_LENSES),
        skill_response_profile_map=dict(SKILL_RESPONSE_PROFILE_MAP),
        profile_required_sections_map={
            profile_id: list(sections) for profile_id, sections in PROFILE_REQUIRED_SECTIONS_MAP.items()
        },
    )

    direct_entries, direct_warnings = load_direct_skill_metadata(skills_root)
    metadata.warnings.extend(direct_warnings)
    for name, entry in direct_entries.items():
        register_skill_metadata(metadata, name, entry, overwrite=True)

    direct_metadata_complete = all_skill_dirs_have_direct_metadata(skills_root, direct_entries)

    direct_lenses, direct_lens_warnings = load_direct_lens_ids(skills_root)
    metadata.warnings.extend(direct_lens_warnings)
    if direct_lenses:
        metadata.valid_lenses = direct_lenses

    if direct_metadata_complete and direct_lenses:
        try:
            for path in skills_root.iterdir():
                if not path.is_dir() or path.name.startswith("."):
                    continue
                if path.name == DIRECT_META_DIR:
                    continue
                if (path / "SKILL.md").exists():
                    metadata.skill_names.add(path.name)
        except OSError:
            pass
        return metadata

    try:
        for path in skills_root.iterdir():
            if not path.is_dir() or path.name.startswith("."):
                continue
            if path.name == DIRECT_META_DIR:
                continue
            if (path / "SKILL.md").exists():
                metadata.skill_names.add(path.name)
    except OSError:
        pass

    return metadata


def expand_workflow_skills(skills: List[str], workflow_registry: Dict[str, dict]) -> Tuple[List[str], List[str]]:
    warnings: List[str] = []
    expanded: List[str] = []
    expansion_cache: Dict[str, List[str]] = {}

    def expand_one(skill: str, stack: List[str]) -> List[str]:
        if skill not in workflow_registry:
            if skill.startswith("workflow-"):
                raise ValueError(
                    f"Workflow metadata missing for `${skill}`. Add `skills/{skill}/{PER_SKILL_META_FILE}` so workflow expansion can run."
                )
            return [skill]
        if skill in expansion_cache:
            return list(expansion_cache[skill])
        if skill in stack:
            cycle = " -> ".join(stack + [skill])
            raise ValueError(f"Workflow cycle detected: {cycle}")

        entry = workflow_registry[skill]
        stack.append(skill)
        flattened: List[str] = []
        for raw in entry.get("expands_to", []):
            target = raw[1:] if isinstance(raw, str) and raw.startswith("$") else raw
            if not isinstance(target, str) or not target:
                raise ValueError(f"Workflow `{skill}` has invalid expands_to token: {raw}")
            flattened.extend(expand_one(target, stack))
        stack.pop()
        expansion_cache[skill] = list(flattened)
        warnings.append(
            f"Expanded workflow `${skill}` -> " + " + ".join(f"${name}" for name in flattened)
        )
        return list(flattened)

    for skill in skills:
        expanded.extend(expand_one(skill, []))
    return expanded, warnings


def collapse_duplicate_skills(skills: List[str]) -> Tuple[List[str], List[str]]:
    warnings: List[str] = []
    collapsed: List[str] = []
    seen: Set[str] = set()

    for skill in skills:
        if skill in seen:
            warnings.append(f"Collapsed duplicate skill `${skill}` after workflow expansion.")
            continue
        seen.add(skill)
        collapsed.append(skill)
    return collapsed, warnings


@dataclass
class Program:
    stages: List[str] = field(default_factory=list)
    policy: List[str] = field(default_factory=list)
    lens: Optional[str] = None
    scope: Optional[str] = None
    output: Optional[str] = None


@dataclass
class RuntimeMetadata:
    valid_lenses: Set[str] = field(default_factory=set)
    skill_response_profile_map: Dict[str, str] = field(default_factory=dict)
    profile_required_sections_map: Dict[str, List[str]] = field(default_factory=dict)
    workflow_registry: Dict[str, dict] = field(default_factory=dict)
    default_program_map: Dict[str, str] = field(default_factory=dict)
    skill_metadata: Dict[str, dict] = field(default_factory=dict)
    skill_names: Set[str] = field(default_factory=set)
    warnings: List[str] = field(default_factory=list)


@dataclass
class MacroParse:
    skills: List[str] = field(default_factory=list)
    lens: Optional[str] = None
    approval: Optional[str] = None
    scope: Optional[str] = None
    output: Optional[str] = None
    policy: List[str] = field(default_factory=list)
    docs: List[str] = field(default_factory=list)
    prompt_tail: Optional[str] = None
    unknown: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def split_top_level_csv(text: str) -> List[str]:
    out: List[str] = []
    cur: List[str] = []
    depth = 0
    for ch in text:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            tok = "".join(cur).strip()
            if tok:
                out.append(tok)
            cur = []
            continue
        cur.append(ch)
    tok = "".join(cur).strip()
    if tok:
        out.append(tok)
    return out


def extract_default_program_block(skill_path: Path) -> str:
    try:
        content = skill_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Failed to read skill file {skill_path}: {exc}") from exc
    m = re.search(r"##\s+Default\s+Program\s*\n```text\n(.*?)\n```", content, flags=re.S)
    if not m:
        raise ValueError(f"Default Program block not found in {skill_path}")
    return m.group(1).strip()


def parse_program_block(block: str) -> Program:
    one = " ".join(line.strip() for line in block.splitlines() if line.strip())
    one = one.strip()
    if not (one.startswith("[") and one.endswith("]")):
        raise ValueError(f"Invalid PROGRAM block: {one}")
    body = one[1:-1].strip()

    p = Program()
    # Split only on top-level field separators (" | "), not on scope unions like "repo|diff|paths(...)"
    parts = [x.strip() for x in re.split(r"\s+\|\s+", body) if x.strip()]
    for part in parts:
        if ":" not in part:
            continue
        key, val = part.split(":", 1)
        key = key.strip()
        val = val.strip()
        if key == "stages":
            stages = [s for s in val.replace(" ", "").split(">") if s]
            stages = [re.sub(r"@panel\([^)]*\)", "", s) for s in stages]
            p.stages = [s for s in stages if s]
        elif key == "policy":
            p.policy = split_top_level_csv(val.replace(" ", ""))
        elif key == "lens":
            p.lens = val
        elif key == "scope":
            p.scope = val
        elif key == "output":
            p.output = val

    return p


def tokenize_macro_expr(expr: str, allow_bracket_grouping: bool = True) -> List[str]:
    stripped = expr.strip()
    if not stripped:
        return []

    if not allow_bracket_grouping:
        # Fallback mode for malformed bracket input.
        return [t for t in re.split(r"\s*\+\s*|\s+", stripped) if t]

    # Split on top-level separators only.
    # - `+` and whitespace are equivalent separators at depth 0.
    # - Inside bracket prompt blocks (`[...]`), keep raw content as one token.
    # - Escaped separators (e.g. `\+`) are preserved.
    out: List[str] = []
    cur: List[str] = []
    depth = 0
    paren_depth = 0
    escaped = False

    for ch in stripped:
        if escaped:
            cur.append(ch)
            escaped = False
            continue

        if ch == "\\":
            cur.append(ch)
            escaped = True
            continue

        if ch == "[":
            depth += 1
            cur.append(ch)
            continue
        if ch == "]" and depth > 0:
            depth -= 1
            cur.append(ch)
            continue

        if depth == 0 and ch == "(":
            paren_depth += 1
            cur.append(ch)
            continue
        if depth == 0 and ch == ")" and paren_depth > 0:
            paren_depth -= 1
            cur.append(ch)
            continue

        if depth == 0 and paren_depth == 0 and (ch.isspace() or ch == "+"):
            tok = "".join(cur).strip()
            if tok:
                out.append(tok)
            cur = []
            continue

        cur.append(ch)

    tok = "".join(cur).strip()
    if tok:
        out.append(tok)
    return out


def _scan_bracket_balance(text: str) -> Tuple[bool, bool]:
    depth = 0
    escaped = False
    extra_closing = False

    for ch in text:
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == "[":
            depth += 1
            continue
        if ch == "]":
            if depth == 0:
                extra_closing = True
            else:
                depth -= 1
    return depth != 0, extra_closing


def _is_valid_bracket_prompt_token(token: str) -> bool:
    if len(token) < 2 or not (token.startswith("[") and token.endswith("]")):
        return False

    depth = 0
    escaped = False
    last_index = len(token) - 1
    for i, ch in enumerate(token):
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == "[":
            depth += 1
            continue
        if ch == "]":
            depth -= 1
            if depth < 0:
                return False
            # A full bracket token should close at the last character.
            if depth == 0 and i != last_index:
                return False
    return depth == 0


def _unescape_macro_text(text: str) -> str:
    out: List[str] = []
    escaped = False
    for ch in text:
        if escaped:
            out.append(ch)
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        out.append(ch)
    if escaped:
        out.append("\\")
    return "".join(out)


def _decode_bracket_prompt_token(token: str) -> str:
    # Token validity is checked before calling this helper.
    inner = token[1:-1]
    return _unescape_macro_text(inner).strip()


def _looks_like_doc_path(path_token: str) -> bool:
    if not path_token or any(ch.isspace() for ch in path_token):
        return False
    if path_token in {".", "..", "/"}:
        return False
    if path_token.startswith("$"):
        return False

    # Any non-space token after '@' is treated as an explicit scope path token.
    # This enables forms like: $tidy-cut-fat + @src + [custom prompt]
    return True


def parse_macro_expr(expr: str) -> MacroParse:
    m = MacroParse()
    unclosed_bracket, extra_closing_bracket = _scan_bracket_balance(expr)
    if unclosed_bracket:
        m.warnings.append(
            "Detected unclosed bracket prompt block (`[` without matching `]`); "
            "parsed in fallback token mode."
        )
    if extra_closing_bracket:
        m.warnings.append(
            "Detected unmatched closing bracket (`]`) in macro; treated as plain text."
        )

    tokens = tokenize_macro_expr(expr, allow_bracket_grouping=not unclosed_bracket)
    prompt_tail_parts: List[str] = []

    for tok in tokens:
        if tok.startswith("$"):
            skill = tok[1:].strip().lower()
            m.skills.append(skill)
            continue

        low = tok.lower()
        if low.startswith("lens:"):
            m.lens = tok.split(":", 1)[1].strip().lower()
            continue
        if low.startswith("scope:"):
            m.scope = tok.split(":", 1)[1].strip()
            continue
        if low.startswith("output:"):
            m.output = tok.split(":", 1)[1].strip()
            continue
        if low.startswith("policy:"):
            payload = tok.split(":", 1)[1].strip()
            m.policy.extend(split_top_level_csv(payload))
            continue
        if low.startswith("approval:"):
            mode = tok.split(":", 1)[1].strip().lower()
            if mode in {"explicit", "required", "ask", "ask-first", "strict"}:
                m.approval = "explicit"
                m.policy.append("approval-gates{explicit,no-fallback}")
                continue
            m.unknown.append(tok)
            continue

        if _is_valid_bracket_prompt_token(tok):
            content = _decode_bracket_prompt_token(tok)
            if content:
                prompt_tail_parts.append(content)
            continue

        if tok.startswith("@"):
            candidate = tok[1:]
            if _looks_like_doc_path(candidate):
                m.docs.append(candidate)
            else:
                m.unknown.append(tok)
            continue
        if tok.endswith((".md", ".markdown")) and _looks_like_doc_path(tok):
            m.docs.append(tok)
            continue

        if m.skills:
            prompt_tail_parts.append(_unescape_macro_text(tok))
            continue

        m.unknown.append(tok)

    if prompt_tail_parts:
        m.prompt_tail = " ".join(part for part in prompt_tail_parts if part).strip()

    return m


def merge_quality_gates(policies: List[str]) -> List[str]:
    gates: List[str] = []
    other: List[str] = []

    for p in policies:
        mm = re.match(r"^quality-gates\{([^}]*)\}$", p)
        if mm:
            gates.extend([g for g in mm.group(1).split(",") if g])
        else:
            other.append(p)

    if gates:
        uniq = sorted(set(gates), key=lambda x: ["tests", "check-security-holes", "compat", "docs", "style"].index(x) if x in {"tests", "check-security-holes", "compat", "docs", "style"} else 999)
        other.append(f"quality-gates{{{','.join(uniq)}}}")

    return other


def sort_policies(policies: List[str]) -> List[str]:
    policies = merge_quality_gates(policies)
    policies = merge_approval_gates(policies)
    policies = merge_response_contract(policies)
    seen = []
    for p in policies:
        if p not in seen:
            seen.append(p)

    def pri(p: str) -> int:
        if p.startswith("quality-gates{"):
            base = "quality-gates"
        elif p.startswith("approval-gates{"):
            base = "approval-gates"
        elif p.startswith("response-contract{"):
            base = "response-contract"
        else:
            base = p
        try:
            return POLICY_PRIORITY.index(base)
        except ValueError:
            return 999

    return sorted(seen, key=pri)


def parse_scope_value(scope: str) -> Tuple[str, List[str]]:
    s = scope.strip()
    if s in {"repo|diff|paths(glob,...)", "repo|diff|paths(glob,...)"}:
        return "any", []
    if "|" in s:
        parts = [p.strip() for p in s.split("|") if p.strip()]
        allowed = {"repo", "diff", "paths(glob,...)", "paths(glob,...)"}  # tolerate docs variants
        if parts and all(p in allowed for p in parts):
            return "any", []
        raise ValueError(f"Invalid scope: {scope}")
    if s in VALID_SCOPES:
        return s, []
    mm = re.match(r"^paths\((.*)\)$", s)
    if mm:
        raw = mm.group(1).strip()
        if not raw:
            return "paths", []
        return "paths", split_top_level_csv(raw)
    raise ValueError(f"Invalid scope: {scope}")


def merge_approval_gates(policies: List[str]) -> List[str]:
    options: List[str] = []
    other: List[str] = []
    order = ["explicit", "no-fallback"]

    for p in policies:
        mm = re.match(r"^approval-gates\{([^}]*)\}$", p)
        if mm:
            options.extend([g for g in mm.group(1).split(",") if g])
        else:
            other.append(p)

    if options:
        uniq = sorted(set(options), key=lambda x: order.index(x) if x in order else 999)
        other.append(f"approval-gates{{{','.join(uniq)}}}")

    return other


def merge_response_contract(policies: List[str]) -> List[str]:
    options: List[str] = []
    other: List[str] = []
    order = ["plain-korean", "feynman-clear", "actionable", "core-first", "short-sentences", "plain-words", "concrete-details"]

    for p in policies:
        mm = re.match(r"^response-contract\{([^}]*)\}$", p)
        if mm:
            options.extend([g for g in mm.group(1).split(",") if g])
        else:
            other.append(p)

    if options:
        uniq = sorted(set(options), key=lambda x: order.index(x) if x in order else 999)
        other.append(f"response-contract{{{','.join(uniq)}}}")

    return other


def suggest_skill_name(unknown_skill: str, skills_root: Path, known_skill_names: Optional[Set[str]] = None) -> Optional[str]:
    if unknown_skill in LEGACY_SKILL_GUIDANCE:
        return None
    candidates: List[str] = []
    try:
        if known_skill_names:
            candidates.extend(name for name in known_skill_names if isinstance(name, str))
        for p in skills_root.iterdir():
            if not p.is_dir():
                continue
            if p.name.startswith(".") or p.name == DIRECT_META_DIR:
                continue
            if (p / "SKILL.md").exists():
                candidates.append(p.name)
    except OSError:
        return None
    except Exception:
        pass
    matches = get_close_matches(unknown_skill, sorted(candidates), n=1, cutoff=0.6)
    return matches[0] if matches else None


def resolve_lens_source(
    macro: MacroParse,
    effective_skills: List[str],
    workflow_lens_map: Dict[str, str],
    skill_lens_map: Dict[str, str],
    out: Program,
    skill_response_profile_map: Dict[str, str],
) -> str:
    if macro.lens:
        return "explicit-override"
    primary_skill = select_primary_skill(effective_skills, skill_response_profile_map)
    if primary_skill in workflow_lens_map:
        return "workflow-default"
    if primary_skill in skill_lens_map:
        return "atomic-default"
    if out.lens:
        return "fallback-default"
    return "fallback-default"


def compose_program(
    macro: MacroParse,
    skills_root: Path,
    runtime_metadata: RuntimeMetadata,
) -> Tuple[Program, List[str], List[str], List[str], str]:
    warnings: List[str] = list(macro.warnings)
    warnings.extend(runtime_metadata.warnings)
    if macro.unknown:
        raise ValueError(f"Unknown macro token(s): {macro.unknown}")

    if not macro.skills:
        raise ValueError("Macro must include at least one $skill token")

    effective_skills: List[str] = list(macro.skills)

    workflow_registry = runtime_metadata.workflow_registry
    expanded_skills, expansion_warnings = expand_workflow_skills(effective_skills, workflow_registry)
    warnings.extend(expansion_warnings)
    expanded_skills, dedupe_warnings = collapse_duplicate_skills(expanded_skills)
    warnings.extend(dedupe_warnings)

    resolved: List[Program] = []
    skill_lens_map: Dict[str, str] = {}
    workflow_lens_map: Dict[str, str] = {}
    has_non_compose_skill = any(s != "compose" for s in expanded_skills)
    for skill, entry in workflow_registry.items():
        block = entry.get("default_program")
        if not isinstance(block, str) or not block.strip():
            continue
        try:
            prog = parse_program_block(block.strip())
        except ValueError:
            continue
        if prog.lens:
            workflow_lens_map[skill] = prog.lens
    for s in expanded_skills:
        # Compose acts as an orchestration entrypoint. When other skills are explicitly provided,
        # do not combine compose's own default program into the merged program.
        if s == "compose" and has_non_compose_skill:
            continue

        skill_file = skills_root / s / "SKILL.md"
        if not skill_file.exists():
            legacy_guidance = LEGACY_SKILL_GUIDANCE.get(s)
            if legacy_guidance:
                raise ValueError(f"Unknown skill: ${s}. {legacy_guidance}")
            suggestion = suggest_skill_name(s, skills_root, runtime_metadata.skill_names)
            if suggestion:
                raise ValueError(f"Unknown skill: ${s}. Did you mean ${suggestion}?")
            raise ValueError(f"Unknown skill: ${s}")
        block = runtime_metadata.default_program_map.get(s)
        if block is None:
            block = extract_default_program_block(skill_file)
        prog = parse_program_block(block)
        resolved.append(prog)
        if prog.lens:
            skill_lens_map[s] = prog.lens

    out = Program()

    scope_candidates: List[str] = []
    output_candidates: List[str] = []
    lens_candidates: List[str] = []

    for p in resolved:
        out.stages.extend(p.stages)
        out.policy.extend(p.policy)
        if p.scope:
            scope_candidates.append(p.scope)
        if p.output:
            output_candidates.append(p.output)
        if p.lens:
            lens_candidates.append(p.lens)

    out.policy.extend(macro.policy)

    # stage canonical ordering
    stage_set = set([s for s in out.stages if s])
    out.stages = [s for s in STAGE_ORDER if s in stage_set]

    # lens precedence
    if macro.lens:
        if macro.lens not in runtime_metadata.valid_lenses:
            raise ValueError(f"Invalid lens: {macro.lens}")
        out.lens = macro.lens
    elif not out.lens:
        primary_skill = select_primary_skill(effective_skills, runtime_metadata.skill_response_profile_map)
        if primary_skill in workflow_lens_map:
            out.lens = workflow_lens_map[primary_skill]
        elif primary_skill in skill_lens_map:
            out.lens = skill_lens_map[primary_skill]
        elif lens_candidates:
            out.lens = lens_candidates[0]
    if not out.lens:
        out.lens = "hickey-carmack"

    # scope precedence
    if macro.scope:
        parse_scope_value(macro.scope)  # validate
        out.scope = macro.scope
    elif macro.docs:
        # Keep explicit macro docs primary, but preserve path-level constraints from skill scopes.
        macro_doc_paths = list(macro.docs)
        scoped_paths: List[str] = []
        for sc in scope_candidates:
            mode, globs = parse_scope_value(sc)
            if mode == "paths":
                scoped_paths.extend(globs)
        if "plan-sync-tasks" in effective_skills and macro_doc_paths:
            scoped_paths = [path for path in scoped_paths if path not in DEFAULT_PLAN_DOC_PATHS]
        merged = sorted(set(macro_doc_paths + scoped_paths))
        out.scope = f"paths({','.join(merged)})"
    else:
        # Documentation flows should default to repo-wide context when scope is omitted.
        # This avoids under-scoped README/architecture output caused by diff-only defaults.
        if "doc-write" in effective_skills:
            out.scope = "repo"
        else:
        # choose narrowest among candidates: paths > diff > repo
            modes = []
            paths_acc: List[str] = []
            for sc in scope_candidates:
                mode, globs = parse_scope_value(sc)
                if mode == "any":
                    continue
                modes.append(mode)
                paths_acc.extend(globs)
            if "paths" in modes:
                merged = sorted(set(paths_acc))
                out.scope = f"paths({','.join(merged)})" if merged else "paths()"
            elif "diff" in modes:
                out.scope = "diff"
            elif "repo" in modes:
                out.scope = "repo"
            else:
                out.scope = "diff"

    # output precedence
    if macro.output:
        if macro.output not in VALID_OUTPUTS:
            raise ValueError(f"Invalid output: {macro.output}")
        out.output = macro.output
    elif output_candidates:
        out.output = output_candidates[0]
    else:
        out.output = "md(contract=v1)"

    if not out.stages:
        raise ValueError("No stages resolved from macro")

    out.policy = sort_policies(out.policy)
    if not out.policy:
        out.policy = ["evidence", "deterministic-output"]
        warnings.append("No policy resolved; fallback to evidence + deterministic-output.")

    lens_source = resolve_lens_source(
        macro,
        effective_skills,
        workflow_lens_map,
        skill_lens_map,
        out,
        runtime_metadata.skill_response_profile_map,
    )
    return out, warnings, effective_skills, expanded_skills, lens_source


def format_program_one_liner(p: Program) -> str:
    return (
        f"[stages: {'>'.join(p.stages)} | "
        f"scope: {p.scope} | "
        f"policy: {','.join(p.policy)} | "
        f"lens: {p.lens} | "
        f"output: {p.output}]"
    )


def select_primary_skill(skills: List[str], skill_response_profile_map: Optional[Dict[str, str]] = None) -> str:
    explicit = [s.strip().lower() for s in skills if s and s.strip()]
    if not explicit:
        return "compose"

    profile_map = skill_response_profile_map or SKILL_RESPONSE_PROFILE_MAP

    # Completion-control skills own the loop semantics even when companion skills are composed
    # beside them. Keep the controller as primary so response profile and stop conditions remain visible.
    for skill in reversed(explicit):
        if skill in COMPLETION_CONTROL_SKILLS:
            return skill

    # Choose the last concrete domain skill so chained macros ($scout-structure-map $plan-task-breakdown, $plan-task-breakdown $build-write-code)
    # render in the profile of the final intent.
    for skill in reversed(explicit):
        if skill in ROUTING_SKIP_SKILLS:
            continue
        if skill in profile_map:
            return skill

    # Fallback: prefer any mapped non-compose skill in reverse order
    # so orchestration wrapper `$compose` does not hide explicit intent.
    for skill in reversed(explicit):
        if skill == "compose":
            continue
        if skill in profile_map:
            return skill

    for skill in explicit:
        if skill in profile_map:
            return skill

    return explicit[0]


def should_use_generic_profile(skills: List[str]) -> bool:
    explicit = [s.strip().lower() for s in skills if s and s.strip()]
    if any(skill in COMPLETION_CONTROL_SKILLS for skill in explicit):
        return False
    return len(explicit) > 1


def build_response_profile(
    skills: List[str],
    skill_response_profile_map: Optional[Dict[str, str]] = None,
    profile_required_sections_map: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, object]:
    profile_map = skill_response_profile_map or SKILL_RESPONSE_PROFILE_MAP
    sections_map = profile_required_sections_map or PROFILE_REQUIRED_SECTIONS_MAP
    primary_skill = select_primary_skill(skills, profile_map)
    profile_id = "generic" if should_use_generic_profile(skills) else profile_map.get(primary_skill, "generic")
    required_sections = sections_map.get(
        profile_id,
        sections_map.get("generic", FALLBACK_PROFILE_REQUIRED_SECTIONS["generic"]),
    )
    return {
        "primary_skill": primary_skill,
        "is_composite": should_use_generic_profile(skills),
        "profile_id": profile_id,
        "required_sections": list(required_sections),
    }


def build_input_routing(
    macro: Optional[MacroParse],
    effective_skills: List[str],
    runtime_metadata: RuntimeMetadata,
    normalized_scope: Optional[str],
) -> Dict[str, object]:
    raw_request = macro.prompt_tail if macro else None
    scope_source = None
    if macro:
        if macro.scope:
            scope_source = macro.scope
        elif macro.docs:
            scope_source = " ".join(f"@{doc}" for doc in macro.docs)

    input_route_table: List[Dict[str, object]] = []
    missing_required_inputs: List[Dict[str, object]] = []
    starter_input_state: List[Dict[str, object]] = []

    for skill in effective_skills:
        if skill in ROUTING_SKIP_SKILLS:
            continue
        metadata = runtime_metadata.skill_metadata.get(skill, {})
        starter_inputs = metadata.get("starter_inputs")
        required_inputs = metadata.get("required_inputs")
        if not isinstance(required_inputs, list):
            continue
        if not isinstance(starter_inputs, list):
            starter_inputs = []

        satisfied_fields: Set[str] = set()
        suggested_starter_key_by_field: Dict[str, str] = {}

        for starter in starter_inputs:
            if not isinstance(starter, dict):
                continue
            starter_key = starter.get("key")
            maps_to = starter.get("maps_to")
            if not isinstance(starter_key, str) or not isinstance(maps_to, list):
                continue
            for target_field in maps_to:
                if isinstance(target_field, str) and target_field:
                    suggested_starter_key_by_field[target_field] = starter_key

            status = "optional-unset"
            value_source = None
            if starter_key == "SCOPE" and normalized_scope and scope_source:
                status = "mapped"
                value_source = scope_source
                for target_field in maps_to:
                    if not isinstance(target_field, str) or not target_field:
                        continue
                    satisfied_fields.add(target_field)
                    input_route_table.append(
                        {
                            "starter_key": starter_key,
                            "value_source": value_source,
                            "target_skill": skill,
                            "target_field": target_field,
                            "status": status,
                        }
                    )
            elif starter_key == "EVIDENCE" and macro and macro.docs and any(is_doclike_input(doc) for doc in macro.docs):
                status = "mapped"
                value_source = "DOC_INPUTS"
                for target_field in maps_to:
                    if not isinstance(target_field, str) or not target_field:
                        continue
                    satisfied_fields.add(target_field)
                    input_route_table.append(
                        {
                            "starter_key": starter_key,
                            "value_source": value_source,
                            "target_skill": skill,
                            "target_field": target_field,
                            "status": status,
                        }
                    )
            elif raw_request and starter.get("derive_from_raw_request") and starter_key in {"GOAL", "DONE", "EXPECTED", "EVIDENCE", "CONSTRAINTS", "CONTEXT"}:
                status = "derived"
                value_source = "RAW_REQUEST"
                for target_field in maps_to:
                    if not isinstance(target_field, str) or not target_field:
                        continue
                    satisfied_fields.add(target_field)
                    input_route_table.append(
                        {
                            "starter_key": starter_key,
                            "value_source": value_source,
                            "target_skill": skill,
                            "target_field": target_field,
                            "status": status,
                        }
                    )
            elif starter.get("required"):
                status = "missing"

            starter_input_state.append(
                {
                    "target_skill": skill,
                    "starter_key": starter_key,
                    "required": bool(starter.get("required")),
                    "status": status,
                    "maps_to": [field for field in maps_to if isinstance(field, str)],
                    "value_source": value_source,
                }
            )

        if skill == "plan-sync-tasks" and macro and macro.docs:
            for doc in macro.docs:
                role = infer_plan_artifact_role(doc)
                if role == "plan":
                    satisfied_fields.add("IMPLEMENTATION_PLAN_PATH")
                    input_route_table.append(
                        {
                            "starter_key": "DOC_PATH",
                            "value_source": doc,
                            "target_skill": skill,
                            "target_field": "IMPLEMENTATION_PLAN_PATH",
                            "status": "mapped",
                        }
                    )
                if role == "tasks":
                    satisfied_fields.add("TASKS_PATH")
                    input_route_table.append(
                        {
                            "starter_key": "DOC_PATH",
                            "value_source": doc,
                            "target_skill": skill,
                            "target_field": "TASKS_PATH",
                            "status": "mapped",
                        }
                    )

        for required_input in required_inputs:
            if not isinstance(required_input, dict) or not required_input.get("required"):
                continue
            field_name = required_input.get("name")
            if not isinstance(field_name, str) or not field_name or field_name in satisfied_fields:
                continue
            missing_required_inputs.append(
                {
                    "target_skill": skill,
                    "target_field": field_name,
                    "suggested_starter_key": suggested_starter_key_by_field.get(field_name),
                    "reason": "required and not mapped from current compose inputs",
                }
            )

    return {
        "raw_request": raw_request,
        "input_route_table": input_route_table,
        "missing_required_inputs": missing_required_inputs,
        "starter_input_state": starter_input_state,
    }


def build_contract_outputs(
    *,
    macro: Optional[MacroParse],
    effective_skills: List[str],
    expanded_skills: List[str],
    response_profile: Optional[Dict[str, object]],
    program: Optional[str],
    normalized_scope: Optional[str],
    lens_source: Optional[str],
    routing: Optional[Dict[str, object]],
    warnings: List[str],
    errors: List[str],
) -> Dict[str, object]:
    return {
        "INPUT_MODE": "macro",
        "PARSED_SKILLS": list(macro.skills) if macro else [],
        "EFFECTIVE_SKILLS": list(effective_skills),
        "EXPANDED_SKILLS": list(expanded_skills),
        "PARSED_DOC_INPUTS": list(macro.docs) if macro else [],
        "PROMPT_TAIL": macro.prompt_tail if macro else None,
        "RAW_REQUEST": routing.get("raw_request") if routing else (macro.prompt_tail if macro else None),
        "NORMALIZED_SCOPE": normalized_scope,
        "LENS_SOURCE": lens_source,
        "PROGRAM": program,
        "RESPONSE_PROFILE": response_profile,
        "INPUT_ROUTE_TABLE": list(routing.get("input_route_table", [])) if routing else [],
        "MISSING_REQUIRED_INPUTS": list(routing.get("missing_required_inputs", [])) if routing else [],
        "STARTER_INPUT_STATE": list(routing.get("starter_input_state", [])) if routing else [],
        "STRUCTURAL_WARNINGS": list(warnings),
        "STRUCTURAL_ERRORS": list(errors),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Parse skill macro expression into Fusion PROGRAM")
    ap.add_argument(
        "--macro",
        required=True,
        help=(
            "Macro expression. '+' separators are optional for skill tokens, and plain text after "
            "skill tokens is captured as prompt tail. "
            "Use bracket blocks '[...]' for explicit prompt payloads (supports nesting/escaping). "
            "Example: '$plan-sync-tasks $build-write-code $check-final-verify [continue with this prompt] @plans/TASKS.md'"
        ),
    )
    default_skills_root = str(Path(__file__).resolve().parents[2])
    ap.add_argument("--skills-root", default=default_skills_root, help="Skills root path")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    args = ap.parse_args()

    macro: Optional[MacroParse] = None
    runtime_metadata: Optional[RuntimeMetadata] = None
    try:
        macro = parse_macro_expr(args.macro)
        runtime_metadata = build_runtime_metadata(Path(args.skills_root))
        merged, warnings, effective_skills, expanded_skills, lens_source = compose_program(
            macro,
            Path(args.skills_root),
            runtime_metadata,
        )
        response_profile = build_response_profile(
            effective_skills,
            runtime_metadata.skill_response_profile_map,
            runtime_metadata.profile_required_sections_map,
        )
        program = format_program_one_liner(merged)
        routing = build_input_routing(macro, effective_skills, runtime_metadata, merged.scope)
    except ValueError as exc:
        if args.format == "json":
            errors = [str(exc)]
            warnings = list(macro.warnings) if macro else []
            if runtime_metadata:
                warnings.extend(runtime_metadata.warnings)
            routing = build_input_routing(macro, [], RuntimeMetadata(), None) if macro else None
            payload = {
                "input_macro": args.macro,
                "parsed": {
                    "skills": list(macro.skills) if macro else [],
                    "effective_skills": [],
                    "expanded_skills": [],
                    "input_mode": "macro",
                    "lens": macro.lens if macro else None,
                    "approval": macro.approval if macro else None,
                    "scope": macro.scope if macro else None,
                    "output": macro.output if macro else None,
                    "policy": list(macro.policy) if macro else [],
                    "docs": list(macro.docs) if macro else [],
                    "prompt_tail": macro.prompt_tail if macro else None,
                    "raw_request": macro.prompt_tail if macro else None,
                },
                "program": None,
                "response_profile": None,
                "program_one_liner": None,
                "routing": routing,
                "contract_outputs": build_contract_outputs(
                    macro=macro,
                    effective_skills=[],
                    expanded_skills=[],
                    response_profile=None,
                    program=None,
                    normalized_scope=None,
                    lens_source=None,
                    routing=routing,
                    warnings=warnings,
                    errors=errors,
                ),
                "resolved": {
                    "normalized_scope": None,
                    "lens_source": None,
                    "structural_warnings": warnings,
                    "structural_errors": errors,
                },
                "warnings": warnings,
                "errors": errors,
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 2
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        contract_outputs = build_contract_outputs(
            macro=macro,
            effective_skills=effective_skills,
            expanded_skills=expanded_skills,
            response_profile=response_profile,
            program=program,
            normalized_scope=merged.scope,
            lens_source=lens_source,
            routing=routing,
            warnings=warnings,
            errors=[],
        )
        payload = {
            "input_macro": args.macro,
            "parsed": {
                "skills": macro.skills,
                "effective_skills": effective_skills,
                "expanded_skills": expanded_skills,
                "input_mode": "macro",
                "lens": macro.lens,
                "approval": macro.approval,
                "scope": macro.scope,
                "output": macro.output,
                "policy": macro.policy,
                "docs": macro.docs,
                "prompt_tail": macro.prompt_tail,
                "raw_request": macro.prompt_tail,
            },
            "program": {
                "stages": merged.stages,
                "scope": merged.scope,
                "policy": merged.policy,
                "lens": merged.lens,
                "output": merged.output,
            },
            "response_profile": response_profile,
            "program_one_liner": program,
            "routing": routing,
            "contract_outputs": contract_outputs,
            "resolved": {
                "normalized_scope": merged.scope,
                "lens_source": lens_source,
                "structural_warnings": warnings,
                "structural_errors": [],
            },
            "warnings": warnings,
            "errors": [],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print("## Compose Parse")
    print(f"- Input: `{args.macro}`")
    print(f"- Skills: {', '.join('$'+s for s in macro.skills) if macro.skills else 'None'}")
    print(f"- Effective skills: {', '.join('$'+s for s in effective_skills) if effective_skills else 'None'}")
    print(f"- Approval: {macro.approval or 'None'}")
    print(f"- Docs: {', '.join(macro.docs) if macro.docs else 'None'}")
    print(f"- Prompt tail: {macro.prompt_tail or 'None'}")
    print(
        f"- Response profile: {response_profile['profile_id']} "
        f"(primary skill: ${response_profile['primary_skill']})"
    )
    if warnings:
        print(f"- Warnings: {'; '.join(warnings)}")
    print()
    print("## Normalized PROGRAM")
    print(program)
    print()
    print("## Compose-Ready Prompt")
    print("$compose")
    print(program)
    if macro.docs:
        print("CONTEXT:")
        for d in macro.docs:
            print(f"- Plan doc: @{d}")
    if macro.prompt_tail:
        print("PROMPT:")
        print(macro.prompt_tail)
    print("RESPONSE_PROFILE:")
    print(f"- primary_skill: {response_profile['primary_skill']}")
    print(f"- profile_id: {response_profile['profile_id']}")
    print(f"- required_sections: {', '.join(response_profile['required_sections'])}")
    print()
    print("ROUTING:")
    print(f"- raw_request: {routing['raw_request'] or 'None'}")
    if routing["input_route_table"]:
        print("- input_route_table:")
        for row in routing["input_route_table"]:
            print(
                f"  - {row['starter_key']} -> ${row['target_skill']}.{row['target_field']} "
                f"({row['status']}, source={row['value_source']})"
            )
    else:
        print("- input_route_table: none")
    if routing["missing_required_inputs"]:
        print("- missing_required_inputs:")
        for row in routing["missing_required_inputs"]:
            suggested = row["suggested_starter_key"] or "None"
            print(
                f"  - ${row['target_skill']}.{row['target_field']} "
                f"(suggested_starter_key={suggested})"
            )
    else:
        print("- missing_required_inputs: none")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
