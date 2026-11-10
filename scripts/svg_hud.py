#!/usr/bin/env python3
"""Solo Leveling Holographic System HUD SVG Generator.

Generates 5 self-contained, animated SVG 1.1 files in `assets/` directly from
`skill-report.json` using only the Python standard library. Designed to render
flawlessly inside GitHub Flavored Markdown via `<img>` tags with zero reliance
on flaky third-party widget servers.
"""

import html
import math
import os
from collections import Counter

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_ASSETS_DIR = os.path.join(REPO_ROOT, "assets")


def esc(text):
    """Escape text safely for XML/SVG."""
    return html.escape(str(text or ""), quote=True)


def rank_palette(rank):
    """Return (primary_hex, glow_hex, badge_label) for a Solo Leveling rank."""
    table = {
        "S": ("#00E5FF", "#9D4EDD", "S-RANK // MONARCH"),
        "A": ("#A855F7", "#6366F1", "A-RANK // ELITE"),
        "B": ("#38BDF8", "#2563EB", "B-RANK // VETERAN"),
        "C": ("#10B981", "#059669", "C-RANK // SKILLED"),
        "D": ("#F59E0B", "#D97706", "D-RANK // APPRENTICE"),
        "E": ("#94A3B8", "#64748B", "E-RANK // NOVICE"),
    }
    return table.get(rank, table["E"])


def shared_defs():
    """Shared SVG defs: gradients, glow filters, patterns, and CSS animations."""
    return """
  <defs>
    <linearGradient id="bgVoid" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#04060C"/>
      <stop offset="50%" stop-color="#090D1A"/>
      <stop offset="100%" stop-color="#050711"/>
    </linearGradient>
    <linearGradient id="panelBg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0D1428" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#070B16" stop-opacity="0.96"/>
    </linearGradient>
    <linearGradient id="cyanViolet" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00E5FF"/>
      <stop offset="55%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#C084FC"/>
    </linearGradient>
    <linearGradient id="violetCyan" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#9D4EDD"/>
      <stop offset="50%" stop-color="#3B82F6"/>
      <stop offset="100%" stop-color="#00E5FF"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#FDE047"/>
    </linearGradient>
    <linearGradient id="radarFill" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#9D4EDD" stop-opacity="0.48"/>
    </linearGradient>
    <radialGradient id="monarchAura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#7C3AED" stop-opacity="0.32"/>
      <stop offset="55%" stop-color="#00E5FF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#05070E" stop-opacity="0"/>
    </radialGradient>
    <pattern id="sysGrid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 32 0 L 0 0 0 32" fill="none" stroke="#1E293B" stroke-width="0.6" stroke-opacity="0.45"/>
    </pattern>
    <filter id="glowCyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glowSoft" x="-15%" y="-15%" width="130%" height="130%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <style>
      .sys-mono { font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace; }
      .sys-sans { font-family: 'Segoe UI', 'Inter', 'Roboto', Helvetica, Arial, sans-serif; }
      @keyframes pulseGlow {
        0%, 100% { opacity: 0.85; }
        50% { opacity: 1; }
      }
      @keyframes scanline {
        0% { transform: translateY(0px); opacity: 0.0; }
        15% { opacity: 0.35; }
        85% { opacity: 0.35; }
        100% { transform: translateY(320px); opacity: 0.0; }
      }
      @keyframes floatParticle {
        0% { transform: translateY(0px); opacity: 0.15; }
        50% { opacity: 0.75; }
        100% { transform: translateY(-45px); opacity: 0.0; }
      }
      @keyframes blinkAlert {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.35; }
      }
      .pulse { animation: pulseGlow 3s ease-in-out infinite; }
      .blink { animation: blinkAlert 2.2s ease-in-out infinite; }
      .p1 { animation: floatParticle 4.2s ease-in-out infinite; }
      .p2 { animation: floatParticle 5.5s ease-in-out 1.2s infinite; }
      .p3 { animation: floatParticle 3.8s ease-in-out 2.1s infinite; }
    </style>
  </defs>
"""


def hud_frame(x, y, w, h, stroke="#00E5FF", accent="#9D4EDD"):
    """Render a chamfered Solo Leveling System window with corner targeting brackets."""
    c = 14
    pts = f"{x+c},{y} {x+w-c},{y} {x+w},{y+c} {x+w},{y+h-c} {x+w-c},{y+h} {x+c},{y+h} {x},{y+h-c} {x},{y+c}"
    b = 26
    return f"""
  <polygon points="{pts}" fill="url(#panelBg)" stroke="{stroke}" stroke-width="1.2" stroke-opacity="0.55"/>
  <polyline points="{x},{y+c+b} {x},{y+c} {x+c},{y} {x+c+b},{y}" fill="none" stroke="{stroke}" stroke-width="2.6" filter="url(#glowSoft)"/>
  <polyline points="{x+w-c-b},{y} {x+w-c},{y} {x+w},{y+c} {x+w},{y+c+b}" fill="none" stroke="{accent}" stroke-width="2.6" filter="url(#glowSoft)"/>
  <polyline points="{x},{y+h-c-b} {x},{y+h-c} {x+c},{y+h} {x+c+b},{y+h}" fill="none" stroke="{accent}" stroke-width="2.6" filter="url(#glowSoft)"/>
  <polyline points="{x+w-c-b},{y+h} {x+w-c},{y+h} {x+w},{y+h-c} {x+w},{y+h-c-b}" fill="none" stroke="{stroke}" stroke-width="2.6" filter="url(#glowSoft)"/>
"""


