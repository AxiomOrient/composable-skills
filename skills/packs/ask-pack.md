# ask-pack

> 이 pack은 runtime skill이 아니다.
> `ask-*` 질문 설계 카테고리를 바로 고를 수 있게 묶어 둔 카탈로그다.

## 이 pack이 맡는 경계

- 답보다 질문 품질을 먼저 다듬는다.
- 구현, 리뷰, 릴리즈 판단은 하지 않는다.

## core runtime surface

- `ask-find-question`
- `ask-break-it-down`
- `ask-flip-assumption`
- `ask-fix-prompt`
- `wf-ask-get-clear`
- `wf-ask-sharpen`

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 질문 자체가 안 나온다 | `wf-ask-get-clear` |
| 질문을 더 날카롭게 만들고 싶다 | `wf-ask-sharpen` |
| 이미 받은 답이 약했다 | `ask-fix-prompt` |

## 대표 매크로

```text
$compose + $wf-ask-sharpen
```
