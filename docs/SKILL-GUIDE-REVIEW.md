# 검증하기 — review / release / commit / control 스킬 가이드

> 이 파일은 [Atomic Skills 가이드](./ATOMIC-SKILLS-GUIDE.md)의 일부입니다.

---

## 이 파일의 스킬

| 카테고리 | 스킬 | 한 줄 설명 |
|----------|------|-----------|
| review | `review-change` | 변경 사항을 리뷰하고 병합 가능/보류 판단을 냅니다 |
| review | `review-quality` | 9가지 품질 항목으로 코드를 체계적으로 검사합니다 |
| review | `review-failure-paths` | 실패 경로와 예외 처리만 집중해서 점검합니다 |
| review | `review-security` | OWASP 기준으로 보안 취약점을 찾습니다 |
| review | `review-final-verify` | 작업 완료 조건이 정말 다 됐는지 최종 확인합니다 |
| release | `release-check-repo` | 배포 전 저장소 상태와 브랜치를 확인합니다 |
| release | `release-check-hygiene` | 낡은 파일과 문서 불일치를 배포 전에 점검합니다 |
| release | `release-verdict` | 배포 GO / NO-GO 최종 판단을 내립니다 |
| commit | `commit-write-message` | Conventional Commit 형식의 메시지 후보를 만듭니다 |
| control | `control-build-until-done` | 코드 작업을 끝날 때까지 자율 루프로 실행합니다 |
| control | `control-finish-until-done` | 문서·리뷰·계획 작업을 끝날 때까지 자율 루프로 실행합니다 |
| control | `control-improve-loop` | 품질 기준에 도달할 때까지 반복 개선합니다 |

---

## review — 판정을 내리는 리뷰 스킬

> **판단 없는 분석은 `analyze-*`에서** 합니다.
> `review-*`는 **pass/fail, integrate/hold** 같은 명시적 결론을 냅니다.

### 어떤 review 스킬을 써야 하나?

| 상황 | 쓸 스킬 |
|------|---------|
| PR 머지 가능/보류 판단이 필요하다 | `review-change` |
| 9가지 품질 체크리스트로 검사하고 싶다 | `review-quality` |
| 에러 처리와 실패 경로만 집중 확인하고 싶다 | `review-failure-paths` |
| 보안 취약점을 OWASP 기준으로 찾고 싶다 | `review-security` |
| 작업 완료 조건이 정말 다 됐는지 최종 확인하고 싶다 | `review-final-verify` |
| 품질 기준에 도달할 때까지 반복 개선하고 싶다 | `control-improve-loop` |

---

### `review-change` — PR/코드 리뷰하기

**한 줄 설명:** 변경 사항을 우선순위와 근거와 함께 리뷰하고 병합 가능/보류 판단을 내립니다.

**언제 써요?**
- PR 리뷰가 필요할 때
- "이 코드 머지해도 되나?" 확인할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `REVIEW_GOAL` | ✅ | 리뷰 목적 (`general-verdict` / `regression-risk` / `change-intent-check` / `narrow-focus`) |
| `TARGET_SCOPE` | ✅ | 리뷰할 범위 (`diff` / `file` / `module` / `folder`) |
| `CHANGE_INTENT` | ✅ | 이 변경의 목적 |
| `KNOWN_TEST_SIGNAL` | 선택 | 테스트 현황 (통과/실패/없음) |
| `CONSTRAINTS` | 선택 | 특별히 집중할 영역 (보안만, 성능만 등) |

**예제**

```
$review-change
REVIEW_GOAL: general-verdict
TARGET_SCOPE: diff
CHANGE_INTENT: 결제 서비스를 PG사 A에서 B로 교체
KNOWN_TEST_SIGNAL: 단위테스트 통과, E2E 테스트 미실행
```

---

### `review-quality` — 9가지 품질 항목 체크

**한 줄 설명:** 미리 정해진 9가지 품질 항목으로 코드를 체계적으로 검사하고 pass/fail 판정을 냅니다.

**언제 써요?**
- "코드 품질 전반을 훑고 싶다"
- 릴리즈 전 품질 체크리스트가 필요할 때

**9가지 항목:** 정확성, 명확성, 단순성, 경계 존중, 에러 처리, 보안, 테스트 가능성, 성능, 목표 정합성

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `SCOPE` | ✅ | 검사할 범위 |
| `GOAL` | ✅ | 이 코드의 의도 (무엇을 하는 코드인지) |
| `FOCUS_ITEMS` | 선택 | 집중할 항목 번호 (1-9, 생략 시 전체) |
| `EVIDENCE` | 선택 | 테스트 결과, 벤치마크 등 참고 정보 |

