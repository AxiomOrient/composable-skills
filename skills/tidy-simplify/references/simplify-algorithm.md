# `tidy-simplify` Algorithm Reference

Primary procedure reference for `$tidy-simplify`.

Core goal: cognitive-load reduction under strict functional equivalence.
This is a four-step reduction sequence, not a planning exercise.

## Core Sequence

1. `Intent Extraction`
   - Read the whole bounded scope first.
   - Write one sentence that names the final value, behavior, or guarantee the code must preserve.
   - If the intent cannot be named clearly, do not simplify yet.

2. `Abstraction Cost`
   - Inspect interfaces, wrappers, helper chains, and transformation hops.
   - Ask whether each layer protects a real invariant or only adds indirection.
   - Mark one-use helpers, pass-through wrappers, and decorative layers as collapse candidates.

3. `Collapse & Merge`
   - Replace nested branching with guard clauses or early returns when the control flow becomes clearer.
   - Merge multi-hop data transformations into one explicit pipeline when intermediate steps add no contract value.
   - Prefer standard-library operations over bespoke logic when behavior remains equivalent.

4. `Immutability Check`
   - Reduce mutable temporary state.
   - Prefer derived values, one-way data flow, and explicit transformation over stateful bookkeeping.

## Good Moves

- Guard clause instead of nested `if/else`
- One visible data pipeline instead of several wrappers
- Concrete standard-library call instead of custom utility
- Inline a one-use helper when it hides more than it clarifies
- Replace temporal mutation with explicit derived values

## Stop Conditions

Stop or narrow the pass when any of these are true.

- The structure carries a real invariant or public contract.
- The target scope is too wide to verify behavior confidently.
- The simplification would blend unrelated cleanup with the requested change.
- The improvement is aesthetic only and does not reduce cognitive steps.

## Prompt Frame

Apply this internal frame:

> Preserve functional equivalence. Minimize the reader's mental energy. Remove unnecessary indirection. Prefer declarative logic, concrete names, and explicit data flow.
