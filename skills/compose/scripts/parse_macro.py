#!/usr/bin/env python3
"""Macro composition parser for Fusion skills.

Converts expressions like:
  $scout-facts + $plan-task-breakdown + $build-write-code + $check-delivered + [extra context] + @/abs/path/plan.md
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

PRIMARY_SELECTION_UTILITY_SKILLS = {"compose", "respond", "check-delivered", "plan-driven-delivery"}

LEGACY_SKILL_GUIDANCE: Dict[str, str] = {}

FALLBACK_SKILL_RESPONSE_PROFILE_MAP: Dict[str, str] = {
    "compose": "generic",
    "respond": "generic",
    "scout-facts": "analysis_report",
    "finish-until-done": "analysis_report",
    "test-run-user-scenarios": "analysis_report",
    "debug-map-blast-radius": "analysis_report",
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
    "build-write-code": "implementation_delta",
    "plan-driven-delivery": "implementation_delta",
    "check-delivered": "self_verify_report",
    "check-ship-risk": "review_findings",
    "check-merge-ready": "review_findings",
    "check-quality-scan": "review_findings",
    "debug-find-root-cause": "debug_report",
    "build-make-faster": "performance_report",
    "scout-baseline": "performance_report",
    "test-write-guards": "test_report",
    "test-design-cases": "test_report",
    "check-security-holes": "security_report",
    "ship-check-repo": "analysis_report",
    "ship-check-hygiene": "analysis_report",
    "ship-go-nogo": "release_decision",
    "release-publish": "generic",
    "tidy-find-magic-numbers": "review_findings",
    "tidy-find-copies": "review_findings",
    "check-module-walls": "review_findings",
    "check-failure-paths": "review_findings",
    "test-find-gaps": "review_findings",
    "tidy-reorganize": "implementation_delta",
    "tidy-cut-fat": "implementation_delta",
    "plan-what-it-does": "spec_contract",
    "plan-how-to-build": "design_contract",
    "ship-commit": "commit_proposal",
    "ask-find-question": "clarify_question",
    "ask-break-it-down": "question_stack",
    "ask-flip-assumption": "analysis_report",
    "ask-fix-prompt": "repair_report",
    "wf-ask-get-clear": "question_stack",
    "wf-ask-sharpen": "question_stack",
    "wf-check-full-review": "review_findings",
    "wf-check-with-checklist": "review_findings",
    "wf-debug-this": "debug_report",
    "wf-tidy-find-improvements": "analysis_report",
    "wf-ship-it": "generic",
    "wf-ship-ready-check": "release_decision",
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


def _parse_markdown_table_row(line: str) -> List[str]:
    raw = line.strip()
    if not (raw.startswith("|") and raw.endswith("|")):
        return []
    return [c.strip() for c in raw.strip("|").split("|")]


def _is_markdown_separator_row(cells: List[str]) -> bool:
    if not cells:
        return False
    for c in cells:
        token = c.replace(":", "").strip()
        if not token:
            continue
        if not re.fullmatch(r"-+", token):
            return False
    return True


def _normalize_skill_token(token: str) -> str:
    out = token.strip().lower()
    out = out.replace("`", "")
    out = re.sub(r"\(.*?\)", "", out)
    out = out.strip()
    return out


def _split_required_sections(raw: str) -> List[str]:
    sections: List[str] = []
    current: List[str] = []
    depth_paren = 0
    depth_bracket = 0
    depth_brace = 0

    for ch in raw:
        if ch == "," and depth_paren == 0 and depth_bracket == 0 and depth_brace == 0:
            token = "".join(current).strip()
            if token:
                sections.append(token)
            current = []
            continue

        if ch == "(":
            depth_paren += 1
        elif ch == ")" and depth_paren > 0:
            depth_paren -= 1
        elif ch == "[":
            depth_bracket += 1
        elif ch == "]" and depth_bracket > 0:
            depth_bracket -= 1
        elif ch == "{":
            depth_brace += 1
        elif ch == "}" and depth_brace > 0:
            depth_brace -= 1

        current.append(ch)

    token = "".join(current).strip()
    if token:
        sections.append(token)

    return sections


def load_skill_response_profile_map(catalog_file: Optional[Path] = None) -> Tuple[Dict[str, str], bool, str]:
    if catalog_file is None:
        catalog_file = Path(__file__).resolve().parents[2] / "_core" / "SKILL-INTERACTION-MATRIX-v1.md"
    try:
        if not catalog_file.exists():
            return (
                dict(FALLBACK_SKILL_RESPONSE_PROFILE_MAP),
                True,
                f"Skill interaction matrix missing at {catalog_file}; using built-in response profile map.",
            )
        mapping: Dict[str, str] = {}
        for line in catalog_file.read_text(encoding="utf-8").splitlines():
            cells = _parse_markdown_table_row(line)
            if len(cells) < 4:
                continue
            if _is_markdown_separator_row(cells):
                continue
            if cells[0].lower() == "skill":
                continue

            skill = _normalize_skill_token(cells[0])
            profile_id = cells[3].strip().lower()
            if not skill or not profile_id:
                continue
            mapping[skill] = profile_id

        if mapping:
            return mapping, False, ""
        return (
            dict(FALLBACK_SKILL_RESPONSE_PROFILE_MAP),
            True,
            f"Skill interaction matrix at {catalog_file} has no valid skill->profile rows; using built-in fallback map.",
        )
    except Exception as exc:
        return (
            dict(FALLBACK_SKILL_RESPONSE_PROFILE_MAP),
            True,
            f"Skill interaction matrix load failed ({exc.__class__.__name__}) at {catalog_file}; using built-in fallback map.",
        )


def load_profile_required_sections(catalog_file: Optional[Path] = None) -> Tuple[Dict[str, List[str]], bool, str]:
    if catalog_file is None:
        catalog_file = Path(__file__).resolve().parents[2] / "_core" / "RESPONSE-PROFILES-v1.md"
    try:
        if not catalog_file.exists():
            return (
                dict(FALLBACK_PROFILE_REQUIRED_SECTIONS),
                True,
                f"Response profiles catalog missing at {catalog_file}; using built-in required sections map.",
            )
        mapping: Dict[str, List[str]] = {}
        for line in catalog_file.read_text(encoding="utf-8").splitlines():
            cells = _parse_markdown_table_row(line)
            if len(cells) < 3:
                continue
            if _is_markdown_separator_row(cells):
                continue
            if cells[0].lower() == "profile_id":
                continue

            profile_id = cells[0].strip().lower()
            required_sections = _split_required_sections(cells[2])
            if not profile_id or not required_sections:
                continue
            mapping[profile_id] = required_sections

        if mapping:
            return mapping, False, ""
        return (
            dict(FALLBACK_PROFILE_REQUIRED_SECTIONS),
            True,
            f"Response profiles catalog at {catalog_file} has no valid rows; using built-in required sections map.",
        )
    except Exception as exc:
        return (
            dict(FALLBACK_PROFILE_REQUIRED_SECTIONS),
            True,
            f"Response profiles catalog load failed ({exc.__class__.__name__}) at {catalog_file}; using built-in required sections map.",
        )

def load_valid_lenses(catalog_file: Optional[Path] = None) -> Tuple[Set[str], bool, str]:
    fallback = {
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
    }
    if catalog_file is None:
        catalog_file = Path(__file__).resolve().parents[2] / "_core" / "lenses.json"
    try:
        if not catalog_file.exists():
            return (
                fallback,
                True,
                f"Lens catalog missing at {catalog_file}; using built-in fallback lens set.",
            )
        data = json.loads(catalog_file.read_text(encoding="utf-8"))
        lenses = data.get("lenses", [])
        loaded = set()
        for item in lenses:
            if not isinstance(item, dict):
                continue
            lens_id = item.get("id")
            if isinstance(lens_id, str) and re.match(r"^[a-z0-9-]+$", lens_id):
                loaded.add(lens_id)
        if loaded:
            return loaded, False, ""
        return (
            fallback,
            True,
            f"Lens catalog at {catalog_file} has no valid lens IDs; using built-in fallback lens set.",
        )
    except Exception as exc:
        return (
            fallback,
            True,
            f"Lens catalog load failed ({exc.__class__.__name__}) at {catalog_file}; using built-in fallback lens set.",
        )


VALID_LENSES, VALID_LENSES_FALLBACK_USED, VALID_LENSES_FALLBACK_WARNING = load_valid_lenses()
SKILL_RESPONSE_PROFILE_MAP, SKILL_RESPONSE_PROFILE_FALLBACK_USED, SKILL_RESPONSE_PROFILE_FALLBACK_WARNING = (
    load_skill_response_profile_map()
)
PROFILE_REQUIRED_SECTIONS_MAP, PROFILE_REQUIRED_SECTIONS_FALLBACK_USED, PROFILE_REQUIRED_SECTIONS_FALLBACK_WARNING = (
    load_profile_required_sections()
)
VALID_OUTPUTS = {"md(contract=v1)", "json(schema=v1)", "both"}
VALID_SCOPES = {"repo", "diff"}
AUTO_RESPONSE_SKILL = "respond"


def load_workflow_registry(skills_root: Path) -> Tuple[Dict[str, dict], List[str]]:
    workflow_dir = skills_root / "_registry" / "workflow"
    warnings: List[str] = []
    workflows: Dict[str, dict] = {}
    if not workflow_dir.exists():
        return workflows, warnings

    for path in sorted(workflow_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - parser should degrade gracefully
            warnings.append(f"Failed to load workflow registry entry `{path.name}`: {exc}")
            continue
        name = data.get("name")
        expands_to = data.get("expands_to")
        if not isinstance(name, str) or not name:
            warnings.append(f"Workflow registry entry `{path.name}` is missing a valid `name`.")
            continue
        if not isinstance(expands_to, list) or not expands_to:
            warnings.append(f"Workflow registry entry `{path.name}` is missing a valid `expands_to` list.")
            continue
        workflows[name] = data
    return workflows, warnings


def expand_workflow_skills(skills: List[str], workflow_registry: Dict[str, dict]) -> Tuple[List[str], List[str]]:
    warnings: List[str] = []
    expanded: List[str] = []
    expansion_cache: Dict[str, List[str]] = {}

    def expand_one(skill: str, stack: List[str]) -> List[str]:
        if skill not in workflow_registry:
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
    content = skill_path.read_text(encoding="utf-8")
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


def suggest_skill_name(unknown_skill: str, skills_root: Path) -> Optional[str]:
    if unknown_skill in LEGACY_SKILL_GUIDANCE:
        return None
    candidates: List[str] = []
    try:
        for p in skills_root.iterdir():
            if not p.is_dir():
                continue
            if p.name.startswith(".") or p.name == "_core":
                continue
            if (p / "SKILL.md").exists():
                candidates.append(p.name)
        registry_index = skills_root / "_registry" / "index.json"
        if registry_index.exists():
            data = json.loads(registry_index.read_text(encoding="utf-8"))
            for names in data.values():
                if isinstance(names, list):
                    candidates.extend(name for name in names if isinstance(name, str))
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
) -> str:
    if macro.lens:
        return "explicit-override"
    primary_skill = select_primary_skill(effective_skills)
    if primary_skill in workflow_lens_map:
        return "workflow-default"
    if primary_skill in skill_lens_map:
        return "atomic-default"
    if out.lens:
        return "fallback-default"
    return "fallback-default"


def compose_program(macro: MacroParse, skills_root: Path) -> Tuple[Program, List[str], List[str], List[str], str]:
    warnings: List[str] = list(macro.warnings)
    if VALID_LENSES_FALLBACK_USED and VALID_LENSES_FALLBACK_WARNING:
        warnings.append(VALID_LENSES_FALLBACK_WARNING)
    if SKILL_RESPONSE_PROFILE_FALLBACK_USED and SKILL_RESPONSE_PROFILE_FALLBACK_WARNING:
        warnings.append(SKILL_RESPONSE_PROFILE_FALLBACK_WARNING)
    if PROFILE_REQUIRED_SECTIONS_FALLBACK_USED and PROFILE_REQUIRED_SECTIONS_FALLBACK_WARNING:
        warnings.append(PROFILE_REQUIRED_SECTIONS_FALLBACK_WARNING)
    if macro.unknown:
        raise ValueError(f"Unknown macro token(s): {macro.unknown}")

    if not macro.skills:
        raise ValueError("Macro must include at least one $skill token")

    effective_skills: List[str] = list(macro.skills)

    workflow_registry, workflow_warnings = load_workflow_registry(skills_root)
    warnings.extend(workflow_warnings)
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
            suggestion = suggest_skill_name(s, skills_root)
            if suggestion:
                raise ValueError(f"Unknown skill: ${s}. Did you mean ${suggestion}?")
            raise ValueError(f"Unknown skill: ${s}")
        block = extract_default_program_block(skill_file)
        prog = parse_program_block(block)
        resolved.append(prog)
        if prog.lens:
            skill_lens_map[s] = prog.lens

    if AUTO_RESPONSE_SKILL not in effective_skills:
        respond_file = skills_root / AUTO_RESPONSE_SKILL / "SKILL.md"
        if respond_file.exists():
            respond_block = extract_default_program_block(respond_file)
            resolved.append(parse_program_block(respond_block))
            warnings.append("Auto-appended $respond response layer.")

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
        if macro.lens not in VALID_LENSES:
            raise ValueError(f"Invalid lens: {macro.lens}")
        out.lens = macro.lens
    elif not out.lens:
        primary_skill = select_primary_skill(effective_skills)
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

    lens_source = resolve_lens_source(macro, effective_skills, workflow_lens_map, skill_lens_map, out)
    return out, warnings, effective_skills, expanded_skills, lens_source


def format_program_one_liner(p: Program) -> str:
    return (
        f"[stages: {'>'.join(p.stages)} | "
        f"scope: {p.scope} | "
        f"policy: {','.join(p.policy)} | "
        f"lens: {p.lens} | "
        f"output: {p.output}]"
    )


def select_primary_skill(skills: List[str]) -> str:
    explicit = [s.strip().lower() for s in skills if s and s.strip()]
    if not explicit:
        return AUTO_RESPONSE_SKILL

    # Choose the last concrete domain skill so chained macros ($scout-facts $plan-task-breakdown, $plan-task-breakdown $build-write-code)
    # render in the profile of the final intent.
    for skill in reversed(explicit):
        if skill in PRIMARY_SELECTION_UTILITY_SKILLS:
            continue
        if skill in SKILL_RESPONSE_PROFILE_MAP:
            return skill

    # Fallback: prefer any mapped non-compose skill in reverse order
    # so orchestration wrapper `$compose` does not hide explicit intent.
    for skill in reversed(explicit):
        if skill in {"compose", "respond"}:
            continue
        if skill in SKILL_RESPONSE_PROFILE_MAP:
            return skill

    for skill in explicit:
        if skill in SKILL_RESPONSE_PROFILE_MAP:
            return skill

    return explicit[0]


def should_use_generic_profile(skills: List[str]) -> bool:
    explicit = [s.strip().lower() for s in skills if s and s.strip()]
    return len(explicit) > 1


def build_response_profile(skills: List[str]) -> Dict[str, object]:
    primary_skill = select_primary_skill(skills)
    profile_id = "generic" if should_use_generic_profile(skills) else SKILL_RESPONSE_PROFILE_MAP.get(primary_skill, "generic")
    required_sections = PROFILE_REQUIRED_SECTIONS_MAP.get(
        profile_id,
        PROFILE_REQUIRED_SECTIONS_MAP.get("generic", FALLBACK_PROFILE_REQUIRED_SECTIONS["generic"]),
    )
    return {
        "primary_skill": primary_skill,
        "is_composite": should_use_generic_profile(skills),
        "profile_id": profile_id,
        "required_sections": list(required_sections),
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
        "NORMALIZED_SCOPE": normalized_scope,
        "LENS_SOURCE": lens_source,
        "PROGRAM": program,
        "RESPONSE_PROFILE": response_profile,
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
            "Example: '$plan-driven-delivery $build-write-code $check-delivered [continue with this prompt] @docs/TASKS.md'"
        ),
    )
    default_skills_root = str(Path(__file__).resolve().parents[2])
    ap.add_argument("--skills-root", default=default_skills_root, help="Skills root path")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    args = ap.parse_args()

    macro: Optional[MacroParse] = None
    try:
        macro = parse_macro_expr(args.macro)
        merged, warnings, effective_skills, expanded_skills, lens_source = compose_program(macro, Path(args.skills_root))
        response_profile = build_response_profile(effective_skills)
        program = format_program_one_liner(merged)
    except ValueError as exc:
        if args.format == "json":
            errors = [str(exc)]
            warnings = list(macro.warnings) if macro else []
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
                },
                "program": None,
                "response_profile": None,
                "program_one_liner": None,
                "contract_outputs": build_contract_outputs(
                    macro=macro,
                    effective_skills=[],
                    expanded_skills=[],
                    response_profile=None,
                    program=None,
                    normalized_scope=None,
                    lens_source=None,
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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
