# scout-pack

> 이 pack은 runtime skill이 아니다.
> `scout-*` 카테고리 경계와 추천 entrypoint를 설명한다.

## 이 pack이 맡는 경계

- 구현 전에 범위, 사실, 기준값을 먼저 고정한다.
- 아직 코드를 바꾸지 않는다.

## core runtime surface

- `scout-facts`
- `scout-scope`
- `scout-boundaries`
- `scout-baseline`

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 근거 기반 분석 | `scout-facts` |
| 요청 명확화 | `scout-scope` |
| in/out scope와 done condition 고정 | `scout-boundaries` |
| 최적화 전 baseline 측정 | `scout-baseline` |

## 대표 매크로

```text
$compose + $scout-boundaries
```

```text
$compose + $scout-facts
```
