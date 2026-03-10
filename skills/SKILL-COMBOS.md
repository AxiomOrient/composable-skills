# Skill Combos — 조합 가이드

> 이 문서는 **스킬 조합**만 설명합니다.
> 각 스킬 하나하나의 기능은 [`ATOMIC-SKILLS.md`](./ATOMIC-SKILLS.md)에서 확인하세요.

---

## 워크플로우 스킬 한눈에 보기

워크플로우 스킬은 여러 아토믹 스킬을 미리 묶어놓은 "완성형 흐름"입니다. 매번 스킬을 수동으로 나열하지 않아도 됩니다.

| 워크플로우 스킬               | 내부 조합                                                                                                                      | 언제 쓰나                                              |
| :---------------------------- | :----------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------- |
| `wf-ask-get-clear`             | ask-find-question → ask-break-it-down                                                                                           | 막연한 주제를 문제 정의와 질문 스택으로 바꾸고 싶을 때 |
| `wf-ask-sharpen`           | ask-find-question → ask-break-it-down → ask-flip-assumption                                                                        | 질문을 바로 던질 수준까지 날카롭게 만들고 싶을 때      |
| `wf-check-full-review`           | scout-facts → tidy-find-magic-numbers → tidy-find-copies → check-module-walls → check-failure-paths → test-find-gaps → check-merge-ready | 프로젝트·모듈을 종합적으로 리뷰하고 싶을 때            |
| `wf-check-with-checklist` | wf-check-full-review + check-quality-scan                                                                                          | 리뷰와 9종 체크리스트를 함께 보고 싶을 때              |
| `wf-debug-this`            | debug-map-blast-radius → debug-find-root-cause → test-find-gaps                                                                 | 버그 범위를 좁히고 원인을 찾고 싶을 때                 |
| `wf-tidy-find-improvements`  | tidy-find-copies → tidy-find-magic-numbers → tidy-cut-fat → tidy-reorganize                                                   | 중복·상수화·단순화 기회를 먼저 파악하고 싶을 때        |
| `wf-ship-ready-check`           | ship-check-repo → ship-check-hygiene → ship-go-nogo                                                                 | 출시 가능 여부를 투명하게 검토하고 싶을 때             |
| `wf-ship-it`             | ship-check-repo → ship-check-hygiene → ship-go-nogo → release-publish                                               | 검토부터 태그·발행까지 한 번에 하고 싶을 때            |

---

## 유틸리티 스킬 역할 요약

| 유틸리티 스킬          | 역할                                               |
| :--------------------- | :------------------------------------------------- |
| `compose`              | 스킬 매크로를 파싱해 실행 순서를 고정하는 지휘자   |
| `plan-driven-delivery` | 이미 있는 계획서와 실제 구현을 동기화              |
| `release-publish`      | 검증된 변경을 release-only 커밋·태그·릴리즈로 발행 |
| `respond`              | 마지막 결과를 사용자가 읽기 쉽게 렌더링            |
| `gemini`               | 사용자가 요청했을 때만 외부 대형 분석을 위임       |

---

## 조합 예시 읽는 법

```text
$compose + $wf-debug-this + @src/session

TARGET_SCOPE: src/session
FAILURE_SYMPTOM: 로그인 후 새로고침하면 세션이 사라진다
EXPECTED_BEHAVIOR: 새로고침해도 로그인 유지
```

- **첫 줄**: 실행할 스킬 조합
- **`@경로`**: 분석 대상 폴더/파일 지정
- **하단 블록**: 입력값 (자신의 상황에 맞게 바꾸세요)
- `$check-delivered`를 마지막에 붙이면 결과가 요구사항을 지켰는지 마지막으로 체크합니다

---

## 어떤 조합을 고를까?

