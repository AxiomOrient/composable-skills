# Skill Registry

`skills/_registry/` is the source of truth for the upgraded skill system.

`index.json` is the public discovery surface for upgraded skills.

## Layers

- `atomic/`: single-problem, single-output skills
- `utility/`: orchestration, rendering, execution-governance, or middleware helpers
- `workflow/`: named compositions that expand to atomic/utility skills

## Out of Scope

- `skills/.system/*` is internal system surface, not part of the public upgraded registry.
- `.system` skills can exist on disk without matching registry entries.
- Registry validation applies only to public upgraded skills under `atomic/`, `utility/`, and `workflow/`.

## Required registry fields

Every registry entry must declare:

- `name`
- `layer`
- `family`
- `job_type`
- `description`
- `purpose`
- `when_to_use`
- `do_not_use`
- `required_inputs`
- `structured_outputs`
- `artifacts_in`
- `artifacts_out`
- `neutrality_rules`
- `response_profile`
- `default_prompt`
- `explicit_only`

Workflow entries must also declare:

- `expands_to`

Atomic entries must also declare:

- `primary_lens`
- `lens_rationale`

Lens catalog entries in `../_core/lenses.json` must declare:

- `status` (`active` | `reserve` | `alias`)
- `frame_name` and `thesis` for active/reserve lenses
- `decision_rules`
- `anti_patterns`
- `good_for`
- `not_for`
- `references`

## Rules

1. Registry is the only source of truth.
2. `skills/<name>/SKILL.md` and `agents/openai.yaml` are materialized outputs.
3. `docs/SKILL-STATE-REPORT.md` is a generated report derived from registry entries.
4. Atomic skills must solve one precise problem and produce one stable output shape.
5. Utility skills must not masquerade as domain-solving skills.
6. Workflow skills must be transparent named compositions. Hidden logic is forbidden.
7. Public workflow names use the `wf-` prefix only.
8. Neutrality rules are mandatory for every analysis/review/feedback-oriented skill.
9. Atomic skills carry exactly one primary lens. Lenses are mental-model cards, not celebrity roleplay prompts.
10. Atomic `primary_lens` must point to an `active` lens, not to a reserve lens or public alias.
11. Reserve lenses can remain in the catalog, but only active lenses should drive default skill behavior.
