---
name: workflow-consensus-engine
description: "Workflow skill that locks a bounded scope contract and then runs the consensus engine to arbitrate one design, debugging, or planning decision across Codex, Claude Code, and Gemini CLI. Use when the public entrypoint should expose multi-model consensus without hiding the boundary-setting step."
---

# Workflow / Consensus Engine

## Purpose
Public entrypoint for bounded multi-model consensus: first lock the boundary, then run the script-backed engine.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit | scope: repo|diff|paths(glob,...) | policy: evidence,safety-gates,deterministic-output | lens: kahneman-tversky | output: md(contract=v1)]
```

## Lens Rationale
This workflow uses `kahneman-tversky` because it should separate observed evidence from confidence, show where options collide, and avoid treating weak agreement as proof.

## Use When
- Need a public entrypoint for choosing between design, refactor, debugging, or plan alternatives.
- Need the engine to preserve disagreement instead of reducing everything to a single prose answer.
- Need scope, constraints, and done condition locked before multi-model arbitration starts.

## Do Not Use When
- Need direct code changes right away.
- The task is a deterministic computation or a simple factual lookup.
- External CLI use is disallowed for this mission.
- The request is still too fuzzy and needs a clarify workflow first.

## Required Inputs
- `REQUEST` (string; required): Original decision or analysis request.
- `TARGET_SCOPE` (path|module|folder|repo|artifact; required): Bounded scope for the consensus run.
- `DONE_CONDITION` (list; required; shape: `{CONDITION}`): What the final recommendation must prove or include.
- `CONSTRAINTS` (list; optional; shape: `{CONSTRAINT}`): Hard limits and non-goals.
- `CONTEXT_FILES` (list; optional; shape: `{PATH}`): Local files or notes to include in the packet.
- `CONSENSUS_MODE` (analysis|plan|implement-review; optional): Consensus output mode. Defaults to `analysis`.

## Input Contract Notes
- This workflow expects one bounded decision surface. If the user asks for multiple unrelated choices, split them first.
- `DONE_CONDITION` should describe observable answer requirements, not vague quality wishes.
- `CONTEXT_FILES` should stay bounded and relevant to the scoped question.

## Structured Outputs
- `BOUNDARY_CONTRACT` (object; required; shape: `{GOAL, IN_SCOPE, OUT_OF_SCOPE, DONE_CONDITION}`): Locked scope contract produced before consensus.
- `CONSENSUS_VERDICT` (strong-consensus|provisional-consensus|no-consensus; required): Final consensus strength.
- `CONSENSUS_RECOMMENDATION` (string; required): Best current recommendation after arbitration.
- `UNRESOLVED_CONFLICTS` (list; required): Conflicts that still block a fully accepted recommendation.
- `CHEAPEST_NEXT_CHECKS` (list; required): Next checks that would most reduce remaining uncertainty.

## Output Contract Notes
- The workflow must expose both the boundary contract and the final consensus output.
- `UNRESOLVED_CONFLICTS` may be empty only when the disagreement surface has been reduced cleanly.
- Do not hide the `clarify-boundaries` step or rewrite its output as if it never happened.

## Artifacts
- `artifacts_in`: scope-contract.v1
- `artifacts_out`: consensus-report.v1

## Neutrality Rules
- Do not skip the boundary step even if the request sounds mostly clear.
- Do not promote popularity over evidence in the consensus step.
- Keep unresolved collisions explicit.

## Execution Constraints
- This is analysis-only. Do not patch repository files from this workflow.
- Keep the mission bounded to one decision surface per run.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

먼저 범위 계약:
- 목표: [한 문장]
- 포함 / 제외 / 완료 조건

그 다음 합의 결과:
- 합의 강도
- 권고안
- 남는 충돌
- 가장 싼 다음 확인

## Mandatory Rules
- `clarify-boundaries` 출력 없이 바로 consensus-engine을 호출하지 않는다.
- 합의 결과는 accepted, provisional, unresolved를 구분한다.

## Expansion
- `$clarify-boundaries`
- `$consensus-engine`

## Example Invocation
```text
$workflow-consensus-engine
REQUEST: decide the best auth refresh redesign for this repository
TARGET_SCOPE: src/auth
DONE_CONDITION:
  - recommend one path
  - list remaining risks
CONSTRAINTS:
  - keep public API stable
```

## Eval Cases

| Prompt | Should Trigger | Key Output Check |
|--------|---------------|-----------------|
| auth refresh flow 설계안을 셋 중 하나로 좁혀야 하는데 모델 3개 의견을 합의로 정리해줘. | YES | CONSENSUS_VERDICT 존재 |
| 이 리팩터링 방향 둘 중 뭐가 나은지 Codex/Claude/Gemini 의견을 합쳐서 결론 내려줘. | YES | CONSENSUS_RECOMMENDATION 존재 |
| 이 버그 원인 가설 두 개를 비교해서 가장 가능성 높은 쪽을 정리해줘. | YES | UNRESOLVED_CONFLICTS 존재 |
| 바로 코드 수정해. | NO | 구현 작업이므로 build 계열 workflow 권장 |
| 12457 * 98 계산해줘. | NO | 결정적 계산이므로 consensus-engine 불필요 |
| 외부 CLI 쓰지 말고 로컬 분석만 해줘. | NO | 외부 CLI 금지이므로 일반 analyze/review 스킬 권장 |
