# Skill Fusion Contract v1.2

## 1) MECE Axes (Do not mix)

- Stage: procedural pipeline (`preflight > detect > analyze > plan > implement > verify > review > reflect > handoff > audit`)
- Policy: invariants and gates
- Lens: prioritized reasoning style translated into enforceable artifacts
- Scope: `repo | diff | paths(glob,...)`
- Output: `md(contract=v1) | json(schema=v1) | both`

## 2) Program DSL v1

```text
[stages: preflight>detect>analyze>plan>implement>verify>review>reflect>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,correctness-first,quality-gates{tests,security},safety-gates,approval-gates{explicit,no-fallback},perf-aware,deterministic-output,response-contract{plain-korean,feynman-clear,actionable,core-first,short-sentences,plain-words,concrete-details} |
 lens: hickey-carmack |
 output: md(contract=v1) ]
```

### Operators

- `@panel(k)`: stage-local multi-view synthesis (`analyze@panel(3)`). Resolve disagreements in `check-ship-risk`.
- `loop(limit=n){...}`: repeat a sub-pipeline with policy-based stop conditions.

### Normalization

- No alias normalization is applied.
- Tokens must match the canonical DSL exactly.

## 3) Deterministic Execution Rules

1. Parse -> normalize -> fill defaults.
2. Resolve policies by priority and hardness.
3. Execute stages left-to-right.
4. Emit Stage Contract for each stage.
5. Build final-response payload according to `RESPONSE-CONTRACT-v1.md`; user-facing rendering is delegated to `respond`.
6. Run audit internally, apply fixes internally, and emit one final internal stage payload. Only the 'respond' skill is allowed to format and emit the user-facing output.
7. If target is outside scope, output `uncertain` plus the cheapest verification step.
8. If `safety-gates` triggers, stop before destructive or irreversible actions and request approval.
9. If a required command is blocked by permissions/sandbox, request explicit user approval and do not bypass via `/tmp`, stubs, mocks, or fake-success reports.
10. Any skill that produces user-facing strings must defer formatting to the 'respond' skill. The final output language must be Korean unless explicitly requested otherwise.
11. If `response-contract{...}` is active, final user output must conform to `RESPONSE-CONTRACT-v1.md` writing rules and the resolved profile order from `RESPONSE-PROFILES-v1.md`.
12. Hide internal stage logs and internal correction wording unless the user explicitly asks for trace/full-contract output.
13. If any stage produces blockers/questions, surface them in final output as `확인 질문` (numbered list). If direct questioning is not possible, persist them to `docs/CLARIFYING_QUESTIONS.md` and include that path in the response.

## 4) STATE (Visible)

```text
STATE = {
  program, scope_lock, data_model, evidence, hypotheses,
  risks(P0/P1/P2), plan, changes, verification_map,
  results, rollback, next_actions, blockers, policy_resolution
}
```

## 5) Stage Contract v1 (STRICT)

```markdown
- Result: (1-5 lines)
- Evidence: (file/command/log/measurement or verification step)
- Next: (1-3 inputs/decisions for next stage)
- Blockers: (max 3 questions, or None)
```

## 6) Final Output Contract v1

Internal trace contract (internal or explicit trace requests only):

```markdown
## Parsed Program

## Policy Resolution

## Stage Logs

## Final Deliverables

## Risks & Rollback

## Next Actions

## Audit Notes (internal)
```

External user contract:

- Use `RESPONSE-CONTRACT-v1.md` writing rules and `RESPONSE-PROFILES-v1.md` section order.
- Keep language plain, concise, and Korean by default.
- Emit one final response only via the 'respond' skill.

## 7) Policy Stack (Priority, Hardness)

1. `safety-gates` (100, HARD)
2. `deterministic-output` (95, HARD)
3. `response-contract{...}` (92, HARD when present)
4. `evidence` (90, HARD)
5. `approval-gates{...}` (85, HARD)
6. `quality-gates{...}` (80, HARD)
7. `perf-aware` (60, SOFT -> HARD conditionally)
8. `correctness-first` (50, SOFT)

### Conflict Resolution

- HARD vs SOFT: HARD wins.
- HARD vs HARD: higher priority wins and loser is recorded.
- `correctness-first` never waives any HARD policy.
- `perf-aware(HARD)` outranks `correctness-first`.

### Policy Details

- `safety-gates`: block destructive or irreversible actions until approval.
- `deterministic-output`: emit contract-compliant final output if violated.
- `response-contract{plain-korean,feynman-clear,actionable,core-first,short-sentences,plain-words,concrete-details}`:
  - final response must be plain, concise, actionable, and easy to read.
  - use Korean by default.
  - `concrete-details`: use file names, line numbers, function names, and measurements instead of abstract descriptions. See RESPONSE-CONTRACT-v1.md for good/bad examples.
