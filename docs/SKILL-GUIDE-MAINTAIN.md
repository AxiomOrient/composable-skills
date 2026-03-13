# 정리하기 — tidy / doc 스킬 가이드

> 이 파일은 [Atomic Skills 가이드](./ATOMIC-SKILLS-GUIDE.md)의 일부입니다.

---

## 이 파일의 스킬

| 카테고리 | 스킬 | 한 줄 설명 |
|----------|------|-----------|
| tidy | `tidy-analyze` | 왜 이 코드가 복잡한지 원인을 먼저 분해합니다 |
| tidy | `tidy-review` | 코드를 바꾸기 전 재사용·품질·효율 관점에서 발견사항을 만듭니다 |
| tidy | `tidy-cut-fat` | 핵심 동작은 그대로 두고 쓸데없는 복잡함만 제거합니다 |
| tidy | `tidy-find-copies` | 같은 로직이나 구조가 여러 곳에 복제돼 있는지 찾습니다 |
| tidy | `tidy-find-magic-numbers` | 코드 곳곳에 흩어진 숫자나 문자열을 찾아 한 곳으로 모읍니다 |
| tidy | `tidy-reorganize` | 동작은 그대로 유지하면서 파일 구조와 모듈 경계를 재배치합니다 |
| tidy | `tidy-simplify` | 한정된 범위에서 코드 구조를 더 짧고 이해하기 쉽게 단순화합니다 |
| tidy | `tidy-apply-review-fixes` | 리뷰 발견사항을 모아 안전한 수정만 실제 코드에 반영합니다 |
| tidy | `tidy-remove-legacy` | 오래된 파일, 완료된 계획 문서, 죽은 별칭, 쓸모없는 코드를 제거합니다 |
| doc | `doc-find-all` | 문서를 모두 찾아서 고아·중복·시간에 묶인 문서를 분류합니다 |
| doc | `doc-curate` | 각 문서를 keep/update/deprecate/delete로 판정합니다 |
| doc | `doc-write` | 아키텍처 노트, 사용 가이드, 개념 설명 등 일반 문서를 직접 씁니다 |
| doc | `doc-build-index` | 폴더 트리를 부모 overview + 자식 detail 계층 문서 세트로 만듭니다 |
| doc | `doc-write-release-docs` | 릴리즈 노트, changelog, 업그레이드 가이드 같은 릴리즈 전용 문서를 씁니다 |
| doc | `doc-publish-readme` | 저장소 루트 README를 만들고 다국어 번역본도 함께 퍼블리시합니다 |

---

## tidy — 코드를 정리하는 스킬

> 새 기능 추가가 아닙니다. **같은 일을 더 단순하게** 만듭니다.

### tidy 스킬 어떤 걸 골라야 하나?

| 상황 | 쓸 스킬 |
|------|---------|
| 왜 복잡한지 원인부터 파악하고 싶다 | `tidy-analyze` |
| 코드 변경 전 재사용/품질/효율 검토를 하고 싶다 | `tidy-review` |
| 복잡한 구조를 직접 줄이고 싶다 | `tidy-cut-fat` |
| 중복 코드를 찾고 싶다 | `tidy-find-copies` |
| 흩어진 상수/마법 숫자를 찾고 싶다 | `tidy-find-magic-numbers` |
| 파일 구조를 재배치하고 싶다 | `tidy-reorganize` |
| 코드를 직접 단순화하고 싶다 | `tidy-simplify` |
| 리뷰 발견사항을 코드에 적용하고 싶다 | `tidy-apply-review-fixes` |
| 낡은 파일/코드를 제거하고 싶다 | `tidy-remove-legacy` |

---

### `tidy-analyze` — 복잡한 이유 먼저 파악하기

**한 줄 설명:** 왜 이 코드가 복잡한지 원인을 먼저 분해합니다.

**언제 써요?**
- "이 코드가 너무 복잡한데 뭐가 문제인지 모르겠다"
- 정리하기 전에 원인 분석을 먼저 할 때
- 복잡성이 도메인 자체의 문제인지, 잘못된 구조 때문인지 구분하고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 분석할 범위 (경로·모듈·저장소) |
| `SIMPLIFICATION_GOAL` | ✅ | 집중할 복잡성 종류 (`naming` / `structure` / `side-effects` / `mixed`) |

