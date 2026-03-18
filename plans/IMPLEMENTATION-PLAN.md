# Composable Skills Project Site Plan

## Request
Build a static GitHub Pages project site that explains the philosophy, system, and every skill in this repository.

## Scope Contract
- In scope:
  - A static site published from `docs/`
  - A clean source structure for styles, behavior, and generated data
  - Philosophy, system, user value, and skill catalog content
  - A repeatable local generation step so the catalog stays synced with `skills/*/SKILL.md`
- Out of scope:
  - Server-side rendering
  - GitHub Actions or CI-based deployment
  - CMS, database, or runtime framework adoption

## Done Condition
1. `docs/index.html` renders a polished project site for GitHub Pages.
2. The site explains:
   - the philosophy in short, clear language
   - the system in a concise way
   - what a user gains from the system
   - each skill with enough detail to choose it correctly
3. Skill data is generated from repository source files instead of hand-maintained duplication.
4. The published folder is deployable from GitHub Pages without extra build infrastructure.
5. Local verification exists for generation and HTML output.

## Design Summary
- Keep the stack intentionally small: plain HTML, CSS, and JavaScript in `docs/`, plus one Python generator script in `scripts/`.
- Use `docs/` as the publish root so GitHub Pages can serve directly from the default branch without CI.
- Generate a `docs/data/skills.json` catalog from `skills/*/SKILL.md` by parsing frontmatter and core sections (`Purpose`, `Use When`, `Do Not Use When`, `Expansion`).
- Build the page around five user questions:
  1. What is this?
  2. Why does it exist?
  3. What do I get from it?
  4. How is the system organized?
  5. Which skill should I use now?
- Keep philosophy and system copy short; keep skill explanations rich, filterable, and searchable.

## Information Architecture
1. Hero
2. Philosophy
3. What Users Get
4. System Layers
5. Operating Flow
6. Skill Atlas
7. Docs / Install / Deploy

## Implementation Notes
- Prefer relative asset paths so the site works on project pages under a repository subpath.
- Add `.nojekyll` to the published folder for predictable static serving.
- Remove stray macOS legacy files from the published folder.
- Keep generated data separate from authored assets:
  - `docs/index.html`
  - `docs/assets/styles.css`
  - `docs/assets/app.js`
  - `docs/data/skills.json`
  - `scripts/build_site_data.py`
