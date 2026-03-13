# 만들기 — plan / build / debug / test 스킬 가이드

> 이 파일은 [Atomic Skills 가이드](./ATOMIC-SKILLS-GUIDE.md)의 일부입니다.

---

## 이 파일의 스킬

| 카테고리 | 스킬 | 한 줄 설명 |
|----------|------|-----------|
| plan | `plan-why-build-this` | 왜 만드는지 — 사용자, 문제, 기대 결과를 짧게 정리 |
| plan | `plan-what-it-does` | 기능이 정확히 무엇을 해야 하는지 명세 작성 |
| plan | `plan-screen-map` | 화면과 페이지 간 이동 흐름 설계 |
| plan | `plan-how-to-build` | 데이터 흐름과 구조까지 포함한 기술 설계 |
| plan | `plan-dependency-rules` | 어떤 모듈이 어떤 모듈을 참조해도 되는지 규칙 정의 |
| plan | `plan-verify-order` | 코드를 바꾸기 전에 어떤 순서로 확인할지 계획 |
| plan | `plan-task-breakdown` | 설계를 실제 작업 목록으로 쪼개 TASKS.md 문서 생성 |
| build | `build-write-code` | 실제 코드를 변경하고 검증 근거를 남김 |
| build | `build-make-faster` | 성능 병목을 측정하고 전후 수치로 비교 |
| debug | `debug-capture-failure` | "가끔 오류가 나요"를 재현 가능한 단계로 변환 |
| debug | `debug-map-impact` | 버그가 어디까지 번지는지 영향 범위 파악 |
| debug | `debug-find-root-cause` | 재현 가능한 버그의 진짜 원인을 증거 중심으로 탐색 |
| debug | `debug-confirm-fix` | 수정 후 버그가 정말 사라졌는지, 재발 방지까지 확인 |
| test | `test-find-gaps` | 중요한 동작에 테스트가 빠진 곳 탐지 |
| test | `test-design-cases` | 정상·경계·실패 케이스를 빠짐없이 설계 |
| test | `test-write-guards` | 실제 자동화 테스트를 작성하여 회귀 방지 |
| test | `test-run-user-scenarios` | 진짜 사용자처럼 돌려보며 헷갈리는 지점과 깨지는 곳 탐색 |

---

## plan — 설계와 계획을 세우는 스킬

> 만들기 전에 **길을 그립니다**.

### 어떤 plan 스킬을 써야 하나?

| 상황 | 쓸 스킬 |
|------|---------|
| "왜 이걸 만들어야 하지?" 정리가 안 됨 | `plan-why-build-this` |
| "이 기능이 정확히 뭘 해야 하지?" 명세가 없음 | `plan-what-it-does` |
| 화면 간 이동 구조가 없음, UI 개발 전 흐름이 필요함 | `plan-screen-map` |
| 어떻게 만들지 기술 설계가 필요함 | `plan-how-to-build` |
| "A가 B를 불러도 되나?" 의존성 규칙이 불명확함 | `plan-dependency-rules` |
| 큰 변경 전에 "어떤 테스트부터 돌려야 하지?" 결정 필요 | `plan-verify-order` |
| 설계를 작업 목록으로 쪼개야 함 | `plan-task-breakdown` |

---

### `plan-why-build-this` — 왜 만드는지 정리하기

**한 줄 설명:** 기능을 만들기 전에 "누구를 위해, 어떤 문제를 해결하는가"를 짧게 정리합니다.

**언제 써요?**
- 새 기능을 시작하기 전에 방향을 맞춰야 할 때
- 팀원이나 이해관계자에게 왜 이 기능이 필요한지 설명해야 할 때
- 요구사항보다 먼저 문제와 목적을 문서로 남기고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `BRIEF_SCOPE` | ✅ | 범위 (`feature` / `initiative` / `product` / `project`) |
| `PROBLEM_STATEMENT` | ✅ | 해결하려는 문제를 평범한 말로 |
| `TARGET_AUDIENCE` | ✅ | 주요 사용자 또는 이해관계자 |
| `DESIRED_OUTCOMES` | ✅ | 기대하는 결과물 |
| `SUCCESS_SIGNALS` | ✅ | 성공했다는 것을 어떻게 알 수 있나 |
| `CONSTRAINTS` | 선택 | 기간, 예산, 기술 제약 등 |
| `KNOWN_NON_GOALS` | 선택 | 이번에 하지 않을 것 |