**예제**

```
$tidy-analyze
TARGET_SCOPE: src/auth
SIMPLIFICATION_GOAL: structure
```

---

### `tidy-review` — 정리 전 코드 검토

**한 줄 설명:** 코드를 바꾸기 전 재사용·품질·효율 관점에서 발견사항을 만들어 `tidy-apply-review-fixes`에 넘깁니다.

**언제 써요?**
- 실제 수정에 앞서 "무엇을 고쳐야 하는지" 목록을 먼저 만들고 싶을 때
- `workflow-tidy-simplify-this`를 구성하는 검토 단계로 쓸 때
- 재사용·품질·효율 세 가지 관점 중 하나 또는 전부를 살펴봐야 할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 검토할 범위 (경로·모듈·폴더·diff) |
| `FOCUS` | 선택 | 검토 관점 (`reuse` / `quality` / `efficiency` / `all`, 기본값 `all`) |
| `KNOWN_EVIDENCE` | 선택 | 기존 테스트 결과, 벤치마크, 이전 검토 노트 |

**예제**

```
$tidy-review
TARGET_SCOPE: diff
FOCUS: all
```

---

### `tidy-cut-fat` — 군살 제거하기

**한 줄 설명:** 핵심 동작은 그대로 두고 쓸데없는 복잡함만 제거합니다.

**언제 써요?**
- "구조가 너무 무거운데 핵심만 남기고 싶다"
- 과한 추상화, 시끄러운 폴더 구조 정리
- 직접 코드를 바꾸기보다 단순화 계획서가 먼저 필요할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 정리할 범위 (경로·모듈·폴더·저장소) |
| `SIMPLIFICATION_GOAL` | ✅ | 제거할 복잡성 방향 (`naming` / `structure` / `side-effects` / `mixed`) |
| `PRESERVE_BEHAVIOR` | ✅ | 기존 동작 유지 여부 (`yes` / `no-change-intent`) |
| `KNOWN_PAIN` | 선택 | 이미 알고 있는 문제 부분 목록 |

**예제**

```
$tidy-cut-fat
TARGET_SCOPE: src/components/
SIMPLIFICATION_GOAL: structure
PRESERVE_BEHAVIOR: yes
KNOWN_PAIN:
  - 컴포넌트가 너무 많은 props를 받음
```

---

### `tidy-find-copies` — 중복 코드 찾기

**한 줄 설명:** 같은 로직이나 구조가 여러 곳에 복제돼 있는지 찾습니다.

**언제 써요?**
- "어딘가 비슷한 코드가 여러 군데 있는 것 같다"
- 중복 제거 전 전수 조사
- 진짜 중복인지 아니면 의도적으로 다른 코드인지 판단이 필요할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 찾을 범위 (경로·모듈·저장소) |
| `DUPLICATION_KIND` | ✅ | 중복 종류 (`logic` / `structure` / `flow` / `mixed`) |

**예제**

```
$tidy-find-copies
TARGET_SCOPE: src/payments
DUPLICATION_KIND: flow
```

---

### `tidy-find-magic-numbers` — 흩어진 숫자 상수 찾기

**한 줄 설명:** 코드 곳곳에 흩어진 숫자나 문자열을 찾아 한 곳으로 모읍니다.

**언제 써요?**
- "30이 어디서 온 숫자야?" 같은 상황
- 설정값, 정책 상수를 한 곳에 모아야 할 때
- 같은 숫자가 여러 파일에 흩어져 있어 수정할 때 빠뜨릴 위험이 있을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 찾을 범위 (경로·모듈·저장소) |
| `EXTRACTION_POLICY` | ✅ | 추출 목적지 (`constants` / `config` / `shared-definition`) |

**예제**

```
$tidy-find-magic-numbers
TARGET_SCOPE: src/auth
EXTRACTION_POLICY: constants
```

---

