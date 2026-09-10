# EADGE-T interview prep

A GitHub Pages study site for the **Senior Software Engineer &ndash; EADGE-T Tech
Refresh &ndash; EXPAT UAE** role at Lockheed Martin, plus a runnable practice
repo.

Nineteen lessons covering every skill named in the job posting, roughly eighty
worked code examples, a 132-question mock interview bank, sixteen worked
scenario answers, and 106 passing tests across Python and Java practice
modules.

The two Python lessons assume no prior knowledge and build the language from
first principles, explaining why each construct exists rather than only how to
type it.

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

## Contents

| Lesson | Topic |
| --- | --- |
| 1 | Program and role brief: what EADGE-T is and what the job actually does |
| 2 | Track data, standards and fusion: plots, tracks, Link 16, ASTERIX, data reduction |
| 3 | Interview map and a 14-day study plan |
| 4 | Python foundations: the language from zero, and why each piece exists |
| 5 | Python in practice: standard library, generators, decorators, testing |
| 6 | Java refresher |
| 7 | Data structures, algorithms, and 24 practice problems |
| 8 | Object-oriented design, SOLID, and a live design exercise |
| 9 | Linux / RHEL and production troubleshooting |
| 10 | Git, GitLab, baseline merges, Scrum and Kanban |
| 11 | Testing and CI/CD |
| 12 | Docker, Kubernetes and Helm |
| 13 | Architecture and the Software Factory |
| 14 | Cybersecurity, STIGs, and COTS/FOSS upgrades |
| 15 | Turning the Qatar ADOC product owner role into credible answers |
| 16 | Behavioral questions and the expat conversation |
| 17 | Sixteen worked scenario answers, with the follow-ups |
| 18 | Mock interview bank, 132 questions |
| 19 | Cheat sheets for the morning of |

## Practice

```bash
cd practice/python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q                          # 84 tests, all passing
PREP_TARGET=exercises pytest -q    # grade your own attempts

cd ../java
mvn -B test                        # 22 tests, all passing
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

## Sources

Role and program details come from the public job posting and program coverage:

- [Senior Software Engineer &ndash; EADGE-T Tech Refresh &ndash; EXPAT UAE (ClearanceJobs)](https://www.clearancejobs.com/jobs/9040193/senior-software-engineer-eadge-t-tech-refresh-expat-uae)
- [Software Engineer &ndash; EADGE-T Tech Refresh (Lockheed Martin Jobs)](https://www.lockheedmartinjobs.com/job/colorado-springs/software-engineer-eadge-t-tech-refresh/694/97890638880)
- [Lockheed Martin preferred bidder for UAE's air-defence system (The National)](https://www.thenationalnews.com/business/lockheed-martin-preferred-bidder-for-uae-s-air-defence-system-1.289304)

Track data standards in lesson 2 are drawn from EUROCONTROL's published ASTERIX
specifications and open documentation of the tactical data link standards; each
lesson lists its own sources.
