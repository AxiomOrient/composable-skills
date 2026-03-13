# composable-skills 검토 보고서

## 0. 작업 게이트 확인

- 요청한 커밋 `9d6798c`는 저장소 커밋 히스토리에서 확인되었다.
- 따라서 분석을 계속 진행했다.

## 1. 총평

**판정: `Codex-compatible + repo-specific overlay` 로는 타당하다.  
다만 `Codex-native spec 그대로`라고 보기에는 과장이다.**

왜냐하면:

1. **Codex가 실제로 요구하는 최소 계약**은 `SKILL.md`(front matter의 `name`, `description`)와 선택적 `agents/openai.yaml`, `scripts/`, `references/`, `assets/`다.
2. 이 저장소는 그 위에 `skill.json`, `_meta/lenses.json`, `scripts/skills.py`, `scripts/sync.sh`를 얹어서 **자체 런타임/동기화/검증 계층**을 만든다.
3. 따라서 이 저장소는 **Codex 스킬 규격을 잘 활용한 커스텀 프레임워크**이지, `skill.json` 자체가 Codex 표준이라는 뜻은 아니다.

즉, 현재 구조는 **사용 가능**하고 **잘 설계된 부분이 많다**.  
하지만 **스킬 경계가 너무 잘게 분해된 곳이 많고**, 일부는 **문서/머신 메타데이터/expands_to 간 불일치**가 있어 정리 필요성이 높다.

---

## 2. Codex Skills 적합성 평가

### 2.1 합격 요소

- `SKILL.md` 중심 구조를 채택했다.
- front matter에 `name`, `description`가 들어간 패턴을 일관되게 사용한다.
- `Use When / Do Not Use When / Required Inputs / Structured Outputs / Neutrality Rules / Execution Constraints`가 있어 **작업 경계가 명시적**이다.
- workflow / atomic / utility / internal_control 계층을 둬서 **진입면과 내부 조합면을 분리**하려는 의도가 좋다.
- `scripts/skills.py`가 `SKILL.md`와 `skill.json` drift, 렌즈 유효성, `openai.yaml` 파생 규칙을 검증하도록 설계되어 있어 **운영 일관성**이 높다.

### 2.2 주의 요소

- `skill.json`은 **Codex-native 표준이 아니라 저장소 로컬 계약**이다.
- `_meta/lenses.json`과 `default_program` DSL도 **repo-specific overlay**다.
- `agents/openai.yaml`는 sync 시 파생 생성되므로, **이 저장소를 그대로 압축 업로드/복사할 때와 sync 후 Codex에 설치했을 때의 표면이 완전히 동일하다고 가정하면 안 된다.**
- Codex는 스킬 발견 시 **모든 스킬의 metadata(`name`, `description`, path)를 먼저 본다.**  
  즉 **스킬 수가 많을수록 discovery cost와 implicit matching ambiguity가 증가**한다.

### 2.3 내 결론

- **“Codex skills에 적합하게 생성됐는가?” → 예, 다만 “표준 스킬 + 커스텀 메타 레이어”로 보는 것이 정확하다.**
- 현재 저장소는 **authoring/runtime framework**로는 좋다.
- 그러나 **core pack 관점에서는 skill count를 줄이고 경계를 다시 그어야 한다.**

---

## 3. 핵심 발견

### 3.1 현재 스킬 수는 과하다

현재 `skills/`에는 총 **72개 스킬 디렉터리**가 있다.  
문제는 절대 개수 자체보다, **암묵적 선택 대상이 너무 많아진다**는 점이다.  
Codex는 스킬 전체의 metadata를 먼저 보므로, workflow를 잘 만들더라도 너무 많은 근접 스킬은 선택 품질을 떨어뜨린다.

### 3.2 가장 큰 장점

현재 저장소의 가장 좋은 점은 다음 두 가지다.

