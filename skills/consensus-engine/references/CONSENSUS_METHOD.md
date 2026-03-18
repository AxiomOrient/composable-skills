# Consensus Method

This package uses a **parallel-first consensus protocol**.

## 1. Normalize the Mission

Build one bounded packet:

- request summary
- scope in / scope out
- constraints
- done signals
- local evidence
- open questions

If the mission cannot be bounded, stop.

## 2. Shared Execution Contract (optional)

When the caller supplies a `compose` macro:

- normalize it first with the local compose parser
- share the same program, scope, response profile, and missing-input warnings with all three agents
- ask each agent to produce one concrete work product, not only a recommendation
- stop immediately if required compose inputs are still unresolved

This keeps orchestration explicit and aligned with the repository's compose philosophy.

## 3. Independent Round

Ask Codex, Claude Code, and Gemini CLI the same mission.

Each agent returns structured JSON with:

- `summary`
- `proposal`
- `must_keep`
- `must_avoid`
- `assumptions`
- `uncertainties`
- `next_checks`
- `confidence`

Round 1 is fully independent. No peer answers are shown.

## 4. Normalize Atomic Decisions

The orchestrator extracts atomic decisions from `must_keep` and `must_avoid`.

Decision statements should be normalized to **positive action phrases**.
Example:

- keep: `preserve public API`
- avoid: `inspect repository files`

Each decision is clustered by semantic similarity. The goal is not perfect ontology; the goal is a stable disagreement surface.

## 5. Build the Disagreement Packet

For each clustered decision:

- who wants to keep it
- who wants to avoid it
- evidence strength
- why it matters

Also include short proposal summaries.
When the run is execution-oriented, also include short work summaries.

The packet is anonymized before the rebuttal round.

## 6. Adaptive Rebuttal Round

Each agent sees:

- anonymized proposal summaries
- the disagreement packet
- the instruction to update only when the evidence justifies it

Run round 2 only when disagreement or divergent work products justify it. If round 1 is already unanimous and the work summaries converge, skip the extra debate.

## 7. Deterministic Arbitration

The final result is **not** a majority-vote paragraph.

Decision rules:

- `3 keep / 0 avoid` → accepted keep
- `0 keep / 3 avoid` → accepted avoid
- `2 keep / 0 avoid` and stronger evidence than alternatives → provisional keep
- `0 keep / 2 avoid` and stronger evidence than alternatives → provisional avoid
- any keep/avoid collision on the same clustered decision → unresolved
- aligned votes without enough concrete anchors → needs-more-evidence
- low-evidence agreement does not get promoted just because multiple models repeated it
- unsupported claims are never promoted just because multiple models repeated them
- when work products exist, select the strongest final draft by consensus-fit first and provider confidence second
- if verdict is `no-consensus`, withhold the selected work product
- if a compose response profile defines required sections, withhold selection until one candidate covers them all

## 8. Final Output

The report must preserve five layers:

1. final verdict
2. consensus recommendation
3. selected work product when present
4. accepted decisions / unresolved conflicts
5. cheapest next checks

A good consensus engine does not hide uncertainty. It compresses uncertainty into a smaller, testable surface.
