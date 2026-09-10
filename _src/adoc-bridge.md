# 14. Your ADOC bridge

You were product owner on the Qatar ADOC programme. That is a much stronger
hand than you seem to think it is, and it needs to be played deliberately
rather than mentioned in passing.

This lesson is about converting that experience into credible answers for a
hands-on software role, without claiming a single thing you did not do.

## 1. Why this is the strongest thing on your resume

Publicly, the Qatar Air and Missile Defense Operations Center is a Foreign
Military Sales programme, contracted through the US Air Force, to deliver an
integrated air and missile defense command and control capability for Qatar. It
integrates US air defense systems including Patriot, an early warning radar and
THAAD, alongside European air defense systems and radars, and connects to
Qatar's own Air Operations Center.

Now read the EADGE-T description again. Integrated air and missile defense and
air battle management for the UAE, connecting existing sensors and weapons
including THAAD and Patriot PAC-3, delivered as a foreign military sale, in the
Gulf.

| | Qatar ADOC | EADGE-T |
| --- | --- | --- |
| Mission | Integrated air and missile defense C2 | Integrated air and missile defense C2 |
| Customer | Gulf state ministry of defence, via FMS | Gulf state ministry of defence, via FMS |
| Integrates | Patriot, EWR, THAAD, European systems, national AOC | Patriot PAC-3, THAAD, existing sensors and weapons |
| Core problem | Making separately procured systems behave as one | Making separately procured systems behave as one |
| Region | GCC | GCC |
| Prime | Raytheon | Lockheed Martin |

**These are the same programme with a different prime and a different flag.**
Almost nobody who applies to EADGE-T has stood inside the customer-facing side
of a Gulf IAMD C2 delivery. You have. That is rare, it is directly relevant, and
it is not something a stronger coder can acquire in a year.

Your gap is recent hands-on software depth. Their gap, in most candidates, is
any understanding of what this customer, this contract vehicle and this
integration problem actually demand. You are trading in a market where your
scarce good is genuinely scarce.

**Two cautions before you use any of this.**

First, discuss your ADOC work **only at a level you know is releasable**. An FMS
programme carries classification, export control and foreign disclosure
constraints on top of ordinary proprietary sensitivity. Anything specific about
architecture, performance, deficiencies, schedule or customer positions is
almost certainly not yours to share with a competitor's hiring panel, and
Lockheed Martin is a competitor to Raytheon. The correct instinct is to speak
about **your role, your methods and your judgment**, in general terms, and to
say plainly when something is not discussable. Interviewers on defense
programmes read that as professionalism, not evasion. A candidate who
overshares about a competitor's programme is a candidate who will overshare
about theirs.

Second, do not let the parallel make you sound like you are applying to be a
product owner. You are applying for a hands-on senior software engineering
role. The domain background is your differentiator, not your job description.

## 2. The honesty rule

You said it yourself: you did not do a lot of software on ADOC. So do not imply
that you did. Not once, not by omission, not by a carefully ambiguous verb.

This matters for two reasons. The obvious one is integrity. The practical one
is that **it will not survive contact.** A technical interviewer who believes
you built the correlator will ask a correlator question, and the answer you
cannot give will cost you far more than the honest framing would have.

The framing that works is a **two-part sentence**, used consistently:

> "On ADOC I owned [the specific thing you owned] rather than writing the
> production code. What that gave me was [the durable capability], and what I
> am doing now to close the hands-on gap is [the specific, verifiable thing]."

Every scenario answer in this lesson uses that shape. It concedes the gap in
the first clause, which buys you credibility for the second and third.

The one thing that makes this framing work is that the third clause has to be
true. Before the interview, have something real: the
[practice repo](../practice/README.html) with your own commits in it, a small
tool you wrote, a certificate in progress, anything you can describe in
specifics. "I have been brushing up" is worthless. "I have been working through
a set of exercises I built around parsing and aggregation problems, and I have
54 tests passing against my own implementations" is worth a great deal, and
takes two weeks to make true.

## 3. Translating product owner work into engineering signal

A product owner on a programme like ADOC does a lot of things that map cleanly
onto what this role is graded on. The mapping is real, not a rhetorical trick.

| What you did as PO | What it demonstrates for this role |
| --- | --- |
| Wrote and groomed backlog items against a requirements baseline | You understand traceability from requirement to implementation to verification, which is the whole game on an accredited system |
| Defined acceptance criteria | You think in terms of verifiable behavior, which is exactly what a test is |
| Ran or attended defect triage | You know how severity and priority differ, and how a defect actually moves from a lab finding to a fix |
| Prioritized across capability, defects and technical debt | You have made the cost-of-delay argument to people who did not want to hear it |
| Sat between systems engineering, software, integration and cyber | The cross-discipline collaboration the posting explicitly asks for |
| Worked customer expectations in country | You know what an FMS customer needs to see, and how a demonstration lands |
| Made scope calls against a fixed delivery date | You have been accountable for a trade rather than commenting on one |
| Participated in sprint reviews and retrospectives | Real Agile experience, from the seat that has to say no |

