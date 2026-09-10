# 16. Behavioral and expat questions

For this role, the behavioral rounds carry at least as much weight as the
technical ones. A dispersed team on a foreign assignment cannot absorb someone
who goes quiet, cannot disagree productively, or leaves at month eight. They
will probe for all three.

## 1. STAR, done well

**Situation** briefly, **Task** you owned, **Action** you personally took,
**Result** with a number where possible.

Three failure modes to avoid:

- **Spending three minutes on Situation.** Twenty seconds of context is enough.
- **Saying "we."** They are evaluating you, not your former team. "We decided"
  tells them nothing. "I proposed, and after pushback from the lead I adjusted
  to" tells them everything.
- **No result.** Every story ends with an outcome, and ideally a number: hours
  saved, defects prevented, a schedule met, a percentage.

Add a fourth beat that most candidates skip: **what you learned or would do
differently.** It signals self-awareness and it preempts the follow-up.

## 2. The six stories to write out in full

Write these as text, in advance, and read them aloud. Do not memorize them
word-for-word; memorize the beats. Each should run about two minutes.

**Story 1: A hard technical problem you solved.** Ideally a debugging story with
a non-obvious root cause. This is your credibility story. It should show method:
how you narrowed it, what you ruled out, how you confirmed the fix.

**Story 2: A time you disagreed with someone.** They are testing whether you can
hold a position without damaging the relationship. The best version ends with
either "I changed my mind when I saw their data" or "we ran a small experiment
to settle it." A version where you were simply right and everyone eventually
agreed is a weaker answer.

**Story 3: A time you failed, or shipped a defect.** Do not deflect and do not
choose a fake weakness. Own a real one, describe the impact honestly, and spend
most of the answer on what you changed afterward. Interviewers trust candidates
who can do this and distrust ones who cannot produce a real failure.

**Story 4: A time you delivered under a deadline or with incomplete
information.** Show how you decided what to cut and how you communicated the
tradeoff, rather than heroics.

**Story 5: A time you improved a process, a test suite, or a build.** This one
maps directly onto the posting. Automation, test coverage, pipeline speed, a
manual procedure you eliminated. Have the numbers.

**Story 6: A time you worked across a boundary.** With a different discipline, a
customer, a vendor, or a distant time zone. This is the one they will use to
predict how you do on this program specifically.

If your recent coding has been light, weight stories 5 and 6 heavily. They are
where senior judgment shows and they are less dependent on recent hands-on
volume.

## 3. Answering "you have not coded much lately"

If it comes up, and it may, do not apologize and do not oversell. A structure
that works:

> Most of the last [period] I have been [what you were doing], which kept me
> close to the systems but lighter on daily implementation. I knew that going
> into this process, so I have been deliberately rebuilding: I have been working
> through [specific thing you actually did], and I have [concrete artifact].
> What I did not lose is the part that took years to build, which is knowing
> what to test, where systems break in integration, and how to work a problem
> when the obvious explanation is wrong. The syntax comes back in weeks.

Two things make that answer land. It is **specific** about what you actually did
to prepare, so bring the practice repo and be able to describe it. And it
**reframes without dodging**: you concede the real gap and name the durable
skill, rather than pretending there is no gap.

Then make it true. Have something you built in the last two weeks that you can
talk about.

## 4. The questions you should expect

Prepare an answer for each. Say them out loud once.

1. Walk me through your background.
2. Why this role? Why Lockheed Martin? Why now?
3. What do you know about the program?
4. Tell me about the most technically challenging thing you have done.
5. Tell me about a production defect you caused.
6. Tell me about a time you disagreed with a technical decision.
7. How do you handle a requirement you think is wrong?
8. How do you approach code you did not write and that has no tests?
9. Describe your ideal code review.
10. How do you keep current technically?
11. Tell me about a time you had to learn something quickly.
12. How do you prioritize when everything is urgent?
13. Tell me about mentoring someone.
14. How do you work with people you never see in person?
15. What would your last team say is your weakness?
16. Where do you want to be in five years?
17. What questions do you have for us?

## 5. Answers worth pre-building

**"How do you handle a requirement you think is wrong?"**

> I start by assuming I am missing context, because on a system like this the
> requirement usually encodes something operational I have not seen. So I go to
> the systems engineer who owns it and ask what it is protecting against. Often
> that resolves it. If after that I still think it is wrong, I write up the
> specific concern with the consequence and a proposed alternative, and I raise
> it early, because a requirement change costs almost nothing in the analysis
> phase and a great deal after integration. Then whatever the decision is, I
> implement it properly. What I do not do is quietly implement something
> different from what was specified.

**"How do you prioritize when everything is urgent?"**

> I separate severity from urgency. Something that blocks other people comes
> first, because their idle time compounds. Then anything that affects the
> fielded system. Then the sprint commitment. And I make the tradeoff visible
> rather than absorbing it: if three things are asked of me in a sprint sized
> for two, that is a conversation with the product owner in week one, with my
> recommendation on which one slips.

