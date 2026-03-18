# Runtime Skills

> 이 문서는 `skills/` 안의 스킬을 처음 고르는 사람을 위한 설명서다.
> 예전 `ATOMIC-SKILLS.md`가 expert reference에 가까웠다면, 여기서는 먼저 "그래서 이 스킬이 실제로 뭘 해 주는데?"를 답한다.
> 더 엄밀한 계약은 각 스킬 폴더의 `SKILL.md`를 열면 된다.

## 이 폴더가 무엇인가

이 폴더는 Codex runtime이 바로 읽는 스킬 surface다.

- `skills/<name>/SKILL.md`: 사람이 읽는 설명서다.
- `skills/<name>/skill.json`: runtime이 읽는 기계용 계약이다.
- `skills/_meta/*.json`: 여러 스킬이 함께 쓰는 공통 메타데이터다.

## 먼저 감을 잡자

스킬은 크게 세 층으로 보면 쉽다.

- `workflow-*`: 코스 요리다. 질문 정리, 디버깅, 테스트 보강처럼 한 덩어리 일을 처음부터 끝까지 이어 준다.
- atomic skills: 단품 공구다. 이미 무엇을 할지 아는 사람이 필요한 동작만 골라 정밀하게 쓴다.
- control / utility: 공구를 묶고, 반복을 밀어주고, 마지막 응답을 다듬는 내부 제어 장치다.

처음이면 거의 항상 workflow부터 고르면 된다.
atomic은 "나는 지금 정확히 이 동작만 필요하다"는 순간에 꺼내 쓰면 된다.

## 이 문서를 읽는 순서

- 무엇을 써야 할지 아직 감이 없으면 `Workflow Skills`부터 본다.
- 한 번에 맡기지 말고 세밀하게 조립하고 싶으면 `Atomic Skills`로 내려간다.
- 입력 키, 출력 키, 제약 조건까지 확인해야 하면 각 스킬의 `SKILL.md`를 연다.

## 빠르게 고르기