### `tidy-reorganize` — 파일 구조 재배치 계획

**한 줄 설명:** 동작은 그대로 유지하면서 파일 구조와 모듈 경계를 더 낫게 재배치합니다.

**언제 써요?**
- "파일이 너무 뒤섞여 있다. 구조를 다시 잡고 싶다"
- 모듈 경계 정리나 의존성 방향 정비가 필요할 때
- 실제 코드 변경 전 단계별 리팩터링 계획이 필요할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 재배치할 범위 (경로·모듈·폴더·저장소) |
| `REFACTOR_BOUNDARY` | ✅ | 리팩터링 유형 (`module-boundary` / `dependency-hygiene` / `structure-preserving-cleanup`) |
| `BEHAVIOR_INVARIANTS` | ✅ | 반드시 유지해야 할 것 목록 |
| `CONSTRAINTS` | 선택 | 호환성, 테스트 제약 목록 |

**예제**

```
$tidy-reorganize
TARGET_SCOPE: src/
REFACTOR_BOUNDARY: module-boundary
BEHAVIOR_INVARIANTS:
  - 기존 API 경로 유지
  - 외부 라이브러리 import 경로 유지
```

---

### `tidy-simplify` — 코드 단순화

**한 줄 설명:** 한정된 범위에서 코드 구조를 더 짧고 이해하기 쉬운 모양으로 단순화합니다.

**언제 써요?**
- `tidy-cut-fat`이 단순화 계획을 만들었고 이제 실제 코드를 줄여야 할 때
- 중첩 분기, 불필요한 간접 참조, 일회용 헬퍼를 직접 제거하고 싶을 때
- 범위가 명확하고 동작 동등성을 확인할 수 있는 경우

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 단순화할 범위 (경로·모듈·폴더·diff) |
| `FUNCTIONAL_EQUIVALENCE` | ✅ | 동작 유지 확인 (`yes` 만 허용) |
| `SIMPLIFY_GOAL` | ✅ | 집중할 방향 (`control-flow` / `data-flow` / `indirection` / `immutability` / `mixed`) |
| `KNOWN_PAIN` | 선택 | 특히 복잡한 부분 목록 (`SYMPTOM`, `LOCATION`, `WHY_RELEVANT`) |

**예제**

```
$tidy-simplify
TARGET_SCOPE: src/auth/session.ts
FUNCTIONAL_EQUIVALENCE: yes
SIMPLIFY_GOAL: indirection
KNOWN_PAIN:
  - nested branching hides refresh intent
  - one-use helper chain obscures data flow
```

---

### `tidy-apply-review-fixes` — 리뷰 결과 적용하기

**한 줄 설명:** 여러 리뷰 결과를 모아 겹치는 지적을 정리하고 안전한 수정만 실제 코드에 반영합니다.

**언제 써요?**
- `tidy-review`나 다른 스킬이 발견사항을 만들었고 이제 실제로 고쳐야 할 때
- 여러 리뷰 결과를 한 번에 적용하되 위험한 변경은 걸러내고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 수정 적용 범위 (경로·모듈·폴더·diff) |
| `REVIEW_FINDINGS` | ✅ | 적용할 리뷰 발견사항 목록 (`SOURCE_SKILL`, `ISSUE`, `LOCATION`, `RECOMMENDED_FIX`, `EVIDENCE`) |
| `FUNCTIONAL_EQUIVALENCE` | ✅ | 동작 유지 (`yes` / `preserve-current-behavior`) |
| `APPLY_POLICY` | 선택 | 적용 강도 (`fix-high-signal` / `fix-all-safe`) |

**예제**

```
$tidy-apply-review-fixes
TARGET_SCOPE: src/utils/
REVIEW_FINDINGS:
  - dateFormat 함수가 3곳에 중복 (tidy-review 결과)
  - maxRetry 상수값 하드코딩 (tidy-find-magic-numbers 결과)
FUNCTIONAL_EQUIVALENCE: yes
APPLY_POLICY: fix-high-signal
```

---

### `tidy-remove-legacy` — 낡은 코드/파일 제거

