---
name: analyze-structure
description: "Analyze current-state structure, module coupling, data flow, and hidden dependencies in a bounded scope. Use when deep structural understanding is needed before planning, refactoring, or design work."
---

# Analyze / Structure

## Purpose
Produce a structure-first analytical map covering boundaries, coupling, data flow, and hidden dependencies — not just a list of files.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,quality-gates{docs},deterministic-output | lens: hickey-carmack | output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, explicit coupling and performance characteristics.

## Use When
- Need to understand current module structure, ownership split, and data flow before planning or refactoring.
- Need coupling and cohesion evidence before boundary work.
- Need to find hidden dependencies, shared state, or cross-layer leaks.

## Do Not Use When
- Need option comparison rather than current-state analysis.
- Need evidence-gap analysis rather than structure explanation.
- Need debugging, implementation, or review verdicts.

## Required Inputs
- `TARGET_SCOPE` (file|module|folder|repo; required): Bounded scope to analyze.
- `ANALYSIS_QUESTION` (string; optional): Exact structure or coupling question to resolve.
- `ANALYSIS_FOCUS` (coupling|data-flow|boundaries|hidden-state|mixed; optional): Primary analytical dimension.
- `KNOWN_EVIDENCE` (list; optional; shape: {TYPE, REF, WHY_RELEVANT}): Existing files, docs, or traces.
- `CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Scope or time limits.

## Input Contract Notes
- ANALYSIS_QUESTION should ask about the current shape, not a preferred future design.
- ANALYSIS_FOCUS narrows the analytical dimension; `mixed` runs all dimensions at reduced depth.
- Use coupling focus when planning refactoring; data-flow when debugging side effects; hidden-state when tracking implicit behavior.

## Structured Outputs
- `BOUNDARY_MAP` (list; required; shape: {MODULE, RESPONSIBILITY, INPUTS, OUTPUTS}): What each boundary owns, accepts, and emits.
- `COUPLING_FINDINGS` (list; required; shape: {SOURCE, TARGET, COUPLING_KIND, STRENGTH}): Observed coupling — direct call, indirect, or shared-state.
- `DATA_FLOW_TRACES` (list; required; shape: {FLOW, PATH, SIDE_EFFECTS}): Key data flows with noted side effects.
- `HIDDEN_DEPENDENCIES` (list; required; shape: {DEPENDENCY, LOCATION, WHY_HIDDEN}): Implicit dependencies not visible from public interfaces.
- `OPEN_STRUCTURE_QUESTIONS` (list; required; shape: {QUESTION, CHEAPEST_NEXT_CHECK}): Remaining questions still needing evidence.

## Output Contract Notes
- BOUNDARY_MAP should describe current ownership, not proposed redesign.
- COUPLING_FINDINGS should distinguish direct call coupling from shared-state coupling.
- HIDDEN_DEPENDENCIES may be empty when the scope has no implicit coupling.
- OPEN_STRUCTURE_QUESTIONS may be empty when the analysis is sufficiently complete.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Structure analysis must expose data model, coupling chains, and side effects before any design judgement.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: structure-analysis.v1

## Neutrality Rules
- Map current structure before suggesting improvements.
- Separate observed boundaries from inferred responsibilities.
- Do not recommend redesign when the job is current-state analysis only.

## Execution Constraints
- Do not collapse the analysis into vague architecture prose.
- Prefer an explicit coupling list over a narrative summary.
- If source is long, extract 3-7 anchor facts first; include at least one from the middle.
- Before finalizing, ask 2-4 verification questions about potentially missed couplings or hidden state, then rescan.
- If first pass misses a salient boundary or coupling already implied by anchors, rewrite with higher density.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

경계 지도:
- [모듈] — 책임: [무엇을 담당] — 받는 것: [input] — 내보내는 것: [output]

결합도:
- [모듈A] → [모듈B] — 방식: [직접 호출/공유 상태/이벤트] — 강도: [높음/중간/낮음]

숨겨진 의존성 있으면:
- [의존성] — 위치: [파일:줄] — 왜 숨겨져 있나

미확인: "[근거 없어서 확인 못 한 부분]"

마지막에: "[가장 복잡한 결합] 더 파볼까요?"

## Mandatory Rules
- Do not finalize BOUNDARY_MAP until coupling findings and data flow traces are consistent with the stated scope.

## Example Invocation
```text
$analyze-structure
SCOPE: src/auth
FOCUS: coupling
```