| 지금 필요한 것 | 먼저 고를 스킬 | 왜 이걸 먼저 고르나 |
|---|---|---|
| 머릿속 주제가 흐리다 | [`workflow-clarify-request`](./workflow-clarify-request/SKILL.md) | 문제 정의와 질문 구조를 한 번에 또렷하게 만든다 |
| 현재 구조를 먼저 알고 싶다 | [`workflow-scout-structure`](./workflow-scout-structure/SKILL.md) | 범위를 정하고 지금 모양을 지도처럼 펼쳐 준다 |
| 구조·복잡도·의존성을 한 번에 분석하고 싶다 | [`workflow-analyze-codebase`](./workflow-analyze-codebase/SKILL.md) | 판정 없이 코드베이스 전체 분석 지도를 만든다 |
| 설계안, 리팩터링 방향, 디버깅 가설을 3개 모델 합의로 좁히고 싶다 | [`workflow-consensus-engine`](./workflow-consensus-engine/SKILL.md) | 경계를 먼저 잠그고 다중 모델 합의를 돌려 권고안과 충돌 지점을 분리한다 |
| 간단한 코드 리뷰가 필요하다 | [`workflow-review-change`](./workflow-review-change/SKILL.md) | 구조 파악과 리뷰 스캔을 함께 돌린다 |
| 구조·품질·보안·실패경로 완전한 리뷰가 필요하다 | [`workflow-review-complete`](./workflow-review-complete/SKILL.md) | 5가지 리뷰 렌즈를 모두 통과하는 완전한 리뷰 |
| 버그를 처음부터 끝까지 추적하고 싶다 | [`workflow-debug-this`](./workflow-debug-this/SKILL.md) | 재현, 원인, 수정 확인까지 한 흐름으로 묶는다 |
| 구현 전에 계획을 세우고 싶다 | [`workflow-plan-build-ready`](./workflow-plan-build-ready/SKILL.md) | 범위 계약부터 설계와 태스크 아티팩트까지 만든다 |
| 바로 구현하고 테스트 보호막까지 같이 만들고 싶다 | [`workflow-build-implement-and-guard`](./workflow-build-implement-and-guard/SKILL.md) | 코드 수정 뒤 회귀 방지 테스트까지 이어 준다 |
| 기존 태스크 문서를 끝까지 자동 실행하고 싶다 | [`workflow-build-execute-plan`](./workflow-build-execute-plan/SKILL.md) | `plans/TASKS.md`를 읽고 루프를 계속 돈다 |
| 테스트가 어디 비었는지 찾고 메우고 싶다 | [`workflow-test-close-gaps`](./workflow-test-close-gaps/SKILL.md) | 빈 구멍 찾기부터 테스트 작성까지 이어 준다 |
| 방금 바꾼 코드를 더 깔끔하고 빠르게 다듬고 싶다 | [`workflow-tidy-simplify-this`](./workflow-tidy-simplify-this/SKILL.md) | 최근 변경분을 리유즈·퀄리티·효율 관점으로 리뷰하고 바로 고친다 |
| 어디부터 정리해야 할지 먼저 지도부터 보고 싶다 | [`workflow-tidy-find-improvements`](./workflow-tidy-find-improvements/SKILL.md) | 복잡성 지도부터 개선 포인트까지 정리한다 |
| 문서 표면을 keep/update/deprecate/delete 기준으로 정리하고 싶다 | [`workflow-doc-systemize`](./workflow-doc-systemize/SKILL.md) | 인벤토리부터 수명주기 판정과 필요한 브리지 문서 작성까지 한 번에 이어 준다 |
| 폴더 트리를 부모 README + 자식 프로젝트 정보 문서로 만들고 싶다 | [`workflow-doc-build-docset`](./workflow-doc-build-docset/SKILL.md) | 상위 폴더는 요약과 링크, 하위 폴더는 상세 정보로 나눠 계층 문서 세트를 만든다 |
| 릴리즈 노트, 변경 요약, 업그레이드 문서를 만들고 싶다 | [`workflow-doc-release-package`](./workflow-doc-release-package/SKILL.md) | 현재 릴리즈 범위를 근거로 릴리즈 문서를 묶어서 만든다 |
| 보안 노출만 좁게 보고 싶다 | [`review-security`](./review-security/SKILL.md) | 비밀키, ignore drift, 공개 설정 노출 같은 위험만 좁게 본다 |
| 배포 가능한지 먼저 판단하고 싶다 | [`workflow-release-ready-check`](./workflow-release-ready-check/SKILL.md) | 저장소 상태, 릴리즈 위생, 최종 출고 준비를 점검한다 |
| 릴리즈 점검부터 publish까지 한 번에 하고 싶다 | [`control-release-publish-flow`](./control-release-publish-flow/SKILL.md) | 점검, 커밋/태그, 공개까지 한 흐름으로 묶는 내부 제어 경로다 |

## Sync Profiles

- `core`: planning, build, debug, review, test, tidy 중심 기본 surface
- `docs-release`: docs, release, security 중심 surface
- `extras`: `gemini`, `commit-write-message`
- `all`: 전체 runtime surface

## 입력을 조금만 더 잘 주는 법

스킬은 마법이 아니라 좋은 작업 지시를 잘게 쪼개 둔 것이다.
그래서 아래 네 가지만 붙여도 결과가 훨씬 안정적이다.

- 범위가 흐리면 `SCOPE`: 어디를 볼지 적는다.
- 목표가 흐리면 `GOAL`: 결국 무엇을 이루고 싶은지 적는다.
- 기대 동작이 있으면 `EXPECTED`: 어떤 결과를 기대하는지 적는다.
- 완료 기준이 있으면 `DONE`: 무엇을 보면 끝났다고 인정할지 적는다.

## Workflow Skills

기본 진입은 workflow다.
쉽게 말해 "어떤 공구를 어떤 순서로 써야 할지 내가 다 고르고 싶지 않다"면 workflow를 쓰면 된다.

### 질문을 또렷하게 만드는 workflow

- [`workflow-clarify-request`](./workflow-clarify-request/SKILL.md): 이미 있는 질문을 더 쪼개고, 무엇을 가정하고 있는지 흔들어 보면서 "진짜 물어야 할 질문"으로 벼린다.

