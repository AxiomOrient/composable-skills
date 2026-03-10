# Response Profiles v1

## 목적

스킬별 응답 섹션 순서와 각 섹션 안에 뭘 써야 하는지를 고정한다.

## 선택 규칙

- 단독 실행: `response_profile`에 맞는 프로필을 사용한다.
- 합성 실행: 항상 generic 합성 템플릿을 사용한다.
- `profile_id`가 없거나 매핑 실패: `generic`을 사용한다.
- 프로필 섹션 순서의 단일 소스는 이 문서의 `Profile Map` 표다.
- `compose/scripts/parse_macro.py`는 이 표를 읽어 `PROFILE_REQUIRED_SECTIONS_MAP`을 만든다.
- 모든 프로필에 RESPONSE-CONTRACT-v1.md의 작성 규칙이 우선 적용된다.

---

## Profile Map

섹션 순서는 아래 표와 정확히 일치해야 한다.

| profile_id | 트리거 스킬 | 섹션 순서 |
|---|---|---|
| generic | compose / respond / release-publish / wf-ship-it / 모든 합성 실행 | 결과, 근거, 다음에 할 것, 질문 |
| analysis_report | scout-facts / build-until-done / finish-until-done / test-run-user-scenarios / debug-map-blast-radius / tidy-why-complex / ship-check-repo / ship-check-hygiene / wf-tidy-find-improvements | 결과, 핵심 발견, 옵션 비교, 근거, 다음에 할 것 |
| question_stack | ask-break-it-down / wf-ask-get-clear / wf-ask-sharpen | 결과, 문제 정의, 핵심 질문, 세부 질문, 다음에 할 것 |
| repair_report | ask-fix-prompt | 결과, 실패 유형, 왜 틀렸는지, 최소 질문 수정, 다음에 할 것 |
| self_verify_report | check-delivered | 결과, 막힌 것 또는 수정 필요 항목, 검증 근거, 남은 위험, 다음에 할 것(필요 시) |
| documentation_report | doc-write / doc-build-index / doc-publish-readme / doc-curate / doc-find-all | 결과, 프로젝트 개요, 아키텍처, 설치/실행, 사용 예시, 문서 경로, 근거 |
| clarify_question | scout-scope | 결과, 잠정 요구사항, 근거, 다음에 할 것, 확인 질문(맨 마지막) |
| brief_contract | plan-why-build-this | 결과, 브리프 요약, 대상 사용자와 문제, 성공 신호와 비목표, 열린 가정, 근거 |
| ia_contract | plan-screen-map | 결과, 구조 요약, 계층 구조, 탐색 경로와 흐름, 라벨링 메모, 근거 |
| spec_contract | plan-what-it-does | 결과, 스펙 요약, 완료 조건 체크리스트, 근거 |
| design_contract | plan-how-to-build | 결과, 설계 요약, 경계와 흐름, 결정과 트레이드오프, 위험과 검증, 근거 |
| planning_doc | plan-task-breakdown / scout-boundaries / plan-dependency-rules / plan-verify-order | 결과, 계획 요약, 할 일 목록, 문서 경로, 근거, 다음에 할 것 |
| implementation_delta | build-write-code / plan-driven-delivery / tidy-reorganize / tidy-cut-fat | 결과, 변경 사항, 영향 및 위험, 검증 결과, 다음에 할 것 |
| review_findings | check-ship-risk / check-merge-ready / check-quality-scan / tidy-find-magic-numbers / tidy-find-copies / check-module-walls / check-failure-paths / test-find-gaps / wf-check-full-review / wf-check-with-checklist | 결과, 발견된 문제, 테스트가 부족한 부분, 판정, 다음에 할 것 |
| debug_report | debug-find-root-cause / wf-debug-this | 결과, 원인 분석, 수정 내용, 재발 방지, 다음에 할 것 |
| performance_report | build-make-faster / scout-baseline | 결과, 성능 수치 (전/후), 병목 분석 및 수정, 위험, 다음에 할 것 |
| test_report | test-write-guards / test-design-cases | 결과, 추가/수정 테스트, 커버리지 영향, 근거 |
| security_report | check-security-holes | 결과, 취약점 목록, 위험도, 대응 우선순위, 다음에 할 것(발견 시에만) |
| release_decision | ship-go-nogo / wf-ship-ready-check | 결과, 릴리즈 가능 여부와 이유, 위험 및 복구 방법, 승인 필요사항, 다음에 할 것(NO-GO 시에만) |
| commit_proposal | ship-commit | 결과, 커밋 타입/메시지, 대안, 근거 |
| external_verification | gemini | 결과, 외부 검증 결과, 신뢰도 및 한계, 근거, 다음에 할 것 |

---

## 프로필별 섹션 작성 지침