**예제**

```
$plan-why-build-this
BRIEF_SCOPE: feature
PROBLEM_STATEMENT: 사용자가 비밀번호를 자주 잊어서 매번 고객센터에 문의한다
TARGET_AUDIENCE:
  - USER: 모바일 앱 사용자
    CONTEXT: 30-50대, 월 1-2회 앱 접속
DESIRED_OUTCOMES:
  - OUTCOME: 비밀번호 찾기를 앱에서 직접 할 수 있다
    WHY_IT_MATTERS: 고객센터 비용 절감 및 사용자 불편 해소
SUCCESS_SIGNALS:
  - SIGNAL: 고객센터 비밀번호 관련 문의 감소
    HOW_MEASURED: 기능 출시 후 30일 문의 건수 비교
KNOWN_NON_GOALS:
  - NON_GOAL: 소셜 로그인 추가
    WHY_OUT: 이번 범위 밖, 별도 기획 필요
```

---

### `plan-what-it-does` — 기능 명세 작성하기

**한 줄 설명:** "이 기능이 정확히 무엇을 해야 하는지"를 구체적인 동작과 엣지 케이스까지 정리합니다.

**언제 써요?**
- 개발을 시작하기 전에 기능 명세를 만들어야 할 때
- 요구사항을 글로 정리하고 경계를 명확히 해야 할 때
- "어디까지 만들어야 하지?"를 팀과 합의해야 할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `FEATURE_SCOPE` | ✅ | 범위 (`feature` / `screen` / `flow` / `api` / `module`) |
| `USER_OUTCOME` | ✅ | 사용자가 이 기능으로 얻는 핵심 결과 |
| `REQUIRED_BEHAVIORS` | ✅ | 구현해야 할 구체적인 동작 목록 |
| `ACCEPTANCE_SCENARIOS` | ✅ | 완료됐음을 확인하는 시나리오 |
| `OUT_OF_SCOPE` | 선택 | 이번에 하지 않을 것 |
| `CONSTRAINTS` | 선택 | 기술/비즈니스 제약 |

**예제**

```
$plan-what-it-does
FEATURE_SCOPE: flow
USER_OUTCOME: 이메일로 임시 링크를 받아서 비밀번호를 재설정할 수 있다
REQUIRED_BEHAVIORS:
  - ID: FR-1
    BEHAVIOR: 이메일 입력 후 재설정 링크 발송
    WHY: 사용자가 스스로 비밀번호를 바꿀 수 있어야 함
  - ID: FR-2
    BEHAVIOR: 링크는 30분 후 만료
    WHY: 보안 요건
  - ID: FR-3
    BEHAVIOR: 링크 사용 후 비밀번호 변경 완료 시 기존 세션 무효화
    WHY: 탈취 방지
ACCEPTANCE_SCENARIOS:
  - SCENARIO: 정상 링크로 접근
    EXPECTED_RESULT: 새 비밀번호 입력 화면 표시
  - SCENARIO: 만료된 링크로 접근
    EXPECTED_RESULT: "링크가 만료되었습니다" 메시지 표시
OUT_OF_SCOPE:
  - ITEM: 소셜 계정 연동 비밀번호 변경
    WHY_OUT: 소셜 로그인은 별도 처리
```

---

### `plan-screen-map` — 화면/페이지 흐름 설계

**한 줄 설명:** 화면과 페이지 간 이동 흐름을 먼저 그립니다.

**언제 써요?**
- UI 개발 전에 화면 구조와 이동 경로를 정리해야 할 때
- 서비스 흐름(사용자 여정)을 설계할 때
- "어떤 화면에서 어떤 화면으로 가는지" 팀이 공유해야 할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `IA_SCOPE` | ✅ | 범위 (`site` / `app` / `section` / `feature`) |
| `PRIMARY_USERS` | ✅ | 주요 사용자와 그들의 목표 |
| `CONTENT_OBJECTS` | ✅ | 반드시 있어야 할 페이지/화면 목록 |
| `ENTRY_POINTS` | ✅ | 사용자가 처음 진입하는 지점 |
| `KNOWN_FLOWS` | 선택 | 이미 알고 있는 이동 흐름 |
| `NAV_CONSTRAINTS` | 선택 | 플랫폼 제약, 라우팅 규칙 등 |