- **설명 계약이 매우 명시적**이다.
- **workflow → atomic 조합 구조를 실제로 운영 가능하게 만든다.**

즉, 방향은 맞다.  
지금 필요한 것은 **전면 폐기**가 아니라 **경계 압축(boundary compression)** 이다.

### 3.3 가장 큰 문제

#### A. 너무 좁은 micro-skill
예:
- `ask-break-it-down`
- `ask-flip-assumption`
- `tidy-find-copies`
- `tidy-find-magic-numbers`
- `test-design-cases`

이들은 유용한 “동작”이지만, **독립 discovery target**으로 놓기엔 너무 좁다.

#### B. modifier 성격인데 skill로 분리됨
예:
- `workflow-check-with-checklist`는 사실상 `workflow-check-full-review + checklist mode`
- `workflow-security-preflight`는 사실상 `check-security-holes`의 public wrapper
- `check-quality-scan`, `check-failure-paths`, `check-module-bounds`는 `review profile`로 흡수 가능한 성격

#### C. 문서와 머신 메타데이터의 surface 불일치
특히:
- 루트 README는 `build-until-done`, `finish-until-done`을 internal control surface처럼 설명한다.
- 그러나 실제 `skill.json`은 둘 다 `codex_surface=public_entry`다.
- `workflow-release-publish`는 `workflow-*` 이름을 쓰지만 실제는 `internal_control`이다.

#### D. workflow 설명과 expands_to 불일치
- `workflow-debug-this` 설명은 “수정 확인까지”라고 읽히는데, 실제 `expands_to`에는 `debug-confirm-fix`가 없다.
- 대신 `test-find-gaps`가 들어간다.  
  이것은 **의도와 실행 경로가 어긋난 대표 사례**다.

#### E. public_entry 입력 라우팅 결함
- `workflow-release-ready-check`는 `TARGET_BRANCHES`가 required인데 starter_inputs에서 이 필드를 매핑하지 않는다.
- 이건 실제 compose/input routing 관점에서 결함이다.

---

## 4. 설계 원칙: 앞으로의 atomic / workflow 기준

이 프로젝트를 계속 키우려면, 스킬 설계 기준을 먼저 고정해야 한다.

### 4.1 Atomic skill 기준

Atomic skill은 아래 조건을 만족해야 한다.

1. **하나의 주된 artifact 또는 verdict를 만든다.**
2. **한 문장으로 “이 스킬은 무엇을 끝내는가”를 설명할 수 있다.**
3. **입력 enum이나 mode로 흡수 가능한 차이는 별도 skill로 만들지 않는다.**
4. **workflow 밖에서도 재사용 가치가 있어야 한다.**

### 4.2 Workflow skill 기준

Workflow skill은 아래 조건을 만족해야 한다.

1. **사용자가 바로 이해하는 job-to-be-done**이어야 한다.
2. **2~5개 atomic 정도**로 구성되어야 한다.
3. public entry는 **카테고리당 1개 default workflow**를 우선한다.
4. “체크리스트 추가”, “보안만 보기”, “가정 뒤집기” 같은 것은 **workflow 분기 옵션**이지 workflow 이름 자체가 되지 않는 편이 좋다.

### 4.3 Control skill 기준

Control skill은 아래 조건으로 분리한다.

1. orchestration / looping / mutation / sync 전용
2. 기본 implicit invocation 대상이 아님
3. 명시 호출 또는 workflow 내부에서만 사용
4. 이름도 `workflow-*`처럼 보이지 않게 하는 편이 좋다

---

## 5. 내가 권하는 목표 구조

### 5.1 1차 목표: 총 72 → 총 50

보수적으로 줄여도 **72개를 50개 전후**까지 줄일 수 있다.  
핵심은 capability 삭제가 아니라 **중복 경계 통합**이다.

#### 목표 카운트

- Public workflows: **11**
- Expert atomics: **33**
- Control: **4**
- Extras: **2**
- 합계: **50**

