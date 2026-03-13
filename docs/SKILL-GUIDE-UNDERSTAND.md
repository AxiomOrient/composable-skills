# 이해하기 — ask / clarify / analyze 스킬 가이드

> 이 파일은 [Atomic Skills 가이드](./ATOMIC-SKILLS-GUIDE.md)의 일부입니다.

---

## 이 파일의 스킬

| 카테고리 | 스킬 | 한 줄 설명 |
|----------|------|------------|
| ask | `ask-clarify-question` | 막연한 생각을 하나의 명확한 문제 문장으로 정리 |
| ask | `ask-break-it-down` | 하나의 큰 질문을 우선순위 있는 작은 질문 묶음으로 분해 |
| ask | `ask-flip-assumption` | 현재 질문에 숨은 전제를 뒤집어 새로운 시각 확보 |
| ask | `ask-fix-prompt` | 엉뚱한 답을 받았을 때 질문을 최소한으로 수정 |
| clarify | `clarify-scope` | 모호한 요청을 목표·범위·완료 기준이 있는 계약으로 변환 |
| clarify | `clarify-boundaries` | 이미 이해한 방향을 포함/제외/완료 기준으로 명확히 경계화 |
| analyze | `analyze-structure` | 코드 경계·결합도·데이터 흐름·숨은 의존성 지도화 |
| analyze | `analyze-complexity` | 복잡도를 필수/우발로 분류하고 제거 우선순위 도출 |
| analyze | `analyze-dependencies` | 모듈 의존성 방향·순환 의존성·결합도 지표 분석 |
| analyze | `analyze-impact` | 변경의 직접·간접·공유 상태 영향 범위 전체 파악 |
| analyze | `analyze-module-bounds` | 모듈·API 경계 계약 명확성과 책임 누수를 중립적으로 분석 |
| analyze | `analyze-baseline` | 최적화 전 통계적으로 유효한 성능 기준값 측정 |
| analyze | `analyze-options` | 여러 선택지를 근거 기반 가중치 점수표로 비교 |
| analyze | `analyze-evidence-gap` | 어떤 주장을 믿기 전 빠진 근거와 신뢰도 점수 확인 |
| analyze | `analyze-release-risk` | 릴리즈 게이트 상태를 GO/NO-GO 판정 없이 중립 분석 |

---

## ask — 질문을 다듬는 스킬

> 답을 구하기 전에, **무엇을 물어야 하는지** 먼저 다듬습니다.

### 어떤 ask 스킬을 써야 하나?

| 상황 | 쓸 스킬 |
|------|---------|
| 생각이 흐릿하고 뭘 물어야 할지도 모르겠다 | `ask-clarify-question` |
| 질문은 있는데 너무 크고 어디서 시작해야 할지 모른다 | `ask-break-it-down` |
| 같은 방향으로만 생각하다 막혔고 다른 각도가 필요하다 | `ask-flip-assumption` |
| 이미 물었는데 답이 틀렸거나 부족했다 | `ask-fix-prompt` |

---

### `ask-clarify-question` — 흐릿한 생각을 하나의 문제 문장으로

**한 줄 설명:** 막연한 주제나 생각을 세 개의 핵심 단어, 하나의 제약, 하나의 명확한 문제 문장으로 압축합니다.

**언제 써요?**
- "뭔가 해야 할 것 같은데 뭐부터 시작해야 할지 모르겠다"
- 머릿속에 생각이 많은데 핵심이 뭔지 모를 때
- 질문의 경계를 좁혀야 다음 단계로 넘어갈 수 있을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `RAW_TOPIC` | ✅ | 정리하고 싶은 주제나 생각 (지저분해도 됨) |
| `AUDIENCE` | 선택 | 이 질문의 답이 누구를 위한 것인지 |
| `CONSTRAINTS` | 선택 | 시간, 도메인, 리소스 등 알고 있는 제약 |

**예제**

```
$ask-clarify-question
RAW_TOPIC: 우리 앱이 느린 것 같은데 어디서부터 봐야 할지
AUDIENCE: 백엔드 개발자
```

---

### `ask-break-it-down` — 하나의 큰 질문을 작은 질문 묶음으로

**한 줄 설명:** 하나의 명확한 문제 문장을 비즈니스·기술·사용자 경험 레이어로 분리해 3~5개의 우선순위 있는 작은 질문으로 쪼갭니다.

