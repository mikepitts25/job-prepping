# P5. Predictive Mechanics You Need Cold

This is the reference page for the Process domain: the arithmetic and the
artefacts. It is the only part of PMP that has right answers independent of
judgment, so it is the cheapest set of marks on the paper. Everything here is
worth knowing to the point of automaticity.

Where a topic overlaps something you already hold from CISSP, the heading says
so and the section stays short.

## The spine: charter to closure

| Artefact | Who authorises it | What it does |
| --- | --- | --- |
| Business case | Sponsor / organisation | Justifies the project. Exists *before* the project. |
| **Project charter** | Sponsor (never the PM) | Authorises the project and names the PM. Without it, no project. |
| Project management plan | PM, approved by stakeholders | Integrates all subsidiary plans and the three baselines. |
| **Baselines** (scope, schedule, cost) | Approved, then frozen | Changed only through change control. |
| Performance measurement baseline | Scope + schedule + cost, integrated | What you measure against. |
| Deliverables | Produced in execution | Verified (quality), then validated (customer accepts). |
| Final report + lessons | PM | Closure. |

Two exam-reliable facts: **the sponsor signs the charter, not the PM**, and
**verify scope is quality control's downstream cousin** — control quality checks
correctness internally, validate scope gets customer acceptance. Questions
exploit the difference constantly.

## Scope and the WBS

The **work breakdown structure** decomposes the total scope hierarchically. Rules
that get tested:

- The WBS contains **100% of the scope and nothing else** (the 100% rule). If it
  is not in the WBS, it is not in the project.
- The lowest level is a **work package**. Below that, in scheduling, sit
  activities. The WBS does not contain activities.
- Each work package gets a **WBS dictionary** entry: description, acceptance
  criteria, owner, resources, estimates.
- The WBS is deliverable-oriented, not phase- or function-oriented, though it can
  be organised by phase at the top level.

**Scope creep** is uncontrolled change. **Gold plating** is the team adding
unrequested extras. Both are bad; the exam wants you to name which one is
happening.

## Schedule

### Network diagrams and the critical path

Activities with dependencies. The **critical path** is the longest path through
the network, and therefore the shortest possible project duration. Activities on
it have **zero float**.

- **Total float** — how long an activity can slip without delaying the project
  end.
- **Free float** — how long it can slip without delaying its immediate successor.
- Total float = LS − ES = LF − EF.

Forward pass gives early start and early finish; backward pass gives late start
and late finish. If a question shows a network with durations, add the durations
along each path; the longest is critical.

There can be more than one critical path. More critical paths means more risk,
because more of the project has no slack.

### Dependency types

| Type | Meaning |
| --- | --- |
| Finish-to-start (FS) | B cannot start until A finishes. The default and the common one. |
| Start-to-start (SS) | B cannot start until A starts. |
| Finish-to-finish (FF) | B cannot finish until A finishes. |
| Start-to-finish (SF) | Rare. Almost always a distractor. |

**Lead** = an overlap, a successor starting early. **Lag** = an enforced wait.
Mandatory dependencies are hard logic; discretionary are preferred practice;
external come from outside the project; internal are within the team's control.

### Compressing a schedule

| Technique | What you do | What it costs |
| --- | --- | --- |
| **Crashing** | Add resources to critical path activities | Cost. Often disproportionate. |
| **Fast-tracking** | Run sequential activities in parallel | **Risk and rework.** |

Both apply only to the critical path — shortening a non-critical activity changes
nothing. If a question asks to shorten the schedule without increasing cost, the
answer is fast-tracking; without increasing risk, crashing. Reducing scope is a
change request, not compression.

Remember the **law of diminishing returns**: adding resources improves the
schedule only up to a point, and beyond it the effect shrinks. That is the
reasoning behind rejecting "add more people" as a reflex answer.

### Resource optimisation

Two techniques that get confused, and therefore get tested:

| Technique | What it does | Effect on the critical path |
| --- | --- | --- |
| **Resource levelling** | Resolves over-allocation — a resource assigned to two activities at once | **Can change it.** Start and finish dates may move. |
| **Resource smoothing** | Adjusts activities **within their existing float** only | **Never changes it.** |

If the question says the critical path must not move, the answer is smoothing.
If a resource is double-booked and something has to give, it is levelling.

### Forward and backward pass

To find float by hand: enter durations, run a **forward pass** for early start
and early finish, then a **backward pass** for late start and late finish. Float
is then `LS − ES` (equivalently `LF − EF`). The critical path is the path with
zero float.

