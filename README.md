# Composable Skills

스킬 기반 작업 자동화 런타임. 한 스킬은 한 가지 일만 합니다.

## 설치

```bash
git clone git@github.com:AxiomOrient/composable-skills.git
cd composable-skills
./scripts/sync.sh
```

프로젝트 로컬 설치:

```bash
./scripts/sync.sh local
```

프로파일별 설치:

```bash
./scripts/sync.sh core          # 기본 (planning, build, debug, review, test, tidy)
./scripts/sync.sh docs-release  # 문서 + 릴리즈 + 보안
./scripts/sync.sh extras        # gemini, commit-write-message
./scripts/sync.sh all           # 전체
```

## 요구사항

- `bash`
- `python3`

---

## 어떻게 쓰나요?

스킬은 세 층으로 나뉩니다.

| 층 | 이름 | 언제 쓰나 |
|----|------|-----------|
| **workflow** | `workflow-*` | 처음 시작할 때. 한 덩어리 일을 처음부터 끝까지 맡김 |
| **atomic** | 개별 스킬 | 정확히 이 동작만 필요할 때. 세밀하게 조립 |
| **control** | `control-*` | 반복 실행, 루프 제어가 필요할 때 |

Atomic 스킬 카테고리:

| 카테고리 | 무엇을 하나 |
|---------|------------|
| `analyze-*` | 중립 분석. 판정 없이 구조·복잡도·의존성·근거를 지도로 만든다 |
| `clarify-*` | 요구사항 명확화. 범위·경계·완료 조건을 계약서로 만든다 |
| `review-*` | 판정 포함 리뷰. pass/fail, 이슈 목록, 병합 가능/보류 결론을 낸다 |
| `plan-*` | 설계와 계획. 명세, 작업 분해, 검증 순서를 만든다 |
| `build-*` | 코드 구현과 성능 개선 |
| `debug-*` | 버그 재현, 영향 분석, 근본 원인 찾기 |
| `test-*` | 테스트 빈틈 분석, 케이스 설계, 테스트 작성 |
| `tidy-*` | 코드 정리, 중복 제거, 복잡도 감소 |
| `doc-*` | 문서 인벤토리, 정리, 작성, 배포 |
| `release-*` | 릴리즈 검사, 판정, 배포 |
| `ask-*` | 질문 설계, 가정 뒤집기, 프롬프트 수정 |

**처음이라면 workflow부터** 고르면 됩니다.

---

## Workflow 빠른 선택 가이드

| 지금 필요한 것 | 쓸 workflow |
|----------------|------------|
| 질문/요청이 흐리다, 뭘 해야 할지 모르겠다 | [`workflow-clarify-request`](./skills/workflow-clarify-request/SKILL.md) |
| 코드 구조·복잡도·의존성을 한 번에 분석하고 싶다 | [`workflow-analyze-codebase`](./skills/workflow-analyze-codebase/SKILL.md) |
| 현재 코드 구조와 범위를 먼저 파악하고 싶다 | [`workflow-scout-structure`](./skills/workflow-scout-structure/SKILL.md) |
| 간단한 코드 리뷰가 필요하다 | [`workflow-review-change`](./skills/workflow-review-change/SKILL.md) |
| 구조·품질·보안·실패경로 완전한 리뷰가 필요하다 | [`workflow-review-complete`](./skills/workflow-review-complete/SKILL.md) |
| 버그를 처음부터 끝까지 잡고 싶다 | [`workflow-debug-this`](./skills/workflow-debug-this/SKILL.md) |
| 구현 전에 계획을 세우고 싶다 | [`workflow-plan-build-ready`](./skills/workflow-plan-build-ready/SKILL.md) |
| 코드를 구현하고 테스트까지 한 번에 | [`workflow-build-implement-and-guard`](./skills/workflow-build-implement-and-guard/SKILL.md) |
| 기존 TASKS.md를 끝까지 실행하고 싶다 | [`workflow-build-execute-plan`](./skills/workflow-build-execute-plan/SKILL.md) |
| 테스트 빈 곳 찾고 채우고 싶다 | [`workflow-test-close-gaps`](./skills/workflow-test-close-gaps/SKILL.md) |
| 방금 바꾼 코드를 더 깔끔하게 다듬고 싶다 | [`workflow-tidy-simplify-this`](./skills/workflow-tidy-simplify-this/SKILL.md) |
| 어디를 정리해야 할지 지도부터 보고 싶다 | [`workflow-tidy-find-improvements`](./skills/workflow-tidy-find-improvements/SKILL.md) |
| 문서 표면을 keep/update/deprecate/delete 기준으로 정리하고 싶다 | [`workflow-doc-systemize`](./skills/workflow-doc-systemize/SKILL.md) |
| 폴더 트리를 부모 README + 자식 프로젝트 정보 문서로 만들고 싶다 | [`workflow-doc-build-docset`](./skills/workflow-doc-build-docset/SKILL.md) |
| 릴리즈 노트, 변경 요약, 업그레이드 문서를 만들고 싶다 | [`workflow-doc-release-package`](./skills/workflow-doc-release-package/SKILL.md) |
| 배포 가능한지 확인하고 싶다 | [`workflow-release-ready-check`](./skills/workflow-release-ready-check/SKILL.md) |
| 릴리즈 점검부터 배포까지 한 번에 | [`control-release-publish-flow`](./skills/control-release-publish-flow/SKILL.md) |

---

## 더 깊이 보기

| 문서 | 설명 |
|------|------|
| **[Atomic Skills 가이드](./docs/ATOMIC-SKILLS-GUIDE.md)** | 전체 스킬 목록, 카테고리별 선택 가이드, 빠른 참조표 |
| [이해하기 (ask/clarify/analyze)](./docs/SKILL-GUIDE-UNDERSTAND.md) | 질문 다듬기, 범위 명확화, 중립 분석 스킬 15개 상세 설명 |
| [만들기 (plan/build/debug/test)](./docs/SKILL-GUIDE-BUILD.md) | 설계, 구현, 디버그, 테스트 스킬 17개 상세 설명 |
| [검증하기 (review/release/commit/control)](./docs/SKILL-GUIDE-REVIEW.md) | 리뷰 판정, 배포 검증, 반복 제어 스킬 12개 상세 설명 |
| [정리하기 (tidy/doc)](./docs/SKILL-GUIDE-MAINTAIN.md) | 코드 정리, 문서 관리 스킬 15개 상세 설명 |
| [스킬 전체 목록](./skills/README.md) | workflow + atomic 전체 목록 및 선택 가이드 |
| [스킬 시스템 구조](./docs/SKILL-SYSTEM.md) | 시스템 레이어, 운영 원칙 |
| [스킬 제작 가이드](./docs/CODEX-SKILL-AUTHORING-GUIDE.md) | 새 스킬을 만들거나 수정할 때 |

---

## 저장소 구조

```
skills/               런타임 스킬 surface
  <name>/SKILL.md     사람이 읽는 스킬 설명서
  <name>/skill.json   런타임이 읽는 기계용 계약
  _meta/              공통 메타데이터
docs/                 상세 문서
scripts/sync.sh       스킬 설치/업데이트
scripts/skills.py     검증 및 sync CLI
```

## Requirements

- `bash`
- `python3`