**예제**

```
$plan-screen-map
IA_SCOPE: app
PRIMARY_USERS:
  - USER: 온라인 쇼핑 고객
    GOAL: 상품을 골라서 구매 완료하기
CONTENT_OBJECTS:
  - ITEM: 메인 홈
    PURPOSE: 추천 상품과 카테고리 진입점
  - ITEM: 상품 목록
    PURPOSE: 카테고리별 상품 탐색
  - ITEM: 상품 상세
    PURPOSE: 상품 정보 확인 및 장바구니 담기
  - ITEM: 장바구니
    PURPOSE: 선택 상품 확인 및 결제 진행
  - ITEM: 결제
    PURPOSE: 배송지/결제 수단 입력
  - ITEM: 주문 완료
    PURPOSE: 주문 확인 및 이후 행동 안내
ENTRY_POINTS:
  - ENTRY: 홈 화면
    USER_NEED: 어디서 시작할지 파악
  - ENTRY: 외부 공유 링크
    USER_NEED: 특정 상품으로 바로 이동
```

---

### `plan-how-to-build` — 기술 설계 만들기

**한 줄 설명:** 요구사항이 확정된 후 데이터 흐름, 구조, 검증 방법까지 포함한 기술 설계를 만듭니다.

**언제 써요?**
- "어떻게 만들지" 기술적 설계가 필요할 때
- 복잡한 기능의 구현 전략을 문서로 남겨야 할 때
- 컴포넌트 경계와 트레이드오프를 팀과 공유해야 할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `DESIGN_SCOPE` | ✅ | 범위 (`feature` / `service` / `module` / `system`) |
| `IMPLEMENTATION_GOAL` | ✅ | 이 설계가 구현해야 할 핵심 기능 |
| `REQUIREMENT_SOURCES` | ✅ | 참고할 명세서나 계약 문서 |
| `SYSTEM_BOUNDARIES` | 선택 | 설계에 포함되어야 할 컴포넌트 |
| `CONSTRAINTS` | 선택 | 호환성, 성능, 마이그레이션 제약 |
| `ROLLBACK_OR_MIGRATION` | 선택 | 롤백이나 마이그레이션 고려사항 |

**예제**

```
$plan-how-to-build
DESIGN_SCOPE: feature
IMPLEMENTATION_GOAL: 이메일 인증 기반 비밀번호 재설정
REQUIREMENT_SOURCES:
  - REF: docs/specs/password-reset.md
    WHY_RELEVANT: 기능 요구사항과 엣지 케이스 규칙 정의
CONSTRAINTS:
  - CONSTRAINT: 기존 users 테이블 스키마 변경 없이 구현
ROLLBACK_OR_MIGRATION:
  - STEP: 기능 플래그로 점진적 배포
    WHY: 기존 로그인 흐름에 영향 없이 테스트
```

---

### `plan-dependency-rules` — 모듈 의존성 규칙 정하기

**한 줄 설명:** 어떤 모듈이 어떤 모듈을 참조해도 되는지 규칙을 정합니다.

**언제 써요?**
- 리팩터링 전에 모듈 경계를 명확히 해야 할 때
- "A가 B를 불러도 되나?" 혼란이 생길 때
- 순환 참조나 잘못된 레이어 참조를 정리해야 할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 규칙을 정할 경로/모듈/레이어 |
| `CURRENT_BOUNDARY_NOTES` | 선택 | 현재 알고 있는 의존성 문제 |

**예제**

```
$plan-dependency-rules
TARGET_SCOPE: src/
CURRENT_BOUNDARY_NOTES:
  - NOTE: UI 컴포넌트가 직접 DB 쿼리를 호출하는 경우가 있음
    EVIDENCE: src/components/ProductList.tsx에서 db.query() 직접 호출
  - NOTE: utils가 서로 순환 참조함
    EVIDENCE: src/utils/format.ts ↔ src/utils/date.ts
```

---

### `plan-verify-order` — 검증 순서 정하기

**한 줄 설명:** 코드를 바꾸기 전에 어떤 순서로 확인할지 계획합니다.

