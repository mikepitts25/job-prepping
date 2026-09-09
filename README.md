# EADGE-T interview prep

A GitHub Pages study site for the **Senior Software Engineer &ndash; EADGE-T Tech
Refresh &ndash; EXPAT UAE** role at Lockheed Martin, plus a runnable practice
repo.

Fifteen lessons covering every skill named in the job posting, roughly sixty
worked code examples, a 120-question mock interview bank with model answers, and
76 passing tests across Python and Java practice modules.

## Read it

Open `index.html` locally, or publish it:

**Settings → Pages → Source: "Deploy from a branch" → Branch:
`claude/lockheed-martin-interview-prep-0asm6i`, folder `/ (root)` → Save.**

The site appears at `https://<your-username>.github.io/job-prepping/` after a
minute or two. Merge the branch to `main` first if you would rather serve from
there.

To read it without publishing:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Contents

| Lesson | Topic |
| --- | --- |
| 1 | Program and role brief: what EADGE-T is and what the job actually does |
| 2 | Interview map and a 14-day study plan |
| 3 | Python refresher |
| 4 | Java refresher |
| 5 | Data structures, algorithms, and 24 practice problems |
| 6 | Object-oriented design, SOLID, and a live design exercise |
| 7 | Linux / RHEL and production troubleshooting |
| 8 | Git, GitLab, baseline merges, Scrum and Kanban |
| 9 | Testing and CI/CD |
| 10 | Docker, Kubernetes and Helm |
| 11 | Architecture and the Software Factory |
| 12 | Cybersecurity, STIGs, and COTS/FOSS upgrades |
| 13 | Behavioral questions and the expat conversation |
| 14 | Mock interview bank, 120 questions |
| 15 | Cheat sheets for the morning of |

## Practice

```bash
cd practice/python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q                          # 54 tests, all passing
PREP_TARGET=exercises pytest -q    # grade your own attempts

cd ../java
mvn -B test                        # 22 tests, all passing
```

See [practice/README.md](practice/README.md) for the suggested order.

## Editing

Lesson content lives in `_src/*.md`. After editing, rebuild the HTML:

```bash
pip install markdown
python3 build.py
```

`build.py` renders each Markdown source into `lessons/`, wraps it in the shared
layout with navigation, and regenerates `index.html`. Add a lesson by dropping a
new `_src/<slug>.md` file in and adding it to the `PAGES` list in `build.py`.

## Sources

Role and program details come from the public job posting and program coverage:

- [Senior Software Engineer &ndash; EADGE-T Tech Refresh &ndash; EXPAT UAE (ClearanceJobs)](https://www.clearancejobs.com/jobs/9040193/senior-software-engineer-eadge-t-tech-refresh-expat-uae)
- [Software Engineer &ndash; EADGE-T Tech Refresh (Lockheed Martin Jobs)](https://www.lockheedmartinjobs.com/job/colorado-springs/software-engineer-eadge-t-tech-refresh/694/97890638880)
- [Lockheed Martin preferred bidder for UAE's air-defence system (The National)](https://www.thenationalnews.com/business/lockheed-martin-preferred-bidder-for-uae-s-air-defence-system-1.289304)