### 5.2 2차 목표: 기본 활성 surface는 24개 안팎

전체 저장소 capability를 남기더라도, 실제 설치/동기화는 **profile 기반**으로 나눠야 한다.

권장 profile:

- `core`: planning/build/debug/review/test/tidy 중심
- `docs-release`: doc/release/security 중심
- `extras`: gemini/commit/perf/research helper

이렇게 하면 **repo capability는 유지하면서도 Codex에 노출되는 active surface를 크게 줄일 수 있다.**

---

## 6. 권장 target atomic set

아래는 내가 권하는 **1차 정리 후 atomic/control 목표 집합**이다.

### 6.1 Expert atomics (33)

#### Question
- `ask-clarify-question`
- `ask-fix-prompt`

#### Discovery / Scope
- `scout-scope-contract`
- `scout-structure-map`
- `scout-option-compare`
- `scout-evidence-gap`

#### Planning
- `plan-why-build-this`
- `plan-what-it-does`  ← acceptance criteria까지 포함하도록 확대
- `plan-screen-map`
- `plan-how-to-build`  ← dependency rules 포함하도록 확대
- `plan-task-breakdown` ← verify order 일부 흡수

#### Build / Perf
- `build-write-code`
- `build-make-faster` ← baseline 기능 일부 흡수

#### Debug
- `debug-capture-failure`
- `debug-find-root-cause` ← impact mapping 흡수
- `debug-confirm-fix`

#### Review / Verify
- `check-change-review`
- `check-security-holes`
- `check-final-verify`

#### Test
- `test-find-gaps` ← case design까지 포함하도록 확대
- `test-write-guards`
- `test-run-user-scenarios`

#### Tidy
- `tidy-analyze`
- `tidy-simplify`
- `tidy-reorganize`
- `tidy-remove-legacy`

#### Docs
- `doc-find-all`
- `doc-curate`
- `doc-write`

#### Release
- `release-check-repo`
- `release-check-hygiene`
- `release-verdict`
- `release-publish`

### 6.2 Control (4)

- `compose`
- `plan-sync-tasks`
- `control-build-until-done`
- `control-finish-until-done`

### 6.3 Extras (2)

- `gemini`
- `commit-write-message`

---

## 7. 권장 target workflow set

### 7.1 Public default workflows (11)

1. `workflow-clarify-request`
2. `workflow-scout-structure`
3. `workflow-plan-build-ready`
4. `workflow-build-implement-and-guard`
5. `workflow-build-execute-plan`
6. `workflow-debug-this`
7. `workflow-review-change`
8. `workflow-test-close-gaps`
9. `workflow-tidy-improvements`
10. `workflow-doc-systemize`
11. `workflow-release-ready-check`

### 7.2 Internal control workflow

- `control-release-publish-flow`  
  (`workflow-release-publish`를 internal 이름에 맞게 정리)

---

## 8. 현재 skill별 판정

아래 표는 **현재 스킬 하나하나에 대한 판정**이다.  
기준은 다음 6개다.

- **경계 타당성**
- **독립 discovery target 가치**
- **workflow 내부 sub-step로 충분한지**
- **현재 naming/surface와 codex_surface의 일치 여부**
- **다른 skill과의 중복 정도**
- **target 구조에서의 존치/통합 여부**

---

## 8.1 Ask family

| Current skill | Type | 현재 경계 평가 | 판정 | 권장 조치 | Target |
|---|---|---|---|---|---|
| ask-form-question | atomic | fog → one problem statement | 좋지만 너무 잘게 분해됨 | Merge | ask-clarify-question |
| ask-break-it-down | atomic | bounded question decomposition | 단독 discovery target으로는 약함 | Merge | ask-clarify-question |
| ask-flip-assumption | atomic | assumption challenge tactic | 유용하지만 tactic 성격 | Merge | ask-clarify-question |
| ask-fix-prompt | atomic | failed answer → repaired prompt | 명확하고 독립적 | Keep | ask-fix-prompt |
| workflow-ask-get-clear | workflow(expert) | form + break 흐름 | sharpen과 차이가 너무 작음 | Merge | workflow-clarify-request |
| workflow-ask-sharpen | workflow(public) | form + break + flip | default clarify workflow로는 적합 | Merge | workflow-clarify-request |