**언제 써요?**
- 큰 변경 전에 "어떤 테스트부터 돌려야 하지?" 결정해야 할 때
- 좁은 확인 → 넓은 확인 순서를 만들 때
- 변경 후 성공 기준을 미리 정해두고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 변경 대상 범위 |
| `CHANGE_GOAL` | ✅ | 무엇을 바꾸는지 |
| `RISK_AREAS` | 선택 | 특히 조심해야 할 영역 |

**예제**

```
$plan-verify-order
TARGET_SCOPE: src/payment
CHANGE_GOAL: 결제 로직을 새 PG사 SDK로 교체
RISK_AREAS:
  - RISK: 기존 결제 내역 조회
    WHY_IT_MATTERS: 이미 완료된 주문 데이터에 영향 줄 수 있음
  - RISK: 환불 처리
    WHY_IT_MATTERS: SDK가 바뀌면 환불 API 응답 형식이 달라질 수 있음
```

---

### `plan-task-breakdown` — 구현 태스크 문서 만들기

**한 줄 설명:** 설계를 실제 작업 목록으로 쪼개 `TASKS.md` 문서를 만듭니다.

**언제 써요?**
- 큰 구현 작업을 단계별 할 일 목록으로 나눠야 할 때
- 팀원과 작업을 나눠서 진행해야 할 때
- "다 됐다"는 기준을 미리 정해두고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `PLANNING_GOAL` | ✅ | 이 작업으로 무엇을 만드는지 |
| `TARGET_SCOPE` | ✅ | 작업 대상 범위 |
| `DONE_CONDITION` | ✅ | 완료 기준 (이걸 보면 다 됐다고 할 수 있는 것) |
| `PLAN_OUTPUT_PATH` | 선택 | 계획 문서 저장 경로 (기본: `plans/IMPLEMENTATION-PLAN.md`) |
| `TASKS_OUTPUT_PATH` | 선택 | 태스크 문서 저장 경로 (기본: `plans/TASKS.md`) |
| `ARTIFACT_MODE` | 선택 | `create` (새로 만들기) / `update` (기존 업데이트) |
| `CONSTRAINTS` | 선택 | 제약 조건 |
| `EXISTING_ARTIFACTS` | 선택 | 이미 있는 계획 문서 (ARTIFACT_MODE=update일 때 필요) |

**예제**

```
$plan-task-breakdown
PLANNING_GOAL: 비밀번호 재설정 기능 구현
TARGET_SCOPE: src/auth
DONE_CONDITION:
  - CONDITION: 이메일 발송 테스트 통과
  - CONDITION: E2E 시나리오 (정상/만료/중복) 통과
ARTIFACT_MODE: create
```

---

## build — 실제로 만드는 스킬

> 설계가 끝났으면 **손을 움직입니다**.

### `build-write-code` — 코드 구현하기

**한 줄 설명:** 실제 코드를 변경하고, 변경이 맞다는 검증 근거를 남깁니다.

**언제 써요?**
- 기능 추가, 버그 수정, 리팩터링을 직접 실행할 때
- 태스크 ID가 있는 작업을 구현하고 증거를 남겨야 할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `CHANGE_GOAL` | ✅ | 무엇을 바꿀지 (한 문장으로) |
| `TARGET_SCOPE` | ✅ | 어디를 바꿀지 (파일/폴더 경로) |
| `VERIFICATION_MAP` | ✅ | 검증 순서 (좁은 것 → 넓은 것 순서로) |
| `IMPLEMENTATION_MODE` | 선택 | `bugfix` / `feature` / `refactor` / `integration` / `cleanup` |
| `TASK_IDS` | 선택 | plans/TASKS.md의 태스크 ID (있으면) |
| `TASK_SOURCE` | 선택 | 태스크 출처 (`tasks-md` / `explicit-user` / `adhoc`) |
| `CONSTRAINTS` | 선택 | 바꾸면 안 되는 것, 지켜야 할 규칙 |

**예제**

```
$build-write-code
CHANGE_GOAL: 로그인 후 세션이 새로고침 시에도 유지되도록 수정
TARGET_SCOPE: src/auth/session.ts
VERIFICATION_MAP:
  - CHECK: auth/session 단위 테스트
    ORDER: 1
    PASS_CONDITION: 전체 통과
  - CHECK: 로그인 E2E 시나리오
    ORDER: 2
    PASS_CONDITION: 새로고침 후 세션 유지 확인
IMPLEMENTATION_MODE: bugfix
CONSTRAINTS:
  - CONSTRAINT: 쿠키 형식은 기존과 동일하게 유지
```

