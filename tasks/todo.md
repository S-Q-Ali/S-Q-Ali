# Task List: Solo Leveling GitHub Profile Overhaul

## Task 1: Write TDD Test Suite (`tests/test_analyze.py`)
**Description:** Create unit and integration tests verifying skill scoring, rank/SFIA thresholds, generation of all 5 animated SVGs, strict XML validity of each SVG, and absence of broken 503/402 widget URLs in `README.md`.
**Acceptance criteria:**
- [x] `tests/test_analyze.py` covers `rank_for_score`, `sfia_for_index`, `build_readme_section`, SVG generation, XML parsing, and README URL checks.
**Verification:**
- [x] Run `python -m unittest discover -s tests -v`

## Task 2: Build Solo Leveling SVG HUD Generator (`scripts/svg_hud.py`)
**Description:** Build pure-Python generator producing 5 animated Solo Leveling SVGs in `assets/`:
1. `assets/system-header.svg` (Hero awakening banner with animated runes, particles, HP/MP/XP bars, and ARISE prompt)
2. `assets/status-window.svg` (Hunter Status Card + 7-Axis Radar Chart + Skill Inventory Bars + SFIA levels)
3. `assets/shadow-army-raids.svg` (6-Card Holographic Bento Grid of Flagship Projects)
4. `assets/combat-telemetry.svg` (Daily Quest Notification Window + Multi-Language Mastery Breakdown + Repo Telemetry)
5. `assets/monarch-decree.svg` (Animated Shadow Extraction Footer Banner)
**Acceptance criteria:**
- [x] All 5 SVGs generate deterministically from `skill-report.json`.
- [x] Every SVG passes `xml.etree.ElementTree.fromstring()` validation.
**Verification:**
- [x] Run `python -m unittest discover -s tests -v`

## Task 3: Upgrade `scripts/analyze.py`
**Description:** Integrate `svg_hud.py` into `scripts/analyze.py`, add `--from-report` CLI flag, and upgrade `build_readme_section(report)` to render a sleek Solo Leveling System HUD summary + collapsible detailed skill inventory table.
**Acceptance criteria:**
- [x] `python scripts/analyze.py --from-report` updates `assets/*.svg` and `README.md` without hitting network errors.
**Verification:**
- [x] Run `python scripts/analyze.py --from-report` and `python -m unittest discover -s tests -v`

## Task 4: Overhaul `README.md`
**Description:** Rewrite `README.md` into an immersive Solo Leveling System Interface featuring the 5 custom animated SVGs, clickable Dungeon Raid project links, upgraded Tech Arsenal (Python, TypeScript, Dart/Flutter, Rust, React, Next.js, Node.js, C#, Tailwind, etc.), interactive `<details>` System Log, Contribution Snake, and Guild Connections.
**Acceptance criteria:**
- [x] Zero broken 503/402 URLs in `README.md`.
- [x] `<!--SKILL-RANK:START-->` and `<!--SKILL-RANK:END-->` markers intact and populated.
**Verification:**
- [x] Test all external URLs in `README.md` and run `python -m unittest discover -s tests -v`.

## Task 5: Upgrade CI Workflow (`.github/workflows/skill-rank.yml`)
**Description:** Add unit test step and stage `assets/*.svg` alongside `README.md` and `skill-report.json`.
**Acceptance criteria:**
- [x] Workflow runs `python -m unittest discover -s tests -v` and commits `assets/*.svg`.
**Verification:**
- [x] Inspect workflow YAML and verify git status.
