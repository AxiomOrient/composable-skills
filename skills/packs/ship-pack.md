# ship-pack

> 이 pack은 runtime skill이 아니다.
> `ship-*` 카테고리와 릴리즈 workflow를 prefix 기준으로 묶는다.

## 이 pack이 맡는 경계

- git 현실, hygiene, GO/NO-GO, publish를 분리한다.
- 검토와 publish를 섞지 않는다.

## core runtime surface

- `ship-check-repo`
- `ship-check-hygiene`
- `ship-go-nogo`
- `ship-commit`
- `release-publish`
- `wf-ship-ready-check`
- `wf-ship-it`

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| git/repo 현실 확인 | `ship-check-repo` |
| docs/public surface hygiene 점검 | `ship-check-hygiene` |
| 출시 가능 여부 판단 | `ship-go-nogo` |
| 검토만 하고 싶다 | `wf-ship-ready-check` |
| 검토 후 publish까지 간다 | `wf-ship-it` |

## 대표 매크로

```text
$compose + $wf-ship-ready-check + $check-delivered
```
