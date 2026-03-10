# Skill System

## Goal

이 문서는 현재 스킬 시스템의 아키텍처, 운영 원칙, 신규 스킬 추가 기준을 한 곳에 모은 운영 기준서다.

핵심 목표는 세 가지다.

1. runtime surface를 작고 명확하게 유지한다.
2. 새로운 스킬이 기존 스킬과 겹치지 않게 추가한다.
3. 외부 스킬 모음이 들어와도 system 전체가 MECE하게 유지되게 한다.

---

## 1. Source of Truth

단일 source-of-truth는 아래 둘이다.

- runtime discovery: [`../skills/_registry/index.json`](../skills/_registry/index.json)
- runtime spec: `skills/_registry/{atomic|utility|workflow}/*.json`

다른 문서는 source-of-truth가 아니다.

- `skills/<name>/SKILL.md`는 materialized surface다.
- `README.md`, `SKILL-COMBOS.md`, `SKILL-STATE-REPORT.md`는 설명/파생 문서다.

즉, 스킬을 추가하거나 바꿀 때 먼저 registry를 바꾸고, 그 다음 materialize와 검증을 한다.

---

## 2. Runtime Architecture

runtime layer는 세 개만 둔다.

### atomic

하나의 문제를 하나의 출력으로 해결하는 실행 단위다.

예:

- `tidy-find-copies`
- `tidy-find-magic-numbers`
- `ask-break-it-down`
- `check-delivered`

판정 기준:

- 입력이 하나의 작업으로 수렴한다.
- 출력이 다음 스킬이 그대로 받을 수 있는 구조다.
- 다른 역할을 몰래 하지 않는다.

### utility

도메인 문제를 직접 풀지 않는다.
오케스트레이션, 렌더링, 실행 동기화, 외부 위임만 담당한다.

현재 utility:

- `compose`
- `plan-driven-delivery`
- `release-publish`
- `respond`
- `gemini`

### workflow

반복적으로 같이 쓰는 atomic 조합에 이름을 붙인 실행 entrypoint다.

규칙:

- 공개 workflow 이름은 `wf-*`만 허용
- `expands_to`를 반드시 공개
- hidden logic 금지
- duplicate collapse 허용
- cycle 금지

예:

- `wf-ask-get-clear`
- `wf-ask-sharpen`
- `wf-check-full-review`
- `wf-tidy-find-improvements`
- `wf-ship-it`

---

## 3. Non-Runtime Layer

future pack은 둘 수 있다. 다만 pack은 runtime skill이 아니다.

pack은 atomic과 workflow를 함께 포함할 수 있다.
하지만 포함 목록일 뿐, pack 자체가 실행 node가 되지는 않는다.

pack은 아래 역할만 한다.

- 설치 단위
- 발견(discovery) 단위
- 카탈로그 단위
- 도메인 묶음 설명 단위
- atomic/workflow 묶음 설명 단위

pack은 아래 역할을 하지 않는다.

- parser가 직접 실행하는 entrypoint
- workflow를 대체하는 runtime node
- broad phase 명령

좋은 예:

- `question-answer-pack`
- `documentation-pack`
- `project-quality-pack`
- `delivery-pack`

나쁜 예:

- `phase-development`
- `phase-design`
- `phase-product`

위 이름들은 유지 대상이 아니다.
지금 문서에 남아 있는 경우도 "이런 broad phase 이름은 금지"라는 금지 예시일 뿐이다.

이유는 간단하다.

- pack은 "무엇이 들어 있는가"를 설명하는 층
- skill은 "무엇을 실행하는가"를 담당하는 층

둘을 섞으면 runtime surface가 다시 비대해진다.

---

## 4. Operating Principles

### 4.1 One Skill = One Job

스킬 하나는 하나의 job만 가져야 한다.

나쁜 예:

- `bug-and-refactor-review`
- `design-and-implement-auth`
- `phase-development`

좋은 예:

- `check-failure-paths`
- `tidy-reorganize`
- `build-write-code`

### 4.2 Explicit Inputs and Outputs

모든 운영 스킬은 아래를 가져야 한다.

- `Required Inputs`
- `Structured Outputs`
- `Neutrality Rules`
- `Output Discipline`

좋은 입력은 범위와 종료 조건을 포함한다.

나쁜 예:

- `버그 찾아줘`
- `프로젝트 개선해줘`

좋은 예:

- `TARGET_SCOPE: src/auth`
- `FAILURE_SYMPTOM: refresh 후 세션이 사라짐`
- `EXPECTED_BEHAVIOR: refresh 후에도 로그인 유지`

### 4.3 Neutrality First

분석/리뷰/피드백 계열은 결과를 유도하면 안 된다.

반드시 지켜야 할 규칙:

- evidence와 inference를 분리한다.
- 근거가 부족하면 `no finding` 또는 `inconclusive`를 허용한다.
- 없는 결함을 만들어내지 않는다.

### 4.4 Compose Is the Engine

`compose`는 엔진이다.
초보자용 사용 예시는 `SKILL-COMBOS.md`에 둔다.

