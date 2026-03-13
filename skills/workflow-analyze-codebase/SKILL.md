---
name: workflow-analyze-codebase
description: "Workflow skill that chains structure analysis, complexity mapping, and dependency graph analysis into one complete codebase understanding session. Use when you need a full analytical picture before planning, refactoring, or design work."
---

# Workflow / Analyze Codebase

## Purpose
Compose structure, complexity, and dependency analysis into one explicit analytical workflow — producing a complete current-state picture before any planning or refactoring begins.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, coupling chains, and essential vs accidental complexity.

## Use When
- Need a full analytical picture of a codebase or module before planning or refactoring.
- Need structure, complexity, and dependency analysis in one pass.
- Need evidence-backed answers to "where is the complexity?", "what depends on what?", and "what are the key boundaries?".

## Do Not Use When
- Need direct code implementation without prior analysis.
- Need a review verdict rather than neutral analysis.
- Already have a clear structural picture and only need one specific analysis dimension.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Codebase or module to analyze.
- `ANALYSIS_GOAL` (structure|complexity|dependencies|full; optional): Primary analytical objective. Defaults to `full`.
- `KNOWN_CONCERNS` (list; optional): Known problem areas or questions to focus on.

## Input Contract Notes
- TARGET_SCOPE should be bounded enough that each subanalysis can cite concrete files or modules.
- ANALYSIS_GOAL narrows which subanalysis to emphasize; `full` runs all three at proportional depth.
- KNOWN_CONCERNS helps the workflow focus on the most relevant analytical dimensions first.

## Structured Outputs
- `STRUCTURE_MAP` (structure-analysis.v1; required): Boundary map, coupling findings, data flow traces, and hidden dependencies.
- `COMPLEXITY_MAP` (complexity-analysis.v1; required): Essential vs accidental complexity map with hotspot ranking.
- `DEPENDENCY_MAP` (dependency-analysis.v1; required): Full dependency graph with circular deps and coupling metrics.
- `ANALYTICAL_SUMMARY` (object; required; shape: {KEY_FINDING, HIGHEST_RISK_AREA, RECOMMENDED_NEXT_STEP}): Synthesized findings across all three analyses.
- `EXPANDED_ATOMIC_PATH` (list; required; shape: {SKILL}): Actual atomic path executed by the workflow.

## Output Contract Notes
- STRUCTURE_MAP, COMPLEXITY_MAP, and DEPENDENCY_MAP should be consistent — findings from one should be traceable in the others.
- ANALYTICAL_SUMMARY should synthesize across all three analyses, not just repeat one.
- EXPANDED_ATOMIC_PATH must preserve execution order.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: structure-analysis.v1, complexity-analysis.v1, dependency-analysis.v1

## Neutrality Rules
- Preserve the neutrality rules of each underlying analysis skill.
- Do not turn findings into a redesign prescription — deliver the analytical map only.
- Keep workflow output inspectable by preserving the explicit subanalysis trail.

## Execution Constraints
- Do not patch code from this workflow — analysis only.
- If a required subanalysis cannot run, surface that gap in EXPANDED_ATOMIC_PATH.
- Keep each subanalysis bounded to its stated dimension before synthesizing.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

단계별 결과:
- analyze-structure → 주요 경계와 결합도 요약
- analyze-complexity → 복잡도 핫스팟 목록
- analyze-dependencies → 순환 의존성 및 결합 지표

종합 요약:
- 핵심 발견: [가장 중요한 것]
- 가장 위험한 영역: [어디]
- 다음 작업 권고: [무엇부터]

단계 실패 시: 멈추고 무엇이 막혔는지 질문.

끝에: "[가장 위험한 영역] 바로 리뷰 또는 리팩터링 시작할까요?"

## Mandatory Rules
- Expose the expanded atomic path explicitly.
- Keep each subanalysis neutral — no verdict, no redesign prescription.

## Expansion
- `$analyze-structure`
- `$analyze-complexity`
- `$analyze-dependencies`

## Example Invocation
```text
$workflow-analyze-codebase
SCOPE: src/
GOAL: full
```
