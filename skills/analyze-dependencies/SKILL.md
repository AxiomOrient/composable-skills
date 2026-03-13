---
name: analyze-dependencies
description: "Map module dependency directions, detect circular dependencies, measure coupling metrics, and identify dependency rule violations. Use when you need to understand the full dependency graph before refactoring or boundary work."
---

# Analyze / Dependencies

## Purpose
Produce an explicit dependency graph with coupling metrics, circular dependency detection, and dependency direction violations.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: uncle-bob | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `uncle-bob` because it keeps the work aligned with: Stable dependency principle, dependency inversion, and explicit boundary direction enforcement.

## Use When
- Need to understand module dependency directions before refactoring.
- Need to detect circular dependencies and fan-out coupling problems.
- Need to verify whether dependencies follow intended architecture rules.

## Do Not Use When
- Need a full refactoring plan rather than dependency analysis.
- Need direct implementation work.
- Need general code review without a dependency focus.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Scope to map dependencies in.
- `DEP_FOCUS` (direction|cycles|coupling|violations|mixed; optional): Which dependency dimension to prioritize.
- `ALLOWED_DIRECTIONS` (list; optional; shape: {FROM, TO}): Expected allowed dependency directions for violation detection.

## Input Contract Notes
- TARGET_SCOPE should be bounded to a module tree or subsystem, not the entire repo unless necessary.
- DEP_FOCUS narrows the analysis lens; `mixed` covers all dimensions.
- ALLOWED_DIRECTIONS enables explicit violation detection; omit to analyze without checking against rules.

## Structured Outputs
- `DEPENDENCY_GRAPH` (list; required; shape: {MODULE, DEPENDS_ON, DEP_KIND, STRENGTH}): Full dependency map with kind (import/call/data/config) and strength.
- `CIRCULAR_DEPENDENCIES` (list; required; shape: {CYCLE, PATH, SEVERITY}): All detected circular dependency cycles with severity.
- `COUPLING_METRICS` (list; required; shape: {MODULE, FAN_IN, FAN_OUT, INSTABILITY}): Coupling metrics per module — fan-in, fan-out, instability score.
- `DIRECTION_VIOLATIONS` (list; required; shape: {FROM, TO, VIOLATION_KIND, EVIDENCE}): Dependencies violating stated or architectural rules.
- `STABILIZATION_CANDIDATES` (list; required; shape: {MODULE, ISSUE, RECOMMENDED_DIRECTION}): Modules worth restructuring for dependency stability.

## Output Contract Notes
- DEPENDENCY_GRAPH should include all observed dependency kinds, not just imports.
- CIRCULAR_DEPENDENCIES may be empty when no cycles exist.
- COUPLING_METRICS should identify both highly coupled (high fan-out) and highly depended-upon (high fan-in) modules.
- DIRECTION_VIOLATIONS may be empty when ALLOWED_DIRECTIONS is not provided.

## Primary Lens
- `primary_lens`: `uncle-bob`
- `why`: Dependency analysis must expose direction, coupling strength, and stability before recommending restructuring.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: dependency-analysis.v1

## Neutrality Rules
- Map actual dependencies before judging direction.
- Separate proven violations from architectural preferences.
- Do not recommend restructuring beyond what the dependency evidence supports.

## Execution Constraints
- Do not turn dependency analysis into a full refactoring plan.
- If the dependency graph is large, focus on the modules with the highest coupling metrics first.
- Prefer explicit directed graph notation over prose narrative.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

의존성 지도:
- [모듈] → [모듈] — 종류: [import/호출/데이터] — 강도: [강/중/약]

순환 의존성 있으면:
- [모듈A] → [모듈B] → [모듈A] — 심각도: [높음/낮음]

결합도 지표:
- [모듈] — 내보내는 곳: [fan-out], 들어오는 곳: [fan-in] — 불안정도: [0-1]

규칙 위반 있으면:
- [모듈A] → [모듈B] — 왜 위반인지: [설명]

안정화가 필요한 곳:
1. [모듈] — 문제: [무엇이 문제] — 개선 방향: [한 줄]

마지막에: "[순환 의존성 또는 가장 불안정한 모듈] 먼저 정리할까요?"

## Example Invocation
```text
$analyze-dependencies
SCOPE: src/
FOCUS: cycles
ALLOWED_DIRECTIONS:
  - from: ui, to: domain
  - from: domain, to: infra
```
