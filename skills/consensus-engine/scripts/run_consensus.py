#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


AGENTS = ("codex", "claude", "gemini")
LENSES = {
    "codex": "contract-evidence-verifier",
    "claude": "craft-clarity",
    "gemini": "feynman",
    "orchestrator": "compose",
}
SUPPORT_WEIGHTS = {
    "grounded": 3.0,
    "reasoned": 2.0,
    "speculative": 1.0,
}
SIMILARITY_THRESHOLD = 0.80
HELP_TIMEOUT_SEC = 15
# Arbitration thresholds for classify_cluster.
# Unanimous acceptance: all 3 agents agree and average support score exceeds "speculative" (1.0).
# 1.4 sits between speculative(1.0) and reasoned(2.0), requiring at least mixed-quality evidence.
UNANIMOUS_AVG_SCORE_THRESHOLD = 1.4
# Provisional acceptance: 2 agents agree with aggregate score above a two-reasoned baseline (2×1.25).
PROVISIONAL_TOTAL_SCORE_THRESHOLD = 2.5
# Evidence floor: at minimum 2 anchor mentions AND at least 1 concrete anchor (file/symbol/prefix).
EVIDENCE_FLOOR_MIN_ANCHORS = 2
EVIDENCE_FLOOR_MIN_QUALITY = 1
ANCHOR_PREFIXES = (
    "constraint:",
    "constraints:",
    "done:",
    "done_signal:",
    "done_signals:",
    "context:",
    "path:",
    "symbol:",
    "request_summary:",
    "request_packet.",
    "request_packet:",
)
NEGATION_PATTERNS = (
    re.compile(r"^(?:do not|don't|never)\s+(.+)$", flags=re.I),
    re.compile(r"^avoid\s+(.+)$", flags=re.I),
    re.compile(r"^no\s+(.+)$", flags=re.I),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a two-round three-agent consensus flow across Codex, Claude Code, and Gemini CLI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--task", required=True, help="Bounded mission or decision question")
    parser.add_argument(
        "--mode",
        default="execute",
        choices=("execute", "analysis", "plan", "implement-review"),
        help="Mission mode",
    )
    parser.add_argument(
        "--macro-expression",
        default="",
        help="Optional explicit compose macro expression. When supplied, the engine runs the shared composed contract in parallel before consensus.",
    )
    parser.add_argument(
        "--skills-root",
        default="",
        help="Optional skills root path used when parsing a compose macro. Defaults to the repository skills root.",
    )
    parser.add_argument(
        "--constraint",
        action="append",
        default=[],
        help="Constraint to preserve (repeatable)",
    )
    parser.add_argument(
        "--done-signal",
        action="append",
        default=[],
        help="Observable done signal (repeatable)",
    )
    parser.add_argument(
        "--context-file",
        action="append",
        default=[],
        help="Path to a local context file to embed (repeatable)",
    )
    parser.add_argument(
        "--local-evidence",
        action="append",
        default=[],
        help="Locally verified fact or observation (repeatable)",
    )
    parser.add_argument(
        "--out-dir",
        default="",
        help="Output directory. Defaults to assets/runs/<timestamp> relative to the skill root.",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=2,
        choices=(1, 2),
        help="Number of consensus rounds",
    )
    parser.add_argument(
        "--timeout-sec",
        type=int,
        default=600,
        help="Per-agent subprocess timeout",
    )
    parser.add_argument(
        "--max-context-chars",
        type=int,
        default=5000,
        help="Maximum characters to include from each context file",
    )
    parser.add_argument("--codex-cmd", default="codex", help="Codex CLI command")
    parser.add_argument("--claude-cmd", default="claude", help="Claude Code CLI command")
    parser.add_argument("--gemini-cmd", default="gemini", help="Gemini CLI command")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write request packet and prompts only. Do not call external CLIs.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final consensus.result.json to stdout",
    )
    return parser.parse_args()


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def runtime_skills_root() -> Path:
    return skill_root().parent


def compose_parser_path() -> Path:
    return runtime_skills_root() / "compose" / "scripts" / "parse_macro.py"


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def quote_yaml_scalar(value: Any) -> str:
    if value is None:
        return '""'
    text = str(value)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_dump(data: Any, indent: int = 0) -> str:
    pad = "  " * indent
    if isinstance(data, dict):
        lines: List[str] = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.append(yaml_dump(value, indent + 1))
            else:
                lines.append(f"{pad}{key}: {quote_yaml_scalar(value)}")
        return "\n".join(lines)
    if isinstance(data, list):
        lines = []
        if not data:
            return f"{pad}[]"
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(yaml_dump(item, indent + 1))
            else:
                lines.append(f"{pad}- {quote_yaml_scalar(item)}")
        return "\n".join(lines)
    return f"{pad}{quote_yaml_scalar(data)}"


def normalize_text(text: str) -> str:
    normalized = re.sub(r"[^a-z0-9가-힣\s]", " ", text.lower())
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def token_set(text: str) -> set:
    norm = normalize_text(text)
    return set(norm.split()) if norm else set()


def decision_similarity(left: str, right: str) -> float:
    a = normalize_text(left)
    b = normalize_text(right)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    ratio = SequenceMatcher(None, a, b).ratio()
    ta = token_set(a)
    tb = token_set(b)
    if not ta or not tb:
        return ratio
    inter = len(ta & tb)
    union = len(ta | tb)
    jaccard = inter / union if union else 0.0
    overlap = inter / min(len(ta), len(tb)) if min(len(ta), len(tb)) else 0.0
    return max(ratio, jaccard, overlap * 0.95)


def support_score(item: Dict[str, Any]) -> float:
    support = str(item.get("support", "speculative"))
    confidence = float(item.get("confidence", 0.0))
    return SUPPORT_WEIGHTS.get(support, 1.0) * confidence


def dedupe_preserve(items: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        key = normalize_text(item)
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item.strip())
    return result


def anchor_quality(anchors: Iterable[str]) -> int:
    score = 0
    for item in anchors:
        if re.search(r"[A-Za-z0-9_./-]+\.[A-Za-z0-9]+", item):
            score += 1
        elif "/" in item or "::" in item or "()" in item:
            score += 1
        elif item.lower().startswith(ANCHOR_PREFIXES):
            score += 1
    return score


def trim_statement(statement: str) -> str:
    return re.sub(r"[\s:;,.]+$", "", statement.strip())


def canonicalize_decision(statement: str, polarity: str) -> Tuple[str, str]:
    raw = trim_statement(statement)
    if not raw:
        return "", polarity
    for pattern in NEGATION_PATTERNS:
        match = pattern.match(raw)
        if not match:
            continue
        canonical = trim_statement(match.group(1))
        return canonical or raw, "avoid"
    return raw, polarity


