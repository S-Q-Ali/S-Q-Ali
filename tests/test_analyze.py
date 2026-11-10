import json
import os
import sys
import unittest
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import analyze  # noqa: E402


class TestSoloLevelingProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        report_path = os.path.join(REPO_ROOT, "skill-report.json")
        with open(report_path, "r", encoding="utf-8") as fh:
            cls.report = json.load(fh)

    def test_rank_and_sfia_thresholds(self):
        self.assertEqual(analyze.rank_for_score(6.66), "S")
        self.assertEqual(analyze.rank_for_score(1.58), "A")
        self.assertEqual(analyze.rank_for_score(1.10), "B")
        self.assertEqual(analyze.rank_for_score(0.70), "C")
        self.assertEqual(analyze.rank_for_score(0.35), "D")
        self.assertEqual(analyze.rank_for_score(0.10), "E")

        lvl, label = analyze.sfia_for_index(6.66)
        self.assertEqual((lvl, label), (7, "Set strategy"))
        lvl_a, label_a = analyze.sfia_for_index(1.58)
        self.assertEqual((lvl_a, label_a), (4, "Enable"))

    def test_svg_hud_generation_and_xml_validity(self):
        import svg_hud

        assets_dir = os.path.join(REPO_ROOT, "assets")
        generated = svg_hud.generate_all_svgs(self.report, assets_dir=assets_dir)
        expected_files = [
            "system-header.svg",
            "status-window.svg",
            "shadow-army-raids.svg",
            "combat-telemetry.svg",
            "monarch-decree.svg",
        ]
        for fname in expected_files:
            fpath = os.path.join(assets_dir, fname)
            self.assertIn(fname, generated)
            self.assertTrue(os.path.exists(fpath), f"Missing SVG file: {fname}")
            with open(fpath, "r", encoding="utf-8") as fh:
                svg_content = fh.read()
            self.assertGreater(len(svg_content), 1000, f"SVG too small: {fname}")
            # Strictly parse XML to guarantee GitHub renders it without errors
            root = ET.fromstring(svg_content)
            self.assertTrue(root.tag.endswith("svg"), f"Root tag is not <svg> in {fname}")

    def test_build_readme_section_contains_system_hud(self):
        section = analyze.build_readme_section(self.report)
        self.assertIn("assets/status-window.svg", section)
        self.assertIn("S-Rank (Monarch)", section)
        self.assertIn("Video / AI Media Tools", section)
        self.assertIn("S-Q-Creator-Studio", section)

    def test_readme_has_no_broken_third_party_urls(self):
        readme_path = os.path.join(REPO_ROOT, "README.md")
        with open(readme_path, "r", encoding="utf-8") as fh:
            readme = fh.read()
        # Ensure broken 503/402 URLs are removed
        self.assertNotIn("github-readme-stats.vercel.app", readme)
        self.assertNotIn("github-readme-activity-graph.vercel.app", readme)
        # Ensure custom Solo Leveling SVG HUD assets are referenced
        self.assertIn("assets/system-header.svg", readme)
        self.assertIn("assets/status-window.svg", readme)
        self.assertIn("assets/shadow-army-raids.svg", readme)
        self.assertIn("assets/combat-telemetry.svg", readme)
        self.assertIn("assets/monarch-decree.svg", readme)
        # Ensure auto-update markers exist
        self.assertIn(analyze.START_MARKER, readme)
        self.assertIn(analyze.END_MARKER, readme)


if __name__ == "__main__":
    unittest.main()