### 범위와 현재 구조를 파악하는 workflow

- [`workflow-scout-structure`](./workflow-scout-structure/SKILL.md): 먼저 범위를 분명히 정한 다음 (`clarify-scope`), 그 안의 현재 구조를 지도로 그려 준다 (`analyze-structure`). 새 설계 전에 "지금 뭐가 어디에 있는지"부터 알고 싶을 때 맞다.
- [`workflow-analyze-codebase`](./workflow-analyze-codebase/SKILL.md): 구조, 복잡도, 의존성을 한 번에 분석한다. 코드베이스를 처음 파악하거나 리팩터링 전에 전체 그림이 필요할 때 쓴다.

### 다중 모델 합의를 위한 workflow

- [`workflow-consensus-engine`](./workflow-consensus-engine/SKILL.md): 범위와 완료 조건을 먼저 잠근 뒤, Codex, Claude Code, Gemini CLI의 독립 응답과 반박 라운드를 통해 권고안, 남는 충돌, 가장 싼 다음 확인을 정리한다.

### 리뷰와 점검을 위한 workflow

- [`workflow-review-change`](./workflow-review-change/SKILL.md): 한 폴더나 모듈을 보고 구조 파악과 리뷰 스캔을 함께 수행한다. 막연한 "버그 좀 봐 줘"보다 훨씬 투명한 리뷰 흐름이다.
- [`workflow-review-complete`](./workflow-review-complete/SKILL.md): 구조 분석, 품질, 보안, 실패 경로, 변경 리뷰를 모두 포함하는 완전한 리뷰. 중요한 PR이나 릴리즈 전 전면 점검에 맞다.
- 체크리스트 관점이 추가로 필요하면 `workflow-review-change` 뒤에 `review-quality`를 compose하는 쪽이 기본이다.

### 버그를 잡는 workflow

- [`workflow-debug-this`](./workflow-debug-this/SKILL.md): 증상을 재현 가능한 실패로 바꾸고, 실패 범위를 좁히고, 원인을 찾고, 정말 고쳐졌는지까지 확인한다. 디버깅 풀코스라고 생각하면 된다.

### 계획을 만드는 workflow

- [`workflow-plan-build-ready`](./workflow-plan-build-ready/SKILL.md): 흐린 요청을 작업 가능한 범위 계약으로 바꾸고, 구현 가능한 설계와 실행용 태스크 문서까지 만든다. 구현 전에 길을 그리는 일이다.

### 구현과 실행을 맡기는 workflow

- [`workflow-build-implement-and-guard`](./workflow-build-implement-and-guard/SKILL.md): 코드를 바꾸고 끝내지 않는다. 바뀐 동작을 지켜 줄 테스트나 회귀 방지 장치까지 바로 붙인다.
- [`workflow-build-execute-plan`](./workflow-build-execute-plan/SKILL.md): 이미 `plans/TASKS.md` 같은 태스크 장부가 있을 때, 그 장부를 따라 구현하고 점검하고 다시 sync하는 루프를 끝까지 돌린다.
- [`control-build-until-done`](./control-build-until-done/SKILL.md): 플랜 문서 없이, DONE_CONDITION만으로 코드 작업을 끝까지 자율 실행한다. evaluate → implement → verify를 반복하며 done이 증명될 때까지 멈추지 않는다.
- [`control-finish-until-done`](./control-finish-until-done/SKILL.md): `control-build-until-done`의 비코드 대응. 플랜 문서 없이 문서/리뷰/계획을 끝까지 자율 실행한다. evaluate → improve → verify, craft-clarity lens.

#### 어떤 스킬을 골라야 할까?

| 상황 | 스킬 | 플랜 필요? | 도메인 | "완료" 기준 |
|------|------|:---------:|--------|------------|
| 코드를 끝까지 고쳐야 한다. 태스크 문서 없음 | `control-build-until-done` | ✗ | 코드 | 테스트 통과 |
| TASKS.md가 있고 전부 실행해야 한다 | `workflow-build-execute-plan` | **필수** | 코드 | 모든 태스크 행 완료 |
| 문서/리뷰/계획을 끝까지 만들어야 한다 | `control-finish-until-done` | ✗ | 비코드 | 독자가 이해할 수 있음 |