즉:

- `compose`를 `combos`로 바꾸지 않는다.
- recipe 문서는 engine 위에 얹는다.

### 4.5 Workflow Is a Named Composition

workflow는 broad mega-skill이 아니다.

workflow를 만들 수 있는 경우:

- 같은 atomic 조합이 반복된다.
- 사용자 의도가 분명하다.
- 출력 구조가 새 이름으로 고정될 가치가 있다.

workflow를 만들면 안 되는 경우:

- 단지 phase를 묶고 싶다.
- 입력/출력이 여전히 너무 넓다.
- 내부 로직을 숨기고 싶다.

---

## 5. MECE Admission Rule

새 스킬은 아래 순서로 판정한다.

### Step 1. 먼저 새 스킬이 정말 필요한지 본다

질문:

1. 지금 registry 안에 같은 job을 하는 스킬이 이미 있는가
2. 기존 스킬의 입력을 더 구체적으로 써서 해결 가능한가
3. 기존 atomic 조합에 이름만 붙이면 충분한가

셋 중 하나라도 `yes`면 새 atomic을 만들지 않는다.

### Step 2. layer를 먼저 판정한다

질문:

1. 직접 도메인 문제를 해결하는가
2. 오케스트레이션/렌더링/동기화만 하는가
3. 반복 조합에 이름을 붙이는가
4. 설치/카탈로그/묶음 설명만 필요한가

판정:

- 1 -> `atomic`
- 2 -> `utility`
- 3 -> `workflow`
- 4 -> `pack` (non-runtime)

### Step 3. atomic인지 broad request인지 본다

새 후보가 아래처럼 들리면 atomic이 아니다.

- `개발 전체를 해줘`
- `버그를 찾아서 고치고 구조도 정리해줘`
- `제품 전략을 잡고 PRD도 쓰고 출시 계획도 세워줘`

이런 경우는 쪼갠다.

예:

- `problem-interview-brief`
- `prd-scope-contract`
- `roadmap-tradeoff-map`
- `launch-readiness-review`

### Step 4. output artifact가 하나로 수렴하는지 본다

atomic은 주 출력 artifact가 하나여야 한다.

좋은 예:

- `duplication-report.v1`
- `question-stack.v1`
- `release-decision.v1`

나쁜 예:

- “분석도 하고 구현도 하고 테스트도 하는 결과물”

### Step 5. boundary 침범이 없는지 본다

새 스킬 설명에 아래가 같이 섞이면 실패다.

- 분석 + 구현
- 리뷰 + 수정
- 계획 + 검증
- 문서화 + 코드 변경

이 경우는 나눈다.

---

## 6. New Skill Decision Tree

### A. 새 atomic이 필요한 경우

아래가 모두 참이어야 한다.

1. 기존 atomic으로 대체 불가
2. 입력이 좁다
3. 출력이 하나다
4. 다른 family와 경계가 선다
5. 이름만 보고 무슨 일인지 알 수 있다

예:

- `roadmap-tradeoff-map`
- `problem-interview-brief`
- `outcome-metric-check`

### B. 새 workflow가 필요한 경우

아래가 모두 참이어야 한다.

1. 기존 atomic 조합이 2회 이상 반복된다
2. 사용자 입장에서 하나의 의도로 읽힌다
3. `expands_to`를 공개해도 설명 가능하다
4. 출력 계약이 새 이름으로 묶일 가치가 있다

예:

- `wf-ask-sharpen`
- `wf-tidy-find-improvements`

### C. 새 utility가 필요한 경우

매우 드물어야 한다.

아래 셋 중 하나여야 한다.

- orchestration
- rendering
- execution governance

그 외에는 utility를 만들지 않는다.

### D. 새 pack이 필요한 경우

runtime이 아니라 catalog가 필요할 때만 만든다.

예:

- `project-quality-pack`
- `delivery-pack`

pack 안에는 이런 것만 들어간다.

- 포함된 atomic/workflow 목록
- 추천 entrypoint
- 포함하지 않는 것
- 대상 사용자

---

## 7. Naming Rules

### atomic naming

규칙:

- 동작이 바로 보이게
- broad 명사 대신 구체 동사/대상 포함
- 하나의 문제만 표현

좋은 예:

- `tidy-find-magic-numbers`
- `check-module-walls`
- `problem-interview-brief`

나쁜 예:

- `developer-helper`
- `product-skill`
- `bug-fixer`

### workflow naming

규칙:

- 반드시 `wf-*`
- 사용자 의도와 결과를 같이 드러낸다

좋은 예:

- `wf-ask-get-clear`
- `wf-check-full-review`
- `wf-tidy-find-improvements`

나쁜 예:

- `wf-dev-phase`
- `wf-design-phase`
- `wf-all-in-one`

### pack naming

규칙:

- 실행 이름처럼 보이면 안 된다
- 묶음/카탈로그처럼 읽혀야 한다

좋은 예:

- `check-pack`
- `delivery-pack`

---

## 8. Contract Rules for New Skills

새 스킬은 아래 contract를 먼저 고정한다.

