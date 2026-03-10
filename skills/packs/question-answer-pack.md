# question-answer-pack

> 이 pack은 runtime skill이 아니다.
> 질문과 답변 준비를 위한 `추천 묶음`을 설명하는 카탈로그다.

## 누구를 위한 pack인가

- 무슨 질문을 해야 할지 막막한 사람
- 질문은 있는데 너무 넓거나 목적이 섞여 있는 사람
- 한 번 받은 답이 별로라서 질문을 최소 수정하고 싶은 사람

## 이 pack의 철학

- 답을 대신 내놓지 않는다.
- 질문자가 스스로 질문의 핸들을 잡게 만든다.
- 길고 똑똑해 보이는 질문보다, 짧고 본질적인 질문을 우선한다.
- 질문은 `선명화 -> 분해 -> 관점 전환` 순서로 다룬다.

## 추천 runtime surface

### Core atomic

- `ask-find-question`: 막연한 생각을 한 문장 문제 정의로 줄인다
- `ask-break-it-down`: 큰 질문을 3~5개의 작은 질문으로 쪼갠다
- `ask-flip-assumption`: 숨은 가정을 뒤집어 두 개의 도전적 질문을 만든다
- `ask-fix-prompt`: 약한 답이 나온 뒤 질문을 최소 수정한다

### Core workflow

- `wf-ask-get-clear`: 막연한 주제를 문제 정의 + 질문 스택으로 만든다
- `wf-ask-sharpen`: 문제 정의 + 질문 스택 + 관점 전환까지 한 번에 만든다

## 일반 사용자에게는 이렇게 추천한다

| 지금 상태 | 먼저 쓸 것 |
|---|---|
| 너무 막막해서 질문 자체가 안 나온다 | `wf-ask-get-clear` |
| 질문은 만들고 싶은데 더 날카롭게 만들고 싶다 | `wf-ask-sharpen` |
| 이미 받은 답이 약했다 | `ask-fix-prompt` |

## 추천 매크로

```text
$compose + $wf-ask-get-clear
```

```text
$compose + $wf-ask-sharpen
```

```text
$compose + $ask-fix-prompt
```

## 다음에 볼 문서

- 조합 예시: [`../SKILL-COMBOS.md`](../SKILL-COMBOS.md)
- atomic 설명: [`../ATOMIC-SKILLS.md`](../ATOMIC-SKILLS.md)
- 전체 안내: [`../README.md`](../README.md)
