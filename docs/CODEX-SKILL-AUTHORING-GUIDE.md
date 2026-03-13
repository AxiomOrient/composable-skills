# Codex Skill Authoring Guide

이 저장소의 직접 source-of-truth는 각 스킬 폴더 자체다.

- `skills/<name>/SKILL.md`: 사람이 읽는 지시문
- `skills/<name>/skill.json`: 기계가 읽는 메타데이터
- `skills/_meta/lenses.json`

## 기본 원칙

- 한 스킬은 한 가지 일만 한다.
- `description`은 trigger surface다.
- 입력과 출력은 명시적으로 잡는다.
- 분석/리뷰 계열은 근거와 추론을 섞지 않는다.
- `SKILL.md`는 짧고 명령형으로 유지한다.

## skill.json 에 꼭 있어야 하는 것

- `name`
- `layer`
- `default_program`
- `required_inputs`
- `display_name`
- `browse_category`
- `browse_priority`
- `is_category_default`
- `codex_surface`
- `starter_inputs`

workflow면 추가로:

- `expands_to`

## 새 skill 뼈대 만들기

기본은 dry-run 이다.

```bash
python3 scripts/skills.py new build-example --layer atomic
```

실제로 만들려면 `--write`를 붙인다.

```bash
python3 scripts/skills.py new build-example --layer atomic --write
```

생성물은:

- `skills/<name>/SKILL.md`
- `skills/<name>/skill.json`

이 scaffold 는 일부러 placeholder 상태로 만들어진다.
placeholder 를 실제 계약으로 바꾸기 전에는 `python3 scripts/skills.py validate` 가 통과하지 않는다.
또 `agents/openai.yaml` 도 `SKILL.md` 와 `skill.json` 에 맞게 유지되어야 한다.
runtime install 에서는 `sync` 가 그 파일을 direct contract 기준으로 다시 렌더링한다.
source repo 에서 그 파일이 빠져 있어도 `validate` 와 `sync` 는 direct contract 기준으로 계속 동작한다.

drift 를 수동으로 고치기 싫다면 먼저 dry-run:

```bash
python3 scripts/skills.py refresh-agent-yaml workflow-build-implement-and-guard
```

문제가 없으면 `--write` 로 반영한다.

## 어떻게 검증하나

```bash
python3 scripts/skills.py validate
```

이 검사는:

- 모든 skill folder에 `skill.json`이 있는지
- `SKILL.md`의 Default Program이 메타데이터와 맞는지
- `_meta`의 lens metadata가 유효한지

## 어떻게 sync 하나

```bash
./scripts/sync.sh
```

또는 직접:

```bash
python3 scripts/skills.py sync ~/.agents
```

sync는 현재 runtime surface만 설치하고, repo 내부의 불필요한 생성물은 설치하지 않는다.
