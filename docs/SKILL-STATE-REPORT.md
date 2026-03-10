# Skill State Report

> Generated from `skills/_registry/index.json` and registry entries. Do not edit manually.

## Summary

- registry 기준 현재 구성: `atomic 46 / utility 5 / workflow 8 / total 59`
- `State` 열은 registry field가 아니라 generated classification이다.
- classification rule:
  - atomic + `split_candidates` 있음 -> `broad-entrypoint`
  - atomic + `split_candidates` 없음 -> `atomic-stable`
  - utility -> `utility-stable`
  - workflow -> `workflow-stable`

## State Labels

- `atomic-stable`: 하나의 문제와 하나의 산출물에 집중된 atomic skill
- `broad-entrypoint`: direct entry는 허용하지만 더 좁은 skill이 있으면 우선 대체해야 하는 skill
- `utility-stable`: orchestration/rendering/execution-governance 전용 utility
- `workflow-stable`: explicit `expands_to`를 가진 named workflow

## Atomic Skills

| Skill | Family | Job | State | Required Inputs | Structured Outputs | Current State |
|---|---|---|---|---|---|---|
| ask-break-it-down | question | ask-break-it-down | atomic-stable | `PROBLEM_STATEMENT`, `AUDIENCE`, `CONSTRAINTS` | `QUESTION_LAYERS`, `FIRST_PRINCIPLES`, `DATA_CONTROL_VIEW`, `CORE_QUESTION`, `NEXT_RECOMMENDED_SKILL` | Single-problem atomic skill. |
| ask-find-question | question | ask-find-question | atomic-stable | `RAW_TOPIC`, `AUDIENCE`, `CONSTRAINTS` | `FOG_KEYS`, `NEGATIVE_SPACE`, `PRIMARY_CONSTRAINT`, `PROBLEM_STATEMENT`, `NEXT_RECOMMENDED_SKILL` | Single-problem atomic skill. |
| ask-fix-prompt | question | ask-fix-prompt | atomic-stable | `TOPIC`, `QUESTION_OR_STACK`, `BAD_ANSWER`, `GOAL` | `FAILURE_CLASS`, `WHY_WRONG`, `WHAT_WAS_MISSING`, `MINIMAL_QUESTION_DELTA`, `REPAIRED_PROMPT`, `RE_RUN_RECOMMENDATION` | Single-problem atomic skill. |
| ask-flip-assumption | question | ask-flip-assumption | atomic-stable | `CORE_QUESTION`, `ASSUMPTIONS`, `CONSTRAINTS` | `ASSUMPTION_LIST`, `REVERSAL_TESTS`, `CHALLENGE_QUESTIONS`, `EXPECTED_FEEDBACK`, `NEXT_RECOMMENDED_SKILL` | Single-problem atomic skill. |
| test-write-guards | test | test-write-guards | broad-entrypoint | `TEST_GOAL`, `TARGET_SCOPE`, `TARGET_BEHAVIORS`, `FAILURE_PATHS` | `TEST_MATRIX`, `ADDED_TESTS`, `VERIFICATION_RESULTS` | Direct entrypoint. Prefer `test-design-cases`, `test-find-gaps` when scope is narrower. |
| test-run-user-scenarios | test | test-run-user-scenarios | broad-entrypoint | `SYSTEM_UNDER_TEST`, `TARGET_SCOPE`, `PRIMARY_USERS`, `SCENARIO_COUNT`, `FAILURE_CLASSES`, `KNOWN_CONSTRAINTS` | `USE_CASE_MATRIX`, `FAILURE_CASES`, `ODD_CASES`, `EXECUTION_LOG`, `USABILITY_FINDINGS`, `NEXT_FIXES` | Direct entrypoint. Prefer `test-design-cases`, `test-find-gaps`, `check-delivered` when scope is narrower. |
| build-make-faster | implementation | build-make-faster | broad-entrypoint | `TARGET_SCOPE`, `METRIC_NAME`, `PERFORMANCE_BUDGET`, `BASELINE_EVIDENCE` | `METRIC_BASELINE`, `BOTTLENECK_EVIDENCE`, `BEFORE_AFTER_RESULTS` | Direct entrypoint. Prefer `scout-baseline` when scope is narrower. |
| build-until-done | completion | build-until-done | broad-entrypoint | `MISSION_GOAL`, `TARGET_SCOPE`, `DONE_CONDITION`, `CURRENT_EVIDENCE`, `COMPANION_SKILLS`, `MAX_PASSES`, `CONSTRAINTS` | `MISSION_STATUS`, `DONE_CONDITION_STATUS`, `NEXT_PASS`, `BLOCKERS`, `LOOP_EXIT_REASON` | Direct entrypoint. Prefer `check-delivered`, `plan-task-breakdown`, `plan-driven-delivery` when scope is narrower. |
| build-write-code | implementation | build-write-code | broad-entrypoint | `CHANGE_GOAL`, `TARGET_SCOPE`, `TASK_IDS`, `TASK_SOURCE`, `VERIFICATION_MAP`, `CONSTRAINTS` | `CHANGED_ARTIFACTS`, `VERIFICATION_RESULTS`, `VERIFICATION_GAPS`, `IMPLEMENTATION_EVIDENCE_NOTES` | Direct entrypoint. Prefer `plan-verify-order`, `test-design-cases`, `scout-baseline` when scope is narrower. |
| check-delivered | check-merge-ready | check-delivered | atomic-stable | `VERIFY_TARGETS`, `EXPECTED_CONTRACTS`, `VERIFY_SCOPE`, `KNOWN_EVIDENCE` | `BLOCKERS`, `VERIFIED_CHECKS`, `EVIDENCE_GAPS`, `P2_RESIDUALS`, `FINAL_VERIFICATION_STATUS` | Single-problem atomic skill. |
| check-failure-paths | check-merge-ready | check-failure-paths | atomic-stable | `TARGET_SCOPE`, `FAILURE_MODES` | `ERROR_PATH_FINDINGS`, `MISSING_GUARDS`, `RECOVERY_GAPS` | Single-problem atomic skill. |
| check-merge-ready | check-merge-ready | check-merge-ready | broad-entrypoint | `REVIEW_GOAL`, `TARGET_SCOPE`, `CHANGE_INTENT`, `KNOWN_TEST_SIGNAL`, `CONSTRAINTS` | `FINDINGS`, `TESTING_GAPS`, `VERDICT` | Direct entrypoint. Prefer `tidy-find-magic-numbers`, `tidy-find-copies`, `check-module-walls`, `check-failure-paths`, `test-find-gaps` when scope is narrower. |
| test-find-gaps | test | test-find-gaps | atomic-stable | `TARGET_SCOPE`, `TEST_FOCUS` | `MISSING_TEST_SCENARIOS`, `CURRENT_COVERAGE_NOTES`, `TEST_PRIORITY_ORDER` | Single-problem atomic skill. |
| check-module-walls | check-merge-ready | check-module-walls | atomic-stable | `TARGET_SCOPE`, `BOUNDARY_KIND` | `BOUNDARY_CONTRACTS`, `LEAKED_ASSUMPTIONS`, `HARDENING_ACTIONS` | Single-problem atomic skill. |
| check-quality-scan | check-merge-ready | check-quality-scan | broad-entrypoint | `CHECK_SCOPE`, `CHANGE_GOAL`, `TARGET_AREA`, `KNOWN_EVIDENCE` | `CHECKLIST_TABLE`, `FINDINGS_SUMMARY`, `UNKNOWN_ITEMS` | Direct entrypoint. Prefer `tidy-find-magic-numbers`, `tidy-find-copies`, `check-module-walls`, `check-failure-paths`, `test-find-gaps` when scope is narrower. |
| check-security-holes | check-merge-ready | check-security-holes | atomic-stable | `SECURITY_GOAL`, `TARGET_SCOPE`, `ASSETS_OR_BOUNDARIES`, `KNOWN_EVIDENCE` | `THREAT_MODEL`, `SECURITY_FINDINGS`, `MITIGATION_VERIFICATION` | Single-problem atomic skill. |
| check-ship-risk | check-merge-ready | check-ship-risk | broad-entrypoint | `AUDIT_GOAL`, `TARGET_SCOPE`, `CHANGE_INTENT`, `KNOWN_GATE_SIGNAL` | `GATE_STATUS`, `AUDIT_FINDINGS`, `RISK_RECOMMENDATION` | Direct entrypoint. Prefer `check-merge-ready`, `check-security-holes`, `ship-go-nogo` when scope is narrower. |
| debug-find-root-cause | analysis | debug-find-root-cause | broad-entrypoint | `FAILURE_SYMPTOM`, `TARGET_SCOPE`, `EXPECTED_BEHAVIOR`, `REPRO_STATUS`, `KNOWN_EVIDENCE` | `REPRO_STEPS`, `OBSERVED_VS_EXPECTED`, `CONFIRMED_CAUSE`, `MINIMAL_FIX_DIRECTION`, `REGRESSION_GUARD` | Direct entrypoint. Prefer `debug-map-blast-radius`, `check-failure-paths`, `test-find-gaps` when scope is narrower. |
| debug-map-blast-radius | analysis | debug-map-blast-radius | atomic-stable | `TARGET_SCOPE`, `FAILURE_SYMPTOM`, `EXPECTED_BEHAVIOR`, `REPRO_HINTS` | `REPRO_WINDOW`, `IMPACTED_PATHS`, `OBSERVED_VS_EXPECTED`, `NEXT_DEBUG_ENTRY_POINTS` | Single-problem atomic skill. |
| doc-build-index | docs | doc-build-index | atomic-stable | `DOCSET_KIND`, `DOC_FORM`, `TARGET_SCOPE`, `INDEX_DEPTH`, `INDEX_LAYOUT`, `AUDIENCE`, `AUDIENCE_LEVEL`, `EVIDENCE_LINKS` | `ANALYSIS_DOCS`, `LOCAL_INDEX_FILES`, `GUIDE_INDEX_FILES`, `COVERAGE_GAPS` | Single-problem atomic skill. |
| doc-curate | docs | doc-curate | broad-entrypoint | `CURATION_GOAL`, `TARGET_SCOPE`, `ENTRY_DOC_STYLE`, `INVENTORY_SCOPE` | `DOC_INVENTORY`, `DOC_ENTRY_STRUCTURE`, `DOC_NAVIGATION_MAP`, `CLEANUP_ACTIONS` | Direct entrypoint. Prefer `doc-find-all` when scope is narrower. |
| doc-find-all | docs | doc-find-all | atomic-stable | `TARGET_SCOPE`, `INVENTORY_GOAL` | `DOC_INVENTORY`, `ORPHAN_OR_DUPLICATE_SET`, `NEXT_CURATION_TARGETS` | Single-problem atomic skill. |
| doc-publish-readme | docs | doc-publish-readme | atomic-stable | `PROJECT_SCOPE`, `README_GOAL`, `AUDIENCE`, `AUDIENCE_LEVEL`, `PRIMARY_LANGUAGE`, `TARGET_LANGUAGES`, `SOURCE_DOCS` | `ROOT_README_PATH`, `LANGUAGE_DOCS`, `LANGUAGE_SELECTOR_LINKS`, `DOC_PORTAL_MAP` | Single-problem atomic skill. |
| doc-write | docs | doc-write | broad-entrypoint | `DOC_GOAL`, `DOC_FORM`, `TARGET_SCOPE`, `AUDIENCE`, `AUDIENCE_LEVEL`, `EVIDENCE_LINKS` | `DOC_PLAN`, `WRITTEN_DOCS`, `EVIDENCE_MAP` | Direct entrypoint. Prefer `doc-build-index`, `doc-publish-readme` when scope is narrower. |
| plan-dependency-rules | planning | plan-dependency-rules | atomic-stable | `TARGET_SCOPE`, `CURRENT_BOUNDARY_NOTES` | `ALLOWED_DEPENDENCIES`, `FORBIDDEN_DEPENDENCIES`, `TRANSITION_STEPS` | Single-problem atomic skill. |
| plan-how-to-build | planning | plan-how-to-build | atomic-stable | `DESIGN_SCOPE`, `IMPLEMENTATION_GOAL`, `REQUIREMENT_SOURCES`, `SYSTEM_BOUNDARIES`, `CONSTRAINTS`, `ROLLBACK_OR_MIGRATION` | `DESIGN_SUMMARY`, `BOUNDARY_MAP`, `DATA_AND_CONTROL_FLOW`, `DECISIONS_AND_TRADEOFFS`, `RISKS_AND_VERIFICATION`, `MIGRATION_AND_ROLLBACK` | Single-problem atomic skill. |
| plan-task-breakdown | planning | plan-task-breakdown | broad-entrypoint | `PLANNING_GOAL`, `TARGET_SCOPE`, `DONE_CONDITION`, `PLAN_OUTPUT_PATH`, `TASKS_OUTPUT_PATH`, `ARTIFACT_MODE`, `CONSTRAINTS`, `EXISTING_ARTIFACTS` | `IMPLEMENTATION_PLAN_PATH`, `TASKS_ARTIFACT_PATH`, `TASK_ROWS`, `DECISION_GATES` | Direct entrypoint. Prefer `scout-boundaries`, `plan-verify-order` when scope is narrower. |
| plan-screen-map | planning | plan-screen-map | atomic-stable | `IA_SCOPE`, `PRIMARY_USERS`, `CONTENT_OBJECTS`, `ENTRY_POINTS`, `KNOWN_FLOWS`, `NAV_CONSTRAINTS` | `IA_SUMMARY`, `HIERARCHY_MAP`, `NAVIGATION_PATHS`, `CORE_FLOWS`, `LABELING_NOTES` | Single-problem atomic skill. |
| test-design-cases | test | test-design-cases | atomic-stable | `TARGET_SCOPE`, `TEST_GOAL`, `TARGET_BEHAVIORS` | `HAPPY_PATH_CASES`, `EDGE_CASES`, `FAILURE_CASES` | Single-problem atomic skill. |
| plan-verify-order | planning | plan-verify-order | atomic-stable | `TARGET_SCOPE`, `CHANGE_GOAL`, `RISK_AREAS` | `NARROW_CHECKS`, `BROADER_CHECKS`, `STOP_CONDITIONS` | Single-problem atomic skill. |
| plan-what-it-does | planning | plan-what-it-does | atomic-stable | `FEATURE_SCOPE`, `USER_OUTCOME`, `REQUIRED_BEHAVIORS`, `ACCEPTANCE_SCENARIOS`, `OUT_OF_SCOPE`, `CONSTRAINTS` | `SPEC_SUMMARY`, `FUNCTIONAL_REQUIREMENTS`, `ACCEPTANCE_CRITERIA`, `EDGE_CASES`, `NON_REQUIREMENTS` | Single-problem atomic skill. |
| plan-why-build-this | planning | plan-why-build-this | atomic-stable | `BRIEF_SCOPE`, `PROBLEM_STATEMENT`, `TARGET_AUDIENCE`, `DESIRED_OUTCOMES`, `SUCCESS_SIGNALS`, `CONSTRAINTS`, `KNOWN_NON_GOALS` | `BRIEF_SUMMARY`, `USER_JOBS`, `OUTCOME_PRIORITIES`, `NON_GOALS`, `OPEN_ASSUMPTIONS` | Single-problem atomic skill. |
| scout-baseline | planning | scout-baseline | atomic-stable | `TARGET_SCOPE`, `METRIC_NAME`, `MEASUREMENT_METHOD`, `BUDGET_HINT` | `METRIC_DEFINITION`, `BASELINE_RESULT`, `PERFORMANCE_BUDGET` | Single-problem atomic skill. |
| scout-boundaries | planning | scout-boundaries | atomic-stable | `REQUEST`, `TARGET_SCOPE`, `KNOWN_CONSTRAINTS` | `GOAL`, `IN_SCOPE`, `OUT_OF_SCOPE`, `DONE_CONDITION` | Single-problem atomic skill. |
| scout-facts | analysis | scout-facts | broad-entrypoint | `ANALYSIS_GOAL`, `TARGET_SCOPE`, `QUESTION`, `KNOWN_EVIDENCE`, `CONSTRAINTS` | `OBSERVED_EVIDENCE`, `INFERRED_FINDINGS`, `OPTION_SET`, `RECOMMENDATION`, `NEXT_VERIFICATION_STEPS` | Direct entrypoint. Prefer `debug-map-blast-radius` when scope is narrower. |
| scout-scope | analysis | scout-scope | broad-entrypoint | `REQUEST`, `TARGET_SCOPE`, `KNOWN_CONSTRAINTS`, `KNOWN_DONE_CONDITION` | `CLARIFYING_QUESTIONS`, `DRAFT_SCOPE_CONTRACT`, `OUT_OF_SCOPE` | Direct entrypoint. Prefer `scout-boundaries` when scope is narrower. |
| ship-check-hygiene | release | ship-check-hygiene | atomic-stable | `HYGIENE_SCOPE`, `REQUIRED_DOCS`, `SURFACE_CONTRACTS`, `LEGACY_PATTERNS` | `HYGIENE_FINDINGS`, `DOC_GATE_STATUS`, `SURFACE_SYNC_STATUS`, `REQUIRED_CLEANUPS` | Single-problem atomic skill. |
| ship-check-repo | release | ship-check-repo | atomic-stable | `TARGET_BRANCHES`, `REMOTE_NAME`, `TAG_INTENT`, `REPO_EXPECTATIONS` | `REPO_FACTS`, `BRANCH_MAP`, `REPO_BLOCKERS`, `REPO_RELEASE_STATUS` | Single-problem atomic skill. |
| ship-commit | docs | ship-commit | atomic-stable | `DIFF_SUMMARY`, `CHANGE_INTENT`, `SCOPE_HINT`, `BREAKING_CHANGE` | `TOP_CANDIDATE`, `ALTERNATIVES`, `BODY_FOOTER_NOTES` | Single-problem atomic skill. |
| ship-go-nogo | release | ship-go-nogo | atomic-stable | `RELEASE_SCOPE`, `ROLLOUT_PLAN`, `ROLLBACK_PATH`, `KNOWN_GATES` | `BLAST_RADIUS`, `ROLLBACK_CHECKLIST`, `RELEASE_DECISION` | Single-problem atomic skill. |
| tidy-cut-fat | planning | tidy-cut-fat | broad-entrypoint | `TARGET_SCOPE`, `SIMPLIFICATION_GOAL`, `PRESERVE_BEHAVIOR`, `KNOWN_PAIN` | `COMPLEXITY_INVENTORY`, `SIMPLIFICATION_PLAN`, `BEHAVIOR_GUARDS` | Direct entrypoint. Prefer `tidy-why-complex`, `tidy-find-copies`, `tidy-find-magic-numbers` when scope is narrower. |
| tidy-find-copies | check-merge-ready | tidy-find-copies | atomic-stable | `TARGET_SCOPE`, `DUPLICATION_KIND` | `DUPLICATION_CLUSTERS`, `SAFE_MERGE_OPPORTUNITIES`, `KEEP_SEPARATE_REASONS` | Single-problem atomic skill. |
| tidy-find-magic-numbers | check-merge-ready | tidy-find-magic-numbers | atomic-stable | `TARGET_SCOPE`, `EXTRACTION_POLICY` | `EXTRACTABLE_CONSTANTS`, `REUSE_OPPORTUNITIES`, `EXTRACTION_BLOCKERS` | Single-problem atomic skill. |
| tidy-reorganize | planning | tidy-reorganize | broad-entrypoint | `TARGET_SCOPE`, `REFACTOR_BOUNDARY`, `BEHAVIOR_INVARIANTS`, `CONSTRAINTS` | `TARGET_DEPENDENCY_RULES`, `ATOMIC_REFACTOR_STEPS`, `ROLLBACK_PATH` | Direct entrypoint. Prefer `plan-dependency-rules`, `tidy-find-copies`, `check-module-walls`, `tidy-find-magic-numbers` when scope is narrower. |
| tidy-why-complex | planning | tidy-why-complex | atomic-stable | `TARGET_SCOPE`, `SIMPLIFICATION_GOAL` | `ESSENTIAL_COMPLEXITY`, `ACCIDENTAL_COMPLEXITY`, `SIMPLIFICATION_CANDIDATES` | Single-problem atomic skill. |
| finish-until-done | completion | finish-until-done | broad-entrypoint | `MISSION_GOAL`, `TARGET_SCOPE`, `DONE_CONDITION`, `CURRENT_EVIDENCE`, `COMPANION_SKILLS`, `MAX_PASSES`, `CONSTRAINTS` | `MISSION_STATUS`, `DONE_CONDITION_STATUS`, `NEXT_PASS`, `BLOCKERS`, `LOOP_EXIT_REASON` | Direct entrypoint. Prefer `check-delivered`, `doc-write`, `plan-task-breakdown`, `check-merge-ready` when scope is narrower. |

