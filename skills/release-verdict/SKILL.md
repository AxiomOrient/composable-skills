---
name: release-verdict
description: "Use when assessing release safety, rollout risk, compatibility impact, and rollback readiness. Use it for release verdict analysis, not for publication execution."
---

# Release / Verdict

## Purpose
Judge release safety and rollback readiness.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: diff|repo |
 policy: evidence,safety-gates,quality-gates{compat,docs,security,tests},deterministic-output |
 lens: release-gatekeeper |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `release-gatekeeper` because it keeps the work aligned with: Treat release as a sequence of explicit gates and judge only the gate in scope with concrete evidence.

## Use When
- Need rollout, impact, or rollback judgement before release.
- Need a release verdict grounded in release evidence.
- Need rollout, interface, and monitoring checks before deployment.

## Do Not Use When
- Need direct implementation or bug debugging.
- Need only repository or docs hygiene checks — use release-check-hygiene instead.
- Need actual branch, tag, or release publication execution — use release-publish instead.
- Need only diff/PR gate audit without rollout or rollback judgment — use check-release-risk instead.

## Required Inputs
- `RELEASE_SCOPE` (diff|repo|deployment-slice; required): Release scope under evaluation.
- `ROLLOUT_PLAN` (string; required): Intended rollout path.
- `ROLLBACK_PATH` (string; required): Rollback or stop strategy.
- `KNOWN_GATES` (list; optional; shape: {GATE, STATUS, EVIDENCE}): Known tests, docs, approval, compatibility, or security signals.

## Input Contract Notes
- RELEASE_SCOPE should stay bounded to the actual release candidate under consideration.
- ROLLOUT_PLAN and ROLLBACK_PATH should describe real operational paths, not aspirational placeholders.
- KNOWN_GATES should cite observable gate evidence rather than predicted success.

## Structured Outputs
- `BLAST_RADIUS` (string; required): Affected users, systems, or consumer radius.
- `ROLLBACK_CHECKLIST` (list; required; shape: {STEP, PURPOSE}): Rollback conditions and procedure.
- `RELEASE_DECISION` (go|no-go|blocked; required; allowed: go|no-go|blocked): Go, no-go, or blocked decision with rationale.

## Output Contract Notes
- RELEASE_DECISION should remain blocked when a required gate is unresolved rather than optimistic by default.
- ROLLBACK_CHECKLIST should describe actual recovery steps, not generic rollback slogans.
- BLAST_RADIUS should reflect the real release slice and consumer impact.

## Primary Lens
- `primary_lens`: `release-gatekeeper`
- `why`: Release decisions should center on blast radius, rollback readiness, and delivery stability signals.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: release-decision.v1

## Neutrality Rules
- Separate observed release evidence from the release verdict.
- If rollback or monitoring evidence is missing, mark the decision as blocked.
- Do not imply release readiness when approval or safety gates are unresolved.

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

결과부터: **출시 가능** / **출시 불가** / **중단**

영향 범위 한 줄로: [누가/무엇이 어느 정도 영향받는지]

중단 사유가 있으면:
- [검사 항목] — [문제] — 심각도: [높음/보통]

롤백(되돌리기) 체크리스트: 단계 → 이유

끝에: "롤백 경로 확인됐나요? 승인이 필요한 항목이 있나요?"

## Execution Constraints
- Do not mutate branches, tags, remotes, or release hosts from this skill.
- Keep rollout and rollback judgement explicit and evidence-backed.
- Do not convert hygiene or repository precondition gaps into hidden assumptions.