**한 줄 설명:** 오래된 파일, 완료된 계획 문서, 죽은 별칭, 쓸모없는 코드를 제거합니다.

**언제 써요?**
- 이미 끝난 계획 문서나 deprecated 폴더를 지워야 할 때
- 더 이상 쓰지 않는 별칭이나 glue 코드를 정리해야 할 때
- 삭제 후 남은 참조도 함께 업데이트해야 할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 제거 허용 범위 (경로·모듈·폴더·저장소) |
| `LEGACY_TARGETS` | ✅ | 제거할 파일·패턴 목록 (`PATH_OR_PATTERN`, `WHY_LEGACY`) |
| `CLEANUP_MODE` | ✅ | 제거 방식 (`delete-only` / `delete-and-relink` / `collapse-alias` / `mixed`) |
| `VERIFICATION_MAP` | ✅ | 정리 후 검증 기준 목록 (`CHECK`, `ORDER`, `PASS_CONDITION`) |
| `PRESERVE_SURFACE` | 선택 | 반드시 남겨야 할 파일/경로 목록 |
| `CONSTRAINTS` | 선택 | 호환성, 비목표 제약 목록 |

**예제**

```
$tidy-remove-legacy
TARGET_SCOPE: ./
LEGACY_TARGETS:
  - path: plans/IMPLEMENTATION-PLAN.md
    why: 완료된 계획 문서
  - path: src/legacy-api/
    why: 더 이상 사용 안 하는 폴더
CLEANUP_MODE: delete-only
VERIFICATION_MAP:
  - check: npm test
    order: 1
    pass_condition: 전체 통과
PRESERVE_SURFACE:
  - path: docs/
    why: 현재 사용 중인 문서
  - path: README.md
    why: 프로젝트 진입점
```

---

## doc — 문서를 다루는 스킬

> 코드가 아니라 **설명**을 정리합니다.

### doc 스킬 어떤 걸 골라야 하나?

| 상황 | 쓸 스킬 |
|------|---------|
| 문서가 어디 뭐가 있는지 먼저 파악하고 싶다 | `doc-find-all` |
| 각 문서를 keep/update/deprecate/delete로 정리하고 싶다 | `doc-curate` |
| 일반 가이드, 아키텍처, 사용법 문서를 새로 쓰고 싶다 | `doc-write` |
| 폴더 트리를 부모 overview + 자식 detail 계층 문서로 만들고 싶다 | `doc-build-index` |
| 릴리즈 노트, 변경 요약, 업그레이드 가이드를 만들고 싶다 | `doc-write-release-docs` |
| 저장소 루트 README를 만들거나 다국어로 퍼블리시하고 싶다 | `doc-publish-readme` |

---

### `doc-find-all` — 문서 전수 조사

**한 줄 설명:** 문서를 모두 찾아서 고아 문서, 중복 문서, 시간에 묶인 문서, 배달용 문서를 분류합니다.

**언제 써요?**
- "문서가 너무 많은데 어디에 뭐가 있는지 모르겠다"
- 문서 정리, 계층 문서화, 릴리즈 문서 작성 전에 인벤토리 만들기
- 어떤 문서가 낡았는지, 중복인지, 독자가 있는지 판단하기 전

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `TARGET_SCOPE` | ✅ | 조사할 범위 (문서 폴더·저장소) |
| `INVENTORY_GOAL` | 선택 | 조사 목적 (`cleanup` / `navigation` / `coverage` / `lifecycle` / `mixed`, 기본값 `mixed`) |

**예제**

```
$doc-find-all
TARGET_SCOPE: docs/
INVENTORY_GOAL: lifecycle
```

---

### `doc-curate` — 문서 수명주기 판정

**한 줄 설명:** 각 문서를 keep, update, deprecate, delete로 분류하고, 지우기 전에 옮겨야 할 지식을 분리합니다.

