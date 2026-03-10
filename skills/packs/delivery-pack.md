# delivery-pack

> 이 pack은 runtime skill이 아니다.
> 범위 확정에서 구현, 테스트, 최종 검증까지 이어지는 delivery 흐름을 설명한다.

## 이 pack이 맡는 경계

- 요청을 실행 가능한 delivery 계약으로 줄인다.
- 계획, 구현, 테스트, 최종 검증을 한 흐름으로 본다.

## core runtime surface

- `scout-boundaries`
- `plan-task-breakdown`
- `plan-verify-order`
- `build-write-code`
- `test-write-guards`
- `check-delivered`
- `plan-driven-delivery`

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 실행 범위와 done condition 확정 | `scout-boundaries` |
| 계획서와 task table 작성 | `plan-task-breakdown` |
| 구현 전 검증 순서 확정 | `plan-verify-order` |
| 코드 구현 + 검증 근거 | `build-write-code` |
| 계획/실행 동기화 | `plan-driven-delivery` |

## 대표 매크로

```text
$compose + $scout-boundaries + $plan-task-breakdown + $plan-verify-order + $build-write-code + $test-write-guards + $check-delivered
```
