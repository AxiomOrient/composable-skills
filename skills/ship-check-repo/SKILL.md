---
name: ship-check-repo
description: "Use when release work must start by confirming the repository is a real git release target with usable branches, remotes, and a clean enough working tree. Do not use for rollout judgement or actual publication."
---

# Ship / Check Repo

## Purpose
Check repository, branch, remote, and tag preconditions before release review or publication.

## Default Program
```text
[stages: preflight>detect>analyze>review>handoff>audit |
 scope: repo |
 policy: evidence,safety-gates,quality-gates{release,git},deterministic-output |
 lens: release-gatekeeper |
 output: md(contract=v1)]
```

## Use When
- Need to confirm the target is a git repository before any release work.
- Need to inspect source/target branch state, worktree cleanliness, remotes, or tag collisions.
- Need explicit repository preconditions before release review or publish execution.

## Do Not Use When
- Need rollout risk or GO/NO-GO judgement; use ship-release-verdict instead.
- Need documentation or public-surface hygiene checks; use ship-check-hygiene instead.
- Need to mutate branches, tags, or remotes; use release-publish instead.

## Required Inputs
- `TARGET_BRANCHES` (list; required; shape: {BRANCH, ROLE}): Branches involved in the release, such as source/dev and target/main.
- `REMOTE_NAME` (string; optional): Remote expected to receive the release refs. Default is origin.
- `TAG_INTENT` (string; optional): Candidate tag or version label to validate for collisions.
- `REPO_EXPECTATIONS` (list; optional; shape: {CHECK}): Extra repository preconditions such as clean worktree, tracking branch, or remote push access.

## Input Contract Notes
- TARGET_BRANCHES should identify the actual release branch roles rather than vague branch names with no role.
- Use TAG_INTENT when the release process cares about tag collisions or pre-existing version refs.
- This skill checks repository reality only; it does not decide whether the release should go out.

## Structured Outputs
- `REPO_FACTS` (list; required; shape: {CHECK, RESULT, EVIDENCE}): Observed repository facts such as git root presence, worktree state, remote existence, or tag availability.
- `BRANCH_MAP` (list; required; shape: {BRANCH, ROLE, STATUS}): Observed branch roles and current state.
- `REPO_BLOCKERS` (list; required; shape: {ISSUE, WHY_BLOCKING}): Repository conditions that stop release work.
- `REPO_RELEASE_STATUS` (ready|blocked|inconclusive; required; allowed: ready|blocked|inconclusive): Overall repository readiness for release work.

## Output Contract Notes
- REPO_FACTS should stay purely observational and cite concrete repository evidence.
- Use REPO_RELEASE_STATUS=blocked when a hard precondition fails, such as not being in a git repo or target branch missing.
- Use inconclusive when the repository exists but a critical fact such as remote push capability could not be verified.
- REPO_BLOCKERS may be an empty list when repository preconditions are clean; do not invent blockers to fill the section.

## Primary Lens
- `primary_lens`: `release-gatekeeper`
- `why`: Release work should begin from explicit repository reality rather than branch-name assumptions or optimistic publish expectations.

## Artifacts
- `artifacts_in`: none
- `artifacts_out`: release-repo-check-report.v1

## Neutrality Rules
- Report repository facts as observed state, not as guessed release policy.
- Do not infer push or publish success from branch names alone.
- If a repository precondition cannot be verified, mark it inconclusive rather than assuming ready.

## Execution Constraints
- Do not modify branches, tags, remotes, or files from this skill.
- Keep repository checks bounded to release-relevant state instead of broad repo review.
- Prefer concrete git evidence such as current branch, clean worktree, remote refs, and tag presence.
