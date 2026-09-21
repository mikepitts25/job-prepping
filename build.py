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

SITE_TITLE = "Prep Library"
BRAND = "Prep Library"

# Section headings, in the order they appear in the sidebar and on the home page.
SECTIONS = [
    ("pmp", "PMP certification"),
    ("cam", "CAM / EVMS certification"),
    ("eadge", "EADGE-T interview prep"),
]

# (slug, nav title, short blurb, section) in reading order.
PAGES = [
    ("pmp-overview", "P1. PMP: What You Are Signing Up For", "The 2026 exam, eligibility, cost, the application, and how it differs from CISSP.", "pmp"),
    ("pmp-eco", "P2. The 2026 Exam Content Outline", "Three domains, 26 tasks, decoded one line at a time with what each looks like on the exam.", "pmp"),
    ("pmp-mindset", "P3. The PMI Mindset", "The single highest-value lesson: how to pick the right answer when two look right.", "pmp"),
    ("pmp-predictive", "P4. Predictive Mechanics", "Charter to closure: scope, WBS, critical path, EVM, quality, risk, procurement, change control.", "pmp"),
    ("pmp-agile", "P5. Agile &amp; Hybrid", "Scrum, Kanban, XP, servant leadership, and how the exam phrases hybrid tailoring.", "pmp"),
    ("pmp-drills", "P6. Drill Set", "Forty exam-style questions with the reasoning spelled out, not just the answer key.", "pmp"),
    ("pmp-plan", "P7. Ten-Week Plan &amp; Free Resources", "A week-by-week schedule and the official free material, with links.", "pmp"),
    ("cam-evms", "C1. Control Account Manager: EVMS", "What a CAM owns, EIA-748-E, the WBS-to-control-account chain, and every formula.", "cam"),
    ("cam-drills", "C2. CAM Interview &amp; IBR Drill", "The questions a DCMA reviewer actually asks, plus worked variance analysis.", "cam"),
    ("program-brief", "1. Program &amp; Role Brief", "What EADGE-T is, what the team does, and what they are actually hiring for.", "eadge"),
    ("track-data", "2. Track Data, Standards &amp; Fusion", "Plots, tracks, Link 16, ASTERIX, data reduction, and the metrics that test a fusion system.", "eadge"),
    ("interview-map", "3. Interview Map &amp; 14-Day Plan", "The likely loop, what each round tests, and a day-by-day study schedule.", "eadge"),
    ("python-sprint", "4. Sprint: Python in Four Hours", "Timed intensive: from nothing to a tested command-line program.", "eadge"),
    ("testing-sprint", "5. Sprint: Testing in Four Hours", "A simple Python program and 46 unit tests, building the whole testing skill set.", "eadge"),
    ("frontend-sprint", "6. Sprint: Frontend in Four Hours", "HTML, CSS and TypeScript through to a tested page, then the same thing in Angular.", "eadge"),
    ("apis-sprint", "7. Sprint: APIs in Four Hours", "A validated REST API, its test suite, and a client that survives a flaky server.", "eadge"),
    ("docker-sprint", "8. Sprint: Docker in Four Hours", "From first container to a hardened multi-stage image you can defend in review.", "eadge"),
    ("sdlc-sprint", "9. Sprint: SDLC in Four Hours", "Real Git drills, code review, the lifecycle, and a working CI/CD pipeline.", "eadge"),
    ("python", "10. Python Foundations", "The language from zero: names and objects, containers, functions, classes, and why each exists.", "eadge"),
    ("python-practice", "11. Python in Practice", "Standard library, generators, decorators, logging, and testing with pytest from first principles.", "eadge"),
    ("frontend", "12. Frontend: Angular, TypeScript, HTML &amp; CSS", "The reference: the web from zero through to tested Angular components.", "eadge"),
    ("apis", "13. APIs: REST, SOAP, gRPC &amp; Flask", "Contracts between systems, versioning under interface control, and a working Flask API.", "eadge"),
    ("java", "14. Java Refresher", "Collections, streams, concurrency, and modern Java features with examples.", "eadge"),
    ("dsa", "15. Data Structures &amp; Algorithms", "Complexity, the core structures, patterns, and 24 practice problems.", "eadge"),
    ("ood", "16. OO Design &amp; SOLID", "Design principles, patterns you will be asked about, and a live design exercise.", "eadge"),
    ("linux", "17. Linux / RHEL", "Shell, systemd, networking, permissions, and production troubleshooting drills.", "eadge"),
    ("git-agile", "18. Git, GitLab &amp; Agile", "Branching, baseline merges, conflict resolution, Scrum and Kanban mechanics.", "eadge"),
    ("testing-ci", "19. Testing &amp; CI/CD", "The pyramid, mocking, coverage, GitLab CI and Jenkins pipelines end to end.", "eadge"),
    ("containers", "20. Docker, Kubernetes &amp; Helm", "Images, orchestration, Helm charts, and the questions asked about each.", "eadge"),
    ("architecture", "21. Architecture &amp; Software Factory", "SOA, microservices, messaging, cloud-native, and the DevSecOps factory model.", "eadge"),
    ("cyber", "22. Cybersecurity &amp; Sustainment", "STIGs, RMF, CVE remediation, and COTS/FOSS upgrade strategy.", "eadge"),
    ("adoc-bridge", "23. Your ADOC Bridge", "Turning the Qatar ADOC product owner role into credible answers for a hands-on job.", "eadge"),
    ("behavioral", "24. Behavioral &amp; Expat Questions", "STAR stories, LM interview style, and the UAE assignment conversation.", "eadge"),
    ("scenarios", "25. Scenario Answers", "Sixteen worked \"what would you do if\" answers, with the follow-ups they will ask.", "eadge"),
    ("mock-interview", "26. Mock Interview Bank", "146 questions with model answers, graded by round.", "eadge"),
    ("cheatsheets", "27. Cheat Sheets", "One-page recalls for the morning of the interview.", "eadge"),
]

