# release-pack

> 이 pack은 runtime skill이 아니다.
> 릴리즈를 `git 현실 확인`, `release hygiene`, `GO/NO-GO 판단`, `실제 publish`로 나눠 설명하는 카탈로그다.

## 이 pack의 핵심 구조

릴리즈의 핵심 검토는 `3개 atomic + 1개 utility`로 유지하고, 사용자는 그 위에 올라간 `2개 workflow entrypoint` 중 하나를 고른다.

1. `ship-check-repo`
git repo, 브랜치, remote, tag 상태를 본다.

2. `ship-check-hygiene`
문서 업그레이드, 레거시 제거, public surface sync를 본다.

3. `ship-go-nogo`
이제 출시해도 되는지 `go / no-go / blocked`로 판단한다.

4. `release-publish` (utility)
검토를 통과한 변경을 release-only 커밋, 태그, GitHub release로 정리한다.

## workflow entrypoint

1. `wf-ship-ready-check`
검토만 한다.

2. `wf-ship-it`
검토 후 release-only 커밋, 태그, publish까지 간다.

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 지금 릴리즈 작업을 걸 수 있는 저장소 상태인지 | `ship-check-repo` |
| 문서와 public surface가 정리됐는지 | `ship-check-hygiene` |
| 출시해도 되는지 판단 | `ship-go-nogo` |
| 검토만 투명하게 보고 싶다 | `wf-ship-ready-check` |
| 검토 후 실제 태그와 release publish까지 하고 싶다 | `wf-ship-it` |
| 이미 검토는 끝났고 publish stage만 직접 제어하고 싶다 | `release-publish` |

## 권장 흐름

### 릴리즈 검토만 할 때

```text
$compose + $wf-ship-ready-check + $check-delivered
```

### 검토 후 실제 publish까지 갈 때

```text
$compose + $wf-ship-it + $check-delivered
```

## 기본 원칙

- git 현실 확인 없이 릴리즈를 시작하지 않는다.
- 문서 업그레이드가 release gate라면, 문서가 끝나기 전에는 publish하지 않는다.
- 레거시 이름이나 stale public surface가 남아 있으면 hygiene blocker로 본다.
- `main`이 release-only 브랜치라면 publish는 single release commit 기준으로 정리한다.
- 검토와 publish를 모두 원하면 `wf-ship-it`을 기본 entrypoint로 쓴다.

## 다음에 볼 문서

- 조합 예시: [`../SKILL-COMBOS.md`](../SKILL-COMBOS.md)
- atomic 설명: [`../ATOMIC-SKILLS.md`](../ATOMIC-SKILLS.md)
- 전체 안내: [`../README.md`](../README.md)
