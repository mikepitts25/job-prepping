# Interview prep: Senior Software Engineer, EADGE-T Tech Refresh (Expat UAE)

You have not written much code lately. That is a solvable problem, and it is not
the thing that decides this interview. What decides it is whether you can talk
credibly about shipping software in a large, regulated, integration-heavy
program, and then not fumble a straightforward coding exercise.

This site is built for that. Twenty-two lessons, roughly 110 worked code examples, a
runnable practice repo, a 146-question mock bank and 16 worked scenario answers.

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

This is the **Senior Software Engineer, EADGE-T Tech Refresh, EXPAT UAE**
requisition specifically. Lockheed has several EADGE-T software reqs open and
their qualification lists differ, so check yours against this table.

| Basic qualifications | Desired skills |
| --- | --- |
| 3+ years relevant experience (an advanced degree substitutes for 2) | Agile methodologies and tools |
| Java and/or Python | UI/UX test frameworks: Cypress, Selenium, Playwright, Jest |
| **Frontend framework development: Angular, JavaScript, CSS, HTML** | Full-stack engineering experience |
| Familiarity with **Docker, REST APIs, or SOAP** | GitLab CI/CD, Helm, Kubernetes |
| Full SDLC experience | gRPC |
| Ability to obtain a US DoD Secret clearance | Python, Flask |
| | UI/UX design tools: MockFlow, UXPin, Axure |
| | RHEL and Windows |
| | Services, microservices, software factories, cloud-native architectures |

Three things in that list are worth reading twice, because they are easy to
miss and they change how you prepare.

**Angular is a basic qualification, not a nice-to-have.** This is a full-stack
role, not a backend one. [Lesson 7](lessons/frontend.html) covers it from
nothing.

**The bar is three years, not five,** and an advanced degree substitutes for
two of them. This req is more accessible than it first looks.

**The clearance requirement is the ability to obtain one**, not holding one
already. If you are not currently cleared, that is not a disqualifier here.

Every one of those rows has a lesson below.

## How to use this

If your interview is more than two weeks out, work the lessons in order and do
the practice repo alongside. If it is sooner, go straight to
[the interview map](lessons/interview-map.html), pick the compressed plan,
and do [the four-hour sprint](lessons/python-sprint.html) first, then
lessons 7, 14 and 20.

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