### 테스트를 메우는 workflow

- [`workflow-test-close-gaps`](./workflow-test-close-gaps/SKILL.md): 어디가 비어 있는지 찾고, 어떤 케이스를 막아야 하는지 설계하고, 실제 테스트까지 쓴다. "테스트 좀 보강해"의 표준 진입점이다.

### 구조 개선을 위한 workflow

- [`workflow-tidy-simplify-this`](./workflow-tidy-simplify-this/SKILL.md): 최근 변경분을 리유즈, 구조 품질, 효율 관점으로 병렬 리뷰하고, 안전한 수정만 바로 적용한다. 구현 뒤 마지막 정리 패스로 쓰기 좋다.
- [`workflow-tidy-find-improvements`](./workflow-tidy-find-improvements/SKILL.md): 복잡한 곳, 중복된 곳, 정리하면 좋아질 곳을 먼저 지도처럼 보여 준다. 막연한 "좀 더 깔끔하게"를 구체적인 개선 후보로 바꾸는 분석 전용 workflow다.

### 문서를 다루는 workflow

- [`workflow-doc-systemize`](./workflow-doc-systemize/SKILL.md): 문서를 전수 조사한 뒤 keep/update/deprecate/delete 기준으로 판정하고, 필요한 브리지 문서나 갱신만 좁게 적용한다. 문서 거버넌스의 기본 진입점이다.
- [`workflow-doc-build-docset`](./workflow-doc-build-docset/SKILL.md): 폴더 트리를 부모 README 스타일 요약 문서와 자식 프로젝트 정보 문서로 나눠 계층 문서 세트로 만든다. 상위는 요약, 하위는 상세라는 경계를 분명히 하고 싶을 때 맞다.
- [`workflow-doc-release-package`](./workflow-doc-release-package/SKILL.md): 릴리즈 범위를 근거로 릴리즈 노트, 변경 요약, 업그레이드/마이그레이션 문서를 만든다. 릴리즈 설명 자체를 문서 artifact로 남기고 싶을 때 쓴다.

### 보안과 릴리즈를 다루는 workflow

- [`review-security`](./review-security/SKILL.md): 비밀 정보 노출, ignore drift, 공개 설정 누락 같은 위험을 점검한다.
- [`workflow-release-ready-check`](./workflow-release-ready-check/SKILL.md): 저장소가 실제로 릴리즈할 상태인지, 문서와 위생이 맞는지, 최종 출고해도 되는지 차분하게 점검한다.
- [`control-release-publish-flow`](./control-release-publish-flow/SKILL.md): 릴리즈 준비 점검에서 끝나지 않고, release-only 커밋과 태그, publish 흐름까지 묶어 실제 출고까지 밀어 준다.

## Atomic Skills

atomic은 "공구함"이다.
workflow가 세트 메뉴라면, atomic은 드라이버, 스패너, 테스터기 하나씩 꺼내 쓰는 방식이다.

여기서부터는 "무엇을 할지 이미 안다"는 전제가 있다.
그래서 설명도 "이 공구가 무슨 일만 담당하는가"에 집중한다.

### `ask-` — 질문을 만드는 공구

이 묶음은 생각을 질문으로 바꾸는 공구다.
답을 구하기 전에, 먼저 무엇을 물어야 하는지 다듬는다.

- [`ask-clarify-question`](./ask-clarify-question/SKILL.md): 흐릿한 주제를 한 문장 질문으로 묶는다. 아무 말이나 많을 때 핵심 한 줄을 잡는 공구다.
- [`ask-break-it-down`](./ask-break-it-down/SKILL.md): 이미 잡힌 질문을 작은 질문 묶음으로 쪼갠다. 큰 문제를 한 번에 삼키지 않게 해 준다.
- [`ask-flip-assumption`](./ask-flip-assumption/SKILL.md): 질문 뒤에 숨어 있는 당연하다고 믿은 전제를 뒤집어 본다. 막힌 생각을 옆문으로 열 때 유용하다.
- [`ask-fix-prompt`](./ask-fix-prompt/SKILL.md): 이미 받은 답이 엉뚱하거나 얕았을 때, 프롬프트를 최소한으로 고쳐 다시 묻도록 도와준다.

