# P7. Agile and Hybrid

Roughly half the exam is set in agile or hybrid environments. You have run a
backlog as a product owner, so much of this is familiar; the risk for you is the
opposite of the usual one. You know how agile works *in a real organisation*,
with its compromises. The exam tests how agile works *as PMI describes it*. Where
those differ, answer PMI's version.

## The Agile Manifesto

Four value statements, agreed by seventeen practitioners in 2001. The exam uses
them as a tiebreaker, so know which side of each pair wins.

> **Individuals and interactions** over processes and tools
> **Working software** over comprehensive documentation
> **Customer collaboration** over contract negotiation
> **Responding to change** over following a plan

The right-hand items still have value — the left-hand items have *more*. An exam
answer that abandons documentation or contracts entirely is overshooting; one
that prioritises a process or a document over a conversation is undershooting.

The twelve principles behind it are worth one read. The four that carry the most
exam weight:

- Satisfy the customer through **early and continuous delivery** of value.
- **Welcome changing requirements, even late** in development.
- **Face-to-face conversation** is the most efficient way to convey information.
- **Working software is the primary measure of progress** — not reports, not
  percentage complete.

That last one decides a recurring question type: when the options include
producing a status report and demonstrating working output, demonstrate.

## Telling which world a question is in

| Signal words | World |
| --- | --- |
| sprint, backlog, product owner, Scrum Master, velocity, retrospective, increment | Agile |
| baseline, change control board, WBS, critical path, earned value, phase gate | Predictive |
| both sets in one scenario | Hybrid |

This matters because the correct answer flips. A scope change in a predictive
scenario goes to the CCB. The same change in an agile scenario goes into the
product backlog for the product owner to prioritise — **no change request, no
CCB**. Getting this backwards is one of the most common avoidable failures.

## Scrum, as PMI describes it

Three accountabilities, five events, three artefacts. Know them exactly.

**Accountabilities**

| Role | Owns |
| --- | --- |
| **Product Owner** | The product backlog, its ordering, and value. One person, not a committee. Decides *what*. |
| **Scrum Master** | The process. Coaches, facilitates, removes impediments. **Servant leader, not a manager.** |
| **Developers** | How the work gets done, and the sprint backlog. Self-managing. Decides *how*. |

The Scrum Master does not assign work, does not estimate for the team, and does
not commit on the team's behalf. If an answer has the Scrum Master deciding
something the team should decide, it is wrong.

**Events**

| Event | Timebox (1-month sprint) | Purpose |
| --- | --- | --- |
| Sprint | ≤ 1 month | The container for everything else |
| Sprint planning | ≤ 8 hours | What and how for this sprint |
| Daily scrum | 15 minutes | The developers re-plan the day. Not a status report to the PM. |
| Sprint review | ≤ 4 hours | Inspect the increment **with stakeholders**, adapt the backlog |
| Sprint retrospective | ≤ 3 hours | Inspect the team's process, commit to one improvement |

**Artefacts and their commitments**: product backlog → product goal; sprint
backlog → sprint goal; increment → **definition of done**.

The definition of done is the quality bar for "shippable". Acceptance criteria
are per-story. Confusing the two is a tested distinction. A third term rounds it
out: the **definition of ready** is the criteria a backlog item must meet before
the team will start it. Ready gates work *in*, done gates work *out*.

**Backlog refinement** is where the customer, developers and testers break epics
down into user stories and add acceptance criteria. Aim small enough to fit
inside one iteration. The product backlog and product roadmap are high level;
**user stories are the detailed level**.

**Sprint rules that get tested**

- Scope within a sprint may be **renegotiated** with the product owner as more is
  learned, but new work is not simply injected.
- **Only the product owner can cancel a sprint**, and it happens when the sprint
  goal becomes obsolete. It is rare.
- Unfinished work at sprint end goes **back to the product backlog** and is
  re-estimated and re-prioritised. It does not "roll over" automatically, and
  sprints are not extended to finish it.
- The sprint length is fixed. If the team keeps missing, the answer is to take
  less work in, not to lengthen the sprint.

## Estimation and measurement

- **Story points** are relative size — effort, complexity, uncertainty — not
  hours. They are not comparable across teams and are never used to compare
  teams.
- **Velocity** is points completed per sprint, averaged over recent sprints. Used
  for forecasting *by this team*, never as a performance target. If an answer
  uses velocity to judge or compare people, it is wrong.
- **Planning poker** for relative estimation; **affinity estimation** for large
  backlogs quickly; **t-shirt sizing** for coarse early work.
- Burndown shows work remaining against time. **Burnup** shows work completed
  against total scope, which makes scope changes visible — the reason PMI
  prefers it for stakeholder communication.
- **Cumulative flow diagram** shows work in each state over time. Widening bands
  mean a bottleneck. This is the graphic most likely to appear as a
  graphic-based question.

## Kanban and lean

- Visualise the workflow, **limit work in progress**, manage flow, make policies
  explicit, improve collaboratively.
