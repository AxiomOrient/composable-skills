---
name: analyze-complexity
description: "Measure and classify complexity in a bounded scope — cyclomatic, cognitive, coupling, and hidden-state complexity. Use when you need to understand where complexity comes from and which clusters are worth simplifying."
---

# Analyze / Complexity

## Purpose
Produce an evidence-backed complexity map that classifies essential vs accidental complexity and ranks the highest-value simplification targets.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, separation of essential from accidental complexity.

## Use When
- Need to understand where complexity comes from before simplification.
- Need to separate domain-required complexity from accidental structure.
- Need a ranked list of complexity hotspots to target first.

## Do Not Use When
- Need a full simplification plan or refactoring implementation.
- Need direct implementation work.
- The target scope is not bounded.

## Required Inputs
- `TARGET_SCOPE` (path|module|repo; required): Where to analyze complexity.
- `COMPLEXITY_FOCUS` (cyclomatic|coupling|cognitive|hidden-state|mixed; optional): Which complexity dimension to prioritize.

## Input Contract Notes
- TARGET_SCOPE should be bounded enough that complexity can be traced to specific files or modules.
- COMPLEXITY_FOCUS narrows the measurement lens; `mixed` covers all dimensions at reduced depth.
- Use `coupling` when planning module splits; `cognitive` when the code is hard to read; `hidden-state` when debugging implicit behavior.

## Structured Outputs
- `COMPLEXITY_MAP` (list; required; shape: {MODULE, COMPLEXITY_KIND, SCORE, EVIDENCE}): Each module with complexity kind, score, and evidence.
- `ESSENTIAL_COMPLEXITY` (list; required; shape: {ITEM, DOMAIN_REASON}): Complexity inherent to the domain — do not remove.
- `ACCIDENTAL_COMPLEXITY` (list; required; shape: {ITEM, CAUSE, REMOVAL_COST}): Complexity from incidental structure, naming, or indirection.
- `HOTSPOTS` (list; required; shape: {ITEM, COMPLEXITY_SCORE, REMOVAL_VALUE, WHY_FIRST}): Ranked simplification candidates by removal value.

## Output Contract Notes
- COMPLEXITY_MAP should measure actual complexity, not style preference.
- ESSENTIAL_COMPLEXITY should cite domain rules, not just say "it's complicated".
- ACCIDENTAL_COMPLEXITY should identify the mechanism (over-abstraction, hidden state, naming confusion, etc.).
- HOTSPOTS should rank by removal value, not just raw score.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Complexity analysis must separate essential structure from accidental abstraction before recommending removal.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: complexity-analysis.v1

## Neutrality Rules
- Do not label domain-required complexity as accidental without evidence.
- Separate pain points from actual simplification candidates.
- Keep the inventory descriptive before recommending changes.

## Execution Constraints
- Do not turn complexity analysis into a simplification plan.
- Prefer explicit per-module measurements over vague "this feels complex".
- If source is long, focus on the modules with the highest estimated complexity first.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

복잡도 지도:
- [모듈] — 종류: [순환/결합/인지/숨겨진상태] — 점수: [높음/중간/낮음] — 근거: [한 줄]

필수 복잡도 (손대면 안 됨):
- [항목] — 이유: [도메인 요구사항]

없애도 되는 복잡도:
- [항목] — 원인: [과도한 추상화/이름 혼동/숨겨진 상태] — 제거 비용: [작음/중간/큼]

우선순위 제거 대상:
1. [항목] — 제거하면 좋은 점: [무엇이 나아지는지]

마지막에: "[1번 항목] 먼저 정리할까요, 아니면 전체 복잡도 지도 보고 나서 결정할까요?"

## Example Invocation
```text
$analyze-complexity
SCOPE: src/auth
FOCUS: coupling
```