### `clarify-` — 요청과 범위를 명확히 하는 공구

이 묶음은 흐릿한 요청을 명확한 계약으로 바꾸는 공구다.
무엇을 할지 모르는 상태에서 시작하지 않게 해 준다.

- [`clarify-scope`](./clarify-scope/SKILL.md): 모호한 요청을 범위, 제약, 완료 기준으로 정리한다. 아직 일의 테두리가 흐릴 때 쓴다.
- [`clarify-boundaries`](./clarify-boundaries/SKILL.md): 어디까지가 이번 일이고 어디부터가 아닌지 경계를 선명하게 그린다.

### `analyze-` — 판정 없이 구조를 분석하는 공구

이 묶음은 결론이나 verdict 없이 구조, 복잡도, 의존성, 근거를 지도로 그리는 공구다.
"무엇이 문제인가" 전에 "무엇이 있는가"를 보는 공구다.

- [`analyze-structure`](./analyze-structure/SKILL.md): 현재 구조를 지도처럼 그린다. 파일, 책임, 경계가 어떻게 나뉘는지 보고 싶을 때 맞다.
- [`analyze-options`](./analyze-options/SKILL.md): 몇 가지 선택지를 나란히 놓고 장단점을 비교한다. "A로 갈까 B로 갈까"를 따질 때 쓴다.
- [`analyze-evidence-gap`](./analyze-evidence-gap/SKILL.md): 결론을 믿기 전에 빠진 근거가 무엇인지 찾는다. 자신감이 아니라 증거가 필요한 순간에 맞다.
- [`analyze-baseline`](./analyze-baseline/SKILL.md): 성능이나 수치를 개선하기 전에 현재 기준선을 정확히 찍어 둔다. 빠르게 만들기 전에 먼저 재는 공구다.
- [`analyze-complexity`](./analyze-complexity/SKILL.md): 코드 복잡도를 순환 복잡도, 인지 복잡도, 결합 복잡도 기준으로 지도로 만든다.
- [`analyze-dependencies`](./analyze-dependencies/SKILL.md): 의존성 방향, 순환, fan-in/fan-out, 위반을 분석한다. 모듈 결합을 줄이기 전에 전체 그림부터 보는 공구다.
- [`analyze-impact`](./analyze-impact/SKILL.md): 변경이 어디까지 영향을 미치는지 직접/전이 범위를 추적한다. 수정 전에 파장을 먼저 확인하는 공구다.
- [`analyze-module-bounds`](./analyze-module-bounds/SKILL.md): 모듈이나 API 경계가 흐린지, 책임이 새는지 중립적으로 확인한다.
- [`analyze-release-risk`](./analyze-release-risk/SKILL.md): 배포 전 위험 게이트를 neutral하게 지도로 만든다. GO/NO-GO는 내지 않는다.

### `plan-` — 만들기 전에 설계하는 공구

이 묶음은 바로 손대지 않고 먼저 설계를 세우는 공구다.
무턱대고 코드를 바꾸지 않게 해 준다.