---

### `build-make-faster` — 성능 개선하기

**한 줄 설명:** 성능 병목을 측정하고 개선하며 전후 차이를 수치로 확인합니다.

**언제 써요?**
- "이 API가 너무 느린데 어디가 문제인지 찾고 고치고 싶다"
- 감이 아니라 측정 결과를 기반으로 최적화할 때
- 개선 전후를 수치로 비교해야 할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 최적화 대상 경로/모듈 |
| `METRIC_NAME` | ✅ | 지표 (`latency` / `throughput` / `memory` / `custom`) |
| `PERFORMANCE_BUDGET` | ✅ | 목표 수치 또는 개선 목표 |
| `BASELINE_EVIDENCE` | ✅ | 현재 측정값 (벤치마크, 프로파일 결과) |

**예제**

```
$build-make-faster
TARGET_SCOPE: api/v1/products
METRIC_NAME: latency
PERFORMANCE_BUDGET: 500ms → 200ms 이하로
BASELINE_EVIDENCE:
  - 현재 평균 응답시간 520ms (로컬 k6 측정, 50 VU)
  - DB 쿼리가 응답 시간의 80% 차지 (slow query log 확인)
```

---

## debug — 버그를 찾는 스킬

> 버그를 "느낌"이 아닌 **재현 가능한 사실**로 다룹니다.

### debug 스킬 순서

버그 하나를 처음부터 끝까지 다룰 때 아래 순서로 씁니다.

```
1. debug-capture-failure   — 재현 방법이 없다 → 재현 레시피 만들기
        ↓
2. debug-map-impact        — 재현은 됐다 → 영향 범위 파악하기
        ↓
3. debug-find-root-cause   — 영향 범위 파악 후 → 진짜 원인 찾기
        ↓
4. debug-confirm-fix       — 수정 완료 후 → 정말 고쳐졌는지 확인
```

이미 재현 방법을 알고 있다면 2번 또는 3번부터 시작해도 됩니다.

---

### `debug-capture-failure` — 재현 방법 만들기

**한 줄 설명:** "가끔 오류가 나요"를 누구나 재현할 수 있는 단계로 바꿉니다.

**언제 써요?**
- 버그가 있는데 어떻게 재현해야 할지 모를 때
- 다른 사람한테 버그를 설명해야 할 때
- 디버깅을 시작하기 전에 재현 레시피가 필요할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 오류가 나타나는 범위 |
| `FAILURE_SYMPTOM` | ✅ | 관찰된 오류 증상 |
| `EXPECTED_BEHAVIOR` | ✅ | 원래 어떻게 되어야 했는지 |
| `KNOWN_EVIDENCE` | 선택 | 로그, 에러 메시지 등 이미 알고 있는 것 |

**예제**

```
$debug-capture-failure
TARGET_SCOPE: src/checkout
FAILURE_SYMPTOM: 장바구니에서 결제 버튼 클릭 시 500 에러 발생
EXPECTED_BEHAVIOR: 결제 화면으로 이동
KNOWN_EVIDENCE:
  - TYPE: log
    REF: 서버 로그
    WHY_RELEVANT: "NullPointerException at PaymentService.java:45" 출력됨
```

---

### `debug-map-impact` — 버그 영향 범위 파악하기

**한 줄 설명:** 이 버그가 어디까지 번지는지, 무엇이 잘못된 건지 영향 지도를 그립니다.

**언제 써요?**
- 버그는 알겠는데 얼마나 심각한지, 어디까지 영향을 주는지 모를 때
- 고치기 전에 영향 받는 곳을 파악하고 싶을 때
- 어디서 디버깅을 시작해야 할지 모를 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 버그가 있는 범위 |
| `FAILURE_SYMPTOM` | ✅ | 관찰된 증상 |
| `EXPECTED_BEHAVIOR` | ✅ | 원래 되어야 할 동작 |
| `REPRO_HINTS` | 선택 | 재현에 필요한 조건 힌트 |

**예제**

