# Atomic Skills 사용 가이드

> 한 스킬은 한 가지 일만 합니다.
> 이 문서는 **전체 atomic 스킬 목록과 빠른 선택 가이드**입니다.
> 각 카테고리 상세 설명은 아래 파일을 여세요.

---

## 카테고리별 상세 가이드

| 파일 | 카테고리 | 스킬 수 | 무엇을 하나 |
|------|---------|:------:|------------|
| [이해하기](./SKILL-GUIDE-UNDERSTAND.md) | ask, clarify, analyze | 15 | 질문 다듬기, 범위 명확화, 중립 분석 |
| [만들기](./SKILL-GUIDE-BUILD.md) | plan, build, debug, test | 17 | 설계, 구현, 버그 추적, 테스트 |
| [검증하기](./SKILL-GUIDE-REVIEW.md) | review, release, commit, control | 12 | 리뷰 판정, 배포 검증, 반복 제어 |
| [정리하기](./SKILL-GUIDE-MAINTAIN.md) | tidy, doc | 15 | 코드 정리, 문서 관리 |

---

## 처음이라면

Atomic 스킬 대신 **workflow 스킬부터** 고르면 됩니다.
Atomic은 "이 동작만 딱 필요해"라는 순간에 꺼내 씁니다.

```
$[스킬이름]
[입력키]: [값]
```

예시:
```
$build-write-code
GOAL: 로그인 버튼 클릭 시 세션이 유지되도록 수정
SCOPE: src/auth
DONE: 로그인 후 새로고침해도 로그인 상태 유지
```

---

## 카테고리 한눈에 보기

| 카테고리 | 역할 | 대표 스킬 |
|---------|------|---------|
| `ask-*` | 질문 자체를 다듬기 | ask-clarify-question, ask-break-it-down |
| `clarify-*` | 범위와 경계를 계약으로 | clarify-scope, clarify-boundaries |
| `analyze-*` | 판정 없는 중립 분석 | analyze-structure, analyze-complexity |
| `plan-*` | 설계와 계획 | plan-how-to-build, plan-task-breakdown |
| `build-*` | 코드 구현과 성능 개선 | build-write-code, build-make-faster |
| `debug-*` | 버그 재현·분석·수정 확인 | debug-find-root-cause |
| `review-*` | 판정 포함 리뷰 (integrate/hold) | review-change, review-security |
| `test-*` | 테스트 빈틈 찾기·설계·작성 | test-find-gaps, test-write-guards |
| `tidy-*` | 코드 정리, 중복 제거 | tidy-analyze, tidy-cut-fat |
| `doc-*` | 문서 인벤토리·정리·작성 | doc-find-all, doc-write |
| `release-*` | 배포 상태 점검·판단 | release-verdict |
| `commit` | 커밋 메시지 생성 | commit-write-message |
| `control-*` | 반복 루프 제어 | control-improve-loop |

---

## 빠른 선택표

