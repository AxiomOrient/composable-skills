# Skill Interaction Matrix v1

## 목적

각 스킬이 언제 질문/블로커를 남겨야 하는지와 어떤 `response_profile`을 써야 하는지 고정한다.

## 규칙

- 질문이나 blocker는 개별 스킬이 바로 출력하지 않고 payload로 축적한다.
- 직접 질문이 필요하면 최종 응답 맨 마지막에만 노출한다.
- canonical workflow 이름은 `wf-*`다.
- 단독 실행은 skill/workflow의 mapped `response_profile`을 따른다.
- 합성 실행(스킬 2개 이상)은 항상 `generic`을 따른다.
- matrix/profile 로딩이 실패하거나 매핑이 없으면 final fallback은 `generic`이다.

## 스킬별 기준

| Skill | 1차 기능 | Payload 축적 필요 시점 | response_profile | 필수 결과물 |
|---|---|---|---|---|
| compose | 합성/정규화 | 입력 모호, 구조 오류, blocker 발생 시 | generic | 정규화 PROGRAM + orchestration state |
| respond | 최종 답변 렌더링 | 없음 | generic | 최종 사용자 응답 |
| release-publish | 릴리즈 실행/게시 | 검증 실패, branch policy 불만족, publish host 실패 시 | generic | cleanup report + release refs + publish status |
| scout-facts | 원인/옵션 분석 | 가설 검증 데이터 부족 시 | analysis_report | 분석 리포트 |
| build-until-done | 완료 계약 반복 판정 | 완료 조건 증거 부족 또는 다음 패스 필요 시 | analysis_report | completion status + next smallest pass |
| finish-until-done | 범용 완료 계약 반복 판정 | 비코드 작업의 완료 조건 증거 부족 또는 다음 패스 필요 시 | analysis_report | completion status + next smallest pass |
| test-run-user-scenarios | 실제 사용자 시나리오 시험 | realistic use-case 근거 부족 시 | analysis_report | use-case matrix + execution log + usability findings |
| debug-map-blast-radius | 실패 표면 축소 | 재현 조건/경계 부족 시 | analysis_report | 재현 범위 + 영향 경로 + 디버그 진입점 |
| tidy-why-complex | 복잡도 재고 | 구조 근거 부족 시 | analysis_report | essential vs accidental complexity map |
| scout-scope | 요구사항 명확화 | 목표/범위/종료조건 미정 시 | clarify_question | 질문 목록 + 초안 scope contract |
| ask-find-question | 막연한 질문 선명화 | 원 질문/제약이 흐릴 때 | clarify_question | fog keys + problem statement |
| ask-break-it-down | 핵심 질문 분해 | problem statement가 아직 너무 넓을 때 | question_stack | question-stack.v1 |
| ask-flip-assumption | 가정 반전 질문 생성 | 기본 가정/관점이 고착돼 있을 때 | analysis_report | ask-flip-assumption.v1 |
| ask-fix-prompt | 실패 답변 기준 질문 수리 | 실패 답변/원 질문 부족 시 | repair_report | repair-playbook.v2 |
| plan-task-breakdown | 구현 계획 수립 | 목표/제약/완료조건 미정 시 | planning_doc | 구현 계획 + task 목록 |
| plan-why-build-this | 문제/사용자/성과 브리프 작성 | 사용자, 문제, 성공 신호가 흐릴 때 | brief_contract | brief summary + user jobs + non-goals |
| plan-screen-map | 구조/탐색/흐름 설계 | 사용자 흐름, 계층 구조, 진입점 근거 부족 시 | ia_contract | hierarchy map + navigation paths + core flows |
| scout-boundaries | 범위 계약 고정 | scope/done 근거 부족 시 | planning_doc | goal + in/out scope + done condition |
| plan-dependency-rules | 의존성 규칙 계획 | 경계/의존성 근거 부족 시 | planning_doc | allowed/forbidden dependencies + transition |
| plan-verify-order | 검증 경로 계획 | verification 근거 부족 시 | planning_doc | checks + stop conditions |
| build-write-code | 코드 구현 | 계획/검증 근거 누락 시 | implementation_delta | 코드 변경 + 검증 근거 |
| plan-driven-delivery | 계획-구현 동기화 | TASK-ID/증거 누락 시 | implementation_delta | 동기화된 plan/task 상태 |
| tidy-reorganize | 구조 개선 계획/변경 | behavior invariants 불명확 시 | implementation_delta | 구조 변경 또는 구조 계획 |
| tidy-cut-fat | 단순화 재구성 | 단순화 근거 부족 시 | implementation_delta | complexity inventory + simplification plan |
| build-make-faster | 성능 최적화 | baseline/metric 누락 시 | performance_report | 전후 수치 + 병목 근거 |
| scout-baseline | 성능 baseline 확보 | metric/budget 근거 부족 시 | performance_report | metric definition + baseline + budget |
| test-write-guards | 테스트 가드 구현 | 대상 시나리오 불명확 시 | test_report | 테스트 케이스/코드 |
| test-design-cases | 테스트 케이스 설계 | scenario 근거 부족 시 | test_report | happy/edge/failure matrix |
| tidy-find-magic-numbers | 상수/공통화 후보 탐지 | 범위/의미 근거 부족 시 | review_findings | constant-extraction-report.v1 |
| tidy-find-copies | 중복 군집 탐지 | 비교 범위 부족 시 | review_findings | duplication-report.v1 |
| check-module-walls | 경계 계약 점검 | 인터페이스/경계 근거 부족 시 | review_findings | boundary-contract-report.v1 |
| check-failure-paths | 실패 경로 검토 | failure mode 근거 부족 시 | review_findings | check-failure-paths.v1 |
| test-find-gaps | 테스트 공백 점검 | 테스트 근거 부족 시 | review_findings | test-gap-report.v1 |
| check-merge-ready | 리뷰 판정 | 판정 근거 부족 시 | review_findings | findings + testing gaps + verdict |
| check-ship-risk | gate/배포 위험 판단 | gate 근거 부족 시 | review_findings | findings + gate recommendation |
| check-quality-scan | 9항목 checklist 점검 | 항목별 증거 부족 시 | review_findings | checklist table + findings + residual risk |
| check-security-holes | 보안 점검 | 자산/위협 범위 불명확 시 | security_report | threat model + prioritized findings |
| ship-check-repo | 릴리즈용 git/repo 현실 점검 | git root, branch, remote, tag 상태 부족 시 | analysis_report | repo facts + branch map + blockers |
| ship-check-hygiene | 릴리즈 hygiene/docs/surface 점검 | docs gate, legacy cleanup, public surface 근거 부족 시 | analysis_report | hygiene findings + docs gate + cleanup list |
| ship-go-nogo | 릴리즈 GO/NO-GO 판단 | 승인/롤백 정보 부족 시 | release_decision | release decision + rollback readiness |
| check-delivered | 최종 검증 | 근거/동기화 불충분 시 | self_verify_report | verification status + residuals |
| doc-write | 문서 생성/갱신 | 근거/대상 독자 부족 시 | documentation_report | docs + evidence map |
| doc-build-index | 계층형 분석 문서 + 인덱스 작성 | 범위/증거/레이아웃 부족 시 | documentation_report | analysis docs + local indexes + guide index |
| doc-publish-readme | 루트 README + 다국어 게시 | 언어 범위/소스 문서 부족 시 | documentation_report | root README + language portal |
| doc-curate | 비-루트 문서 구조/인덱싱/정리 | 문서 분류 근거 부족 시 | documentation_report | inventory + entry structure + navigation map + cleanup actions |
| doc-find-all | 문서 인벤토리 스캔 | 문서 상태 근거 부족 시 | documentation_report | doc inventory + orphan/duplicate set |
| plan-what-it-does | 기능 스펙 정의 | required behavior, acceptance, edge case가 모호할 때 | spec_contract | feature spec |
| plan-how-to-build | 기술 설계 문서화 | boundary, data/control flow, trade-off 근거 부족 시 | design_contract | technical design doc |
| ship-commit | 커밋 메시지/전략 | 커밋 의도 불명확 시 | commit_proposal | commit proposal |
| wf-ask-get-clear | 문제 정의 + 질문 스택 workflow | 토픽 입력 부족 시 | question_stack | ask-find-question.v1 + question-stack.v1 |
| wf-ask-sharpen | 질문 준비 완료 workflow | 토픽/제약 입력 부족 시 | question_stack | ask-find-question.v1 + question-stack.v1 + ask-flip-assumption.v1 |
| wf-check-full-review | 프로젝트 리뷰 workflow | 범위/리뷰 포커스 부족 시 | review_findings | subcheck 기반 리뷰 결과 |
| wf-check-with-checklist | 프로젝트 체크리스트 리뷰 workflow | 범위/리뷰 포커스 부족 시 | review_findings | subcheck review + checklist table |
| wf-debug-this | 프로젝트 디버그 workflow | 실패 증상/기대 동작 부족 시 | debug_report | surface map + debug report + test gaps |
| wf-tidy-find-improvements | 프로젝트 개선 맵 workflow | 범위/개선 목표 부족 시 | analysis_report | improvement report |
| wf-ship-ready-check | 릴리즈 검토 workflow | branch role, docs gate, rollout/rollback 정보 부족 시 | release_decision | repo check + hygiene check + release decision |
| wf-ship-it | 릴리즈 실행 workflow | branch role, checks, tag policy, publish intent 정보 부족 시 | generic | release review + publish refs + publish status |
| gemini | 외부 검증 호출 | 명시 호출/세션 정보 부족 시 | external_verification | Gemini 요약 + local comparison |
