# Runtime Skills

이 폴더는 설치된 Codex runtime이 바로 읽는 스킬 surface다.

핵심 구조는 세 가지다.

- `skills/<name>/SKILL.md`: 사람이 읽는 스킬 설명
- `skills/<name>/skill.json`: `compose`와 sync가 읽는 메타데이터
- `skills/_meta/*.json`: 렌즈와 응답 프로필 같은 공통 메타데이터

## 어떻게 시작하나

처음이면 category 기본 workflow부터 쓴다.

| 카테고리 | 기본 workflow |
|---|---|
| 질문 정리 | `workflow-ask-sharpen` |
| 범위+구조 파악 | `workflow-scout-structure` |
| 리뷰 | `workflow-check-full-review` |
| 디버그 | `workflow-debug-this` |
| 계획 | `workflow-plan-build-ready` |
| 구현 | `workflow-build-implement-and-guard` |
| 테스트 | `workflow-test-close-gaps` |
| 구조 개선 | `workflow-tidy-find-improvements` |
| 문서 | `workflow-doc-systemize` |
| 보안 프리플라이트 | `workflow-security-preflight` |
| 릴리즈 점검 | `workflow-ship-ready-check` |

범위가 흐리면 `SCOPE`, 목표가 흐리면 `GOAL`, 기대 결과가 있으면 `EXPECTED`, 완료 기준이 있으면 `DONE`을 같이 적는 쪽이 좋다.

## 언제 `compose`를 쓰나

하나의 workflow로 충분하지 않을 때만 쓴다.

예:

```text
$compose + $workflow-check-full-review + @src/auth + $check-final-verify
```

이 뜻은:

- `src/auth` 범위를 리뷰하고
- 마지막에 `check-final-verify`로 결과를 한 번 더 검증한다

커밋 직전의 가벼운 보안 게이트는 이렇게 묶는다.

```text
$compose + $workflow-security-preflight + $ship-commit + @ios + [Push 전에 plist, env, 키 파일이 새로 들어갔는지 확인]
```

## 참고

- 설치된 runtime에서는 이 문서와 각 skill의 `SKILL.md`를 우선 본다.
