#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from build_state_report import STATE_REPORT_PATH, render_state_report


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_ROOT = ROOT / "_registry"
SKILLS_ROOT = ROOT


ATOMIC_SKILLS = {
    "scout-baseline",
    "scout-facts",
    "ask-fix-prompt",
    "check-ship-risk",
    "scout-scope",
    "ship-commit",
    "doc-curate",
    "debug-find-root-cause",
    "doc-write",
    "plan-screen-map",
    "build-write-code",
    "doc-build-index",
    "build-make-faster",
    "build-until-done",
    "plan-dependency-rules",
    "plan-task-breakdown",
    "plan-why-build-this",
    "doc-publish-readme",
    "check-quality-scan",
    "ask-find-question",
    "ask-flip-assumption",
    "ask-break-it-down",
    "tidy-reorganize",
    "ship-check-hygiene",
    "ship-go-nogo",
    "ship-check-repo",
    "check-merge-ready",
    "check-security-holes",
    "check-delivered",
    "tidy-cut-fat",
    "plan-what-it-does",
    "plan-how-to-build",
    "test-design-cases",
    "test-find-gaps",
    "test-write-guards",
    "test-run-user-scenarios",
    "finish-until-done",
}

UTILITY_SKILLS = {
    "compose",
    "gemini",
    "plan-driven-delivery",
    "release-publish",
    "respond",
}

FAMILY_MAP = {
    "scout-baseline": "analysis",
    "scout-facts": "analysis",
    "scout-scope": "analysis",
    "debug-find-root-cause": "analysis",
    "plan-dependency-rules": "planning",
    "plan-task-breakdown": "planning",
    "plan-why-build-this": "planning",
    "plan-screen-map": "planning",
    "plan-what-it-does": "planning",
    "plan-how-to-build": "planning",
    "tidy-cut-fat": "planning",
    "tidy-reorganize": "planning",
    "build-write-code": "implementation",
    "build-make-faster": "implementation",
    "test-write-guards": "test",
    "test-run-user-scenarios": "test",
    "build-until-done": "completion",
    "finish-until-done": "completion",
    "check-quality-scan": "check-merge-ready",
    "check-merge-ready": "check-merge-ready",
    "check-ship-risk": "check-merge-ready",
    "check-security-holes": "check-merge-ready",
    "ship-check-repo": "release",
    "ship-check-hygiene": "release",
    "ship-go-nogo": "release",
    "check-delivered": "check-merge-ready",
    "test-find-gaps": "test",
    "test-design-cases": "test",
    "doc-write": "docs",
    "doc-build-index": "docs",
    "doc-publish-readme": "docs",
    "doc-curate": "docs",
    "ship-commit": "docs",
    "ask-find-question": "question",
    "ask-break-it-down": "question",
    "ask-flip-assumption": "question",
    "ask-fix-prompt": "question",
    "compose": "utility",
    "respond": "utility",
    "plan-driven-delivery": "utility",
    "release-publish": "utility",
    "gemini": "utility",
}

PROFILE_MAP = {
    "scout-baseline": "performance_report",
    "scout-facts": "analysis_report",
    "ask-find-question": "clarify_question",
    "ask-break-it-down": "question_stack",
    "ask-flip-assumption": "analysis_report",
    "ask-fix-prompt": "repair_report",
    "check-merge-ready": "review_findings",
    "check-ship-risk": "review_findings",
    "check-quality-scan": "review_findings",
    "debug-find-root-cause": "debug_report",
    "plan-dependency-rules": "planning_doc",
    "plan-task-breakdown": "planning_doc",
    "plan-why-build-this": "brief_contract",
    "plan-screen-map": "ia_contract",
    "build-write-code": "implementation_delta",
    "build-make-faster": "performance_report",
    "test-write-guards": "test_report",
    "test-design-cases": "test_report",
    "test-find-gaps": "review_findings",
    "test-run-user-scenarios": "analysis_report",
    "build-until-done": "analysis_report",
    "finish-until-done": "analysis_report",
    "check-security-holes": "security_report",
    "ship-check-repo": "analysis_report",
    "ship-check-hygiene": "analysis_report",
    "ship-go-nogo": "release_decision",
    "doc-write": "documentation_report",
    "doc-build-index": "documentation_report",
    "doc-publish-readme": "documentation_report",
    "doc-curate": "documentation_report",
    "plan-what-it-does": "spec_contract",
    "plan-how-to-build": "design_contract",
    "ship-commit": "commit_proposal",
    "compose": "generic",
    "respond": "generic",
    "plan-driven-delivery": "implementation_delta",
    "release-publish": "generic",
    "check-delivered": "self_verify_report",
    "tidy-reorganize": "implementation_delta",
    "tidy-cut-fat": "implementation_delta",
    "scout-scope": "clarify_question",
    "gemini": "external_verification",
}

