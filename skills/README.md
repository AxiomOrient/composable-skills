# Composable Skill Packs

이 폴더는 큰 작업을 작은 스킬로 나눠 정확하게 처리하기 위한 공개 스킬 모음이다.

핵심 원칙은 세 가지다.

- 한 스킬은 한 가지 문제에 집중한다.
- 입력과 출력이 먼저 정해져 있어야 한다.
- 여러 스킬을 묶을 때는 `compose`로 명시적으로 합성한다.

공개 스킬의 실제 기준은 [`_registry/index.json`](./_registry/index.json)이다.
운영 원칙과 아키텍처 설명은 [`../docs/SKILL-SYSTEM.md`](../docs/SKILL-SYSTEM.md)에 있다.

## 빠른 시작

처음이면 이 순서로 보면 된다.

1. 바로 쓸 조합이 필요하면 [`SKILL-COMBOS.md`](./SKILL-COMBOS.md)에서 찾는다.
2. 작은 스킬 하나의 뜻이 궁금하면 [`ATOMIC-SKILLS.md`](./ATOMIC-SKILLS.md)에서 찾는다.
3. 카테고리나 도메인 pack부터 고르고 싶으면 [`packs/README.md`](./packs/README.md)에서 찾는다.
4. 예시는 그대로 복사하고 입력값만 내 상황에 맞게 바꾼다.
5. 범위가 너무 넓으면 먼저 더 작은 폴더나 파일로 줄인다.

가장 자주 쓰는 시작점은 아래 일곱 개다.

| 하고 싶은 일 | 먼저 쓰면 되는 스킬 |
|---|---|
| 구조와 위험을 보고 싶다 | `wf-check-full-review` |
| 버그 원인을 좁히고 싶다 | `wf-debug-this` |
| 중복과 단순화 후보를 찾고 싶다 | `wf-tidy-find-improvements` |
| 질문을 더 좋게 만들고 싶다 | `wf-ask-sharpen` |
| 출시 가능 여부를 투명하게 보고 싶다 | `wf-ship-ready-check` |
| 검토부터 실제 릴리즈까지 한 번에 가고 싶다 | `wf-ship-it` |
| 기획서, 기능 스펙, IA, 기술 설계 문서를 만들고 싶다 | [`packs/spec-pack.md`](./packs/spec-pack.md) |

모든 pack 목록은 [`packs/README.md`](./packs/README.md)에 모아 두었다. 질문/답변 준비용 추천 묶음은 [`packs/question-answer-pack.md`](./packs/question-answer-pack.md)에, 스펙/기획/IA/기술 설계용 추천 묶음은 [`packs/spec-pack.md`](./packs/spec-pack.md)에, 문서 체계용 추천 묶음은 [`packs/documentation-pack.md`](./packs/documentation-pack.md)에, 리뷰/디버그/개선 흐름 묶음은 [`packs/project-quality-pack.md`](./packs/project-quality-pack.md)에, 계획-구현-검증 흐름 묶음은 [`packs/delivery-pack.md`](./packs/delivery-pack.md)에, 릴리즈용 추천 묶음은 [`packs/release-pack.md`](./packs/release-pack.md)에 따로 정리돼 있다.

## 스킬은 세 층으로 나뉜다

### `wf-*` workflow

사용자가 바로 쓰기 쉬운 완성형 흐름이다.
여러 atomic skill을 이미 묶어 둔 entrypoint라고 생각하면 된다.

예:

- `wf-check-full-review`
- `wf-debug-this`
- `wf-tidy-find-improvements`
- `wf-ask-sharpen`
- `wf-ship-ready-check`
- `wf-ship-it`

### atomic

한 가지 일만 하는 작은 스킬이다.
결과가 좁고 해석이 쉽다.

전체 atomic 설명은 [`ATOMIC-SKILLS.md`](./ATOMIC-SKILLS.md)에 모아 두었다.

예:

- `tidy-find-copies`
- `tidy-find-magic-numbers`
- `check-failure-paths`
- `scout-boundaries`

### utility

직접 분석이나 구현을 하지 않고, 흐름을 연결하거나 동기화하거나 최종 응답을 정리한다.

현재 공개 utility는 아래 다섯 개다.

- `compose`
- `plan-driven-delivery`
- `release-publish`
- `respond`
- `gemini`

참고:

- `skills/.system/*`는 내부 시스템 스킬이다.
- 이 README는 공개 운영 surface만 다룬다.

## 무엇부터 써야 하나

### 바로 결과가 필요하다

`wf-*` workflow부터 쓴다.

예:

- 구조 리뷰: `wf-check-full-review`
- 버그 디버그 시작: `wf-debug-this`
- 개선 후보 찾기: `wf-tidy-find-improvements`
- 질문 품질 올리기: `wf-ask-sharpen`
- 릴리즈 검토: `wf-ship-ready-check`
- 릴리즈 실행: `wf-ship-it`

질문이 너무 막막하면:

- `wf-ask-get-clear`
- 또는 [`packs/ask-pack.md`](./packs/ask-pack.md), [`packs/question-answer-pack.md`](./packs/question-answer-pack.md)부터 본다

문서 체계를 새로 잡고 싶다면:

- [`packs/doc-pack.md`](./packs/doc-pack.md), [`packs/documentation-pack.md`](./packs/documentation-pack.md)부터 본다

기획, 스펙, IA, 기술 설계 문서를 나눠 쓰고 싶다면:

- [`packs/plan-pack.md`](./packs/plan-pack.md), [`packs/spec-pack.md`](./packs/spec-pack.md)부터 본다

릴리즈를 검토하거나 배포하고 싶다면:

- [`packs/ship-pack.md`](./packs/ship-pack.md), [`packs/release-pack.md`](./packs/release-pack.md)부터 본다

### 한 가지 관점만 빠르게 점검하고 싶다

narrow atomic을 쓴다.

예:

- 상수화 후보만: `tidy-find-magic-numbers`
- 중복만: `tidy-find-copies`
- 실패 경로만: `check-failure-paths`
- 테스트 공백만: `test-find-gaps`

### 아직 범위가 흐리다

먼저 범위와 종료 조건부터 고정한다.

예:

- `scout-boundaries`
- `scout-scope`
- `plan-task-breakdown`

## 좋은 요청은 어떻게 생겼나

나쁜 요청:

- `버그 찾아줘`
- `프로젝트 개선해줘`
- `README 좀 정리해줘`

좋은 요청:

- `wf-debug-this로 src/session의 새로고침 후 세션 소실 문제를 좁혀`
- `tidy-find-copies으로 src/auth의 중복 로직만 찾아`
- `doc-curate로 docs와 guides의 링크 구조를 정리해`

좋은 요청에는 보통 세 가지가 있다.

- 범위: 어디를 볼지
- 목표: 무엇을 알고 싶은지
- 종료 조건: 무엇이 나오면 끝인지

## 입력을 잘 넣는 법

아래 항목만 잘 적어도 결과 품질이 많이 좋아진다.

| 입력 종류 | 어떻게 적으면 좋은가 | 나쁜 예 | 좋은 예 |
|---|---|---|---|
| `TARGET_SCOPE` | 가능한 한 좁게 적는다 | `src` | `src/auth`, `src/session/store.ts` |
| `QUESTION` | 한 번에 하나의 판단만 묻는다 | `이 구조 어때?` | `현재 auth 모듈에서 토큰 검증 책임이 어디에 있어야 하는가` |
| `FAILURE_SYMPTOM` | 관찰된 현상만 적는다 | `아마 캐시 문제 같아` | `새로고침 후 로그인 상태가 초기화된다` |
| `DONE_CONDITION` | 확인 가능한 완료 조건으로 적는다 | `잘 동작해야 함` | `로그인/재발급 테스트 통과, 커버리지 80% 이상` |
| `CONSTRAINTS` | 꼭 지켜야 하는 것만 적는다 | `좋게 해줘` | `외부 인증 서비스 사용 금지, PostgreSQL 유지` |

## `compose`는 왜 필요한가

`compose`는 문제를 해결하는 스킬이 아니라, 어떤 스킬들을 어떤 순서로 쓸지 고정하는 엔진이다.

예:

```text
$compose + $wf-check-full-review + @src/auth + $check-delivered
```

이 한 줄은 아래 뜻을 가진다.

- `wf-check-full-review`로 구조 리뷰를 하고
- 범위는 `src/auth`로 제한하고
- 마지막에 `$check-delivered`로 결과를 한 번 더 확인한다

처음에는 `compose`를 직접 이해하려고 하기보다, [`SKILL-COMBOS.md`](./SKILL-COMBOS.md)의 예시를 그대로 쓰는 쪽이 더 쉽다.

카테고리별로 고르고 싶다면 [`packs/README.md`](./packs/README.md)에서 `ask-pack`, `check-pack`, `delivery-pack`, `project-quality-pack` 같은 묶음부터 보는 편이 빠르다.

## `plan-task-breakdown`와 `plan-driven-delivery`는 다르다

이 둘은 이름이 비슷하지만 역할이 완전히 다르다.

### `plan-task-breakdown`

계획을 만든다.