def generate_system_header(report):
    """1. assets/system-header.svg: Hero Awakening Banner (1200x340)."""
    top_skill = esc(report.get("top_skill", "Video / AI Media Tools").upper())
    overall_rank = esc(report.get("overall_rank", "S"))
    repos_count = int(report.get("analyzed_repos", 25))
    top_idx = report.get("indexes", {}).get(report.get("top_skill", ""), 6.66)

    particles = []
    coords = [
        (95, 290, 3.0, "#00E5FF", "p1"),
        (210, 310, 2.2, "#9D4EDD", "p2"),
        (340, 280, 3.5, "#00E5FF", "p3"),
        (520, 305, 2.5, "#C084FC", "p1"),
        (740, 295, 3.2, "#00E5FF", "p2"),
        (890, 285, 2.8, "#9D4EDD", "p3"),
        (1040, 300, 3.6, "#00E5FF", "p1"),
        (1120, 270, 2.4, "#C084FC", "p2"),
    ]
    for cx, cy, r, col, cls in coords:
        particles.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" class="{cls}"/>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 340" width="100%" height="100%">
  {shared_defs()}
  <rect width="1200" height="340" rx="14" fill="url(#bgVoid)"/>
  <rect width="1200" height="340" rx="14" fill="url(#sysGrid)"/>
  <circle cx="960" cy="170" r="240" fill="url(#monarchAura)"/>
  <circle cx="240" cy="170" r="200" fill="url(#monarchAura)"/>

  <!-- Rotating Arcane Summoning Sigil (Right Background) -->
  <g transform="translate(975, 170)" opacity="0.26">
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="45s" repeatCount="indefinite"/>
      <circle cx="0" cy="0" r="128" fill="none" stroke="#00E5FF" stroke-width="1.5" stroke-dasharray="10 6"/>
      <circle cx="0" cy="0" r="98" fill="none" stroke="#9D4EDD" stroke-width="1.2"/>
      <polygon points="0,-96 83,48 -83,48" fill="none" stroke="#00E5FF" stroke-width="1.2"/>
      <polygon points="0,96 83,-48 -83,-48" fill="none" stroke="#9D4EDD" stroke-width="1.2"/>
      <circle cx="0" cy="0" r="42" fill="none" stroke="#00E5FF" stroke-width="2" stroke-dasharray="4 4"/>
    </g>
  </g>

  {''.join(particles)}
  {hud_frame(16, 16, 1168, 308)}

  <!-- Top System Notification Bar -->
  <rect x="38" y="34" width="1124" height="34" rx="4" fill="#0B132B" stroke="#00E5FF" stroke-width="0.9" stroke-opacity="0.6"/>
  <circle cx="58" cy="51" r="5" fill="#00E5FF" class="blink" filter="url(#glowCyan)"/>
  <text x="74" y="56" fill="#00E5FF" font-size="12.5" font-weight="700" letter-spacing="2.5" class="sys-mono">
    [ ! ] SYSTEM NOTIFICATION // PLAYER AWAKENING VERIFIED — NATIONAL LEVEL ARCHITECT
  </text>
  <text x="1144" y="56" text-anchor="end" fill="#C084FC" font-size="12" font-weight="700" letter-spacing="1.5" class="sys-mono">
    STATUS: ONLINE • RANK: {overall_rank}-MONARCH
  </text>

  <!-- Left/Center Identity Block -->
  <text x="48" y="106" fill="#94A3B8" font-size="13" font-weight="600" letter-spacing="3" class="sys-mono">
    SHADOW SOVEREIGN OF FULL-STACK, AI AGENTS &amp; VIDEO AUTOMATION
  </text>

  <text x="46" y="164" fill="#FFFFFF" font-size="52" font-weight="900" letter-spacing="3" class="sys-sans" filter="url(#glowSoft)">
    SYED QASIM ALI
  </text>
  <text x="455" y="164" fill="url(#cyanViolet)" font-size="52" font-weight="900" letter-spacing="3" class="sys-sans" opacity="0.18">
    // S-Q-ALI
  </text>

  <!-- Class & Primary Discipline Pills -->
  <g transform="translate(48, 184)">
    <rect x="0" y="0" width="248" height="30" rx="5" fill="#111C38" stroke="#00E5FF" stroke-width="1.2"/>
    <text x="124" y="20" text-anchor="middle" fill="#00E5FF" font-size="12" font-weight="700" letter-spacing="1.5" class="sys-mono">
      ⚔️ CLASS: SHADOW MONARCH
    </text>

    <rect x="262" y="0" width="380" height="30" rx="5" fill="#191034" stroke="#9D4EDD" stroke-width="1.2"/>
    <text x="452" y="20" text-anchor="middle" fill="#E9D5FF" font-size="12" font-weight="700" letter-spacing="1.2" class="sys-mono">
      👑 DOMAIN: {top_skill}
    </text>

    <rect x="656" y="0" width="210" height="30" rx="5" fill="#1E1B10" stroke="#F59E0B" stroke-width="1.2"/>
    <text x="761" y="20" text-anchor="middle" fill="#FDE047" font-size="12" font-weight="700" letter-spacing="1.2" class="sys-mono">
      ★ SFIA L7 · STRATEGY
    </text>
  </g>

  <!-- HP / MP / EXP Bars -->
  <g transform="translate(48, 236)">
    <!-- HP Bar -->
    <text x="0" y="14" fill="#38BDF8" font-size="11.5" font-weight="700" letter-spacing="1.5" class="sys-mono">HP // VITALITY</text>
    <text x="235" y="14" text-anchor="end" fill="#E2E8F0" font-size="11" class="sys-mono">99,999 / 99,999</text>
    <rect x="0" y="21" width="235" height="9" rx="4.5" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>
    <rect x="0" y="21" width="235" height="9" rx="4.5" fill="url(#cyanViolet)"/>

    <!-- MP Bar -->
    <text x="260" y="14" fill="#C084FC" font-size="11.5" font-weight="700" letter-spacing="1.5" class="sys-mono">MP // SHADOW MANA</text>
    <text x="515" y="14" text-anchor="end" fill="#E2E8F0" font-size="11" class="sys-mono">INFINITE (INDEX {top_idx})</text>
    <rect x="260" y="21" width="255" height="9" rx="4.5" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>
    <rect x="260" y="21" width="255" height="9" rx="4.5" fill="url(#violetCyan)"/>

    <!-- EXP Bar -->
    <text x="540" y="14" fill="#FDE047" font-size="11.5" font-weight="700" letter-spacing="1.5" class="sys-mono">EXP // DUNGEONS CLEARED</text>
    <text x="840" y="14" text-anchor="end" fill="#FDE047" font-size="11" font-weight="700" class="sys-mono">{repos_count} REPOSITORIES [LVL. 99]</text>
    <rect x="540" y="21" width="300" height="9" rx="4.5" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>
    <rect x="540" y="21" width="292" height="9" rx="4.5" fill="url(#goldGrad)"/>
  </g>

  <!-- Right Sovereign Emblem Card -->
  <g transform="translate(905, 86)">
    <polygon points="16,0 244,0 260,16 260,192 244,208 16,208 0,192 0,16" fill="#090E20" fill-opacity="0.9" stroke="#00E5FF" stroke-width="1.5"/>
    <text x="130" y="30" text-anchor="middle" fill="#94A3B8" font-size="10.5" font-weight="700" letter-spacing="2" class="sys-mono">
      SOVEREIGN RANK SEAL
    </text>
    <circle cx="130" cy="96" r="46" fill="#120D2B" stroke="url(#cyanViolet)" stroke-width="2.5" filter="url(#glowSoft)"/>
    <text x="130" y="114" text-anchor="middle" fill="#00E5FF" font-size="52" font-weight="900" class="sys-sans" filter="url(#glowCyan)">
      {overall_rank}
    </text>
    <text x="130" y="164" text-anchor="middle" fill="#FFFFFF" font-size="13" font-weight="800" letter-spacing="2.5" class="sys-mono">
      SHADOW MONARCH
    </text>
    <rect x="34" y="174" width="192" height="22" rx="4" fill="#1E103A" stroke="#9D4EDD" stroke-width="1"/>
    <text x="130" y="189" text-anchor="middle" fill="#00E5FF" font-size="11.5" font-weight="800" letter-spacing="3" class="sys-mono blink">
      &gt; COMMAND: "ARISE" &lt;
    </text>
  </g>

  <!-- Bottom Telemetry Strip -->
  <line x1="48" y1="286" x2="880" y2="286" stroke="#1E293B" stroke-width="1"/>
  <text x="48" y="306" fill="#64748B" font-size="11.5" letter-spacing="1.4" class="sys-mono">
    LOCATION: PAKISTAN 🇵🇰  |  EDUCATION: BS COMPUTER SCIENCE (UCP)  |  PORTFOLIO: FLOWPOST-STUDIO.VERCEL.APP
  </text>