```
$debug-map-impact
TARGET_SCOPE: src/payment
FAILURE_SYMPTOM: 결제 완료 후 주문 내역에 상품이 안 뜸
EXPECTED_BEHAVIOR: 결제 완료 시 주문 내역에 자동 추가
REPRO_HINTS:
  - 특정 카드사(국민카드)에서만 발생
  - 모바일 환경에서 재현율 높음
```

---

### `debug-find-root-cause` — 진짜 원인 찾기

**한 줄 설명:** 재현 가능한 버그의 진짜 원인을 추측이 아니라 증거 중심으로 찾습니다.

**언제 써요?**
- 버그는 재현됐는데 왜 일어나는지 모를 때
- "이게 왜 이렇게 되는 거야?" 파고들 때
- 수정 방향을 결정하기 전에 원인을 확실히 하고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `FAILURE_SYMPTOM` | ✅ | 관찰된 버그 증상 |
| `TARGET_SCOPE` | ✅ | 버그가 나타나는 범위 |
| `EXPECTED_BEHAVIOR` | ✅ | 원래 되어야 할 동작 |
| `REPRO_STATUS` | ✅ | 재현 가능 여부 (`yes` / `no` / `partial`) |
| `KNOWN_EVIDENCE` | 선택 | 스택 트레이스, 로그, 실패하는 테스트 등 |

**예제**

```
$debug-find-root-cause
FAILURE_SYMPTOM: 국민카드 결제 완료 후 주문 DB에 데이터가 안 들어감
TARGET_SCOPE: src/payment/OrderService.ts
EXPECTED_BEHAVIOR: 결제 완료 이벤트 수신 후 주문 테이블에 삽입
REPRO_STATUS: yes
KNOWN_EVIDENCE:
  - TYPE: log
    REF: webhook 수신 로그
    WHY_RELEVANT: 결제 webhook은 정상 수신되는데 DB 삽입 로그가 없음
```

---

### `debug-confirm-fix` — 수정이 정말 됐는지 확인

**한 줄 설명:** 수정 후 버그가 정말 사라졌는지, 다시 안 터지게 막았는지 확인합니다.

**언제 써요?**
- "고쳤는데 진짜 된 건지 확신이 없다"
- 수정 후 최종 검증이 필요할 때
- 회귀 방지 장치가 제대로 있는지 확인하고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 수정이 적용된 범위 |
| `FIX_CANDIDATE` | ✅ | 어떤 수정을 했는지 설명 |
| `EXPECTED_BEHAVIOR` | ✅ | 수정 후 기대하는 동작 |
| `REPRO_STEPS` | ✅ | 재현 단계 (수정 전 버그 재현에 쓰던 것) |
| `KNOWN_EVIDENCE` | 선택 | 테스트, 로그 등 이미 확인한 것 |

**예제**

```
$debug-confirm-fix
TARGET_SCOPE: src/payment/OrderService.ts
FIX_CANDIDATE: webhook 수신 후 트랜잭션 처리를 동기로 변경 (line 45)
EXPECTED_BEHAVIOR: 결제 완료 후 주문 내역에 즉시 표시
REPRO_STEPS:
  - STEP: 국민카드로 결제 진행
    PURPOSE: 버그 트리거 조건 재현
    EXPECTED_SIGNAL: 결제 완료 응답 수신
  - STEP: 결제 완료 후 주문 내역 조회
    PURPOSE: 수정 효과 확인
    EXPECTED_SIGNAL: 주문 내역에 상품 표시
```

---

## test — 테스트를 만드는 스킬

> 테스트를 "있다/없다"가 아닌 **무엇을 지키는가**로 봅니다.

### `test-find-gaps` — 테스트 빈 곳 찾기

**한 줄 설명:** 중요한 동작에 테스트가 빠진 곳이 어디인지 찾습니다.

**언제 써요?**
- "테스트가 충분한지 모르겠다"
- 코드는 있는데 테스트가 부족한 것 같을 때
- 어떤 테스트를 추가해야 할지 우선순위를 정하고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 점검할 범위 |
| `TEST_FOCUS` | ✅ | 집중할 종류 (`core-behavior` / `edge-cases` / `failure-paths` / `boundary-contracts` / `mixed`) |

**예제**

```
$test-find-gaps
TARGET_SCOPE: src/payment/
TEST_FOCUS: failure-paths
```

---

### `test-design-cases` — 테스트 케이스 설계하기

**한 줄 설명:** 정상, 경계, 실패 케이스를 빠짐없이 설계합니다.

