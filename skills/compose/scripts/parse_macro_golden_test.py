#!/usr/bin/env python3
"""Golden tests for compose macro parser."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List

PARSER = Path(__file__).resolve().with_name("parse_macro.py")


@dataclass
class Case:
    name: str
    macro: str
    should_succeed: bool
    check: Callable[[subprocess.CompletedProcess[str], dict], None]


def run_parser(macro: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PARSER), "--macro", macro, "--format", "json"],
        text=True,
        capture_output=True,
    )


def must(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_analyze_minimal(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["parsed"]["skills"] == ["scout-facts"], "skills mismatch")
    must(payload["parsed"]["input_mode"] == "macro", "input mode mismatch")
    must(payload["response_profile"]["profile_id"] == "analysis_report", "profile mismatch")
    must(payload["program"]["lens"] == "kahneman-tversky", "analyze lens mismatch")
    must(payload["resolved"]["lens_source"] == "atomic-default", "lens source mismatch")
    must(payload["program"]["stages"] == ["preflight", "detect", "analyze", "review", "handoff", "audit"], "stage mismatch")


def check_compose_analyze_orchestration_only(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["profile_id"] == "generic", "profile mismatch")
    must(payload["response_profile"]["is_composite"] is True, "composite flag mismatch")
    must(payload["resolved"]["normalized_scope"] == "diff", "normalized scope mismatch")
    must(payload["contract_outputs"]["PROGRAM"] == payload["program_one_liner"], "contract program mismatch")
    must("build-write-code" not in payload["program"]["stages"], "compose default program should not expand with explicit domain skills")


def check_unknown_skill_hint(proc: subprocess.CompletedProcess[str], _payload: dict) -> None:
    must(proc.returncode != 0, "expected failure for unknown skill")
    must("Did you mean $compose?" in _payload["errors"][0], "missing unknown-skill hint")


def check_removed_entry_syntax(proc: subprocess.CompletedProcess[str], _payload: dict) -> None:
    must(proc.returncode != 0, "removed entry syntax should fail")
    must("Unknown skill" in _payload["errors"][0], "removed entry syntax error message mismatch")


def check_clarify_prompt_tail(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["parsed"]["prompt_tail"] == "요구사항 애매함", "prompt tail mismatch")
    must(payload["response_profile"]["profile_id"] == "clarify_question", "profile mismatch")


def check_question_clarify_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["parsed"]["skills"] == ["ask-find-question"], "skills mismatch")
    must(payload["response_profile"]["profile_id"] == "clarify_question", "profile mismatch")
    must(payload["program"]["lens"] == "inversion-focus", "ask-find-question lens mismatch")


def check_plan_driven_delivery_implement_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "build-write-code", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "generic", "profile mismatch")
    policies = payload["program"]["policy"]
    must("deterministic-output" in policies, "implementation policy should stay deterministic")
    must(payload["parsed"]["docs"] == ["docs/IMPLEMENTATION-PLAN.md", "docs/TASKS.md"], "docs capture mismatch")


def check_simplifier_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "tidy-cut-fat", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "generic", "profile mismatch")


def check_curate_docs_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["parsed"]["docs"] == ["docs"], "@docs token parsing mismatch")
    must(payload["program"]["scope"] == "paths(docs)", "scope mismatch for doc-curate")
    must(payload["response_profile"]["primary_skill"] == "doc-curate", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "generic", "profile mismatch")


def check_wf_question_ready(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["parsed"]["skills"] == ["wf-ask-sharpen"], "skills mismatch")
    must(payload["response_profile"]["primary_skill"] == "wf-ask-sharpen", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "question_stack", "profile mismatch")
    must(payload["program"]["lens"] == "popper-falsification", "workflow lens mismatch")
    must(
        payload["parsed"]["expanded_skills"] == [
            "ask-find-question",
            "ask-break-it-down",
            "ask-flip-assumption",
        ],
        "workflow expansion mismatch",
    )


def check_wf_question_map(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["parsed"]["skills"] == ["wf-ask-get-clear"], "skills mismatch")
    must(payload["response_profile"]["primary_skill"] == "wf-ask-get-clear", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "question_stack", "profile mismatch")
    must(payload["program"]["lens"] == "inversion-focus", "workflow lens mismatch")
    must(
        payload["parsed"]["expanded_skills"] == [
            "ask-find-question",
            "ask-break-it-down",
        ],
        "workflow expansion mismatch",
    )


def check_wf_project_review(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "wf-check-full-review", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "generic", "profile mismatch")
    must(payload["program"]["lens"] == "kahneman-tversky", "workflow lens mismatch")
    expanded = payload["parsed"]["expanded_skills"]
    must("tidy-find-magic-numbers" in expanded, "missing tidy-find-magic-numbers expansion")
    must("tidy-find-copies" in expanded, "missing tidy-find-copies expansion")
    must("check-merge-ready" in expanded, "missing review expansion")
    must("check-quality-scan" not in expanded, "wf-check-full-review should stay narrow by default")


def check_workflow_duplicate_collapse(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    expanded = payload["parsed"]["expanded_skills"]
    must(expanded.count("check-merge-ready") == 1, "duplicate review should be collapsed after expansion")
    warnings = payload.get("warnings", [])
    must(any("Collapsed duplicate skill `$check-merge-ready`" in w for w in warnings), "missing duplicate collapse warning")


def check_wf_project_debug(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "wf-debug-this", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "debug_report", "profile mismatch")
    must(payload["program"]["lens"] == "feynman", "workflow lens mismatch")
    must(
        payload["parsed"]["expanded_skills"] == [
            "debug-map-blast-radius",
            "debug-find-root-cause",
            "test-find-gaps",
        ],
        "workflow expansion mismatch",
    )


def check_wf_project_checklist_review(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "wf-check-with-checklist", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "review_findings", "profile mismatch")
    expanded = payload["parsed"]["expanded_skills"]
    must("wf-check-full-review" not in expanded, "nested workflow names should be flattened")
    must("check-quality-scan" in expanded, "checklist expansion missing")
    must("check-merge-ready" in expanded, "review expansion missing")


def check_wf_project_improvement_map(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "wf-tidy-find-improvements", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "analysis_report", "profile mismatch")
    must(payload["program"]["lens"] == "hickey-carmack", "workflow lens mismatch")
    must(payload["resolved"]["lens_source"] == "workflow-default", "lens source mismatch")
    must(
        payload["parsed"]["expanded_skills"] == ["tidy-find-copies", "tidy-find-magic-numbers", "tidy-cut-fat", "tidy-reorganize"],
        "workflow expansion mismatch",
    )
    must(
        payload["contract_outputs"]["EXPANDED_SKILLS"] == payload["parsed"]["expanded_skills"],
        "contract expanded skills mismatch",
    )


def check_scope_contract_map_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "scout-boundaries", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "planning_doc", "profile mismatch")


def check_baseline_metric_capture_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "scout-baseline", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "performance_report", "profile mismatch")


def check_test_design_cases_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "test-design-cases", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "test_report", "profile mismatch")


def check_test_write_guards_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "test-write-guards", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "test_report", "profile mismatch")


def check_test_find_gaps_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "test-find-gaps", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "review_findings", "profile mismatch")


def check_test_run_user_scenarios_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "test-run-user-scenarios", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "analysis_report", "profile mismatch")


def check_doc_inventory_scan_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "doc-find-all", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "documentation_report", "profile mismatch")


def check_knowledge_index_docs_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "doc-build-index", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "documentation_report", "profile mismatch")
    must(payload["program"]["lens"] == "nielsen-norman", "doc-build-index lens mismatch")


def check_project_readme_localize_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "doc-publish-readme", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "documentation_report", "profile mismatch")
    must(payload["program"]["lens"] == "feynman-teaching", "doc-publish-readme lens mismatch")


def check_product_brief_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "plan-why-build-this", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "brief_contract", "profile mismatch")
    must(payload["program"]["lens"] == "christensen-jtbd", "plan-why-build-this lens mismatch")


def check_information_architecture_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "plan-screen-map", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "ia_contract", "profile mismatch")
    must(payload["program"]["lens"] == "nielsen-norman", "plan-screen-map lens mismatch")


def check_spec_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "plan-what-it-does", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "spec_contract", "profile mismatch")
    must(payload["program"]["lens"] == "minto-pyramid", "spec lens mismatch")


def check_technical_design_doc_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "plan-how-to-build", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "design_contract", "profile mismatch")
    must(payload["program"]["lens"] == "hickey-carmack", "plan-how-to-build lens mismatch")


def check_release_repo_check_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "ship-check-repo", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "analysis_report", "profile mismatch")
    must(payload["program"]["lens"] == "release-gatekeeper", "ship-check-repo lens mismatch")


def check_release_readiness_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "ship-go-nogo", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "release_decision", "profile mismatch")
    must(payload["program"]["lens"] == "release-gatekeeper", "ship-go-nogo lens mismatch")


def check_wf_release_review(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "wf-ship-ready-check", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "release_decision", "profile mismatch")
    must(payload["program"]["lens"] == "release-gatekeeper", "workflow lens mismatch")
    must(
        payload["parsed"]["expanded_skills"] == [
            "ship-check-repo",
            "ship-check-hygiene",
            "ship-go-nogo",
        ],
        "workflow expansion mismatch",
    )


def check_wf_release_ship(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "wf-ship-it", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "generic", "profile mismatch")
    must(payload["program"]["lens"] == "release-gatekeeper", "workflow lens mismatch")
    must(
        payload["parsed"]["expanded_skills"] == [
            "ship-check-repo",
            "ship-check-hygiene",
            "ship-go-nogo",
            "release-publish",
        ],
        "workflow expansion mismatch",
    )


def check_release_publish_profile(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "release-publish", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "generic", "profile mismatch")
    must(payload["program"]["lens"] == "release-gatekeeper", "release-publish lens mismatch")


def check_generic_required_sections(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "check-delivered", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "self_verify_report", "profile mismatch")
    must(
        payload["response_profile"]["required_sections"]
        == ["결과", "막힌 것 또는 수정 필요 항목", "검증 근거", "남은 위험", "다음에 할 것(필요 시)"],
        "required sections parsing mismatch",
    )


def check_respond_canonical_policy(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["response_profile"]["primary_skill"] == "respond", "primary skill mismatch")
    policies = payload["program"]["policy"]
    must(
        "response-contract{plain-korean,feynman-clear,actionable,core-first,short-sentences,plain-words,concrete-details}" in policies,
        "respond should use canonical concrete-details response-contract policy",
    )


def check_docs_scope_tail(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["parsed"]["docs"] == ["docs/IMPLEMENTATION-PLAN.md", "docs/TASKS.md"], "docs capture mismatch")
    must(payload["parsed"]["prompt_tail"] == "그리고 계속 진행", "prompt tail mismatch")
    must(payload["program"]["scope"] == "paths(docs/IMPLEMENTATION-PLAN.md,docs/TASKS.md)", "scope mismatch")


def check_bracket_prompt_and_docs(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["parsed"]["prompt_tail"] == "skills 폴더 구조 분석", "bracket prompt parsing mismatch")
    must(payload["parsed"]["docs"] == ["docs/IMPLEMENTATION-PLAN.md"], "doc parsing mismatch with bracket prompt")
    must(payload["program"]["scope"] == "paths(docs/IMPLEMENTATION-PLAN.md)", "scope mismatch for bracket/doc combo")


def check_nested_bracket_and_escape(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["parsed"]["prompt_tail"] == "[A+B] [raw]", "nested/escaped bracket payload mismatch")
    must(payload["parsed"]["docs"] == ["docs/TASKS.md"], "doc parsing mismatch with nested bracket")


def check_at_folder_and_custom_prompt(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["parsed"]["docs"] == ["src"], "@folder token should be parsed as scope path")
    must(payload["parsed"]["prompt_tail"] == "구조 단순화", "custom prompt mismatch")
    must(payload["response_profile"]["primary_skill"] == "tidy-cut-fat", "primary skill mismatch")
    must(payload["response_profile"]["profile_id"] == "generic", "profile mismatch")


def check_simplifier_implement_combo(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["parsed"]["docs"] == ["src"], "@folder token should be parsed as scope path")
    must(payload["parsed"]["prompt_tail"] == "바로 수정", "custom prompt mismatch in implement combo")
    must(payload["response_profile"]["primary_skill"] == "build-write-code", "implement should be selected as primary skill")
    must(payload["response_profile"]["profile_id"] == "generic", "profile mismatch")


def check_unclosed_bracket_fallback(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    must(payload["parsed"]["docs"] == ["docs/TASKS.md"], "unclosed bracket should not swallow doc token")
    must(payload["parsed"]["prompt_tail"] == "[닫히지않음", "unclosed bracket prompt parsing mismatch")
    warnings = payload.get("warnings", [])
    must(any("Detected unclosed bracket prompt block" in w for w in warnings), "missing unclosed bracket warning")


def check_contract_output_aliases(proc: subprocess.CompletedProcess[str], payload: dict) -> None:
    must(proc.returncode == 0, f"expected success, got {proc.returncode}")
    contract = payload["contract_outputs"]
    must(contract["INPUT_MODE"] == "macro", "contract input mode mismatch")
    must(contract["PARSED_SKILLS"] == payload["parsed"]["skills"], "parsed skills alias mismatch")
    must(contract["EFFECTIVE_SKILLS"] == payload["parsed"]["effective_skills"], "effective skills alias mismatch")
    must(contract["PARSED_DOC_INPUTS"] == payload["parsed"]["docs"], "doc alias mismatch")
    must(contract["PROMPT_TAIL"] == payload["parsed"]["prompt_tail"], "prompt alias mismatch")
    must(contract["NORMALIZED_SCOPE"] == payload["resolved"]["normalized_scope"], "scope alias mismatch")
    must(contract["LENS_SOURCE"] == payload["resolved"]["lens_source"], "lens source alias mismatch")
    must(contract["STRUCTURAL_WARNINGS"] == payload["warnings"], "warnings alias mismatch")
    must(contract["STRUCTURAL_ERRORS"] == payload["errors"], "errors alias mismatch")


def parse_payload(proc: subprocess.CompletedProcess[str]) -> dict:
    if not proc.stdout.strip():
        return {}
    return json.loads(proc.stdout)


def main() -> int:
    cases: List[Case] = [
        Case("analyze-minimal", "$scout-facts", True, check_analyze_minimal),
        Case("compose-analyze-orchestration-only", "$compose $scout-facts", True, check_compose_analyze_orchestration_only),
        Case("wf-ask-sharpen", "$wf-ask-sharpen", True, check_wf_question_ready),
        Case("wf-check-full-review", "$compose $wf-check-full-review @src", True, check_wf_project_review),
        Case("workflow-duplicate-collapse", "$wf-check-full-review + $check-merge-ready @src", True, check_workflow_duplicate_collapse),
        Case("wf-debug-this", "$wf-debug-this", True, check_wf_project_debug),
        Case("wf-check-with-checklist", "$wf-check-with-checklist", True, check_wf_project_checklist_review),
        Case("wf-tidy-find-improvements", "$wf-tidy-find-improvements", True, check_wf_project_improvement_map),
        Case("scope-contract-map-profile", "$scout-boundaries", True, check_scope_contract_map_profile),
        Case("baseline-metric-capture-profile", "$scout-baseline", True, check_baseline_metric_capture_profile),
        Case("test-design-cases-profile", "$test-design-cases", True, check_test_design_cases_profile),
        Case("test-write-guards-profile", "$test-write-guards", True, check_test_write_guards_profile),
        Case("test-find-gaps-profile", "$test-find-gaps", True, check_test_find_gaps_profile),
        Case("test-run-user-scenarios-profile", "$test-run-user-scenarios", True, check_test_run_user_scenarios_profile),
        Case("doc-inventory-scan-profile", "$doc-find-all", True, check_doc_inventory_scan_profile),
        Case("knowledge-index-docs-profile", "$doc-build-index", True, check_knowledge_index_docs_profile),
        Case("project-readme-localize-profile", "$doc-publish-readme", True, check_project_readme_localize_profile),
        Case("product-brief-profile", "$plan-why-build-this", True, check_product_brief_profile),
        Case("information-architecture-profile", "$plan-screen-map", True, check_information_architecture_profile),
        Case("spec-profile", "$plan-what-it-does", True, check_spec_profile),
        Case("technical-design-doc-profile", "$plan-how-to-build", True, check_technical_design_doc_profile),
        Case("release-repo-check-profile", "$ship-check-repo", True, check_release_repo_check_profile),
        Case("release-readiness-profile", "$ship-go-nogo", True, check_release_readiness_profile),
        Case("wf-ship-ready-check", "$wf-ship-ready-check", True, check_wf_release_review),
        Case("wf-ship-it", "$wf-ship-it", True, check_wf_release_ship),
        Case("release-publish-profile", "$release-publish", True, check_release_publish_profile),
        Case("unknown-skill-hint", "$composer + $scout-facts", False, check_unknown_skill_hint),
        Case("clarify-prompt-tail", "$scout-scope 요구사항 애매함", True, check_clarify_prompt_tail),
        Case("question-clarify-profile", "$ask-find-question", True, check_question_clarify_profile),
        Case("wf-ask-get-clear", "$wf-ask-get-clear", True, check_wf_question_map),
        Case(
            "plan-driven-delivery-implement-profile",
            "$plan-driven-delivery $build-write-code $check-delivered docs/IMPLEMENTATION-PLAN.md docs/TASKS.md",
            True,
            check_plan_driven_delivery_implement_profile,
        ),
        Case("simplifier-profile", "$compose $tidy-cut-fat $check-delivered", True, check_simplifier_profile),
        Case("curate-docs-profile", "$compose $doc-curate @docs", True, check_curate_docs_profile),
        Case("generic-required-sections", "$check-delivered", True, check_generic_required_sections),
        Case("respond-canonical-policy", "$respond", True, check_respond_canonical_policy),
        Case("removed-entry-syntax", "$phase:check-merge-ready", False, check_removed_entry_syntax),
        Case("docs-scope-tail", "$build-write-code docs/IMPLEMENTATION-PLAN.md docs/TASKS.md 그리고 계속 진행", True, check_docs_scope_tail),
        Case("bracket-prompt-and-docs", "$compose $scout-facts $scout-scope $check-delivered [skills 폴더 구조 분석] @docs/IMPLEMENTATION-PLAN.md", True, check_bracket_prompt_and_docs),
        Case("nested-bracket-and-escape", "$compose $scout-facts [[A\\+B] \\[raw\\]] @docs/TASKS.md", True, check_nested_bracket_and_escape),
        Case("at-folder-and-custom-prompt", "$compose $tidy-cut-fat @src [구조 단순화]", True, check_at_folder_and_custom_prompt),
        Case("simplifier-implement-combo", "$compose $tidy-cut-fat @src [바로 수정] $build-write-code", True, check_simplifier_implement_combo),
        Case("unclosed-bracket-fallback", "$compose $scout-facts [닫히지않음 @docs/TASKS.md", True, check_unclosed_bracket_fallback),
        Case("contract-output-aliases", "$compose + $wf-tidy-find-improvements + @src + [구조 분석]", True, check_contract_output_aliases),
    ]

    failures = []
    for case in cases:
        proc = run_parser(case.macro)
        payload = parse_payload(proc)
        try:
            if case.should_succeed:
                must(proc.returncode == 0, f"expected success, got {proc.returncode}")
            else:
                must(proc.returncode != 0, "expected failure, got success")
            case.check(proc, payload)
            print(f"[PASS] {case.name}")
        except Exception as exc:
            failures.append((case.name, str(exc), proc.stderr.strip(), proc.stdout.strip()))
            print(f"[FAIL] {case.name}: {exc}")

    if failures:
        print("\nFailures:")
        for name, err, stderr, stdout in failures:
            print(f"- {name}: {err}")
            if stderr:
                print(f"  stderr: {stderr}")
            if stdout:
                print(f"  stdout: {stdout}")
        return 1

    print("\nAll golden tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
