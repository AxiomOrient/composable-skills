# doc-pack

> 이 pack은 runtime skill이 아니다.
> `doc-*` 카테고리를 prefix 기준으로 고를 수 있게 만든 카탈로그다.

## 이 pack이 맡는 경계

- 문서 작성, 인덱싱, 큐레이션, 루트 README 게시를 분리한다.
- 런타임 코드 수정을 하지 않는다.

## core runtime surface

- `doc-write`
- `doc-build-index`
- `doc-curate`
- `doc-find-all`
- `doc-publish-readme`

## 이렇게 고르면 된다

| 지금 필요한 것 | 먼저 쓸 것 |
|---|---|
| 일반 문서 작성 | `doc-write` |
| 계층형 인덱스 문서 | `doc-build-index` |
| 문서 구조 정리 | `doc-curate` |
| 문서 현황 스캔 | `doc-find-all` |
| 루트 README + 다국어 entry docs | `doc-publish-readme` |

## 대표 매크로

```text
$compose + $doc-build-index
```