### Ask 결론
- ask 계열은 **4 atomic + 2 workflow가 아니라 2 atomic + 1 workflow**가 맞다.
- 질문 설계는 “form / break / flip”보다 **clarify / repair** 경계가 더 안정적이다.

---

## 8.2 Scout family

| Current skill | Type | 현재 경계 평가 | 판정 | 권장 조치 | Target |
|---|---|---|---|---|---|
| scout-scope | atomic | request/scope/done normalization | boundaries와 강하게 겹침 | Merge | scout-scope-contract |
| scout-boundaries | atomic | inclusion/exclusion boundary | scope와 강하게 겹침 | Merge | scout-scope-contract |
| scout-structure-map | atomic | current structure map | 경계 좋음 | Keep | scout-structure-map |
| scout-option-compare | atomic | explicit option comparison | 유효하지만 optional pack 후보 | Keep / Optional | scout-option-compare |
| scout-evidence-gap | atomic | missing evidence identification | 유효하지만 optional pack 후보 | Keep / Optional | scout-evidence-gap |
| scout-baseline | atomic | pre-improvement baseline measurement | performance mode에 더 가까움 | Absorb | build-make-faster |
| workflow-scout-structure | workflow(public) | scope + structure map | 자연스러운 흐름 | Keep | workflow-scout-structure |

### Scout 결론
- `scope`와 `boundaries`는 분리보다 **contract 하나**로 묶는 편이 낫다.
- `baseline`은 scout 계열보다 **perf/build 계열**에 두는 편이 더 자연스럽다.

---

## 8.3 Plan family

| Current skill | Type | 현재 경계 평가 | 판정 | 권장 조치 | Target |
|---|---|---|---|---|---|
| plan-why-build-this | atomic | product brief / problem framing | 좋음 | Keep | plan-why-build-this |
| plan-what-it-does | atomic | functional spec | acceptance criteria 역할이 부족함 | Keep / Widen | plan-what-it-does |
| plan-screen-map | atomic | UI / flow map | 좋음 | Keep | plan-screen-map |
| plan-how-to-build | atomic | technical design | dependency/data boundary를 흡수해야 함 | Keep / Widen | plan-how-to-build |
| plan-dependency-rules | atomic | dependency policy only | 너무 좁음 | Absorb | plan-how-to-build |
| plan-verify-order | atomic | verification sequence | 단독 atomic으로는 약함 | Absorb | plan-task-breakdown |
| plan-task-breakdown | atomic | execution-ready tasks | 좋음 | Keep / Widen | plan-task-breakdown |
| plan-sync-tasks | utility | tasks ledger sync | internal control로 적절 | Keep | plan-sync-tasks |
| workflow-plan-build-ready | workflow(public) | scope → spec → design → tasks | 현재 public planning entry로 가장 적절 | Keep | workflow-plan-build-ready |

### Plan 결론
- **새 skill을 추가할 필요는 없다.**
- 대신 `plan-what-it-does`에 **acceptance criteria / examples**를 넣고,
- `plan-how-to-build`에 **data shape / dependency rules / verification hooks**를 흡수하면 된다.

---

## 8.4 Build / control family

