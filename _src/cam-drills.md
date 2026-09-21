# C2. CAM Interview and Variance Analysis Drill

A CAM interview is not a quiz. A government reviewer sits with you and your
control account data and asks you to explain your own numbers. They are testing
one thing: **do you actually manage this control account, or does someone else
manage it and you sign the reports?**

The tell is always the same. A CAM who manages their account answers from
knowledge and reaches for evidence to confirm. A CAM who does not answers by
reaching for the binder and reading.

## The twenty questions you will be asked

Answer each of these out loud before reading the guidance. If an answer takes
you more than about twenty seconds to begin, that is the gap.

### Scope and authorisation

**1. What is the scope of your control account?**
Describe the work in your own words, then point to the WBS dictionary entry and
the statement of work extract. Not a job title — a description of deliverables.

**2. How was this work authorised to you, and by whom?**
The work authorisation document, signed, with the date. Know that it exists and
where it is.

**3. Is any of the work in your control account not yet on contract?**
The honest answer is either "no" or "yes, this portion is authorised unpriced
work" — and if the latter, know the AUW and how it is budgeted.

**4. How do you know your scope is complete — that nothing is missing?**
The 100% rule, the RAM, and the reconciliation of your budget to the PMB. The
underlying question is whether you have unbudgeted work you are quietly
absorbing.

### Schedule

**5. Walk me through your schedule.**
Open the IMS extract. Show the logic, not just the bars. Name the predecessors
and successors that cross into other control accounts.

**6. What drives your critical path, and how much float do you have?**
If the answer is "I don't look at float", the interview is effectively over.

**7. Are there any constraints or date-locked tasks in your schedule?**
Hard constraints break network logic and are a standard finding. Know yours and
why they exist.

**8. How does your schedule connect to the ones around you?**
Interfaces and handoffs. A control account whose schedule has no external links
is a red flag — it means the integration is not modelled.

### Budget and earned value

**9. How is your budget time-phased, and by element of cost?**
Labour, material, subcontract, other direct, indirect. Know the shape.

**10. What earned value method does each work package use, and why?**
Be ready to defend every choice, and be especially ready to defend any LOE.

**11. What percentage of your control account is LOE?**
Know the number. Expect a follow-up asking why any specific item is LOE rather
than discrete.

**12. How do you take earned value each month — walk me through last month.**
The process, the evidence, who reviews it. "The analyst does it" is the wrong
answer, even when it is partly true. You own the assessment.

**13. Do you have any planning packages, and when do they convert?**
Rolling wave. Know the conversion dates and that the conversions are happening
on time — late conversions are a common finding.

### Performance and variances

**14. What are your current CV and SV, and what is driving them?**
Numbers first, then root cause. **Root cause is not "we spent more than planned"
— that is a restatement of the variance.** Root cause is *why*: a test rig was
unavailable for three weeks, a design change added rework, a supplier slipped, a
skill mix was richer than planned.

**15. What corrective action are you taking, and when will it show in the data?**
A corrective action with no date and no expected effect is not a corrective
action.

**16. What is your EAC, and what is it based on?**
Your bottom-up basis of estimate, and how it compares to the statistical
`BAC / CPI`. If the two diverge widely, you need a reason. "My EAC equals my BAC"
while running CPI 0.85 is the answer that triggers the hard follow-ups.

**17. Has your EAC changed since last month? Why?**
An EAC that never moves is not being maintained.

### Changes and risk

**18. Have you had any baseline changes? Walk me through one.**
The change, its authorisation, the date, and whether any of it touched work
already performed. Know that last part cold.

**19. Have you used management reserve? For what?**
In-scope unanticipated work, documented and authorised. Never to cover a
variance.

**20. What are the top risks to your control account, and what are you doing
about them?**
Specific risks with owners and responses, and how they connect to your EAC. A
risk that would blow your EAC and is not reflected in it is an inconsistency a
reviewer will find.

## Worked variance analysis

This is the core CAM skill. Do these three by hand before reading the answers.

### Case 1

> Control account 1.3.2, cumulative to date:
> BAC = $2,400,000 · PV = $900,000 · EV = $750,000 · AC = $880,000
> Variance thresholds: report any cumulative CV% or SV% beyond ±10%.

Work it:

- `CV = 750,000 − 880,000 = −$130,000`
- `CV% = −130,000 / 750,000 = −17.3%` → **over threshold, report required**
- `SV = 750,000 − 900,000 = −$150,000`
- `SV% = −150,000 / 900,000 = −16.7%` → **over threshold, report required**
- `CPI = 750,000 / 880,000 = 0.85`
- `SPI = 750,000 / 900,000 = 0.83`
- `% complete = 750,000 / 2,400,000 = 31.3%`
- `EAC (statistical) = 2,400,000 / 0.85 = $2,823,529`
- `VAC = 2,400,000 − 2,823,529 = −$423,529`
- `TCPI (to BAC) = (2,400,000 − 750,000) / (2,400,000 − 880,000) = 1,650,000 / 1,520,000 = 1.086`

**The reading.** Behind and overrunning together at 31% complete, which is early
enough that the trend is likely structural rather than a one-off. TCPI of 1.09
against demonstrated 0.85 means recovering to BAC requires a 28% improvement in
efficiency, sustained, for the remaining 69% of the work. That is not credible
without a specific, identified change in how the work is done.

**What a reviewer wants to hear:** the root cause, a corrective action with a
date, and an EAC that reflects reality rather than hope. If your EAC is still
$2.4M here, explain precisely what changes to make that achievable — or revise
it.

### Case 2

> BAC = $500,000 · PV = $400,000 · EV = $400,000 · AC = $470,000

- `SV = 0`, `SPI = 1.00` → on schedule
- `CV = −$70,000`, `CV% = −17.5%`, `CPI = 0.85` → significant overrun
- `EAC = 500,000 / 0.85 = $588,235`

