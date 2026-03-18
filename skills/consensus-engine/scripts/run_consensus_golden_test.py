#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import run_consensus as rc


RUNNER = Path(__file__).resolve().with_name("run_consensus.py")


def decision(statement: str, anchors: list[str], confidence: float = 1.0) -> dict:
    return {
        "statement": statement,
        "why": f"Need to preserve `{statement}`.",
        "anchors": anchors,
        "support": "grounded",
        "confidence": confidence,
    }


def payload(
    *,
    summary: str,
    work_summary: str,
    work_output: str,
    confidence: float,
    must_keep: list[dict] | None = None,
    must_avoid: list[dict] | None = None,
) -> dict:
    return {
        "summary": summary,
        "proposal": summary,
        "work_summary": work_summary,
        "work_output": work_output,
        "output_artifacts": [],
        "must_keep": must_keep or [],
        "must_avoid": must_avoid or [],
        "assumptions": [],
        "uncertainties": [],
        "next_checks": [],
        "confidence": confidence,
    }


class ConsensusGoldenTest(unittest.TestCase):
    def test_explicit_starter_inputs_unblock_build_and_guard_macro(self) -> None:
        with tempfile.TemporaryDirectory(prefix="consensus-explicit-inputs-") as tmpdir:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--task",
                    "Draft the best auth refresh redesign proposal",
                    "--macro-expression",
                    "$workflow-build-implement-and-guard + @src/auth + [GOAL: keep the session after refresh] + [DONE: session refresh test => stay signed in after refresh] + [CONTEXT: keep the session after refresh during an active login] + [CONSTRAINTS: keep public API stable]",
                    "--done-signal",
                    "Return one selected work product and remaining conflicts",
                    "--dry-run",
                    "--out-dir",
                    tmpdir,
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
            contract = json.loads((Path(tmpdir) / "compose.contract.json").read_text(encoding="utf-8"))
            starter_inputs = contract["contract_outputs"]["STARTER_INPUT_VALUES"]
            self.assertIn("DONE", starter_inputs)
            self.assertIn("CONTEXT", starter_inputs)
            self.assertEqual(contract["contract_outputs"]["MISSING_REQUIRED_INPUTS"], [])
            self.assertFalse((Path(tmpdir) / "contract.blockers.json").exists())

    def test_compose_missing_inputs_block_dry_run(self) -> None:
        with tempfile.TemporaryDirectory(prefix="consensus-blocker-") as tmpdir:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--task",
                    "Draft the best auth refresh redesign proposal",
                    "--macro-expression",
                    "$workflow-build-implement-and-guard + @src/auth + [keep public API stable]",
                    "--done-signal",
                    "Return one selected work product and remaining conflicts",
                    "--dry-run",
                    "--out-dir",
                    tmpdir,
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn(
                "compose contract has unresolved required inputs",
                proc.stderr or proc.stdout,
            )
            self.assertTrue((Path(tmpdir) / "compose.contract.json").exists())
            self.assertTrue((Path(tmpdir) / "contract.blockers.json").exists())

    def test_negative_statement_normalization_avoids_false_conflict(self) -> None:
        anchors = ["constraints: Do not inspect repository files"]
        responses = {
            "codex": payload(
                summary="codex",
                work_summary="codex output",
                work_output="codex output",
                confidence=0.9,
                must_keep=[decision("Do not inspect repository files", anchors, 0.95)],
            ),
            "claude": payload(
                summary="claude",
                work_summary="claude output",
                work_output="claude output",
                confidence=0.9,
                must_avoid=[decision("Do not inspect repository files", anchors, 0.95)],
            ),
            "gemini": payload(
                summary="gemini",
                work_summary="gemini output",
                work_output="gemini output",
                confidence=0.9,
                must_avoid=[decision("Do not inspect repository files", anchors, 0.95)],
            ),
        }
        result = rc.build_consensus_result({"task_kind": "decision"}, responses, Path("/tmp/consensus-test"))
        self.assertEqual(result["verdict"], "strong-consensus")
        self.assertFalse(result["unresolved"])
        self.assertEqual(result["accepted_avoid"][0]["statement"], "inspect repository files")

    def test_done_signal_anchor_counts_toward_evidence_floor(self) -> None:
        anchors = ["done_signals: Return one report and one next check"]
        responses = {
            agent: payload(
                summary=agent,
                work_summary=f"{agent} output",
                work_output=f"{agent} output",
                confidence=0.9,
                must_keep=[decision("return one report", anchors, 0.95)],
            )
            for agent in rc.AGENTS
        }
        result = rc.build_consensus_result({"task_kind": "decision"}, responses, Path("/tmp/consensus-test"))
        self.assertEqual(result["verdict"], "strong-consensus")
        self.assertEqual(result["accepted_keep"][0]["statement"], "return one report")

    def test_no_consensus_withholds_selected_work_product(self) -> None:
        responses = {
            "codex": payload(
                summary="codex",
                work_summary="codex output",
                work_output="codex output",
                confidence=0.99,
                must_keep=[decision("change auth flow", ["path: src/auth.py"], 0.99)],
            ),
            "claude": payload(
                summary="claude",
                work_summary="claude output",
                work_output="claude output",
                confidence=0.98,
                must_keep=[decision("rewrite session docs", ["path: docs/session.md"], 0.98)],
            ),
            "gemini": payload(
                summary="gemini",
                work_summary="gemini output",
                work_output="gemini output",
                confidence=0.97,
                must_keep=[decision("split retry policy", ["path: src/retry.py"], 0.97)],
            ),
        }
        result = rc.build_consensus_result({"task_kind": "decision"}, responses, Path("/tmp/consensus-test"))
        self.assertEqual(result["verdict"], "no-consensus")
        self.assertIsNone(result["selected_work_product"])
        self.assertEqual(result["work_product_selection_status"], "withheld")

    def test_compose_selection_requires_required_sections(self) -> None:
        keep = [decision("keep public API stable", ["path: src/auth.py"], 0.95)]
        packet = {
            "task_kind": "compose-execution",
            "compose_contract": {
                "response_profile": {
                    "required_sections": ["결과", "변경 사항"],
                }
            },
        }
        responses = {
            "codex": payload(
                summary="codex",
                work_summary="complete codex draft",
                work_output="# 결과\n안\n# 변경 사항\n패치",
                confidence=0.9,
                must_keep=keep,
            ),
            "claude": payload(
                summary="claude",
                work_summary="incomplete claude draft",
                work_output="# 결과\n안",
                confidence=0.99,
                must_keep=keep,
            ),
            "gemini": payload(
                summary="gemini",
                work_summary="complete gemini draft",
                work_output="# 결과\n안\n# 변경 사항\n패치",
                confidence=0.85,
                must_keep=keep,
            ),
        }
        result = rc.build_consensus_result(packet, responses, Path("/tmp/consensus-test"))
        self.assertEqual(result["verdict"], "strong-consensus")
        self.assertEqual(result["selected_work_product"]["agent"], "codex")
        claude = next(item for item in result["candidate_work_products"] if item["agent"] == "claude")
        self.assertFalse(claude["required_sections_complete"])


if __name__ == "__main__":
    unittest.main()
