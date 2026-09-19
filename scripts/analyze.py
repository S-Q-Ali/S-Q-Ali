#!/usr/bin/env python3
"""Solo Leveling Skill Rank Analyzer

Fetches all public repos of a GitHub user, analyzes language/framework/keyword
signals, computes a skill score per domain, maps it to an E-D-C-B-A-S rank,
writes skill-report.json and updates the README section between the markers:
    <!--SKILL-RANK:START--> ... <!--SKILL-RANK:END-->
Only the Python standard library is used so it runs on any GitHub runner.
"""

import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

USER = os.environ.get("GITHUB_USER", "S-Q-Ali")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_PATH = os.path.join(REPO_ROOT, "skill-report.json")
README_PATH = os.path.join(REPO_ROOT, "README.md")
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")

START_MARKER = "<!--SKILL-RANK:START-->"
END_MARKER = "<!--SKILL-RANK:END-->"

# Skill index = total contribution / analyzed repos. Rank comes from the
# index (not the raw score) so thresholds stay stable no matter how many
# repos are analyzed. Higher index => more projects consistently matching.
RANK_THRESHOLDS = [
    (2.0, "S"),
    (1.5, "A"),
    (1.0, "B"),
    (0.6, "C"),
    (0.3, "D"),
    (0.0, "E"),
]

# Mapping of skill index onto the SFIA 8 responsibility levels (1-7).
# This is an approximation: SFIA is normally assessed via evidence/rubric,
# here we use the repo-derived index as a proxy signal.
SFIA_THRESHOLDS = [
    (3.0, 7, "Set strategy"),
    (2.2, 6, "Initiate"),
    (1.6, 5, "Ensure"),
    (1.1, 4, "Enable"),
    (0.6, 3, "Apply"),
    (0.3, 2, "Assist"),
    (0.0, 1, "Follow"),
]

# Keyword matching costs for a repo's text signals.
WEIGHT_NAME = 3.0
WEIGHT_DESC = 2.0
WEIGHT_TOPIC = 1.5
WEIGHT_README = 0.5
README_MAX_HITS = 6
STRENGTH_KW = 0.8
STRENGTH_LANG = 2.0

# Recency multiplier applied per repo based on last push.
RECENCY_WINDOWS = [(90, 1.5), (180, 1.2), (365, 1.0)]

SKILLS = {
    "AI Engineer": {
        "langs": {"Python": 1.0, "Jupyter Notebook": 0.9},
        "keywords": [
            "ai", "ml engineer", "machine learning", "deep learning", "neural",
            "pytorch", "tensorflow", "keras", "openai", "langchain", "llm", "gpt",
            "agent", "veo", "flux", "whisper", "transformer", "fine-tun", "inference",
            "genai", "generative", "prediction", "caption", "lip sync", "auto caption",
        ],
        "role": "AI / Machine Learning Engineer",
        "blurb": "Building models, agents and generative AI tooling.",
    },
    "Frontend Developer": {
        "langs": {"JavaScript": 1.0, "TypeScript": 1.0, "HTML": 0.7, "CSS": 0.7},
        "keywords": [
            "react", "vue", "nextjs", "next.js", "angular", "tailwind", "frontend",
            "front-end", "ui ", "ux ", "website", "portfolio", "landing page",
            "dashboard", "web app",
        ],
        "role": "Frontend Web Developer",
        "blurb": "Crafting interfaces with React/TypeScript and modern CSS.",
    },
    "Backend Developer": {
        "langs": {"JavaScript": 0.6, "TypeScript": 0.6, "Python": 0.7, "SQL": 0.8,
                   "C#": 0.5, "PHP": 0.5, "Go": 0.5},
        "keywords": [
            "api", "backend", "back-end", "server", "nodejs", "node.js", "express",
            "django", "flask", "fastapi", "rest", "graphql", "database", "sql",
            "postgres", "mysql", "mongodb", "hrms", "auth",
        ],
        "role": "Backend / API Developer",
        "blurb": "Designing servers, databases and REST/GraphQL APIs.",
    },
    "Full-Stack Developer": {
        "langs": {"JavaScript": 1.0, "TypeScript": 1.0, "HTML": 0.5, "CSS": 0.5,
                   "Python": 0.5},
        "keywords": [
            "fullstack", "full-stack", "mern", "crud", "ecommerce", "e-commerce",
            "buy ", "shop", "portal", "hrms", "web app", "store",
        ],
        "role": "Full-Stack Web Developer",
        "blurb": "Shipping end-to-end products across the whole stack.",
    },
    "Automation Engineer": {
        "langs": {"Python": 1.0, "JavaScript": 0.6},
        "keywords": [
            "automation", "scrape", "scraper", "bot", "workflow", "playwright",
            "selenium", "auto", "scheduler", "otp", "extractor", "crawler", "pipeline",
        ],
        "role": "Automation Engineer",
        "blurb": "Scripting scrapers, bots and data pipelines.",
    },
    "Video / AI Media Tools": {
        "langs": {"Python": 1.0, "TypeScript": 0.8, "JavaScript": 0.7},
        "keywords": [
            "video", "editor", "caption", "youtube", "tiktok", "snip", "clip",
            "studio", "creator", "content", "ffmpeg", "stream", "cut ", "veo",
            "flux", "lip sync", "openshot",
        ],
        "role": "Video / Media Tooling Engineer",
        "blurb": "Automating video workflows and content tools.",
    },
    "Technical Writing": {
        "langs": {},
        "keywords": [
            "user guide", "userguide", "documentation", "docs", "guide", "manual",
            "tutorial", "walkthrough",
        ],
        "role": "Technical Writer",
        "blurb": "Producing clear guides and product documentation.",
    },
}