**언제 써요?**
- 테스트를 짜기 전에 "어떤 케이스를 다뤄야 하지?" 목록을 먼저 만들 때
- 테스트 범위를 팀과 합의해야 할 때
- 빠진 시나리오가 없는지 체크하고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 테스트할 대상 |
| `TEST_GOAL` | ✅ | 테스트 목적 (`regression` / `edge-case` / `failure-path` / `mixed`) |
| `TARGET_BEHAVIORS` | ✅ | 반드시 포함해야 할 동작 목록 |

**예제**

```
$test-design-cases
TARGET_SCOPE: src/auth/login
TEST_GOAL: mixed
TARGET_BEHAVIORS:
  - BEHAVIOR: 올바른 이메일/비밀번호로 로그인 성공
    WHY_IT_MATTERS: 핵심 기능
  - BEHAVIOR: 틀린 비밀번호로 로그인 실패
    WHY_IT_MATTERS: 보안
  - BEHAVIOR: 비밀번호 5회 틀린 후 계정 잠금
    WHY_IT_MATTERS: 무차별 대입 공격 방지
```

---

### `test-write-guards` — 실제 테스트 작성

**한 줄 설명:** 실제 자동화 테스트를 써서 같은 버그가 다시 생기지 않도록 막습니다.

**언제 써요?**
- 버그 수정 후 회귀 방지 테스트가 필요할 때
- 새 기능에 테스트를 추가해야 할 때
- 테스트 케이스 설계가 끝난 후 실제 코드로 옮길 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TEST_GOAL` | ✅ | 테스트 목적 (`regression` / `edge-case` / `failure-path` / `mixed`) |
| `TARGET_SCOPE` | ✅ | 테스트할 범위 |
| `TARGET_BEHAVIORS` | ✅ | 테스트가 보호해야 할 동작 목록 |
| `FAILURE_PATHS` | 선택 | 포함해야 할 실패 경로 |
| `TEST_LAYER` | 선택 | 테스트 종류 (`unit` / `integration` / `contract` / `scenario`) |

**예제**

```
$test-write-guards
TEST_GOAL: regression
TARGET_SCOPE: src/payment/OrderService.ts
TARGET_BEHAVIORS:
  - 결제 완료 후 주문이 DB에 저장됨
  - 중복 결제 시 두 번째 요청이 거절됨
FAILURE_PATHS:
  - PG사 API 타임아웃 시 에러 반환 (저장 안 됨)
TEST_LAYER: integration
```

---

### `test-run-user-scenarios` — 실제 사용자처럼 테스트

**한 줄 설명:** 진짜 사용자가 쓸 법한 시나리오로 돌려보면서 헷갈리는 지점과 깨지는 곳을 찾습니다.

**언제 써요?**
- "실제 사용자가 쓰면 어떤 문제가 생길지 보고 싶다"
- 시스템 통합 테스트, 사용성 검증이 필요할 때
- 출시 전 또는 큰 리팩터링 전에 전체 흐름을 점검할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `SYSTEM_UNDER_TEST` | ✅ | 무엇을 테스트하는지 (`skill` / `workflow` / `macro-surface`) |
| `TARGET_SCOPE` | ✅ | 테스트 대상 범위 |
| `PRIMARY_USERS` | ✅ | 가상 사용자 페르소나와 그들의 목표 |
| `SCENARIO_COUNT` | 선택 | 생성할 시나리오 수 (기본: 6) |
| `FAILURE_CLASSES` | 선택 | 강제로 테스트할 실패 유형 |
| `KNOWN_CONSTRAINTS` | 선택 | 시나리오 제약 |

**예제**

```
$test-run-user-scenarios
SYSTEM_UNDER_TEST: workflow
TARGET_SCOPE: src/checkout/
PRIMARY_USERS:
  - ROLE: 신규 사용자
    GOAL: 처음으로 상품 구매 완료
    CONTEXT: 결제 수단 등록 안 됨
  - ROLE: 기존 사용자
    GOAL: 저장된 정보로 빠른 재구매
    CONTEXT: 배송지와 카드 등록됨
FAILURE_CLASSES:
  - CLASS: 결제 실패 후 재시도
  - CLASS: 세션 만료 중 결제 진행
SCENARIO_COUNT: 6
```
