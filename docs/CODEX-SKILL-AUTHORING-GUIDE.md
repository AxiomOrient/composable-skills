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

판정 enum 출력이 있는 스킬은 선택적으로:

- `outputs` — enum 값이 고정된 필드만 등록한다 (`check-output` 검증 대상)

```json
"outputs": [
  {
    "name": "INTEGRATE_OR_HOLD",
    "required": true,
    "allowed_values": ["integrate", "hold"],
    "description": "Final review stance."
  }
]
```

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

## Eval Cases — workflow 스킬 필수 섹션

모든 workflow/control 레이어 스킬은 `SKILL.md` 끝에 `## Eval Cases` 섹션을 포함해야 한다.
`validate` 가 이 섹션이 없으면 경고를 낸다.

```markdown
## Eval Cases

| Prompt | Should Trigger | Key Output Check |
|--------|---------------|-----------------|
| <YES 트리거 프롬프트 1> | YES | <출력 필드명> 존재 |
| <YES 트리거 프롬프트 2> | YES | <출력 필드명> 존재 |
| <경계 케이스 — 트리거 안 돼야 하는 것> | NO | <이유 + 대안 스킬> |
```

목적:
- **트리거 정밀도** — 어떤 요청이 이 스킬을 선택해야 하는지, 어떤 것은 선택하면 안 되는지 명시
- **출력 기대값** — 스킬 실행 후 어떤 필드가 반드시 있어야 하는지 기록

## 어떻게 검증하나

```bash
python3 scripts/skills.py validate
```

이 검사는:

- 모든 skill folder에 `skill.json`이 있는지
- `SKILL.md`의 Default Program이 메타데이터와 맞는지
- `_meta`의 lens metadata가 유효한지
- workflow 레이어 스킬에 `## Eval Cases` 섹션이 있는지

### LLM 출력 계약 검증

`outputs` 스키마가 있는 스킬은 실제 LLM 출력을 바로 검증할 수 있다:

```bash
# PASS 예시
python3 scripts/skills.py check-output workflow-review-change '{"INTEGRATE_OR_HOLD": "integrate"}'

# FAIL 예시 — 허용값 외
python3 scripts/skills.py check-output release-verdict '{"RELEASE_DECISION": "yes"}'
```

현재 `outputs` 스키마가 등록된 스킬:

| 스킬 | 필드 | 허용값 |
|------|------|--------|
| `workflow-review-change` | `INTEGRATE_OR_HOLD` | integrate, hold |
| `workflow-review-complete` | `FINAL_VERDICT` | integrate, hold |
| `workflow-check-with-checklist` | `INTEGRATE_OR_HOLD` | integrate, hold |
| `release-verdict` | `RELEASE_DECISION` | go, no-go, blocked |
| `release-check-repo` | `REPO_RELEASE_STATUS` | ready, blocked, inconclusive |

## 어떻게 sync 하나

```bash
./scripts/sync.sh
```

또는 직접:

```bash
python3 scripts/skills.py sync ~/.agents
```

sync는 현재 runtime surface만 설치하고, repo 내부의 불필요한 생성물은 설치하지 않는다.