PURPOSE_MAP = {
    "scout-baseline": "Capture the current performance baseline before optimization work starts.",
    "scout-facts": "Produce an evidence-first analysis without implementation or verdict work.",
    "debug-find-root-cause": "Reproduce a concrete failure, confirm root cause, and isolate the minimal fix path.",
    "scout-scope": "Turn vague requests into concrete goal, scope, constraints, and acceptance criteria.",
    "plan-dependency-rules": "Make allowed and forbidden dependency directions explicit before structural cleanup.",
    "plan-task-breakdown": "Create execution-ready plan and task artifacts.",
    "plan-why-build-this": "Write a short product brief that makes user, problem, success, and non-goals explicit.",
    "plan-screen-map": "Define hierarchy, navigation, and user-flow structure before detailed design and implementation.",
    "plan-what-it-does": "Write implementation-ready feature specifications with explicit scope, behavior, and acceptance checks.",
    "plan-how-to-build": "Write a buildable technical design with explicit boundaries, flows, trade-offs, and verification paths.",
    "tidy-cut-fat": "Identify and propose the smallest useful complexity reduction.",
    "tidy-reorganize": "Plan structure-preserving cleanup without changing behavior.",
    "build-write-code": "Apply code changes and emit verification-backed implementation evidence.",
    "build-make-faster": "Measure and improve performance bottlenecks.",
    "test-write-guards": "Write meaningful regression guards with execution evidence.",
    "test-design-cases": "Design a realistic behavior matrix before test writing.",
    "test-find-gaps": "Find missing regression protection in the current test surface.",
    "test-run-user-scenarios": "Simulate realistic user and agent scenarios against the framework surface.",
    "build-until-done": "Keep one bounded code-changing mission moving until its done contract is satisfied.",
    "finish-until-done": "Keep one bounded non-code mission moving until its done contract is satisfied.",
    "check-quality-scan": "Check code quality against a fixed checklist without replacing verdict review.",
    "check-merge-ready": "Issue a findings-first review verdict with evidence.",
    "check-ship-risk": "Assess release or gate risk with explicit evidence.",
    "check-security-holes": "Surface security issues and threat-relevant risks.",
    "ship-check-repo": "Check git repository and branch reality before release work begins.",
    "ship-check-hygiene": "Verify docs, legacy cleanup, and public-surface sync before release.",
    "ship-go-nogo": "Judge release safety and rollback readiness.",
    "check-delivered": "Perform final contract and evidence verification.",
    "doc-write": "Write or refresh non-root documentation in an explicit document form.",
    "doc-build-index": "Build hierarchical analysis docs and index files for modules, libraries, or papers.",
    "doc-publish-readme": "Publish a root README and localized project doc entrypoints.",
    "doc-curate": "Reorganize non-root docs with entry structure, navigation, and cleanup actions.",
    "ship-commit": "Generate precise commit proposals from completed changes.",
    "ask-find-question": "Turn fuzzy intent into one clear problem statement.",
    "ask-break-it-down": "Break one broad question into a prioritized question stack.",
    "ask-flip-assumption": "Generate challenge questions by reversing hidden assumptions.",
    "ask-fix-prompt": "Repair a question after a weak or wrong answer.",
    "compose": "Parse and normalize multi-skill macros into deterministic execution programs.",
    "respond": "Render the final user-facing response only.",
    "plan-driven-delivery": "Enforce synchronization between planning artifacts, task lifecycle, and implementation evidence.",
    "release-publish": "Execute release-only commit, tag, and release publication after gates pass.",
    "gemini": "Run the external Gemini workflow only when explicitly requested.",
}