**예제**

```
$review-quality
SCOPE: src/payment/
GOAL: 결제 처리 로직
FOCUS_ITEMS: [3, 5, 6]
```

---

### `review-failure-paths` — 실패 경로만 집중 점검

**한 줄 설명:** 정상 동작이 아닌 실패 시 처리 — 예외 처리, 복구 로직 — 만 집중해서 보고 clean/needs-fix 판정을 냅니다.

**언제 써요?**
- "에러가 났을 때 제대로 처리하고 있나?"
- 예외 처리가 충분한지 확인할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 점검할 범위 |
| `FAILURE_FOCUS` | 선택 | 집중 유형 (`exceptions` / `fallbacks` / `recovery` / `all`) |
| `FAILURE_MODES` | 선택 | 특히 집중할 실패 모드 목록 |

**예제**

```
$review-failure-paths
TARGET_SCOPE: src/payment/
FAILURE_FOCUS: exceptions
FAILURE_MODES:
  - 결제 API 타임아웃
  - 중복 결제 요청
  - 잔액 부족
```

---

### `review-security` — 보안 취약점 점검

**한 줄 설명:** OWASP 기준으로 비밀 정보 노출, 취약한 인증, 보안 구멍을 찾고 safe/at-risk/blocked 판정을 냅니다.

**언제 써요?**
- 배포 전 보안 점검
- "비밀키가 코드에 들어간 것 같다"
- 인증 로직이 안전한지 확인할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `SECURITY_GOAL` | ✅ | 목적 (`audit` / `repo-exposure-review` / `threat-model` / `mitigation-verify`) |
| `TARGET_SCOPE` | ✅ | 점검할 범위 |
| `REVIEW_STAGE` | 선택 | 언제 하는 리뷰 (`github-commit` / `release` / `general`) |
| `SENSITIVE_SURFACES` | 선택 | 특히 집중할 민감 영역 |
| `KNOWN_EVIDENCE` | 선택 | 기존 스캔 결과, 알려진 취약점 |

**예제**

```
$review-security
SECURITY_GOAL: repo-exposure-review
TARGET_SCOPE: ./
REVIEW_STAGE: github-commit
SENSITIVE_SURFACES:
  - .env 파일
  - config/ 폴더
  - API 키 사용 부분
```

---

### `review-final-verify` — 작업 완료 최종 확인

**한 줄 설명:** 작업이 끝난 후 약속했던 완료 조건이 정말 다 됐는지 마지막으로 확인하고 통과/보류 판정을 냅니다.

**언제 써요?**
- "다 했다고 생각하는데 정말 다 됐는지 확인하고 싶다"
- 결과물을 전달하기 전 최종 검증

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `VERIFY_TARGETS` | ✅ | 확인할 파일, 문서, 결과물 목록 |
| `DONE_CRITERIA` | ✅ | 반드시 만족해야 할 완료 조건 목록 |
| `VERIFY_SCOPE` | ✅ | 확인 범위 (`diff` / `docs` / `path-set`) |
| `KNOWN_EVIDENCE` | 선택 | 이미 확인한 근거 (테스트 결과 등) |

**예제**

```
$review-final-verify
VERIFY_TARGETS:
  - src/auth/session.ts
  - docs/auth.md
DONE_CRITERIA:
  - 세션 갱신 테스트 통과
  - 문서에 갱신 흐름 설명 포함
VERIFY_SCOPE: path-set
```

---

## release — 배포를 준비하는 스킬

> "코드가 돌아간다"를 넘어서 **내보내도 되는가**를 판단합니다.
> 순서: `release-check-repo` → `release-check-hygiene` → `release-verdict`

---

### `release-check-repo` — 저장소 상태 확인

**한 줄 설명:** 이 저장소가 배포 가능한 git 상태인지, 브랜치와 원격 저장소가 올바른지 확인합니다.

