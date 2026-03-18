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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a two-round three-agent consensus flow across Codex, Claude Code, and Gemini CLI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--task", required=True, help="Bounded mission or decision question")
    parser.add_argument(
        "--mode",
        default="analysis",
        choices=("analysis", "plan", "implement-review"),
        help="Mission mode",
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


def build_request_packet(args: argparse.Namespace, contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
    done_signals = args.done_signal[:] or [
        "Return one defensible recommendation, preserve disagreements, and list cheapest next checks"
    ]
    return {
        "request_summary": args.task.strip(),
        "mode": args.mode,
        "scope": {
            "in": ["the bounded mission in --task", "supplied context files", "supplied local evidence"],
            "out": ["product code edits", "silent majority vote", "fabricated certainty"],
        },
        "constraints": args.constraint[:],
        "done_signals": done_signals,
        "local_evidence": args.local_evidence[:],
        "open_questions": [],
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
    }


def format_request_packet_for_prompt(packet: Dict[str, Any], contexts: List[Dict[str, Any]]) -> str:
    lines = [
        f"request_summary: {packet['request_summary']}",
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
    return textwrap.dedent(
        f"""
        You are participating in a three-agent consensus engine.

        Agent: {agent}
        Lens: {lens}

        Mission:
        Produce one bounded recommendation for the request packet below.

        Hard rules:
        - Round 1 is independent. Do not assume or simulate peer answers.
        - Do not invoke skills, slash commands, subagents, or hidden delegation loops.
        - Do not expose chain-of-thought. Return only conclusions, atomic decisions, and explicit uncertainty.
        - This is analysis-only. Do not edit files.
        - Every item in `must_keep` and `must_avoid` must be a short atomic decision sentence.
        - Use `grounded` only for claims anchored in explicit evidence or specifications.
        - Use `reasoned` for justified inference.
        - Use `speculative` for plausible but weakly grounded ideas.
        - Prefer saying uncertain over guessing.

        Lens guidance:
        {agent_guidance}

        Request packet:
        {packet_text}

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
                items.append(
                    {
                        "agent": agent,
                        "polarity": polarity,
                        "statement": entry.get("statement", "").strip(),
                        "why": entry.get("why", "").strip(),
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

    return {
        "anonymous_proposal_summaries": proposal_summaries,
        "decision_clusters": packet_clusters,
        "instructions": [
            "Challenge weak claims instead of following the majority.",
            "Update only when the evidence packet justifies it.",
            "Keep must_keep and must_avoid atomic and comparison-friendly.",
        ],
    }


def build_round2_prompt(
    agent: str,
    packet_text: str,
    schema_text: str,
    disagreement_packet: Dict[str, Any],
) -> str:
    lens = LENSES[agent]
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
        - Keep `must_keep` and `must_avoid` atomic and comparison-friendly.
        - Preserve explicit uncertainty where the tie cannot be broken.

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

    for key in ("summary", "proposal"):
        if key in data and not isinstance(data[key], str):
            errors.append(f"{key} must be a string")

    for key in ("must_keep", "must_avoid", "assumptions", "uncertainties", "next_checks"):
        if key in data and not isinstance(data[key], list):
            errors.append(f"{key} must be a list")

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
            if "statement" in item and not isinstance(item["statement"], str):
                errors.append(f"{field}[{index}].statement must be a string")
            if "why" in item and not isinstance(item["why"], str):
                errors.append(f"{field}[{index}].why must be a string")
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

    for item in cluster["items"]:
        target = keep_scores if item["polarity"] == "keep" else avoid_scores
        prev = target.get(item["agent"], 0.0)
        target[item["agent"]] = max(prev, item["score"])

    keep_count = len(keep_scores)
    avoid_count = len(avoid_scores)
    keep_total = round(sum(keep_scores.values()), 3)
    avoid_total = round(sum(avoid_scores.values()), 3)
    keep_avg = (keep_total / keep_count) if keep_count else 0.0
    avoid_avg = (avoid_total / avoid_count) if avoid_count else 0.0

    classification = "unresolved"
    rationale = "insufficient aligned evidence"

    if keep_count and avoid_count:
        classification = "unresolved"
        rationale = "direct keep/avoid collision"
    elif keep_count == 3 and keep_avg >= 1.4:
        classification = "accepted_keep"
        rationale = "3 keep / 0 avoid with adequate average evidence"
    elif avoid_count == 3 and avoid_avg >= 1.4:
        classification = "accepted_avoid"
        rationale = "0 keep / 3 avoid with adequate average evidence"
    elif keep_count >= 2 and avoid_count == 0 and keep_total >= 2.5:
        classification = "provisional_keep"
        rationale = "2 keep / 0 avoid with stronger aggregate evidence"
    elif avoid_count >= 2 and keep_count == 0 and avoid_total >= 2.5:
        classification = "provisional_avoid"
        rationale = "0 keep / 2 avoid with stronger aggregate evidence"
    elif keep_count == 3 and keep_avg < 1.4:
        classification = "provisional_keep"
        rationale = "unanimous keep but weak evidence"
    elif avoid_count == 3 and avoid_avg < 1.4:
        classification = "provisional_avoid"
        rationale = "unanimous avoid but weak evidence"

    return {
        "statement": cluster["statement"],
        "classification": classification,
        "rationale": rationale,
        "keep_by": sorted(keep_scores.keys()),
        "avoid_by": sorted(avoid_scores.keys()),
        "keep_strength": keep_total,
        "avoid_strength": avoid_total,
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


def build_consensus_result(
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

    if (accepted_keep or accepted_avoid) and not unresolved:
        verdict = "strong-consensus"
    elif accepted_keep or accepted_avoid or provisional_keep or provisional_avoid:
        verdict = "provisional-consensus"
    else:
        verdict = "no-consensus"

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
        "cheapest_next_checks": aggregate_next_checks(final_responses),
        "agent_status": agent_status,
        "artifacts": {
            "out_dir": str(out_dir),
            "report": str(out_dir / "consensus.report.md"),
            "result": str(out_dir / "consensus.result.json"),
        },
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
    return "\n".join(lines) + "\n"


def build_report(
    packet: Dict[str, Any],
    result: Dict[str, Any],
) -> str:
    constraints = packet["constraints"] or ["none"]
    done_signals = packet["done_signals"] or ["none"]
    checks = result["cheapest_next_checks"] or ["none"]

    lines = [
        "# Consensus Report",
        "",
        "## Request",
        f"- Summary: {packet['request_summary']}",
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

    for title, key in (
        ("Accepted Keep", "accepted_keep"),
        ("Accepted Avoid", "accepted_avoid"),
        ("Provisional Keep", "provisional_keep"),
        ("Provisional Avoid", "provisional_avoid"),
        ("Unresolved", "unresolved"),
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
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    root = skill_root()
    out_dir = Path(args.out_dir) if args.out_dir else root / "assets" / "runs" / now_stamp()
    ensure_dir(out_dir)

    contexts = load_context_files(args.context_file, args.max_context_chars)
    packet = build_request_packet(args, contexts)
    write_text(out_dir / "request.packet.yaml", yaml_dump(packet) + "\n")

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
    if args.rounds == 2:
        round2 = {}
        for agent in AGENTS:
            prompt = build_round2_prompt(agent, packet_text, schema_text, disagreement_packet)
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

    result = build_consensus_result(final_responses, out_dir)
    write_json(out_dir / "consensus.result.json", result)
    write_text(out_dir / "consensus.report.md", build_report(packet, result))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[OK] consensus artifacts written to {out_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
