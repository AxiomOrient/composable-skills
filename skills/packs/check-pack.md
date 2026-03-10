# check-pack

> 이 pack은 runtime skill이 아니다.
> `check-*` 카테고리와 review 계열 workflow를 함께 고르기 위한 카탈로그다.

## 이 pack이 맡는 경계

- 구현 없이 품질, 위험, 경계, 실패 경로를 점검한다.
- findings와 gate evidence를 남긴다.

## core runtime surface

- `check-merge-ready`
- `check-quality-scan`
- `check-ship-risk`
- `check-security-holes`
- `check-module-walls`
- `check-failure-paths`
- `check-delivered`
- `wf-check-full-review`
- `wf-check-with-checklist`

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 구조/품질 종합 리뷰 | `wf-check-full-review` |
| 리뷰 + 9항목 체크리스트 | `wf-check-with-checklist` |
| 최종 계약 검증 | `check-delivered` |
| 보안만 점검 | `check-security-holes` |

## 대표 매크로

```text
$compose + $wf-check-full-review + $check-delivered
```