- 목표를 정리한다.
- 작업을 쪼갠다.
- `docs/IMPLEMENTATION-PLAN.md`와 `docs/TASKS.md`를 만든다.

대표 입력:

- `PLANNING_GOAL`
- `TARGET_SCOPE`
- `DONE_CONDITION`

대표 출력:

- `IMPLEMENTATION_PLAN_PATH`
- `TASK_ROWS`
- `DECISION_GATES`

### `plan-driven-delivery`

이미 있는 계획에 맞춰 실행을 정렬한다.

- 어떤 `TASK-ID`를 이번 실행에 연결할지 본다.
- 구현 근거를 task 상태와 연결한다.
- 계획 문서와 실제 작업 흔적이 어긋나지 않게 맞춘다.

대표 입력:

- `IMPLEMENTATION_PLAN_PATH`
- `TASKS_PATH`
- `SELECTED_TASK_IDS`

대표 출력:

- `TASK_LINK_MAP`
- `TASK_STATUS_UPDATES`
- `SYNC_STATUS`

짧게 말하면:

- 계획을 만드는 것은 `plan-task-breakdown`
- 계획에 맞춰 실행을 동기화하는 것은 `plan-driven-delivery`

## 릴리즈 pack은 네 단계다

릴리즈는 한 스킬로 끝내기보다 네 단계로 나누는 편이 더 안전하다.

### `ship-check-repo`

릴리즈를 걸 수 있는 git 상태인지 먼저 본다.

- 지금 위치가 git repo인지
- 작업 브랜치와 대상 브랜치가 있는지
- worktree, remote, tag 상태가 괜찮은지

### `ship-check-hygiene`

릴리즈 전에 정리되어야 할 public surface를 본다.

- 레거시 이름이 남아 있는지
- 문서 업그레이드가 끝났는지
- registry와 user docs가 서로 맞는지

### `ship-go-nogo`

이제 출시해도 되는지 판단한다.

- 배포 위험을 본다
- 롤백 준비를 본다
- `go / no-go / blocked`를 낸다

### `release-publish`

검증이 끝난 변경을 실제 릴리즈 단위로 정리한다.

- source 브랜치를 release candidate로 본다
- `main`에 release-only 커밋을 만든다
- 태그와 GitHub release를 만든다

처음에는 아래 두 entrypoint만 기억하면 된다.

- 검토만 할 때는 `wf-ship-ready-check`
- 검토부터 릴리즈 실행까지 갈 때는 `wf-ship-it`

짧게 말하면:

- git 현실 확인은 `ship-check-repo`
- 문서/레거시/surface gate는 `ship-check-hygiene`
- 출시 판단은 `ship-go-nogo`
- low-level 실제 릴리즈 실행은 `release-publish`

## 문서 작업은 네 종류다

### `doc-write`

문서 내용을 쓴다.

예:

- 사용 가이드 업데이트
- 아키텍처 설명 정리
- 개념 설명 문서 쓰기

형식은 `DOC_FORM`으로 고른다.

- `guide`
- `tutorial`
- `reference`
- `paper-summary`
- `survey`

### `doc-build-index`

계층 구조를 가진 대상을 분석 문서와 인덱스로 묶는다.

예:

- 폴더별 설명 문서 만들기
- 모듈별 분석 문서와 로컬 인덱스 만들기
- 라이브러리나 논문 묶음을 가이드형 또는 요약형으로 정리하기

형식은 `DOC_FORM`으로 고른다.

- `guide`
- `reference`
- `paper-summary`
- `survey`

### `doc-curate`

문서 지형과 링크 구조를 정리한다.

예:

- 어떤 문서가 중복인지 찾기
- guides와 하위 문서 entry 구조 정리
- 남길 문서와 합칠 문서 구분하기

### `doc-publish-readme`

루트 README와 다국어 진입 문서를 만든다.

예:

- GitHub 첫 화면용 README 정리
- 영어 루트 README 작성
- `docs/i18n/<lang>/` 다국어 entry docs 생성

짧게 말하면:

- 문서 내용을 쓰는 것은 `doc-write`
- 계층형 설명 문서와 인덱스를 만드는 것은 `doc-build-index`
- 문서 구조와 탐색성을 정리하는 것은 `doc-curate`
- 루트 README와 다국어 진입 문서를 만드는 것은 `doc-publish-readme`

## 자주 쓰는 workflow