</svg>
"""


def generate_status_window(report):
    """2. assets/status-window.svg: Bilateral Status Window + 7-Axis Radar + Skill Bars (1200x580)."""
    indexes = report.get("indexes", {})
    ranks = report.get("ranks", {})
    sfia = report.get("sfia", {})
    updated = esc(report.get("generated_at", "")[:10] or "2026-11-11")
    analyzed_repos = int(report.get("analyzed_repos", 25))
    top_skill = esc(report.get("top_skill", "Video / AI Media Tools"))

    # Fixed canonical skill order for the 7-axis heptagon radar chart
    skill_order = [
        ("Video / AI Media Tools", "VIDEO / AI MEDIA"),
        ("Automation Engineer", "AUTOMATION"),
        ("Frontend Developer", "FRONTEND UI"),
        ("Backend Developer", "BACKEND API"),
        ("AI Engineer", "AI / AGENTS"),
        ("Full-Stack Developer", "FULL-STACK"),
        ("Technical Writing", "TECH DOCS"),
    ]

    # Radar geometry (Center panel)
    cx, cy = 575.0, 315.0
    max_r = 132.0
    n_axes = len(skill_order)

    # Concentric heptagonal rings
    grid_polygons = []
    for pct in (0.25, 0.50, 0.75, 1.0):
        r = max_r * pct
        pts = []
        for i in range(n_axes):
            angle = -math.pi / 2 + (2 * math.pi * i / n_axes)
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            pts.append(f"{px:.1f},{py:.1f}")
        stroke_col = "#00E5FF" if pct == 1.0 else "#1E293B"
        stroke_op = "0.55" if pct == 1.0 else "0.85"
        grid_polygons.append(
            f'<polygon points="{" ".join(pts)}" fill="none" stroke="{stroke_col}" stroke-width="1" stroke-opacity="{stroke_op}"/>'
        )

    # Radar axes, data vertices, and labels
    axis_lines = []
    data_pts = []
    vertex_nodes = []
    axis_labels = []

    for i, (skill_key, short_label) in enumerate(skill_order):
        angle = -math.pi / 2 + (2 * math.pi * i / n_axes)
        ex = cx + max_r * math.cos(angle)
        ey = cy + max_r * math.sin(angle)
        axis_lines.append(
            f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#1E293B" stroke-width="1"/>'
        )

        idx_val = float(indexes.get(skill_key, 0.5))
        # Normalize index onto [0.28, 1.0] so all axes are clearly visible while S-rank peaks hit outer rim
        norm = min(1.0, max(0.28, 0.25 + (idx_val / 6.8) * 0.75))
        vx = cx + (max_r * norm) * math.cos(angle)
        vy = cy + (max_r * norm) * math.sin(angle)
        data_pts.append(f"{vx:.1f},{vy:.1f}")
        vertex_nodes.append(
            f'<circle cx="{vx:.1f}" cy="{vy:.1f}" r="4.5" fill="#00E5FF" stroke="#FFFFFF" stroke-width="1.5" filter="url(#glowSoft)"/>'
        )

        lx = cx + (max_r + 28) * math.cos(angle)
        ly = cy + (max_r + 24) * math.sin(angle)
        anchor = "middle"
        if math.cos(angle) > 0.25:
            anchor = "start"
        elif math.cos(angle) < -0.25:
            anchor = "end"
        axis_labels.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" fill="#E2E8F0" font-size="10.5" font-weight="700" class="sys-mono">{esc(short_label)}</text>'
            f'<text x="{lx:.1f}" y="{ly+13:.1f}" text-anchor="{anchor}" fill="#00E5FF" font-size="9.5" class="sys-mono">IDX {idx_val:.2f}</text>'
        )

    # Right column: Skill Inventory Bars
    skill_rows = []
    sorted_skills = sorted(skill_order, key=lambda item: float(indexes.get(item[0], 0.0)), reverse=True)
    for idx_pos, (skill_key, _) in enumerate(sorted_skills):
        ry = 126 + idx_pos * 60
        idx_val = float(indexes.get(skill_key, 0.0))
        rk = ranks.get(skill_key, "C")
        sfia_pair = sfia.get(skill_key, [3, "Apply"])
        sfia_str = f"SFIA L{sfia_pair[0]} · {sfia_pair[1]}"
        col_primary, _, _ = rank_palette(rk)
        bar_max = 365
        bar_w = int(min(bar_max, max(48, (idx_val / 6.8) * bar_max)))

        skill_rows.append(f"""
  <g transform="translate(780, {ry})">
    <rect x="0" y="0" width="380" height="48" rx="6" fill="#0B1122" stroke="#1E293B" stroke-width="1"/>
    <rect x="10" y="9" width="28" height="20" rx="4" fill="#131C38" stroke="{col_primary}" stroke-width="1.2"/>
    <text x="24" y="23" text-anchor="middle" fill="{col_primary}" font-size="12" font-weight="900" class="sys-mono">{esc(rk)}</text>
    <text x="48" y="23" fill="#F8FAFC" font-size="13" font-weight="700" class="sys-sans">{esc(skill_key)}</text>
    <text x="368" y="23" text-anchor="end" fill="#94A3B8" font-size="10.5" font-weight="600" class="sys-mono">{esc(sfia_str)} | {idx_val:.2f}</text>
    <rect x="10" y="34" width="{bar_max}" height="6" rx="3" fill="#060913"/>
    <rect x="10" y="34" width="{bar_w}" height="6" rx="3" fill="url(#cyanViolet)"/>
  </g>""")

    # Left column: Hunter Core Stats
    stats = [
        ("SEN // MEDIA & AI TOOLING", "99", "S+", "#00E5FF"),
        ("AGI // AUTOMATION & SCRAPERS", "97", "S", "#38BDF8"),
        ("INT // AI AGENTS & LLMS", "96", "S", "#A855F7"),
        ("STR // BACKEND & RUST SYSTEMS", "94", "S", "#C084FC"),
        ("VIT // FRONTEND & FLUTTER UI", "95", "S", "#00E5FF"),
        ("LUK // END-TO-END SHIPPING", "91", "A+", "#F59E0B"),
    ]
    stat_nodes = []
    for i, (label, val, tier, col) in enumerate(stats):
        sy = 278 + i * 42
        stat_nodes.append(f"""
  <g transform="translate(42, {sy})">
    <rect x="0" y="0" width="316" height="34" rx="5" fill="#0B1122" stroke="#1E293B" stroke-width="1"/>
    <text x="12" y="21" fill="#CBD5E1" font-size="11" font-weight="700" class="sys-mono">{esc(label)}</text>
    <text x="262" y="22" text-anchor="end" fill="{col}" font-size="15" font-weight="900" class="sys-mono">{val}</text>
    <rect x="272" y="7" width="34" height="20" rx="4" fill="#131C36" stroke="{col}" stroke-width="1"/>
    <text x="289" y="21" text-anchor="middle" fill="{col}" font-size="10.5" font-weight="800" class="sys-mono">{tier}</text>
  </g>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 580" width="100%" height="100%">
  {shared_defs()}
  <rect width="1200" height="580" rx="14" fill="url(#bgVoid)"/>
  <rect width="1200" height="580" rx="14" fill="url(#sysGrid)"/>
  <circle cx="575" cy="315" r="220" fill="url(#monarchAura)"/>

  {hud_frame(16, 16, 1168, 548)}

  <!-- Window Title Bar -->
  <rect x="38" y="34" width="1124" height="38" rx="5" fill="#0B132B" stroke="#00E5FF" stroke-width="1" stroke-opacity="0.65"/>
  <text x="56" y="58" fill="#00E5FF" font-size="15" font-weight="800" letter-spacing="3" class="sys-mono">
    [ STATUS WINDOW ] // HUNTER ATTRIBUTES &amp; SKILL INVENTORY
  </text>
  <text x="1144" y="58" text-anchor="end" fill="#94A3B8" font-size="11.5" font-weight="600" class="sys-mono">
    SCOUT SYNC: {updated} • {analyzed_repos} REPOS ANALYZED
  </text>

  <!-- Column 1: Player Profile & Core Stats -->
  <text x="42" y="106" fill="#00E5FF" font-size="12.5" font-weight="800" letter-spacing="2" class="sys-mono">
    01 // HUNTER IDENTIFICATION
  </text>
  <rect x="42" y="118" width="316" height="126" rx="8" fill="#0B1122" stroke="#9D4EDD" stroke-width="1.2" stroke-opacity="0.7"/>
  <text x="58" y="144" fill="#94A3B8" font-size="11" class="sys-mono">NAME:</text>
  <text x="145" y="144" fill="#FFFFFF" font-size="13" font-weight="800" class="sys-sans">Syed Qasim Ali (S-Q-Ali)</text>

  <text x="58" y="168" fill="#94A3B8" font-size="11" class="sys-mono">TITLE:</text>
  <text x="145" y="168" fill="#C084FC" font-size="12.5" font-weight="700" class="sys-sans">Shadow Monarch of Code</text>

  <text x="58" y="192" fill="#94A3B8" font-size="11" class="sys-mono">SPECIALTY:</text>
  <text x="145" y="192" fill="#00E5FF" font-size="12.5" font-weight="700" class="sys-sans">{top_skill}</text>

  <text x="58" y="216" fill="#94A3B8" font-size="11" class="sys-mono">DEGREE:</text>
  <text x="145" y="216" fill="#E2E8F0" font-size="12" font-weight="600" class="sys-sans">BS Computer Science (UCP)</text>

  <text x="42" y="266" fill="#00E5FF" font-size="12.5" font-weight="800" letter-spacing="2" class="sys-mono">
    02 // CORE COMBAT ATTRIBUTES
  </text>
  {''.join(stat_nodes)}

  <!-- Column 2: 7-Axis Heptagonal Radar Matrix -->
  <text x="575" y="106" text-anchor="middle" fill="#00E5FF" font-size="12.5" font-weight="800" letter-spacing="2" class="sys-mono">
    03 // 7-AXIS DOMAIN RESONANCE MATRIX
  </text>
  {''.join(grid_polygons)}
  {''.join(axis_lines)}
  <polygon points="{' '.join(data_pts)}" fill="url(#radarFill)" stroke="#00E5FF" stroke-width="2.4" filter="url(#glowSoft)"/>
  {''.join(vertex_nodes)}
  {''.join(axis_labels)}

  <rect x="415" y="492" width="320" height="44" rx="6" fill="#0B1122" stroke="#1E293B" stroke-width="1"/>
  <text x="575" y="511" text-anchor="middle" fill="#E2E8F0" font-size="11" font-weight="700" class="sys-mono">
    OVERALL EVALUATION: S-RANK MONARCH
  </text>
  <text x="575" y="527" text-anchor="middle" fill="#94A3B8" font-size="10" class="sys-mono">
    5 S-Rank • 1 A-Rank • 1 C-Rank across 7 Engineering Domains
  </text>

  <!-- Column 3: Skill Inventory Ranks & SFIA 8 -->
  <text x="780" y="106" fill="#00E5FF" font-size="12.5" font-weight="800" letter-spacing="2" class="sys-mono">
    04 // ACTIVE SKILL INVENTORY (SFIA 8)
  </text>
  {''.join(skill_rows)}