None of those require you to have written the code. All of them are things a
strong senior engineer is expected to do well, and most engineers do them
poorly because they have never sat on the other side of the table.

**The line to have ready:**

> "I have spent three years being the person who had to decide what got built
> and what got deferred, with a customer waiting and a fixed date. That changes
> how you write software. I do not need to be told why a story needs acceptance
> criteria, or why a test that cannot fail is worthless, or why the schedule
> conversation has to happen in week one rather than week five."

## 4. Your ninety-second positioning statement

Rehearse this until it is smooth. It is the answer to "walk me through your
background," and to "why you," and it is the frame everything else hangs on.

> "My background is integrated air and missile defense command and control in
> the Gulf. Most recently I was product owner on the Qatar ADOC programme, so I
> have been on the customer-facing side of exactly this problem: taking
> separately procured sensors and effectors and making them behave as one
> system, under a foreign military sales contract, with a Gulf ministry of
> defence as the customer.
>
> What I owned there was the backlog and the acceptance side rather than the
> production code, and I want to be straight about that, because the role I am
> interviewing for is hands-on. My engineering background is [X years] in
> [languages and domains], and over the last [period] my day-to-day drifted
> away from implementation. I have been deliberately rebuilding that: [the
> specific thing you have done].
>
> What I think I bring that is hard to hire is that I already understand this
> customer, this contract structure, and this class of integration problem. I
> know what an FMS acceptance event feels like and what the customer needs to
> see. And I want the overseas assignment, which I have already done once with
> my eyes open.
>
> What I would want from you is a real ramp on the codebase, and I would expect
> to earn my way in through test coverage and defect work before I touch
> anything in the mission thread."

That last paragraph is the one that closes it. Asking for a ramp and proposing
to start on tests and defects is exactly right for this role, and it signals
that you are not going to arrive and immediately start redesigning things.

## 5. Six adaptable scenarios from your ADOC experience

Fill the brackets with your real specifics. Do not invent numbers; if you do
not remember a figure, use a truthful qualitative statement instead. "Several
sprints" is fine. A fabricated "37 percent" is not, and a follow-up question
will find it.

Each of these ends in software judgment, which is what makes it usable in a
technical interview rather than a management one.

---

### Scenario A: cross-discipline integration

**Use for:** "Tell me about working across disciplines." "Tell me about a time
you had to align people who disagreed."

> On ADOC the recurring hard problem was not any one subsystem, it was the
> seams between them. [Describe a specific instance in general terms: two
> subsystems whose interpretation of an interface differed, or a capability
> that needed systems, software and integration to agree before anyone could
> start.]
>
> What I did was get the disagreement out of email and into one artifact.
> [Describe: a working session, an interface note, a decision log, a
> demonstration.] The specific thing I insisted on was that we write down the
> expected behavior in terms someone could verify, not in terms of intent,
> because "the interface shall provide track data" is not something you can
> test and "for this input the output shall be these fields with these units at
> this rate" is.
>
> The result was [outcome]. What I took from it, and what I would bring here, is
> that most integration failures are agreement failures that surface late. The
> engineering fix is to make the agreement executable as early as possible: a
> contract test, a simulator, a recorded scenario both sides run. That is
> cheaper than the meeting, and it does not decay.

**Why it works:** the action is genuinely PO-shaped, and the lesson lands on
contract testing, which is a software answer.

---

### Scenario B: prioritizing under a fixed date

**Use for:** "How do you prioritize?" "Tell me about a hard trade-off."
"A time you delivered under pressure."

> As product owner I had [describe the constraint: a delivery event, an
> acceptance milestone, a fixed customer date] and more scope than the team
> could complete. [Describe the specific competing items.]
>
> The way I worked it was to separate what the customer would actually
> demonstrate from what the team wanted to finish, and then to be explicit
> about what deferring each item cost. [Describe what you deferred and why.]
> The one thing I refused to trade was [the thing you protected, e.g. the
> verification evidence, or a defect affecting the mission thread], because
> [reason].
>
> I took it to [stakeholders] in [when: early], with a recommendation rather
> than a menu, and the decision was [outcome].
>
> The part relevant to this role is that the technical debt we deferred was
> written down as debt, with a named owner and a target release, rather than
> quietly absorbed. On a sustainment programme, undocumented deferrals are how
> a baseline becomes unmaintainable ten years later.

