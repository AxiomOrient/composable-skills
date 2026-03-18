# Consensus Method

This package uses a **two-round consensus protocol**.

## 1. Normalize the Mission

Build one bounded packet:

- request summary
- scope in / scope out
- constraints
- done signals
- local evidence
- open questions

If the mission cannot be bounded, stop.

## 2. Independent Round

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

## 3. Normalize Atomic Decisions

The orchestrator extracts atomic decisions from `must_keep` and `must_avoid`.

Each decision is clustered by semantic similarity. The goal is not perfect ontology; the goal is a stable disagreement surface.

## 4. Build the Disagreement Packet

For each clustered decision:

- who wants to keep it
- who wants to avoid it
- evidence strength
- why it matters

Also include short proposal summaries.

The packet is anonymized before the rebuttal round.

## 5. Rebuttal Round

Each agent sees:

- anonymized proposal summaries
- the disagreement packet
- the instruction to update only when the evidence justifies it

This creates actual cross-model challenge without turning the run into pure imitation.

## 6. Deterministic Arbitration

The final result is **not** a majority-vote paragraph.

Decision rules:

- `3 keep / 0 avoid` → accepted keep
- `0 keep / 3 avoid` → accepted avoid
- `2 keep / 0 avoid` and stronger evidence than alternatives → provisional keep
- `0 keep / 2 avoid` and stronger evidence than alternatives → provisional avoid
- any keep/avoid collision on the same clustered decision → unresolved
- low-evidence agreement stays provisional or unresolved
- unsupported claims are never promoted just because multiple models repeated them

## 7. Final Output

The report must preserve five layers:

1. final verdict
2. consensus recommendation
3. accepted decisions
4. unresolved conflicts
5. cheapest next checks

A good consensus engine does not hide uncertainty. It compresses uncertainty into a smaller, testable surface.
