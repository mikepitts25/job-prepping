# P9. Matching and Drag-and-Drop Drills

Alongside the scenario questions, the exam uses **matching**, **drag-and-drop**,
and **point-and-click** items. These test recall of named things rather than
judgment, which makes them the most reliably winnable questions on the paper —
and the ones you lose purely by not having learned a list.

Sixty pairs below, grouped by topic. Cover the right-hand column, work down the
left, then check. Anything you miss twice goes on a flashcard.

## 1. Estimating techniques

| Description | Technique |
| --- | --- |
| Add together the smallest pieces of the WBS to get a total | **Bottom-up** |
| Use a rate — $55 per metre, $100 per hour | **Parametric** |
| Use a similar past project or product as the basis | **Analogous** |
| Average optimistic, most likely and pessimistic equally | **Three-point (triangular)** |
| Weight the most likely estimate four times | **PERT / beta** |
| Estimators discuss the high and low outliers, then re-estimate until consensus | **Wideband Delphi / planning poker** |

Speed and accuracy run opposite: analogous is fastest and least accurate,
bottom-up is slowest and most accurate, parametric sits in the middle.

## 2. Charts and visual tools

| Need | Tool |
| --- | --- |
| Show planned work remaining against actual, over an iteration | **Burndown chart** |
| Show work completed against total scope, so scope growth is visible | **Burnup chart** |
| Count items completed per day or per period | **Throughput chart** |
| See project activities on a calendar as bars | **Gantt chart** |
| Show work in each state over time; widening bands reveal bottlenecks | **Cumulative flow diagram** |
| Trace customer requirements through to completed deliverables and tests | **Requirements traceability matrix** |
| Show which risks have the largest impact on an outcome, ranked | **Tornado diagram (sensitivity analysis)** |
| Show decision paths with costs, benefits and probabilities | **Decision tree** |

## 3. Earned value and variance

| Equation | Name |
| --- | --- |
| EV − AC | **Cost variance (CV)** |
| EV − PV | **Schedule variance (SV)** |
| EV / AC | **Cost performance index (CPI)** |
| EV / PV | **Schedule performance index (SPI)** |
| BAC / CPI | **EAC**, assuming current performance continues |
| BAC − EAC | **Variance at completion (VAC)** |
| (BAC − EV) / (BAC − AC) | **TCPI** to the original budget |
| EAC − AC | **Estimate to complete (ETC)** |

The shape to remember: **EV comes first in every formula.** Subtraction gives a
variance in currency; division gives an index. Compare to AC for cost, PV for
schedule. Negative variance and index below 1.0 are both bad.

## 4. Risk responses

| Situation | Threat response |
| --- | --- |
| Remove the scope that causes it | **Avoid** |
| Buy insurance, or contract it to a third party | **Transfer** |
| Take action to reduce probability or impact | **Mitigate** |
| Acknowledge it, take no action, carry on | **Accept** |
| It is outside your authority to address | **Escalate** |

| Situation | Opportunity response |
| --- | --- |
| Make certain it happens — assign resources, prioritise it | **Exploit** |
| Give a third party ownership so the benefit is realised | **Share** |
| Increase the probability or the benefit | **Enhance** |
| Acknowledge it, take no action | **Accept** |
| It is outside the project's scope | **Escalate** |

Avoid/exploit are the mirrored pair at the aggressive end; accept and escalate
appear on both lists unchanged.

## 5. Risks, issues and changes

| It is… | Record it in the… |
| --- | --- |
| Something that might happen in future | **Risk register** |
| Something that has already happened | **Issue log** |
| A requested change to a baselined item | **Change log** |
| A dependency or belief behind an estimate | **Assumption log** |
| Knowledge captured for the benefit of later work | **Lessons learned register** |

**If it has already happened it is an issue, not a risk.** If a response was
already planned for it, execute that response first.

## 6. Procurement