</svg>
"""


def generate_shadow_army_raids(report):
    """3. assets/shadow-army-raids.svg: 6-Card Holographic Bento Grid of Flagship Repos (1200x520)."""
    raids = [
        {
            "name": "S-Q-Creator-Studio",
            "rank": "S-RANK BOSS",
            "stack": "PYTHON • AI MEDIA • FFMPEG • BROWSER",
            "desc1": "Bulk-download TikTok, YouTube, Instagram & Facebook videos,",
            "desc2": "reframe 9:16 shorts in Vertical Studio & verify creator accounts.",
            "metric": "INDEX 21.43 // MEDIA SOVEREIGN",
            "color": "#00E5FF",
        },
        {
            "name": "flowpost-studio",
            "rank": "S-RANK BOSS",
            "stack": "DART / FLUTTER • SUPABASE • WINDOWS",
            "desc1": "Native cross-platform studio to schedule & auto-publish videos",
            "desc2": "to YouTube Shorts, TikTok, Instagram, Facebook & LinkedIn.",
            "metric": "INDEX 16.43 // MULTI-PLATFORM",
            "color": "#A855F7",
        },
        {
            "name": "Easy-Window",
            "rank": "S-RANK RAID",
            "stack": "RUST • WINDOWS 11 SYSTEMS • SAFETY RAILS",
            "desc1": "High-speed Windows 11 system utility detecting persistent Chrome",
            "desc2": "sessions & background processes wasting CPU, RAM, disk or GPU.",
            "metric": "SYSTEMS ENGINEERING // RUST",
            "color": "#38BDF8",
        },
        {
            "name": "Editor-Agent",
            "rank": "S-RANK RAID",
            "stack": "PYTHON • AI AGENT • VIDEO PIPELINE",
            "desc1": "Autonomous AI video editing & media orchestration agent built",
            "desc2": "for intelligent clip assembly, automated cuts & creator workflows.",
            "metric": "INDEX 6.23 // AUTONOMOUS AI",
            "color": "#C084FC",
        },
        {
            "name": "SnipVid",
            "rank": "A-RANK RAID",
            "stack": "TYPESCRIPT • MODERN WEB • VERCEL",
            "desc1": "Precision web-based video clipping & content creator toolkit",
            "desc2": "engineered for rapid short-form extraction and web publishing.",
            "metric": "LIVE APP // SNIP-VID.VERCEL.APP",
            "color": "#00E5FF",
        },
        {
            "name": "Auto-Captions & Vid-Automator",
            "rank": "A-RANK RAID",
            "stack": "TYPESCRIPT & PYTHON • SPEECH AI • BOTS",
            "desc1": "End-to-end automated video transcription, dynamic subtitle",
            "desc2": "rendering, and headless content pipeline automation engines.",
            "metric": "AI TRANSCRIPTION & PIPELINES",
            "color": "#F59E0B",
        },
    ]

    cards_svg = []
    for idx, raid in enumerate(raids):
        col = idx % 3
        row = idx // 3
        cx = 40 + col * 378
        cy = 92 + row * 202
        accent = raid["color"]
        cards_svg.append(f"""
  <g transform="translate({cx}, {cy})">
    <polygon points="12,0 352,0 364,12 364,174 352,186 12,186 0,174 0,12" fill="#0B1122" stroke="{accent}" stroke-width="1.3" stroke-opacity="0.75"/>
    <polyline points="0,28 0,12 12,0 28,0" fill="none" stroke="{accent}" stroke-width="2.5"/>
    <polyline points="336,186 352,186 364,174 364,158" fill="none" stroke="{accent}" stroke-width="2.5"/>

    <rect x="16" y="16" width="112" height="22" rx="4" fill="#131C38" stroke="{accent}" stroke-width="1"/>
    <text x="72" y="31" text-anchor="middle" fill="{accent}" font-size="10.5" font-weight="800" letter-spacing="1.2" class="sys-mono">
      {esc(raid["rank"])}
    </text>
    <text x="348" y="31" text-anchor="end" fill="#64748B" font-size="10.5" font-weight="700" class="sys-mono">
      SHADOW UNIT #{idx+1:02d}
    </text>

    <text x="16" y="64" fill="#FFFFFF" font-size="18" font-weight="800" class="sys-sans">
      ⚔️ {esc(raid["name"])}
    </text>
    <text x="16" y="86" fill="{accent}" font-size="10.5" font-weight="700" letter-spacing="1" class="sys-mono">
      {esc(raid["stack"])}
    </text>

    <text x="16" y="114" fill="#CBD5E1" font-size="12" class="sys-sans">
      {esc(raid["desc1"])}
    </text>
    <text x="16" y="132" fill="#CBD5E1" font-size="12" class="sys-sans">
      {esc(raid["desc2"])}
    </text>

    <line x1="16" y1="148" x2="348" y2="148" stroke="#1E293B" stroke-width="1"/>
    <text x="16" y="168" fill="#94A3B8" font-size="10.5" font-weight="700" letter-spacing="1" class="sys-mono">
      ✦ {esc(raid["metric"])}
    </text>
    <text x="348" y="168" text-anchor="end" fill="#00E5FF" font-size="10.5" font-weight="800" class="sys-mono">
      EXTRACTED ✓
    </text>
  </g>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520" width="100%" height="100%">
  {shared_defs()}
  <rect width="1200" height="520" rx="14" fill="url(#bgVoid)"/>
  <rect width="1200" height="520" rx="14" fill="url(#sysGrid)"/>
  <circle cx="600" cy="260" r="280" fill="url(#monarchAura)"/>

  {hud_frame(16, 16, 1168, 488)}

  <rect x="38" y="34" width="1124" height="38" rx="5" fill="#0B132B" stroke="#9D4EDD" stroke-width="1" stroke-opacity="0.7"/>
  <text x="56" y="58" fill="#C084FC" font-size="15" font-weight="800" letter-spacing="3" class="sys-mono">
    [ SHADOW ARMY EXTRACTION ] // S-RANK DUNGEON RAIDS &amp; FLAGSHIP SYSTEMS
  </text>
  <text x="1144" y="58" text-anchor="end" fill="#00E5FF" font-size="11.5" font-weight="700" class="sys-mono">
    6 COMMANDER-GRADE REPOSITORIES ACTIVE
  </text>

  {''.join(cards_svg)}