- [`plan-why-build-this`](./plan-why-build-this/SKILL.md): 왜 이걸 만드는지부터 짧게 정리한다. 사용자, 문제, 기대 효과, 비목표를 잡는 제품 브리프 공구다.
- [`plan-what-it-does`](./plan-what-it-does/SKILL.md): 기능이 정확히 무엇을 해야 하는지, 어떤 경우를 처리해야 하는지 스펙으로 적는다.
- [`plan-screen-map`](./plan-screen-map/SKILL.md): 화면, 페이지, 이동 흐름을 먼저 그린다. UI나 사용자 흐름을 설계할 때 맞다.
- [`plan-how-to-build`](./plan-how-to-build/SKILL.md): 요구사항이 이미 승인된 상태에서, 데이터 흐름과 구조와 검증 방법까지 포함한 기술 설계를 만든다.
- [`plan-dependency-rules`](./plan-dependency-rules/SKILL.md): 모듈 사이에 누가 누구를 참조해도 되는지 규칙을 세운다. 리팩터링 전에 선을 긋는 공구다.
- [`plan-verify-order`](./plan-verify-order/SKILL.md): 코드를 바꾸기 전에 어떤 순서로 검증할지 정한다. 작은 확인부터 큰 확인으로 가는 길을 만드는 공구다.
- [`plan-task-breakdown`](./plan-task-breakdown/SKILL.md): 설계를 실제 작업 항목으로 쪼개 `IMPLEMENTATION-PLAN`이나 `TASKS` 문서로 만든다.

### `build-` — 실제로 바꾸는 공구

이 묶음은 설계가 끝났고 이제 손을 움직일 차례일 때 쓰는 공구다.
생각이 아니라 실행을 담당한다.

- [`build-write-code`](./build-write-code/SKILL.md): 실제 코드 변경을 수행하고, 그 변경이 맞다는 검증 근거를 남긴다. 구현 자체를 담당하는 핵심 공구다.
- [`build-make-faster`](./build-make-faster/SKILL.md): 성능 병목을 측정하고, 개선하고, 전후 차이를 확인한다. 감으로 최적화하지 않게 해 준다.

### `debug-` — 왜 망가졌는지 찾는 공구

이 묶음은 버그를 "느낌"이 아니라 "재현 가능한 현상"으로 다루게 해 준다.
증상, 범위, 원인, 수정 확인을 나눠 본다.

- [`debug-capture-failure`](./debug-capture-failure/SKILL.md): "가끔 망가져요"를 재현 가능한 실패 절차로 바꾼다.
- [`debug-map-impact`](./debug-map-impact/SKILL.md): 이 버그가 어디까지 번지는지, 무엇이 기대와 다르게 보이는지 영향 범위를 그린다.
- [`debug-find-root-cause`](./debug-find-root-cause/SKILL.md): 재현 가능한 버그가 있을 때 진짜 원인을 찾아낸다. 추측이 아니라 근거 중심으로 파고드는 공구다.
- [`debug-confirm-fix`](./debug-confirm-fix/SKILL.md): 고친 것처럼 보이는 수정안이 정말 문제를 없앴는지, 다시 안 터지게 막았는지 확인한다.

### `review-` — 판정을 내리는 리뷰 공구

이 묶음은 "좋아 보인다"가 아니라 pass/fail, integrate/hold 같은 명시적 결론을 내는 공구다.
판단 없는 분석이 필요하면 `analyze-*`를 쓴다.

- [`review-change`](./review-change/SKILL.md): PR 리뷰처럼 문제를 우선순위와 근거와 함께 정리한다. 승인할지 보류할지 판단하는 공구다.
- [`review-quality`](./review-quality/SKILL.md): 정해진 9개 품질 항목으로 바뀐 코드를 훑는다. 체크리스트 검사관에 가깝다.
- [`review-failure-paths`](./review-failure-paths/SKILL.md): 정상 경로가 아니라 실패 경로만 집중해서 본다. 예외 처리와 복구가 약한지 점검할 때 맞다.
- [`review-security`](./review-security/SKILL.md): 보안 노출, 비밀 정보 유출, OWASP 취약 지점을 우선순위와 함께 검토한다.
- [`review-final-verify`](./review-final-verify/SKILL.md): 작업이 끝난 뒤, 약속한 완료 조건이 정말 충족됐는지 마지막으로 확인한다.
- [`control-improve-loop`](./control-improve-loop/SKILL.md): 결과물을 보고 가장 값비싼 흠을 하나씩 고치며 품질 문턱까지 반복한다. 자기 피드백 루프 공구 (control 카테고리).

### `test-` — 보호막을 만드는 공구

이 묶음은 테스트를 "있다/없다"가 아니라 "무엇을 지켜야 하는가"로 보게 해 준다.