**언제 써요?**
- 배포 작업을 시작하기 전에 저장소 상태를 먼저 검증할 때
- 브랜치, 원격 저장소, 태그 충돌 여부를 확인할 때
- "배포 대상이 맞는 저장소인지" 먼저 확인하고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_BRANCHES` | ✅ | 배포에 관련된 브랜치 목록 |
| `REMOTE_NAME` | 선택 | 원격 저장소 이름 (기본: `origin`) |
| `TAG_INTENT` | 선택 | 사용할 버전 태그 후보 |
| `REPO_EXPECTATIONS` | 선택 | 추가 확인 조건 (워킹트리 클린 등) |

**예제**

```
$release-check-repo
TARGET_BRANCHES: [main, develop]
TAG_INTENT: v2.1.0
```

---

### `release-check-hygiene` — 배포 위생 점검

**한 줄 설명:** 낡은 파일이 남아있지 않은지, 문서와 공개 표면이 어긋나지 않는지 확인합니다.

**언제 써요?**
- 배포 전에 지워야 할 임시 파일이나 계획 문서가 남아있는지 확인할 때
- README, CHANGELOG 등 필수 문서가 최신 상태인지 검증할 때
- 스킬 메타데이터와 공개 문서가 일치하는지 확인할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `HYGIENE_SCOPE` | ✅ | 점검 범위 (`diff` / `repo`) |
| `REQUIRED_DOCS` | 선택 | 배포 전 반드시 있어야 할 문서 목록 |
| `SURFACE_CONTRACTS` | 선택 | 공개 표면 계약 (스킬 메타데이터 일치 등) |
| `LEGACY_PATTERNS` | 선택 | 배포 전에 사라져야 할 파일 패턴 |

**예제**

```
$release-check-hygiene
HYGIENE_SCOPE: repo
REQUIRED_DOCS: [README.md, CHANGELOG.md]
LEGACY_PATTERNS: [plans/, .DS_Store]
```

---

### `release-verdict` — GO / NO-GO 판단

**한 줄 설명:** 배포 범위, 롤아웃 방법, 롤백 준비를 보고 출시해도 되는지 최종 판단합니다.

**언제 써요?**
- `release-check-repo`와 `release-check-hygiene`을 마친 후 최종 배포 결정이 필요할 때
- 영향 범위와 롤백 방법을 점검하고 싶을 때
- "지금 배포해도 되나?" 판단 근거가 필요할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `RELEASE_SCOPE` | ✅ | 배포 범위 (`diff` / `repo` / `deployment-slice`) |
| `ROLLOUT_PLAN` | ✅ | 배포 계획 (어떻게 내보낼 것인지) |
| `ROLLBACK_PATH` | ✅ | 문제 생기면 어떻게 되돌릴지 |
| `KNOWN_GATES` | 선택 | 이미 통과한 테스트, 보안 점검 등 |

**예제**

```
$release-verdict
RELEASE_SCOPE: repo
ROLLOUT_PLAN: main 브랜치 태그 후 npm 퍼블리시
ROLLBACK_PATH: 이전 태그로 재배포 (npm publish v2.0.1)
KNOWN_GATES:
  - CI 전체 통과
  - 스테이징 검증 완료
```

---

## commit — 커밋 메시지를 만드는 스킬

---

### `commit-write-message` — 커밋 메시지 작성

**한 줄 설명:** 변경 내용을 기반으로 Conventional Commit 형식의 메시지 후보를 만듭니다.

**언제 써요?**
- "이 변경에 어울리는 커밋 메시지가 뭔지 모르겠다"
- 팀 커밋 규칙에 맞는 메시지가 필요할 때
- 구현이 끝난 후 커밋 메시지 후보를 3-5개 받고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `DIFF_SUMMARY` | ✅ | 변경 내용 요약 또는 실제 diff |
| `CHANGE_INTENT` | ✅ | 이 변경의 목적 |
| `SCOPE_HINT` | 선택 | 커밋 스코프 힌트 (예: `auth`, `payment`) |
| `BREAKING_CHANGE` | 선택 | 하위 호환성 깨짐 여부 (`yes` / `no` / `uncertain`) |

**예제**

```
$commit-write-message
DIFF_SUMMARY: session.ts에서 쿠키 만료 처리 수정 (line 45-67)
CHANGE_INTENT: 새로고침 후 세션이 사라지는 버그 수정
SCOPE_HINT: auth
BREAKING_CHANGE: no
```

**결과 예시:**
```
fix(auth): 새로고침 후 세션이 사라지는 버그 수정