def read_skill(skill_name: str) -> tuple[str, str]:
    text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
    desc = ""
    for line in text.splitlines()[:10]:
        if line.startswith("description:"):
            desc = line.split(":", 1)[1].strip().strip('"')
            break
    m = re.search(r"## Default Program\s+```text\s*(.*?)\s*```", text, re.S)
    default_program = m.group(1).strip() if m else "[orchestration-only]"
    return desc, default_program


def field(name: str, type_: str, required: bool, description: str) -> dict:
    return {"name": name, "type": type_, "required": required, "description": description}


def io_templates(skill: str) -> tuple[list[dict], list[dict], list[str], list[str], list[str], list[str], list[str]]:
    default_neutral = [
        "Separate evidence from recommendation.",
        "Do not invent defects or conclusions without evidence.",
        "Return no-finding or inconclusive when evidence is insufficient.",
    ]
    common_repo_input = [field("TARGET_SCOPE", "path|module|repo", True, "Exact target scope for the skill.")]
    templates = {
        "scout-facts": (
            common_repo_input + [
                field("ANALYSIS_GOAL", "root-cause|option-compare|structure-map|evidence-gap", True, "Exact analysis job."),
                field("QUESTION", "string", True, "Uncertainty or decision to resolve."),
            ],
            [
                field("OBSERVED_EVIDENCE", "list", True, "Observed facts grounded in files, logs, commands, or measurements."),
                field("INFERRED_FINDINGS", "list", True, "Interpretations derived from observed evidence."),
                field("OPTION_SET", "list", True, "Compared options with trade-offs."),
                field("RECOMMENDATION", "string", True, "Selected recommendation."),
            ],
            [],
            ["analysis-report.v1"],
            default_neutral,
            ["Need evidence-first analysis before implementation.", "Need option comparison or structure mapping."],
            ["Need direct code changes.", "Need final review verdict."],
        ),
        "debug-find-root-cause": (
            common_repo_input + [
                field("FAILURE_SYMPTOM", "string", True, "Observed failure symptom."),
                field("EXPECTED_BEHAVIOR", "string", True, "What should have happened."),
            ],
            [
                field("REPRO_STEPS", "list", True, "Cheapest reproduction steps."),
                field("CONFIRMED_CAUSE", "string", True, "Confirmed root cause or inconclusive result."),
                field("MINIMAL_FIX_DIRECTION", "string", True, "Narrow fix path."),
            ],
            [],
            ["debug-report.v1"],
            default_neutral,
            ["A concrete failure or crash exists.", "A reproducible RCA path is required."],
            ["The request is exploratory with no concrete failure.", "The request is new feature implementation."],
        ),
    }
    if skill in templates:
        return templates[skill]
    family = FAMILY_MAP.get(skill, "general")
    if family == "question":
        return (
            [
                field("TOPIC", "string", True, "Topic or question pack target."),
                field("TARGET_SCOPE", "topic|artifact", True, "Exact target scope."),
            ],
            [
                field("RESULT", "object", True, "Structured question artifact."),
                field("NEXT_STEP", "string", True, "Next recommended action."),
            ],
            [],
            [f"{skill}-artifact.v1"],
            default_neutral,
            [f"Need {skill} for question engineering."],
            ["Need direct implementation or repository modification."],
        )
    if family == "check-merge-ready":
        return (
            common_repo_input + [field("REVIEW_GOAL", "string", True, "Exact review or gate goal.")],
            [
                field("FINDINGS", "list", True, "Evidence-backed findings or explicit no-findings."),
                field("RISKS", "list", True, "Residual risks or gaps."),
            ],
            [],
            [f"{skill}-report.v1"],
            default_neutral,
            [f"Need {skill} review or gate output."],
            ["Need direct code implementation."],
        )
    if family == "implementation":
        return (
            common_repo_input + [field("CHANGE_GOAL", "string", True, "Exact change goal.")],
            [
                field("CHANGED_ARTIFACTS", "list", True, "Changed files or artifacts."),
                field("VERIFICATION", "list", True, "Verification results."),
            ],
            [],
            [f"{skill}-report.v1"],
            [
                "Do not claim success without verification evidence.",
                "Separate implemented change from optional future improvement.",
                "Mark incomplete verification explicitly.",
            ],
            [f"Need {skill} execution."],
            ["Need only analysis or verdict output."],
        )
    if family == "test":
        return (
            common_repo_input + [field("TEST_GOAL", "string", True, "Exact testing or scenario goal.")],
            [
                field("TEST_OUTPUT", "object", True, "Structured test or scenario artifact."),
                field("VERIFICATION", "list", True, "Executed evidence or scenario results."),
            ],
            [],
            [f"{skill}-artifact.v1"],
            [
                "Prefer observable behavior over implementation trivia.",
                "Do not invent coverage or pass signals without evidence.",
                "Keep scenarios and cases realistic enough to teach something.",
            ],
            [f"Need {skill} test output."],
            ["Need direct feature implementation unrelated to test or scenario work."],
        )
    if family == "completion":
        return (
            common_repo_input + [field("MISSION_GOAL", "string", True, "Exact bounded mission.")],
            [
                field("MISSION_STATUS", "continue|done|blocked", True, "Loop status."),
                field("DONE_CONDITION_STATUS", "list", True, "Per-condition evidence or gap."),
            ],
            [],
            ["completion-contract-loop-report.v1"],
            [
                "Do not claim completion without explicit proof.",
                "Prefer one smallest next pass over a backlog.",
                "Surface real blockers instead of guessing success.",
            ],
            [f"Need {skill} completion control."],
            ["Need broad orchestration without an explicit done contract."],
        )
    if family == "planning":
        return (
            common_repo_input + [field("GOAL", "string", True, "Exact planning target.")],
            [
                field("PLAN", "object", True, "Structured plan output."),
                field("TASKS", "list", True, "Task list or next steps."),
            ],
            [],
            [f"{skill}-artifact.v1"],
            default_neutral,
            [f"Need {skill} planning output."],
            ["Need direct code changes."],
        )
    if family == "docs":
        return (
            common_repo_input + [field("DOC_GOAL", "string", True, "Documentation or message goal.")],
            [
                field("DOC_OUTPUT", "object", True, "Documentation artifact."),
                field("RATIONALE", "string", True, "Why this output fits."),
            ],
            [],
            [f"{skill}-artifact.v1"],
            default_neutral,
            [f"Need {skill} artifact."],
            ["Need code execution or code verdict output."],
        )
    return (
        common_repo_input,
        [field("RESULT", "object", True, "Structured result artifact.")],
        [],
        [f"{skill}-artifact.v1"],
        default_neutral,
        [f"Need {skill}."],
        ["Different primary goal."],
    )