**언제 써요?**
- 문서 대청소 전에 "무엇을 살리고 무엇을 내릴지" 먼저 정해야 할 때
- 예전 문서를 바로 지워도 되는지 확신이 없을 때
- 삭제 후보 문서 안에 아직 살아있는 지식이 있는지 확인하고 싶을 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `CURATION_GOAL` | ✅ | 정리 목표 (`lifecycle-governance` / `cleanup` / `surface-sync` / `mixed`) |
| `TARGET_SCOPE` | ✅ | 정리할 범위 (문서 폴더·저장소·서브트리) |
| `INVENTORY_SCOPE` | ✅ | 조사 깊이 (`folder-tree` / `repo-wide` / `release-surface`) |
| `DECISION_MODE` | 선택 | 삭제 판단 강도 (`conservative` / `balanced` / `aggressive`, 기본값 `conservative`) |
| `CANONICAL_SURFACES` | 선택 | 유지해야 할 기준 문서 목록 (`PATH`, `WHY_CANONICAL`) |

**예제**

```
$doc-curate
CURATION_GOAL: lifecycle-governance
TARGET_SCOPE: docs/
INVENTORY_SCOPE: folder-tree
```

---

### `doc-write` — 문서 작성

**한 줄 설명:** 아키텍처 노트, 사용 가이드, 개념 설명, redirect, deprecation 문서를 직접 씁니다.

**언제 써요?**
- 새 기능을 만들었는데 문서가 없을 때
- 사용법 가이드, API 문서, 모듈 설명을 만들어야 할 때
- 문서를 바로 지우지 않고 짧은 브리지 문서를 남겨야 할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `DOC_GOAL` | ✅ | 문서 목적 (`refresh` / `concept-guide` / `architecture-guide` / `usage-guide` / `api-guide` / `module-note` / `deprecation-note` / `redirect-note` / `mixed`) |
| `TARGET_SCOPE` | ✅ | 문서화할 대상 범위 (폴더·모듈·아티팩트·서브트리) |
| `AUDIENCE` | ✅ | 주요 독자 (`general` / `developer` / `operator` / `maintainer` / `mixed`) |
| `EVIDENCE_LINKS` | ✅ | 문서 내용의 근거가 될 파일, 명령어, 로그, 업스트림 결과물 |
| `DOC_FORM` | 선택 | 문서 형태 (`guide` / `tutorial` / `reference` / `concept-note` / `redirect` / `deprecation-note`, 기본값 `guide`) |
| `AUDIENCE_LEVEL` | 선택 | 독자 수준 (`general` / `intermediate` / `expert`) |

**예제**

```
$doc-write
DOC_GOAL: usage-guide
TARGET_SCOPE: src/auth/
AUDIENCE: developer
EVIDENCE_LINKS:
  - type: file
    ref: src/auth/README.md
    why_relevant: 현재 인증 흐름 설명
  - type: file
    ref: src/auth/session.ts
    why_relevant: 세션 관리 구현
AUDIENCE_LEVEL: general
```

---

### `doc-build-index` — 부모 요약 + 자식 상세 문서 세트 만들기

**한 줄 설명:** 폴더 트리를 부모 README 스타일 요약과 자식 프로젝트 정보 문서로 나눠 계층 문서 세트를 만듭니다.

**언제 써요?**
- 상위 폴더는 overview, 하위 폴더는 detail로 경계를 나누고 싶을 때
- 긴 트리를 한 문서에 뭉개지 않고 읽기 좋게 내려가게 만들고 싶을 때
- 저장소 루트 README가 아닌 하위 폴더 계층에 탐색 구조를 만들 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `DOCSET_KIND` | ✅ | 대상 종류 (`folder-tree` / `module-tree` / `project-tree`) |
| `TREE_SCOPE` | ✅ | 문서화할 폴더 트리 범위 |
| `INDEX_DEPTH` | ✅ | 깊이 (`one-level` / `recursive`) |
| `AUDIENCE` | ✅ | 독자 (`general` / `developer` / `maintainer` / `mixed`) |
| `INDEX_LAYOUT` | 선택 | 인덱스 위치 (`docs-mirror` / `in-place-readme`, 기본값 `in-place-readme`) |
| `PARENT_ENTRY_STYLE` | 선택 | 부모 문서 형태 (`readme-overview` / `index-page`, 기본값 `readme-overview`) |
| `CHILD_DOC_STYLE` | 선택 | 자식 문서 형태 (`project-info` / `module-info` / `mixed`, 기본값 `project-info`) |
| `AUDIENCE_LEVEL` | 선택 | 독자 수준 |
| `EVIDENCE_LINKS` | 선택 | 추가 근거 자료 |