## Utility Skills

| Skill | Family | Job | State | Required Inputs | Structured Outputs | Current State |
|---|---|---|---|---|---|---|
| compose | orchestration | compose | utility-stable | `MACRO_EXPRESSION`, `LENS_OVERRIDE`, `SCOPE_OVERRIDE` | `INPUT_MODE`, `PARSED_SKILLS`, `EFFECTIVE_SKILLS`, `EXPANDED_SKILLS`, `PARSED_DOC_INPUTS`, `PROMPT_TAIL`, `NORMALIZED_SCOPE`, `LENS_SOURCE`, `PROGRAM`, `RESPONSE_PROFILE`, `STRUCTURAL_WARNINGS`, `STRUCTURAL_ERRORS` | Utility-only skill. |
| gemini | external-delegation | gemini | utility-stable | `GEMINI_MODE`, `GEMINI_GOAL`, `TARGET_SCOPE`, `SESSION_ID` | `GEMINI_FINDINGS`, `LOCAL_COMPARISON`, `CONFLICTS` | Utility-only skill. |
| plan-driven-delivery | execution-governance | plan-driven-delivery | utility-stable | `IMPLEMENTATION_PLAN_PATH`, `TASKS_PATH`, `SELECTED_TASK_IDS`, `KNOWN_EVIDENCE`, `IMPLEMENTATION_EVIDENCE_NOTES` | `TASK_LINK_MAP`, `TASK_STATUS_UPDATES`, `SYNC_STATUS` | Utility-only skill. |
| release-publish | release-governance | release-publish | utility-stable | `SOURCE_BRANCH`, `TARGET_BRANCH`, `RELEASE_BUMP`, `RELEASE_TAG`, `REQUIRED_CHECKS`, `PUBLISH_TARGET`, `REMOTE_NAME`, `LEGACY_CLEANUP_SCOPE`, `RELEASE_NOTES_SOURCE`, `RELEASE_NOTES_PATH` | `CLEANUP_REPORT`, `RELEASE_COMMITS`, `PUBLISH_RESULTS`, `RELEASE_STATUS` | Utility-only skill. |
| respond | rendering | respond | utility-stable | `RESPONSE_PROFILE`, `STAGE_PAYLOADS`, `LANGUAGE_PREFERENCE` | `FINAL_RESPONSE`, `RENDERED_SECTIONS` | Utility-only skill. |