| Workflow | 언제 쓰나 | 필요한 핵심 입력 | 받는 핵심 결과 |
|---|---|---|---|
| `wf-ask-get-clear` | 막연한 주제를 문제 정의와 질문 스택으로 바꾸고 싶을 때 | `TOPIC`, `AUDIENCE` | `PROBLEM_STATEMENT`, `QUESTION_STACK` |
| `wf-ask-sharpen` | 질문을 바로 던질 수준까지 날카롭게 만들고 싶을 때 | `TOPIC`, `AUDIENCE`, `CONSTRAINTS` | `PROBLEM_STATEMENT`, `CORE_QUESTION`, `CHALLENGE_QUESTIONS` |
| `wf-check-full-review` | 구조와 리스크를 리뷰하고 싶을 때 | `TARGET_SCOPE`, `REVIEW_FOCUS` | `REVIEW_FINDINGS`, `CHECK_REPORTS`, `INTEGRATE_OR_HOLD` |
| `wf-check-with-checklist` | 리뷰와 체크리스트를 함께 보고 싶을 때 | `TARGET_SCOPE`, `REVIEW_FOCUS` | `REVIEW_FINDINGS`, `CHECKLIST_TABLE`, `INTEGRATE_OR_HOLD` |
| `wf-debug-this` | 실패 원인을 좁히고 싶을 때 | `TARGET_SCOPE`, `FAILURE_SYMPTOM`, `EXPECTED_BEHAVIOR` | `FAILURE_SURFACE_MAP`, `DEBUG_REPORT`, `TEST_GAP_REPORT` |
| `wf-tidy-find-improvements` | 중복, 상수화, 단순화 후보를 찾고 싶을 때 | `TARGET_SCOPE`, `IMPROVEMENT_GOAL` | `IMPROVEMENT_FINDINGS`, `SIMPLIFICATION_DIRECTION`, `EVIDENCE_BASIS`, `NEXT_IMPLEMENTATION_STEP` |

## 자주 쓰는 atomic

### 리뷰/점검

- `tidy-find-magic-numbers`: 상수화 후보만 찾는다
- `tidy-find-copies`: 중복만 찾는다
- `check-module-walls`: 경계만 점검한다
- `check-failure-paths`: 실패 경로만 본다
- `test-find-gaps`: 테스트 공백만 본다

### 계획/구현 보조

- `scout-boundaries`: 범위와 종료 조건을 고정한다
- `plan-verify-order`: 구현 전에 검증 순서와 stop condition을 만든다
- `test-design-cases`: happy, edge, failure 테스트 케이스를 정리한다
- `plan-task-breakdown`: brief/spec/design 이후 실행 계획과 작업 목록 문서를 만든다
- `doc-find-all`: 문서 목록과 중복을 수집한다

### 테스트 작업을 나누는 법

- `test-design-cases`: 무엇을 테스트해야 하는지 먼저 정리할 때
- `test-find-gaps`: 지금 무엇이 빠졌는지 찾을 때
- `test-write-guards`: 실제 테스트 코드를 추가하고 실행할 때
- `test-run-user-scenarios`: 실제 사용자/에이전트처럼 시나리오를 돌려 framework surface를 검증할 때
- `check-delivered`: 마지막에 계약대로 증명됐는지 확인할 때

`check-delivered`는 테스트 스킬이 아니라 최종 계약 검증 스킬이라 `test-` family 밖에 둔다.

## 가장 많이 쓰는 시작 조합

### 특정 폴더를 리뷰하고 싶다

```text
$compose + $wf-check-full-review + @src/auth + $check-delivered
```

### 버그 원인을 좁히고 싶다

```text
$compose + $wf-debug-this + @src/session + [새로고침 후 세션이 사라진다]
```

### 개선 후보를 먼저 찾고 싶다

```text
$compose + $wf-tidy-find-improvements + @src/api
```

### 계획부터 만들고 싶다

```text
$compose + $plan-task-breakdown
```

### 계획에 맞춰 구현하고 검증하고 싶다

```text
$compose + $plan-driven-delivery + $build-write-code + [execution-mode: final-only] + $check-delivered + docs/IMPLEMENTATION-PLAN.md + docs/TASKS.md
```

## 더 쉬운 예시는 어디에 있나

- 실전 복붙 예시집: [`SKILL-COMBOS.md`](./SKILL-COMBOS.md)
- atomic 스킬 설명서: [`ATOMIC-SKILLS.md`](./ATOMIC-SKILLS.md)
- 질문/답변 준비 pack: [`packs/question-answer-pack.md`](./packs/question-answer-pack.md)
- 릴리즈 pack: [`packs/release-pack.md`](./packs/release-pack.md)
- compose 엔진 설명: [`compose/SKILL.md`](./compose/SKILL.md)
- registry 기준: [`_registry/README.md`](./_registry/README.md)
- 현재 시스템 상태: [`../docs/SKILL-STATE-REPORT.md`](../docs/SKILL-STATE-REPORT.md)