**"Your ideal code review?"**

> Small enough to actually read, which for me means under about four hundred
> lines. Description says why, not what. Reviewer looks at error paths, edge
> cases, whether the tests would fail if the code were wrong, and whether a
> dependency was added. Comments distinguish blocking issues from preferences,
> because a reviewer who marks style opinions as blocking trains people to stop
> asking for review. And after two or three rounds of comments, take it to a
> call, especially with a time-zone gap where each round costs a day.

**"How do you keep current?"**

Be specific and honest. One or two sources you actually read, one thing you have
learned recently, and one thing you are curious about. Vague answers here are
worse than modest ones.

## 6. The expat conversation

Take this seriously. It is a substantial part of the decision, and the most
common reason a candidate with a strong technical showing does not get an offer.

### What they are worried about

That you will accept, relocate at considerable program expense, and leave within
a year because the reality did not match the idea. Expat turnover is expensive
and it disrupts a team that is already stretched across time zones.

### How to be convincing

**Be specific about why.** "I want to travel" is weak. Better: *"I have wanted
an overseas assignment for a long time and this one is the right combination: a
technical role rather than a management one, a program I find genuinely
interesting, and a location where my family and I have already talked through
what daily life would look like."*

**Show that you have done homework.** Know roughly where you would be based,
what the working week looks like (in the UAE the standard workweek is Monday to
Friday, with Friday commonly a half day, and the weekend is Saturday and
Sunday), that summer heat is extreme, and that the expat population is very
large so the practical infrastructure for it is well established.

**Have talked to your family.** Say so. If you have a partner or children, name
the specific questions you have worked through: schooling, whether a partner can
work, healthcare, how often you would travel home. A candidate who has clearly
had that conversation reads as low risk. A candidate who says "I would need to
discuss it with my wife" in the interview reads as not yet decided.

**Ask about the practicalities**, which also signals seriousness: housing
allowance and whether it is provided or reimbursed, schooling support, the trip
home allowance, tax equalization (the UAE has no personal income tax but US
citizens still file, and most large employers offer tax preparation support or
equalization), medical coverage and evacuation, the visa and residency process,
whether the assignment length is firm, and what happens at the end of the term.

**Be honest about the ties you have.** If you have a constraint, say it early. A
constraint disclosed in the first conversation is a logistics problem. The same
constraint discovered after an offer is a trust problem.

### Questions they may ask you

- Have you lived or worked abroad before? If yes, what was hard about it?
- What does your family think?
- What is your understanding of the assignment length?
- How do you expect to handle working with a team that is asleep for most of
  your day?
- What would make you want to come home early?

That last one deserves a genuine answer rather than "nothing." Something like:
*"A family health situation would bring me home, and I would tell you that the
day it happened rather than let it degrade quietly. Short of that, I have signed
up for the term."*

## 7. Compensation

Decide your number before the recruiter screen. For an expat assignment the
package has several components and the base salary is not the whole picture:

- Base salary.
- Any overseas or hardship premium.
- Housing allowance or provided housing.
- Cost-of-living adjustment.
- Education allowance for dependents.
- Home leave travel.
- Tax preparation or equalization.
- Relocation and shipment of household goods.
- Repatriation terms at the end of the assignment.

Two practical notes. Ask for the **total package in writing** and compare that
to your current total compensation, not base to base. And if pressed for a
number first, it is fine to say: *"For the base I am targeting the [X to Y]
range, and I would want to understand the full expat package before committing
to a number, since the components vary a lot between programs. What range is
budgeted for this role?"*

## 8. Questions to ask them

Ask three or four. Choose ones that show you understood the program.

**For the hiring manager:**

- What does the software team look like day to day, and how much of it is in the
  UAE versus the United States?
- What is the current state of automated test coverage on the baseline, and
  where would you want a new senior engineer to push first?
- How far along is the migration into the Software Factory pipelines, and what
  has been hardest about it?
- What does the integration lab cycle look like, and what is the turnaround from
  a code change to seeing it run against representative hardware?
- What would you want someone in this role to have accomplished by the end of
  the first six months?

**For engineers on the panel:**

- What surprised you most about the codebase when you joined?
- What is the most annoying part of the current development workflow?
- How does a defect found in the lab get back to a developer, and how long does
  that loop take?
- How much of the team's time goes to sustainment versus new capability?

**About the assignment:**

- How long have most people on the team been on assignment, and how many have
  extended?
- What does the onboarding look like for someone relocating?
- How is the overlap window with the US team handled in practice?

The question about the annoying part of the workflow is a good one: it gets you
an honest answer, it tells you what you would actually be walking into, and it
signals that you intend to fix things.

## 9. The close

If you want the job, say so at the end. Plainly, once:

> I want to be direct: this is the job I want. The combination of the
> modernization work and the overseas assignment is exactly what I was looking
> for, and I think the test and pipeline side is where I can contribute quickest.
> What are the next steps?

Candidates dramatically underestimate how much that matters, particularly for a
role where the employer is about to invest in relocating someone.
