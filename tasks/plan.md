# Implementation Plan: Solo Leveling "Shadow Monarch System HUD" Overhaul

## Overview
Upgrade `S-Q-Ali/S-Q-Ali` into a self-healing, automated Solo Leveling System HUD GitHub Profile. We will build a pure-Python SVG HUD generator (`scripts/svg_hud.py`), integrate it with `scripts/analyze.py` (adding a `--from-report` offline mode and live language aggregation), create a comprehensive test suite (`tests/test_analyze.py`), redesign `README.md` with zero broken external links, and upgrade `.github/workflows/skill-rank.yml` to run tests and commit updated SVG assets automatically.

## Architecture Decisions
1. **Self-Hosted Data-Driven SVGs over Flaky 3rd-Party Vercel Widgets:**
   - External services (`github-readme-stats`, `github-readme-activity-graph`) currently fail with HTTP 503 and HTTP 402. Generating custom SVGs inside `scripts/svg_hud.py` guarantees 100% uptime, instant GitHub camo caching, and authentic Solo Leveling aesthetics.
2. **7-Axis Heptagonal Radar Chart + Progress HUD (`assets/status-window.svg`):**
   - Computed directly using trigonometry (`math.sin`, `math.cos`) from the 7 skill indexes in `skill-report.json`, paired with Hunter attributes (`STR`, `AGI`, `INT`, `SEN`, `VIT`) and SFIA 8 levels.
3. **Zero External Dependencies:**
   - Keep everything in Python 3 standard library (`unittest`, `xml.etree.ElementTree`, `math`, `json`, `html`) so GitHub Actions runs in <15 seconds with zero `pip install` fragility.

## Task List

### Phase 1: Test Suite & SVG HUD Engine (TDD)
- [x] Task 1: Create `tests/test_analyze.py` with failing tests for SVG HUD generation, XML validation, `--from-report` execution, and README marker/link integrity.
- [x] Task 2: Implement `scripts/svg_hud.py` to generate 5 bespoke animated Solo Leveling SVGs (`system-header.svg`, `status-window.svg`, `shadow-army-raids.svg`, `combat-telemetry.svg`, `monarch-decree.svg`).
- [x] Task 3: Upgrade `scripts/analyze.py` to invoke `svg_hud.generate_all_svgs(report)`, support `--from-report`, and produce an upgraded `<!--SKILL-RANK:START-->` HUD block.

### Checkpoint 1: Core Engine & SVG Verification
- [x] All unit and XML validation tests pass (`python -m unittest discover -s tests -v`).
- [x] All 5 SVGs exist in `assets/` and parse cleanly as strict XML.

### Phase 2: Profile README Overhaul & CI/CD Pipeline
- [x] Task 4: Overhaul `README.md` with the new Solo Leveling System HUD layout, custom SVGs, categorized Legendary Skills arsenal, interactive `<details>` System Lore & Quest Logs, and verified working badges.
- [x] Task 5: Upgrade `.github/workflows/skill-rank.yml` to run the test suite before committing and include `assets/*.svg` in automated commits.

### Checkpoint 2: Final Review & Visual Verification
- [x] Verify all external URLs in `README.md` return HTTP 200.
- [x] Perform 5-axis code review (`code-review-and-quality`).

## Risks and Mitigations
| Risk | Impact | Mitigation |
|---|---|---|
| Unescaped characters (`&`, `<`, `>`) in repo descriptions breaking SVG XML | High | Escape all dynamic text via `html.escape()` and enforce `ElementTree.fromstring()` in tests |
| GitHub API rate limits during local runs | Medium | Add `--from-report` flag to `scripts/analyze.py` to build SVGs and README from existing `skill-report.json` |
| External widget downtime | High | Replace broken 503/402 widgets with self-generated `assets/*.svg` |