- [`test-find-gaps`](./test-find-gaps/SKILL.md): 중요한 동작에 테스트 구멍이 어디 있는지 찾는다.
- [`test-design-cases`](./test-design-cases/SKILL.md): 정상, 경계, 실패 케이스를 빠짐없이 설계한다. 테스트 설계도 역할을 한다.
- [`test-write-guards`](./test-write-guards/SKILL.md): 실제 자동화 테스트를 써서 다음 번 같은 버그를 막는 보호막을 만든다.
- [`test-run-user-scenarios`](./test-run-user-scenarios/SKILL.md): 진짜 사용자나 에이전트가 쓸 법한 시나리오로 돌려 보면서 헷갈리는 지점과 깨지는 지점을 찾는다.

### `tidy-` — 복잡함을 줄이는 공구

이 묶음은 "새 기능 추가"가 아니라 "같은 일을 더 단순하게" 만드는 공구다.
복잡성의 원인을 보고, 중복을 찾고, 낡은 흔적을 걷어낸다.

- [`tidy-analyze`](./tidy-analyze/SKILL.md): 지금 왜 복잡한지 원인을 먼저 분해한다. 본질적인 복잡함과 쓸데없는 복잡함을 구분하는 공구다.
- [`tidy-cut-fat`](./tidy-cut-fat/SKILL.md): 핵심 동작은 그대로 두고 군살만 도려낸다. 과한 구조, 시끄러운 폴더, 쓸데없는 추상화를 줄일 때 맞다.
- [`tidy-review-reuse`](./tidy-review-reuse/SKILL.md): 최근 변경분에서 이미 있는 유틸이나 헬퍼를 재사용할 수 있었는지 찾는다.
- [`tidy-review-quality`](./tidy-review-quality/SKILL.md): 중복 상태, 파라미터 비대화, 새는 추상화 같은 구조 품질 문제를 리뷰한다.
- [`tidy-review-efficiency`](./tidy-review-efficiency/SKILL.md): 불필요한 일, 놓친 병렬화, 핫패스 비대화, 메모리 낭비 같은 효율 문제를 리뷰한다.
- [`tidy-find-copies`](./tidy-find-copies/SKILL.md): 같은 로직이나 구조가 여러 군데 복제돼 있는지 찾는다.
- [`tidy-find-magic-numbers`](./tidy-find-magic-numbers/SKILL.md): 여기저기 흩어진 숫자와 상수 후보를 찾아 한곳으로 모으도록 돕는다.
- [`tidy-reorganize`](./tidy-reorganize/SKILL.md): 동작은 유지한 채 파일 구조와 경계를 더 낫게 재배치하는 리팩터링 계획 공구다.
- [`tidy-simplify`](./tidy-simplify/SKILL.md): 한정된 범위에서 실제 코드 구조를 더 짧고 이해하기 쉬운 모양으로 단순화한다. "방금 바꾼 diff를 전체적으로 정리"하는 기본 진입은 아니다.
- [`tidy-apply-review-fixes`](./tidy-apply-review-fixes/SKILL.md): 여러 review atomic 결과를 모아 겹치는 지적을 정리한 뒤, 안전한 수정만 실제 코드에 반영한다.
- [`tidy-remove-legacy`](./tidy-remove-legacy/SKILL.md): 오래된 파일, 다 끝난 계획 문서, 죽은 별칭, 쓸모없는 접착 코드 같은 잔재를 치운다.

### `doc-` — 문서를 다루는 공구

이 묶음은 코드가 아니라 설명과 문서 표면을 정리하는 공구다.
무엇이 있는지 찾고, 수명주기를 판정하고, 계층 문서를 만들고, 필요한 문서를 실제로 쓴다.