각 섹션 안에 뭘 써야 하는지를 설명한다. 섹션 이름은 위 표와 정확히 일치해야 한다.

---

### generic

**결과**: "무엇을 했고 결과가 어떤지" 1-2문장.

**근거**: 파일/명령/수치 — 이게 뭘 보여주는지.

---

### analysis_report (scout-facts / build-until-done / finish-until-done / test-run-user-scenarios / debug-map-blast-radius / tidy-why-complex)

**결과**: "어떤 분석을 했고 가장 중요한 발견이 뭔지" 1-2문장.

**핵심 발견**: 증거가 있는 것만 적는다. 형식:
> `**발견 이름** — 구체적 위치 — 왜 중요한가`

증거가 없으면 "확인 필요 — [검증 방법]"을 적는다.

**옵션 비교**: 선택지가 있을 때만 출력. 각 옵션: 장점 1개 / 단점 1개 / 권장 여부.

**근거**: 파일/명령/결과 — 이게 뭘 보여주는지.

**다음에 할 것**: 분석 결과로 해야 할 행동. 없으면 생략.

---

### question_stack (ask-break-it-down / wf-ask-get-clear / wf-ask-sharpen)

**결과**: "어떤 막연한 주제를 어떤 질문 형태로 좁혔는지" 1-2문장.

**문제 정의**: 지금 정말 물어야 하는 문제를 한 문장으로 적는다.

**핵심 질문**: 지금 먼저 던져야 하는 질문 1개를 코드 블록으로 적는다.

**세부 질문**: 핵심 질문을 받쳐 주는 3~5개의 작은 질문. 우선순위가 보이게 적는다.

**다음에 할 것**: 바로 이 질문을 묻거나, 필요하면 ask-flip-assumption 또는 ask-fix-prompt로 넘어가도록 안내한다.

---

### repair_report (ask-fix-prompt)

**결과**: "어떤 이유로 답이 약했고, 질문에서 무엇을 바꿨는지" 1-2문장.

**실패 유형**: 답이 나빴던 유형 분류. (너무 일반적 / 근거 없음 / 핵심 누락 / 모호한 기준 등)

**왜 틀렸는지**: 질문에서 어떤 부분이 약한 답을 유도했는지. "질문의 [부분]이 [어떻게] 잘못됐다"는 형태로.

**최소 질문 수정**: 바꾼 부분만. diff 형태로 보여주면 좋다.

**다음에 할 것**: 수정된 질문을 어디에 쓸지.

---

### self_verify_report (check-delivered)

**결과**: "검증 통과 여부 + 발견한 문제 개수" 1문장.

**막힌 것 또는 수정 필요 항목**: 아직 pass를 막는 항목. 없으면 "막힌 항목 없음."
각 항목: `**항목명** — 파일:라인 — 왜 막는지`

**검증 근거**: 어떤 명령/테스트/확인으로 검증했는지.

**남은 위험**: 아직 해결 안 된 것. 없으면 섹션 생략.

**다음에 할 것(필요 시)**: 남은 위험이 있을 때만. 없으면 생략.

---

### documentation_report (doc-write / doc-build-index / doc-publish-readme / doc-curate / doc-find-all)

**결과**: "어떤 문서를 만들거나 정리했는지" 1-2문장.

**프로젝트 개요**: 이 문서가 다루는 대상 요약. doc-write 스킬일 때 출력.

**아키텍처**: 구조 설명. 필요할 때만 출력. 없으면 생략.

**설치/실행**: 실행 방법. 필요할 때만 출력. 없으면 생략.

**사용 예시**: 예시 코드나 명령. 필요할 때만 출력. 없으면 생략.

**문서 경로**: 작성/변경된 파일 경로 목록.

**근거**: 어떤 소스를 참고했는지. doc-curate라면 어떤 문서를 정리했는지.

"다음에 할 것"은 후속 문서 작업이 명확할 때만 출력. 없으면 생략.

---

### clarify_question (scout-scope / ask-find-question)

**결과**: "어떤 요청을 정리 중이고, 아직 결정해야 할 것이 몇 개인지" 1-2문장.

**잠정 요구사항**: 지금까지 파악한 범위. 확실한 것과 불확실한 것을 구분.

**근거**: 어떤 정보를 바탕으로 위 요구사항을 정리했는지.

**다음에 할 것**: 보통 질문에 답하면 plan-task-breakdown으로 넘어간다고 안내.

**확인 질문(맨 마지막)**: 반드시 마지막에. 숫자 목록으로. 최대 5개.

---

### brief_contract (plan-why-build-this)

**결과**: "어떤 문제를 누구를 위해 풀려는지" 1-2문장.

**브리프 요약**: 문제, 대상 사용자, 핵심 결과를 짧게 적는다.

