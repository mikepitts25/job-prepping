# P2. The 2026 Exam Content Outline, Decoded

The Exam Content Outline is the syllabus. Everything on the exam maps to one of
26 tasks across three domains, and nothing that is not on this list is testable.
It is about twenty pages and free. Read the real thing once; use this page as the
working translation.

Structure, in PMI's terms:

- **Domain** — a broad area of practice. There are three.
- **Task** — a responsibility within a domain. There are 26.
- **Enabler** — illustrative examples under each task. *Not* an exhaustive list,
  and not something to memorise. They show the flavour of the task.

| Domain | Weight | Tasks | Roughly, of 170 scored questions |
| --- | --- | --- | --- |
| People | 33% | 8 | ~56 |
| Process | 41% | 10 | ~70 |
| Business Environment | 26% | 8 | ~44 |

## Domain I — People (33%)

Leading and building the team. This is the domain where the "right" answer is
almost always the one involving talking to a human before doing anything else.

| Task | What it means | A question looks like |
| --- | --- | --- |
| Build a shared vision and team culture | Charter the team, set ground rules, establish shared purpose | "The team has no agreed definition of done. What first?" |
| Develop and empower the team | Assess skills, train, delegate, give autonomy | "A capable developer keeps escalating trivial decisions to you." |
| Lead the team | Set direction, model behaviour, choose a leadership style to fit the situation | "Team is new and unsure. Which style?" |
| Manage conflict | Surface it, interpret the source, resolve at the lowest level | "Two leads disagree publicly in a review." |
| Support and mentor stakeholders | Coach, build capability outside the team too | "A new product owner does not know how to write acceptance criteria." |
| Engage stakeholders | Identify, analyse, plan engagement, keep them engaged | "A stakeholder went quiet three sprints ago." |
| Communicate | Tailor channel, frequency, and detail to the audience | "Sponsor says they are surprised by a status." |
| Manage knowledge transfer | Capture lessons, hand over, avoid single points of knowledge | "The only person who understands the integration is leaving." |

**Where your CISSP does not help:** almost nowhere here. This is the domain to
spend real hours on. Security exams reward decisive control selection; this
domain rewards consultative, low-coercion, talk-first behaviour. That is the
habit gap.

## Domain II — Process (41%)

The technical work of delivering. Biggest domain, most formulas, most of the
graphic-based questions.

| Task | What it means | A question looks like |
| --- | --- | --- |
| Plan and manage the project | Integrate the subsidiary plans; select the right development approach | "Requirements are volatile and the customer is available. Which approach?" |
| Plan and manage scope | Collect requirements, define scope, WBS, control scope | "A stakeholder asks for one small extra feature." |
| Deliver value | Increments, MVP, benefits realisation, value over output | "How do you show value before final delivery?" |
| Plan and manage resources | Physical and team resources, acquisition, allocation | "Two projects need the same test rig." |
| Plan and manage procurement | Make-or-buy, contract type, vendor management | "Scope is poorly defined. Which contract type?" |
| Plan and manage budget | Estimate, baseline, control cost, earned value | "CPI is 0.85 at 40% complete. What is the EAC?" |
| Plan and manage quality | Standards, prevention over inspection, cost of quality | "Defects keep escaping into UAT." |
| Plan and manage schedule | Activities, dependencies, critical path, compression | "You need to shorten the schedule without changing scope." |
| Assess and report status | Baselines, variance, forecasts, reporting cadence | Read this burndown and say what is happening. |
| Close the project or phase | Formal acceptance, records, lessons, release of resources | "The customer is using the product but has not signed off." |

**Where your CISSP helps a little:** the procurement and quality tasks touch
third-party risk and assurance ideas you already have. The estimating, critical
path, and earned value mechanics are genuinely new, and they are the only part of
PMP that is arithmetic. [P4](pmp-predictive.html) covers all of it.

## Domain III — Business Environment (26%)

Connecting the project to the organisation and the world outside it. Grew from 8%
to 26% in the 2026 outline, mostly by absorbing tasks that used to live in
Process.

| Task | What it means | Your CISSP equivalent |
| --- | --- | --- |
| Define and establish project governance | Decision rights, escalation paths, steering structure, PMO relationship | Security governance, RACI, committee structures — near-identical |
| Plan and manage project compliance | Regulatory, contractual, organisational, and now **sustainability** compliance | Compliance domain, control mapping, audit evidence |
| Manage and control changes | Change requests, impact analysis, CCB, baseline integrity | Change management and configuration control |
| Remove impediments and manage issues | Unblock the team; issue log; escalate when you must | Incident and problem management, by another name |
| Plan and manage risk | Identify, analyse (qualitative and quantitative), respond, monitor | Risk management — the closest single mapping on the whole exam |
| Drive continuous improvement | Retrospectives, process tailoring, maturity | Continuous monitoring and improvement |
| Support organisational change | Readiness, adoption, resistance, benefits after handover | Security awareness and culture change |
| Monitor and evaluate external changes | Market, regulation, technology, geopolitics — and respond | Threat landscape monitoring |

**Read that right-hand column as a study plan.** You are not learning this domain
from zero; you are relearning vocabulary for concepts you already hold. Two
genuine deltas to watch:

1. **Risk response vocabulary differs.** PMI uses avoid / transfer / mitigate /
   accept / *escalate* for threats, and exploit / share / enhance / accept /
   escalate for **opportunities**. CISSP barely treats upside risk. PMP tests it
   constantly, and "escalate" as a fifth response is a 2017-era addition people
   still miss.
2. **Sustainability is examinable now.** Environmental and social impact sit
   inside compliance and risk. If a question offers an option that considers
   environmental or community impact and the others do not, that option is
   usually live rather than a distractor — which is the opposite of how you would
   read it on a security exam.

## What "enablers" mean for your study

Do not memorise the enabler bullets. They are examples. The exam tests whether
you would *do the task*, not whether you can recite what sits under it. If you
find yourself making flashcards of enablers, you have misread the document.

The one thing worth memorising from the ECO is the **task list itself**, because
it tells you what the exam thinks a project manager's job consists of. When you
are stuck between two answers, asking "which of these is a task on the ECO" is a
surprisingly effective tiebreaker.

## Sources

- [PMP Examination Content Outline, July 2026 (PMI, PDF)](https://www.pmi.org/-/media/pmi/documents/public/pdf/certifications/new-pmp-examination-content-outline-2026.pdf)
- [The new PMP exam (PMI)](https://www.pmi.org/certifications/project-management-pmp/new-exam)

The task titles above are paraphrased for brevity. PMI's own wording is in the
PDF, and where this page and the PDF differ, the PDF is right.