- `evidence`: every major claim requires evidence or a concrete verification procedure.
- `approval-gates{explicit,no-fallback}`: on permission-denied/sandbox block, ask for approval first and do not bypass with `/tmp`, stubs, mocks, or fake checks.
- `quality-gates{...}`: if empty, default to `{tests,security}`.
- `perf-aware`: hardens only when hot-path evidence exists, or user marks hot path and accepts measurement.
- `correctness-first`: prioritize correctness and maintainability over diff size; broad renewal/refactoring is allowed when it is the most reliable path under active HARD policies.

## 8) Public Entrypoint Rule

- Use explicit `wf-*` workflows or explicit skill macros on the public compose surface.
- Do not add alternate shorthand entry syntaxes to new macros.
- Canonical public entry examples:
  - review: `$compose + $wf-check-full-review + @src + $check-delivered`
  - debug: `$compose + $wf-debug-this + @src/auth + [session disappears after refresh]`
  - improvement-map: `$compose + $wf-tidy-find-improvements + @src/auth`
  - question-ready: `$compose + $wf-ask-sharpen + $check-delivered`

## 9) Lens Enforcement

- Canonical lens registry (single source of truth): `skills/_core/lenses.json`.
- Compose parser validates `lens:<id>` and `required_artifacts` against that registry.
- `hickey-carmack`: include `Data Model`, `Transformations vs Side Effects`, `Perf Notes`. Apply `principles` from lenses.json across all stages.
- `ive`: include `Intent (1 sentence)`, `Primary Flow`, `Edge States`, `System Rules`.
- `feynman`: include `Repro Steps`, `Observed vs Expected`, `Hypotheses + Falsification Tests`, `Regression Guard`.
- `sinek-miller`: include `Why-How-What`, `StoryBrand 7 (character/problem/guide/plan/cta/success/failure)`, `Message Fit`.
- `eisenhower`: include `Priority Matrix (urgent/important)`, `Critical Path`, `Decision Gates`.
- `uncle-bob`: include `Boundary Map`, `Dependency Direction`, `Refactor Safety Notes`.
- `karpathy`: include `Data Pipeline`, `Eval Metrics`, `Failure Buckets`.
- `kent-beck`: include `Red-Green-Refactor Plan`, `Test Intent`, `Small Safe Steps`.
- `nielsen-norman`: include `Heuristic Mapping (10 checks)`, `Usability Risks`, `Mitigation Actions`.
- `wardley`: include `Value Chain Map`, `Evolution Stage Map`, `Strategic Moves`.
- `ries-lean`: include `Hypothesis`, `Experiment Plan`, `Build-Measure-Learn Decision (pivot/persevere)`.
- `christensen-jtbd`: include `Job Statement`, `Current Alternatives`, `Switching Trigger + Success Criteria`.
- `shape-up`: include `Shaped Pitch`, `Appetite`, `Hill Chart / Bet Scope`.
- `sre-dora`: include `SLO/Error Budget Note`, `DORA Signal Set`, `Reliability Risks + Mitigations`.
- `aws-well-architected`: include `Pillar-by-Pillar Tradeoff Note`, `Risk Register`, `Remediation Priorities`.
- `nist-rmf`: include `System Categorization`, `Control Selection/Status`, `Continuous Monitoring Plan`.
- `goldratt-toc`: include `Constraint Identification`, `Throughput Impact`, `Exploit/Subordinate/Elevate Plan`.
- `ideo-design-thinking`: include `User Insight Summary`, `Prototype Plan`, `Learning Loop`.
- `fowler-strangler`: include `Modernization Outcomes`, `Seam Plan`, `Incremental Cutover Steps`.

## 9.1 Default Lens Source

- Do not duplicate category defaults in this file.
- Canonical default lens mapping lives only in `skills/_core/lenses.json` under `defaults`.

## 10) Mandatory Audit Procedure

Use this instruction in the audit step (internal only):
`Run an internal audit now: identify exactly 3 concrete defects (assumption error, missing evidence, or contract violation), apply complete fixes, and emit one final internal stage payload.`

Do not expose audit/correction wording in normal user output.

Then execute:

1. Contract completeness check:
   - required sections exist and respect strict order.
2. Claim-evidence check:
   - every major conclusion/risk/recommendation has evidence or a concrete verification step.
3. Lens artifact check:
   - all required artifacts for the selected lens are present.
4. List exactly 3 concrete defects.
5. Apply complete fixes.
6. Emit only one final internal stage payload.