def load_context_files(paths: List[str], max_chars: int) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for raw in paths:
        path = Path(raw)
        if not path.exists():
            raise FileNotFoundError(f"context file not found: {path}")
        content = read_text(path)
        truncated = len(content) > max_chars
        preview = content[:max_chars]
        items.append(
            {
                "path": str(path),
                "bytes": len(content.encode("utf-8")),
                "truncated": truncated,
                "preview": preview,
            }
        )
    return items


def selected_skills_root(args: argparse.Namespace) -> Path:
    return Path(args.skills_root).resolve() if args.skills_root else runtime_skills_root()


def load_compose_contract(args: argparse.Namespace, out_dir: Path) -> Optional[Dict[str, Any]]:
    if not args.macro_expression.strip():
        return None

    parser_path = compose_parser_path()
    if not parser_path.exists():
        raise FileNotFoundError(f"compose parser not found: {parser_path}")

    proc = subprocess.run(
        [
            sys.executable,
            str(parser_path),
            "--macro",
            args.macro_expression,
            "--skills-root",
            str(selected_skills_root(args)),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        timeout=HELP_TIMEOUT_SEC,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"compose parser failed: rc={proc.returncode} stderr={proc.stderr.strip() or proc.stdout.strip()}"
        )
    payload = json.loads(proc.stdout)
    write_json(out_dir / "compose.contract.json", payload)
    return payload


def compose_missing_inputs(compose_contract: Optional[Dict[str, Any]]) -> List[str]:
    if not compose_contract:
        return []
    rows = compose_contract.get("contract_outputs", {}).get("MISSING_REQUIRED_INPUTS", [])
    items = []
    for row in rows:
        target_skill = row.get("target_skill", "unknown-skill")
        target_field = row.get("target_field", "unknown-field")
        starter_key = row.get("suggested_starter_key", "unknown")
        reason = row.get("reason", "missing")
        items.append(
            f"{target_skill}.{target_field} unresolved — suggested input {starter_key} ({reason})"
        )
    return items


def compose_blockers(compose_contract: Optional[Dict[str, Any]]) -> List[str]:
    return compose_missing_inputs(compose_contract)


def compose_contract_for_packet(compose_contract: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not compose_contract:
        return None
    contract = compose_contract.get("contract_outputs", {})
    response_profile = contract.get("RESPONSE_PROFILE") or {}
    return {
        "macro_expression": compose_contract.get("input_macro", ""),
        "program": contract.get("PROGRAM", ""),
        "normalized_scope": contract.get("NORMALIZED_SCOPE", ""),
        "effective_skills": contract.get("EFFECTIVE_SKILLS", []),
        "expanded_skills": contract.get("EXPANDED_SKILLS", []),
        "parsed_doc_inputs": contract.get("PARSED_DOC_INPUTS", []),
        "prompt_tail": contract.get("PROMPT_TAIL", ""),
        "starter_input_values": contract.get("STARTER_INPUT_VALUES", {}),
        "response_profile": {
            "primary_skill": response_profile.get("primary_skill"),
            "profile_id": response_profile.get("profile_id"),
            "required_sections": response_profile.get("required_sections", []),
        },
        "missing_required_inputs": contract.get("MISSING_REQUIRED_INPUTS", []),
        "structural_warnings": contract.get("STRUCTURAL_WARNINGS", []),
    }


def build_request_packet(
    args: argparse.Namespace,
    contexts: List[Dict[str, Any]],
    compose_contract: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    done_signals = args.done_signal[:] or [
        "Return one defensible recommendation, preserve disagreements, and list cheapest next checks"
    ]
    if compose_contract:
        profile_sections = (
            compose_contract.get("contract_outputs", {})
            .get("RESPONSE_PROFILE", {})
            .get("required_sections", [])
        )
        if profile_sections and not args.done_signal:
            done_signals = [
                "Produce one work product that covers the required response profile sections: "
                + ", ".join(profile_sections)
            ]

    task_kind = "compose-execution" if compose_contract else "decision"
    effective_mode = args.mode
    if compose_contract and args.mode == "execute":
        effective_mode = "execute"

    return {
        "request_summary": args.task.strip(),
        "mode": effective_mode,
        "task_kind": task_kind,
        "scope": {
            "in": [
                "the bounded mission in --task",
                "supplied context files",
                "supplied local evidence",
            ]
            + (["shared compose execution contract"] if compose_contract else []),
            "out": [
                "silent majority vote",
                "fabricated certainty",
                "shared-workspace concurrent edits",
            ],
        },
        "constraints": args.constraint[:],
        "done_signals": done_signals,
        "local_evidence": args.local_evidence[:],
        "open_questions": compose_missing_inputs(compose_contract),
        "safety": {
            "external_model_access_ok": True,
            "secrets_redacted": True,
        },
        "mental_models": LENSES,
        "context_files": [
            {
                "path": item["path"],
                "bytes": item["bytes"],
                "truncated": item["truncated"],
            }
            for item in contexts
        ],
        "compose_contract": compose_contract_for_packet(compose_contract),
    }


def format_request_packet_for_prompt(packet: Dict[str, Any], contexts: List[Dict[str, Any]]) -> str:
    lines = [
        f"request_summary: {packet['request_summary']}",
        f"task_kind: {packet['task_kind']}",
        f"mode: {packet['mode']}",
        "constraints:",
    ]
    if packet["constraints"]:
        lines.extend([f"- {x}" for x in packet["constraints"]])
    else:
        lines.append("- none")
    lines.append("done_signals:")
    lines.extend([f"- {x}" for x in packet["done_signals"]])
    lines.append("local_evidence:")
    if packet["local_evidence"]:
        lines.extend([f"- {x}" for x in packet["local_evidence"]])
    else:
        lines.append("- none")
    lines.append("open_questions:")
    if packet["open_questions"]:
        lines.extend([f"- {x}" for x in packet["open_questions"]])
    else:
        lines.append("- none")
    if contexts:
        lines.append("context_files:")
        for item in contexts:
            lines.append(f"- path: {item['path']}")
            lines.append(f"  truncated: {item['truncated']}")
            lines.append("  preview: |")
            for line in item["preview"].splitlines() or [""]:
                lines.append(f"    {line}")
    else:
        lines.append("context_files: []")
    compose_contract = packet.get("compose_contract")
    if compose_contract:
        lines.append("compose_contract:")
        lines.append(f"- macro_expression: {compose_contract.get('macro_expression') or '(none)'}")
        lines.append(f"- program: {compose_contract.get('program') or '(none)'}")
        lines.append(f"- normalized_scope: {compose_contract.get('normalized_scope') or '(none)'}")
        lines.append(
            "- effective_skills: "
            + (", ".join(compose_contract.get("effective_skills", [])) or "none")
        )
        lines.append(
            "- expanded_skills: "
            + (", ".join(compose_contract.get("expanded_skills", [])) or "none")
        )
        starter_input_values = compose_contract.get("starter_input_values") or {}
        if starter_input_values:
            lines.append(
                "- starter_input_values: "
                + json.dumps(starter_input_values, ensure_ascii=False, sort_keys=True)
            )
        response_profile = compose_contract.get("response_profile") or {}
        lines.append(f"- response_profile_id: {response_profile.get('profile_id') or 'none'}")
        lines.append(
            "- required_sections: "
            + (", ".join(response_profile.get("required_sections", [])) or "none")
        )
        lines.append(
            "- structural_warnings: "
            + (", ".join(compose_contract.get("structural_warnings", [])) or "none")
        )
    return "\n".join(lines)


def load_schema_text() -> str:
    schema_path = skill_root() / "assets" / "agent-response.schema.json"
    return read_text(schema_path)


def preflight_commands(args: argparse.Namespace) -> Dict[str, str]:
    commands = {
        "codex": args.codex_cmd,
        "claude": args.claude_cmd,
        "gemini": args.gemini_cmd,
    }
    resolved = {}
    missing = []
    for name, cmd in commands.items():
        resolved_path = shutil.which(cmd)
        if not resolved_path:
            missing.append(f"{name}: {cmd}")
        else:
            resolved[name] = resolved_path
    if missing:
        raise RuntimeError(
            "missing required CLI commands from PATH: " + ", ".join(missing)
        )
    return resolved


def probe_help(command: List[str]) -> str:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=HELP_TIMEOUT_SEC,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"failed to probe CLI help for {' '.join(command)} (exit={result.returncode})"
        )
    return (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")


def detect_cli_capabilities(resolved: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    probes = {
        "codex": [resolved["codex"], "exec", "--help"],
        "claude": [resolved["claude"], "--help"],
        "gemini": [resolved["gemini"], "--help"],
    }
    patterns = {
        "codex": {
            "sandbox": "--sandbox",
            "ask_for_approval": "--ask-for-approval",
            "output_schema": "--output-schema",
            "output_last_message": "--output-last-message",
            "json": "--json",
        },
        "claude": {
            "print": "-p, --print",
            "disable_slash_commands": "--disable-slash-commands",
            "no_session_persistence": "--no-session-persistence",
            "permission_mode": "--permission-mode",
            "output_format": "--output-format",
            "json_schema": "--json-schema",
        },
        "gemini": {
            "prompt": "-p, --prompt",
            "output_format": "--output-format",
            "approval_mode": "--approval-mode",
        },
    }

    capabilities: Dict[str, Dict[str, Any]] = {}
    for agent, command in probes.items():
        help_text = probe_help(command)
        supports = {
            key: token in help_text
            for key, token in patterns[agent].items()
        }
        capabilities[agent] = {
            "command": command,
            "supports": supports,
        }
    return capabilities


def build_round1_prompt(
    agent: str,
    packet: Dict[str, Any],
    packet_text: str,
    schema_text: str,
) -> str:
    lens = LENSES[agent]
    task_kind = packet.get("task_kind", "decision")
    compose_contract = packet.get("compose_contract")
    agent_guidance = {
        "codex": (
            "Drive toward an executable, testable, implementation-facing contract. "
            "Prefer atomic decisions that can be validated inside a repository."
        ),
        "claude": (
            "Drive toward clarity, ambiguity removal, hidden-assumption exposure, and reader-usable output. "
            "Do not confuse 'written' with 'finished'."
        ),
        "gemini": (
            "Drive toward first-principles explanation, disprovable hypotheses, and simple trade-off analysis. "
            "Prefer plain language over jargon when possible."
        ),
    }[agent]
    mission_text = (
        "Execute the shared composed workflow contract below and return one concrete work product plus the key decisions behind it."
        if task_kind == "compose-execution"
        else "Produce one bounded recommendation for the request packet below."
    )
    task_rules = [
        "- Round 1 is independent. Do not assume or simulate peer answers.",
        "- Do not invoke skills, slash commands, subagents, or hidden delegation loops.",
        "- Do not expose chain-of-thought. Return only conclusions, work product, atomic decisions, and explicit uncertainty.",
        "- Always fill `work_summary` with the concrete deliverable summary and `work_output` with the full draft, recommendation, report, or patch-style proposal you want selected.",
        "- Use `output_artifacts` for intended artifact paths or output units. Leave it empty only when no concrete artifact target exists.",
        "- Express every decision as a positive action phrase. Example: use `inspect repository files`, not `do not inspect repository files`; use `must_keep` or `must_avoid` for polarity.",
        "- Every item in `must_keep` and `must_avoid` must include `anchors` using canonical prefixes like `constraints:`, `done_signals:`, `path:`, `symbol:`, `request_summary:`, or `request_packet...`. If no concrete anchor exists, leave `anchors` empty and do not mark the claim as `grounded`.",
        "- Use `grounded` only for claims anchored in explicit evidence or specifications.",
        "- Use `reasoned` for justified inference.",
        "- Use `speculative` for plausible but weakly grounded ideas.",
        "- Prefer saying uncertain over guessing.",
    ]
    if task_kind == "compose-execution":
        task_rules.extend(
            [
                "- This is not analysis-only. Produce the actual deliverable in `work_output`.",
                "- Keep the deliverable aligned to the compose response profile required sections.",
                "- When required sections are present, render each section label verbatim as a Markdown heading inside `work_output`.",
                "- Do not edit repository files directly. Put the full draft, proposed patch, doc, PRD, or research output in `work_output` and list the intended artifact targets in `output_artifacts`.",
                "- For code-oriented work, prefer concise unified diff blocks or file-scoped patch sections inside `work_output`.",
            ]
        )
    else:
        task_rules.append("- Keep the run analysis-oriented. Do not edit files.")
    compose_hint = ""
    if compose_contract:
        compose_hint = (
            "\nCompose execution contract:\n"
            f"{json.dumps(compose_contract, ensure_ascii=False, indent=2)}\n"
        )
    return textwrap.dedent(
        f"""
        You are participating in a three-agent consensus engine.

        Agent: {agent}
        Lens: {lens}

        Mission:
        {mission_text}

        Hard rules:
        {chr(10).join(task_rules)}

        Lens guidance:
        {agent_guidance}

        Request packet:
        {packet_text}
        {compose_hint}

        Required output schema:
        {schema_text}

        Return ONLY one JSON object matching the schema.
        """
    ).strip()


def anonymized_slots() -> Dict[str, str]:
    return {"codex": "A", "claude": "B", "gemini": "C"}


def summarize_decisions(responses: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for agent, payload in responses.items():
        for polarity, field in (("keep", "must_keep"), ("avoid", "must_avoid")):
            for entry in payload.get(field, []):
                statement, canonical_polarity = canonicalize_decision(
                    entry.get("statement", "").strip(),
                    polarity,
                )
                items.append(
                    {
                        "agent": agent,
                        "polarity": canonical_polarity,
                        "statement": statement,
                        "raw_statement": entry.get("statement", "").strip(),
                        "why": entry.get("why", "").strip(),
                        "anchors": dedupe_preserve(entry.get("anchors", [])),
                        "support": entry.get("support", "speculative"),
                        "confidence": float(entry.get("confidence", 0.0)),
                        "score": support_score(entry),
                    }
                )
    return items


def cluster_decisions(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    clusters: List[Dict[str, Any]] = []
    for item in items:
        statement = item["statement"]
        if not statement:
            continue
        best_index = -1
        best_score = 0.0
        for idx, cluster in enumerate(clusters):
            score = decision_similarity(statement, cluster["statement"])
            if score > best_score:
                best_index = idx
                best_score = score
        if best_index >= 0 and best_score >= SIMILARITY_THRESHOLD:
            clusters[best_index]["items"].append(item)
        else:
            clusters.append(
                {
                    "statement": statement,
                    "items": [item],
                }
            )
    return clusters


def cluster_status(cluster: Dict[str, Any]) -> str:
    keep_agents = sorted({item["agent"] for item in cluster["items"] if item["polarity"] == "keep"})
    avoid_agents = sorted({item["agent"] for item in cluster["items"] if item["polarity"] == "avoid"})
    if keep_agents and avoid_agents:
        return "conflict"
    if len(keep_agents) == 3:
        return "keep-unanimous"
    if len(avoid_agents) == 3:
        return "avoid-unanimous"
    if len(keep_agents) >= 2:
        return "keep-lean"
    if len(avoid_agents) >= 2:
        return "avoid-lean"
    return "isolated"


def build_disagreement_packet(responses: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    slots = anonymized_slots()
    decisions = summarize_decisions(responses)
    clusters = cluster_decisions(decisions)

    packet_clusters = []
    for index, cluster in enumerate(clusters, start=1):
        keep_items = [x for x in cluster["items"] if x["polarity"] == "keep"]
        avoid_items = [x for x in cluster["items"] if x["polarity"] == "avoid"]

        def best_items_by_agent(items: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
            best: Dict[str, Dict[str, Any]] = {}
            for item in items:
                prev = best.get(item["agent"])
                if prev is None or item["score"] > prev["score"]:
                    best[item["agent"]] = item
            return best

        keep_best = best_items_by_agent(keep_items)
        avoid_best = best_items_by_agent(avoid_items)

        packet_clusters.append(
            {
                "id": f"D{index:02d}",
                "statement": cluster["statement"],
                "status": cluster_status(cluster),
                "keep_by": [slots[name] for name in sorted(keep_best.keys())],
                "avoid_by": [slots[name] for name in sorted(avoid_best.keys())],
                "keep_strength": round(sum(x["score"] for x in keep_best.values()), 3),
                "avoid_strength": round(sum(x["score"] for x in avoid_best.values()), 3),
                "keep_why_samples": [x["why"] for x in keep_best.values()][:2],
                "avoid_why_samples": [x["why"] for x in avoid_best.values()][:2],
            }
        )

    proposal_summaries = []
    for agent, payload in responses.items():
        proposal_summaries.append(
            {
                "slot": slots[agent],
                "summary": payload.get("summary", ""),
                "proposal": payload.get("proposal", ""),
                "work_summary": payload.get("work_summary", ""),
                "output_artifacts": payload.get("output_artifacts", []),
                "confidence": payload.get("confidence", 0.0),
            }
        )

    packet_clusters.sort(
        key=lambda item: (
            0 if item["status"] == "conflict" else 1,
            -max(item["keep_strength"], item["avoid_strength"]),
            item["id"],
        )
    )

    work_summary_variants = {
        normalize_text(payload.get("work_summary", ""))
        for payload in responses.values()
        if payload.get("work_summary", "").strip()
    }
    needs_rebuttal = any(
        item["status"] not in {"keep-unanimous", "avoid-unanimous"}
        for item in packet_clusters
    ) or len(work_summary_variants) > 1

    return {
        "anonymous_proposal_summaries": proposal_summaries,
        "decision_clusters": packet_clusters,
        "requires_rebuttal": needs_rebuttal,
        "instructions": [
            "Challenge weak claims instead of following the majority.",
            "Update only when the evidence packet justifies it.",
            "Keep must_keep and must_avoid atomic and comparison-friendly.",
        ],
    }


def build_round2_prompt(
    agent: str,
    packet: Dict[str, Any],
    packet_text: str,
    schema_text: str,
    disagreement_packet: Dict[str, Any],
) -> str:
    lens = LENSES[agent]
    task_kind = packet.get("task_kind", "decision")
    return textwrap.dedent(
        f"""
        You are participating in round 2 of a three-agent consensus engine.

        Agent: {agent}
        Lens: {lens}

        Your task:
        Re-evaluate your prior recommendation using the anonymized peer disagreement packet below.

        Hard rules:
        - Do not follow the majority blindly.
        - Weight evidence over popularity.
        - Update your position only when the disagreement packet materially changes your view.
        - Do not invoke skills, slash commands, subagents, or hidden delegation loops.
        - Do not expose chain-of-thought.
        - Keep `work_summary` and `work_output` aligned with your final position.
        - Express every decision as a positive action phrase. Example: use `inspect repository files`, not `do not inspect repository files`; use `must_keep` or `must_avoid` for polarity.
        - Every item in `must_keep` and `must_avoid` must include `anchors` using canonical prefixes like `constraints:`, `done_signals:`, `path:`, `symbol:`, `request_summary:`, or `request_packet...`. If no concrete anchor exists, leave `anchors` empty and do not mark the claim as `grounded`.
        - Preserve explicit uncertainty where the tie cannot be broken.
        {'- If you change the underlying deliverable, update `work_summary`, `work_output`, and `output_artifacts` as well. Keep required section labels verbatim as Markdown headings when the compose contract lists them.' if task_kind == 'compose-execution' else '- Keep the focus on the recommendation rather than stylistic drift.'}

        Original request packet:
        {packet_text}

        Anonymous disagreement packet:
        {json.dumps(disagreement_packet, ensure_ascii=False, indent=2)}

        Required output schema:
        {schema_text}

        Return ONLY one JSON object matching the schema.
        """
    ).strip()


def run_subprocess(
    command: List[str],
    stdout_path: Path,
    stderr_path: Path,
    timeout_sec: int,
) -> subprocess.CompletedProcess:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
    )
    write_text(stdout_path, result.stdout)
    write_text(stderr_path, result.stderr)
    return result


def extract_json_from_text(raw: str) -> Any:
    raw = raw.strip()
    if not raw:
        raise ValueError("empty output")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    start = raw.find("{")
    if start == -1:
        raise ValueError("no JSON object found in output")

    depth = 0
    in_string = False
    escape = False
    for index in range(start, len(raw)):
        char = raw[index]
        if escape:
            escape = False
            continue
        if char == "\\":
            escape = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                candidate = raw[start : index + 1]
                return json.loads(candidate)
    raise ValueError("unterminated JSON object in output")


def validate_agent_response(data: Any) -> List[str]:
    errors: List[str] = []
    if not isinstance(data, dict):
        return ["response is not a JSON object"]

    required = [
        "summary",
        "proposal",
        "work_summary",
        "work_output",
        "output_artifacts",
        "must_keep",
        "must_avoid",
        "assumptions",
        "uncertainties",
        "next_checks",
        "confidence",
    ]
    for key in required:
        if key not in data:
            errors.append(f"missing field: {key}")

    for key in ("summary", "proposal", "work_summary", "work_output"):
        if key in data and not isinstance(data[key], str):
            errors.append(f"{key} must be a string")

    for key in ("output_artifacts", "must_keep", "must_avoid", "assumptions", "uncertainties", "next_checks"):
        if key in data and not isinstance(data[key], list):
            errors.append(f"{key} must be a list")
    if "output_artifacts" in data and isinstance(data["output_artifacts"], list):
        for index, item in enumerate(data["output_artifacts"]):
            if not isinstance(item, str) or not item.strip():
                errors.append(f"output_artifacts[{index}] must be a non-empty string")

    confidence = data.get("confidence")
    if not isinstance(confidence, (int, float)):
        errors.append("confidence must be a number")
    elif not (0 <= float(confidence) <= 1):
        errors.append("confidence must be between 0 and 1")

    for field in ("must_keep", "must_avoid"):
        items = data.get(field, [])
        if not isinstance(items, list):
            continue
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"{field}[{index}] must be an object")
                continue
            for key in ("statement", "why", "support", "confidence"):
                if key not in item:
                    errors.append(f"{field}[{index}] missing {key}")
            if "anchors" not in item:
                errors.append(f"{field}[{index}] missing anchors")
            if "statement" in item and not isinstance(item["statement"], str):
                errors.append(f"{field}[{index}].statement must be a string")
            if "why" in item and not isinstance(item["why"], str):
                errors.append(f"{field}[{index}].why must be a string")
            if "anchors" in item and (
                not isinstance(item["anchors"], list)
                or any(not isinstance(anchor, str) or not anchor.strip() for anchor in item["anchors"])
            ):
                errors.append(f"{field}[{index}].anchors must be a list of non-empty strings")
            if "support" in item and item["support"] not in SUPPORT_WEIGHTS:
                errors.append(
                    f"{field}[{index}].support must be one of {sorted(SUPPORT_WEIGHTS.keys())}"
                )
            if "confidence" in item:
                value = item["confidence"]
                if not isinstance(value, (int, float)) or not (0 <= float(value) <= 1):
                    errors.append(f"{field}[{index}].confidence must be a number between 0 and 1")
    return errors


def parse_codex_output(response_path: Path) -> Dict[str, Any]:
    return extract_json_from_text(read_text(response_path))


def parse_claude_output(stdout_path: Path) -> Dict[str, Any]:
    payload = extract_json_from_text(read_text(stdout_path))
    if isinstance(payload, dict) and "structured_output" in payload:
        return payload["structured_output"]
    if isinstance(payload, dict) and "result" in payload and isinstance(payload["result"], str):
        return extract_json_from_text(payload["result"])
    return payload


def parse_gemini_output(stdout_path: Path) -> Dict[str, Any]:
    payload = extract_json_from_text(read_text(stdout_path))
    if isinstance(payload, dict) and isinstance(payload.get("response"), str):
        return extract_json_from_text(payload["response"])
    return payload


def codex_command(
    binary: str,
    prompt: str,
    schema_path: Path,
    response_path: Path,
    capabilities: Dict[str, Any],
) -> List[str]:
    command = [binary, "exec"]
    supports = capabilities["supports"]
    if supports.get("sandbox"):
        command.extend(["--sandbox", "read-only"])
    if supports.get("ask_for_approval"):
        command.extend(["--ask-for-approval", "never"])
    if supports.get("output_schema"):
        command.extend(["--output-schema", str(schema_path)])
    if supports.get("output_last_message"):
        command.extend(["--output-last-message", str(response_path)])
    command.append(prompt)
    return command


def claude_command(
    binary: str,
    prompt: str,
    schema_text: str,
    capabilities: Dict[str, Any],
) -> List[str]:
    supports = capabilities["supports"]
    command = [binary]
    if supports.get("print"):
        command.append("-p")
        command.append(prompt)
    else:
        raise RuntimeError("claude CLI does not support -p/--print non-interactive mode")
    if supports.get("disable_slash_commands"):
        command.append("--disable-slash-commands")
    if supports.get("no_session_persistence"):
        command.append("--no-session-persistence")
    if supports.get("permission_mode"):
        command.extend(["--permission-mode", "plan"])
    if supports.get("output_format"):
        command.extend(["--output-format", "json"])
    if supports.get("json_schema"):
        command.extend(["--json-schema", schema_text])
    return command


def gemini_command(
    binary: str,
    prompt: str,
    capabilities: Dict[str, Any],
) -> List[str]:
    supports = capabilities["supports"]
    command = [binary]
    if supports.get("prompt"):
        command.extend(["-p", prompt])
    else:
        raise RuntimeError("gemini CLI does not support -p/--prompt headless mode")
    if supports.get("output_format"):
        command.extend(["--output-format", "json"])
    if supports.get("approval_mode"):
        command.extend(["--approval-mode", "plan"])
    return command


def run_one_agent(
    agent: str,
    args: argparse.Namespace,
    resolved_cmd: str,
    prompt: str,
    schema_path: Path,
    schema_text: str,
    out_dir: Path,
    round_name: str,
    capabilities: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    prompt_path = out_dir / f"{agent}.{round_name}.prompt.txt"
    write_text(prompt_path, prompt)

    parser = {
        "codex": parse_codex_output,
        "claude": parse_claude_output,
        "gemini": parse_gemini_output,
    }[agent]

    for attempt in (1, 2):
        strict_prompt = prompt
        if attempt == 2:
            strict_prompt += "\n\nSTRICT RETRY: Your previous output failed parsing or validation. Return ONLY valid JSON matching the schema."

        stdout_path = out_dir / f"{agent}.{round_name}.attempt{attempt}.stdout.log"
        stderr_path = out_dir / f"{agent}.{round_name}.attempt{attempt}.stderr.log"

        if agent == "codex":
            response_path = out_dir / f"{agent}.{round_name}.attempt{attempt}.response.txt"
            command = codex_command(
                resolved_cmd,
                strict_prompt,
                schema_path,
                response_path,
                capabilities[agent],
            )
            if not capabilities[agent]["supports"].get("output_last_message"):
                response_path = stdout_path
        elif agent == "claude":
            response_path = stdout_path
            command = claude_command(
                resolved_cmd,
                strict_prompt,
                schema_text,
                capabilities[agent],
            )
        else:
            response_path = stdout_path
            command = gemini_command(
                resolved_cmd,
                strict_prompt,
                capabilities[agent],
            )

        result = run_subprocess(command, stdout_path, stderr_path, args.timeout_sec)

        if result.returncode != 0:
            if attempt == 2:
                raise RuntimeError(
                    f"{agent} {round_name} failed with exit code {result.returncode}; see {stderr_path.name}"
                )
            continue

        try:
            data = parser(response_path)
            errors = validate_agent_response(data)
            if errors:
                raise ValueError("; ".join(errors))
            final_path = out_dir / f"{agent}.{round_name}.json"
            write_json(final_path, data)
            return data
        except Exception as exc:
            if attempt == 2:
                raise RuntimeError(
                    f"{agent} {round_name} returned invalid structured output: {exc}"
                ) from exc

    raise RuntimeError(f"unreachable retry state for {agent} {round_name}")


def classify_cluster(cluster: Dict[str, Any]) -> Dict[str, Any]:
    keep_scores: Dict[str, float] = {}
    avoid_scores: Dict[str, float] = {}
    keep_anchors: Dict[str, List[str]] = {}
    avoid_anchors: Dict[str, List[str]] = {}

    for item in cluster["items"]:
        target_scores = keep_scores if item["polarity"] == "keep" else avoid_scores
        target_anchors = keep_anchors if item["polarity"] == "keep" else avoid_anchors
        prev = target_scores.get(item["agent"], 0.0)
        if item["score"] >= prev:
            target_scores[item["agent"]] = item["score"]
            target_anchors[item["agent"]] = dedupe_preserve(item.get("anchors", []))

    keep_count = len(keep_scores)
    avoid_count = len(avoid_scores)
    keep_total = round(sum(keep_scores.values()), 3)
    avoid_total = round(sum(avoid_scores.values()), 3)
    keep_avg = (keep_total / keep_count) if keep_count else 0.0
    avoid_avg = (avoid_total / avoid_count) if avoid_count else 0.0
    keep_anchor_list = [anchor for anchors in keep_anchors.values() for anchor in anchors]
    avoid_anchor_list = [anchor for anchors in avoid_anchors.values() for anchor in anchors]
    keep_anchor_mentions = len(keep_anchor_list)
    avoid_anchor_mentions = len(avoid_anchor_list)
    keep_anchor_quality = anchor_quality(keep_anchor_list)
    avoid_anchor_quality = anchor_quality(avoid_anchor_list)
    keep_evidence_floor = keep_anchor_mentions >= EVIDENCE_FLOOR_MIN_ANCHORS and keep_anchor_quality >= EVIDENCE_FLOOR_MIN_QUALITY
    avoid_evidence_floor = avoid_anchor_mentions >= EVIDENCE_FLOOR_MIN_ANCHORS and avoid_anchor_quality >= EVIDENCE_FLOOR_MIN_QUALITY

    classification = "unresolved"
    rationale = "insufficient aligned evidence"

    if keep_count and avoid_count:
        classification = "unresolved"
        rationale = "direct keep/avoid collision"
    elif keep_count == 3 and keep_avg >= UNANIMOUS_AVG_SCORE_THRESHOLD and keep_evidence_floor:
        classification = "accepted_keep"
        rationale = "3 keep / 0 avoid with adequate average evidence"
    elif avoid_count == 3 and avoid_avg >= UNANIMOUS_AVG_SCORE_THRESHOLD and avoid_evidence_floor:
        classification = "accepted_avoid"
        rationale = "0 keep / 3 avoid with adequate average evidence"
    elif keep_count >= 2 and avoid_count == 0 and keep_total >= PROVISIONAL_TOTAL_SCORE_THRESHOLD and keep_evidence_floor:
        classification = "provisional_keep"
        rationale = "2 keep / 0 avoid with stronger aggregate evidence"
    elif avoid_count >= 2 and keep_count == 0 and avoid_total >= PROVISIONAL_TOTAL_SCORE_THRESHOLD and avoid_evidence_floor:
        classification = "provisional_avoid"
        rationale = "0 keep / 2 avoid with stronger aggregate evidence"
    elif keep_count >= 2 and avoid_count == 0:
        classification = "needs_more_evidence"
        rationale = "aligned keep votes but evidence floor not met"
    elif avoid_count >= 2 and keep_count == 0:
        classification = "needs_more_evidence"
        rationale = "aligned avoid votes but evidence floor not met"

    return {
        "statement": cluster["statement"],
        "classification": classification,
        "rationale": rationale,
        "keep_by": sorted(keep_scores.keys()),
        "avoid_by": sorted(avoid_scores.keys()),
        "keep_strength": keep_total,
        "avoid_strength": avoid_total,
        "keep_evidence_floor_met": keep_evidence_floor,
        "avoid_evidence_floor_met": avoid_evidence_floor,
        "keep_anchor_mentions": keep_anchor_mentions,
        "avoid_anchor_mentions": avoid_anchor_mentions,
        "keep_anchor_quality": keep_anchor_quality,
        "avoid_anchor_quality": avoid_anchor_quality,
        "keep_anchors": dedupe_preserve(keep_anchor_list),
        "avoid_anchors": dedupe_preserve(avoid_anchor_list),
    }


def aggregate_next_checks(responses: Dict[str, Dict[str, Any]]) -> List[str]:
    counts: Dict[str, Tuple[str, int]] = {}
    for payload in responses.values():
        for item in payload.get("next_checks", []):
            key = normalize_text(item)
            if not key:
                continue
            if key in counts:
                original, count = counts[key]
                counts[key] = (original, count + 1)
            else:
                counts[key] = (item.strip(), 1)
    ranked = sorted(counts.values(), key=lambda x: (-x[1], len(x[0]), x[0]))
    return [text for text, _ in ranked[:10]]


def payload_aligns_with_statement(payload: Dict[str, Any], statement: str, expected_polarity: str) -> bool:
    for field, fallback_polarity in (("must_keep", "keep"), ("must_avoid", "avoid")):
        for item in payload.get(field, []):
            candidate, candidate_polarity = canonicalize_decision(
                item.get("statement", ""),
                fallback_polarity,
            )
            if candidate_polarity != expected_polarity:
                continue
            if decision_similarity(candidate, statement) >= SIMILARITY_THRESHOLD:
                return True
    return False


def required_sections_for_packet(packet: Dict[str, Any]) -> List[str]:
    compose_contract = packet.get("compose_contract") or {}
    response_profile = compose_contract.get("response_profile") or {}
    sections = response_profile.get("required_sections", [])
    return [section for section in sections if isinstance(section, str) and section.strip()]


def section_coverage(work_output: str, required_sections: List[str]) -> Dict[str, Any]:
    if not required_sections:
        return {
            "matched": [],
            "missing": [],
            "complete": True,
        }
    normalized_lines = []
    for raw in work_output.splitlines():
        line = raw.strip()
        if not line:
            continue
        line = re.sub(r"^[#*\-\d.\)\s]+", "", line).strip()
        normalized_lines.append(line.lower())
    matched = []
    for section in required_sections:
        lowered = section.strip().lower()
        if any(
            line == lowered
            or line.startswith(f"{lowered}:")
            or line.startswith(f"{lowered} -")
            for line in normalized_lines
        ):
            matched.append(section)
    missing = [section for section in required_sections if section not in matched]
    return {
        "matched": matched,
        "missing": missing,
        "complete": not missing,
    }


def select_work_product(
    packet: Dict[str, Any],
    verdict: str,
    final_responses: Dict[str, Dict[str, Any]],
    accepted_keep: List[Dict[str, Any]],
    accepted_avoid: List[Dict[str, Any]],
    provisional_keep: List[Dict[str, Any]],
    provisional_avoid: List[Dict[str, Any]],
) -> Dict[str, Any]:
    required_sections = required_sections_for_packet(packet)
    candidates = []
    for agent, payload in final_responses.items():
        fit_score = 0.0
        for item in accepted_keep:
            if payload_aligns_with_statement(payload, item["statement"], "keep"):
                fit_score += 3.0
        for item in accepted_avoid:
            if payload_aligns_with_statement(payload, item["statement"], "avoid"):
                fit_score += 3.0
        for item in provisional_keep:
            if payload_aligns_with_statement(payload, item["statement"], "keep"):
                fit_score += 1.5
        for item in provisional_avoid:
            if payload_aligns_with_statement(payload, item["statement"], "avoid"):
                fit_score += 1.5
        fit_score += float(payload.get("confidence", 0.0))
        coverage = section_coverage(payload.get("work_output", ""), required_sections)
        candidate = {
            "agent": agent,
            "fit_score": round(fit_score, 3),
            "confidence": payload.get("confidence", 0.0),
            "work_summary": payload.get("work_summary", ""),
            "output_artifacts": payload.get("output_artifacts", []),
            "work_output": payload.get("work_output", ""),
            "required_sections_complete": coverage["complete"],
            "matched_required_sections": coverage["matched"],
            "missing_required_sections": coverage["missing"],
        }
        candidates.append(candidate)

    candidates.sort(
        key=lambda item: (
            0 if item["required_sections_complete"] else 1,
            -len(item["matched_required_sections"]),
            -item["fit_score"],
            -item["confidence"],
            item["agent"],
        )
    )

    selected = None
    status = "withheld"
    reason = "no candidate work products were produced"
    if candidates and verdict != "no-consensus":
        eligible = candidates
        if required_sections:
            eligible = [item for item in candidates if item["required_sections_complete"]]
        if eligible:
            selected = eligible[0]
            status = "selected"
            reason = "highest-fit candidate among eligible work products"
        elif required_sections:
            reason = "withheld because no candidate covered all required sections"
    elif verdict == "no-consensus":
        reason = "withheld because the consensus verdict is no-consensus"

    return {
        "selected": selected,
        "status": status,
        "reason": reason,
        "candidates": [{k: v for k, v in item.items() if k != "work_output"} for item in candidates],
    }


def build_consensus_result(
    packet: Dict[str, Any],
    final_responses: Dict[str, Dict[str, Any]],
    out_dir: Path,
) -> Dict[str, Any]:
    clusters = cluster_decisions(summarize_decisions(final_responses))
    classified = [classify_cluster(cluster) for cluster in clusters]

    accepted_keep = [x for x in classified if x["classification"] == "accepted_keep"]
    accepted_avoid = [x for x in classified if x["classification"] == "accepted_avoid"]
    provisional_keep = [x for x in classified if x["classification"] == "provisional_keep"]
    provisional_avoid = [x for x in classified if x["classification"] == "provisional_avoid"]
    unresolved = [x for x in classified if x["classification"] == "unresolved"]
    needs_more_evidence = [x for x in classified if x["classification"] == "needs_more_evidence"]

    if (accepted_keep or accepted_avoid) and not unresolved:
        verdict = "strong-consensus"
    elif accepted_keep or accepted_avoid or provisional_keep or provisional_avoid:
        verdict = "provisional-consensus"
    else:
        verdict = "no-consensus"

    work_product_bundle = select_work_product(
        packet,
        verdict,
        final_responses,
        accepted_keep,
        accepted_avoid,
        provisional_keep,
        provisional_avoid,
    )

    recommendation_lines: List[str] = []
    if accepted_keep:
        recommendation_lines.append(
            "Adopt the accepted keep decisions first: "
            + "; ".join(item["statement"] for item in accepted_keep[:5])
        )
    if accepted_avoid:
        recommendation_lines.append(
            "Avoid the accepted avoid decisions: "
            + "; ".join(item["statement"] for item in accepted_avoid[:5])
        )
    if not accepted_keep and provisional_keep:
        recommendation_lines.append(
            "Best current direction is provisional: "
            + "; ".join(item["statement"] for item in provisional_keep[:5])
        )
    if unresolved:
        recommendation_lines.append(
            "Do not lock in unresolved items yet: "
            + "; ".join(item["statement"] for item in unresolved[:5])
        )
    if needs_more_evidence:
        recommendation_lines.append(
            "These directions still lack the evidence floor: "
            + "; ".join(item["statement"] for item in needs_more_evidence[:5])
        )
    if not recommendation_lines:
        recommendation_lines.append(
            "No decision reached the acceptance threshold. Break the tie with the cheapest next checks."
        )

    agent_status = {
        agent: {
            "status": "ok",
            "confidence": final_responses[agent].get("confidence", 0.0),
        }
        for agent in AGENTS
    }

    result = {
        "verdict": verdict,
        "consensus_recommendation": " ".join(recommendation_lines),
        "accepted_keep": accepted_keep,
        "accepted_avoid": accepted_avoid,
        "provisional_keep": provisional_keep,
        "provisional_avoid": provisional_avoid,
        "unresolved": unresolved,
        "needs_more_evidence": needs_more_evidence,
        "cheapest_next_checks": aggregate_next_checks(final_responses),
        "agent_status": agent_status,
        "selected_work_product": work_product_bundle["selected"],
        "work_product_selection_status": work_product_bundle["status"],
        "work_product_selection_reason": work_product_bundle["reason"],
        "candidate_work_products": work_product_bundle["candidates"],
        "artifacts": {
            "out_dir": str(out_dir),
            "report": str(out_dir / "consensus.report.md"),
            "result": str(out_dir / "consensus.result.json"),
        },
        "task_kind": packet.get("task_kind", "decision"),
    }
    return result


def format_section(title: str, items: List[Dict[str, Any]]) -> str:
    if not items:
        return f"## {title}\n- none\n"
    lines = [f"## {title}"]
    for item in items:
        lines.append(f"- {item['statement']}")
        lines.append(
            f"  - rationale: {item['rationale']}"
        )
        lines.append(
            f"  - keep_by: {', '.join(item['keep_by']) or 'none'} | avoid_by: {', '.join(item['avoid_by']) or 'none'}"
        )
        lines.append(
            f"  - keep_strength: {item['keep_strength']} | avoid_strength: {item['avoid_strength']}"
        )
        lines.append(
            f"  - keep_evidence_floor: {'yes' if item['keep_evidence_floor_met'] else 'no'} ({item['keep_anchor_mentions']} anchors, quality={item['keep_anchor_quality']})"
        )
        lines.append(
            f"  - avoid_evidence_floor: {'yes' if item['avoid_evidence_floor_met'] else 'no'} ({item['avoid_anchor_mentions']} anchors, quality={item['avoid_anchor_quality']})"
        )
        if item["keep_anchors"]:
            lines.append(f"  - keep_anchors: {', '.join(item['keep_anchors'][:4])}")
        if item["avoid_anchors"]:
            lines.append(f"  - avoid_anchors: {', '.join(item['avoid_anchors'][:4])}")
    return "\n".join(lines) + "\n"


def build_report(
    packet: Dict[str, Any],
    result: Dict[str, Any],
) -> str:
    constraints = packet["constraints"] or ["none"]
    done_signals = packet["done_signals"] or ["none"]
    checks = result["cheapest_next_checks"] or ["none"]
    selected_work = result.get("selected_work_product")

    lines = [
        "# Consensus Report",
        "",
        "## Request",
        f"- Summary: {packet['request_summary']}",
        f"- Task kind: {packet['task_kind']}",
        f"- Mode: {packet['mode']}",
        "- Constraints:",
    ]
    lines.extend([f"  - {item}" for item in constraints])
    lines.append("- Done signals:")
    lines.extend([f"  - {item}" for item in done_signals])

    lines.extend(
        [
            "",
            "## Verdict",
            result["verdict"],
            "",
            "## Consensus Recommendation",
            result["consensus_recommendation"],
            "",
        ]
    )

    if packet.get("compose_contract"):
        compose_contract = packet["compose_contract"]
        lines.extend(
            [
                "## Compose Contract",
                f"- Macro: {compose_contract.get('macro_expression') or 'none'}",
                f"- Program: {compose_contract.get('program') or 'none'}",
                "- Expanded skills: " + (", ".join(compose_contract.get("expanded_skills", [])) or "none"),
                "- Required sections: "
                + (
                    ", ".join(
                        (compose_contract.get("response_profile") or {}).get("required_sections", [])
                    )
                    or "none"
                ),
                "",
            ]
        )

    if selected_work and selected_work.get("work_summary"):
        lines.extend(
            [
                "## Selected Work Product",
                f"- Agent: {selected_work['agent']}",
                f"- Fit score: {selected_work['fit_score']}",
                f"- Summary: {selected_work['work_summary']}",
                "- Output artifacts: " + (", ".join(selected_work.get("output_artifacts", [])) or "none"),
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Selected Work Product",
                f"- Selection status: {result.get('work_product_selection_status', 'withheld')}",
                f"- Reason: {result.get('work_product_selection_reason', 'none')}",
                "",
            ]
        )

    for title, key in (
        ("Accepted Keep", "accepted_keep"),
        ("Accepted Avoid", "accepted_avoid"),
        ("Provisional Keep", "provisional_keep"),
        ("Provisional Avoid", "provisional_avoid"),
        ("Unresolved", "unresolved"),
        ("Needs More Evidence", "needs_more_evidence"),
    ):
        lines.append(format_section(title, result[key]).rstrip())
        lines.append("")

    lines.append("## Cheapest Next Checks")
    for item in checks:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Agent Status")
    for agent, payload in result["agent_status"].items():
        lines.append(f"- {agent}: {payload['status']} (confidence={payload['confidence']})")
    if result.get("candidate_work_products"):
        lines.append("")
        lines.append("## Candidate Work Products")
        for item in result["candidate_work_products"]:
            lines.append(
                f"- {item['agent']}: fit={item['fit_score']} sections={'complete' if item['required_sections_complete'] else 'incomplete'} summary={item['work_summary'] or 'none'}"
            )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    root = skill_root()
    out_dir = Path(args.out_dir) if args.out_dir else root / "assets" / "runs" / now_stamp()
    ensure_dir(out_dir)

    contexts = load_context_files(args.context_file, args.max_context_chars)
    compose_contract = load_compose_contract(args, out_dir)
    packet = build_request_packet(args, contexts, compose_contract)
    write_text(out_dir / "request.packet.yaml", yaml_dump(packet) + "\n")
    blockers = compose_blockers(compose_contract)
    if blockers:
        write_json(out_dir / "contract.blockers.json", {"blockers": blockers})
        raise RuntimeError(
            "compose contract has unresolved required inputs: " + "; ".join(blockers)
        )

    schema_path = root / "assets" / "agent-response.schema.json"
    schema_text = read_text(schema_path)
    packet_text = format_request_packet_for_prompt(packet, contexts)

    round1_prompts = {
        agent: build_round1_prompt(agent, packet, packet_text, schema_text)
        for agent in AGENTS
    }

    if args.dry_run:
        for agent, prompt in round1_prompts.items():
            write_text(out_dir / f"{agent}.round1.prompt.txt", prompt)
        result = {
            "status": "dry-run",
            "out_dir": str(out_dir),
            "written": [str(out_dir / f"{agent}.round1.prompt.txt") for agent in AGENTS],
        }
        if compose_contract:
            result["compose_contract"] = str(out_dir / "compose.contract.json")
        write_json(out_dir / "dry-run.json", result)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    resolved = preflight_commands(args)
    capabilities = detect_cli_capabilities(resolved)
    write_json(out_dir / "cli.capabilities.json", capabilities)

    round1 = {}
    for agent in AGENTS:
        round1[agent] = run_one_agent(
            agent=agent,
            args=args,
            resolved_cmd=resolved[agent],
            prompt=round1_prompts[agent],
            schema_path=schema_path,
            schema_text=schema_text,
            out_dir=out_dir,
            round_name="round1",
            capabilities=capabilities,
        )

    disagreement_packet = build_disagreement_packet(round1)
    write_json(out_dir / "disagreement.packet.json", disagreement_packet)

    final_responses = round1
    if args.rounds == 2 and disagreement_packet.get("requires_rebuttal", True):
        round2 = {}
        for agent in AGENTS:
            prompt = build_round2_prompt(agent, packet, packet_text, schema_text, disagreement_packet)
            round2[agent] = run_one_agent(
                agent=agent,
                args=args,
                resolved_cmd=resolved[agent],
                prompt=prompt,
                schema_path=schema_path,
                schema_text=schema_text,
                out_dir=out_dir,
                round_name="round2",
                capabilities=capabilities,
            )
        final_responses = round2

    result = build_consensus_result(packet, final_responses, out_dir)
    selected_work = result.get("selected_work_product")
    if selected_work and selected_work.get("work_output"):
        work_product_path = out_dir / "consensus.work-product.md"
        write_text(work_product_path, selected_work["work_output"])
        result["artifacts"]["work_product"] = str(work_product_path)

    write_text(out_dir / "consensus.report.md", build_report(packet, result))
    write_json(out_dir / "consensus.result.json", result)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[OK] consensus artifacts written to {out_dir}")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - CLI should fail with concise error text
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