**대상 사용자와 문제**: 사용자별로 어떤 상황에서 어떤 불편이나 진전 욕구가 있는지.

**성공 신호와 비목표**: 무엇이 좋아지면 성공인지, 무엇은 이번에 안 하는지.

**열린 가정**: 아직 검증되지 않은 전제. 없으면 생략.

**근거**: 어떤 자료나 입력을 바탕으로 위 브리프를 만들었는지.

---

### ia_contract (plan-screen-map)

**결과**: "어떤 구조를 만들었고 왜 그렇게 묶었는지" 1-2문장.

**구조 요약**: 전체 계층과 핵심 진입점 요약.

**계층 구조**: 상위-하위 노드 관계를 바로 이해할 수 있게 적는다.

**탐색 경로와 흐름**: 사용자가 어디서 들어와 어디로 이동하는지, 핵심 흐름이 어떻게 이어지는지.

**라벨링 메모**: 용어, 메뉴명, 섹션명이 왜 그렇게 정해졌는지.

**근거**: 어떤 사용자 목표, 콘텐츠, 제약을 기준으로 구조를 만들었는지.

---

### spec_contract (plan-what-it-does)

**결과**: "어떤 기능 스펙을 작성했고 핵심 범위와 제약이 뭔지" 1-2문장.

**스펙 요약**: 사용자 결과, 범위, 핵심 요구사항과 비요구사항.

**완료 조건 체크리스트**: 체크박스 형태. 각 항목은 "테스트로 확인 가능한" 조건이어야 한다.

**근거**: 어떤 정보를 바탕으로 스펙을 작성했는지.

---

### design_contract (plan-how-to-build)

**결과**: "어떤 기술 설계를 잡았고 가장 중요한 설계 선택이 뭔지" 1-2문장.

**설계 요약**: 전체 메커니즘과 중심 trade-off를 짧게 적는다.

**경계와 흐름**: 어떤 컴포넌트가 무엇을 맡고, 데이터나 제어가 어떻게 흐르는지.

**결정과 트레이드오프**: 어떤 선택을 했고 무엇을 포기하거나 보호했는지.

**위험과 검증**: 가장 큰 위험과 그 위험을 줄일 확인 방법.

**근거**: 어떤 상위 요구사항, 제약, 기존 구조를 기준으로 설계했는지.

---

### planning_doc (plan-task-breakdown / scout-boundaries / plan-dependency-rules / plan-verify-order)

**결과**: "어떤 계획을 만들었고 단계가 몇 개인지" 1-2문장.

**계획 요약**: 전체 흐름을 3-5단계로. 각 단계의 목적.

**할 일 목록**: 행동 텍스트만. 이번에 바로 시작할 수 있는 것 우선.
각 항목: `[동사로 시작] — 왜 필요한지`

**문서 경로**: 계획 문서가 저장된 위치.

**근거**: 계획을 세울 때 참고한 정보.

**다음에 할 것**: 보통 plan-driven-delivery + build-write-code로 넘어간다고 안내.

---

### implementation_delta (build-write-code / plan-driven-delivery / tidy-reorganize / tidy-cut-fat)

**결과**: "무엇을 구현/변경했고 검증이 통과했는지" 1-2문장.

**변경 사항**: 파일별로 무엇을 바꿨는지. 왜 그렇게 바꿨는지 한 줄씩.
형식: `파일:라인 — 무엇을 → 어떻게 — 왜`

**영향 및 위험**: 이 변경으로 영향받는 부분. 위험이 없으면 "영향 없음."

**검증 결과**: 어떤 테스트/명령으로 확인했는지 + 결과. 실패하면 실패 내용.

**다음에 할 것**: 후속 작업이 있으면. 없으면 생략.

---

### review_findings (check-ship-risk / check-merge-ready / check-quality-scan / tidy-find-magic-numbers / tidy-find-copies / check-module-walls / check-failure-paths / test-find-gaps / wf-check-full-review / wf-check-with-checklist)

**결과**: "몇 개를 점검해서 몇 개 문제를 찾았고, 가장 중요한 게 뭔지" 1-2문장.

**발견된 문제**: 각 항목은 아래 형태로:
> `**문제 이름** — 파일:라인 — 왜 문제인가 (영향)`

없으면 "이 범위에서 문제를 찾지 못했다."

**테스트가 부족한 부분**: 테스트가 없거나 약한 시나리오. 없으면 생략.

**판정**: PASS / HOLD / FAIL + 한 줄 이유.

**다음에 할 것**: 고쳐야 할 순서. 없으면 생략.

---

### debug_report (debug-find-root-cause / wf-debug-this)

**결과**: "어떤 버그를 잡았고 원인이 뭔지" 1-2문장.