| Current skill | Type | 현재 경계 평가 | 판정 | 권장 조치 | Target |
|---|---|---|---|---|---|
| build-write-code | atomic | bounded implementation pass | 좋음 | Keep | build-write-code |
| build-make-faster | atomic | measured perf improvement | 좋음, 다만 optional perf pack 추천 | Keep / Optional | build-make-faster |
| build-until-done | atomic(public) | autonomous code loop | 기능은 좋지만 surface 분류가 문서와 충돌 | Reclassify | control-build-until-done |
| finish-until-done | atomic(public) | autonomous non-code loop | 기능은 좋지만 surface 분류가 문서와 충돌 | Reclassify | control-finish-until-done |
| workflow-build-implement-and-guard | workflow(public) | implement + guard | 좋음 | Keep | workflow-build-implement-and-guard |
| workflow-build-execute-plan | workflow(public) | execute task ledger | 좋음 | Keep | workflow-build-execute-plan |

### Build 결론
- `until-done` 류는 **좋은 skill**이지만 **public atomic이 아니라 control loop**로 보는 게 맞다.
- 이름도 `control-*`처럼 드러내는 편이 운영상 안전하다.

---

## 8.5 Debug family

| Current skill | Type | 현재 경계 평가 | 판정 | 권장 조치 | Target |
|---|---|---|---|---|---|
| debug-capture-failure | atomic | symptom → repro surface | 좋음 | Keep | debug-capture-failure |
| debug-map-impact | atomic | impact surface mapping | root-cause와 너무 밀접 | Merge | debug-find-root-cause |
| debug-find-root-cause | atomic | root cause analysis | 좋음 | Keep / Widen | debug-find-root-cause |
| debug-confirm-fix | atomic | prove fix | 좋음 | Keep | debug-confirm-fix |
| workflow-debug-this | workflow(public) | end-to-end debugging | expands_to가 설명과 어긋남 | Keep / Fix | workflow-debug-this |

### Debug 결론
- 디버그 atomic은 **3개면 충분**하다.
- 특히 `workflow-debug-this`는 **반드시 `debug-confirm-fix`를 포함하도록 수정**해야 한다.

---

## 8.6 Check / review family

| Current skill | Type | 현재 경계 평가 | 판정 | 권장 조치 | Target |
|---|---|---|---|---|---|
| check-merge-ready | atomic | review verdict anchor | 좋음 | Keep / Widen | check-change-review |
| check-quality-scan | atomic | checklist review | mode 성격 | Merge | check-change-review |
| check-failure-paths | atomic | unhappy-path review | mode 성격 | Merge | check-change-review |
| check-module-bounds | atomic | boundary review | mode 성격 | Merge | check-change-review |
| check-security-holes | atomic | security exposure review | distinct | Keep | check-security-holes |
| check-release-risk | atomic | release risk judgement | release-verdict와 중복 | Absorb | release-verdict |
| check-final-verify | atomic | final contract verification | distinct and 중요 | Keep | check-final-verify |
| check-improve-loop | atomic | self-critique loop | domain skill보다 control loop | Reclassify | control-improve-loop 또는 workflow-build-execute-plan 내부 |
| workflow-check-full-review | workflow(public) | default full review | public review entry로 좋음 | Merge | workflow-review-change |
| workflow-check-with-checklist | workflow(expert) | review + checklist | modifier workflow | Merge | workflow-review-change |
| workflow-security-preflight | workflow(public) | security preflight | single-step workflow라 과분 | Reclassify / Merge | check-security-holes mode 또는 release/review 내부 |

### Check 결론
- review 계열은 지금 **너무 쪼개졌다**.
- 현실적으로는  
  **`change review / security review / final verify`**  
  세 개면 충분하다.

---

## 8.7 Test family

| Current skill | Type | 현재 경계 평가 | 판정 | 권장 조치 | Target |
|---|---|---|---|---|---|
| test-find-gaps | atomic | missing test surface | 좋음 | Keep / Widen | test-find-gaps |
| test-design-cases | atomic | case design only | gap analysis와 거의 연속 단계 | Absorb | test-find-gaps |
| test-write-guards | atomic | regression test writing | 좋음 | Keep | test-write-guards |
| test-run-user-scenarios | atomic | realistic scenario runs | distinct, 다만 optional pack 가능 | Keep / Optional | test-run-user-scenarios |
| workflow-test-close-gaps | workflow(public) | gap → design → guard | 좋음 | Keep | workflow-test-close-gaps |

