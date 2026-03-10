# Answer Repair Playbook

Use this file when the answer is weak, wrong, shallow, or structurally off-target.

## Failure classes
1. **Scope drift** — the answer discussed nearby topics instead of the selected one.
2. **Unsupported claims** — claims were made without evidence or source handling.
3. **Missed disagreement** — opposing expert views or trade-offs were not surfaced.
4. **Definition failure** — core terms were left ambiguous.
5. **No operational consequence** — the answer stayed abstract and did not reach a decision boundary.
6. **False certainty** — uncertainty, ambiguity, or evidence gaps were hidden.
7. **Contour mismatch** — the answer ignored the requested section structure.

## Minimum repair loop
1. State why the answer failed.
2. Identify what was missing.
3. Produce the minimal question change that would likely fix it.
4. If needed, produce a repaired prompt.
5. Re-evaluate against the rubric.

## Preferred repair style
- Fix the narrowest thing first.
- Preserve useful parts of the original question.
- Do not redesign the entire prompt unless the failure is structural.