## Workflow Skills

| Skill | Family | Job | State | Required Inputs | Structured Outputs | Current State |
|---|---|---|---|---|---|---|
| wf-ask-get-clear | question-workflow | wf-ask-get-clear | workflow-stable | `TOPIC`, `AUDIENCE`, `CONSTRAINTS` | `PROBLEM_STATEMENT`, `QUESTION_STACK`, `EXPANDED_ATOMIC_PATH` | Canonical workflow. |
| wf-ask-sharpen | question-workflow | wf-ask-sharpen | workflow-stable | `TOPIC`, `AUDIENCE`, `CONSTRAINTS` | `PROBLEM_STATEMENT`, `CORE_QUESTION`, `CHALLENGE_QUESTIONS`, `EXPANDED_ATOMIC_PATH` | Canonical workflow. |
| wf-check-full-review | project-workflow | wf-check-full-review | workflow-stable | `TARGET_SCOPE`, `REVIEW_FOCUS` | `REVIEW_FINDINGS`, `CHECK_REPORTS`, `INTEGRATE_OR_HOLD` | Canonical workflow. |
| wf-check-with-checklist | project-workflow | wf-check-with-checklist | workflow-stable | `TARGET_SCOPE`, `REVIEW_FOCUS` | `REVIEW_FINDINGS`, `CHECKLIST_TABLE`, `INTEGRATE_OR_HOLD` | Canonical workflow. |
| wf-debug-this | project-workflow | wf-debug-this | workflow-stable | `TARGET_SCOPE`, `FAILURE_SYMPTOM`, `EXPECTED_BEHAVIOR` | `FAILURE_SURFACE_MAP`, `DEBUG_REPORT`, `TEST_GAP_REPORT` | Canonical workflow. |
| wf-ship-it | release-workflow | wf-ship-it | workflow-stable | `TARGET_BRANCHES`, `ROLLOUT_PLAN`, `ROLLBACK_PATH`, `RELEASE_BUMP`, `RELEASE_TAG`, `RELEASE_SCOPE`, `HYGIENE_SCOPE`, `REQUIRED_DOCS`, `LEGACY_PATTERNS`, `SURFACE_CONTRACTS`, `KNOWN_GATES`, `REQUIRED_CHECKS`, `PUBLISH_TARGET`, `REMOTE_NAME`, `RELEASE_NOTES_SOURCE`, `RELEASE_NOTES_PATH` | `CHECK_REPORTS`, `RELEASE_DECISION`, `CLEANUP_REPORT`, `RELEASE_COMMITS`, `PUBLISH_RESULTS`, `RELEASE_STATUS`, `EXPANDED_EXECUTION_PATH` | Canonical workflow. |
| wf-ship-ready-check | release-workflow | wf-ship-ready-check | workflow-stable | `RELEASE_SCOPE`, `TARGET_BRANCHES`, `HYGIENE_SCOPE`, `ROLLOUT_PLAN`, `ROLLBACK_PATH`, `REQUIRED_DOCS`, `LEGACY_PATTERNS`, `REMOTE_NAME`, `TAG_INTENT`, `KNOWN_GATES`, `SURFACE_CONTRACTS` | `REPO_RELEASE_STATUS`, `HYGIENE_SUMMARY`, `CHECK_REPORTS`, `RELEASE_DECISION`, `EXPANDED_ATOMIC_PATH` | Canonical workflow. |
| wf-tidy-find-improvements | project-workflow | wf-tidy-find-improvements | workflow-stable | `TARGET_SCOPE`, `IMPROVEMENT_GOAL` | `IMPROVEMENT_FINDINGS`, `SIMPLIFICATION_DIRECTION`, `EVIDENCE_BASIS`, `EXPANDED_ATOMIC_PATH`, `NEXT_IMPLEMENTATION_STEP` | Canonical workflow. |
