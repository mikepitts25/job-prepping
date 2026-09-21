# Prep Library

A GitHub Pages study site holding two things: a **PMP and CAM/EVMS
certification track**, and the original **EADGE-T interview prep** body of work,
kept intact.

## PMP and CAM tracks

Seven PMP lessons built against the **Exam Content Outline that took effect on
9 July 2026** — the version that reweighted the domains to People 33%, Process
41%, Business Environment 26% and consolidated 35 tasks down to 26. Plus two
Control Account Manager lessons covering EIA-748-E, the WBS-to-control-account
chain, every earned value formula, and the questions asked in a CAM interview.

The material assumes the reader holds a CISSP and deliberately skips ground the CISSP
already covers — governance, compliance, risk, and change control are treated as
vocabulary translation rather than new content.

| Lesson | Topic |
| --- | --- |
| P1 | PMP: the 2026 exam, eligibility, cost, application, audit |
| P2 | The Exam Content Outline decoded, task by task |
| P3 | The PMI mindset: the seven rules and the four-step answer routine |
| P4 | Predictive mechanics: WBS, critical path, EVM, quality, risk, procurement |
| P5 | Agile and hybrid: Scrum, Kanban, XP, servant leadership, tailoring |
| P6 | Forty drill questions with the reasoning, not just the key |
| P7 | Ten-week plan and the free official material, ranked |
| C1 | Control Account Manager: EVMS, EIA-748-E, the budget stack, EV methods |
| C2 | CAM interview and IBR drill, with worked variance analysis |

All practice questions are original, written against published outlines. No
retired or genuine exam content is reproduced anywhere in this repo.

## EADGE-T interview prep

The original site, for the **Senior Software Engineer &ndash; EADGE-T Tech
Refresh &ndash; EXPAT UAE** role at Lockheed Martin, plus a runnable practice
repo. That role is closed; the material stands on its own as a software
engineering refresher.

Twenty-seven lessons covering every skill named in the job posting, roughly one
hundred and fifty worked code examples, a 146-question mock interview bank,
sixteen worked scenario answers, and 138 passing tests across Python, Java and
TypeScript practice modules.

**Lessons 4 to 9 are timed four-hour sprints**, one per basic qualification.
Each builds one real, working thing rather than covering a topic: a tested
command-line tool, 46 unit tests, a filterable page rebuilt in Angular, a
validated REST API with a resilient client, a hardened container image, and a
CI/CD pipeline with real Git drills.

## Read it

Published at **https://mikepitts25.github.io/job-prepping/**.

Deployment runs through `.github/workflows/pages.yml`, so the repository's
**Settings → Pages → Source must be set to "GitHub Actions"**, not "Deploy from
a branch".

Every push to `main` rebuilds the site from `_src/` and republishes. The build
job fails rather than publishing if either check does not hold:

- the committed HTML does not match a fresh build of the Markdown sources, which
  means someone edited `_src/` and forgot to run `build.py`
- any internal link does not resolve

The workflow sets `cancel-in-progress: true` on the `pages` concurrency group so
a newer push supersedes an older deployment. GitHub's stock template leaves that
false, which lets one stalled deployment block every later run.

To read it without publishing:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## EADGE-T lesson contents