def api_get(path, accept_raw=False):
    """GET a GitHub API path, with optional local disk cache for raw readmes."""
    url = API + path
    req_headers = {
        "Accept": "application/vnd.github.raw" if accept_raw else "application/vnd.github+json",
        "User-Agent": "skill-rank-analyzer",
    }
    if TOKEN:
        req_headers["Authorization"] = "Bearer " + TOKEN

    cache_key = path.replace("/", "_").replace("?", "_")
    cache_file = os.path.join(CACHE_DIR, cache_key + (".txt" if accept_raw else ".json"))
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as fh:
            return json.load(fh) if not accept_raw else fh.read()
    if os.environ.get("SKIP_NET") == "1":
        return None
    if os.environ.get("SKIP_CACHE") == "1":
        cache_file = None

    for attempt in range(3):
        req = urllib.request.Request(url, headers=req_headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read()
                if accept_raw:
                    text = body.decode("utf-8", errors="replace")
                    if cache_file:
                        os.makedirs(CACHE_DIR, exist_ok=True)
                        with open(cache_file, "w", encoding="utf-8") as fh:
                            fh.write(text)
                    return text
                data = json.loads(body.decode("utf-8"))
                if cache_file:
                    os.makedirs(CACHE_DIR, exist_ok=True)
                    with open(cache_file, "w", encoding="utf-8") as fh:
                        json.dump(data, fh)
                return data
        except urllib.error.HTTPError as err:
            if err.code == 429 or err.code >= 500:
                time.sleep(5 * (attempt + 1))
                continue
            if err.code == 404:
                return None
            if err.code == 403:
                remaining = err.headers.get("X-RateLimit-Remaining")
                if remaining == "0":
                    reset = int(err.headers.get("X-RateLimit-Reset", "0"))
                    wait = max(0, reset - int(time.time())) + 2
                    print("  rate-limited; sleeping %ss" % wait, file=sys.stderr)
                    time.sleep(min(wait, 900))
                    continue
            print("  API error %s on %s" % (err.code, url), file=sys.stderr)
            return None
        except urllib.error.URLError as err:
            print("  network error: %s" % err.reason, file=sys.stderr)
            time.sleep(3)
    return None


def fetch_repos():
    repos, page = [], 1
    while True:
        data = api_get("/users/%s/repos?per_page=100&page=%d&sort=updated" % (USER, page))
        if not isinstance(data, list):
            break
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1
    return repos


def rank_for_score(score):
    for threshold, rank in RANK_THRESHOLDS:
        if score >= threshold:
            return rank
    return "E"


def sfia_for_index(index):
    for threshold, level, label in SFIA_THRESHOLDS:
        if index >= threshold:
            return level, label
    return 1, "Follow"


def days_since(iso):
    if not iso:
        return 9999
    try:
        dt = datetime.strptime(iso[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    except ValueError:
        return 9999
    now = datetime.now(timezone.utc)
    return max(0, (now - dt).days)


def recency_multiplier(days):
    for window, mult in RECENCY_WINDOWS:
        if days <= window:
            return mult
    return 0.7


def analyze():
    print("Fetching repos for %s ..." % USER)
    repos = fetch_repos()
    repos = [r for r in repos if not r.get("fork")]
    max_repos = int(os.environ.get("MAX_REPOS", "0") or "0")
    if max_repos > 0:
        repos = repos[:max_repos]
    print("  %d repos to analyze (forks skipped)" % len(repos))

    lang_cache = {}
    scores = {s: 0.0 for s in SKILLS}
    evidence = {s: [] for s in SKILLS}
    repo_detail = []

    for r in repos:
        name = r.get("name", "")
        desc = (r.get("description") or "") 
        topics = " ".join(r.get("topics") or [])
        langs, lang_matches = {}, {}

        lang_key = r.get("full_name", name)
        if lang_key not in lang_cache:
            lang_cache[lang_key] = api_get("/repos/%s/languages" % lang_key) or {}
        langs = lang_cache[lang_key]
        total = float(sum(langs.values())) or 1.0
        top_lang = max(langs, key=langs.get) if langs else None

        readme_text = ""
        if os.environ.get("SKIP_README") != "1":
            readme = api_get("/repos/%s/readme" % lang_key, accept_raw=True)
            if readme:
                readme_text = html.unescape(readme)

        text = (name + " " + desc + " " + topics).lower()
        readme_lower = readme_text.lower()

        pushed_days = days_since(r.get("pushed_at"))
        recency = recency_multiplier(pushed_days)
        size_kb = r.get("size") or 0
        size_factor = min(1.5, 0.5 + size_kb / 2000.0)

        row = {"name": name, "lang": top_lang, "pushed_days": pushed_days}
        for skill, cfg in SKILLS.items():
            kw = 0.0
            for k in cfg["keywords"]:
                if k in text:
                    kw += WEIGHT_NAME if k in name.lower() else 0.0
                    kw += WEIGHT_DESC if k in desc.lower() else 0.0
                    kw += WEIGHT_TOPIC if k in topics.lower() else 0.0
            if readme_lower:
                hits = sum(1 for k in cfg["keywords"] if k in readme_lower)
                kw += min(hits, README_MAX_HITS) * WEIGHT_README

            lang_score = 0.0
            for lang_name, bytes_count in langs.items():
                w = cfg["langs"].get(lang_name, 0.0)
                if w:
                    lang_score += w * (bytes_count / total)

            strength = kw * STRENGTH_KW + lang_score * STRENGTH_LANG
            contribution = strength * recency * size_factor
            scores[skill] += contribution
            if strength > 0:
                evidence[skill].append(name)
            row[skill] = round(strength, 2)
        repo_detail.append(row)

    n = float(len(repos)) or 1.0
    indexes = {s: sc / n for s, sc in scores.items()}
    ranks = {s: rank_for_score(indexes[s]) for s, sc in scores.items()}
    sfia = {s: sfia_for_index(indexes[s]) for s, sc in scores.items()}
    top_skill = max(indexes, key=lambda s: (indexes[s], scores[s]))

    def role_blurb(skill):
        return "%s — %s" % (SKILLS[skill]["role"], SKILLS[skill]["blurb"])

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "username": USER,
        "analyzed_repos": len(repos),
        "top_skill": top_skill,
        "overall_rank": ranks[top_skill],
        "scores": {k: round(v, 2) for k, v in sorted(scores.items(), key=lambda kv: kv[1], reverse=True)},
        "indexes": {k: round(v, 2) for k, v in sorted(indexes.items(), key=lambda kv: kv[1], reverse=True)},
        "ranks": ranks,
        "sfia": {k: list(v) for k, v in sfia.items()},
        "roles": {s: role_blurb(s) for s in SKILLS},
        "evidence": {k: v[:15] for k, v in evidence.items()},
        "repos": repo_detail,
    }
    with open(REPORT_PATH, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps({k: report[k] for k in ("top_skill", "overall_rank", "scores", "ranks", "sfia")}, indent=2))
    return report


def build_readme_section(report):
    rank_style = {"S": "S-Rank (Monarch)", "A": "A-Rank (Elite)",
                  "B": "B-Rank (Veteran)", "C": "C-Rank (Skilled)",
                  "D": "D-Rank (Apprentice)", "E": "E-Rank (Novice)"}
    sfia_meta = {1: "1 · Follow", 2: "2 · Assist", 3: "3 · Apply",
                 4: "4 · Enable", 5: "5 · Ensure", 6: "6 · Initiate",
                 7: "7 · Set strategy"}
    top = report["top_skill"]
    overall = report["overall_rank"]
    top_label = rank_style.get(overall, overall + "-Rank")
    top_sfia = report["sfia"].get(top, [None, ""])
    top_sfia_label = "SFIA L%s (%s)" % (top_sfia[0], top_sfia[1]) if top_sfia[0] else ""

    rows = ["| Skill | Rank | Index | SFIA 8 Level |",
            "|---|---|---|---|"]
    for skill, sc in report["scores"].items():
        rk = report["ranks"][skill]
        idx = report["indexes"].get(skill)
        sfia = report["sfia"].get(skill)
        sfia_txt = "L%s · %s" % (sfia[0], sfia[1]) if sfia else "-"
        rows.append("| %s | %s | %s | %s |" % (skill, rank_style.get(rk, rk + "-Rank"), idx, sfia_txt))

    evidence_lines = []
    top_ev = report["evidence"].get(top, [])
    for r in top_ev[:8]:
        evidence_lines.append("- %s" % r)
    if not evidence_lines:
        evidence_lines.append("_No direct matches yet._")

    role = report["roles"].get(top, "")

    return "\n".join([
        "<div align=\"center\">",
        "",
        "### ⚔️ **HUNTER RANK: %s** ⚔️" % top_label,
        "",
        "**Primary Discipline: %s**" % top,
        "",
        "> %s" % role,
        "",
        "> **%s**" % top_sfia_label,
        "",
        "<sub>Updated %s | %d public repos analyzed by the Shadow Army's automated scout</sub>" % (
            report["generated_at"][:10], report["analyzed_repos"]),
        "",
        "</div>",
        "",
        "**SKILL INVENTORY RANKS**",
        "",
        "\n".join(rows),
        "",
        "**EVIDENCE — REPOS DRIVING THE %s RANK**" % top.upper(),
        "",
        "\n".join(evidence_lines),
        "",
        "_Ranks follow the Solo Leveling theme; SFIA 8 columns map the repo-derived index onto the ",
        "industry-standard Skills Framework for the Information Age (levels 1-7). This is a ",
        "portfolio-based estimation, not a formal SFIA assessment._",
    ])


def update_readme(report):
    if not os.path.exists(README_PATH):
        return
    section = build_readme_section(report)
    with open(README_PATH, "r", encoding="utf-8") as fh:
        content = fh.read()
    if START_MARKER in content and END_MARKER in content:
        new_content = re.sub(
            re.escape(START_MARKER) + ".*?" + re.escape(END_MARKER),
            START_MARKER + "\n" + section + "\n" + END_MARKER,
            content,
            flags=re.DOTALL,
        )
    else:
        new_content = content + "\n\n" + START_MARKER + "\n" + section + "\n" + END_MARKER + "\n"
    with open(README_PATH, "w", encoding="utf-8") as fh:
        fh.write(new_content)
    print("README updated.")


def main():
    report = analyze()
    update_readme(report)
    print("Report written to %s" % REPORT_PATH)


if __name__ == "__main__":
    main()