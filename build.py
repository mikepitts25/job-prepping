#!/usr/bin/env python3
"""Build the static prep site from Markdown sources in _src/ into HTML.

Usage: python3 build.py
Requires: pip install markdown
"""
import os
import re
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "_src")
OUT = os.path.join(ROOT, "lessons")

SITE_TITLE = "Lockheed Martin EADGE-T Interview Prep"

# (slug, nav title, short blurb) in reading order.
PAGES = [
    ("program-brief", "1. Program &amp; Role Brief", "What EADGE-T is, what the team does, and what they are actually hiring for."),
    ("track-data", "2. Track Data, Standards &amp; Fusion", "Plots, tracks, Link 16, ASTERIX, data reduction, and the metrics that test a fusion system."),
    ("interview-map", "3. Interview Map &amp; 14-Day Plan", "The likely loop, what each round tests, and a day-by-day study schedule."),
    ("python", "4. Python Refresher", "The 20% of Python that shows up in 80% of interviews, plus idioms and testing."),
    ("java", "5. Java Refresher", "Collections, streams, concurrency, and modern Java features with examples."),
    ("dsa", "6. Data Structures &amp; Algorithms", "Complexity, the core structures, patterns, and 24 practice problems."),
    ("ood", "7. OO Design &amp; SOLID", "Design principles, patterns you will be asked about, and a live design exercise."),
    ("linux", "8. Linux / RHEL", "Shell, systemd, networking, permissions, and production troubleshooting drills."),
    ("git-agile", "9. Git, GitLab &amp; Agile", "Branching, baseline merges, conflict resolution, Scrum and Kanban mechanics."),
    ("testing-ci", "10. Testing &amp; CI/CD", "Unit tests, mocking, coverage, GitLab CI and Jenkins pipelines end to end."),
    ("containers", "11. Docker, Kubernetes &amp; Helm", "Images, orchestration, Helm charts, and the questions asked about each."),
    ("architecture", "12. Architecture &amp; Software Factory", "SOA, microservices, messaging, cloud-native, and the DevSecOps factory model."),
    ("cyber", "13. Cybersecurity &amp; Sustainment", "STIGs, RMF, CVE remediation, and COTS/FOSS upgrade strategy."),
    ("adoc-bridge", "14. Your ADOC Bridge", "Turning the Qatar ADOC product owner role into credible answers for a hands-on job."),
    ("behavioral", "15. Behavioral &amp; Expat Questions", "STAR stories, LM interview style, and the UAE assignment conversation."),
    ("scenarios", "16. Scenario Answers", "Sixteen worked \"what would you do if\" answers, with the follow-ups they will ask."),
    ("mock-interview", "17. Mock Interview Bank", "132 questions with model answers, graded by round."),
    ("cheatsheets", "18. Cheat Sheets", "One-page recalls for the morning of the interview."),
]

INDEX_BY_SLUG = {slug: i for i, (slug, _, _) in enumerate(PAGES)}

MD_EXTENSIONS = ["fenced_code", "tables", "toc", "attr_list", "sane_lists", "codehilite"]
MD_CONFIG = {"codehilite": {"noclasses": False, "guess_lang": False},
             "toc": {"permalink": False}}


def nav_html(active_slug, prefix):
    items = []
    for slug, title, _ in PAGES:
        cls = ' class="active"' if slug == active_slug else ""
        items.append(f'<li{cls}><a href="{prefix}lessons/{slug}.html">{title}</a></li>')
    return (
        f'<a class="home" href="{prefix}index.html">&#8962; Start here</a>'
        f'<ul>{"".join(items)}</ul>'
        f'<a class="home" href="{prefix}practice/README.html">&#9881; Practice repo</a>'
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &middot; {site}</title>
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <button id="navtoggle" aria-label="Toggle navigation">&#9776;</button>
  <span class="brand"><a href="{prefix}index.html">EADGE-T Interview Prep</a></span>
  <span class="spacer"></span>
  <button id="themetoggle" aria-label="Toggle theme">&#9681;</button>
</header>
<div class="layout">
<nav id="sidebar">{nav}</nav>
<main id="main">
{body}
{pager}
</main>
</div>
<script src="{prefix}assets/site.js"></script>
</body>
</html>
"""


def pager_html(slug, prefix):
    if slug not in INDEX_BY_SLUG:
        return ""
    i = INDEX_BY_SLUG[slug]
    parts = ['<nav class="pager">']
    if i > 0:
        p = PAGES[i - 1]
        parts.append(f'<a class="prev" href="{prefix}lessons/{p[0]}.html">&larr; {p[1]}</a>')
    else:
        parts.append("<span></span>")
    if i < len(PAGES) - 1:
        n = PAGES[i + 1]
        parts.append(f'<a class="next" href="{prefix}lessons/{n[0]}.html">{n[1]} &rarr;</a>')
    parts.append("</nav>")
    return "".join(parts)


def render(md_text, slug, prefix, title):
    md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
    body = md.convert(md_text)
    return TEMPLATE.format(
        title=title, site=SITE_TITLE, prefix=prefix,
        nav=nav_html(slug, prefix), body=body,
        pager=pager_html(slug, prefix),
    )


def first_heading(md_text, fallback):
    m = re.search(r"^#\s+(.+)$", md_text, re.M)
    return m.group(1).strip() if m else fallback


def build():
    os.makedirs(OUT, exist_ok=True)
    written = []

    for slug, nav_title, _ in PAGES:
        path = os.path.join(SRC, slug + ".md")
        if not os.path.exists(path):
            print(f"  skip (missing): {slug}.md")
            continue
        text = open(path, encoding="utf-8").read()
        html = render(text, slug, "../", first_heading(text, nav_title))
        dest = os.path.join(OUT, slug + ".html")
        open(dest, "w", encoding="utf-8").write(html)
        written.append(dest)

    home_md = open(os.path.join(SRC, "index.md"), encoding="utf-8").read()
    cards = "\n".join(
        f'<a class="card" href="lessons/{s}.html"><h3>{t}</h3><p>{b}</p></a>'
        for s, t, b in PAGES
    )
    home_md = home_md.replace("<!--CARDS-->", f'<div class="cards">{cards}</div>')
    html = render(home_md, "index", "", "Start here")
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    written.append("index.html")

    practice_md_path = os.path.join(ROOT, "practice", "README.md")
    if os.path.exists(practice_md_path):
        text = open(practice_md_path, encoding="utf-8").read()
        html = render(text, "practice", "../", "Practice repo")
        open(os.path.join(ROOT, "practice", "README.html"), "w", encoding="utf-8").write(html)
        written.append("practice/README.html")

    print(f"Built {len(written)} pages.")


if __name__ == "__main__":
    build()