**언제 써요?**
- 질문은 있는데 한 번에 다 해결하려다 막힐 때
- "이 문제가 너무 크다, 어디서부터 풀어야 하지?"
- 비즈니스·기술·사용자 레이어가 뒤섞여 혼란스러울 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `PROBLEM_STATEMENT` | ✅ | 쪼개고 싶은 하나의 명확한 문제 문장 |
| `AUDIENCE` | 선택 | 이 분석의 답이 누구를 위한 것인지 |
| `CONSTRAINTS` | 선택 | 비즈니스·기술·근거 관련 제약 |

**예제**

```
$ask-break-it-down
PROBLEM_STATEMENT: 우리 서비스의 보안을 강화하려면 무엇부터 해야 하나?
AUDIENCE: 스타트업 개발자
CONSTRAINTS: 시간이 별로 없음
```

---

### `ask-flip-assumption` — 숨은 전제를 뒤집어 새 시각 열기

**한 줄 설명:** 현재 질문에 숨어 있는 전제 세 개를 찾아내고 각각을 뒤집어서 시각을 바꾸는 도전 질문 두 개를 만들어 냅니다.

**언제 써요?**
- 같은 방향으로만 생각하다 막혔을 때
- 현재 질문이 특정 해결책을 전제하고 있는 것 같을 때
- "왜 이렇게 해야 하지?" 의문이 들 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `CORE_QUESTION` | ✅ | 지금 막혀 있는 핵심 질문 |
| `ASSUMPTIONS` | 선택 | 이미 파악한 전제 목록 |
| `CONSTRAINTS` | 선택 | 범위·근거·도메인 제한 |

**예제**

```
$ask-flip-assumption
CORE_QUESTION: 사용자가 회원가입을 해야만 서비스를 쓸 수 있어야 하는가?
```

---

### `ask-fix-prompt` — 엉뚱한 답을 받았을 때 질문 고치기

**한 줄 설명:** 실패한 답변의 원인을 분류하고 질문을 최소한으로 수정해 수정된 프롬프트를 돌려줍니다.