One warning on arithmetic conventions. Some materials number days from 1 and use
`EF = ES + duration − 1`; others start from time zero and use
`EF = ES + duration`. Both give the same float and the same critical path — what
changes is the absolute day numbers. Pick one convention, use it consistently,
and read the question to see which it is using.

### Estimating

**Three-point estimating**, given optimistic (O), most likely (M), pessimistic (P):

- Triangular: `(O + M + P) / 3`
- **PERT / beta**: `(O + 4M + P) / 6`
- Standard deviation: `(P − O) / 6`

PERT is the one they mean unless they say otherwise. Learn both formulas; questions
occasionally specify triangular to catch people running on autopilot.

Other terms: **analogous** estimating is top-down from a similar past project
(fast, least accurate); **parametric** uses a rate (units × cost per unit);
**bottom-up** sums the work packages (slowest, most accurate).

## Cost and earned value

This is the highest-density formula area on the exam, and it is the same
machinery you will need for the CAM track in [C1](cam-evms.html). Learn it once,
use it twice.

### The three measurements

| Term | Meaning |
| --- | --- |
| **PV** — planned value | Budgeted cost of the work *scheduled* by now |
| **EV** — earned value | Budgeted cost of the work *actually completed* |
| **AC** — actual cost | What you actually spent to do that work |
| **BAC** — budget at completion | Total budget for the whole project |

EV is the pivot. It is always *budgeted* cost of completed work — never actual.
`EV = BAC × % complete`.

### Variances and indices

| Formula | Reads as |
| --- | --- |
| `CV = EV − AC` | Cost variance. Negative = over budget. |
| `SV = EV − PV` | Schedule variance. Negative = behind schedule. |
| `CPI = EV / AC` | Cost performance index. Below 1.0 = over budget. |
| `SPI = EV / PV` | Schedule performance index. Below 1.0 = behind schedule. |

Memorise the shape, not the four formulas: **EV comes first in every one**.
Subtraction gives a variance in currency; division gives an index. Compare against
AC for cost, PV for schedule. Negative variance and index below 1.0 are both bad.

### Forecasting

| Formula | Use when |
| --- | --- |
| `EAC = BAC / CPI` | Current cost performance will continue. **The default.** |
| `EAC = AC + (BAC − EV)` | The overrun was a one-off; remaining work goes to plan. |
| `EAC = AC + (BAC − EV) / (CPI × SPI)` | Both cost and schedule performance will continue. |
| `EAC = AC + bottom-up ETC` | The original estimate is no longer credible. |
| `ETC = EAC − AC` | Estimate to complete: what is left to spend. |
| `VAC = BAC − EAC` | Variance at completion. Negative = forecast overrun. |
| `TCPI = (BAC − EV) / (BAC − AC)` | Efficiency needed on remaining work to hit the original budget. |
| `TCPI = (BAC − EV) / (EAC − AC)` | Same, but to hit the revised (EAC) budget. |

TCPI above 1.0 means you must perform better than planned from here — harder than
what you have been doing. That is the interpretation they test.

### A worked example

> BAC = $500,000. The project is 40% complete. AC = $250,000. PV = $225,000.

- `EV = 500,000 × 0.40 = $200,000`
- `CV = 200,000 − 250,000 = −$50,000` → over budget
- `SV = 200,000 − 225,000 = −$25,000` → behind schedule
- `CPI = 200,000 / 250,000 = 0.80` → getting 80 cents of value per dollar
- `SPI = 200,000 / 225,000 = 0.89` → running at 89% of planned pace
- `EAC = 500,000 / 0.80 = $625,000`
- `VAC = 500,000 − 625,000 = −$125,000` → forecast $125k overrun
- `TCPI (to BAC) = (500,000 − 200,000) / (500,000 − 250,000) = 300,000 / 250,000 = 1.20`

Read that last number out loud: to still finish on the original budget you must
run at 1.20 efficiency having so far managed 0.80. That is not a recovery plan,
that is a conversation with the sponsor.

## Quality

**Prevention over inspection** is the doctrine, and it decides most quality
questions. Building quality in beats finding defects later.

- **Quality** is fitness for requirements. **Grade** is a category of features.
  Low quality is always a problem; low grade may be perfectly acceptable.
- **Plan quality** → **manage quality** (process, audits, are we doing the right
  things) → **control quality** (inspection, measurement, is this deliverable
  correct).
