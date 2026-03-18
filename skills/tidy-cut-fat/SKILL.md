---
name: tidy-cut-fat
description: "Use when complexity must be reduced without changing core behavior: oversized objects, unclear architecture, noisy folder trees, weak naming, hidden side effects, or accidental abstraction. Produce a minimal simplification blueprint. Do not use for net-new feature work, incident firefighting, or cases where splitting would only increase navigation cost or hurt a measured hot path."
---

# Tidy / Cut Fat

## Purpose
Identify and propose the smallest useful complexity reduction without changing intended behavior or fragmenting structures whose main value is contiguous readability or measured performance.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>reflect>handoff>audit |
 scope: repo|diff|paths(glob,...) |
 policy: evidence,correctness-first,quality-gates{tests,compat,style},deterministic-output |
 lens: hickey-carmack |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `hickey-carmack` because it keeps the work aligned with: Data model first, explicit side effects, and explicit performance characteristics.

## Use When
- Need a simplification blueprint for a bounded scope.
- Need to distinguish essential complexity from accidental complexity.
- Need to reduce structural or naming noise before implementation.

## Do Not Use When
- Need direct code changes rather than a planning output.
- Need security or release review rather than simplification planning.
- Need a dependency-rule refactor plan rather than broad simplification.
- The target is mostly declarative data or configuration and splitting it would only force cross-file lookup without reducing logic complexity.
- The target is a strict procedural sequence or tightly coupled algorithm where breaking the flow would make the behavior harder to follow.
- The target is a measured hot path where extra indirection, dispatch, or call boundaries would risk real performance cost.

## Required Inputs
- `TARGET_SCOPE` (path|module|folder|repo; required): Scope to simplify.
- `SIMPLIFICATION_GOAL` (naming|structure|side-effects|mixed; required): Dimension of simplification to prioritize.
- `PRESERVE_BEHAVIOR` (yes|no-change-intent; required): Behavior-preservation contract.
- `KNOWN_PAIN` (list; optional): Known hotspots or complexity symptoms.

## Input Contract Notes
- File size alone is not evidence that a scope should be split.
- If a large target is mostly declarative data or configuration, first ask whether splitting improves change safety or only increases navigation cost.
- If the main value is strict execution order or measured hot-path performance, default to `Left alone` unless a smaller boundary clearly improves understanding without breaking the flow or cost model.
- Prefer `KNOWN_PAIN` that points to hidden state, accidental branching, weak naming, or needless indirection rather than "this file is long".

## Structured Outputs
- `COMPLEXITY_INVENTORY` (list; required): Essential versus accidental complexity findings.
- `SIMPLIFICATION_PLAN` (list; required): Atomic simplification steps.
- `LEFT_INTACT_AREAS` (list; required): Large structures intentionally not split because keeping them contiguous is simpler, safer, or faster.
- `BEHAVIOR_GUARDS` (list; required): Checks that preserve intended behavior.

## Output Contract Notes
- `SIMPLIFICATION_PLAN` may be empty when the best simplification decision is to keep the large structure intact.
- `LEFT_INTACT_AREAS` should make non-split decisions explicit with the concrete reason: declarative data, strict sequence, or measured hot path.
- `BEHAVIOR_GUARDS` should still describe the checks that protect any recommended change or any decision to preserve an intentional hot path.

## Primary Lens
- `primary_lens`: `hickey-carmack`
- `why`: Simplification should remove hidden indirection and preserve only essential structure.

## Artifacts
- `artifacts_in`: tidy-analyze.v1
- `artifacts_out`: simplification-plan.v1

## Response Format

Think and operate in English, but deliver the final response in Korean.
쉽고 간결한 한국어로 답하라. 전문 용어 금지. 핵심만 간단하게.

Show what changed and what was left alone:
- Simplified: [what] — why: [complexity removed]
- Left alone: [what] — reason: [essential or out of scope]

List behavior guards: [check] — confirms: [what still works]

If scope was constrained, say so plainly: "Stopped at [boundary] — [rest] was out of scope."

Ask about any boundary decision that affected what got simplified.

## Neutrality Rules
- Separate essential complexity from accidental complexity.
- Do not recommend abstraction unless it removes a proven complexity source.
- Keep uncertain complexity causes as candidates, not conclusions.
- Do not treat length, line count, or object size by itself as proof that decomposition is helpful.
- Prefer contiguous declarative data, contiguous required sequences, or contiguous measured hot paths when splitting would only raise cognitive or runtime cost.

## Execution Constraints
- Check these non-split cases before proposing decomposition: declarative tables/config, strict sequential procedures, and measured hot paths.
- If an existing explicit marker such as `tidy-cut-fat: keep-intact` is present in a commentable file, skip decomposition checks for that marked region and continue with other simplification checks.
- Do not add new suppression markers automatically. If durable suppression is needed, prefer the repository's native comment style, or use an adjacent review manifest for formats that do not support comments.