**언제 써요?**
- 이미 받은 답이 틀렸거나 범위를 벗어났거나 형식이 맞지 않았을 때
- "왜 이게 안 통하지?" 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TOPIC` | ✅ | 원래 주제 |
| `QUESTION_OR_STACK` | ✅ | 원래 질문 또는 질문 묶음 |
| `BAD_ANSWER` | ✅ | 만족스럽지 못했던 실제 답변 내용 |

**예제**

```
$ask-fix-prompt
TOPIC: Python 파일 읽기
QUESTION_OR_STACK: "파이썬으로 CSV 파일 읽는 법 알려줘"
BAD_ANSWER: "pandas를 설치하세요"라는 답만 왔고 실제 코드는 없었음
```

---

## clarify — 범위와 경계를 명확히 하는 스킬

> 흐릿한 요청을 명확한 계약으로 바꿉니다. **무엇을 할지 모르면 시작하지 않습니다.**

### 어떤 clarify 스킬을 써야 하나?

| 상황 | 쓸 스킬 |
|------|---------|
| 요청이 막연하고 무엇을 해야 할지 모른다 | `clarify-scope` |
| 방향은 알겠는데 포함/제외 경계만 글로 정리하고 싶다 | `clarify-boundaries` |

---

### `clarify-scope` — 모호한 요청을 명확한 범위로

**한 줄 설명:** "뭔가 해줘"를 목표·포함·제외·완료 기준이 있는 범위 계약으로 바꾸고, 아직 불명확한 것을 질문으로 표면화합니다.

**언제 써요?**
- 요청이 너무 막연해서 어디서 시작해야 할지 모를 때
- 완료 기준이 불분명할 때
- 계획이나 구현 전에 명확한 질문을 먼저 던져야 할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `REQUEST` | ✅ | 원래 요청 (막연해도 됨, 원문 그대로) |
| `TARGET_SCOPE` | ✅ | 대상 파일·폴더·모듈·저장소 |
| `KNOWN_CONSTRAINTS` | 선택 | 이미 알고 있는 제약이나 비목표 |
| `KNOWN_DONE_CONDITION` | 선택 | 이미 생각해둔 완료 기준 |

**예제**

```
$clarify-scope
REQUEST: 코드 좀 정리해줘
TARGET_SCOPE: src/utils
KNOWN_CONSTRAINTS: 기능 변경 없이, 이번 주 안에
```

---

### `clarify-boundaries` — 이번 일의 경계를 명확히

**한 줄 설명:** 이미 이해한 작업 방향을 포함/제외/완료 기준으로 명문화해 하위 계획이나 명세 작성에 바로 쓸 수 있는 범위 계약을 만듭니다.

**언제 써요?**
- 방향은 알지만 경계를 글로 정리해야 다음 단계로 넘어갈 수 있을 때
- 작업 범위가 자꾸 늘어날 것 같을 때
- "어디까지가 내 일이지?" 헷갈릴 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `REQUEST` | ✅ | 원래 요청 |
| `TARGET_SCOPE` | ✅ | 대상 경로·모듈·저장소 |
| `KNOWN_CONSTRAINTS` | 선택 | 이미 알고 있는 제약이나 비목표 |

**예제**

```
$clarify-boundaries
REQUEST: 결제 모듈 리팩터링
TARGET_SCOPE: src/payment
KNOWN_CONSTRAINTS: 외부 결제 API 연동 코드는 건드리지 않음
```

---

## analyze — 판정 없이 분석하는 스킬

> **결론 없이 사실만** 만듭니다. GO/NO-GO 없음, 통과/실패 없음.
> 판정이 필요하면 `review-*` 스킬을 쓰세요.

### 어떤 analyze 스킬을 써야 하나?

| 상황 | 쓸 스킬 |
|------|---------|
| 코드 구조, 결합도, 데이터 흐름을 파악하고 싶다 | `analyze-structure` |
| 복잡도가 어디서 오는지, 뭘 없애면 되는지 알고 싶다 | `analyze-complexity` |
| 모듈 의존성 방향과 순환 의존성을 파악하고 싶다 | `analyze-dependencies` |
| 변경의 직간접 영향 범위를 파악하고 싶다 | `analyze-impact` |
| 모듈·API 경계 계약과 책임 누수를 확인하고 싶다 | `analyze-module-bounds` |
| 최적화 전 통계적으로 신뢰할 수 있는 기준값이 필요하다 | `analyze-baseline` |
| 선택지를 근거와 점수로 비교하고 싶다 | `analyze-options` |
| 어떤 주장이 맞는지 확신하기 전에 빠진 근거를 확인하고 싶다 | `analyze-evidence-gap` |
| 릴리즈 게이트 상태를 판정 없이 확인하고 싶다 | `analyze-release-risk` |

---

### `analyze-structure` — 코드 구조 깊이 분석

**한 줄 설명:** 코드의 경계, 결합도, 데이터 흐름, 숨겨진 의존성을 지도로 그립니다.

**언제 써요?**
- 처음 보는 코드를 깊이 이해해야 할 때
- 리팩터링 전에 결합도와 숨겨진 의존성을 파악할 때
- 설계 작업 전에 현재 구조 증거가 필요할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 분석할 파일·모듈·폴더·저장소 |
| `ANALYSIS_QUESTION` | 선택 | 특별히 해결하고 싶은 구조 질문 |
| `ANALYSIS_FOCUS` | 선택 | 분석 관점 (`coupling` / `data-flow` / `boundaries` / `hidden-state` / `mixed`) |
| `KNOWN_EVIDENCE` | 선택 | 이미 알고 있는 파일·문서·흔적 정보 |
| `CONSTRAINTS` | 선택 | 범위나 시간 제한 |

**예제**

```
$analyze-structure
TARGET_SCOPE: src/auth
ANALYSIS_FOCUS: coupling
```

---

### `analyze-complexity` — 복잡도 원인 분석

**한 줄 설명:** 복잡도를 도메인이 요구하는 필수 복잡도와 구조 문제로 인한 우발 복잡도로 분류하고 제거 우선순위를 제시합니다.

**언제 써요?**
- "이 코드가 왜 이리 복잡하지?" 이유를 알고 싶을 때
- 리팩터링 전에 복잡도 핫스팟을 파악할 때
- 어떤 복잡도를 건드리면 안 되는지 먼저 알고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 복잡도를 분석할 경로·모듈·저장소 |
| `COMPLEXITY_FOCUS` | 선택 | 집중할 복잡도 (`cyclomatic` / `coupling` / `cognitive` / `hidden-state` / `mixed`) |

**예제**

```
$analyze-complexity
TARGET_SCOPE: src/auth
COMPLEXITY_FOCUS: coupling
```

---

### `analyze-dependencies` — 의존성 그래프와 순환 의존성

**한 줄 설명:** 모듈 의존성 방향, 순환 의존성, 결합도 지표를 분석하고 안정화가 필요한 모듈을 찾습니다.

**언제 써요?**
- "이 모듈들이 서로 얽혀 있는 것 같다"
- 모듈 분리 전에 의존성 현황을 파악할 때
- 아키텍처 규칙 위반 여부를 확인할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 의존성을 분석할 경로·모듈·저장소 |
| `DEP_FOCUS` | 선택 | 집중 영역 (`direction` / `cycles` / `coupling` / `violations` / `mixed`) |
| `ALLOWED_DIRECTIONS` | 선택 | 허용된 의존성 방향 규칙 (위반 감지용) |

**예제**

```
$analyze-dependencies
TARGET_SCOPE: src/
DEP_FOCUS: cycles
```

---

### `analyze-impact` — 변경의 직간접 영향 범위

**한 줄 설명:** 변경이 무엇을 건드리는지 직접 영향, 간접 영향, 공유 상태 위험까지 심각도 순으로 전체 파악합니다.

**언제 써요?**
- 변경 전에 "어디까지 영향을 줄까?" 확인할 때
- 릴리즈 전 위험 표면을 파악할 때
- 공유 상태나 전이적 호출 경로가 걱정될 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 변경이 일어나는 파일·모듈·폴더·저장소 |
| `CHANGE_DESCRIPTION` | ✅ | 변경 목적 한 줄 설명 |
| `IMPACT_DEPTH` | 선택 | 영향 추적 깊이 (`direct` / `transitive` / `full`, 기본값 `transitive`) |
| `CONSTRAINTS` | 선택 | 추적 범위나 시간 제한 |

**예제**

```
$analyze-impact
TARGET_SCOPE: src/auth/token-service.ts
CHANGE_DESCRIPTION: JWT 페이로드에 만료 필드 추가
IMPACT_DEPTH: transitive
```

---

### `analyze-module-bounds` — 모듈 경계 계약 중립 분석

**한 줄 설명:** 모듈·API·레이어 경계의 계약 명확성, 소유권, 책임 누수를 판정 없이 분석합니다.

**언제 써요?**
- "이 모듈이 너무 많은 걸 알고 있는 것 같다" → 현황 파악할 때
- 리팩터링 전에 경계 현황 증거가 먼저 필요할 때
- 명시된 계약과 암묵적 가정이 어디서 충돌하는지 확인할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 분석할 경계 경로·모듈·API |
| `BOUNDARY_KIND` | ✅ | 경계 종류 (`module` / `api` / `service` / `layer`) |
| `ANALYSIS_DEPTH` | 선택 | 분석 깊이 (`surface` = 인터페이스만 / `full` = 내부 소유권까지, 기본값 `full`) |

**예제**

```
$analyze-module-bounds
TARGET_SCOPE: src/auth/
BOUNDARY_KIND: module
```

---

### `analyze-baseline` — 성능 기준값 통계적 측정

**한 줄 설명:** 최적화를 시작하기 전에 분산 분석과 신뢰 구간을 포함한 재현 가능한 성능 기준값을 기록합니다.

**언제 써요?**
- "빠르게 만들기 전에 지금 얼마나 느린지부터 재자"
- 전후 비교를 통계적으로 신뢰할 수 있게 하고 싶을 때
- 목표 수치의 근거가 필요할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 측정할 대상 경로·모듈·저장소 |
| `METRIC_NAME` | ✅ | 측정할 지표 (`latency` / `throughput` / `memory` / `cpu` / `custom`) |
| `MEASUREMENT_METHOD` | ✅ | 측정 방법 (`command` / `benchmark` / `profile` / `custom`) |
| `SAMPLE_SIZE` | 선택 | 샘플 수 (없으면 95% 신뢰도에 필요한 최솟값 자동 적용) |
| `BUDGET_HINT` | 선택 | 이미 알고 있는 목표 수치나 임계값 |

**예제**

```
$analyze-baseline
TARGET_SCOPE: api/v1/search
METRIC_NAME: latency
MEASUREMENT_METHOD: benchmark
SAMPLE_SIZE: 100
BUDGET_HINT: 200ms 이하
```

---

### `analyze-options` — 선택지 점수 기반 비교

**한 줄 설명:** 여러 선택지를 기준별 가중치 점수표와 근거로 비교하고 하나의 추천을 제시합니다.

**언제 써요?**
- "A로 갈까 B로 갈까" 결정을 내려야 할 때
- 직관이 아닌 근거로 기술 선택을 해야 할 때
- 점수 비교 결과와 함께 추천 이유가 필요할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 이 결정이 적용되는 파일·모듈·폴더·저장소 |
| `DECISION_QUESTION` | ✅ | 해결해야 할 결정 질문 (하나의 선택) |
| `OPTION_SET` | ✅ | 비교할 선택지 목록 (각각 이름과 설명 포함) |
| `DECISION_CRITERIA` | 선택 | 평가 기준과 비중 (없으면 문맥에서 자동 도출) |
| `KNOWN_EVIDENCE` | 선택 | 이미 알고 있는 파일·문서·측정값 |
| `CONSTRAINTS` | 선택 | 반드시 지켜야 할 제약 (선택지를 탈락시킬 수 있는 것) |

**예제**

```
$analyze-options
TARGET_SCOPE: 백엔드 API 인증
DECISION_QUESTION: JWT vs 세션 쿠키 중 무엇이 더 맞나?
OPTION_SET:
  - option: JWT (stateless), description: 서버 상태 없이 토큰으로 인증
  - option: 세션 쿠키 (stateful), description: 서버에 세션 저장
