# Spec Pack

이 pack은 `기획서`, `기능 명세`, `IA`, `기술 설계`를 한 문서로 뭉개지 않고, 각각 다른 질문에 답하는 문서로 나눈다.

핵심 원칙은 간단하다.

- `왜`를 먼저 정리한다
- `무엇을 해야 하는지`를 그다음 적는다
- `어떻게 이동하고 묶이는지`를 구조로 정리한다
- `어떻게 만들지`는 마지막에 기술 설계로 적는다

## 어떤 스킬이 무엇을 맡나

| 스킬 | 답하는 질문 | 보통 언제 먼저 쓰나 |
|---|---|---|
| `plan-why-build-this` | 왜 만들고, 누구를 위한 일인가 | 문제, 사용자, 성공 기준이 흐릴 때 |
| `plan-what-it-does` | 정확히 무엇을 해야 하는가 | 기능 요구사항과 acceptance를 고정할 때 |
| `plan-screen-map` | 사용자는 어디서 들어와 어떻게 이동하는가 | 화면, 페이지, 섹션 구조가 헷갈릴 때 |
| `plan-how-to-build` | 시스템은 이 요구사항을 어떻게 만족시키는가 | 구현 전에 기술 경계와 trade-off를 맞출 때 |

## 언제 전부 다 쓰지 않아도 되나

- 간단한 내부 기능이면 `plan-why-build-this + plan-what-it-does`만으로 충분할 수 있다.
- 구조가 핵심인 웹/앱 기능이면 `plan-why-build-this + plan-screen-map + plan-what-it-does`가 먼저다.
- 구현 난도가 높거나 경계가 많으면 `plan-what-it-does + plan-how-to-build`를 붙인다.

항상 네 문서를 모두 만들려고 하지 말고, 지금 막힌 질문에 맞는 문서만 추가하는 편이 낫다.

## 가장 많이 쓰는 조합

### 1. 아직 문제 정의가 흐릴 때

```text
$compose + $plan-why-build-this
```

### 2. 기능 명세까지 필요할 때

```text
$compose + $plan-why-build-this + $plan-what-it-does
```

### 3. 구조와 흐름까지 먼저 잡아야 할 때

```text
$compose + $plan-why-build-this + $plan-screen-map + $plan-what-it-does
```

### 4. 구현 전에 기술 설계까지 맞춰야 할 때

```text
$compose + $plan-why-build-this + $plan-what-it-does + $plan-how-to-build + $check-delivered
```

## 어떤 순서가 자연스러운가

1. `plan-why-build-this`
2. `plan-screen-map` 필요 여부 판단
3. `plan-what-it-does`
4. `plan-how-to-build` 필요 여부 판단
5. 마지막에 `$check-delivered`

## 한 줄로 고르는 법

- 왜가 흐리면 `plan-why-build-this`
- 뭐가 흐리면 `plan-what-it-does`
- 구조가 흐리면 `plan-screen-map`
- 구현 방식이 흐리면 `plan-how-to-build`