- [`doc-find-all`](./doc-find-all/SKILL.md): 문서를 전수 조사해서 고아 문서, 중복 문서, 시간에 묶인 문서, delivery-only 문서를 찾는다.
- [`doc-curate`](./doc-curate/SKILL.md): 각 문서를 keep/update/deprecate/delete로 분류하고, 삭제 전에 옮겨야 할 durable knowledge와 대체 경로를 정한다.
- [`doc-write`](./doc-write/SKILL.md): 아키텍처 노트, 사용 가이드, 개념 설명, deprecation/redirect 문서 같은 비루트 문서를 실제로 쓴다.
- [`doc-build-index`](./doc-build-index/SKILL.md): 폴더 트리를 부모 README 스타일 요약 문서와 자식 프로젝트 정보 문서로 나눠 계층 문서 세트로 만든다.
- [`doc-write-release-docs`](./doc-write-release-docs/SKILL.md): 릴리즈 노트, changelog entry, 업그레이드/마이그레이션 문서, 롤백 요약 같은 릴리즈 문서를 쓴다.
- [`doc-publish-readme`](./doc-publish-readme/SKILL.md): 저장소 루트 README를 GitHub 입구답게 만들고, 필요하면 언어별 진입 문서까지 함께 퍼블리시한다.

### `release-` — 출고를 준비하는 공구

이 묶음은 "코드가 돌아간다"를 넘어서 "이걸 내보내도 되나"를 판단하는 공구다.

- [`release-check-repo`](./release-check-repo/SKILL.md): 이 저장소가 실제로 릴리즈 가능한 git 상태인지, 브랜치와 remote가 맞는지부터 확인한다.
- [`release-check-hygiene`](./release-check-hygiene/SKILL.md): 낡은 파일이 남아 있지 않은지, 공개 표면과 문서가 어긋나지 않는지 릴리즈 위생을 본다.
- [`release-verdict`](./release-verdict/SKILL.md): 배포 범위, 롤아웃, 롤백 준비를 보고 GO/NO-GO 판단을 내린다.

### `commit-` — 커밋 메시지를 만드는 공구

- [`commit-write-message`](./commit-write-message/SKILL.md): 이미 끝난 변경을 바탕으로 Conventional Commit 메시지 후보를 만든다.

### Control / Utility Atomic

이 묶음은 일반적인 public entry라기보다, 여러 스킬을 묶고 루프를 돌리고 최종 응답을 정리하는 내부 제어 공구에 가깝다.
정밀 조립이 필요할 때만 꺼내 쓰면 된다.

- [`compose`](./compose/SKILL.md): 여러 스킬을 정해진 순서로 연결하는 조립판이다. 한 번에 하나의 workflow로 안 끝날 때 쓴다.
- [`control-build-until-done`](./control-build-until-done/SKILL.md): 플랜 문서 없이 끝까지 자율 실행 → 위 "구현과 실행" 섹션 참조.
- [`control-finish-until-done`](./control-finish-until-done/SKILL.md): 플랜 문서 없이 문서/리뷰/계획 작업을 끝까지 자율 실행한다. `control-build-until-done`의 비코드 대칭 스킬. craft-clarity lens — "작성됨"과 "완료됨"은 다르다.
- [`control-release-publish-flow`](./control-release-publish-flow/SKILL.md): release ready check와 publish를 한 control path로 묶는다.
- [`plan-sync-tasks`](./plan-sync-tasks/SKILL.md): `TASKS.md` 같은 태스크 장부와 실제 진행 상태를 맞춰 주는 동기화 공구다.
- [`release-publish`](./release-publish/SKILL.md): 점검이 끝난 변경을 release-only 커밋, 태그, GitHub release publish로 실제 출고하는 공구다.
- [`gemini`](./gemini/SKILL.md): 사용자가 명시적으로 원할 때만 Gemini CLI를 외부 조사원처럼 붙이는 특수 공구다. 기본값으로는 쓰지 않는다.

## 마지막으로

헷갈릴 때는 이렇게 고르면 된다.

- 처음 시작한다: workflow에서 고른다.
- 이미 흐름을 알고 있다: atomic에서 필요한 공구만 고른다.
- 여러 atomic을 순서대로 묶어야 한다: `compose`를 쓴다.
- 끝날 때까지 반복 실행이 필요하다: `control-build-until-done` 또는 `control-finish-until-done`을 본다.
- 계약을 엄밀하게 확인해야 한다: 각 스킬 폴더의 `SKILL.md`를 연다.
