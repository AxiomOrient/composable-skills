---
name: analyze-impact
description: "Map the full impact surface of a planned or existing change — direct callers, transitive paths, shared state, and downstream risk. Use when you need to understand what a change touches before implementing or releasing."
---

# Analyze / Impact

## Purpose
Produce a complete impact map for a change — direct effects, transitive paths, shared-state risks, and severity-ranked exposure surface.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: kahneman-tversky | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `kahneman-tversky` because it keeps the work aligned with: Separate observed change surface from inferred risk, expose uncertainty, and resist underestimating transitive impact.

## Use When
- Need to understand what a change touches before starting implementation.
- Need to find transitive effects and shared-state risks before release.
- Need a severity-ranked exposure surface, not just a list of changed files.

## Do Not Use When
- Need full debugging rather than surface mapping.
- Need direct implementation without impact analysis.
- Need a code review verdict rather than impact mapping.

## Required Inputs
- `TARGET_SCOPE` (file|module|folder|repo; required): Where the change is planned or already applied.
- `CHANGE_DESCRIPTION` (string; required): What the change does or intends to do.
- `IMPACT_DEPTH` (direct|transitive|full; optional): How deep to trace impact. Defaults to `transitive`.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Scope or time limits.

## Input Contract Notes
- CHANGE_DESCRIPTION should describe the change intent, not the implementation details.
- IMPACT_DEPTH controls how far to trace: `direct` = immediate callers only; `transitive` = callers of callers; `full` = all reachable paths.
- Use CONSTRAINTS to limit scope when the change is in a widely-used utility.

## Structured Outputs
- `DIRECT_IMPACT` (list; required; shape: {COMPONENT, CHANGE_KIND, EVIDENCE}): Components directly modified or directly calling the changed surface.
- `TRANSITIVE_IMPACT` (list; required; shape: {COMPONENT, PATH, RISK_LEVEL}): Downstream components affected through call chains or shared state.
- `SHARED_STATE_RISKS` (list; required; shape: {STATE, CONSUMERS, RISK}): Shared data structures, globals, or side-channel state that the change may affect.
- `IMPACT_SEVERITY_MAP` (list; required; shape: {COMPONENT, SEVERITY, RATIONALE}): Severity-ranked full impact surface.
- `UNKNOWN_IMPACT_AREAS` (list; required; shape: {AREA, WHY_UNKNOWN}): Paths that could not be traced due to dynamic dispatch, external calls, or scope limits.

## Output Contract Notes
- DIRECT_IMPACT should be exhaustive for the stated scope.
- TRANSITIVE_IMPACT should stop at the stated IMPACT_DEPTH.
- SHARED_STATE_RISKS may be empty when no shared state is involved.
- UNKNOWN_IMPACT_AREAS should be explicit rather than silently omitted.

## Primary Lens
- `primary_lens`: `kahneman-tversky`
- `why`: Impact analysis must separate observed change surface from inferred transitive risk, and mark unknown areas explicitly.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: impact-analysis.v1

## Neutrality Rules
- Map actual call paths and state sharing before estimating risk.
- Do not inflate risk estimates beyond what the call graph supports.
- Mark unknown paths explicitly instead of guessing impact.

## Execution Constraints
- Do not turn impact analysis into a full refactoring plan.
- If the call graph is large, focus on the highest fan-in components first.
- Prefer explicit path notation over narrative.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

직접 영향:
- [컴포넌트] — 변경 종류: [시그니처 변경/동작 변경/데이터 변경] — 근거: [파일:줄]

간접 영향:
- [컴포넌트] — 경로: [A → B → C] — 위험도: [높음/중간/낮음]

공유 상태 위험 있으면:
- [상태] — 사용하는 곳: [목록] — 위험: [무엇이 바뀔 수 있는지]

영향 심각도:
- 높음: [목록]
- 중간: [목록]
- 낮음: [목록]

추적 못 한 영역: "[동적 디스패치, 외부 호출 등 이유와 함께]"

마지막에: "[가장 위험한 간접 영향] 먼저 확인할까요?"

## Example Invocation
```text
$analyze-impact
SCOPE: src/auth/token-service.ts
CHANGE: "Adding token expiry field to JWT payload"
DEPTH: transitive
```
