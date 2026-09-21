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

Eight tasks. PMI's own titles, with what each one is really asking.

| # | Task | What it means | A question looks like |
| --- | --- | --- | --- |
| 1 | **Develop a common vision** | Establish a shared vision with stakeholders, promote it, keep it current, and root-cause any misunderstanding of it | "Two groups describe the project's goal differently." |
| 2 | **Manage conflict** | Identify the source, analyse the context, apply an agreed resolution strategy, set and enforce ground rules | "Two leads disagree publicly in a review." |
| 3 | **Lead the project team** | Set expectations, empower, solve problems, represent the team's voice, choose a leadership style, clarify roles | "The team is new and unsure. Which style?" |
| 4 | **Engage stakeholders** | Identify, analyse, tailor communication, execute the engagement plan, build trust and influence | "A stakeholder went quiet three sprints ago." |
| 5 | **Align stakeholder expectations** | Categorise stakeholders, identify expectations, facilitate discussions to align them, act on mentoring opportunities | "Two stakeholders want incompatible outcomes." |
| 6 | **Manage stakeholder expectations** | Identify internal and external customer expectations, keep outcomes aligned to them, monitor satisfaction and respond | "The customer expected something different." |
| 7 | **Help ensure knowledge transfer** | Identify critical knowledge, gather it, foster an environment where it moves between people | "The only person who understands the integration is leaving." |
| 8 | **Plan and manage communication** | Define a communication strategy, promote transparency, establish a feedback loop, report to sponsor and stakeholder expectations | "The sponsor says they were surprised by a status." |

Note how much of this domain is **stakeholders** — three of the eight tasks
(4, 5, 6) are stakeholder work, split between engaging them, aligning their
expectations with each other, and managing them against delivery. If you are
unsure which task a People question belongs to, stakeholders is the way to bet.

**Where your CISSP does not help:** almost nowhere here. This is the domain to
spend real hours on. Security exams reward decisive control selection; this
domain rewards consultative, low-coercion, talk-first behaviour. That is the
habit gap, and [P6](pmp-people.html) is the lesson for it.

## Domain II — Process (41%)

Ten tasks. Biggest domain, most formulas, most of the graphic-based questions.

| # | Task | What it means | A question looks like |
| --- | --- | --- | --- |
| 1 | **Develop an integrated project management plan and plan delivery** | Assess complexity, **recommend the development approach** (predictive, agile, hybrid), estimate effort, integrate the subsidiary plans, keep them current | "Requirements are volatile and the customer is available. Which approach?" |
| 2 | **Develop and manage project scope** | Define scope, get stakeholder agreement, break it down | "A stakeholder asks for one small extra feature." |
| 3 | **Help ensure value-based delivery** | Identify value components, prioritise by value, deliver incrementally, verify a measurement system tracks benefits | "How do you show value before final delivery?" |
| 4 | **Plan and manage resources** | Define and plan resources against requirements, optimise need against availability | "Two projects need the same test rig." |
| 5 | **Plan and manage procurement** | Make-or-buy, contract type selection, negotiation strategy, vendor performance, supplier management | "Scope is poorly defined. Which contract type?" |
| 6 | **Plan and manage finance** | Analyse financial needs, quantify risk and contingency allocations, track spend, report, **manage financial reserves** | "CPI is 0.85 at 40% complete. What is the EAC?" |
| 7 | **Plan and optimize quality of products/deliverables** | Gather quality requirements, plan processes, ensure regulatory compliance, manage **cost of quality and sustainability**, improve continuously | "Defects keep escaping into UAT." |
| 8 | **Plan and manage schedule** | Prepare a schedule to fit the approach, estimate (milestones, dependencies, **story points**), baseline it, analyse variation | "You need to shorten the schedule without changing scope." |
| 9 | **Evaluate project status** | Develop metrics, tailor and maintain artefacts, assess progress, communicate status | Read this burndown and say what is happening. |
| 10 | **Manage project closure** | Get approval of completion, define closure criteria, validate readiness for transition, conclude lessons, procurement, financials, resources | "The customer is using the product but has not signed off." |

Three things to notice. Task 1 puts **choosing the development approach** at the
very top of the Process domain, which is why [P3's](pmp-mindset.html) routine
makes identifying predictive-versus-agile step two. Task 6 is called *finance*,
not *cost* — it covers reserves and funding, not just estimating. And Task 8
lists story points alongside milestones and dependencies in the same breath,
which tells you how thoroughly hybrid the exam's view of scheduling now is.

**Where your CISSP helps a little:** procurement and quality touch third-party
risk and assurance ideas you already have. The estimating, critical path, and
earned value mechanics are genuinely new, and they are the only part of PMP that
is arithmetic. [P5](pmp-predictive.html) covers all of it.

## Domain III — Business Environment (26%)

Eight tasks. Grew from 8% to 26% in the 2026 outline, mostly by absorbing tasks
that used to live in Process.

| # | Task | What it means | Your CISSP equivalent |
| --- | --- | --- | --- |
| 1 | **Define and establish project governance** | Structure, rules, reporting, ethics and policies via organisational process assets; **define success metrics**; set escalation paths and thresholds | Security governance, RACI, committee structures — near-identical |
| 2 | **Plan and manage project compliance** | Confirm requirements (security, health and safety, **sustainability**, regulatory), classify categories, analyse consequences of non-compliance, measure it | Compliance domain, control mapping, audit evidence |
| 3 | **Manage and control changes** | Execute change control, communicate status of proposals, implement approved changes, update documentation | Change management and configuration control |
| 4 | **Remove impediments and manage issues** | Evaluate impact, prioritise, apply intervention strategies, **recognise when a risk becomes an issue** | Incident and problem management, by another name |
| 5 | **Plan and manage risk** | Identify, analyse, monitor and control, maintain the register, execute responses including **security and sustainability risk** | Risk management — the closest single mapping on the whole exam |
| 6 | **Continuous improvement** | Use lessons learned, keep improvement processes updated, update organisational process assets | Continuous monitoring and improvement |
| 7 | **Support organizational change** | Assess organisational culture, evaluate the impact of change on the project, determine actions | Security awareness and culture change |
| 8 | **Evaluate external business environment changes** | Survey regulatory, technology, geopolitical and market change; assess and prioritise the impact **on scope or backlog** | Threat landscape monitoring |

**Read that right-hand column as a study plan.** You are not learning this domain
from zero; you are relearning vocabulary for concepts you already hold. Two
genuine deltas to watch:

1. **Risk response vocabulary differs.** PMI uses avoid / transfer / mitigate /
   accept / *escalate* for threats, and exploit / share / enhance / accept /
   escalate for **opportunities**. CISSP barely treats upside risk. PMP tests it
   constantly, and "escalate" as a fifth response is a 2017-era addition people
   still miss.
2. **Sustainability is examinable now.** It appears explicitly in the enablers
   for compliance (task 2), risk (task 5), and quality (Process task 7). If a
   question offers an option that considers environmental or community impact
   and the others do not, that option is usually live rather than a distractor —
   which is the opposite of how you would read it on a security exam.

Two enablers worth memorising outright because they are single-sentence exam
answers: **"recognise when a risk becomes an issue"** (task 4) and **"define
success metrics"** (task 1).

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