### Required Inputs

반드시 포함:

- `TARGET_SCOPE` 또는 도메인 equivalent
- `GOAL` 또는 job discriminator
- 필요한 경우 `CONSTRAINTS`

입력 이름은 broad 하지 않아야 한다.

나쁜 예:

- `INPUT`
- `DATA`
- `REQUEST`

좋은 예:

- `REVIEW_FOCUS`
- `FAILURE_SYMPTOM`
- `DONE_CONDITION`
- `IMPROVEMENT_GOAL`

### Structured Outputs

규칙:

- 다음 스킬이 그대로 받을 수 있어야 한다
- 자유 문장 하나로 끝내지 않는다
- 핵심 artifact를 분리한다

좋은 예:

- `QUESTION_STACK`
- `ROLLBACK_CHECKLIST`
- `NEXT_IMPLEMENTATION_STEP`

### Neutrality Rules

반드시 포함:

- evidence 없이 결론 금지
- no-finding / inconclusive 허용
- 경계 밖 작업 금지

### Output Discipline

규칙:

- `response_profile`을 고정
- user-facing rendering은 `respond`에 위임

---

## 9. Lens Rule

lens는 roleplay가 아니다.
mental model card다.

atomic마다 `primary_lens` 하나만 둔다.

선정 기준:

1. 이 skill의 실패를 가장 잘 막아주는 사고 프레임인가
2. output artifact와 자연스럽게 연결되는가
3. 다른 atomic과 구분되는 이유를 설명할 수 있는가

주의:

- lens가 skill boundary를 대신하면 안 된다
- lens 때문에 새 skill을 만들지 않는다
- 같은 job이면 lens만 바꿔서 별도 skill을 만들지 않는다

---

## 10. How to Add External Skill Libraries

예를 들어 PM 계열 스킬 모음이 들어오더라도, raw import는 하지 않는다.

외부 스킬 모음을 처리하는 순서:

1. **catalog로 먼저 본다**
   - runtime import 금지
   - 먼저 후보 목록만 뽑는다
2. **각 후보를 job 단위로 다시 쪼갠다**
   - broad phase 이름 제거
   - one skill = one job으로 환원
3. **기존 registry와 overlap 검사를 한다**
   - 같은 job이면 추가하지 않는다
   - 기존 workflow로 충분하면 workflow만 추가한다
4. **runtime 승격은 필요한 것만 한다**
   - atomic / workflow / utility 중 하나로만 승격
5. **나머지는 pack 수준에 남긴다**

외부 스킬에서 자주 나오는 broad 항목을 그대로 들여오면 안 된다.

나쁜 예:

- `product-strategy-phase`
- `pm-master-skill`
- `discovery-and-roadmap`

좋은 방향:

- `problem-interview-brief`
- `persona-evidence-map`
- `prioritization-tradeoff-review`
- `roadmap-risk-check`
- `launch-readiness-review`

---

## 11. MECE Overlap Check

새 후보를 추가하기 전 아래 표를 채운다.

| 질문 | yes면 어떻게 하나 |
|---|---|
| 기존 skill이 같은 입력과 같은 출력을 이미 가지는가 | 새 스킬 만들지 않음 |
| 기존 skill의 입력을 더 구체화하면 해결되는가 | 새 스킬 만들지 않음 |
| 기존 atomic 여러 개를 반복 조합하는 패턴인가 | 새 workflow 검토 |
| 실행이 아니라 카탈로그/설치 단위인가 | 새 pack 검토 |
| 분석+구현+검증이 같이 들어가는가 | 더 쪼갬 |
| 최종 산출물이 하나로 수렴하지 않는가 | 더 쪼갬 |

이 표에서 `새 스킬 만들지 않음`이 나오면 멈추는 게 맞다.

추가하지 않는 것도 설계다.

---

## 12. Admission Checklist

새 스킬은 아래를 전부 통과해야 한다.

- 이름만 보고 job이 보인다
- layer 판정이 명확하다
- 기존 skill과 역할이 겹치지 않는다
- Required Inputs가 좁고 명확하다
- Structured Outputs가 다음 스킬에 바로 연결된다
- Neutrality Rules가 있다
- response profile이 정해져 있다
- lens rationale을 설명할 수 있다
- workflow라면 `expands_to`가 공개된다
- pack이라면 runtime surface에 들어오지 않는다

하나라도 아니면 아직 추가하면 안 된다.

---

## 13. Recommended Future Direction

앞으로 PM 계열 스킬을 준비할 때는 아래 순서를 권장한다.

1. 먼저 `pm-discovery-pack` 같은 catalog를 설계한다
2. 그 안에서 runtime으로 올릴 후보를 하나씩 판정한다
3. broad phase 이름은 버리고 atomic 후보로 다시 쪼갠다
4. 반복 조합이 검증되면 `wf-*` workflow를 만든다

즉, 먼저 pack으로 정리하고, 나중에 필요한 것만 runtime skill로 승격한다.

이 방식이 가장 단순하고, 가장 덜 겹치고, 가장 유지보수가 쉽다.
