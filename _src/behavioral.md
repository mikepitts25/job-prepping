# 24. Behavioral and expat questions

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

## 6. The expat conversation, when you are already overseas

Take this seriously. It is a substantial part of the decision, and normally the
most common reason a strong technical candidate does not get an offer.

**Your position is unusual, and it is an advantage.** This section is written
for someone who is already living and working outside the United States and
intends to stay there. If that is you, most of the standard expat advice is
aimed at the wrong problem, and following it will make you sound like a
candidate you are not.

### What they are normally worried about, and why it does not apply to you

The usual fear is that a candidate accepts, relocates at considerable programme
expense, discovers the reality does not match the idea, and leaves within a
year. Expat turnover is expensive, it disrupts a team already stretched across
time zones, and it means starting the search again.

Almost none of that risk is present with you. You already live overseas. You
have already done a Gulf assignment. Your family arrangements already work
outside the United States. You are not being persuaded into anything, and there
is no moment eighteen months in where the novelty wears off and you want to go
home, because this **is** home for now.

**Say that explicitly.** It is not visible on a resume and the recruiter will
not infer it. Something like:

> "One thing worth putting on the table early: I am already based in the Gulf
> and intend to stay in the region. So the usual expat risk, somebody relocating
> from the States and finding it is not for them, is not a risk with me. I have
> already done the adjustment, and my family is already set up for life
> overseas."

That is a genuinely strong opening and very few candidates can say it.

### The trap to avoid

There is one way this can work against you. If your motivation reads as *"I
need a job that keeps me overseas and this is one,"* it undercuts everything
else, because it says you would take any role that met the geography.

**Lead with the work. Use the location as the thing that de-risks you, never as
the reason you applied.** The order matters:

> "I applied because of what the work is: modernising a fielded IAMD command and
> control system without disturbing the mission behaviour, on a foreign military
> sales programme with a Gulf customer. That is the exact problem I spent the
> last few years on from the customer-facing side, and I want to be building it
> rather than describing it. The fact that I am already in the region and want
> to stay is a practical bonus for both of us rather than the reason I am here."

### Why you are leaving your current situation

They will ask. This is the question where an already-overseas candidate can
sound unstable if the answer is thin.

Answer toward something, never away from something. Good shapes:

- The work you want to do next is hands-on engineering, and your current role or
  location does not offer it.
- The programme is a closer match to your background than what you are doing now.
- A natural end point: a contract concluding, a delivery phase completing, an
  assignment term finishing.

Avoid anything that reads as dissatisfaction with a current employer or
customer. And do not let it sound like the current situation is collapsing under
you, because urgency reads as weak negotiating position at best and as a problem
you are outrunning at worst.

### Disclosing the constraint

You need to stay outside the United States for family reasons. Disclose the
shape of that early, without the detail.

**A constraint disclosed in the first conversation is a logistics problem. The
same constraint discovered after an offer is a trust problem.** That rule has
not changed. What has changed is that in your case the constraint largely
aligns with what the role wants, so it costs you very little to say:

> "For family reasons I need to remain outside the US for the foreseeable
> future, which is part of why an expat assignment suits me rather than being
> something I have to be talked into. Is there any part of the onboarding or
> clearance process that would require me to be stateside?"

That phrasing does two things at once: it discloses, and it asks the single most
important logistics question in your process.

### The four questions to get answered before you invest further

Ask these of the recruiter early, ideally on the first screen. Any one of them
could make the role unworkable, and you want to know now rather than after an
offer.

1. **Does any part of onboarding, training or processing require me to be in
   the United States, and for how long?** Some prime "expat" roles are
   structured as hire into a US entity, then deploy. That can mean weeks or
   months stateside up front.
2. **Can the clearance investigation proceed while I remain overseas?** The
   requirement here is the *ability to obtain* a Secret clearance, and sponsorship
   is normal, but fingerprinting and the subject interview have practical
   logistics that are easier stateside. Ask how they have handled it for others.
3. **Is this an expatriate package or a local hire?** See the note in section 7.
   The difference is very large and it is not always stated in the posting.
4. **What does the mobilisation look like from where I am?** Moving from one
   Gulf country to another is still a move: visas, residency, shipping, schools,
   and an exit process from your current residency. Ask who handles it and on
   what timeline.

### Questions they will ask you

These differ from the standard expat set, because several of the usual ones are
already answered.

- **How long have you been in the region, and what made you stay?** Have a
  genuine answer. It establishes that you are settled rather than drifting.
- **What has been hard about living overseas?** Do not say "nothing." A real
  answer, distance from family, healthcare logistics, the summer, the
  bureaucracy, is credible and shows you are clear-eyed. Follow it with what you
  do about it.
- **Are you willing to move country within the region?** If the role is in the
  UAE and you are in Qatar, that is still a relocation. Be ready with a real
  answer about timing and what it involves.
- **What is your current visa and residency status, and what is your notice
  period?** Know these precisely.
- **How do you handle working with a team that is asleep for most of your day?**
  Answer from experience, per [lesson 18](git-agile.html) section 9.
- **What would make you leave the assignment early?** The honest answer is no
  longer "I would go home," because you are not going home. Something like:
  *"A family health situation would move me, and I would tell you the day it
  happened rather than let it degrade quietly. Short of that, I have signed up
  for the term, and unlike most people taking an expat assignment I am not
  weighing it against a life back in the States."*

### Do not oversell the region to people who live there

Some of your panel will have been in the Gulf longer than you have. Offer your
experience as relevant background, not as expertise, and never as advice about
their own home. Confidence here is fine; teaching is not.

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

**The fork that matters most for you: expatriate package or local hire.** These
are different products and the posting will not always say which it is. An
expatriate assignment carries housing, schooling, home leave and often tax
equalisation on top of base. A local contract with a regional employer carries
none of that and is priced against the local market. The same base number means
very different things, and a candidate already resident in the region is
sometimes offered the local version by default. Ask which it is before you
discuss any number.

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
