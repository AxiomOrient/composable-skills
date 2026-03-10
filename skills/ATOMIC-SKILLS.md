# Atomic Skills — 완전 가이드

> **\"한 번에 한 가지만 제대로.\"**
> 아토믹 스킬은 특정 문제 하나만 완벽하게 해결하는 최소 단위의 도구입니다.
> 여러 개를 묶어 쓰고 싶다면 [SKILL-COMBOS.md](./SKILL-COMBOS.md)를 참고하세요.
> 카테고리나 업무 묶음부터 고르고 싶다면 [packs/README.md](./packs/README.md)를 먼저 보세요.

---

## 카테고리와 prefix 체계

스킬 이름의 앞부분(prefix)을 보면 같은 카테고리임을 바로 알 수 있습니다.

| Prefix   | 카테고리                                 | 핵심 질문                       |
| :------- | :--------------------------------------- | :------------------------------ |
| `scout-` | [상황 파악](#scout--상황-파악)           | 뭐가 문제야? 어디까지 해?       |
| `ask-`   | [질문 설계·수리](#ask--질문-설계와-수리) | 뭘 물어야 하지? 왜 답이 별로야? |
| `check-` | [리뷰와 검증](#check--리뷰와-검증)       | 이거 합쳐도 돼? 안전해?         |
| `debug-` | [버그 분석](#debug--버그-분석)           | 어디서 터졌어? 왜 안 돼?        |
| `plan-`  | [기획과 설계](#plan--기획과-설계)        | 왜 만들어? 어떻게 만들어?       |
| `test-`  | 테스트 설계·검증                         | 뭘 시험하고 어디서 깨져?        |
| `build-` | [구현과 실행](#build--구현과-실행)       | 코드 짜고 바꿨어?               |
| `tidy-`  | [구조 개선](#tidy--구조-개선)            | 코드 더 깔끔해질 수 있어?       |
| `doc-`   | [문서화](#doc--문서화)                   | 문서 썼어? 정리됐어?            |
| `ship-`  | [릴리즈 준비](#ship--릴리즈-준비)        | 배포해도 돼?                    |

---

## 퀵 메뉴

| 내 상황                                         | 쓸 스킬                   |
| :---------------------------------------------- | :------------------------ |
| 증거 기반으로 상황을 객관적으로 분석해야 할 때  | `scout-facts`             |
| 요청 범위가 뭔지 먼저 잡아야 할 때              | `scout-scope`             |
| 할 것과 안 할 것의 선을 그어야 할 때            | `scout-boundaries`        |
| 뭘 물어야 할지 모를 때                          | `ask-find-question`       |
| 큰 질문을 쪼개고 싶을 때                        | `ask-break-it-down`       |
| 기존 전제를 뒤집고 싶을 때                      | `ask-flip-assumption`     |
| 받은 답이 별로라서 질문을 고치고 싶을 때        | `ask-fix-prompt`          |
| PR 머지 전에 종합 리뷰가 필요할 때              | `check-merge-ready`       |
| 배포 전 위험 점검이 필요할 때                   | `check-ship-risk`         |
| 9종 체크리스트 전부 돌리고 싶을 때              | `check-quality-scan`      |
| 보안 취약점만 집중해서 보고 싶을 때             | `check-security-holes`    |
| 모듈 경계가 제대로 지켜지는지 볼 때             | `check-module-walls`      |
| 에러 처리와 예외 경로만 볼 때                   | `check-failure-paths`     |
| 빠진 테스트를 먼저 찾고 싶을 때                 | `test-find-gaps`            |
| 작업 후 요구사항을 다 만족했는지 최종 확인      | `check-delivered`         |
| 버그 범위를 먼저 지도로 그리고 싶을 때          | `debug-map-blast-radius`  |
| 버그 근본 원인을 찾고 싶을 때                   | `debug-find-root-cause`   |
| 기능을 왜 만드는지 정리하고 싶을 때             | `plan-why-build-this`     |
| 기능이 정확히 어떻게 동작해야 하는지 정할 때    | `plan-what-it-does`       |
| 화면 구조와 탐색 흐름을 설계할 때               | `plan-screen-map`         |
| 기술 구조와 설계도가 필요할 때                  | `plan-how-to-build`       |
| 실행 계획서가 필요할 때                         | `plan-task-breakdown`        |
| 구현 전에 검증 순서를 정하고 싶을 때            | `plan-verify-order`       |
| 테스트 케이스 목록을 체계적으로 만들고 싶을 때  | `test-design-cases`        |
| 최적화 전에 현재 성능을 기록하고 싶을 때        | `scout-baseline`   |
| 의존성 방향 규칙을 정하고 싶을 때               | `plan-dependency-rules`          |
| 코드를 직접 짤 때                               | `build-write-code`        |
| 테스트를 추가할 때                              | `test-write-guards`        |
| 실제 사용자처럼 시나리오를 돌려 보고 싶을 때    | `test-run-user-scenarios`  |
| 성능을 개선할 때                                | `build-make-faster`       |
| 완료 조건이 만족될 때까지 코드 구현을 반복할 때 | `build-until-done`        |
| 코드 아닌 작업을 완료 조건까지 반복할 때        | `finish-until-done`       |
| 중복 코드를 찾고 싶을 때                        | `tidy-find-copies`        |
| 매직 넘버·하드코딩된 상수를 찾고 싶을 때        | `tidy-find-magic-numbers` |
| 복잡도의 원인이 뭔지 파악하고 싶을 때           | `tidy-why-complex`        |
| 불필요한 복잡한 구조를 단순하게 만들고 싶을 때  | `tidy-cut-fat`            |
| 기능은 유지하며 구조만 재배치하고 싶을 때       | `tidy-reorganize`         |
| 문서를 새로 쓰거나 업데이트할 때                | `doc-write`               |
| 모듈·라이브러리 계층 인덱스 문서가 필요할 때    | `doc-build-index`         |
| 루트 README와 다국어 docs를 발행할 때           | `doc-publish-readme`      |
| 문서 구조를 정비하고 큐레이션할 때              | `doc-curate`              |
| 문서 현황 전체를 목록화하고 싶을 때             | `doc-find-all`            |
| 릴리즈 전 Git 저장소 상태를 확인할 때           | `ship-check-repo`         |
| 레거시·문서 위생을 릴리즈 전에 점검할 때        | `ship-check-hygiene`      |
| 배포해도 안전한지 최종 판정이 필요할 때         | `ship-go-nogo`            |
| Conventional Commit 메시지를 만들고 싶을 때     | `ship-commit`             |

---

## `scout-` — 상황 파악

막연한 요청을 구체적인 작업으로 바꾸는 첫 단계입니다.

---

### `scout-facts` — 중립 사실 분석

**한마디로**: 감정·의견없이 증거와 해석, 선택지만 정리하는 탐정 역할

**언제 쓰나**

- \"이 상황이 왜 이렇게 됐는지 객관적으로 봐줘\"
- \"A 방법과 B 방법의 차이를 편견 없이 비교해줘\"
- 아직 구현이나 수정은 안 하고 분석만 필요할 때

**언제 쓰면 안 되나**: 직접 코드를 고쳐야 하거나, 버그 원인을 확인해야 할 때 (→ `debug-find-root-cause` 사용)

**필요한 입력값**

- `ANALYSIS_GOAL`: 분석의 목적
- `TARGET_SCOPE`: 분석할 파일·폴더·모듈

**받는 결과**: 관찰된 증거 목록, 추론된 결론, 열린 가능성 목록

**예시**

```text
$scout-facts
ANALYSIS_GOAL: 서버 응답이 느려진 원인 파악 (구현 아님)
TARGET_SCOPE: src/api/handlers
```

---

### `scout-scope` — 요청 명확화

**한마디로**: \"대충 해줘\"를 \"목표, 범위, 완료 기준\"으로 구체화하는 통역사

**언제 쓰나**

- 작업 범위가 불명확해서 시작하기 전에 방향을 잡아야 할 때
- 나중에 \"이게 아니었는데\"를 방지하고 싶을 때

**언제 쓰면 안 되나**: 이미 명확한 작업이 있을 때, 전체 계획서가 필요할 때 (→ `plan-task-breakdown`)

**필요한 입력값**

- `REQUEST`: 원래 요청
- `TARGET_SCOPE`: 작업 대상 범위

**받는 결과**: 명확화 질문 목록, 초안 범위 계약서 (목표·범위·완료기준)

---

### `scout-boundaries` — 범위 확정

**한마디로**: 할 일과 안 할 일의 선을 명확하게 그어주는 계약서 작성기

**언제 쓰나**

- 요청이 너무 넓어서 계획이나 스펙을 쓰기 전에 범위를 좁혀야 할 때
- \"이번엔 여기까지만, 저건 다음에\"를 문서로 남기고 싶을 때

**필요한 입력값**

- `REQUEST`: 원래 요청
- `TARGET_SCOPE`: 작업 대상
- `KNOWN_CONSTRAINTS`: 이미 알고 있는 제약사항 (선택)

**받는 결과**: 목표 정의, 포함 범위, 제외 범위, 완료 조건

---

### `scout-baseline` — 성능 기준값 측정

**한마디로**: 최적화 또는 변경 전에 "지금 얼마나 빠른지/느린지"를 기록하는 도구

**언제 쓰나**

- 최적화 전에 현재 기준값을 먼저 고정해야 할 때
- before/after 비교를 위해 같은 메트릭과 측정 방식을 먼저 정해야 할 때

**필요한 입력값**

- `TARGET_SCOPE`: 측정 대상
- `METRIC_NAME`: latency | throughput | memory | custom

**받는 결과**: 메트릭 정의, 기준값 결과, 성능 예산(Performance Budget)

---

## `ask-` — 질문 설계와 수리

AI에게 더 좋은 답을 얻기 위해 질문 자체를 다듬습니다.

---

### `ask-find-question` — 막연한 주제를 하나의 문제 정의로

**한마디로**: 머릿속 안개 같은 생각을 한 문장 문제 정의로 바꿔주는 도구

**언제 쓰나**

- \"뭔가 문제가 있긴 한데 뭘 물어봐야 할지 모르겠어\"
- 질문의 방향 자체가 흐릴 때

**필요한 입력값**

- `RAW_TOPIC`: 생각이나 주제 (지저분해도 됨)
- `CONSTRAINTS`: 알고 있는 제약사항 (선택)

**받는 결과**: 핵심 키워드 3개, 피해야 할 것들, 한 문장 문제 정의

---

### `ask-break-it-down` — 큰 질문을 3~5개로 분해

**한마디로**: 복잡한 주제를 답할 수 있는 단위로 쪼개주는 분해기

**언제 쓰나**

- 질문은 있지만 너무 커서 모르는 게 여러 개 섞여 있을 때

**필요한 입력값**

- `PROBLEM_STATEMENT`: 하나의 문제 정의 문장
- `AUDIENCE`: 답을 받을 대상 (선택)

**받는 결과**: 우선순위가 있는 3~5개 질문 스택, 핵심 질문 하나

---

### `ask-flip-assumption` — 전제를 뒤집어 새 관점 발굴

**한마디로**: \"당연하다\"고 생각한 전제를 뒤집어서 돌파구를 찾는 도구

**언제 쓰나**

- 같은 방식으로 생각하다가 막혔을 때
- 질문이 너무 기능 중심이라서 본질을 놓치고 있을 때

**필요한 입력값**

- `CORE_QUESTION`: 현재 질문
- `ASSUMPTIONS`: 이미 알고 있는 전제들 (선택)

**받는 결과**: 전제 목록, 전제 뒤집기 테스트, 관점을 바꾸는 질문 2개

---

### `ask-fix-prompt` — 나쁜 답변을 고치는 질문 수정

**한마디로**: 받은 답이 별로일 때 질문의 어디가 잘못됐는지 찾아 최소한으로 고쳐주는 도구

**언제 쓰나**

- AI가 내 질문을 오해했을 때
- 답이 너무 일반적이거나 관계없는 내용일 때

**필요한 입력값**

- `QUESTION_OR_STACK`: 원래 질문
- `BAD_ANSWER`: 마음에 안 드는 답변

**받는 결과**: 실패 유형 분류, 왜 답이 잘못됐는지, 최소 수정 방향

---

## `check-` — 리뷰와 검증

만든 것이 안전하고 깨끗한지 확인합니다.

---

### `check-merge-ready` — PR 머지 전 종합 리뷰

**한마디로**: \"이 코드 합쳐도 돼?\"에 증거 기반으로 integrate/hold 판정을 내려주는 리뷰어

**언제 쓰나**

- PR 머지 전에 문제를 종합적으로 찾고 싶을 때
- 보안, 호환성, 스타일 등 여러 각도로 한 번에 보고 싶을 때

**언제 쓰면 안 되나**: 9종 체크리스트 전체가 필요할 때 (→ `check-quality-scan`)

**필요한 입력값**

- `REVIEW_GOAL`: `general-verdict` | `regression-risk` | `change-intent-check` | `narrow-focus`
- `TARGET_SCOPE`: 리뷰할 범위
- `CHANGE_INTENT`: 이 변경의 목적

**받는 결과**: 심각도/근거가 있는 발견 목록, 테스트 공백, integrate 또는 hold 판정

---

### `check-ship-risk` — 배포·출시 위험 점검

**한마디로**: 배포해도 되는지 '보안 게이트' 관점에서 집중 심사하는 검사관

**언제 쓰나**

- 배포 전에 릴리즈 위험이 있는지 확인할 때
- \"출시해도 안전한가?\"를 봐야 할 때

**필요한 입력값**

- `AUDIT_GOAL`: 감사 목적
- `TARGET_SCOPE`: 감사 범위

**받는 결과**: 게이트 통과/차단 상태, 증거 기반 감사 결과

---

### `check-quality-scan` — 9종 품질 체크리스트

**한마디로**: 설계·성능·보안·중복·불필요 코드 등 9가지 항목을 전부 체크하는 점검표

**9가지 점검 항목**: 설계 우아함 / 코드 간결성 / 잠재 버그 / 목적 달성 / 보안 / 중복 코드 / 성능 / 상수·공통화 가능성 / 불필요한 코드

**언제 쓰나**

- \"빠진 항목 없이 다 봤다\"는 근거를 남기고 싶을 때

**언제 쓰면 안 되나**: 특정 한 가지만 확인하면 될 때 (`check-merge-ready`, `check-security-holes` 등 사용)

**필요한 입력값**

- `CHECK_SCOPE`: 검사할 범위
- `CHANGE_GOAL`: 이 변경의 의도

**받는 결과**: 9종 항목별 pass/risk/unknown 표, 발견 요약

---

### `check-security-holes` — 보안 취약점 집중 감사

**한마디로**: 해킹·데이터 유출 가능성만 집중해서 찾는 보안 전문가

**언제 쓰나**

- 인증, 권한, API 키, 입력 검증 등 보안 관련 코드를 집중 검토할 때

**필요한 입력값**

- `SECURITY_GOAL`: `check-ship-risk` | `threat-model` | `mitigation-verify`
- `TARGET_SCOPE`: 검사 범위
- `ASSETS_OR_BOUNDARIES`: 중요 자산·신뢰 경계·진입점 목록

**받는 결과**: 위협 모델, 우선순위별 취약점 목록, 완화 조치 확인 결과

---

### `check-module-walls` — 모듈 경계 계약 검증

**한마디로**: \"이 모듈이 저 모듈의 비밀을 너무 많이 알고 있는지\" 확인하는 도구

**언제 쓰나**

- 모듈 간 의존성이 제대로 지켜지는지 확인하고 싶을 때

**필요한 입력값**

- `TARGET_SCOPE`: 확인할 범위
- `BOUNDARY_KIND`: `api` | `module` | `service`

**받는 결과**: 경계 계약 목록, 누설된 가정들, 강화 조치 목록

---

### `check-failure-paths` — 실패 경로 집중 리뷰

**한마디로**: 에러가 났을 때, 예외 상황일 때, 정리 로직이 제대로 작동하는지 확인하는 도구

**언제 쓰나**

- 정상 경로는 OK지만 예외 처리, 클린업이 제대로 됐는지 의심될 때

**필요한 입력값**

- `TARGET_SCOPE`: 검사 범위
- `FAILURE_MODES`: 알고 있는 실패 모드 (선택)

**받는 결과**: 에러 경로 발견 목록, 빠진 가드 목록

---

### `test-find-gaps` — 테스트 공백 파악

**한마디로**: 지금 테스트가 어디를 못 커버하는지 찾아주는 X-ray

**언제 쓰나**

- 테스트를 추가하기 전에 어디가 빠졌는지 먼저 파악하고 싶을 때

**언제 쓰면 안 되나**: 테스트 코드 바로 작성하려고 할 때 (→ `test-write-guards` 사용)

**필요한 입력값**

- `TARGET_SCOPE`: 검사 범위
- `TEST_FOCUS`: `core-behavior` | `edge-cases` | `failure-paths` | `boundary-contracts` | `mixed`

**받는 결과**: 빠진 테스트 시나리오, 우선순위 테스트 목록

---

### `check-delivered` — 최종 납품 전 계약 검증

**한마디로**: 작업 후 \"약속한 대로 다 됐나?\"를 마지막으로 확인하는 체크포인트

**언제 쓰나**

- 구현이나 리뷰 후 최종 결과물이 요구사항을 만족하는지 확인할 때

**필요한 입력값**

- `VERIFY_TARGETS`: 확인할 파일·아티팩트 목록
- `EXPECTED_CONTRACTS`: 만족해야 할 계약 항목들

**받는 결과**: 통과한 체크 목록, 차단 이슈, 최종 상태 (pass/blocked/inconclusive)

**경계 요약**

- `test-design-cases`: 무엇을 테스트해야 하는지 정한다
- `test-find-gaps`: 지금 무엇이 안 덮였는지 찾는다
- `test-write-guards`: 실제 테스트 코드를 추가하고 실행한다
- `test-run-user-scenarios`: 실제 사용자/에이전트처럼 돌려 본다
- `check-delivered`: 마지막에 계약대로 증명됐는지 확인한다

---

## `test-` — 테스트 설계와 검증

테스트를 무엇으로 설계하고, 어디가 비고, 실제 사용자처럼 어떻게 검증할지를 담당합니다.

- `test-design-cases`: 테스트 케이스 설계
- `test-find-gaps`: 현재 테스트 공백 분석
- `test-write-guards`: 의미 있는 회귀 가드 구현
- `test-run-user-scenarios`: 실제 사용자/에이전트 시나리오 시험

---

## `debug-` — 버그 분석

문제가 생겼을 때 원인을 찾고 범위를 좁힙니다.

---

### `debug-map-blast-radius` — 장애 범위 지도 그리기

**한마디로**: \"이 버그가 어디까지 영향을 주는지\" 지도를 그리는 첫 번째 단계

**언제 쓰나**

- 버그가 생겼는데 어디서부터 봐야 할지 모를 때
- 장애 범위를 좁힌 다음 디버그하고 싶을 때

**언제 쓰면 안 되나**: 이미 원인이 파악됐을 때 (→ `debug-find-root-cause`)

**필요한 입력값**

- `TARGET_SCOPE`: 범위
- `FAILURE_SYMPTOM`: 관찰된 증상 (예: \"로그인 후 세션이 사라짐\")
- `EXPECTED_BEHAVIOR`: 기대 동작

**받는 결과**: 재현 가능한 범위, 영향받는 경로 목록

---

### `debug-find-root-cause` — 근본 원인 분석

**한마디로**: 증거를 쌓아 \"왜 안 되는지\" 과학적으로 범인을 잡는 탐정

**언제 쓰나**

- 버그 원인을 구체적으로 확인해야 할 때
- 재현 단계와 수정 방향을 명확히 해야 할 때

**필요한 입력값**

- `FAILURE_SYMPTOM`: 증상
- `TARGET_SCOPE`: 범위
- `EXPECTED_BEHAVIOR`: 기대 동작

**받는 결과**: 재현 단계, 확인된 원인, 격리된 수정 경로

---

## `plan-` — 기획과 설계

실행에 옮기기 전에 밑그림을 그립니다.

---

### `plan-why-build-this` — 제품 기획서 (왜 만드나)

**한마디로**: \"이 기능을 왜 만드는지, 누가 쓰는지\"를 짧게 정리하는 첫 기획 문서

**언제 쓰나**

- 기능을 만들기 전에 배경과 목적을 정리할 때
- 스펙 작성 전에 사용자와 문제를 명확히 해야 할 때

**언제 쓰면 안 되나**: 상세 기능 요구사항, 기술 설계, IA 구조 설계

**필요한 입력값**

- `BRIEF_SCOPE`: feature | initiative | product | project
- `PROBLEM_STATEMENT`: 해결할 문제 설명
- `TARGET_AUDIENCE`: 사용자 목록
- `DESIRED_OUTCOMES`: 기대 결과
- `SUCCESS_SIGNALS`: 성공 측정 방법

**받는 결과**: 브리프 요약, 사용자 Job 목록, 비목표 목록

---

### `plan-what-it-does` — 기능 명세서 (무엇을 해야 하나)

**한마디로**: \"이 기능이 정확히 어떻게 동작해야 하는지\"를 팀이 합의할 수 있게 문서로 만드는 도구

**언제 쓰나**

- 구현 전에 기능 요구사항, 예외 처리, 인수 조건을 확정해야 할 때

**필요한 입력값**

- `FEATURE_SCOPE`: feature | screen | flow | api | module
- `USER_OUTCOME`: 사용자가 달성할 핵심 결과
- `REQUIRED_BEHAVIORS`: 구현해야 할 동작 목록
- `ACCEPTANCE_SCENARIOS`: 인수 시나리오

**받는 결과**: 스펙 요약, 기능 요구사항, 인수 기준, 엣지 케이스

---

### `plan-screen-map` — 화면 구조와 탐색 설계

**한마디로**: \"메뉴가 어떻게 연결되고 사용자가 어떻게 이동하는지\"를 설계하는 도구

**언제 쓰나**

- 앱·사이트의 화면 이동 흐름을 구조화해야 할 때

**필요한 입력값**

- `IA_SCOPE`: 설계 범위
- `PRIMARY_USERS`: 주 사용자와 목표
- `CONTENT_OBJECTS`: 주요 콘텐츠 항목들

**받는 결과**: 계층 구조 맵, 탐색 경로, 엔트리포인트 목록

---

### `plan-how-to-build` — 기술 설계 문서 (어떻게 만드나)

**한마디로**: 개발자가 실제로 코딩할 수 있게 경계·데이터 흐름·트레이드오프를 설계도로 만드는 도구

**언제 쓰나**

- 제품 기획과 스펙이 승인된 후 기술 구조를 확정해야 할 때

**필요한 입력값**

- `DESIGN_SCOPE`: feature | service | module | system
- `IMPLEMENTATION_GOAL`: 설계가 달성해야 할 핵심 기능
- `REQUIREMENT_SOURCES`: 참조할 브리프·스펙·계약 문서

**받는 결과**: 설계 요약, 경계 지도, 데이터/제어 흐름, 결정사항과 트레이드오프

---

### `plan-task-breakdown` — 실행 계획서 작성

**한마디로**: 코딩 전에 \"뭘, 어떤 순서로, 어떻게 확인하며 만들지\"를 계획서로 만드는 도구

**언제 쓰나**

- 실행에 앞서 태스크와 순서를 확정해야 할 때

**언제 쓰면 안 되나**: 직접 코드 작성, 리뷰, 스펙만 필요할 때

**필요한 입력값**

- `PLANNING_GOAL`: 전달해야 할 목표
- `TARGET_SCOPE`: 범위
- `DONE_CONDITION`: 완료 조건 목록
- `PLAN_OUTPUT_PATH`: 실행 계획서 저장 경로

**받는 결과**: 태스크 테이블 (TASK_ID, 완료기준, 의존관계), 의사결정 게이트

---

### `plan-verify-order` — 검증 순서 계획

**한마디로**: \"코드 고친 다음 뭘 먼저 확인해야 하는지\" 순서를 정하는 도구

**필요한 입력값**

- `TARGET_SCOPE`: 범위
- `CHANGE_GOAL`: 바꾸려는 것
- `RISK_AREAS`: 알고 있는 회귀 위험 영역 (선택)

**받는 결과**: 좁은 확인 단계 → 넓은 확인 단계, 중단 조건

---

### `test-design-cases` — 테스트 케이스 표

**한마디로**: 테스트를 쓰기 전에 \"어떤 상황에서 무엇을 확인해야 하는지\" 표로 정리하는 도구

**필요한 입력값**

- `TARGET_SCOPE`: 범위
- `TEST_GOAL`: regression | edge-case | failure-path | mixed
- `TARGET_BEHAVIORS`: 커버해야 할 동작 목록

**받는 결과**: 해피 패스 케이스, 엣지 케이스, 실패 케이스 표

---

### `plan-dependency-rules` — 의존성 규칙 정의

**한마디로**: \"A 모듈이 B 모듈을 불러도 되는지\"를 명확한 규칙으로 정하는 도구

**필요한 입력값**

- `TARGET_SCOPE`: 범위
- `CURRENT_BOUNDARY_NOTES`: 현재 경계에 대한 메모

**받는 결과**: 허용 의존성, 금지 의존성 목록

---

## `build-` — 구현과 실행

실제로 코드를 만들고 검증합니다.

---

### `build-write-code` — 코드 구현

**한마디로**: 계획에 맞춰 실제로 코드를 짜고 결과를 증거로 남기는 도구

**언제 쓰나**

- 코드 변경을 직접 실행해야 할 때

**언제 쓰면 안 되나**: 분석만 필요할 때, 리뷰·계획 단계

**필요한 입력값**

- `CHANGE_GOAL`: 구현 목표
- `TARGET_SCOPE`: 범위
- `VERIFICATION_MAP`: 검증 방법 명세

**받는 결과**: 변경된 파일 목록, 검증 실행 결과

---

### `test-write-guards` — 자동화 테스트 생성

**한마디로**: 버그가 다시 안 생기게 자동 테스트 코드를 만드는 도구

**언제 쓰나**

- 회귀 위험을 테스트로 방어하고 싶을 때
- TDD 방식으로 테스트 먼저 쓰고 싶을 때

**필요한 입력값**

- `TEST_GOAL`: regression | edge-case | failure-path | mixed
- `TARGET_SCOPE`: 범위
- `TARGET_BEHAVIORS`: 보호해야 할 동작 목록

**받는 결과**: 테스트 매트릭스, 추가된 테스트 파일, 실행 결과 증거

---

### `build-make-faster` — 성능 최적화

**한마디로**: 측정된 병목 구간을 실제로 개선하고 Before/After 증거를 남기는 도구

**언제 쓰나**

- 성능 기준값이 있고 실제로 개선 코드를 적용해야 할 때

**언제 쓰면 안 되나**: 기준값만 측정하고 싶을 때 (→ `scout-baseline`), 기능 구현

**필요한 입력값**

- `TARGET_SCOPE`: 최적화 대상
- `METRIC_NAME`: latency | throughput | memory | custom
- `PERFORMANCE_BUDGET`: 목표 임계값
- `BASELINE_EVIDENCE`: 기존 측정값

**받는 결과**: 기준 메트릭 스냅샷, 병목 근거, Before/After 비교 결과

---

### `build-until-done` — 코드 구현 완료까지 반복

**한마디로**: 정해진 완료 조건(테스트 통과 등)이 만족될 때까지 코드 변경 패스를 반복하는 도구

**언제 쓰나**

- \"다 될 때까지 계속 코드 수정해\"가 필요한 복잡한 구현 작업
- 코드 변경 + 테스트 실행 + 재시도를 루프로 돌려야 할 때
- 다음 패스의 핵심이 `build-write-code`, `test-write-guards`, `debug-find-root-cause` 같은 코드 경로일 때

**언제 쓰면 안 되나**: 문서 정리, 리뷰, 계획, 릴리즈 체크처럼 코드 변경이 없는 작업 (→ `finish-until-done` 사용)

**필요한 입력값**

- `MISSION_GOAL`: 달성해야 할 목표
- `DONE_CONDITION`: 완료 조건 목록 (관찰 가능한 형태)
- `COMPANION_SKILLS`: 코드 경로 스킬 목록

**받는 결과**: 미션 상태, 완료 조건별 체크 결과

---

### `finish-until-done` — 범용 반복 루프

**한마디로**: 코드 변경이 없는 일반 작업을 완료 조건이 만족될 때까지 계속 시도하는 도구

**언제 쓰나**

- 문서 작업, 리뷰, 계획, 릴리즈 체크 등 비코드 작업을 완료 조건까지 반복해야 할 때
- DONE 기준이 명확하게 정의된 멀티패스 작업

**언제 쓰면 안 되나**: 코드 구현+테스트 루프 (→ `build-until-done`), DONE 기준이 불명확한 작업

**필요한 입력값**

- `MISSION_GOAL`: 달성해야 할 목표
- `DONE_CONDITION`: 관찰·확인 가능한 완료 조건 목록
- `COMPANION_SKILLS`: 각 패스에서 실행할 비코드 스킬 목록
- `MAX_PASSES`: 최대 반복 횟수 (선택)

**받는 결과**: 미션 상태 (done/in-progress/blocked), 패스별 결과 로그, 완료 조건별 체크

---

## `tidy-` — 구조 개선

이미 만든 코드를 더 읽기 좋고 관리하기 쉽게 만듭니다.

---

### `tidy-find-copies` — 중복 코드 탐지

**한마디로**: 여기저기 복사된 똑같은 코드를 찾아 하나로 합칠 후보를 알려주는 도구

**필요한 입력값**

- `TARGET_SCOPE`: 범위
- `DUPLICATION_KIND`: logic | structure | mixed

**받는 결과**: 중복 클러스터 목록, 안전하게 합칠 수 있는 후보

---

### `tidy-find-magic-numbers` — 상수 추출 대상 탐지

**한마디로**: 코드 중간에 박힌 숫자·문자열 리터럴을 찾아 상수로 분리할 후보를 알려주는 도구

**필요한 입력값**

- `TARGET_SCOPE`: 범위
- `EXTRACTION_POLICY`: all | config-only | named-constants

**받는 결과**: 추출 가능한 상수 목록, 재사용 기회

---

### `tidy-why-complex` — 복잡도 분류

**한마디로**: 코드가 복잡한 이유가 \"꼭 필요한 복잡함\"인지 \"사고로 생긴 복잡함\"인지 분류하는 도구

**필요한 입력값**

- `TARGET_SCOPE`: 범위
- `SIMPLIFICATION_GOAL`: naming | structure | side-effects | mixed

**받는 결과**: 필수 복잡도 목록, 우발적 복잡도 목록

---

### `tidy-cut-fat` — 코드 단순화 청사진

**한마디로**: 복잡한 구조를 깎아내서 기능은 유지하면서 최대한 단순하게 만드는 청사진

**언제 쓰나**

- 불필요한 추상화·중첩·간접 참조로 코드가 이해하기 어려울 때

**언제 쓰면 안 되나**: 경계·의존성 방향만 정리할 때 (→ `tidy-reorganize`)

**필요한 입력값**

- `TARGET_SCOPE`: 범위
- `SIMPLIFICATION_GOAL`: naming | structure | side-effects | mixed
- `PRESERVE_BEHAVIOR`: yes | no-change-intent

**받는 결과**: 복잡도 목록, 단계별 단순화 계획, 동작 보존 가드

---

### `tidy-reorganize` — 경계 보존 리팩터링 계획

**한마디로**: 기능은 그대로 두고 모듈 경계·의존성 방향만 깔끔하게 바꾸는 계획서

**언제 쓰나**

- 의존성 방향을 정리하거나 모듈 경계를 재정비하고 싶을 때

**언제 쓰면 안 되나**: 기능 추가, 버그 수정, 광범위한 단순화 (→ `tidy-cut-fat`)

**필요한 입력값**

- `TARGET_SCOPE`: 범위
- `REFACTOR_BOUNDARY`: module-boundary | dependency-hygiene | structure-preserving-cleanup
- `BEHAVIOR_INVARIANTS`: 변경하면 안 되는 동작 목록

**받는 결과**: 목표 의존성 규칙, 원자적 리팩터 단계, 롤백 경로

---

## `doc-` — 문서화

나중에 봐도 이해할 수 있게 기록을 남깁니다.

---

### `doc-write` — 문서 작성 및 업데이트

**한마디로**: 사용자가 이해할 수 있는 가이드·레퍼런스·설명 문서를 쓰는 도구 (루트 README 제외)

**필요한 입력값**

- `DOC_GOAL`: concept-guide | reference | tutorial | changelog
- `TARGET_SCOPE`: 범위
- `AUDIENCE`: general | developer | operator

**받는 결과**: 문서 계획, 작성된 문서

---

### `doc-build-index` — 모듈·라이브러리 계층 인덱스 생성

**한마디로**: 폴더·모듈·라이브러리가 많은 곳에 계층별 설명 문서와 인덱스 파일을 만드는 도구

**필요한 입력값**

- `DOCSET_KIND`: module-tree | library | paper | mixed
- `TARGET_SCOPE`: 범위
- `INDEX_DEPTH`: artifact-only | folder-tree | multi-level

**받는 결과**: 분석 문서 목록, 로컬 인덱스 파일, 가이드 인덱스 파일

---

### `doc-publish-readme` — 루트 README + 다국어 entry docs 발행

**한마디로**: 프로젝트의 첫 출입문(루트 README)을 만들고 한국어·스페인어 등으로 번역 문서를 만드는 도구

**필요한 입력값**

- `PROJECT_SCOPE`: repo
- `README_GOAL`: github-overview | onboarding | usage-entry | mixed
- `SOURCE_DOCS`: 루트 README가 요약·링크할 근거 문서들

**받는 결과**: 루트 README 경로, 언어별 문서 목록, 포털 맵

---

### `doc-curate` — 문서 정리 및 큐레이션

**한마디로**: 문서 중 낡은 것·중복된 것을 찾아 구조를 정비하고 네비게이션을 개선하는 도구

**필요한 입력값**

- `CURATION_GOAL`: navigation | cleanup | restructure
- `TARGET_SCOPE`: 범위

**받는 결과**: 문서 목록, 네비게이션 맵

---

### `doc-find-all` — 문서 현황 목록화

**한마디로**: 지금 어떤 문서들이 있고 그 상태(최신/낡음/고아/중복)가 어떤지 리스트를 뽑는 도구

**언제 쓰나**

- 문서 전체를 한 번 파악해야 할 때
- `doc-curate` 전에 현황 파악을 먼저 하고 싶을 때

**필요한 입력값**

- `TARGET_SCOPE`: 범위
- `INVENTORY_GOAL`: overview | stale-only | orphan-check

**받는 결과**: 문서 상태 목록, 고아·중복 문서 세트

---

## `ship-` — 릴리즈 준비

사용자에게 결과물을 내보냅니다.

---

### `ship-check-repo` — Git 저장소 사전 상태 확인

**한마디로**: 배포 작업을 시작하기 전에 Git 상태가 깨끗한지, 브랜치·태그·원격이 준비됐는지 확인하는 도구

**필요한 입력값**

- `TARGET_BRANCHES`: 릴리즈에 관련된 브랜치 목록
- `REMOTE_NAME`: 원격 이름

**받는 결과**: 저장소 사실 목록, 브랜치 맵, 차단 요소, 전체 준비 상태

---

### `ship-check-hygiene` — 릴리즈 위생 점검

**한마디로**: 낡은 파일·레거시 이름·문서 불일치가 릴리즈에 포함되지 않았는지 확인하는 도구

**필요한 입력값**

- `HYGIENE_SCOPE`: diff | repo
- `REQUIRED_DOCS`: 릴리즈 필수 문서 목록 (선택)
- `LEGACY_PATTERNS`: 제거해야 할 레거시 패턴 (선택)

**받는 결과**: 위생 발견 목록, 문서 게이트 상태, 필수 정리 작업 목록

---

### `ship-go-nogo` — 릴리즈 최종 판정 (GO/NO-GO)

**한마디로**: \"지금 배포해도 안전한가?\"에 대해 롤아웃·롤백·영향 범위를 근거로 최종 판정을 내리는 도구

**필요한 입력값**

- `RELEASE_SCOPE`: diff | repo | deployment-slice
- `ROLLOUT_PLAN`: 배포 계획
- `ROLLBACK_PATH`: 롤백 전략

**받는 결과**: 영향 범위(Blast Radius), 롤백 체크리스트, GO/NO-GO/차단 판정

---

### `ship-commit` — Conventional Commit 메시지 생성

**한마디로**: 작업 diff와 의도를 입력하면 규격에 맞는 커밋 메시지를 만들어주는 도구

**필요한 입력값**

- `DIFF_SUMMARY`: 변경 내용 요약
- `CHANGE_INTENT`: 변경 의도

**받는 결과**: 최우선 커밋 메시지 후보, 대안 메시지들

---

## 유틸리티 스킬 (시스템 내부용)

직접 호출하기보다 `compose`가 자동으로 사용하는 내부 스킬들입니다.

---

### `compose` — 스킬 조합 지휘자

**한마디로**: \"$skill1 + $skill2 + @경로\" 같은 매크로를 파싱하여 결정론적 실행 계획으로 만드는 오케스트레이터

---

### `plan-driven-delivery` — 계획서와 실행 동기화

**한마디로**: 이미 있는 계획서(IMPLEMENTATION-PLAN.md, TASKS.md)와 실제 구현 결과를 맞춰주는 도구

**필요한 입력값**

- `IMPLEMENTATION_PLAN_PATH`, `TASKS_PATH`: 계획서 경로들
- `SELECTED_TASK_IDS`: 이번에 다룰 태스크 ID

---

### `respond` — 최종 응답 렌더링

**한마디로**: 스킬들이 만든 결과를 사용자가 읽기 쉬운 한 개의 응답으로 정리하는 도구

---

### `gemini` — 외부 Gemini CLI 위임

**한마디로**: 사용자가 명시적으로 요청했을 때만 Gemini CLI를 쓰는 외부 분석 보조 도구

---

> **팁**: 어떤 스킬을 써야 할지 모르겠다면 `wf-*` 워크플로우로 시작하고, 특정 단계만 필요하면 아토믹 스킬로 정밀하게 사용하세요. 조합 예시는 [SKILL-COMBOS.md](./SKILL-COMBOS.md)를 보세요.
