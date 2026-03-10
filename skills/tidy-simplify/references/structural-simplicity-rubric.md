# Structural Simplicity Rubric

Use this file to decide whether a candidate move actually makes the code simpler.

## Macro

- `Essential Complexity`
  - Keep domain-required complexity.
  - Remove accidental complexity that exists only because of incidental structure.
- `Orthogonality`
  - Favor changes that stay local.
  - Penalize code where one adjustment leaks into unrelated modules.
- `Declarative Intent`
  - Prefer code that states what is happening without forcing the reader to simulate the full mechanism.

## Micro

- `Side-Effect Isolation`
  - Keep pure transformation distinct from I/O, mutation, and framework effects.
- `Data-First Integrity`
  - Prefer visible data shape and explicit transformation over opaque wrappers.
- `Mechanical Sympathy`
  - Avoid unnecessary allocations, copies, and runtime-hostile patterns when the simplification target touches hot paths.

## Resilience

- `Failure Modes`
  - Do not simplify away important unhappy-path logic.
  - Make failure handling easier to follow, not more implicit.
- `Boundary Validation`
  - Keep validation at the boundary explicit.
  - Do not collapse a boundary if doing so hides contract checks.

## Pass Test

A simplify move is good when all conditions hold.

- The core intent becomes easier to state.
- The number of mental jumps or hidden assumptions goes down.
- The behavior guard remains explicit.
- The reader can trace data flow and side effects faster than before.