| 내 상황                            | 추천 섹션                                  |
| :--------------------------------- | :----------------------------------------- |
| 좋은 질문부터 만들고 싶다          | [A. 질문 설계](#a-질문-설계)               |
| 코드·폴더를 리뷰하고 싶다          | [B. 프로젝트 리뷰](#b-프로젝트-리뷰)       |
| 버그 원인을 찾고 싶다              | [C. 버그 디버그](#c-버그-디버그)           |
| 개선 포인트를 먼저 파악하고 싶다   | [D. 코드 개선](#d-코드-개선)               |
| 계획을 만들고 실행까지 잇고 싶다   | [E. 계획과 실행](#e-계획과-실행)           |
| 기획·스펙·IA·기술 설계를 쓰고 싶다 | [F. 스펙과 설계 문서](#f-스펙과-설계-문서) |
| README나 문서를 정리하고 싶다      | [G. 문서 작업](#g-문서-작업)               |
| 릴리즈 준비와 배포를 끝내고 싶다   | [H. 릴리즈](#h-릴리즈)                     |

---

## A. 질문 설계

### A-1. 막연한 주제 → 문제 정의 + 질문 스택

**언제**: 무엇을 물어야 할지 모르겠다 / 생각은 있는데 질문이 흐리다

```text
$compose + $wf-ask-get-clear

TOPIC: AI 코드 리뷰 도구를 팀에 도입하면 실제로 생산성이 좋아질까?
AUDIENCE: 스타트업 엔지니어링 리더, 팀 규모 5~20명
CONSTRAINTS: 3개월 이내 도입 가능한 현실적 옵션만, 비용 정보도 포함
```

**받는 결과**: 한 문장 문제 정의 + 우선 물어야 할 핵심 질문 + 3~5개 질문 스택

---

### A-2. 질문을 바로 던질 수준까지 날카롭게

**언제**: 질문 초안은 있는데 좀 더 날카롭게 만들고 싶다 / 기본 시야를 한 번 더 뒤집어보고 싶다

```text
$compose + $wf-ask-sharpen

TOPIC: AI 코드 리뷰 도구를 팀에 도입하면 실제로 생산성이 좋아질까?
AUDIENCE: 스타트업 엔지니어링 리더, 팀 규모 5~20명
CONSTRAINTS: 실제 사례 기반, 비용과 운영 부담 포함
```

**받는 결과**: 문제 정의 + 핵심 질문 + 가정을 뒤집는 도전 질문 2개

---

### A-3. 받은 답이 별로여서 질문을 최소한으로 고치기

**언제**: AI가 제대로 답변하지 못했을 때 질문의 어디가 문제인지 찾고 싶다

```text
$compose + $ask-fix-prompt

TOPIC: AI 코드 리뷰 도구 생산성 효과
QUESTION_OR_STACK: |
  핵심 질문: AI 코드 리뷰 도구를 도입하면 생산성이 오르는가?
BAD_ANSWER: |
  "AI 코드 리뷰 도구는 버그를 줄이고 리뷰 속도를 높일 수 있습니다.
  하지만 팀마다 다르고 도구 선택도 중요합니다."
```

**받는 결과**: 실패 유형 분류 + 왜 답이 약했는지 + 최소 질문 수정 방향

---

## B. 프로젝트 리뷰

### B-1. 특정 폴더의 구조와 위험을 종합 리뷰

**언제**: PR 전이나 구현 후에 코드 품질을 종합적으로 확인하고 싶다

```text
$compose + $wf-check-full-review + @src/auth

TARGET_SCOPE: src/auth
REVIEW_FOCUS: maintainability
```

**받는 결과**: 구조적 문제 + 테스트 공백 + integrate/hold 판정 + 근거 차트

---

### B-2. 리뷰 + 9종 체크리스트를 한 번에

**언제**: 리뷰뿐 아니라 "설계는 우아한가, 불필요 코드는 없는가"까지 다 확인하고 싶다

```text
$compose + $wf-check-with-checklist + @src/auth + $check-delivered

TARGET_SCOPE: src/auth
REVIEW_FOCUS: mixed
```

**받는 결과**: 리뷰 발견 목록 + 9종 체크리스트 표 + integrate/hold 판정

---

### B-3. 현재 변경사항을 배포 전 관점으로 점검

**언제**: "지금 diff를 배포해도 안전한가?"를 확인하고 싶다

```text
$compose + $wf-check-full-review + scope:diff + $check-ship-risk + $ship-go-nogo + $check-delivered

TARGET_SCOPE: diff
REVIEW_FOCUS: risk
ROLLOUT_PLAN: 스테이징 1시간 모니터링 후 프로덕션
ROLLBACK_PATH: git revert 후 5분 내 복구
```

---

### B-4. 보안만 집중적으로 점검

**언제**: 인증·권한·입력 검증 코드를 집중적으로 보안 관점에서 보고 싶다

```text
$compose + $check-security-holes

SECURITY_GOAL: audit
TARGET_SCOPE: src/auth
ASSETS_OR_BOUNDARIES:
  - ASSET_OR_BOUNDARY: JWT 토큰 발급 엔드포인트
    WHY_RELEVANT: 인증 핵심 경로
  - ASSET_OR_BOUNDARY: 사용자 세션 관리
    WHY_RELEVANT: 세션 탈취 가능성
```

---

## C. 버그 디버그

### C-1. 어디서부터 봐야 할지 모를 때

**언제**: 버그가 났는데 범위를 모를 때. 지도 먼저 그리고 원인을 파악

```text
$compose + $wf-debug-this + @src/session

TARGET_SCOPE: src/session
FAILURE_SYMPTOM: 로그인 성공 후 새로고침하면 다시 로그인 화면으로 이동한다
EXPECTED_BEHAVIOR: 새로고침해도 로그인 상태가 유지되어야 한다
```

**받는 결과**: 장애 범위 지도 + 근본 원인 분석 + 테스트 공백 보고

---

### C-2. 디버그 후 수정과 테스트까지 바로 잇기

**언제**: 원인을 찾은 후 바로 수정하고 테스트까지 추가하고 싶다

```text
$compose + $wf-debug-this + @src/payment + $build-write-code + $test-write-guards + $check-delivered

TARGET_SCOPE: src/payment
FAILURE_SYMPTOM: /api/payment/confirm 에서 간헐적 500 에러
EXPECTED_BEHAVIOR: 결제 확인 API는 200 또는 400만 반환해야 한다
CHANGE_GOAL: undefined 접근 에러 수정
VERIFICATION_MAP: |
  - 결제 확인 API 통합 테스트 통과
  - 동일 케이스 재발 없음
```

---

### C-3. 에러 처리만 집중해서 리뷰

**언제**: 예외 상황·에러 경로만 집중해서 보고 싶다

```text
$compose + $check-failure-paths

TARGET_SCOPE: src/auth
FAILURE_MODES:
  - 토큰 만료
  - 네트워크 오류 중 세션 갱신
```

**받는 결과**: 에러 경로 발견 목록 + 빠진 가드 목록

---

## D. 코드 개선

### D-1. 개선 후보 먼저 파악하기

**언제**: "뭘 고치면 좋을지"부터 파악하고, 직접 손대기 전에 지도를 먼저 그리고 싶다

```text
$compose + $wf-tidy-find-improvements + @src/api

TARGET_SCOPE: src/api
IMPROVEMENT_GOAL: mixed
```

**받는 결과**: 중복 후보 + 상수화 후보 + 단순화 방향 + 다음 개선 단계 추천

---

### D-2. 개선 후보 파악 후 바로 구현까지

**언제**: 개선 지점이 명확하면 분석 후 곧바로 수정하고 싶다

```text
$compose + $wf-tidy-find-improvements + @src/api + $build-write-code + $check-delivered

TARGET_SCOPE: src/api
IMPROVEMENT_GOAL: commonize
CHANGE_GOAL: 공통 에러 처리 핸들러 통일
VERIFICATION_MAP: |
  - API 통합 테스트 모두 통과
  - 에러 응답 포맷 변경 없음
```

---

### D-3. 복잡도 먼저 파악 후 단순화

**언제**: "이 코드가 왜 이렇게 복잡하지?"를 먼저 이해하고 단순화 계획을 세우고 싶다

```text
$compose + $tidy-why-complex + $tidy-cut-fat + @src/auth

TARGET_SCOPE: src/auth
SIMPLIFICATION_GOAL: structure
PRESERVE_BEHAVIOR: yes
```

---

### D-4. 모듈 의존성 방향을 리팩터링 계획으로

**언제**: 의존성이 꼬여 있어서 방향 규칙을 정하고 단계적으로 정리하고 싶다

```text
$compose + $plan-dependency-rules + $tidy-reorganize + @src

TARGET_SCOPE: src
REFACTOR_BOUNDARY: dependency-hygiene
BEHAVIOR_INVARIANTS:
  - 공개 API 응답 포맷 유지
  - 기존 DB 스키마 변경 없음
```

---

## E. 계획과 실행

### E-1. 아직 계획이 없을 때 — 계획서부터 만들기

**언제**: 큰 기능을 만들기 전에 단계·검증 방법을 확정하고 싶다

```text
$compose + $plan-task-breakdown

PLANNING_GOAL: JWT 기반 인증 시스템 구현. 로그인·토큰 갱신·로그아웃 포함
TARGET_SCOPE: src/auth
DONE_CONDITION:
  - 로그인 API 동작
  - 토큰 갱신 API 동작
  - 로그아웃 API 동작
  - 통합 테스트 통과
PLAN_OUTPUT_PATH: docs/IMPLEMENTATION-PLAN.md
TASKS_OUTPUT_PATH: docs/TASKS.md
ARTIFACT_MODE: create
CONSTRAINTS: 외부 인증 서비스 미사용, PostgreSQL 사용
```

**받는 결과**: 태스크 테이블 (TASK_ID·완료기준·의존관계) + 의사결정 게이트

---

### E-2. 계획이 이미 있을 때 — 실행과 계획서 동기화

**언제**: TASKS.md가 있고, 특정 태스크를 구현한 후 계획서에 반영하고 싶다

```text
$compose + $plan-driven-delivery + $build-write-code + $check-delivered

IMPLEMENTATION_PLAN_PATH: docs/IMPLEMENTATION-PLAN.md
TASKS_PATH: docs/TASKS.md
SELECTED_TASK_IDS: TASK-003, TASK-004
CHANGE_GOAL: refresh token 갱신 엔드포인트 구현 및 무효 토큰 처리
VERIFICATION_MAP: |
  - POST /auth/refresh 테스트 통과
  - 만료 토큰 거절 테스트 통과
```

---

### E-3. 완료 조건이 만족될 때까지 반복 실행

**언제**: 한 번에 다 안 될 것 같고, 완료 조건이 명확하게 정의된 복잡한 수정 작업

```text
$compose + $build-until-done + $build-write-code + $check-delivered

MISSION_GOAL: refresh 후에도 로그인 상태가 유지되게 만들기
TARGET_SCOPE: src/auth
DONE_CONDITION:
  - refresh 후에도 세션 유지
  - 관련 테스트 통과
COMPANION_SKILLS: build-write-code, check-delivered
MAX_PASSES: 3
```

> **팁**: `DONE_CONDITION`은 핵심 사용자 결과만 넣으세요. 비본질적 정리를 넣으면 완료 기준이 흐려집니다.

---

### E-4. 검증 방법을 먼저 설계하고 구현

**언제**: 코드를 짜기 전에 "어떻게 검증할지"를 먼저 확정하고 싶다 (TDD 스타일)

```text
$compose + $plan-verify-order + $test-design-cases + $build-write-code + $test-write-guards

TARGET_SCOPE: src/auth/session
CHANGE_GOAL: 세션 만료 시 자동 갱신 로직 추가
RISK_AREAS:
  - 기존 세션 유지 동작 회귀
  - 동시 갱신 요청 중복 처리
TEST_GOAL: regression
TARGET_BEHAVIORS:
  - 세션 만료 전 자동 갱신
  - 갱신 실패 시 로그아웃
```

---

## F. 스펙과 설계 문서

4가지 문서를 모두 만들 필요는 없습니다.

| 흐린 점                       | 먼저 만들 문서             |
| :---------------------------- | :------------------------- |
| "왜 만드나"가 불명확          | `plan-why-build-this`            |
| "무엇을 해야 하나"가 불명확   | `plan-what-it-does`                     |
| "구조가 어떻게 되나"가 불명확 | `plan-screen-map` |
| "어떻게 만드나"가 불명확      | `plan-how-to-build`     |

### F-1. 문제와 사용자 정의 (가장 먼저)

```text
$compose + $plan-why-build-this

BRIEF_SCOPE: feature
PROBLEM_STATEMENT: 신규 사용자가 첫 로그인 후 설정 화면에서 길을 잃는다
TARGET_AUDIENCE:
  - USER: 신규 관리자
    CONTEXT: 첫 팀 설정 직후
DESIRED_OUTCOMES:
  - OUTCOME: 첫 설정 완료 시간을 줄인다
    WHY_IT_MATTERS: 초기 이탈을 줄여야 한다
SUCCESS_SIGNALS:
  - SIGNAL: 첫 설정 완료율 증가
    HOW_MEASURED: 7일 cohort 완료율
```

---

### F-2. 기능 명세를 구현 가능하게 고정

```text
$compose + $plan-what-it-does + $check-delivered

FEATURE_SCOPE: flow
USER_OUTCOME: 사용자가 이메일 링크로 비밀번호를 재설정할 수 있어야 한다
REQUIRED_BEHAVIORS:
  - ID: FR-1
    BEHAVIOR: 유효한 토큰이면 새 비밀번호 입력 화면을 보여준다
    WHY: 재설정 흐름 진입점
  - ID: FR-2
    BEHAVIOR: 만료된 토큰이면 재요청 경로를 안내한다
    WHY: 실패 경로 처리
ACCEPTANCE_SCENARIOS:
  - SCENARIO: 만료되지 않은 토큰으로 접근
    EXPECTED_RESULT: 비밀번호 입력 폼 표시
  - SCENARIO: 만료된 토큰으로 접근
    EXPECTED_RESULT: 재요청 안내 표시
```

---

### F-3. 화면 구조와 탐색 흐름 잡기

```text
$compose + $plan-screen-map

IA_SCOPE: feature
PRIMARY_USERS:
  - USER: 신규 관리자
    GOAL: 워크스페이스 기본 설정 완료
CONTENT_OBJECTS:
  - ITEM: Workspace Overview
    PURPOSE: 현재 상태와 다음 행동 표시
  - ITEM: Team Invite
    PURPOSE: 팀원 초대 진행
ENTRY_POINTS:
  - ENTRY: 첫 로그인 직후
    USER_NEED: 어디서 시작할지 바로 알고 싶다
```

---

### F-4. 전체 문서 체인 (브리프 → 스펙 → 기술 설계)

```text
$compose + $plan-why-build-this + $plan-what-it-does + $plan-how-to-build + $check-delivered

BRIEF_SCOPE: feature
PROBLEM_STATEMENT: 비밀번호 재설정 흐름이 느슨해서 실패 경로가 불명확하다
TARGET_AUDIENCE:
  - USER: 기존 사용자
    CONTEXT: 로그인 불가 상태
DESIRED_OUTCOMES:
  - OUTCOME: 재설정 성공률을 높인다
    WHY_IT_MATTERS: 로그인 실패 이탈 감소
SUCCESS_SIGNALS:
  - SIGNAL: 비밀번호 재설정 완료율 증가
    HOW_MEASURED: reset funnel
FEATURE_SCOPE: flow
USER_OUTCOME: 사용자가 이메일 링크로 비밀번호를 안전하게 재설정할 수 있어야 한다
REQUIRED_BEHAVIORS:
  - ID: FR-1
    BEHAVIOR: 유효한 토큰이면 새 비밀번호 저장 허용
    WHY: 핵심 성공 경로
ACCEPTANCE_SCENARIOS:
  - SCENARIO: 유효한 토큰 제출
    EXPECTED_RESULT: 새 비밀번호 저장, 토큰 무효화
DESIGN_SCOPE: feature
IMPLEMENTATION_GOAL: 토큰 검증과 새 비밀번호 저장을 안전하게 처리
REQUIREMENT_SOURCES:
  - REF: docs/specs/password-reset.md
    WHY_RELEVANT: 요구사항 기준
```

---

## G. 문서 작업

### G-1. 일반 가이드·레퍼런스 문서 쓰기 (루트 README 제외)

```text
$compose + $doc-write + @docs

DOC_GOAL: concept-guide
DOC_FORM: guide
TARGET_SCOPE: docs
AUDIENCE: general
AUDIENCE_LEVEL: general
EVIDENCE_LINKS:
  - TYPE: file
    REF: docs/architecture/auth.md
    WHY_RELEVANT: 인증 구조 설명의 핵심 근거
  - TYPE: file
    REF: src/auth/session.ts
    WHY_RELEVANT: 인증 흐름 설명 근거
```

---

### G-2. 모듈·라이브러리 계층별 인덱스 문서 생성

```text
$compose + $doc-build-index + @src/auth

DOCSET_KIND: module-tree
DOC_FORM: guide
TARGET_SCOPE: src/auth
INDEX_DEPTH: multi-level
INDEX_LAYOUT: docs-mirror
AUDIENCE: general
AUDIENCE_LEVEL: general
EVIDENCE_LINKS:
  - TYPE: code
    REF: src/auth
    WHY_RELEVANT: 인증 모듈 구조와 책임 설명 근거
```

---

### G-3. 루트 README + 다국어 entry docs 발행

```text
$compose + $doc-publish-readme + $check-delivered

PROJECT_SCOPE: repo
README_GOAL: github-overview
AUDIENCE: general
AUDIENCE_LEVEL: general
PRIMARY_LANGUAGE: en
TARGET_LANGUAGES: ko, es, zh
SOURCE_DOCS:
  - PATH: docs/GUIDE.md
    ROLE: project-guide
  - PATH: docs/reference/README.md
    ROLE: deeper-index
EXPECTED_CONTRACTS:
  - CONTRACT: 루트 README는 깃허브 첫 화면에서 프로젝트 개요와 시작 경로를 보여준다
    SOURCE: root README contract
  - CONTRACT: 다국어 entry docs는 docs/i18n/<lang>/ 아래 있다
    SOURCE: localization contract
```

---

### G-4. 문서 전체 정리 (목록화 → 큐레이션)

```text
$compose + $doc-find-all + $doc-curate + @docs

INVENTORY_GOAL: overview
CURATION_GOAL: navigation
TARGET_SCOPE: docs
```

---

## H. 릴리즈

### H-1. git·문서·롤백까지 포함해 출시 가능 여부 검토

**언제**: "지금 출시해도 되나?" 를 저장소·문서·안전성 순서로 투명하게 확인하고 싶다

```text
$compose + $wf-ship-ready-check + $check-delivered

TARGET_BRANCHES:
  - {BRANCH: codex/dev, ROLE: source}
  - {BRANCH: main, ROLE: target}
HYGIENE_SCOPE: repo
RELEASE_SCOPE: repo
ROLLOUT_PLAN: 스테이징 1시간 확인 후 프로덕션
ROLLBACK_PATH: git revert 후 재배포
REQUIRED_DOCS:
  - {PATH: skills/README.md, WHY_REQUIRED: 사용자 안내 문서}
  - {PATH: skills/SKILL-COMBOS.md, WHY_REQUIRED: 조합 안내 문서}
LEGACY_PATTERNS:
  - {PATTERN: skills/release/, WHY_BLOCKING: 제거된 예전 release surface}
SURFACE_CONTRACTS:
  - {CONTRACT: registry와 사용자 문서의 release surface가 일치해야 한다, SOURCE: public surface contract}
KNOWN_GATES:
  - {GATE: validate, STATUS: pass, EVIDENCE: ./scripts/validate.sh}
  - {GATE: docs-updated, STATUS: pass, EVIDENCE: skills 문서 최신화}
```

**받는 결과**: 저장소 준비 상태 + 위생 게이트 결과 + GO/NO-GO 판정

---

### H-2. 검토 통과 후 실제 릴리즈 커밋·태그·GitHub 발행까지

**언제**: wf-ship-ready-check를 통과했고, 실제로 버전 태그를 달아 GitHub Release를 올리고 싶다

```text
$compose + $wf-ship-it + $check-delivered

TARGET_BRANCHES:
  - {BRANCH: codex/dev, ROLE: source}
  - {BRANCH: main, ROLE: target}
ROLLOUT_PLAN: 스테이징 확인 후 프로덕션
ROLLBACK_PATH: git revert 후 재배포
RELEASE_BUMP: explicit-tag
RELEASE_TAG: v1.0.0
REQUIRED_DOCS:
  - {PATH: skills/README.md, WHY_REQUIRED: 사용자 안내 문서}
REQUIRED_CHECKS:
  - {NAME: validate, COMMAND: ./scripts/validate.sh, REQUIRED: true}
  - {NAME: diff-check, COMMAND: git diff --check, REQUIRED: true}
PUBLISH_TARGET: github
RELEASE_NOTES_SOURCE: generate
LEGACY_CLEANUP_SCOPE:
  - {AREA: public-surface, RULE: 레거시 이름과 불필요 문서 제거}
```

**받는 결과**: cleanup 보고 + source/main 커밋 ref + 태그·GitHub Release 결과

---

## 자주 붙이는 확장 패턴

### 마지막에 최종 검증 추가

```text
$compose + $wf-check-full-review + @src/auth + $check-delivered
```

중요한 작업 뒤에 `$check-delivered`를 붙이면 결과가 계약을 지켰는지 마지막으로 체크합니다.

### 현재 diff만 대상으로 보기

```text
$compose + $wf-check-full-review + scope:diff
```

폴더 전체가 아니라 지금 바뀐 파일만 봅니다.

### 외부 대형 컨텍스트 분석 붙이기

```text
$compose + $gemini + $wf-check-full-review + @src/auth

GEMINI_MODE: new
GEMINI_GOAL: auth 모듈의 보안 패턴을 공식 가이드와 비교 분석
TARGET_SCOPE: src/auth
```

---

## 다음에 어디로 가면 되나

- **아토믹 스킬 설명**: [`ATOMIC-SKILLS.md`](./ATOMIC-SKILLS.md)
- **전체 안내**: [`README.md`](./README.md)
- **시스템 규칙**: [`../docs/SKILL-SYSTEM.md`](../docs/SKILL-SYSTEM.md)
- **스킬 상태 보고서**: [`../docs/SKILL-STATE-REPORT.md`](../docs/SKILL-STATE-REPORT.md)