INDEX_BY_SLUG = {page[0]: i for i, page in enumerate(PAGES)}

MD_EXTENSIONS = ["fenced_code", "tables", "toc", "attr_list", "sane_lists", "codehilite"]
MD_CONFIG = {"codehilite": {"noclasses": False, "guess_lang": False},
             "toc": {"permalink": False}}


def nav_html(active_slug, prefix):
    parts = [f'<a class="home" href="{prefix}index.html">&#8962; Start here</a>']
    for key, heading in SECTIONS:
        items = []
        for slug, title, _, section in PAGES:
            if section != key:
                continue
            cls = ' class="active"' if slug == active_slug else ""
            items.append(f'<li{cls}><a href="{prefix}lessons/{slug}.html">{title}</a></li>')
        if not items:
            continue
        parts.append(f'<p class="navsection">{heading}</p>')
        parts.append(f'<ul>{"".join(items)}</ul>')
    parts.append(f'<a class="home" href="{prefix}practice/README.html">&#9881; Practice repo</a>')
    return "".join(parts)


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
  <span class="brand"><a href="{prefix}index.html">{brand}</a></span>
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
        title=title, site=SITE_TITLE, brand=BRAND, prefix=prefix,
        nav=nav_html(slug, prefix), body=body,
        pager=pager_html(slug, prefix),
    )


def first_heading(md_text, fallback):
    m = re.search(r"^#\s+(.+)$", md_text, re.M)
    return m.group(1).strip() if m else fallback


def build():
    os.makedirs(OUT, exist_ok=True)
    written = []

    for slug, nav_title, _, _section in PAGES:
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
    blocks = []
    for key, heading in SECTIONS:
        cards = "\n".join(
            f'<a class="card" href="lessons/{slug}.html"><h3>{title}</h3><p>{blurb}</p></a>'
            for slug, title, blurb, section in PAGES if section == key
        )
        if cards:
            blocks.append(f'<h2 class="cardhead">{heading}</h2><div class="cards">{cards}</div>')
    home_md = home_md.replace("<!--CARDS-->", "\n".join(blocks))
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
