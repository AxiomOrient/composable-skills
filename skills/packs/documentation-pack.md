# documentation-pack

> 이 pack은 runtime skill이 아니다.
> 문서 작업을 `일반 docs`, `계층형 지식 docs`, `루트 README + 다국어 게시`로 나눠 설명하는 카탈로그다.

## 이 pack의 핵심 구조

문서 작업은 아래 3개 코어로 나눈다.

1. `doc-write`
일반 문서와 가이드를 쓴다. 루트 README는 건드리지 않는다.

2. `doc-build-index`
폴더, 모듈, 라이브러리, 논문을 분석 문서와 계층형 인덱스로 묶는다. 루트 README는 건드리지 않는다.

3. `doc-publish-readme`
루트 README와 다국어 entry docs를 만든다. 이 skill만 루트 README를 수정한다.

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 일반 설명 문서나 사용 가이드 | `doc-write` |
| 폴더/모듈/라이브러리/논문을 구조적으로 풀어 쓰고 인덱싱 | `doc-build-index` |
| 프로젝트 첫 화면 README와 다국어 진입 문서 | `doc-publish-readme` |

문서 형식은 스킬을 더 쪼개기보다 `DOC_FORM`으로 고른다.

- `guide`, `tutorial`, `reference`, `paper-summary`, `survey`
- 형식은 입력으로 고르고, lens는 설명 방식의 멘탈 모델로 쓴다

## 지원용 helper

아래 스킬은 코어가 아니라 보조다.

- `doc-find-all`: 문서 목록과 상태 파악
- `doc-curate`: 링크 구조, 중복, 탐색 정리

## 권장 흐름

### 일반 docs만 필요할 때

```text
$compose + $doc-write
```

### 계층형 docs를 만들 때

```text
$compose + $doc-build-index
```

### 프로젝트 문서 surface를 마무리할 때

```text
$compose + $doc-publish-readme + $check-delivered
```

## 기본 원칙

- 기본 난이도는 `general`이다.
- 어려운 용어는 쉬운 말로 먼저 풀어쓴다.
- 루트 README는 `doc-publish-readme`만 수정한다.
- 루트 README 기본 언어는 `en`이다.
- 기본 로컬라이징 언어는 `ko`, `es`, `zh`다.
- 다국어 entry docs는 `docs/i18n/<lang>/` 아래에 둔다.

## 다음에 볼 문서

- 조합 예시: [`../SKILL-COMBOS.md`](../SKILL-COMBOS.md)
- atomic 설명: [`../ATOMIC-SKILLS.md`](../ATOMIC-SKILLS.md)
- 전체 안내: [`../README.md`](../README.md)
