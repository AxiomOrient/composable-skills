# build-pack

> 이 pack은 runtime skill이 아니다.
> `build-*` 카테고리와 구현 반복 entrypoint를 설명한다.

## 이 pack이 맡는 경계

- 실제 코드를 바꾸고 검증 근거를 남긴다.
- 계획 문서 작성이나 리뷰 판정은 하지 않는다.

## core runtime surface

- `build-write-code`
- `build-make-faster`
- `build-until-done`

## 함께 자주 붙는 스킬

- `plan-verify-order`
- `test-write-guards`
- `check-delivered`
- `plan-driven-delivery`

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 코드 구현 | `build-write-code` |
| 성능 최적화 | `build-make-faster` |
| 완료 조건까지 반복 구현 | `build-until-done` |

## 대표 매크로

```text
$compose + $build-until-done + $build-write-code + $check-delivered
```
