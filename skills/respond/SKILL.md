---
name: respond
description: "Final-output only skill. Render the final user-facing response in plain, short, easy, concrete language using skill-specific response profiles. Do not analyze, plan, implement, or review here."
---

# Respond

## Purpose

완료된 작업 결과를 사용자가 바로 이해할 수 있는 응답 하나로 만든다.
새로운 분석, 추론, 판단을 여기서 추가하지 않는다.

## Default Program

```text
[stages: handoff |
 scope: diff |
 policy: evidence,deterministic-output,response-contract{plain-korean,feynman-clear,actionable,core-first,short-sentences,plain-words,concrete-details} |
 output: md(contract=v1)]
```

## Use When

- 스킬 실행이 끝나고 사용자에게 최종 응답을 출력해야 할 때.
- 단독 실행 또는 합성 실행 모두에서 하나의 출력 지점이 필요할 때.

## Do Not Use When

- 분석, 구현, 디버그, 리뷰 작업이 필요할 때.
- 위 단계에서 만들어지지 않은 발견이나 판단을 추가할 때.

## Required Inputs

- `RESPONSE_PROFILE` (required): 어떤 스킬이 실행됐는지와 profile id.
- `STAGE_PAYLOADS` (required): 위 단계에서 만든 결과물. 여기 있는 것만 쓴다.
- `LANGUAGE_PREFERENCE` (optional): 출력 언어. 기본은 사용자 언어를 따른다.

## Structured Outputs

- `FINAL_RESPONSE` (markdown.v1, required): 사용자에게 보여주는 최종 응답.
- `RENDERED_SECTIONS` (list, required): 실제로 출력된 섹션 목록.

## Artifacts

- `artifacts_in`: stage-payloads.v1, response-profile.v1
- `artifacts_out`: final-response.v1

## Neutrality Rules

- 위 단계에서 만든 것만 출력한다.
- 새로운 발견, 판단, 권장 사항을 여기서 추가하지 않는다.
- 근거가 없는 섹션은 빈 채로 두는 대신, 섹션 자체를 생략한다.

## Writing Rules

아래 순서로 쓴다.

**1. 결론 먼저**
첫 문장에서 "무슨 일이 있었고 왜 중요한지"를 쉬운 말로 말한다.
좋은 예: "src/auth에서 문제 3개를 찾았다. 그 중 하나는 지금 바로 고쳐야 한다."
나쁜 예: "분석이 완료되었습니다. 다섯 단계 파이프라인이 실행되었습니다."

**2. 초보자도 이해되게**
처음 등장하는 기술 용어는 같은 문장 안에서 쉬운 말로 풀어준다.
좋은 예: "회귀 테스트, 즉 기존 기능이 안 깨졌는지 보는 테스트 3개를 추가했다."
나쁜 예: "회귀 테스트와 idempotency를 보강했다."

**3. 구체적으로**
파일 이름, 라인 번호, 함수 이름, 수치를 쓴다.
좋은 예: "`auth.service.ts:87` — 만료 토큰 체크 없이 200 반환"
나쁜 예: "서비스 레이어에 문제가 발견됐습니다."

**4. 내부 용어 금지**
`KEY_FINDING`, `LEAKED_ASSUMPTION`, `HARDENING_ACTION`, `stage payload`,
`lens:`, `$wf-*`, `P0`, `TASK-ID` 등을 출력하지 않는다.

**5. 짧게**
섹션당 항목 최대 3개. 한 문장에 한 가지 주장. 긴 분류표보다 짧은 문단을 우선한다.

**6. 행동이 보이게**
가능하면 "무엇을 의미하는지"와 "이제 뭘 하면 되는지"를 바로 붙인다.
좋은 예: "README에 Claude 설치법을 넣었다. 이제 사용자는 링크를 따라 바로 설치와 사용법을 볼 수 있다."
나쁜 예: "Claude 섹션을 추가했다."

## Required References

- `../_core/RESPONSE-CONTRACT-v1.md`
- `../_core/RESPONSE-PROFILES-v1.md`

## Output Discipline

- `response_profile=generic`
- 렌더링만 담당한다. 도메인 판단은 upstream에서.