### Test 결론
- `find-gaps`가 **case design까지 출력**하게 넓히면 atomic 하나를 줄일 수 있다.

---

## 8.8 Tidy family

| Current skill | Type | 현재 경계 평가 | 판정 | 권장 조치 | Target |
|---|---|---|---|---|---|
| tidy-why-complex | atomic | complexity analysis | 좋은 anchor | Merge / Widen | tidy-analyze |
| tidy-find-copies | atomic | duplication smell scan | smell mode | Absorb | tidy-analyze |
| tidy-find-magic-numbers | atomic | constant smell scan | smell mode | Absorb | tidy-analyze |
| tidy-cut-fat | atomic | trim excess structure | simplify와 많이 겹침 | Absorb | tidy-simplify |
| tidy-simplify | atomic | behavior-preserving simplification | 좋음 | Keep / Widen | tidy-simplify |
| tidy-reorganize | atomic | structural refactor | distinct | Keep | tidy-reorganize |
| tidy-remove-legacy | atomic | stale surface removal | distinct | Keep | tidy-remove-legacy |
| workflow-tidy-find-improvements | workflow(public) | improvement candidate mapping | 좋음 | Keep | workflow-tidy-improvements |

### Tidy 결론
- tidy는 지금 **smell detector가 너무 많다.**
- `analyze / simplify / reorganize / remove-legacy` 4축으로 줄이면 훨씬 이해하기 쉽다.

---

## 8.9 Doc family

| Current skill | Type | 현재 경계 평가 | 판정 | 권장 조치 | Target |
|---|---|---|---|---|---|
| doc-find-all | atomic | docs inventory | 좋음 | Keep | doc-find-all |
| doc-curate | atomic | navigation / dedup / curation | 좋음 | Keep / Widen | doc-curate |
| doc-build-index | atomic | index docs build | curation output mode | Absorb | doc-curate |
| doc-write | atomic | doc authoring | 좋음 | Keep / Widen | doc-write |
| doc-publish-readme | atomic | root README publish | authoring output mode | Absorb | doc-write |
| workflow-doc-systemize | workflow(public) | inventory + curate + write | 좋음 | Keep | workflow-doc-systemize |

### Doc 결론
- docs는 **inventory / curate / write** 세 개면 충분하다.
- `build-index`, `publish-readme`는 mode로 흡수하는 게 낫다.

---

## 8.10 Release / utility family

| Current skill | Type | 현재 경계 평가 | 판정 | 권장 조치 | Target |
|---|---|---|---|---|---|
| release-check-repo | atomic | repo/branch/tag gate | distinct | Keep | release-check-repo |
| release-check-hygiene | atomic | release hygiene gate | distinct | Keep | release-check-hygiene |
| release-verdict | atomic | go/no-go gate | distinct | Keep | release-verdict |
| release-publish | utility(internal) | mutate branch/tag/release | distinct internal mutator | Keep | release-publish |
| workflow-release-ready-check | workflow(public) | readiness review | 좋지만 required input routing 보강 필요 | Keep / Fix | workflow-release-ready-check |
| workflow-release-publish | workflow(internal) | readiness + publish | 이름과 surface가 어긋남 | Rename / Reclassify | control-release-publish-flow |
| compose | utility(internal) | orchestration | 좋음 | Keep | compose |
| commit-write-message | atomic(expert) | commit message helper | core planning/dev에서 분리 가능 | Move to extras | commit-write-message |
| gemini | utility(expert) | external delegation | core pack에서 분리 권장 | Move to extras | gemini |