</svg>
"""


def generate_combat_telemetry(report):
    """4. assets/combat-telemetry.svg: Daily Quest Alert + Language Telemetry + Combat Record (1200x380)."""
    repos = report.get("repos", [])
    lang_counts = Counter(r.get("lang") for r in repos if r.get("lang"))
    total_lang_repos = max(1, sum(lang_counts.values()))

    # Ensure top languages are represented cleanly
    preferred_langs = [
        ("Python", "#00E5FF"),
        ("JavaScript", "#FDE047"),
        ("TypeScript", "#38BDF8"),
        ("HTML", "#F43F5E"),
        ("C#", "#A855F7"),
        ("Dart / Rust", "#10B981"),
    ]
    lang_rows = []
    for i, (lname, lcol) in enumerate(preferred_langs):
        if lname == "Dart / Rust":
            cnt = lang_counts.get("Dart", 0) + lang_counts.get("Rust", 0)
        else:
            cnt = lang_counts.get(lname, 0)
        pct = int(round((cnt / total_lang_repos) * 100)) if cnt else 8
        bar_w = int(min(220, max(28, (pct / 45.0) * 220)))
        ly = 132 + i * 36
        lang_rows.append(f"""
    <g transform="translate(432, {ly})">
      <text x="0" y="14" fill="#E2E8F0" font-size="11.5" font-weight="700" class="sys-mono">{esc(lname)}</text>
      <text x="336" y="14" text-anchor="end" fill="{lcol}" font-size="11" font-weight="800" class="sys-mono">{cnt} REPOS ({pct}%)</text>
      <rect x="0" y="20" width="336" height="6" rx="3" fill="#060913"/>
      <rect x="0" y="20" width="{bar_w}" height="6" rx="3" fill="{lcol}"/>
    </g>""")

    quests = [
        ("[✓] AI & Video Tooling Mastery", "COMPLETE // S-RANK"),
        ("[✓] Multi-Platform Desktop & Web Apps", "COMPLETE // S-RANK"),
        ("[✓] Systems Optimization (Rust / Win11)", "COMPLETE // S-RANK"),
        ("[✓] Autonomous Agent Workflows", "COMPLETE // S-RANK"),
        ("[!] Daily Commit & Open-Source Grind", "IN PROGRESS // ACTIVE"),
    ]
    quest_rows = []
    for i, (qtitle, qstatus) in enumerate(quests):
        qy = 132 + i * 36
        qcol = "#00E5FF" if "COMPLETE" in qstatus else "#FDE047"
        quest_rows.append(f"""
    <g transform="translate(48, {qy})">
      <rect x="0" y="0" width="340" height="28" rx="4" fill="#0B1122" stroke="#1E293B" stroke-width="1"/>
      <text x="10" y="18" fill="#F8FAFC" font-size="11" font-weight="600" class="sys-sans">{esc(qtitle)}</text>
      <text x="330" y="18" text-anchor="end" fill="{qcol}" font-size="9.5" font-weight="800" class="sys-mono">{esc(qstatus)}</text>
    </g>""")

    metrics = [
        ("PEAK SKILL INDEX", str(report.get("indexes", {}).get(report.get("top_skill", ""), 6.66)), "VIDEO / AI MEDIA", "#00E5FF"),
        ("S-RANK DISCIPLINES", "5 / 7", "MONARCH TIER", "#A855F7"),
        ("SFIA RESPONSIBILITY", "LEVEL 7", "SET STRATEGY", "#FDE047"),
        ("PUBLIC REPOSITORIES", str(report.get("analyzed_repos", 25)), "VERIFIED TELEMETRY", "#38BDF8"),
    ]
    metric_cards = []
    for i, (mtitle, mval, msub, mcol) in enumerate(metrics):
        mx = 812 + (i % 2) * 174
        my = 126 + (i // 2) * 104
        metric_cards.append(f"""
    <g transform="translate({mx}, {my})">
      <rect x="0" y="0" width="162" height="92" rx="6" fill="#0B1122" stroke="{mcol}" stroke-width="1.2" stroke-opacity="0.7"/>
      <text x="81" y="24" text-anchor="middle" fill="#94A3B8" font-size="9.5" font-weight="700" letter-spacing="1" class="sys-mono">{esc(mtitle)}</text>
      <text x="81" y="58" text-anchor="middle" fill="{mcol}" font-size="26" font-weight="900" class="sys-mono">{esc(mval)}</text>
      <text x="81" y="78" text-anchor="middle" fill="#CBD5E1" font-size="9.5" font-weight="600" class="sys-mono">{esc(msub)}</text>
    </g>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="100%" height="100%">
  {shared_defs()}
  <rect width="1200" height="380" rx="14" fill="url(#bgVoid)"/>
  <rect width="1200" height="380" rx="14" fill="url(#sysGrid)"/>

  {hud_frame(16, 16, 1168, 348)}

  <rect x="38" y="34" width="1124" height="38" rx="5" fill="#0B132B" stroke="#00E5FF" stroke-width="1" stroke-opacity="0.65"/>
  <text x="56" y="58" fill="#00E5FF" font-size="15" font-weight="800" letter-spacing="3" class="sys-mono">
    [ QUEST DIRECTIONS &amp; COMBAT TELEMETRY ] // LIVE SYSTEM ANALYTICS
  </text>
  <text x="1144" y="58" text-anchor="end" fill="#F43F5E" font-size="11.5" font-weight="800" class="sys-mono blink">
    [ ! ] PENALTY ZONE PROTECTION: ACTIVE
  </text>

  <!-- Panel 1: Daily Quest Log -->
  <text x="48" y="108" fill="#00E5FF" font-size="12" font-weight="800" letter-spacing="2" class="sys-mono">
    01 // DAILY QUEST: STRENGTH TRAINING
  </text>
  {''.join(quest_rows)}
  <text x="48" y="334" fill="#F43F5E" font-size="10.5" font-weight="700" class="sys-mono">
    ※ WARNING: Ceasing daily commits triggers Penalty Dungeon transfer.
  </text>

  <!-- Panel 2: Language Affinity -->
  <text x="432" y="108" fill="#C084FC" font-size="12" font-weight="800" letter-spacing="2" class="sys-mono">
    02 // MANA AFFINITY (LANGUAGE DISTRIBUTION)
  </text>
  {''.join(lang_rows)}

  <!-- Panel 3: Combat Record Counters -->
  <text x="812" y="108" fill="#FDE047" font-size="12" font-weight="800" letter-spacing="2" class="sys-mono">
    03 // MONARCH COMBAT RECORD
  </text>
  {''.join(metric_cards)}
