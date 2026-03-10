# project-quality-pack

> 이 pack은 runtime skill이 아니다.
> 리뷰, 디버그, 개선 후보 탐색을 하나의 quality surface로 묶어 설명한다.

## 이 pack이 맡는 경계

- 구조 리뷰, 버그 디버그, 개선 후보 탐색을 한 묶음으로 고른다.
- 구현은 직접 하지 않고 evidence-backed findings를 모은다.

## core runtime surface

- `wf-check-full-review`
- `wf-check-with-checklist`
- `wf-debug-this`
- `wf-tidy-find-improvements`
- `check-module-walls`
- `check-failure-paths`
- `check-security-holes`
- `test-find-gaps`

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 종합 리뷰 | `wf-check-full-review` |
| 리뷰 + 체크리스트 | `wf-check-with-checklist` |
| 버그 표면 축소 + RCA | `wf-debug-this` |
| 중복/상수/구조 개선 후보 찾기 | `wf-tidy-find-improvements` |

## 대표 매크로

```text
$compose + $wf-check-full-review + $check-delivered
```
