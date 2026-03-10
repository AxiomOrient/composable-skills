# test-pack

> 이 pack은 runtime skill이 아니다.
> `test-*` 카테고리의 설계/실행/공백 점검 경계를 설명한다.

## 이 pack이 맡는 경계

- 무엇을 시험할지 정하고, 빠진 보호막을 찾고, 실제 가드를 추가한다.
- 기능 구현과 테스트 설계를 섞지 않는다.

## core runtime surface

- `test-design-cases`
- `test-find-gaps`
- `test-write-guards`
- `test-run-user-scenarios`

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 테스트 케이스 설계 | `test-design-cases` |
| 빠진 회귀 보호막 찾기 | `test-find-gaps` |
| 실제 자동화 테스트 추가 | `test-write-guards` |
| 현실적인 사용자/에이전트 시나리오 점검 | `test-run-user-scenarios` |

## 대표 매크로

```text
$compose + $test-design-cases + $test-write-guards
```
