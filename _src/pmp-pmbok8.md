# P4. PMBOK 8, and AI as an Exam Topic

You sit the exam on the [Exam Content Outline](pmp-eco.html), not on the *PMBOK
Guide*. But the 8th edition is what the question writers had open, so knowing
how it is organised tells you how they think. This lesson is the map, not the
territory — read it once, then use it to look things up.

## What changed from the 7th edition

The 7th edition (2021) swung hard toward principles and away from process, which
left a lot of candidates with nothing concrete to hold. The 8th edition swings
partway back.

| | 7th edition | 8th edition |
| --- | --- | --- |
| Principles | 12 | **6** |
| Performance domains | 8 | **7** |
| Processes | Removed to a separate practice guide | **40, embedded in the domains** |
| Character | Principle-based, descriptive | Function-oriented, with processes and outputs restored |
| New content | — | **An Artificial Intelligence chapter** |

The practical effect: the 8th edition tells you, for each area of the project,
what to do in what order and what artefact comes out. That is much closer to how
exam questions are framed.

## How the 8th edition is organised

Nine content areas, each broken into numbered **focus areas** that map to a
process group and produce a named output. This structure is worth skimming
because it answers a very common exam question shape: *"which document would you
use here?"*

### Project foundations

Definitions and framing rather than process. A project is temporary and delivers
change in the form of business or customer value.

**Development approaches** — the table that Process task 1 is really asking
about:

| Approach | Requirements | Activities | Delivery | Goal |
| --- | --- | --- | --- | --- |
| **Predictive** | Fixed | Performed once for the whole project | Single delivery | Manage cost |
| **Iterative** | Dynamic | Repeated until correct | Single delivery | Correctness of the solution |
| **Incremental** | Dynamic | Performed once per increment | Frequent smaller deliveries | Speed |
| **Adaptive (agile)** | Dynamic | Repeated until correct | Frequent small deliveries | Customer value through feedback |
| **Hybrid** | Any combination of predictive and adaptive | | | |

Learn the difference between **iterative** and **incremental**, because the exam
separates them and most people blur them. Iterative means *reworking the same
thing until it is right*. Incremental means *delivering usable pieces one at a
time*. Agile is both at once.

**Project lifecycle** is the set of phases, which may have **phase gates** where
you review against objectives and decide to proceed, change, or stop. The
lifecycle is *when*; the development approach is *how*.

**PMO types**, which come up as a matching question:

| Type | Control | What it does |
| --- | --- | --- |
| **Supportive** | Low | Consultative. Templates, best practice, training, a project repository. |
| **Controlling** | Moderate | Requires compliance with methods, templates, frameworks. |
| **Directive** | High | Directly manages the projects. PMs are assigned by and report to the PMO. |

**Manager types**: the *project manager* leads the team delivering value; the
*functional manager* owns resources in a business unit; the *operations manager*
keeps business operations running. PM authority rises as you move from
functional → weak matrix → balanced matrix → strong matrix → projectized.

**The PMI Talent Triangle**, which is also how your PDUs are categorised later:

- **Ways of working** — methods, and tailoring them to the environment
- **Power skills** — collaborative leadership, communication, the soft skills
- **Business acumen** — cost versus benefit, good business decisions

### Governance

| # | Focus area | Process group | Main output |
| --- | --- | --- | --- |
| 1 | Initiate project or phase | Initiate | **Project charter** |
| 2 | Integrate and align project plan | Plan | Project management plan |
| 3 | Plan sourcing strategy | Plan | Sourcing strategy plan |
| 4 | Manage project execution | Execute | Deliverables, work performance data |
| 5 | Manage quality assurance | Execute | Quality reports |
| 6 | Manage project knowledge | Execute | Lessons learned register |
| 7 | Monitor and control project performance | Monitor & control | Work performance reports |
| 8 | Assess and implement changes | Monitor & control | Approved change requests |
| 9 | Close project or phase | Close | Final report, product transition |

### The other seven

