| ID | Goal | Scope | Verification | Status |
|----|------|-------|--------------|--------|
| site/plan | Fix publish structure and content architecture | `plans/`, `docs/`, `scripts/` | Plan docs exist and match request | Done |
| site/data | Generate skill catalog from source contracts | `scripts/build_site_data.py`, `docs/data/skills.json` | Generator runs and JSON contains all skills | Done |
| site/ui | Build project site UI and authored narrative | `docs/index.html`, `docs/assets/*` | Page loads with philosophy, system, value, and skill atlas sections | Done |
| site/hygiene | Remove legacy noise and document deployment | `.gitignore`, `docs/`, `README.md` | No stray publish junk; deploy instructions are clear | Done |
| site/verify | Verify static output and Pages readiness | local commands | Generator and HTML checks pass | Done |
