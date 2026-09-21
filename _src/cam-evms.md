# C1. Control Account Manager: EVMS from Zero

The Control Account Manager is the person who owns a slice of a defence
programme's scope, schedule, and budget, and who has to explain it when the
government asks. It is the single most scrutinised role in earned value
management, because the CAM is who a DCMA reviewer sits down with.

"CAM certification" means one of two different things, and it is worth being
clear about which you want before spending money. Both are covered here; the
knowledge underneath is the same.

## First: which credential?

| Path | What it is | Cost |
| --- | --- | --- |
| **Employer CAM certification** | Most primes — Lockheed, Boeing, GD, Raytheon — run their own internal CAM certification, because a validated EVMS requires documented CAM training. This is the one most people mean, and it is usually free to employees. | Internal |
| **CCAM** (Certified Control Account Manager, from the Earned Value Management Institute) | A commercial credential: ~40 hours of training plus a CAM notebook build, 60 PDUs on completion. Recognised across the A&D primes. | ~$5,499 |
| *Adjacent:* **EVP** (AACE Earned Value Professional) or **PSP** | Broader project-controls credentials, not CAM-specific | Several hundred dollars |

Two practical notes. The employer path is by far the most common and costs
nothing, so if you land a role at a prime, that is your route — and the material
below is what it will teach you. The CCAM's price tag is aimed at corporate
training budgets rather than individuals; it is a poor personal purchase unless
an employer is paying.

Either way, **do the free DAU and DOE training first** (listed at the end). It is
genuinely good, it costs nothing, and it is the same content.

## How this relates to your PMP

Substantial overlap, different emphasis:

- Everything in [P4's earned value section](pmp-predictive.html) is the
  foundation. The formulas are identical.
- PMP treats EVM as one technique among many, tested lightly. **EVMS treats it as
  the entire management system**, with 27 compliance guidelines and government
  audit behind it.
- PMP asks "what is the EAC". A CAM review asks "why is your CPI 0.87, what is
  the root cause, what is your corrective action, and why should I believe your
  EAC".

Do PMP first. The CAM material sits on top of it comfortably; the reverse is
harder.

## The structural chain

This hierarchy is the thing to internalise. Everything else follows from it.

```
Contract / Program
  └── WBS (work breakdown structure)   ──┐
        └── Control Account (CA)          │ intersection of
              ├── Work Package (WP)       │ WBS element and
              └── Planning Package (PP)  ──┘ OBS element
                    └── Activities / tasks
```

- **WBS** — the product-oriented decomposition of all contract scope. Same
  100% rule you learned for PMP. Defence programmes use MIL-STD-881 as the
  standard WBS template.
- **OBS** — organisation breakdown structure. Who performs the work.
- **Control account** — where the WBS and OBS intersect. **This is the CAM's
  unit of ownership, and the point at which cost and schedule performance is
  measured and reported.** One CAM per control account.
- **Work package** — near-term, detail-planned work inside a control account,
  with a specific scope, budget, schedule, and earned value method.
- **Planning package** — far-term work inside the control account, budgeted but
  not yet detail-planned. Converted to work packages through **rolling wave
  planning** before the work starts.
- **RAM** — responsibility assignment matrix. The grid of WBS against OBS,
  showing who owns which control account.

Two facts a reviewer will check: **every control account has exactly one CAM**,
and **the sum of control account budgets, plus undistributed budget and
management reserve, reconciles to the contract budget base.**

## The budget stack

Learn this vocabulary precisely — the exam-and-audit questions live in the
distinctions.

| Term | What it is |
| --- | --- |
| **NCC** — negotiated contract cost | Contract price less profit or fee |
| **AUW** — authorised unpriced work | Work directed but not yet negotiated |
| **CBB** — contract budget base | NCC + AUW. Everything authorised. |
| **MR** — management reserve | Budget held by the programme manager for in-scope unknowns. **Outside the PMB, inside the CBB.** Never used to cover an overrun. |
| **UB** — undistributed budget | Authorised budget not yet allocated to control accounts. Temporary by nature. |
| **PMB** — performance measurement baseline | CBB − MR. The time-phased plan against which performance is measured. |
| **TAB** — total allocated budget | Sum of all budgets. Equals CBB normally; **exceeds CBB in an over-target baseline.** |

`CBB = PMB + MR` and `PMB = distributed budget (control accounts) + UB`.

**Management reserve is not a contingency slush fund and it is not schedule
margin.** It is applied to in-scope work that was not anticipated, it is
documented when applied, and applying it to paper over a cost variance is exactly
the finding a surveillance review looks for.

## The measurements, again

Same three as PMP, with the defence names:

| Term | Also called | Meaning |
| --- | --- | --- |
| **PV** | BCWS — budgeted cost of work scheduled | Budget for the work planned by now |
| **EV** | BCWP — budgeted cost of work performed | Budget for the work actually done |
| **AC** | ACWP — actual cost of work performed | What was actually spent |

The BCWS/BCWP/ACWP names are still everywhere in defence documentation and in
older tools. Know both sets; the acronyms make the meaning clearer, if anything —
every one of them is "cost of work" qualified by *scheduled*, *performed*, or
*actual*.

### The formula set

| Formula | Meaning |
| --- | --- |
| `CV = EV − AC` | Cost variance. Negative = overrun. |
| `SV = EV − PV` | Schedule variance, in dollars. |
| `CPI = EV / AC` | Cost efficiency. |
| `SPI = EV / PV` | Schedule efficiency. |
| `CV% = CV / EV` | Percent cost variance — what variance thresholds are set on. |
| `SV% = SV / PV` | Percent schedule variance. |
| `EAC = AC + ETC` | The general form. Everything else is a way of estimating ETC. |
| `EAC = BAC / CPI` | Statistical / independent EAC. The reviewer's sanity check. |
| `EAC = AC + (BAC − EV) / (CPI × SPI)` | Composite, when schedule pressure is driving cost. |
| `VAC = BAC − EAC` | Variance at completion. |
| `TCPI = (BAC − EV) / (BAC − AC)` | Efficiency required to finish at BAC. |
| `%complete = EV / BAC` | |
| `%spent = AC / BAC` | |

**Schedule variance in dollars is not time.** SV tells you the budget value of
the work you are behind on, not how many weeks late you are. It also converges to
zero at completion, regardless of how late you finished — which is precisely why
the integrated master schedule, and not SV, is the authority on schedule status.

## Earned value methods

Each work package is assigned an EV method up front. Picking the wrong one is a
common finding.

| Method | How EV is taken | Use for |
| --- | --- | --- |
| **0/100** | Nothing until complete, then all | Short work packages (one accounting period) |
| **50/50** | Half at start, half at completion | Short packages spanning two periods |
| **Milestone / weighted milestone** | At defined milestones with pre-assigned budget values | Longer discrete work with objective checkpoints |
| **Percent complete** | CAM's assessment each period | Discrete work without natural milestones. The most subjective, so the most scrutinised. |
| **Units complete** | Physical count × unit budget | Repetitive production |
| **Apportioned effort** | Proportional to a related discrete base | Work that tracks another task, e.g. inspection against manufacturing |
| **LOE — level of effort** | EV = PV automatically, by passage of time | Sustaining, management, support. **Never generates a schedule variance.** |

**LOE is the one to be careful about.** Because EV always equals PV, LOE work can
never show schedule variance, so over-classifying discrete work as LOE hides
problems. Reviewers check the LOE percentage of a control account and ask why.
Keep it low, keep it genuinely non-discrete.

Prefer **objective, discrete** methods wherever the work allows. "We use percent
complete for everything" is not a defensible answer.

## The EIA-748 guidelines

EIA-748 is the standard that defines what an EVMS must do. **Revision E reduced
the guideline count from 32 to 27**, reorganised for clarity, keeping the same
five process categories:

| Process category | Roughly covers |
| --- | --- |
| **Organization** | Define the work with a WBS, define the organisation with an OBS, integrate them into control accounts, assign responsibility, integrate the subsystems |
| **Planning, Scheduling and Budgeting** | Schedule the work, set measurable milestones, budget it, establish the PMB, hold MR and UB identifiably, reconcile to the CBB |
| **Accounting Considerations** | Record direct costs consistently with budgets, summarise them through the WBS and OBS, track material and indirects properly |
| **Analysis and Management Reports** | Calculate variances monthly at the control account level, explain significant ones, sum them up the structure, maintain EACs, act on the data |
| **Revisions and Data Maintenance** | Incorporate authorised changes promptly, control retroactive changes, maintain baseline integrity, document over-target baselines |

Revision E's notable changes: the previous Guideline 27 was split to separate
control account EACs from programme-level EACs, and the Revisions category was
restructured to distinguish three change types cleanly — **customer-directed**,
**internal replanning**, and **over-target baseline / over-target schedule**.

The **NDIA IPMD Intent Guide** is the document that explains, for each guideline,
what it is for, what attributes demonstrate it, and what objective evidence
satisfies it. It is free and it is what compliance reviewers work from. Linked at
the end.

### Where the guidelines land on you as a CAM

You do not implement the system. You *comply* with it, and roughly ten of the 27
touch your daily work: owning your control account's scope and budget, keeping
your schedule logic valid, taking EV honestly and on the agreed method,
explaining variances above threshold with real root cause, maintaining a
defensible EAC, and processing changes through the proper route rather than by
adjusting history.

## Baseline changes — the rules that get people fired

| Allowed | Not allowed |
| --- | --- |
| Customer-directed changes, incorporated promptly | Changing budget or schedule for work already performed **to eliminate a variance** |
| Internal replanning of **future** work | Moving budget between control accounts without documented authorisation |
| Applying MR to in-scope unanticipated work, documented | Using MR to offset an overrun |
| Rolling wave conversion of planning packages to work packages | Retroactive adjustment of EV or actuals outside a documented correction |
| A formal over-target baseline, with customer approval | Informally "rebaselining" a control account that is running badly |

**Retroactive change is the cardinal sin.** If the baseline is genuinely
unachievable, the honest instrument is an **over-target baseline** (OTB) or
**over-target schedule** (OTS): a formal, customer-approved reset where TAB
deliberately exceeds CBB. It is a serious step and it is visible, which is the
point.

## The IBR

The **Integrated Baseline Review** is a joint government-contractor review,
usually within about six months of contract award or a major change. It is not a
compliance audit of the system — it asks whether the *baseline is realistic*:
does the PMB capture all the scope, is the schedule executable, are the resources
adequate, and are the risks understood?

**The IBR is conducted largely through CAM interviews.** You sit with a
government counterpart and walk through your control account. That interview is
what [C2](cam-drills.html) prepares you for.

Distinguish it from:

- **EVMS validation / compliance review** — does the *system* meet EIA-748? Done
  by DCMA when the contract crosses the threshold.
- **Surveillance** — ongoing checking that the validated system is still being
  used properly.

## When EVMS applies

DoD thresholds moved recently. Under the FY25 NDAA §823 and DFARS class
deviation 2026-O0011, effective 1 February 2026:

| Contract value | Requirement |
| --- | --- |
| Below $20M | EVM optional, applied on a risk basis |
| $20M–$50M | EVMS compliant with EIA-748 required for reporting |
| **$50M and above** | EIA-748 compliance required; DCMA determines compliance |
| **$100M and above** | Subject to EVMS compliance review / validation |

These numbers changed in 2026 and may change again — the trend has been upward.
Verify against current DFARS before relying on them. The reporting deliverable is
the **IPMDAR** (Integrated Program Management Data and Analysis Report), which
replaced the older IPMR and CPR formats.

## The CAM notebook

The artefact you maintain and the thing you bring to an interview. Typical
contents:

1. Control account scope — the statement of work extract, and the WBS dictionary
   entry
2. Work authorisation document, signed
3. The responsibility assignment matrix showing your control account
4. Time-phased budget, by element of cost, reconciling to the PMB
5. The integrated master schedule extract for your work, with logic and float
6. EV methods assigned per work package, with justification
7. Current period and cumulative performance data
8. Variance analysis reports for anything over threshold
9. EAC, with the basis of estimate
10. Change history — every baseline change, with its authorisation
11. Risks and opportunities affecting the control account

If you can produce each of these on request and explain it without hedging, you
will pass a CAM interview. If you cannot, no amount of EVM theory will save the
conversation.

## Free official training, ranked

| Resource | What it gives you |
| --- | --- |
| [DAU EVM 101 — Fundamentals of Earned Value Management](https://icatalog.dau.edu/mobile/CourseDetails.aspx?id=1907) | Free online DoD course. EVM policy, the PMB, measuring performance, and using EVM data for risk. Start here. |
| [DAU EVM 0020 — Performing Variance Analysis](https://www.dau.edu/) | Short, targeted, and the exact skill a CAM interview tests. |
| [DOE EVMS training](https://www.energy.gov/projectmanagement/evms-training) | A free 8-module EVM tutorial plus ~34 short topic videos. Excellent for non-DoD-specific fundamentals. |
| [NDIA IPMD guides and resources](https://www.ndia.org/divisions/ipmd/division-guides-and-resources) | The **EIA-748 Intent Guide** (Rev E, May 2026), the **EVMS Acceptance Guide**, the IBR guide, and the surveillance guide. All free. The Intent Guide is the single most useful document here. |
| [DFARS Subpart 234.2 — EVMS](https://www.acquisition.gov/dfars/subpart-234.2-earned-value-management-system) | The actual regulation and current thresholds. |
| [DoD Integrated Program Management policy and guidance](https://www.acq.osd.mil/asda/dpc/api/ipm/policy-guidance.html) | The EVMS Interpretation Guide, IPMDAR data item description, and implementation guidance. |

The one document to read if you read only one: the **NDIA IPMD EIA-748 Intent
Guide**. It is written to explain intent rather than to state rules, which makes
it the most useful thing in the field for someone learning the system.

Note that EIA-748 itself is a paid SAE standard. You do not need to buy it — the
Intent Guide covers every guideline with more explanation than the standard
provides.

## Sources

- [NDIA IPMD EIA-748 EVMS Intent Guide (Rev E, May 2026)](https://www.ndia.org/divisions/ipmd/division-guides-and-resources)
- [DFARS Subpart 234.2, Earned Value Management System](https://www.acquisition.gov/dfars/subpart-234.2-earned-value-management-system)
- [DAU EVM 101](https://icatalog.dau.edu/mobile/CourseDetails.aspx?id=1907)
- [DOE EVMS training](https://www.energy.gov/projectmanagement/evms-training)
- [CCAM, Earned Value Management Institute](https://www.evmi.com/ccam/)

Thresholds, guideline counts, and revision levels in this field change. The 27
guidelines above are EIA-748 Revision E; the thresholds are the February 2026
class deviation. Check both against current sources before quoting them in a
review.
