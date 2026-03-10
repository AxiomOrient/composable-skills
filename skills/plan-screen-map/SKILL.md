---
name: plan-screen-map
description: "Use when defining hierarchy, navigation, screen or page relationships, and core user flows before detailed UI or technical implementation. Do not use for detailed feature behavior or backend solution design."
---

# Information Architecture

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
- `frame_name`: Findability and Heuristics Reviewer
- `why`: Information architecture succeeds when hierarchy, navigation, and information scent stay explicit enough that users can predict where to go next.
- `summary`: Usability-first decisions based on explicit heuristics, scanning behavior, and information scent.
- `thesis`: Structures become easier to use when navigation, labeling, scanning, and information scent are treated as first-class constraints rather than afterthoughts.
- `decision_rules`:
  - Optimize the first scan path before polishing details.
  - Check whether the user can predict where to go next from labels, grouping, and information scent.
  - Prefer predictable headings, navigation, and labels over clever naming.
  - Treat duplication, orphaned nodes, and hidden paths as structure defects, not just content defects.
- `anti_patterns`:
  - Dense structures with weak labels or headings
  - Navigation that assumes insider knowledge
  - Hierarchy that mirrors implementation history instead of user intent
- `good_for`:
  - information architecture
  - README structure
  - doc inventory
  - doc curation
  - navigation review
- `not_for`:
  - root-cause debugging
  - dependency boundary design
  - security threat modelling
- `required_artifacts`:
  - Hierarchy or Navigation Map
  - Findability Risks
  - Labeling or Mitigation Notes
- `references`:
  - https://www.nngroup.com/articles/ten-usability-heuristics/

## Artifacts
- `artifacts_in`: plan-why-build-this.v1, scope-contract.v1
- `artifacts_out`: ia-map.v1

## Neutrality Rules
- Separate structure choices from visual styling or technical implementation assumptions.
- Do not invent user flows or nodes that the supplied content and user goals do not support.
- Keep ambiguous labels as notes or open edges rather than pretending the terminology is settled.

## Execution Constraints
- Do not turn this skill into a visual design spec or backend architecture document.
- Prefer a small, navigable structure that supports the primary user goals before adding secondary branches.
- If a flow or label is uncertain, mark it explicitly instead of hiding the ambiguity in a polished sitemap.

## Example Invocation
```text
$plan-screen-map
IA_SCOPE: feature
PRIMARY_USERS:
  - USER: 신규 관리자
    GOAL: 첫 팀 설정을 끝낸다
CONTENT_OBJECTS:
  - ITEM: Workspace Overview
    PURPOSE: 현재 상태와 다음 행동 보여주기
ENTRY_POINTS:
  - ENTRY: 첫 로그인 직후
    USER_NEED: 어디부터 설정해야 하는지 바로 이해하고 싶다
```

## Output Discipline
- `response_profile=ia_contract`
- User-facing rendering is delegated to `respond`.