- **Cost of quality**: prevention + appraisal (conformance) versus internal and
  external failure (non-conformance). Prevention is always the cheapest money.
- **Accuracy** is closeness to the true value; **precision** is repeatability.
  Tested more often than it deserves.
- Tools: cause-and-effect (Ishikawa/fishbone) for root cause, Pareto for the
  vital few, control charts for whether a process is in control, histograms,
  scatter diagrams, check sheets.
- **Checklist versus check sheet**: a checklist is a list of items to consider,
  used as a reminder (also called a prompt list). A **check sheet** is a tally
  sheet, counting how often each thing occurs. Tested more than it should be.
- **Flowcharts** show process flow including decision points.

### Structured improvement methods

Named methods that appear as matching pairs and as "which approach" questions:

| Method | Steps |
| --- | --- |
| **PDCA** (Deming / Shewhart cycle) | **Plan** — see the problem directly, find root cause, prioritise solutions with the team. **Do** — pilot it small. **Check** — measure the results. **Act** — adjust. |
| **DMAIC** (Six Sigma) | **Define** the gap, **Measure** with real data, **Analyse** for root cause, **Improve** and measure, **Control** so the new process holds. |
| **Five whys** | Ask why repeatedly. The first answer is usually a symptom. |
| **Ishikawa / fishbone** | Problem at the head; brainstorm causes into categories — people, information, process, systems. |