### Release / utility 결론
- release gate 자체는 잘 쪼개져 있다.
- 다만 `workflow-release-publish`는 **이름/분류 불일치**를 먼저 고쳐야 한다.
- `gemini`, `commit-write-message`는 **extras pack**으로 빼는 것이 discovery 품질에 더 좋다.

---

## 9. 꼭 고쳐야 하는 구체 결함

### 9.1 Surface 규칙 불일치
먼저 이것부터 고치는 게 맞다.

- README: `build-until-done`, `finish-until-done`는 internal control처럼 설명
- 실제 metadata: 둘 다 `public_entry`

**조치**
- 둘 중 하나를 선택해야 한다.
  - A안: README를 바꿔 public entry로 인정
  - B안: metadata를 바꿔 internal_control로 정렬
- 내 추천은 **B안**이다.

### 9.2 workflow-debug-this expands_to 불일치
설명상 “수정 확인까지”인데 실제 expansion에 `debug-confirm-fix`가 없다.

**조치**
- `workflow-debug-this` expands_to를 아래처럼 재정렬 권장
  - `$debug-capture-failure`
  - `$debug-find-root-cause`
  - `$debug-confirm-fix`
  - `$test-write-guards` 또는 `$test-find-gaps`

### 9.3 workflow-release-ready-check starter input 결함
required input:
- `TARGET_BRANCHES`

starter_inputs:
- `RELEASE_SCOPE`, `ROLLOUT_PLAN`, `ROLLBACK_PATH`만 있음

**조치**
- starter_inputs에 `BRANCHES` 또는 `TARGET_BRANCHES`를 추가
- 아니면 required를 완화하고 derive policy를 명시

### 9.4 workflow-security-preflight의 존재 이유 약함
현재는 사실상 `check-security-holes`의 public wrapper다.

**조치**
- 아래 중 하나 추천
  - A안: 삭제 후 `check-security-holes`를 public workflow/entry로 승격
  - B안: `workflow-review-change` / `workflow-release-ready-check` 내부 단계로 흡수

내 추천은 **B안**이다.

---

## 10. “추가해야 할 skill”에 대한 내 판단

**지금은 새 standalone skill을 추가할 때가 아니다.**

지금 부족한 것은 “capability”보다 **경계 정렬**이다.

굳이 하나만 꼽으면 빠져 있는 것은:

- **acceptance criteria / concrete examples artifact**

하지만 이것도 새 skill을 만들기보다:

- `plan-what-it-does`에 acceptance criteria 포함
- `test-find-gaps`가 case plan까지 내보내도록 확대

로 해결하는 것이 더 좋다.

즉, **새 skill 추가보다 기존 planning/test skill의 output contract 확장이 정답**이다.

---

## 11. 내가 권하는 단계별 개선 순서

### Phase 0 — 계약 정렬
1. `README` vs `skill.json` surface 불일치 정리
2. `workflow-debug-this` expansion 수정
3. `workflow-release-ready-check` starter_inputs 수정
4. `workflow-release-publish` naming/surface 정리

### Phase 1 — 1차 merge
1. Ask 통합
2. Scope/Boundary 통합
3. Review quartet 통합
4. Test gap + design 통합
5. Tidy smell detectors 통합
6. Doc output-specialization 통합
7. `check-release-risk` 제거 후 `release-verdict`로 흡수

### Phase 2 — control/extras 분리
1. `build-until-done`, `finish-until-done`를 control로 이동
2. `gemini`, `commit-write-message`를 extras로 이동
3. `workflow-security-preflight`를 review/release 내부로 흡수

### Phase 3 — workflow 재조립
1. `workflow-clarify-request`
2. `workflow-review-change`
3. 정리된 atomic들로 workflow 전부 재선언
4. 각 workflow는 2~5개 atomic만 사용하도록 제한

### Phase 4 — 설치 profile 도입
`scripts/sync.sh`에 profile 추가:
- `core`
- `docs-release`
- `extras`
- `all`

