---
name: analyze-module-bounds
description: "Analyze whether module, API, or layer boundaries have explicit contracts, clear ownership, and no leaking responsibilities. Use when the goal is neutral boundary analysis, not a review verdict."
---

# Analyze / Module Bounds

## Purpose
Produce a neutral boundary analysis showing current contract clarity, ownership split, and leaking assumptions — without verdict or hardening prescription.

## Default Program
```text
[stages: preflight>detect>analyze>review>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: uncle-bob | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `uncle-bob` because it keeps the work aligned with: Strong boundaries, explicit dependency direction, and contract clarity.

## Use When
- Need to understand current contract clarity at a module or API boundary.
- Need to map ownership and responsibility separation across layers.
- Need boundary evidence before refactoring or design decisions.

## Do Not Use When
- Need a broad code review across unrelated concerns.
- Need direct implementation rather than boundary analysis.
- Need a hardening verdict rather than neutral analysis.

## Required Inputs
- `TARGET_SCOPE` (path|module|api; required): Boundary to analyze.
- `BOUNDARY_KIND` (module|api|service|layer; required): Kind of boundary being analyzed.
- `ANALYSIS_DEPTH` (surface|full; optional): Surface = contract interface only; full = includes internal ownership split. Defaults to full.

## Input Contract Notes
- TARGET_SCOPE should identify one concrete interface, module, or boundary slice.
- BOUNDARY_KIND should describe the actual contract surface being analyzed.
- ANALYSIS_DEPTH controls how far into the boundary internals the analysis reaches.

## Structured Outputs
- `CONTRACT_MAP` (list; required; shape: {BOUNDARY, EXPLICIT_CONTRACT, IMPLICIT_ASSUMPTIONS, OWNERSHIP}): Current contracts — both explicit and inferred implicit.
- `LEAKED_ASSUMPTIONS` (list; required; shape: {ASSUMPTION, LOCATION, LEAK_KIND, SEVERITY}): Assumptions or responsibilities leaking across the boundary with leak kind.
- `COUPLING_AT_BOUNDARY` (list; required; shape: {COUPLING, KIND, STRENGTH}): Coupling observed at or through the boundary.
- `OPEN_BOUNDARY_QUESTIONS` (list; required; shape: {QUESTION, IMPACT}): Questions about the boundary still needing evidence.

## Output Contract Notes
- CONTRACT_MAP should distinguish explicit from inferred-implicit contracts.
- LEAKED_ASSUMPTIONS may be empty when the boundary is already explicit.
- COUPLING_AT_BOUNDARY should note whether coupling is through the public interface or around it.
- OPEN_BOUNDARY_QUESTIONS may be empty when the analysis is complete.

## Primary Lens
- `primary_lens`: `uncle-bob`
- `why`: Boundary analysis must expose dependency direction, contract clarity, and leak paths without prescribing a redesign.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: module-bounds-analysis.v1

## Neutrality Rules
- Describe current boundary before judging it weak or unclear.
- Separate proven contract leaks from speculative design concerns.
- Do not recommend redesign when the job is analysis only.

## Execution Constraints
- Keep the analysis bounded to the named boundary and its immediate callers or callees.
- Do not turn general naming preferences into boundary defects without contract evidence.
- If the boundary surface is large, focus on the highest-traffic entry points first.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

현재 계약 상태: [경계가 무엇을 드러내고 무엇을 숨기는지 한 문장]

계약 지도:
- [경계] — 명시된 계약: [있는 것] — 암묵적 가정: [숨겨진 것] — 담당: [누가 무엇]

누수 있으면:
- [가정] — 위치: [파일:줄] — 종류: [책임 누수/상태 누수/의존성 역전] — 심각도: [높음/낮음]

경계에서의 결합:
- [결합] — 방식: [공개 인터페이스/우회] — 강도: [높음/중간/낮음]

미확인: "[아직 근거 없는 경계 질문]"

마지막에: "경계 강화 작업 시작할까요, 아니면 의존성 방향부터 확인할까요?"

## Mandatory Rules
- Do not label a boundary broken without evidence of leakage or ambiguity.
- Keep analysis neutral — provide findings, not a hardening verdict.

## Example Invocation
```text
$analyze-module-bounds
SCOPE: src/api/user-service.ts
BOUNDARY_KIND: service
```