**원인 분석**: 어디서 왜 터졌는지. 파일:라인 포함.
형식: `파일:라인 — 왜 여기서 터지는지 — 어떤 조건에서`

**수정 내용**: 무엇을 어떻게 바꿨는지. 파일:라인 포함.

**재발 방지**: 추가한 테스트나 가드. 없으면 "테스트 추가 권장 — [구체적 시나리오]".

**다음에 할 것**: 관련 코드 더 봐야 하면. 없으면 생략.

---

### performance_report (build-make-faster / scout-baseline)

**결과**: "어떤 지표를 개선했고 얼마나 좋아졌는지" 1-2문장.

**성능 수치 (전/후)**: 기준 수치와 개선 후 수치. 같은 측정 방법으로 비교. 수치 없으면 "측정 필요".

**병목 분석 및 수정**: 어디가 느렸고 어떻게 고쳤는지.

**위험**: 이 최적화가 가져올 수 있는 부작용. 없으면 "없음".

**다음에 할 것**: 더 봐야 할 병목이 있으면. 없으면 생략.

---

### test_report (test-write-guards / test-design-cases)

**결과**: "어떤 테스트를 설계하거나 추가했고, 어떤 행동을 보호하는지" 1-2문장.

**추가/수정 테스트**: `test-design-cases`면 설계한 케이스, `test-write-guards`면 실제로 추가/수정한 테스트를 적는다. 왜 이 케이스를 골랐는지 함께 적는다.

**커버리지 영향**: 수치가 있으면 전/후 커버리지, 없으면 어떤 행동 범위를 새로 보호하게 됐는지 적는다.

**근거**: 어떤 실패 시나리오나 엣지 케이스를 기준으로 만들었는지.

---

### security_report (check-security-holes)

**결과**: "몇 개를 점검해서 취약점이 몇 개인지, 가장 위험한 게 뭔지" 1-2문장.

**취약점 목록**: 각 항목:
> `**이름** — 파일/엔드포인트 — 공격 시나리오 — 위험도 (높음/중간/낮음)`

없으면 "취약점을 찾지 못했다."

**위험도**: 전체 위험 수준 평가. 근거 포함.

**대응 우선순위**: 위험도 높은 것부터 번호 목록으로.

**다음에 할 것(발견 시에만)**: 발견이 있을 때만 출력.

---

### release_decision (ship-go-nogo / wf-ship-ready-check)

**결과**: "GO 또는 NO-GO + 핵심 이유" 1-2문장.

**릴리즈 가능 여부와 이유**: GO면 통과 근거. NO-GO면 블로커 목록.

**위험 및 복구 방법**: 배포 시 예상 위험 + 롤백 방법. "롤백 시간: X분" 포함.

**승인 필요사항**: 배포 전 사람이 확인해야 할 것. 없으면 "없음".

**다음에 할 것(NO-GO 시에만)**: NO-GO일 때만. 블로커 해결 순서.

---

### commit_proposal (ship-commit)

**결과**: "어떤 변경에 대한 커밋 메시지 후보인지" 1-2문장.

**커밋 타입/메시지**: 타입, 스코프, 제목을 코드 블록으로. 본문이 필요하면 포함.

**대안**: 다른 메시지 스타일 1-2개.

**근거**: 이 메시지를 선택한 이유.

---

### external_verification (gemini)

**결과**: "외부 검증 결과와 내부와 일치 여부" 1-2문장.

**외부 검증 결과**: Gemini가 뭐라고 했는지.

**신뢰도 및 한계**: 이 결과를 얼마나 믿을 수 있는지. 부족한 부분.

**근거**: 어떤 입력으로 Gemini를 호출했는지.

**다음에 할 것**: 결과를 어떻게 활용할지.

---

## 공통 규칙

- 첫 문장: 결론을 먼저 말한다.
- 한 문장에는 한 가지 주장만 넣는다.
- 내부 용어(`LEAKED_ASSUMPTION`, `HARDENING_ACTION`, `KEY_FINDING`, `stage payload` 등)를 쓰지 않는다.
- 파일 이름, 라인 번호, 수치를 쓴다. "문제가 있다"가 아니라 "파일:라인에서 뭐가 왜 문제다"처럼 쓴다.
- 근거가 없으면 추측하지 말고 "확인 필요 — [방법]"을 적는다.
- 문제가 없으면 억지로 만들지 말고 "문제 없음"이라고 적는다.
- 질문이 있으면 항상 응답 최하단 "질문" 섹션에만 적는다.
- commit, release GO는 "다음에 할 것" 생략.
- doc-write, test-write-guards, test-design-cases, plan-what-it-does는 산출물 자체가 결과이므로 "다음에 할 것" 불필요하면 생략.