</svg>
"""


def generate_monarch_decree():
    """5. assets/monarch-decree.svg: Cinematic Shadow Extraction Footer Banner (1200x190)."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 190" width="100%" height="100%">
  {shared_defs()}
  <rect width="1200" height="190" rx="14" fill="url(#bgVoid)"/>
  <rect width="1200" height="190" rx="14" fill="url(#sysGrid)"/>
  <circle cx="600" cy="95" r="260" fill="url(#monarchAura)"/>

  {hud_frame(16, 16, 1168, 158, stroke="#9D4EDD", accent="#00E5FF")}

  <text x="600" y="58" text-anchor="middle" fill="#00E5FF" font-size="12" font-weight="800" letter-spacing="4" class="sys-mono">
    [ SOVEREIGN DECREE // SHADOW EXTRACTION PROTOCOL ]
  </text>

  <text x="600" y="104" text-anchor="middle" fill="#FFFFFF" font-size="30" font-weight="900" letter-spacing="4" class="sys-sans" filter="url(#glowSoft)">
    “I ALONE LEVEL UP — SO DOES EVERY LINE OF MY CODE.”
  </text>

  <text x="600" y="138" text-anchor="middle" fill="#C084FC" font-size="13" font-weight="700" letter-spacing="3" class="sys-mono">
    ⚔️ SYED QASIM ALI (S-Q-ALI) • ARISE FROM THE SHADOWS • PAKISTAN 🇵🇰 ⚔️
  </text>
</svg>
"""


def generate_all_svgs(report, assets_dir=DEFAULT_ASSETS_DIR):
    """Generate all 5 Solo Leveling SVG files in `assets_dir` and return their filenames."""
    os.makedirs(assets_dir, exist_ok=True)
    files = {
        "system-header.svg": generate_system_header(report),
        "status-window.svg": generate_status_window(report),
        "shadow-army-raids.svg": generate_shadow_army_raids(report),
        "combat-telemetry.svg": generate_combat_telemetry(report),
        "monarch-decree.svg": generate_monarch_decree(),
    }
    for fname, content in files.items():
        fpath = os.path.join(assets_dir, fname)
        with open(fpath, "w", encoding="utf-8") as fh:
            fh.write(content.strip() + "\n")
    return list(files.keys())