### Phase 5 — lint/validation 강화
`scripts/skills.py`에 다음 검사를 추가 권장:
1. `public_entry`인데 naming 규칙 위반 경고
2. public_entry required input이 starter_inputs로 라우팅 가능한지 검사
3. workflow 설명과 expands_to 핵심 단계 정합성 검사
4. expands_to가 단일 atomic뿐인 workflow 경고
5. merge candidate 힌트를 주는 overlap lint(동일 family, 유사 inputs, 유사 lens, modifier 차이만 존재)

---

## 12. 최종 권고안

### 유지
- `workflow-plan-build-ready`
- `workflow-build-implement-and-guard`
- `workflow-build-execute-plan`
- `workflow-debug-this`(수정 후)
- `workflow-doc-systemize`
- `workflow-test-close-gaps`
- `workflow-release-ready-check`
- `build-write-code`
- `debug-confirm-fix`
- `check-security-holes`
- `check-final-verify`
- `release-check-repo`
- `release-check-hygiene`
- `release-verdict`
- `release-publish`
- `compose`
- `plan-sync-tasks`

### 통합
- ask 계열
- scope/boundary
- review quartet
- test gap/design
- tidy smell detectors
- doc output specializations
- release risk → release verdict

### 재분류
- `build-until-done`
- `finish-until-done`
- `workflow-release-publish`
- `workflow-security-preflight`
- `check-improve-loop`

### extras로 이동
- `gemini`
- `commit-write-message`

---

## 13. 내 결론 한 줄

**이 저장소는 방향이 맞다.  
문제는 품질이 아니라 “스킬 표면이 너무 넓고, 일부 경계가 지나치게 얇다”는 점이다.**  

따라서 정답은 새 skill을 계속 추가하는 것이 아니라:

1. **중복/미세분해를 줄이고**
2. **public workflow를 카테고리당 1개 default로 정리하고**
3. **control / extras / optional packs를 분리하고**
4. **planning outputs(acceptance criteria, verification contract)를 기존 skill에 흡수하는 것**

이다.

---

## 14. 참고 소스

### OpenAI / Codex 공식
- Agent Skills: https://developers.openai.com/codex/skills/
- Customization / Skills: https://developers.openai.com/codex/concepts/customization/
- Skills API guide: https://developers.openai.com/api/docs/guides/tools-skills/
- Skills and OSS maintenance blog: https://developers.openai.com/blog/skills-agents-sdk/

### 저장소
- Repo: https://github.com/AxiomOrient/composable-skills
- Commit history (`9d6798c` visible): https://github.com/AxiomOrient/composable-skills/commits/main/
- Root README: https://raw.githubusercontent.com/AxiomOrient/composable-skills/main/README.md
- Skills README: https://raw.githubusercontent.com/AxiomOrient/composable-skills/main/skills/README.md
- Validator / sync logic: https://raw.githubusercontent.com/AxiomOrient/composable-skills/main/scripts/skills.py

### 대표 inspected skill files
- ask-form-question: https://raw.githubusercontent.com/AxiomOrient/composable-skills/main/skills/ask-form-question/SKILL.md
- workflow-plan-build-ready: https://raw.githubusercontent.com/AxiomOrient/composable-skills/main/skills/workflow-plan-build-ready/SKILL.md
- compose: https://raw.githubusercontent.com/AxiomOrient/composable-skills/main/skills/compose/SKILL.md
- build-until-done: https://raw.githubusercontent.com/AxiomOrient/composable-skills/main/skills/build-until-done/SKILL.md
- finish-until-done: https://raw.githubusercontent.com/AxiomOrient/composable-skills/main/skills/finish-until-done/SKILL.md
- release-publish: https://raw.githubusercontent.com/AxiomOrient/composable-skills/main/skills/release-publish/SKILL.md
- gemini: https://raw.githubusercontent.com/AxiomOrient/composable-skills/main/skills/gemini/SKILL.md
