# Spec: Solo Leveling "Shadow Monarch System HUD" GitHub Profile Overhaul

## 1. Objective
Transform the `S-Q-Ali/S-Q-Ali` GitHub Profile from a generic, partially broken widget page into an unmistakable, bespoke **Solo Leveling System UI ("Shadow Sovereign HUD")** that makes any visitor or recruiter immediately say *"Whoa, cool!"* while showcasing real engineering depth across AI, Video/Media Automation, Full-Stack, Flutter, and Rust systems.

### Key Audit Findings Fixed by This Spec
1. **Broken Third-Party Widgets Eliminated:**
   - `github-readme-stats.vercel.app/api?username=s-q-ali` (HTTP 503 Server Unavailable)
   - `github-readme-stats.vercel.app/api/top-langs/?username=s-q-ali` (HTTP 503 Server Unavailable)
   - `github-readme-activity-graph.vercel.app/graph?username=s-q-ali` (HTTP 402 Payment Required)
2. **Bespoke Animated SVG System Windows (Zero External Failure Points):**
   - Replace broken external cards and plain markdown tables with self-hosted, data-driven, animated SVGs generated in `assets/` by `scripts/analyze.py` and `scripts/svg_hud.py`.
3. **True Portfolio Representation:**
   - Highlight `S-Q-Ali`'s real flagship projects (`S-Q-Creator-Studio`, `flowpost-studio`, `Easy-Window`, `Editor-Agent`, `SnipVid`, `Auto-Captions`, `Vid-Automator`) and true multi-language stack (`Python`, `TypeScript`, `Dart/Flutter`, `Rust`, `JavaScript`, `React`, `Node.js`, `C#`, `HTML/CSS`, `Tailwind`, `Supabase`).
4. **Cohesive Solo Leveling Visual Identity:**
   - Replace generic pink (`#F72585`) and out-of-place Steve Jobs quotes with the authentic **System Blue/Cyan (`#00E5FF`) + Shadow Monarch Violet (`#9D4EDD`) + Sovereign Gold (`#F59E0B`)** on Abyssal Obsidian (`#050811`).

## 2. Tech Stack & Constraints
- **Runtime:** Python 3.12+ (Standard Library ONLY — zero third-party `pip` packages so CI runs instantaneously on any GitHub runner).
- **Graphics Format:** Animated SVG 1.1 (`<style>` CSS `@keyframes` + SMIL `<animate>`, linear/radial gradients, glow filters, vector HUD geometry) rendered via `<img src="assets/...">` in GitHub Flavored Markdown.
- **Automation:** GitHub Actions (`.github/workflows/skill-rank.yml` and `.github/workflows/generate_snake.yml`).

## 3. Commands
```bash
# Run unit and SVG validation test suite
python -m unittest discover -s tests -v

# Run analyzer offline using cached/existing report data to regenerate SVGs & README
python scripts/analyze.py --from-report

# Run full live GitHub API analysis + SVG & README update
python scripts/analyze.py
```

## 4. Project Structure
```text
S-Q-Ali/
├── .github/workflows/
│   ├── generate_snake.yml       # Contribution snake action (every 12h)
│   └── skill-rank.yml           # Daily analyzer + test gate + SVG/README auto-commit
├── assets/
│   ├── system-header.svg        # Animated Solo Leveling System Hero Banner
│   ├── status-window.svg        # Hunter Status HUD + 7-Axis Radar Chart + Skill Bars
│   ├── shadow-army-raids.svg    # 6-Card Holographic Bento Grid of Flagship Repos
│   ├── combat-telemetry.svg     # Language Mastery + Daily Quest + System Telemetry HUD
│   └── monarch-decree.svg       # Animated "ARISE" Shadow Extraction Footer Banner
├── docs/
│   ├── SPEC.md                  # System specification
│   └── DESIGN_PHILOSOPHY.md     # Visual & aesthetic manifesto
├── scripts/
│   ├── analyze.py               # GitHub repo analyzer & README/SVG orchestrator
│   └── svg_hud.py               # Pure-Python Solo Leveling SVG HUD generator
├── tasks/
│   ├── plan.md                  # Implementation plan
│   └── todo.md                  # Verifiable task checklist
├── tests/
│   └── test_analyze.py          # Automated tests for scoring, XML validity & README integrity
├── README.md                    # GitHub Profile entry point
└── skill-report.json            # Generated portfolio telemetry data
```

## 5. Code Style & Conventions
- Pure Python standard library (`json`, `os`, `re`, `math`, `html`, `xml.etree.ElementTree`, `unittest`).
- All dynamic strings injected into SVG templates must be escaped with `html.escape(..., quote=True)` and validated with `xml.etree.ElementTree.fromstring()` to guarantee valid XML.

## 6. Boundaries
- **Always:** Validate every generated SVG with `xml.etree.ElementTree.fromstring`, run `unittest` before committing, preserve `<!--SKILL-RANK:START-->` and `<!--SKILL-RANK:END-->` markers.
- **Ask First:** Adding external Python dependencies or modifying branch names.
- **Never:** Hardcode tokens/secrets, use broken 503/402 widget URLs, or break offline/cached execution.

## 7. Success Criteria
- [ ] `python -m unittest discover -s tests -v` passes 100%.
- [ ] All 5 SVG files in `assets/` are generated, valid XML, visually rich, and animated.
- [ ] `README.md` contains zero broken 503/402 URLs and renders a complete, cohesive Solo Leveling System interface.
- [ ] `.github/workflows/skill-rank.yml` runs tests and commits `README.md`, `skill-report.json`, and `assets/*.svg`.
