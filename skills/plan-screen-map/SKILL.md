---
name: plan-screen-map
description: "Use when defining hierarchy, navigation, screen or page relationships, and core user flows before detailed UI or technical implementation. Do not use for detailed feature behavior or backend solution design."
---

# Plan / Screen Map

## Purpose
Define the content and navigation structure users must move through so later specs and design work share the same map.

## Default Program
```text
[stages: preflight>detect>analyze>plan>review>handoff>audit |
 scope: repo|paths(glob,...) |
 policy: evidence,quality-gates{docs,ux},deterministic-output |
 lens: nielsen-norman |
 output: md(contract=v1)]
```

## Lens Rationale
This skill uses `nielsen-norman` because it keeps the work aligned with: Usability-first decisions based on explicit heuristics, scanning behavior, and information scent.

## Use When
- Need a clear hierarchy for pages, screens, content groups, or routes.
- Need navigation rules and user flows before screen-level design or implementation.
- Need to separate structure decisions from detailed feature requirements.

## Do Not Use When
- Need only a product brief or business framing.
- Need detailed functional requirements and acceptance checks.
- Need technical boundaries, APIs, or data-flow design.

## Required Inputs
- `IA_SCOPE` (site|app|section|feature; required): Boundary the information architecture governs.
- `PRIMARY_USERS` (list; required; shape: {USER, GOAL}): Primary user groups and the goal each one is trying to accomplish.
- `CONTENT_OBJECTS` (list; required; shape: {ITEM, PURPOSE}): Pages, screens, content groups, or entities that must exist in the structure.
- `ENTRY_POINTS` (list; required; shape: {ENTRY, USER_NEED}): Where users enter the structure and what they expect to do from there.
- `KNOWN_FLOWS` (list; optional; shape: {FLOW, START, END}): Known start-to-end flows that the IA must support.
- `NAV_CONSTRAINTS` (list; optional; shape: {CONSTRAINT}): Constraints such as platform limits, route rules, localization needs, or compliance requirements.

## Input Contract Notes
- CONTENT_OBJECTS should name structure elements, not full visual designs or implementation tickets.
- ENTRY_POINTS should reflect real user entry paths, not idealized happy-path assumptions only.
- KNOWN_FLOWS should stay few and core; this skill is for structure, not exhaustive scenario enumeration.
- If naming is still unsettled, keep labels descriptive and plain rather than prematurely brand-polished.

## Structured Outputs
- `IA_SUMMARY` (string; required): One short summary of the hierarchy and why it is organized this way.
- `HIERARCHY_MAP` (list; required; shape: {NODE, PARENT, PURPOSE}): Parent-child structure for the main navigation or content hierarchy.
- `NAVIGATION_PATHS` (list; required; shape: {FROM, TO, WHEN}): Allowed navigation moves and the context in which each one should appear.
- `CORE_FLOWS` (list; required; shape: {FLOW, STEPS, SUCCESS_END}): Core user flows that the IA must support.
- `LABELING_NOTES` (list; required; shape: {LABEL, WHY}): Important naming and labeling notes that improve clarity and findability.

## Output Contract Notes
- HIERARCHY_MAP should make the parent-child structure explicit enough that later UI work does not need to guess the topology.
- NAVIGATION_PATHS should describe when a path is available, not just that two nodes are related somehow.
- CORE_FLOWS should stay focused on the structural path through the system rather than detailed functional logic.
- LABELING_NOTES should explain meaning and findability, not visual copy style.

## Primary Lens
- `primary_lens`: `nielsen-norman`
- `why`: Information architecture succeeds when hierarchy, navigation, and information scent stay explicit enough that users can predict where to go next.

## Artifacts
- `artifacts_in`: plan-why-build-this.v1, scope-contract.v1
- `artifacts_out`: ia-map.v1

## Neutrality Rules
- Separate structure choices from visual styling or technical implementation assumptions.
- Do not invent user flows or nodes that the supplied content and user goals do not support.
- Keep ambiguous labels as notes or open edges rather than pretending the terminology is settled.

## Response Format

Lead with the IA summary in one sentence: how the hierarchy is organized and why.

Show the hierarchy map as a compact tree or parent-child list.

List core flows: [flow] → [steps] → [success end]

Flag uncertain labels or open edges: "Label '[X]' is provisional — unclear if it matches user mental model."

Ask: "Does this hierarchy support [primary user goal], or does [specific node] need to move?"

## Execution Constraints
- Do not turn this skill into a visual design spec or backend architecture document.
- Prefer a small, navigable structure that supports the primary user goals before adding secondary branches.
- If a flow or label is uncertain, mark it explicitly instead of hiding the ambiguity in a polished sitemap.

## Example Invocation
```text
$plan-screen-map
IA_SCOPE: feature
PRIMARY_USERS:
  - USER: new administrator
    GOAL: finish the first team setup
CONTENT_OBJECTS:
  - ITEM: Workspace Overview
    PURPOSE: show current status and the next action
ENTRY_POINTS:
  - ENTRY: immediately after the first login
    USER_NEED: understand immediately where setup should start
```