Both PDCA and DMAIC put **measurement before solution**, which is the same
instinct as [P3's](pmp-mindset.html) first rule.
- Control chart rule: seven consecutive points on one side of the mean is the
  **rule of seven** — a non-random trend needing investigation, even if every
  point is inside the control limits. Points outside the control limits are
  out of control. Specification limits come from the customer; control limits
  come from the process.

## Risk — mostly a translation job

*You know this domain.* The ideas map almost one for one onto CISSP risk
management. What differs is vocabulary and the treatment of upside.

| Concept | PMI's word |
| --- | --- |
| Risk appetite / tolerance / threshold | Same terms, same meanings |
| Qualitative analysis | Probability × impact matrix → prioritised list |
| Quantitative analysis | Monte Carlo, decision trees, EMV. Only for high-priority risks, and often skipped |
| Expected monetary value | `EMV = probability × impact`, summed across risks |
| Threat responses | **Avoid, transfer, mitigate, accept, escalate** |
| Opportunity responses | **Exploit, share, enhance, accept, escalate** |
| Contingency reserve | For **known** risks. Inside the cost baseline. PM controls it. |
| Management reserve | For **unknown** risks. Outside the cost baseline, inside the budget. Sponsor/management controls it. |

Three things to actually learn here:

1. **Opportunities are risks too.** Half the response vocabulary is upside, and
   the exam uses it.
2. **Escalate** is a valid fifth response, for risks outside the project's
   authority. Once escalated, it leaves your risk register.
3. **The reserve distinction.** Contingency = known unknowns, PM's to spend.
   Management = unknown unknowns, needs approval. A question about using reserve
   is usually really a question about which reserve.

**Residual risk** remains after response; **secondary risk** is created by the
response itself. Both are terms you already own.

## Procurement — also mostly translation

Make-or-buy, then contract type. The contract type question is the one that
recurs:

| Type | Risk sits with | Use when |
| --- | --- | --- |
| **Fixed price** (FFP, FPIF, FP-EPA) | **Seller** | Scope is well defined |
| **Cost reimbursable** (CPFF, CPIF, CPAF) | **Buyer** | Scope is uncertain, R&D, evolving |
| **Time and materials** | Shared | Small, short, staff augmentation |

If the scenario says requirements are unclear or the work is developmental,
fixed price is the wrong answer — you cannot fix a price on undefined scope, and
a seller forced to will either pad heavily or claim relentlessly.

**Point of total assumption** applies only to FPIF: the cost above which the
seller absorbs every further dollar. Rarely calculated, occasionally named.

A fourth type appears in the 8th edition: **target-cost**, where buyer and seller
agree a target and share the savings or the overruns. Common on large
infrastructure and complex manufacturing.

Process flow: plan procurement → conduct (bids, source selection) → control
(administer) → close. Procurement documents you should recognise: RFI (information),
RFQ (price), RFP (solution). The **statement of work** defines what is bought.

**Bidder conferences** (also vendor or pre-bid conferences) are meetings with all
prospective sellers before proposals are submitted, so everyone has the same
understanding. Two source-selection variants worth naming: **single source**,
where only one supplier can meet the requirement because of unique expertise or
exclusive rights, and **fixed budget**, where the available budget is disclosed
and the best technical proposal within it wins.

You can have an **agreement without a contract** — a project charter authorising
internal resources is one — but never a contract without an agreement.

### Claims and dispute resolution

A **claim** arises when buyer and seller cannot agree that a change has occurred
or what it is worth. Like change requests, claims can happen at any point. The
escalation ladder, which is a matching-question favourite:

| Route | What happens |
| --- | --- |
| **Negotiation** | Directly between the parties. Always tried first. |
| **Mediation** | A neutral mediator helps them reach agreement. Non-binding. |
| **Arbitration** | A panel hears both sides and issues a **binding** decision. |
| **Dispute review board** | Neutral experts appointed at project start to prevent and resolve disputes as they arise. |
| **Expert determination** | An independent expert decides one specific technical question. |
| **Litigation** | Court. The last resort. |

**Both the claims process and the dispute route are defined in the contract.**
That is the answer to "where do you look first" on any vendor disagreement — and
it is also why "check the contract" beats "escalate to legal" as a first move.

### Emerging contract trends

The 8th edition names five, and they turn up as recognition questions rather than
anything deeper: **agile contracting** (flexibility and iterative delivery),
**smart contracts** (blockchain-automated execution), **outcome-based
contracts** (paying for results rather than inputs), **sustainable contracting**
(ESG criteria written into the agreement), and **collaborative contracting**
(risk and reward sharing with joint problem-solving).

## Stakeholders

Identify → analyse → plan engagement → manage → monitor. The analysis grids:

- **Power / interest grid** — high power + high interest = manage closely; high
  power + low interest = keep satisfied; low power + high interest = keep
  informed; low/low = monitor.
- **Salience model** — power, urgency, legitimacy.
- **Stakeholder engagement assessment matrix** — current versus desired
  engagement level, rated unaware / resistant / neutral / supportive / leading.
  When a question mentions a resistant stakeholder, this matrix is the artefact
  they want named.

## Communication

`n(n − 1) / 2` gives the number of communication channels for n people. If the
team grows from 5 to 8, channels go from 10 to 28 — the point being that adding
people adds communication cost superlinearly. Expect at least one question that
asks for the *increase*, not the total.

Push (email, reports), pull (portal, wiki), interactive (meetings, calls).
Interactive for anything complex or sensitive. Most of a PM's time is
communication, and PMI will tell you so in an answer option.

## Change control — you already know this

Same discipline as configuration and change management in a security programme.
The chain from [P3](pmp-mindset.html):

> assess impact → change request → CCB decision → update baseline → communicate →
> implement

**Configuration control** is about the product's specifications; **change
control** is about the baselines. The corresponding plans split the same way: the
**configuration management plan** says *which* items are baselined and at what
version, while the **change management plan** defines the *process* for changing
them.

The full change sequence, as the 8th edition states it: any stakeholder may raise
a change → record it in the **change log** → analyse the impact on cost and
schedule → take it to the approvers (the CCB) → **communicate the outcome**
(approved, rejected, or deferred) → record the outcome in the log and proceed.
Note that communicating a *rejection* is part of the process — an answer that
stops at the CCB decision is incomplete. An approved change request is an input to
execution, and a *corrective action*, *preventive action*, or *defect repair* is
implemented through the same route.

The PM may sit on the CCB but usually does not chair it. Emergency changes can
have an expedited route if the plan defines one — which is exactly the carve-out
you know from incident response.

## Closing

- Get **formal written acceptance**. Use in production without sign-off is not
  acceptance.
- Close procurements before closing the project.
- Capture lessons learned in the **lessons learned register** during the project
  and roll into the **lessons learned repository** at the end. Lessons are
  captured continuously, not just at the end — a favourite exam distinction.
- Release resources, archive records, transition the product and the benefits to
  the operational owner.
- A cancelled project is still **closed**, formally, with the same process. Why
  it ended is documented; the closure is not skipped.

## Sources

- [PMP Examination Content Outline, July 2026 (PMI, PDF)](https://www.pmi.org/-/media/pmi/documents/public/pdf/certifications/new-pmp-examination-content-outline-2026.pdf)
- *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*, 8th
  edition — free to PMI members at [pmi.org](https://www.pmi.org/)
- *Process Groups: A Practice Guide* (PMI) — the predictive process detail that
  PMBOK 7 and 8 leave out