def build_entry(skill: str) -> dict:
    desc, default_program = read_skill(skill)
    required_inputs, structured_outputs, artifacts_in, artifacts_out, neutrality_rules, when_to_use, do_not_use = io_templates(skill)
    layer = "atomic" if skill in ATOMIC_SKILLS else "utility"
    return {
        "name": skill,
        "layer": layer,
        "family": FAMILY_MAP[skill],
        "job_type": skill,
        "description": desc,
        "purpose": PURPOSE_MAP[skill],
        "when_to_use": when_to_use,
        "do_not_use": do_not_use,
        "required_inputs": required_inputs,
        "structured_outputs": structured_outputs,
        "artifacts_in": artifacts_in,
        "artifacts_out": artifacts_out,
        "neutrality_rules": neutrality_rules,
        "response_profile": PROFILE_MAP.get(skill, "generic"),
        "default_prompt": f"${skill}",
        "default_program": default_program,
        "explicit_only": False,
        "source_path": f"skills/{skill}",
    }


def main() -> int:
    (REGISTRY_ROOT / "atomic").mkdir(parents=True, exist_ok=True)
    (REGISTRY_ROOT / "utility").mkdir(parents=True, exist_ok=True)
    (REGISTRY_ROOT / "workflow").mkdir(parents=True, exist_ok=True)
    for skill in sorted(ATOMIC_SKILLS | UTILITY_SKILLS):
        entry = build_entry(skill)
        out_dir = REGISTRY_ROOT / entry["layer"]
        out_file = out_dir / f"{skill}.json"
        if not out_file.exists():
            out_file.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    current = {
        layer: sorted(entry.stem for entry in (REGISTRY_ROOT / layer).glob("*.json"))
        for layer in ("atomic", "utility", "workflow")
    }
    index_file = REGISTRY_ROOT / "index.json"
    index_file.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    STATE_REPORT_PATH.write_text(render_state_report(), encoding="utf-8")
    print("Bootstrapped registry entries for existing skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