- **Little's Law**: `cycle time = work in progress / throughput`. To reduce cycle
  time, reduce WIP. That is the answer to most "the team is slow" Kanban
  questions.
- **Lead time** is from request to delivery. **Cycle time** is from work started
  to delivered. Lead time is the customer's experience.
- Kanban is continuous flow with no fixed iterations, pull-based, and changes can
  enter the queue at any time. **Scrumban** puts WIP limits and flow onto Scrum's
  cadence.
- The seven lean wastes matter mainly as a concept: anything not adding customer
  value.

## XP practices worth naming

Pair programming, test-driven development, continuous integration, refactoring,
simple design, collective code ownership, small releases, sustainable pace,
on-site customer. XP contributes the engineering discipline that Scrum leaves
unspecified — which is why hybrid answers often pair "Scrum for cadence" with
"XP practices for quality".

## Other frameworks worth recognising

You will not be asked to run these, only to recognise them.

| Framework | Known for |
| --- | --- |
| **Scrum** | Fixed-length sprints, three accountabilities, five events |
| **Kanban** | Continuous flow, WIP limits, no fixed iterations |
| **Scrumban** | Kanban's WIP limits and flow on Scrum's cadence |
| **XP** | Engineering practices — TDD, pair programming, CI, refactoring |
| **FDD** (feature-driven development) | Model first, then a feature list, then design and build by feature |
| **Crystal** | A family of methods tailored by team size and criticality |
| **DSDM** | Fixes time and cost, varies scope; strong on governance and business case |

**Scaling frameworks**, for multiple teams on one product: **SAFe**, **LeSS**,
**Nexus**, **Disciplined Agile**, and **Scrum of Scrums** (a representative from
each team meets to coordinate and surface cross-team impediments). Recognition
level is enough.

**Theory of constraints**: the slowest step sets the pace of the whole system, so
improving anything other than the constraint changes nothing. This is the
reasoning behind fixing the bottleneck in a cumulative flow diagram rather than
adding people upstream.

## Servant leadership

The People domain's agile face. The servant leader:

- removes impediments rather than assigning work
- asks rather than tells
- shields the team from interruption
- builds the team's capability so they need them less
- measures success by the team's growth

Almost every agile People-domain question has one option that coaches or
facilitates and three that direct. Take the coaching one.

## Hybrid

Hybrid is the realistic case and the 2026 exam leans into it. Common shapes:

- Predictive at the programme or phase-gate level, agile within delivery teams.
- Agile for software, predictive for hardware, integration, or certification
  work that has fixed dependencies and long lead times.
- Agile delivery with predictive governance, funding, and reporting — which is
  exactly the defence-programme pattern in the [CAM track](cam-evms.html).

The exam's view of tailoring:

| Factor pushing toward predictive | Factor pushing toward agile |
| --- | --- |
| Stable, well-understood requirements | Volatile or unclear requirements |
| Regulatory or safety certification | Fast feedback available |
| Fixed-price contract, fixed scope | Customer available and engaged |
| Large, distributed, contractual interfaces | Small, co-located, empowered team |
| High cost of change late | Low cost of change |

When a question describes the situation and asks which approach, match against
that table. When it describes a hybrid and asks what to do, apply the rules of
whichever layer the question is operating in.

## The agile equivalents of predictive artefacts

Useful for hybrid questions, and for translating when you already know the
predictive answer.

| Predictive | Agile equivalent |
| --- | --- |
| Requirements document | Product backlog |
| WBS work package | Epic / feature / user story |
| Detailed schedule | Release plan + sprint backlog |
| Status report | Information radiator, burndown, review |
| Change control board | Product owner reprioritising the backlog |
| Verify scope | Sprint review with stakeholders |
| Lessons learned | Retrospective, every sprint |
| Risk register | Risk-adjusted backlog — risks prioritised alongside value work |
| Quality plan | Definition of done |
| Progress by % complete | Working increments delivered |

## What "value delivery" means on the 2026 exam

The Process domain now has an explicit **deliver value** task, and it carries
the exam's strongest bias. Where two options are otherwise equal, the one that:

- gets working output in front of a customer sooner,
- validates an assumption earlier,
- or measures benefit rather than activity,

is the credited one. Terms to recognise: **minimum viable product** (smallest
thing that delivers value and generates learning), **benefits realisation plan**
(how and when benefits materialise, often after the project closes), **return on
investment**, **net present value**, and **cost of delay**.

## Sources

- [PMP Examination Content Outline, July 2026 (PMI, PDF)](https://www.pmi.org/-/media/pmi/documents/public/pdf/certifications/new-pmp-examination-content-outline-2026.pdf)
- *Agile Practice Guide* (PMI and Agile Alliance) — free to PMI members
- [The Scrum Guide](https://scrumguides.org/) — free, about fifteen pages, and
  the authority on everything in the Scrum section above. Read it whole; it takes
  half an hour and it is the highest value-per-page document in this track.