| Area | Focus areas | Signature outputs |
| --- | --- | --- |
| **Stakeholders** | 7 | Stakeholder register, stakeholder engagement plan, communications management plan |
| **Scope** | 6 | Scope management plan, requirements documentation, scope statement, scope baseline (statement + WBS + dictionary + work packages) |
| **Schedule** | 3 | Schedule management plan, schedule baseline, milestones, activity list |
| **Finance** | 4 | Financial management plan, funding strategy, cost estimates and basis of estimates, cost baseline |
| **Resources** | 5 | Resource management plan, **team charter**, resource breakdown structure, resource calendars |
| **Risk** | 6 | Risk management plan, risk register, risk report |
| **Procurement** | — | Procurement documents, agreements, selected sellers |
| **Artificial intelligence** | — | See below |

Notice **finance** has only four focus areas and **schedule** only three, while
stakeholders has seven. That is a reasonable proxy for where the emphasis sits.

## The documents that get confused

The single most reliable matching-question topic on the exam. Learn these four:

| Document | What it is | Who owns it |
| --- | --- | --- |
| **Business case** | A feasibility study — *do we need a project at all?* Contains the need, situation analysis, options, and a recommendation. Exists **before** the project. | Sponsor / organisation |
| **Benefits management plan** | How and when benefits will be delivered, and how they will be measured. Often extends past project close. | Sponsor / benefits owner |
| **Project charter** | Formally authorises the project's existence and gives the PM authority to apply organisational resources. | Issued by the **sponsor or initiator**, never the PM |
| **Project management plan** | How the project will be managed. Contains every subsidiary plan and the baselines. | PM |

And the three logs:

| Log | Records |
| --- | --- |
| **Change log** | Requested changes to baselined items, and their status |
| **Issue log** | Issues affecting the project, their status, and who owns resolving them |
| **Assumption log** | Assumptions and dependencies, especially those behind estimates |

And the two plans people swap:

| Plan | Covers |
| --- | --- |
| **Configuration management plan** | *Which* items are baselined and what their current versions are |
| **Change management plan** | The *process* for raising, assessing and approving changes to baselined items |

## The AI chapter

New in the 8th edition, and the 2026 outline treats AI as examinable. The
questions are not technical — they are governance questions with AI as the
subject. Your CISSP is close to a complete answer here.

**The classification**, which is worth knowing only at the level of not mixing
the terms up:

- **AI** — systems that reason, learn, and act autonomously
- **Machine learning (ML)** — a subfield of AI; trains on data to predict outputs
- **Deep learning (DL)** — multilayer neural networks, data- and compute-hungry
- **Generative AI** — a subset of DL using large language models to generate new
  text, images, audio, video
- **GPT** — generative pre-trained transformer

**The risks, which is what actually gets tested:**

| Risk | The concern |
| --- | --- |
| **Bias** | The model only saw certain things in training |
| **Privacy** | Company data in prompts may train future models |
| **Accountability** | Human accountability still sits on top of AI output |
| **Reliability** | Output may be confidently wrong; validate it |
| **Safety** | The system needs monitoring against a required safety level |
| **Transparency** | Data use, handling, algorithms and decisions should be visible to users |
| **Copyright** | Generated content trained on existing work raises ownership questions |
| **Sustainability** | Each request consumes electricity and water |

The exam's posture: **AI is a tool the project manager governs, not a decision
maker they defer to.** When a question offers "use the AI output" versus "check
the policy and validate the output", take the second. Accountability does not
transfer to a model — which is exactly the position you already hold
professionally.

Sustainability appearing as an *AI* risk is the tell for how seriously the 2026
outline takes sustainability generally. Do not dismiss it as a soft option.

## What to actually do with this lesson

Do not study PMBOK 8 linearly. Use this page three ways:

1. **Before the drills**, to know what the vocabulary space looks like.
2. **When a drill exposes a gap**, to find the right chapter.
3. **For matching questions**, because the document, PMO, and development
   approach tables above are exactly the pairs that get matched.

## Sources

- *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*, 8th
  edition — free to PMI members at [pmi.org](https://www.pmi.org/)
- [PMP Examination Content Outline, July 2026 (PMI, PDF)](https://www.pmi.org/-/media/pmi/documents/public/pdf/certifications/new-pmp-examination-content-outline-2026.pdf)
- Structure and focus-area tables cross-checked against personal PMP course
  notes covering the 8th edition; see [P10](pmp-plan.html) on which study
  material is current for the July 2026 exam.