**예제**

```
$doc-build-index
DOCSET_KIND: folder-tree
TREE_SCOPE: skills/
INDEX_DEPTH: recursive
AUDIENCE: developer
INDEX_LAYOUT: in-place-readme
```

---

### `doc-write-release-docs` — 릴리즈 문서 쓰기

**한 줄 설명:** 릴리즈 노트, changelog entry, 업그레이드 가이드, 마이그레이션 문서 같은 릴리즈 전용 문서를 씁니다.

**언제 써요?**
- 이번 릴리즈에서 무엇이 바뀌었는지 설명해야 할 때
- 사용자가 실제로 해야 할 업그레이드 행동을 적어야 할 때
- 호환성 변경이나 마이그레이션 필요 여부를 명확히 적어야 할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `RELEASE_SCOPE` | ✅ | 릴리즈 범위 (`diff` / `tag` / `version` / `repo` / `deployment-slice`) |
| `RELEASE_DOC_GOAL` | ✅ | 문서 목적 (`release-note` / `changelog-entry` / `upgrade-note` / `migration-guide` / `compatibility-note` / `rollback-note` / `mixed`) |
| `AUDIENCE` | ✅ | 주요 독자 (`user` / `developer` / `operator` / `maintainer` / `mixed`) |
| `RELEASE_VERSION` | 선택 | 버전/태그/라벨 |
| `BREAKING_CHANGE_POLICY` | 선택 | 호환성 영향 강조 방식 (`highlight-all` / `highlight-breaking-only` / `none`, 기본값 `highlight-all`) |
| `RELEASE_EVIDENCE` | 선택 | diff, 이슈, PR, 테스트 같은 근거 |

**예제**

```
$doc-write-release-docs
RELEASE_SCOPE: diff
RELEASE_DOC_GOAL: mixed
AUDIENCE: mixed
RELEASE_VERSION: v2.4.0
```

---

### `doc-publish-readme` — 루트 README 만들기

**한 줄 설명:** 저장소 루트 README를 GitHub 첫 화면답게 만들고, 필요하면 다른 언어 번역본도 함께 만듭니다.

**언제 써요?**
- 저장소 루트 README를 새로 만들거나 전면 개정할 때
- GitHub 첫 화면에서 프로젝트를 빠르게 이해할 수 있도록 정리하고 싶을 때
- 한국어, 영어 등 여러 언어 번역본을 `/i18n/<lang>/` 아래에 함께 퍼블리시할 때

**입력값**

| 입력키 | 필수 | 설명 |
|--------|:---:|------|
| `PROJECT_SCOPE` | ✅ | 저장소 루트 (`repo`) |
| `README_GOAL` | ✅ | 목적 (`github-overview` / `onboarding` / `usage-entry` / `mixed`) |
| `AUDIENCE` | ✅ | 주요 독자 (`general` / `developer` / `operator` / `mixed`) |
| `SOURCE_DOCS` | ✅ | README에 요약/링크할 문서 목록 (`PATH`, `ROLE`) |
| `PRIMARY_LANGUAGE` | 선택 | 주 작성 언어 (기본값 `en`) |
| `TARGET_LANGUAGES` | 선택 | 번역본 언어 목록 (기본값 `ko, es, zh`) |
| `AUDIENCE_LEVEL` | 선택 | 독자 수준 |

**예제**

```
$doc-publish-readme
PROJECT_SCOPE: repo
README_GOAL: github-overview
AUDIENCE: developer
SOURCE_DOCS:
  - path: docs/SKILL-SYSTEM.md
    role: 시스템 개요
  - path: skills/README.md
    role: 스킬 목록 진입점
PRIMARY_LANGUAGE: ko
TARGET_LANGUAGES: [en, ja]
```

---
