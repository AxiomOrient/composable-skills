# tidy-pack

> 이 pack은 runtime skill이 아니다.
> `tidy-*` 카테고리의 구조 개선 경계와 추천 흐름을 설명한다.

## 이 pack이 맡는 경계

- duplication, constants, complexity를 근거로 구조 개선을 계획한다.
- 기능 추가나 incident 대응으로 새지 않는다.

## core runtime surface

- `tidy-find-copies`
- `tidy-find-magic-numbers`
- `tidy-why-complex`
- `tidy-cut-fat`
- `tidy-reorganize`
- `wf-tidy-find-improvements`

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 중복 탐지 | `tidy-find-copies` |
| 상수 추출 후보 탐지 | `tidy-find-magic-numbers` |
| 복잡도 원인 분류 | `tidy-why-complex` |
| 개선 포인트를 묶어 보고 싶다 | `wf-tidy-find-improvements` |

## 대표 매크로

```text
$compose + $wf-tidy-find-improvements
```