DECISION_CRITERIA:
  - criterion: 모바일 호환성, weight: 높음
  - criterion: 서버 부하, weight: 중간
  - criterion: 보안, weight: 높음
```

---

### `analyze-evidence-gap` — 빠진 근거와 신뢰도 확인

**한 줄 설명:** 어떤 주장을 믿기 전에 현재 근거의 신뢰도 점수(0-100)와 빠진 증거, 다음으로 확인할 것을 정보 가치 순으로 제시합니다.

**언제 써요?**
- "이게 맞다고 확신하기 전에 뭘 더 확인해야 하지?"
- 설계 결정 전 근거가 충분한지 검증할 때
- 막연한 "확실하지 않다"가 아니라 정확히 뭐가 빠졌는지 알고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 주장이 적용되는 파일·모듈·폴더·저장소 |
| `CLAIM_UNDER_CHECK` | ✅ | 확인하려는 주장이나 가정 (정확하게) |
| `KNOWN_EVIDENCE` | 선택 | 이미 갖고 있는 근거 |
| `CONSTRAINTS` | 선택 | 추가 조사 범위나 비용 제한 |

**예제**

```
$analyze-evidence-gap
TARGET_SCOPE: src/cache
CLAIM_UNDER_CHECK: Redis 캐시가 응답 속도를 50% 이상 개선한다
KNOWN_EVIDENCE: 개발 환경 벤치마크 결과
```

---

### `analyze-release-risk` — 릴리즈 위험 중립 분석

**한 줄 설명:** 릴리즈 게이트 상태(통과/실패/미확인)를 근거와 함께 파악하고 위험 수준을 GO/NO-GO 판정 없이 설명합니다.

**언제 써요?**
- 배포 전 "어떤 게이트가 미확인 상태인가?" 파악할 때
- GO/NO-GO 판정 전에 위험 현황 데이터가 필요할 때
- 릴리즈 근거를 감사 기록으로 남기고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 분석할 diff·파일·모듈·폴더·저장소 |
| `RISK_FOCUS` | ✅ | 집중할 위험 차원 (`regression` / `compatibility` / `security` / `performance` / `mixed`) |
| `CHANGE_INTENT` | ✅ | 변경 목적 한 줄 설명 |
| `KNOWN_GATE_SIGNAL` | 선택 | 이미 알고 있는 테스트·보안·CI 신호 |

**예제**

```
$analyze-release-risk
TARGET_SCOPE: diff
RISK_FOCUS: regression
CHANGE_INTENT: 결제 모듈 PG사 교체
```
