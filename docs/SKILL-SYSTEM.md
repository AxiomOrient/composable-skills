# Skill System

현재 시스템의 핵심은 단순하다.

## Source Of Truth

- per-skill human contract: `skills/<name>/SKILL.md`
- per-skill machine contract: `skills/<name>/skill.json`
- shared machine metadata: `skills/_meta/*.json`

generated catalog, generated guides, registry materialization은 더 이상 runtime의 기준이 아니다.

## Layers

- `atomic`: 한 문제, 한 출력
- `workflow`: 반복 조합에 이름을 붙인 public entry
- `utility`: orchestration, sync, render, control

## 운영 원칙

- 한 스킬은 한 가지 일만 한다.
- workflow expansion은 숨기지 않는다.
- public entry surface는 작게 유지한다.
- analysis/review 계열은 evidence-first로 간다.

## No Pack Layer

새 runtime layer로 `pack`은 두지 않는다.
도메인 설명이 더 필요하면 README나 skill metadata를 정리한다.

## Validation

- `scripts/skills.py validate`
- `scripts/validate.sh`

이 두 경로가 direct metadata 기반 구조를 검증한다.
