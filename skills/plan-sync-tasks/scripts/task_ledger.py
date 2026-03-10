#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional


OPEN_STATUSES = {"TODO", "DOING"}
BLOCKED_STATUS = "BLOCKED"
DONE_STATUS = "DONE"


def split_table_row(line: str) -> List[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_task_rows(tasks_path: Path) -> List[Dict[str, object]]:
    lines = tasks_path.read_text(encoding="utf-8").splitlines()
    rows: List[Dict[str, object]] = []
    current_section: Optional[str] = None
    in_task_table = False

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("## "):
            current_section = stripped[3:].strip()
            in_task_table = False
            continue
        if stripped.startswith("| ID |"):
            in_task_table = True
            continue
        if in_task_table and stripped.startswith("|---"):
            continue
        if in_task_table and stripped.startswith("|"):
            cells = split_table_row(stripped)
            if len(cells) < 7:
                continue
            row_id, status, task, module, depends_on, done_when, verification = cells[:7]
            rows.append(
                {
                    "section": current_section,
                    "line": idx,
                    "task_id": row_id,
                    "status": status.upper(),
                    "task": task,
                    "module": module,
                    "depends_on": depends_on,
                    "done_when": done_when,
                    "verification": verification,
                }
            )
            continue
        if in_task_table and stripped and not stripped.startswith("|"):
            in_task_table = False

    return rows


def build_verification_map(verification_cell: str) -> List[Dict[str, object]]:
    checks = [item.strip() for item in verification_cell.split(";") if item.strip()]
    return [
        {
            "CHECK": check,
            "ORDER": index,
            "PASS_CONDITION": "check succeeds and supports the task row",
        }
        for index, check in enumerate(checks, start=1)
    ]


def infer_plan_summary(plan_path: Optional[Path]) -> Dict[str, object]:
    if plan_path is None or not plan_path.exists():
        return {"path": str(plan_path) if plan_path else None, "headline": None}
    for line in plan_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return {"path": str(plan_path), "headline": stripped[2:].strip()}
    return {"path": str(plan_path), "headline": None}


def command_summary(tasks_path: Path, plan_path: Optional[Path]) -> int:
    rows = parse_task_rows(tasks_path)
    open_rows = [row for row in rows if row["status"] in OPEN_STATUSES]
    blocked_rows = [row for row in rows if row["status"] == BLOCKED_STATUS]
    done_rows = [row for row in rows if row["status"] == DONE_STATUS]
    payload = {
        "plan": infer_plan_summary(plan_path),
        "tasks_path": str(tasks_path),
        "counts": {
            "total": len(rows),
            "open": len(open_rows),
            "blocked": len(blocked_rows),
            "done": len(done_rows),
        },
        "open_tasks": open_rows,
        "blocked_tasks": blocked_rows,
        "next_task": open_rows[0] if open_rows else None,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def command_next(tasks_path: Path, plan_path: Optional[Path]) -> int:
    rows = parse_task_rows(tasks_path)
    open_rows = [row for row in rows if row["status"] in OPEN_STATUSES]
    next_row = open_rows[0] if open_rows else None
    payload = {
        "plan": infer_plan_summary(plan_path),
        "tasks_path": str(tasks_path),
        "open_task_count": len(open_rows),
        "selected_task_ids": [next_row["task_id"]] if next_row else [],
        "next_task": next_row,
        "verification_map": build_verification_map(str(next_row["verification"])) if next_row else [],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse markdown task ledgers and select the next actionable task.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("summary", "next"):
        sub = subparsers.add_parser(name)
        sub.add_argument("--tasks", required=True, type=Path, help="Path to the markdown task ledger.")
        sub.add_argument("--plan", type=Path, default=None, help="Optional plan document path.")

    args = parser.parse_args()
    if args.command == "summary":
        return command_summary(args.tasks, args.plan)
    if args.command == "next":
        return command_next(args.tasks, args.plan)
    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