**Why it works:** ends on technical debt management, which is a sustainment
concern and precisely this job.

---

### Scenario C: defect triage and the lab bottleneck

**Use for:** "Tell me about a defect." "How do you decide what to fix?"
"A time you improved a process."

> On ADOC the constrained resource was [the lab / the integration environment /
> the customer test window]. Defects came out of [where they came from] and
> everything competed for the same slot.
>
> The pattern I kept seeing was [describe honestly: e.g. issues that only
> appeared in the integrated environment, or defects that turned out to be
> configuration or environment differences rather than code]. [Describe what
> you did about it: how you changed triage, what you asked the team to capture
> before a lab run, how you got repeat offenders separated from genuinely new
> findings.]
>
> The outcome was [outcome].
>
> The engineering conclusion I drew, and it is why this specific job interests
> me, is that lab time is the scarce resource on a programme like this, and
> every defect you can catch before the lab is a slot you get back. That is the
> economic argument for automated test coverage, and it is a much better
> argument than test coverage as hygiene. When the posting talks about
> automated test capability improving deployment efficiency, that is what I
> think it means.

**Why it works:** this connects your real experience to the single most
important theme in the job posting. This may be the best story you have.

---

### Scenario D: a requirement that was wrong, or ambiguous

**Use for:** "How do you handle a requirement you disagree with?" "Tell me
about a time you pushed back."

> [Describe an instance where a requirement, as written, was ambiguous or would
> not have produced the operational outcome intended. Keep it general.]
>
> My first move was to assume I was missing context, because on this kind of
> system a requirement usually encodes something operational that is not
> obvious from the text. So I went to [who] and asked what the requirement was
> protecting against. [What you found out.]
>
> [If it was genuinely wrong:] I wrote up the specific concern, the consequence
> if we built it as written, and a proposed alternative, and raised it at
> [when, early]. The decision was [outcome], and I implemented the decision
> either way.
>
> What I would carry into an engineering role is that ambiguity in a
> requirement is cheap to fix at the analysis stage and extremely expensive
> after integration. So when I read a story now, the question I ask is "how
> would I verify this," and if I cannot answer that, the requirement is not
> done yet regardless of how it reads.

---

### Scenario E: the customer relationship

**Use for:** "Tell me about working with a difficult stakeholder." "What is
different about an FMS customer?" "Why do you want an overseas assignment?"

> Working with a Gulf ministry of defence customer is different from a
> commercial stakeholder in ways that took me time to learn. [Describe what you
> learned, in general and respectful terms. Good honest themes: the importance
> of the relationship and of face-to-face presence; that commitments are held
> to precisely; that a demonstration carries more weight than a status report;
> that the customer's own organizational realities shape what they can accept
> and when; that patience and consistency compound.]
>
> The concrete thing I changed in how I worked was [something specific: how you
> prepared for reviews, how you handled bad news, how you built the
> relationship outside the formal events].
>
> That is a large part of why I want this assignment specifically rather than a
> domestic role. I have already done the version of this where you are in
> country, in the region, working with the customer directly, and I know what
> it costs and what it gives back.

**Why it works:** it makes your expat willingness credible in a way no amount
of enthusiasm can. You have done it. Say so.

---

### Scenario F: the honest one about the software gap

**Use for:** "Why are you moving from product owner back to engineering?"
"Are you not overqualified / underqualified for this?" "Tell me about a
weakness."

> I moved into the product owner role because [true reason]. I learned a great
> deal from it, particularly [what]. But the part of the work I actually want
> to be doing is building the thing, and on ADOC I was increasingly the person
> describing what should be built and then watching someone else have the
> interesting problem.
>
> I am clear-eyed that this is a step back toward hands-on work and that my
> implementation muscle needs rebuilding. That is why I am applying for a
> senior engineer role rather than a lead or a manager role. [Then the specific
> preparation you have done.]
>
> What I do not think I have lost is the judgment: knowing what to test,
> knowing where these systems break at the seams, knowing when a schedule
> commitment is not real. Syntax comes back in weeks. That took years.

**Why it works:** it answers the question they are definitely thinking about,
before they have to ask it awkwardly. Volunteering it is a strength move.
Waiting for them to dig it out is not.

---

## 6. Handling the objection directly

If someone says, in effect, *"this is a hands-on coding role and your recent
experience is product ownership"* — that is not a rejection, it is an invitation
to resolve their concern. Answer it head on:

> "That is the right question to ask and I would ask it too. Let me answer it
> in three parts.
>
> First, the honest scope: on ADOC I owned the backlog and acceptance, not the
> production code. My hands-on background is [X], and it has been [period]
> since I was writing production software daily.
>
> Second, what I have done about it: [specific preparation, with an artifact].
> I am not asking you to take the ramp on faith; give me the coding exercise and
> judge it.
>
> Third, what you get that is hard to hire: I already know this mission, this
> customer, this contract structure and this class of integration problem, and
> I have already done an overseas assignment in the region. If you hire a
> stronger coder without that, you spend a year teaching them the domain and
> you carry the risk that the assignment does not suit them.
>
> Where I would expect to start is test coverage and defect work, because that
> is where I can be useful immediately while I learn the baseline properly."

That answer is confident without being defensive, it concedes the real gap, and
it puts the decision back on the evidence.

## 7. Prepare this before the interview

Sit down for an hour and write out, from memory, what you actually know. You
will be surprised how much there is, and the recall is much harder cold.

**About the programme (only what is publicly releasable, at your own judgment):**

- What the system was for, in one sentence, at an unclassified level.
- The disciplines on the team and roughly how they were organized.
- The development process: sprint length, ceremonies, tooling, how a
  requirement became a story became a verified capability.
- The delivery rhythm: how often a build went to the lab, how a customer event
  worked.

**About your role:**

- Team size, your reporting line, how many sprints, over how long.
- Concrete artifacts you produced: how many stories, epics, acceptance criteria.
- Decisions you personally made, with the trade you accepted.
- Two things that went well because of something you did.
- Two things that went badly and what you changed.

**About the technology you were exposed to, honestly labelled:**

Make three columns: **used hands-on**, **worked alongside and understand**,
**heard of only**. Be strict about the boundaries. Then in the interview, use
the right verb for the right column. That discipline is what lets you speak
confidently about column two without anyone thinking you claimed column one.

**About the gap:**

- The last time you wrote production code, and in what.
- What you have done in the last month, specifically.
- What you would want in a ramp.

## 8. Landmines

- **Do not disclose competitor-sensitive or controlled information.** Covered
  above; it is the most important item here. If in doubt, do not.
- **Do not criticize Raytheon, the programme, or former colleagues.** Even mild
  criticism of a former programme reads as a preview of how you will talk about
  theirs. If asked about difficulties, keep it structural and impersonal.
- **Do not present yourself as a product owner looking for a PO role.** They
  are hiring an engineer. If you would genuinely rather have the PO role, that
  is a different application, and you should decide which one you want before
  the screen.
- **Do not imply the two programmes are interchangeable in detail.** They have
  different primes, architectures and histories. The parallel is at the mission
  and problem level, and that is where you should keep it. Overreaching here
  reads as someone who does not understand how different two systems with the
  same mission can be.
- **Do not oversell the region knowledge to people who live there.** Some of
  your panel will have been in the Gulf longer than you were. Offer it as
  relevant experience, not expertise.

## 9. Questions to ask that use your background

These land differently coming from you than from a candidate without the
history, and they will notice that.

- "How is the systems-to-software handoff structured here? On the programme I
  came from, the seam between the requirements baseline and the sprint backlog
  was where most of our friction lived, and I am curious how you handle it."
- "How much of the team's capacity goes to defect and sustainment work versus
  new capability, and who arbitrates that?"
- "What does a customer acceptance event look like on this programme, and how
  much of the evidence for it is generated automatically today?"
- "Lab access from the UAE side: what is the cycle time from a code change to
  seeing it run against representative hardware?"
- "Where does the team feel the tech refresh is riskiest? I would rather know
  now."

The acceptance-evidence question is the best one in the list. It is a product
owner's question asked in an engineer's terms, it goes straight to the automated
test capability the posting is about, and only someone who has been through a
customer acceptance event would think to ask it.

## Sources

Public reporting on the Qatar programme, for the parallel described in section
1:

- [Raytheon awarded contract to provide the State of Qatar with advanced IAMD command and control system](https://raytheon.mediaroom.com/2014-12-01-Raytheon-awarded-contract-to-provide-the-State-of-Qatar-with-Advanced-Integrated-Air-and-Missile-Defense-IAMD-Command-and-Control-System)
- [Raytheon to create air and missile defence operation centre for Qatar (Airforce Technology)](https://www.airforce-technology.com/news/newsraytheon-to-create-air-and-missile-defence-operation-centre-for-qatar-4457151/)
- [Qatar moves one step closer to receiving U.S. Air and Missile Defense Operations Center (Hanscom AFB)](https://www.hanscom.af.mil/News/Article-Display/Article/846889/qatar-moves-one-step-closer-to-receiving-us-air-and-missile-defense-operations/)
- [Raytheon awarded Qatar ADOC FMS contract (Shephard Media)](https://www.shephardmedia.com/news/digital-battlespace/raytheon-awarded-qatar-adoc-fms-contract/)