쿠키 만료 시간 계산 방식이 잘못되어 페이지 새로고침 시
세션이 초기화되는 문제를 수정했습니다.
```

---

## control — 반복을 제어하는 스킬

> 끝날 때까지 **루프를 돌립니다**. DONE 조건이 충족되거나 실제 장애물이 생길 때까지.

### 어떤 control 스킬을 써야 하나?

| 상황 | 쓸 스킬 |
|------|---------|
| 코드 변경 작업을 끝까지 자율 실행하고 싶다 | `control-build-until-done` |
| 문서/리뷰/계획 작업을 끝까지 자율 실행하고 싶다 | `control-finish-until-done` |
| 품질 기준까지 반복 개선하고 싶다 | `control-improve-loop` |

---

### `control-build-until-done` — 코드 작업 자율 완료 루프

**한 줄 설명:** 코드 작업을 DONE 조건이 증명될 때까지 평가 → 구현 → 검증 → 반복으로 자율 실행합니다.

**언제 써요?**
- 계획 문서 없이 코드 작업을 끝까지 자율 실행하고 싶을 때
- DONE 조건은 명확하지만 구현 경로가 미리 다 정해지지 않았을 때
- 테스트가 실패하면 같은 루프 안에서 바로 디버그하고 재시도하고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `MISSION_GOAL` | ✅ | 실행할 하나의 코드 미션 |
| `TARGET_SCOPE` | ✅ | 건드릴 수 있는 범위 (경로, 모듈, 폴더, 저장소) |
| `DONE_CONDITION` | ✅ | 완료 조건 목록 — 외부에서 확인 가능한 조건만 유효 |
| `CURRENT_EVIDENCE` | 선택 | 이전 패스에서 얻은 관찰, 테스트 결과 등 |
| `MAX_PASSES` | 선택 | 한 턴에서 실행할 최대 패스 수 (기본값: 5) |
| `CONSTRAINTS` | 선택 | 범위 제한, 금지 사항 등 |

**예제**

```
$control-build-until-done
MISSION_GOAL: 브라우저 새로고침 후에도 세션이 유지되도록 수정
TARGET_SCOPE: src/auth
DONE_CONDITION:
  - 세션 갱신 테스트 통과
  - 새로고침 후 로그인 상태 유지 확인
```

---

### `control-finish-until-done` — 비코드 작업 자율 완료 루프

**한 줄 설명:** 문서, 리뷰, 계획 작업을 DONE 조건이 증명될 때까지 읽기 → 개선 → 검증 → 반복으로 자율 실행합니다.

**언제 써요?**
- 계획 문서 없이 문서 작성, 리뷰, 계획 정리를 끝까지 실행하고 싶을 때
- "작성됨"이 아니라 "읽는 사람이 쓸 수 있는 상태"까지 만들고 싶을 때
- 패스마다 새로운 빠진 부분을 발견하면 그 자리에서 이어서 처리하고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `MISSION_GOAL` | ✅ | 실행할 하나의 비코드 미션 |
| `TARGET_SCOPE` | ✅ | 건드릴 수 있는 범위 (경로, 문서, 폴더) |
| `DONE_CONDITION` | ✅ | 완료 조건 목록 — 읽는 사람이 확인할 수 있는 조건만 유효 |
| `CURRENT_EVIDENCE` | 선택 | 이전 패스에서 얻은 관찰, 리뷰 노트 등 |
| `MAX_PASSES` | 선택 | 한 턴에서 실행할 최대 패스 수 (기본값: 5) |
| `CONSTRAINTS` | 선택 | 범위, 대상 독자, 어조, 금지 사항 등 |

**예제**

```
$control-finish-until-done
MISSION_GOAL: 세션 인증 가이드를 초보자도 읽을 수 있게 완성
TARGET_SCOPE: docs/auth/
DONE_CONDITION:
  - 프로젝트를 처음 보는 개발자가 외부 도움 없이 따라올 수 있다
  - 모든 코드 예제가 현재 API와 일치한다
  - TODO나 빈 섹션이 없다
```

---

### `control-improve-loop` — 품질 기준까지 반복 개선

**한 줄 설명:** 작업 결과물을 스스로 검토하고 가장 가치 있는 개선 하나를 골라 적용하는 루프를 품질 기준이 충족될 때까지 반복합니다.

**언제 써요?**
- 하나의 결과물을 더 단순하고 품질 높게 만들고 싶을 때
- "지금 이게 가장 좋은 형태인가?" 스스로 검토하며 개선하고 싶을 때
- 과잉 설계 없이 핵심적인 개선만 적용하고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `MISSION_GOAL` | ✅ | 개선할 하나의 작업 |
| `TARGET_SCOPE` | ✅ | 검토하고 개선할 범위 |
| `DONE_CONDITION` | ✅ | 품질 기준 목록 — 확인 가능한 조건만 유효 |
| `CURRENT_EVIDENCE` | 선택 | 현재 상태, 이전 리뷰 노트, 테스트 결과 등 |
| `COMPANION_SKILLS` | 선택 | 개선 패스에서 쓸 수 있는 스킬 목록 |
| `MAX_PASSES` | 선택 | 한 턴에서 실행할 최대 패스 수 (기본값: 3) |
| `CONSTRAINTS` | 선택 | 단순성 기준, 범위 제한 등 |

**예제**

```
$compose + $control-improve-loop + $build-write-code + $review-final-verify + @src/auth
+ [세션 갱신 흐름을 가장 단순하고 올바른 형태가 증명될 때까지 검토하고 조여라.]
```
