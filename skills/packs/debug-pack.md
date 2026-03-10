# debug-pack

> 이 pack은 runtime skill이 아니다.
> `debug-*` 카테고리와 디버그 workflow를 묶어 설명한다.

## 이 pack이 맡는 경계

- 실패 표면을 줄이고 root cause에 들어간다.
- 막연한 구조 리뷰나 기능 구현으로 새지 않는다.

## core runtime surface

- `debug-map-blast-radius`
- `debug-find-root-cause`
- `wf-debug-this`

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 어디서부터 디버깅할지 모른다 | `debug-map-blast-radius` |
| 재현은 되는데 원인을 못 잡았다 | `debug-find-root-cause` |
| failure surface 축소부터 test gap 확인까지 한 번에 | `wf-debug-this` |

## 대표 매크로

```text
$compose + $wf-debug-this
```
