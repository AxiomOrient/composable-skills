# Skill Boundaries (MECE) v1

## Goal
스킬 하나 = 기능 하나 원칙을 강제한다. 아래 경계를 위반하는 스킬 합성은 금지한다.

## Core Boundaries

### 분석 계열
- `scout-facts`: 원인/옵션 분석 보고서만 작성. 코드 수정/계획 확정/리뷰 판정 금지.
- `debug-find-root-cause`: 구체적 버그의 RCA + 최소 수정만 수행. 신규 기능 구현/광범위 분석 보고서 금지. 막연한 의심은 `scout-facts` 먼저.
- `scout-scope`: 요구사항 명확화 + 초안 스펙 작성만 수행. 코드 구현/계획 문서 확정/리뷰 판정 금지.

### 설계/계획 계열
- `plan-task-breakdown`: 구현 계획 문서 작성/갱신만 수행. 코드 수정/리뷰 판정 금지.
- `plan-what-it-does`: 구현 스펙/RFC/ADR 작성만 수행. 직접 코딩/버그 수정/저장소 행동 분석 금지.
- `tidy-cut-fat`: 복잡도 축소 계획/재구성만 수행. 신규 기능 구현/사고 대응 금지.
- `tidy-reorganize`: 행동 보존형 구조 개선 계획만 수행. 신규 기능 추가/사고 대응/전체 복잡도 재구성(`tidy-cut-fat`) 금지.

### 구현 계열
- `build-write-code`: 코드 구현 + 검증 근거 산출만 수행. plan/tasks 동기화/리뷰 판정 금지.
- `build-make-faster`: 측정 기반 성능 최적화만 수행. 측정 없는 최적화/기능 구현/리뷰 판정 금지.
- `test-write-guards`: 회귀 방지 테스트 설계/추가만 수행. 기능 구현/버그 직접 수정/리뷰 판정 금지.

### 테스트 경계
- `test-design-cases`: 테스트 케이스 설계만 수행. 프레임워크 선택, mock 전략, 실제 테스트 코드 작성 금지.
- `test-find-gaps`: 현재 테스트 공백 분석만 수행. coverage 숫자만으로 gap 선언 금지. 실제 테스트 코드 작성 금지.
- `test-write-guards`: 의미 있는 테스트 코드 구현과 실행 증거만 수행. CI 통과용 저가치 테스트, 구현 디테일 고정 테스트, 중복 테스트 금지.
- `test-run-user-scenarios`: 실제 사용자/에이전트 시나리오 생성과 실행만 수행. happy/failure/weird case를 포함해야 하며, 실제 관찰 없이 pass 판정 금지.
- `check-delivered`: 최종 계약 검증만 수행. 테스트 설계 대체, 테스트 공백 분석 대체, 임의 coverage 취향으로 fail 판정 금지.

### 검토/품질 계열
- `check-ship-risk`: 코드 리뷰 판정만 수행. 코드 수정/새 계획 수립 금지.
- `check-merge-ready`: 코드 리뷰 판정/통합 판단만 수행. 코드 수정/새 계획 수립 금지.
- `check-quality-scan`: 9항목 체크리스트 점검만 수행. 단독으로 최종 통합 판단 대체 금지.
- `check-security-holes`: 보안 감사/취약점 분류만 수행. 보안 패치 직접 적용/기능 구현 금지.
- `check-delivered`: 최종 검증과 누락 교정만 수행. 신규 요구사항 확장 금지.

### 문서화 계열
- `doc-write`: 문서(README/아키텍처/사용 가이드)만 작성/갱신. 런타임 코드 수정/리뷰 판정/구현 계획 확정 금지.
- `doc-curate`: 문서 인덱싱/링크 구조/오래된 문서 정리 계획만 수행. 런타임 코드 수정 금지.

### 릴리즈/종료 계열
- `ship-check-repo`: 릴리즈 가능한 git/repo 현실 확인만 수행. GO/NO-GO 판정/배포 실행 금지.
- `ship-check-hygiene`: 문서/레거시/public surface hygiene 점검만 수행. 브랜치 변경/배포 실행 금지.
- `ship-go-nogo`: 릴리즈 안전성 점검/판정만 수행. 코드 수정/계획 수립/배포 실행 금지.
- `release-publish`: 검증된 변경의 release commit/tag/publish만 수행. GO/NO-GO 판정 대체 금지.
- `ship-commit`: 커밋 메시지 후보 생성만 수행. 구현/디버깅/리뷰 판정 금지. 파이프라인의 마지막 스킬로만 사용.

### 오케스트레이션/라우팅 계열
- `compose`: 매크로 파싱 + 파이프라인 오케스트레이션만 수행. 직접 분석/구현/리뷰 수행 금지. 반드시 다른 스킬과 결합.
- `plan-driven-delivery`: 기존 계획/태스크와 구현 증거의 동기화만 수행. 새 계획 작성은 금지. `plan-task-breakdown`를 대체하지 않는다.
- `gemini`: 사용자가 명시 호출한 외부 Gemini 실행/요약만 수행. 암묵 실행 금지.
- `respond`: 최종 사용자 응답 포맷팅만 수행. 분석/구현/리뷰 수행 금지.

## Planning-Implementation Contract
- 계획 산출물은 markdown 원본으로 유지:
  - `docs/IMPLEMENTATION-PLAN.md`
  - `docs/TASKS.md`
- 구현은 반드시 위 문서를 읽고 갱신한다.
- 실행 동기화는 `plan-driven-delivery`가 담당하고, 계획 생성은 `plan-task-breakdown`가 담당한다.

## Routing Rule
다중 의도가 들어오면 다음 우선순위로 분해한다. 각 역할은 하나의 스킬에만 배정한다:

1. `scout-scope` — 요구사항 불명확 시
2. `scout-facts` — 원인/옵션 분석
3. `debug-find-root-cause` — 구체적 버그 RCA
4. `doc-write` — 문서 본문 작성
5. `doc-curate` — 문서 인덱싱/정리
6. `plan-what-it-does` — 스펙/RFC 작성
7. `plan-task-breakdown` — 구현 계획 수립
8. `tidy-cut-fat` — 복잡도 재구성 계획
9. `tidy-reorganize` — 구조 개선 계획
10. `build-write-code` — 코드 구현
11. `build-make-faster` — 성능 최적화
12. `test-write-guards` — 테스트 추가
13. `check-security-holes` — 보안 감사
14. `ship-check-repo` / `ship-check-hygiene` / `ship-go-nogo` / `wf-ship-ready-check` — 릴리즈 검토
15. `check-ship-risk` — 코드 리뷰 판정
16. `check-merge-ready` — 코드 리뷰 판정/통합 판단
17. `check-quality-scan` — 체크리스트 기반 품질 점검
18. `release-publish` / `wf-ship-it` — 릴리즈 실행/게시
19. `check-delivered` — 최종 검증
20. `respond` — 응답 렌더링
