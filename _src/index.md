# Interview prep: Senior Software Engineer, EADGE-T Tech Refresh (Expat UAE)

You have not written much code lately. That is a solvable problem, and it is not
the thing that decides this interview. What decides it is whether you can talk
credibly about shipping software in a large, regulated, integration-heavy
program, and then not fumble a straightforward coding exercise.

This site is built for that. Fifteen lessons, roughly 60 worked code examples, a
runnable practice repo, and a 120-question mock bank with model answers.

## The short version of what you are walking into

EADGE-T is Lockheed Martin's integrated air and missile defense and air battle
management system for the United Arab Emirates. It ties existing sensors and
weapons, including THAAD and Patriot PAC-3, into one air picture and one battle
management layer. The **Tech Refresh** is the current effort: hardware
modernization plus foundational cybersecurity upgrades on a system that has been
fielded for years.

Your job on that effort, per the posting, is to modernize and maintain the
software: pull in COTS and FOSS updates, migrate legacy capability onto Lockheed
Martin's Software Factory CI/CD pipelines, write unit tests and automated test
capability, and do the unglamorous integration work of baseline merges, defect
resolution, peer reviews, and troubleshooting. The team is geographically
dispersed and runs Agile Scrum. The assignment is a two to three year expat
posting in the UAE.

That description tells you exactly what to prepare. This is not a
build-a-distributed-system-from-scratch role. It is a **sustainment and
modernization** role on a mission-critical baseline, and the interview will
weight accordingly.

## What the posting asks for

| Basic qualifications | Desired skills |
| --- | --- |
| Python and Java proficiency | Services, microservices, SOA, cloud-native architecture |
| RHEL and Windows | Docker, Kubernetes, Helm |
| Agile (Scrum / Kanban) | CI/CD tooling: Git, GitLab, Jenkins |
| Full SDLC experience | Software Factory concepts |
| Git, GitLab, Jira, Confluence | |
| Data structures, algorithms, OO design | |
| Automated testing, unit tests, CI/CD | |
| BS + 5 years, or equivalent | |

Every one of those rows has a lesson below.

## How to use this

If your interview is more than two weeks out, work the lessons in order and do
the practice repo alongside. If it is sooner, go straight to
[the interview map](lessons/01-interview-map.html), pick the compressed plan,
and prioritize lessons 3, 4, 9 and 13.

Type the code. Do not read it. The gap between "I recognize this" and "I can
produce this while someone watches" is the entire problem you are solving in the
next two weeks.

<!--CARDS-->

## A word about the nerves

Being rusty is a real handicap, but it is a narrow one. It affects the 45
minutes of live coding, and nothing else. Rust comes off fast: a dozen hours of
deliberate typing practice will get you back to fluent on the syntax and the
standard library, which is all that a screening exercise actually tests.

What does not come off fast is judgment, and you already have that. Lead with
it.

## Sources

Program and role details drawn from the public posting and program coverage:

- [Senior Software Engineer &ndash; EADGE-T Tech Refresh &ndash; EXPAT UAE (ClearanceJobs)](https://www.clearancejobs.com/jobs/9040193/senior-software-engineer-eadge-t-tech-refresh-expat-uae)
- [Software Engineer &ndash; EADGE-T Tech Refresh (Lockheed Martin Jobs)](https://www.lockheedmartinjobs.com/job/colorado-springs/software-engineer-eadge-t-tech-refresh/694/97890638880)
- [Lockheed Martin preferred bidder for UAE's air-defence system (The National)](https://www.thenationalnews.com/business/lockheed-martin-preferred-bidder-for-uae-s-air-defence-system-1.289304)
- [Lockheed gains preferred bidder status in UAE's Extended Air Defence Ground programme (Defensemirror)](https://defensemirror.com/news/8061/Lockheed_Gains_Preferred_Bidder_Status_In_UAE_s_Extended_Air_Defence_Ground_Program)