| Lesson | Topic |
| --- | --- |
| 1 | Program and role brief: what EADGE-T is and what the job actually does |
| 2 | Track data, standards and fusion: plots, tracks, Link 16, ASTERIX, data reduction |
| 3 | Interview map and a 14-day study plan |
| 4 | **Sprint:** Python in four hours, ending in a tested command-line tool |
| 5 | **Sprint:** testing in four hours, a simple program and 46 unit tests |
| 6 | **Sprint:** frontend in four hours, HTML to tested TypeScript to Angular |
| 7 | **Sprint:** APIs in four hours, a validated REST API and a resilient client |
| 8 | **Sprint:** Docker in four hours, ending in a hardened multi-stage image |
| 9 | **Sprint:** SDLC in four hours, Git drills, review, and a CI/CD pipeline |
| 10 | Python foundations: the language from zero, and why each piece exists |
| 11 | Python in practice: standard library, generators, decorators, testing |
| 12 | Frontend reference: Angular, TypeScript, HTML and CSS |
| 13 | APIs reference: REST, SOAP, gRPC and a working Flask service |
| 14 | Java refresher |
| 15 | Data structures, algorithms, and 24 practice problems |
| 16 | Object-oriented design, SOLID, and a live design exercise |
| 17 | Linux / RHEL and production troubleshooting |
| 18 | Git, GitLab, baseline merges, Scrum and Kanban |
| 19 | Testing and CI/CD |
| 20 | Docker, Kubernetes and Helm |
| 21 | Architecture and the Software Factory |
| 22 | Cybersecurity, STIGs, and COTS/FOSS upgrades |
| 23 | Turning the Qatar ADOC product owner role into credible answers |
| 24 | Behavioral questions and the expat conversation |
| 25 | Sixteen worked scenario answers, with the follow-ups |
| 26 | Mock interview bank, 146 questions |
| 27 | Cheat sheets for the morning of |

## Practice

```bash
cd practice/python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q                          # 84 tests, all passing
PREP_TARGET=exercises pytest -q    # grade your own attempts

cd ../java
mvn -B test                        # 22 tests, all passing

cd ../frontend
npm install
npm test                           # 32 tests, all passing
npm run typecheck                  # strict TypeScript, no errors
```

See [practice/README.md](practice/README.md) for the suggested order.

## Editing

Lesson content lives in `_src/*.md`. After editing, rebuild the HTML:

```bash
pip install -r requirements-build.txt
python3 build.py
```

The build dependencies are pinned because python-markdown's `codehilite`
extension silently emits unhighlighted markup when Pygments is missing, so an
unpinned environment produces a different site.

`build.py` renders each Markdown source into `lessons/`, wraps it in the shared
layout with navigation, and regenerates `index.html`. Add a lesson by dropping a
new `_src/<slug>.md` file in and adding it to the `PAGES` list in `build.py`.

Each `PAGES` entry is `(slug, nav title, blurb, section)`, where `section` is a
key from `SECTIONS`. The section controls which sidebar group and which home-page
card group the lesson appears in; `PAGES` order controls the previous/next
pager.

## Sources

Certification material is built against the current official outlines, linked
from each lesson:

- [PMP Examination Content Outline, July 2026 (PMI)](https://www.pmi.org/-/media/pmi/documents/public/pdf/certifications/new-pmp-examination-content-outline-2026.pdf)
- [The new PMP exam (PMI)](https://www.pmi.org/certifications/project-management-pmp/new-exam)
- [The Scrum Guide](https://scrumguides.org/)
- [NDIA IPMD guides, including the EIA-748 Intent Guide](https://www.ndia.org/divisions/ipmd/division-guides-and-resources)
- [DAU EVM 101](https://icatalog.dau.edu/mobile/CourseDetails.aspx?id=1907) and
  [DOE EVMS training](https://www.energy.gov/projectmanagement/evms-training)
- [DFARS Subpart 234.2, EVMS](https://www.acquisition.gov/dfars/subpart-234.2-earned-value-management-system)

Fees, EVMS dollar thresholds, and standard revision levels all move. Each lesson
says so where it quotes one; check the primary source before relying on a number.

Role and program details come from the public job posting and program coverage:

- [Senior Software Engineer &ndash; EADGE-T Tech Refresh &ndash; EXPAT UAE (ClearanceJobs)](https://www.clearancejobs.com/jobs/9040193/senior-software-engineer-eadge-t-tech-refresh-expat-uae)
- [Software Engineer &ndash; EADGE-T Tech Refresh (Lockheed Martin Jobs)](https://www.lockheedmartinjobs.com/job/colorado-springs/software-engineer-eadge-t-tech-refresh/694/97890638880)
- [Lockheed Martin preferred bidder for UAE's air-defence system (The National)](https://www.thenationalnews.com/business/lockheed-martin-preferred-bidder-for-uae-s-air-defence-system-1.289304)

Track data standards in lesson 2 are drawn from EUROCONTROL's published ASTERIX
specifications and open documentation of the tactical data link standards; each
lesson lists its own sources.