**The reading.** On schedule, over cost. The work is getting done on time but
each unit costs more than planned. Typical causes: a richer labour mix than
budgeted, overtime to hold the schedule, material price increases, or rework.

**The follow-up you must anticipate:** "Are you buying your schedule with
overtime?" If the answer is yes, the reviewer will want to know what happens when
you cannot sustain it, and whether your EAC assumes the overtime continues.

### Case 3

> BAC = $1,000,000 · PV = $600,000 · EV = $700,000 · AC = $690,000
> The control account is 90% level of effort.

- `SV = +$100,000`, `SPI = 1.17` → apparently ahead
- `CV = +$10,000`, `CPI = 1.01` → marginally favourable

**The reading — and the trap.** These numbers look excellent and they are close
to meaningless. LOE work takes EV automatically as time passes, so it cannot
generate a schedule variance. A control account that is 90% LOE and showing
SPI 1.17 has that variance coming entirely from the 10% that is discrete, on a
small base, which makes it statistically noisy.

**The real finding is the 90% itself.** A reviewer will ask why this much of the
account is classified LOE, and whether discrete work has been misclassified to
avoid schedule visibility. Favourable variances get scrutinised too — sometimes
harder, because they are more often artefacts than achievements.

## Root cause, written properly

Variance analysis reports are graded on the quality of the root cause. The
pattern:

| Weak | Strong |
| --- | --- |
| "Costs exceeded budget." | "Integration testing required three additional weeks of senior engineering support because the vendor's interface did not match the ICD, driving 480 unplanned hours at a higher labour rate." |
| "We are behind schedule." | "The environmental test chamber was unavailable for four weeks due to a facility outage, delaying qualification testing that is a predecessor to two downstream work packages." |
| "We will work to recover." | "Two additional test engineers join in November; recovery of 60% of the schedule variance is expected by the January reporting period, with the remainder absorbed by resequencing WP 1.3.2.4." |

A complete variance analysis report has four parts, every time:

1. **What** the variance is — the numbers, current period and cumulative
2. **Why** — root cause, specific and singular where possible
3. **Impact** — on the control account, on downstream work, on the EAC
4. **Corrective action** — what, who, by when, and the expected effect on the data

## Ten self-test questions

Answers below each. Cover them.

**1.** A work package is 50/50 and has started but not finished. What is EV?
> Half the work package budget. No more, regardless of how complete it feels.

**2.** Cumulative SV is −$200,000. How many weeks late are you?
> Unanswerable from SV. Dollars are not time. Go to the IMS.

**3.** `CBB = $50M`, `MR = $3M`. What is the PMB?
> $47M. `PMB = CBB − MR`.

**4.** May management reserve be used to offset a cost overrun?
> No. In-scope unanticipated work only, documented and authorised.

**5.** A control account is running CPI 0.90 and the CAM's EAC equals BAC. What
will a reviewer ask?
> What specifically changes to deliver the remaining work at better than planned
> efficiency, given demonstrated performance below it. Without an answer, the EAC
> is not defensible.

**6.** What does TAB exceeding CBB mean?
> An over-target baseline is in effect: a formal, customer-approved reset because
> the original baseline became unachievable.

**7.** Why can LOE never show a schedule variance?
> EV is taken as time passes, so EV always equals PV by construction.

**8.** A CAM adjusts last month's EV downward to correct an error. Allowed?
> A documented correction of a genuine error, yes. Retroactive adjustment to
> reduce a reported variance, never. The distinction is documentation and intent,
> and reviewers look specifically for the second.

**9.** What is the difference between an IBR and an EVMS compliance review?
> The IBR asks whether the *baseline* is realistic and executable. A compliance
> review asks whether the *system* meets EIA-748.

**10.** `BAC = $1.2M`, `EV = $400K`, `AC = $500K`. What is the TCPI to BAC, and
what does it tell you?
> `(1,200,000 − 400,000) / (1,200,000 − 500,000) = 800,000 / 700,000 = 1.14`.
> You must run 14% better than plan on all remaining work, having so far run at
> `400/500 = 0.80`. The budget is not realistically recoverable.

## Preparing for the real interview

The week before:

- **Rehearse the twenty questions out loud.** Not in your head. The failure mode
  is hesitation, and hesitation only shows up when you speak.
- **Know three numbers cold:** your BAC, your cumulative CPI, and your EAC. Every
  conversation starts from those.
- **Have one clean example ready** of a variance you identified, root-caused, and
  corrected, with the data showing the correction working. This single story does
  more than any other preparation.
- **Reconcile your notebook to the system** the day before. A number in your
  binder that does not match the tool is the worst way to start.
- **Never guess.** "I don't know, I'll get that to you this afternoon" is an
  acceptable answer once or twice and is far better than a confident wrong
  number. Reviewers check.

The disposition that passes: you own this work, you know where it stands, you
know what is wrong with it, and you have a plan. Nobody expects a clean control
account. They expect a CAM who knows their own account's problems before the
reviewer does.

## Sources

- [NDIA IPMD guides: Intent Guide, IBR Guide, Surveillance Guide](https://www.ndia.org/divisions/ipmd/division-guides-and-resources)
- [DAU EVM 101 — Fundamentals of Earned Value Management](https://icatalog.dau.edu/mobile/CourseDetails.aspx?id=1907)
- [DOE EVMS training modules and videos](https://www.energy.gov/projectmanagement/evms-training)
- [DoD Integrated Program Management policy and guidance](https://www.acq.osd.mil/asda/dpc/api/ipm/policy-guidance.html)

Questions here are original, written against published guidance. Formula
conventions follow [C1](cam-evms.html) and [P5](pmp-predictive.html).