| 지금 필요한 것 | 쓸 스킬 |
|--------------|---------|
| 뭘 물어야 할지 모르겠다 | `ask-clarify-question` |
| 큰 문제를 작게 쪼개고 싶다 | `ask-break-it-down` |
| 다른 시각으로 보고 싶다 | `ask-flip-assumption` |
| 답이 엉뚱하게 나왔다 | `ask-fix-prompt` |
| 작업 범위가 흐리다 | `clarify-scope` |
| 경계만 명확히 하고 싶다 | `clarify-boundaries` |
| 코드 구조를 지도처럼 보고 싶다 | `analyze-structure` |
| 복잡도 원인을 측정하고 싶다 | `analyze-complexity` |
| 의존성 방향과 순환을 보고 싶다 | `analyze-dependencies` |
| 변경이 어디까지 영향 미치는지 알고 싶다 | `analyze-impact` |
| 두 방식을 근거로 비교하고 싶다 | `analyze-options` |
| 배포 전 위험 게이트를 지도로 보고 싶다 | `analyze-release-risk` |
| 왜 만드는지 정리하고 싶다 | `plan-why-build-this` |
| 기능 명세를 쓰고 싶다 | `plan-what-it-does` |
| 작업 목록을 만들고 싶다 | `plan-task-breakdown` |
| 코드를 직접 구현하고 싶다 | `build-write-code` |
| 성능을 개선하고 싶다 | `build-make-faster` |
| 버그 재현 방법을 만들고 싶다 | `debug-capture-failure` |
| 버그 원인을 찾고 싶다 | `debug-find-root-cause` |
| PR 머지 가능/보류 판단이 필요하다 | `review-change` |
| 9가지 품질 체크리스트가 필요하다 | `review-quality` |
| 실패 경로만 집중 확인하고 싶다 | `review-failure-paths` |
| 보안 취약점을 OWASP 기준으로 찾고 싶다 | `review-security` |
| 작업 완료 조건을 최종 확인하고 싶다 | `review-final-verify` |
| 테스트가 어디 없는지 찾고 싶다 | `test-find-gaps` |
| 실제 테스트를 작성하고 싶다 | `test-write-guards` |
| 왜 복잡한지 원인부터 파악하고 싶다 | `tidy-analyze` |
| 코드 변경 전 재사용/품질/효율 검토 | `tidy-review` |
| 복잡한 구조를 직접 줄이고 싶다 | `tidy-cut-fat` |
| 중복 코드를 찾고 싶다 | `tidy-find-copies` |
| 문서가 어디 뭐가 있는지 파악하고 싶다 | `doc-find-all` |
| 문서를 살릴지 정리할지 결정하고 싶다 | `doc-curate` |
| 문서를 새로 쓰고 싶다 | `doc-write` |
| 릴리즈 노트를 쓰고 싶다 | `doc-write-release-docs` |
| 배포해도 되는지 GO/NO-GO 판단하고 싶다 | `release-verdict` |
| 끝날 때까지 코드 작업을 자율 실행하고 싶다 | `control-build-until-done` |
| 품질 기준까지 반복 개선하고 싶다 | `control-improve-loop` |

---

## 공통 입력값 설명

거의 모든 스킬에서 반복적으로 나오는 입력값입니다.

| 입력키 | 한 줄 설명 | 예시 |
|--------|-----------|------|
| `GOAL` | 이번 작업으로 이루고 싶은 것 | `"로그인 후 세션이 유지되어야 한다"` |
| `SCOPE` | 작업 대상 범위 (파일, 폴더, 모듈) | `"src/auth"`, `"현재 diff"` |
| `DONE` | 완료 기준 — 무엇을 보면 끝난다고 할 수 있나 | `"테스트 전체 통과"` |
| `EXPECTED` | 기대하는 동작 | `"에러 없이 200 응답"` |
| `EVIDENCE` | 이미 알고 있는 근거 (로그, 테스트, 오류 메시지) | `"콘솔에 TypeError 출력됨"` |
| `CONTEXT` | 배경 정보 (대상 독자, 관련 동작 등) | `"React 초보 개발자 대상"` |
| `CONSTRAINTS` | 지켜야 할 제약 | `"기존 API 형식 유지"` |
| `FOCUS` | 특별히 집중할 영역 | `"보안 취약점만 보고 싶다"` |

---

## analyze-* vs review-* 차이

| | `analyze-*` | `review-*` |
|--|-------------|------------|
| **결론** | 없음 — 사실과 지도만 | 있음 — pass/fail, integrate/hold |
| **판정** | 없음 | 명시적 verdict 포함 |
| **언제** | 이해가 목적일 때 | 판단이 목적일 때 |
| **예시** | `analyze-structure`, `analyze-release-risk` | `review-change`, `review-security` |

---

더 자세한 내용은 각 카테고리 파일에서 확인하세요:
- [이해하기 (ask/clarify/analyze)](./SKILL-GUIDE-UNDERSTAND.md)
- [만들기 (plan/build/debug/test)](./SKILL-GUIDE-BUILD.md)
- [검증하기 (review/release/commit/control)](./SKILL-GUIDE-REVIEW.md)
- [정리하기 (tidy/doc)](./SKILL-GUIDE-MAINTAIN.md)