| Need | Document |
| --- | --- |
| Find out what a seller can provide | **RFI** — request for information |
| Get a price against defined requirements | **RFQ** — request for quote |
| Ask sellers to propose a solution to a problem | **RFP** — request for proposal |
| Define what the vendor must deliver | **Statement of work** |

| Situation | Contract type |
| --- | --- |
| Scope is clear, stable and well defined | **Fixed price** |
| Scope is expected to change; developmental work | **Cost reimbursable** |
| No precise statement of work; staff augmentation or experts | **Time and materials** |
| Share savings and overruns against an agreed target | **Target-cost** |

| Dispute route | What it is |
| --- | --- |
| Buyer and seller cannot agree a change has occurred | **Claim** |
| Talk it out directly | **Negotiation** |
| A neutral third party helps them agree | **Mediation** |
| A panel hears both sides and issues a binding decision | **Arbitration** |
| Neutral experts appointed at project start to head off disputes | **Dispute review board** |
| An independent expert decides one technical issue | **Expert determination** |
| Court | **Litigation** |

The claims process and the dispute route are both defined **in the contract** —
which is the answer to "where do you look first" on any vendor disagreement.

## 7. Quality

| Description | Term |
| --- | --- |
| Number of desirable features | **Grade** |
| Degree to which features meet requirements | **Quality** |
| Training, prototypes, good design — stopping defects arising | **Prevention cost** |
| Testing, inspections, audits — finding defects | **Appraisal cost** |
| Defects found before the customer sees them | **Internal failure cost** |
| Defects, complaints and returns after delivery | **External failure cost** |
| Plan, do, check, act | **Deming / Shewhart cycle (PDCA)** |
| Define, measure, analyse, improve, control | **Six Sigma (DMAIC)** |
| Fishbone diagram grouping causes into categories | **Ishikawa / cause-and-effect** |
| Ask "why" repeatedly until the true cause emerges | **Five whys** |
| Sort defect categories most to least frequent | **Pareto analysis** |
| Count how often each thing occurs, as tallies | **Check sheet** |
| A list of items to be considered, used as a reminder | **Checklist** |

## 8. Schedule

| Description | Term |
| --- | --- |
| The longest path through the network; the shortest possible duration | **Critical path** |
| Delay available before the project end date moves | **Total float** |
| Delay available before the successor's early start moves | **Free float** |
| Overlap sequential activities to compress the schedule | **Fast-tracking** — adds risk |
| Add resources or overtime to compress the schedule | **Crashing** — adds cost |
| Fix over-allocated resources, accepting that the critical path may move | **Resource levelling** |
| Adjust activities within their float only, leaving the critical path alone | **Resource smoothing** |
| Plan near-term work in detail, far-term at a high level | **Rolling wave planning** |
| Bring an activity forward to overlap its predecessor | **Lead** |
| Enforce a wait between two activities | **Lag** |

**Levelling versus smoothing** is a near-guaranteed matching pair: levelling can
change the critical path, smoothing cannot.

## 9. Agile roles, events and artefacts

| Description | Term |
| --- | --- |
| Owns and orders the product backlog; decides *what* | **Product owner** |
| Removes impediments, coaches, facilitates; owns the process | **Scrum master** |
| Decides *how* the work gets done; self-managing | **Developers** |
| The team break epics into user stories and add acceptance criteria | **Backlog refinement** |
| The team plan the coming iteration's work | **Iteration / sprint planning** |
| Fifteen minutes; the team re-plan the day and raise impediments | **Daily scrum / stand-up** |
| The team demonstrate the working increment to the customer | **Sprint review / demonstration** |
| The team inspect their own way of working and commit to an improvement | **Retrospective** |
| Criteria that must be met before work can start | **Definition of ready** |
| Criteria that make an increment complete and shippable | **Definition of done** |
| The smallest release that delivers value and generates learning | **MVP** |
| A timeboxed investigation to reduce uncertainty | **Spike** |
| Project information visible on the team's wall | **Information radiator** |
| Risks prioritised in the backlog alongside value-delivering work | **Risk-adjusted backlog** |

