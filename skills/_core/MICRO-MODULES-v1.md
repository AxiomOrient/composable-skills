# Skill Fusion Micro-Modules v1

## Module Signature (fixed)
```text
module: <name>
inputs: <STATE fields read>
outputs: <STATE fields written>
side-effects: <none | explicit list>
gates: <policies to check>
```

## Stage Modules
- preflight: `m.preflight.repo-safety`, `m.preflight.scope-lock`, `m.preflight.approval-check`
- detect: `m.detect.tooling`, `m.detect.verify-map`, `m.detect.data-model-surface`
- analyze: `m.analyze.evidence-scan`, `m.analyze.evidence-or-hypotheses`, `m.analyze.risk-map`
  - `m.analyze.evidence-or-hypotheses`: 원인 명확도 triage → 명확하면 evidence trail, 불명이면 hypotheses-rank 적용
- plan: `m.plan.acceptance-criteria`, `m.plan.options-compare`, `m.plan.atomic-steps`
- implement: `m.implement.minimal-patch-design`, `m.implement.patch-apply`, `m.implement.rollback-plan`
- verify: `m.verify.narrow`, `m.verify.broader-if-risk`, `m.verify.capture-results`
- review: `m.review.p0p1p2`, `m.review.gate-check`, `m.review.perf-notes`
- reflect: `m.reflect.missed-assumptions`, `m.reflect.rca-lite`, `m.reflect.update-playbook`
- handoff: `m.handoff.next-actions`, `m.handoff.context-pack`
- audit: `m.audit.contract-check`, `m.audit.claim-evidence-check`, `m.audit.lens-check`, `m.audit.self-critique`, `m.audit.self-fix`, `m.audit.reprint-final`

## Usage Rule
Use modules as atomic actions and bind them to stage contracts.
Do not create large monolithic "do everything" actions.
