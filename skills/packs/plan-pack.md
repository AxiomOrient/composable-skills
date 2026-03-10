# plan-pack

> 이 pack은 runtime skill이 아니다.
> `plan-*` 카테고리 경계와 설계 문서 흐름을 설명한다.

## 이 pack이 맡는 경계

- 왜/무엇/구조/기술 설계/실행 계획을 분리한다.
- 직접 코드를 수정하지 않는다.

## core runtime surface

- `plan-why-build-this`
- `plan-what-it-does`
- `plan-screen-map`
- `plan-how-to-build`
- `plan-task-breakdown`
- `plan-dependency-rules`
- `plan-verify-order`

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 왜 만드는지 흐리다 | `plan-why-build-this` |
| 기능 요구사항을 고정해야 한다 | `plan-what-it-does` |
| 화면/탐색 구조가 먼저다 | `plan-screen-map` |
| 기술 경계와 trade-off를 문서화해야 한다 | `plan-how-to-build` |
| 실행 계획과 task table이 필요하다 | `plan-task-breakdown` |

## 대표 매크로

```text
$compose + $plan-why-build-this + $plan-what-it-does + $plan-how-to-build
```