## 10. Agile measurement and flow

| Description | Term |
| --- | --- |
| Story points completed per iteration, averaged | **Velocity** |
| Work in progress ÷ throughput | **Little's Law** (gives cycle time) |
| From request to delivery — the customer's experience | **Lead time** |
| From work started to delivered | **Cycle time** |
| Cap the number of items in a workflow state | **WIP limit** |
| The constraint sets the pace of the whole system | **Theory of constraints** |

To reduce cycle time, reduce work in progress. That single relationship answers
most "the team feels slow" questions.

## 11. Development approaches

| Characteristic | Approach |
| --- | --- |
| Fixed requirements, one delivery, goal is cost control | **Predictive** |
| Dynamic requirements, repeated until correct, one delivery | **Iterative** |
| Dynamic requirements, frequent smaller deliveries, goal is speed | **Incremental** |
| Dynamic requirements, repeated *and* frequent delivery, goal is customer value | **Adaptive / agile** |
| Any combination of the above | **Hybrid** |

## 12. Organisational structures and PMO

| Description | Type |
| --- | --- |
| PM has little authority; functional managers control resources | **Functional / weak matrix** |
| PM and functional manager share authority | **Balanced matrix** |
| PM has most of the authority | **Strong matrix** |
| PM has full authority; the team reports to the PM | **Projectized** |
| Consultative; supplies templates, training, a repository | **Supportive PMO** |
| Requires compliance with methods and templates | **Controlling PMO** |
| Directly manages projects; PMs report to it | **Directive PMO** |

## 13. Teams and people

| Description | Term |
| --- | --- |
| Forming, storming, norming, performing, adjourning | **Tuckman's ladder** |
| Hygiene factors prevent dissatisfaction; motivators create satisfaction | **Herzberg** |
| Needs met bottom to top before the next level is reachable | **Maslow** |
| People avoid work and need directing / people take pride and need trusting | **Theory X / Theory Y** |
| Work expands to fill the time available | **Parkinson's Law** |
| Win/win; incorporate all viewpoints | **Collaborate / problem solve** |
| Lose/lose; everyone gives up something | **Compromise** |
| Lose/win; concede to keep the relationship | **Accommodate / smooth** |
| Win/lose; impose your position | **Force / direct** |
| Senior management and the sponsor | **Upward influence** |
| Suppliers, users, government | **Outward influence** |
| Focuses on the team's growth, autonomy and wellbeing | **Servant leadership** |

## 14. Documents

| Purpose | Document |
| --- | --- |
| Asks whether the project is needed at all | **Business case** |
| Formally authorises the project and empowers the PM | **Project charter** |
| Team values, agreements and ground rules | **Team charter** |
| How and when benefits arrive, and how they are measured | **Benefits management plan** |
| Which items are baselined and at what version | **Configuration management plan** |
| The process for raising and approving changes | **Change management plan** |
| Current versus desired engagement for each stakeholder | **Stakeholder engagement assessment matrix** |

## How to use this page

Three passes, spread out:

1. **First pass, early.** Read it through; expect to know perhaps half.
2. **Second pass, a week later.** Cover the right column. Mark misses.
3. **Third pass, the week of the exam.** Only your marked misses.

Spacing matters more than duration here. Three fifteen-minute passes across three
weeks beats one ninety-minute session, by a wide margin, for exactly the kind of
paired recall these questions test.

## Sources

Pairs are original, written against the published outline and the standard
bodies of knowledge. The topic coverage is modelled on the areas PMI uses for
matching-format items.

- [PMP Examination Content Outline, July 2026 (PMI, PDF)](https://www.pmi.org/-/media/pmi/documents/public/pdf/certifications/new-pmp-examination-content-outline-2026.pdf)
- *PMBOK Guide* 8th edition and *Agile Practice Guide* — free to PMI members
