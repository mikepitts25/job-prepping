# 17. Scenario answers

Scenario questions are the ones that start "what would you do if" or "walk me
through how you'd handle." They are the highest-signal part of a technical
interview for a sustainment role, because there is no memorized fact to recite
and the interviewer learns how you actually think.

Each answer below is written to be **said out loud in sixty to ninety seconds**.
Longer than that and you have stopped answering and started lecturing. Brackets
mark where you substitute your own specifics.

## How to answer any scenario question

Every good scenario answer has the same four beats, and once you internalize
them you can improvise one for a question you have never heard.

1. **Clarify or state assumptions.** One question or one sentence. "Is this the
   fielded site or the lab?" changes everything, and asking is a senior signal.
2. **Establish facts before acting.** Say what you would find out first, and in
   what order. Interviewers are listening for whether you diagnose or guess.
3. **Act, with the trade named.** What you would do, and what it costs.
4. **Close the loop.** How you prevent the recurrence, and who you tell.

Weak candidates jump straight to step three. The four-beat shape is most of
what separates a senior answer from a competent one.

Two habits that improve every answer:

- **Say what you would not do, and why.** "I would not push a fix straight to
  the site" is as informative as what you would do.
- **Name the person you would talk to.** Systems engineering, cyber, the
  integration lead, the product owner. This role is explicitly
  cross-disciplinary, and answers that never mention another human read as
  someone who works alone.

---

## Technical scenarios

### 1. "It works in the lab and fails in integration."

**What they are testing:** whether you have actually debugged a distributed
system, or only read about it. This is the most likely scenario question for
this role.

> First I would confirm the difference is real rather than assumed. Same build
> artifact in both places? I would check the checksum rather than the version
> label, because "same version" and "same bits" are different claims and the
> label is the one people get wrong.
>
> Then I would diff the three things that actually differ between environments.
> The environment: OS patch level, runtime version, library versions,
> environment variables, config files, locale, timezone, file permissions,
> whether the host is hardened. The data: integration sees real inputs, so
> bursts, duplicates, out-of-order timestamps, unexpected optional fields, and
> encodings the lab replay never produced. And the network: latency, MTU,
> multicast routing, name resolution, certificate trust.
>
> Rather than guess between those, I would raise observability in the failing
> environment. Debug logging on the suspect path, a packet capture if it is an
> interface problem, a thread dump or a stack sample at the moment of failure.
> I want evidence, not a theory.
>
> Then I would reduce to the smallest reproducer, and this is the part that
> matters: once I have it, it becomes an automated test, so this class of
> defect cannot come back silently. If it only reproduces with real data, I
> would capture that data as a replay fixture.
>
> What I would not do is start changing configuration in integration to see
> what helps. That destroys the evidence and you end up with a system that
> works and nobody knows why.

**Follow-ups to expect:** "What if you cannot reproduce it in the lab at all?"
(Answer: then the lab is not representative, and closing that gap is itself the
finding worth reporting.) "What if it is intermittent?" (Answer: capture
continuously and wait for it, rather than trying to trigger it; and treat
intermittent as a clue, usually timing, resource exhaustion or ordering.)

---

### 2. "A critical CVE lands in a library you use. What now?"

**What they are testing:** whether you treat security as engineering or as
paperwork. Near-certain for this posting.

> First, facts before reaction. Which exact version, in which components, in
> which baselines. If we have an SBOM that is a five-minute query; if we do not,
> that is a finding in itself. Then: is the vulnerable code path actually
> reachable from how we use the library, and what is our exposure? A
> deserialization flaw in a library we only use for formatting on an air-gapped
> subsystem is a different risk from the same CVE on an exposed interface. That
> determination gets documented and reviewed, not asserted to avoid work.
>
> I would also check whether it is on the known-exploited list or covered by a
> mandated remediation with a deadline, because that changes the conversation
> from "prioritize" to "required by this date."
>
> Then the response, in order of preference: upgrade to a fixed version;
> backport the patch if upgrading is blocked by a breaking change we cannot
> absorb this cycle, accepting that we now maintain a fork and documenting it;
> mitigate by configuration or a network control with the real fix scheduled;
> or accept with a plan of action and milestones if the risk is genuinely low
> and the fix genuinely expensive. That last one is a decision with a named
> owner and a date, not a way of ignoring it.
>
> Doing the upgrade properly means finding out whether it is direct or
> transitive, reading the changelog for **behavior** changes rather than just
> API changes, doing one dependency per merge request so a later lab finding
> maps to a small reversible commit, and running the full regression rather
> than the tests near the change.
>
> And then closing the loop: regenerate the SBOM, and if we learned about this
> from an external notice rather than our own pipeline, get continuous
> dependency scanning in so the next one is not a surprise.

**The sentence that lands:** *"A library four major versions behind is not
stable, it is accumulating an upgrade you will eventually be forced to do under
a deadline."*

---

### 3. "You need to change behavior in a 3,000-line class with no tests."

**What they are testing:** discipline on legacy code. This is the daily reality
of the job.

> I would not refactor first. First I would understand what it does and what
> depends on it, and read the change history, because on a fielded system the
> code usually looks that way for a reason someone had.
>
> Then I would get a net under it before touching anything: characterization
> tests. Not correctness tests, tests that pin what it does today, including
> the odd behaviors, because on an accredited system an odd behavior may be
> exactly what an operator depends on. Golden-file testing works well here.
> Capture the output for a set of representative inputs and assert it stays
> identical.
>
> With that in place I look for a seam, somewhere I can change behavior without
> editing the code in place: an interface, a constructor parameter, a factory.
> If there is no seam I introduce the smallest one that works.
>
> Then the change itself, small and reversible, and the refactoring in a
> separate commit from the behavior change so a reviewer can tell them apart and
> a revert is surgical.
>
> If one of my characterization tests legitimately has to change, that is not a
> nuisance, that is a conversation with the systems engineer about whether the
> old behavior was a requirement or an accident. That conversation is the
> valuable output.

---

### 4. "Migrate this legacy build into our pipeline."

**What they are testing:** exactly what the posting says you would be doing.

> I would start by making the existing build reproducible on a clean machine,
> before any pipeline work. That step alone usually surfaces the real problems:
> a tool at a fixed path, a network share, a license server, a compiler patch
> level, a dependency someone got on media from a vendor once. Until it builds
> from a clean checkout on a clean host, putting it in a pipeline just moves the
> mystery.
>
> Then one capability at a time, each merged and working before the next.
> First, green in the pipeline with tests skipped, so we have a reproducible
> build artifact. Then the tests that can be automated, and an honest inventory
> of the ones that cannot, because those need simulators, recorded data replay
> or hardware in the loop and that is its own project. Then static analysis and
> dependency scanning, with the existing findings baselined and new ones
> blocking, because if you gate on the whole legacy backlog the gate gets
> switched off within a week. Then artifact publishing with immutable tags. The
> deployment step last.
>
> Two things I would watch for on this kind of programme specifically. The
> hardened base images in the factory may be missing something the application
> assumes, and finding that out is engineering work, not a ticket for someone
> else. And in a controlled or air-gapped environment nothing comes from a
> public repository, so every dependency has to exist in the internal mirror
> first, which has its own lead time.
>
> The trap I would avoid is trying to do the whole migration as one change.
> That produces a six-week branch that conflicts with everything and cannot be
> reviewed.

---

### 5. "A defect is reported at the fielded site. You are on point."

**What they are testing:** operational judgment and restraint.

> The first question is impact: is the system degraded, is the mission thread
> affected, is there a workaround the operators can use right now. That decides
> the pace of everything else, and it is a conversation with the site and with
> whoever owns the operational relationship, not something I decide alone.
>
> Then I want evidence before theories. Logs around the event, the exact
> configuration and baseline version at the site, what changed recently, and
> whether it has happened before. On a fielded system "what changed" is the
> highest-yield question there is, and the answer is often something that was
> not a software change at all.
>
> I would try to reproduce in the lab with the site's configuration and, if
> possible, the site's recorded data. If it will not reproduce, the difference
> between lab and site is itself a finding.
>
> On the fix: I would want the root cause, not the symptom, and I would be very
> reluctant to ship anything to an accredited system without it going through
> the normal verification path. If the operational pressure is real, the
> conversation is about a temporary mitigation with a named risk, agreed with
> the customer, and the proper fix on the normal cycle. What I would not do is
> push a hot patch because someone is unhappy. That is how you turn one problem
> into two.
>
> And afterwards, a written record: what happened, why, what we changed, and
> what test now covers it. On a dispersed team, if that is not written down it
> did not happen.

---

### 6. "The service runs out of memory under a sensor burst."

**What they are testing:** whether you understand backpressure. This is a
domain-shaped question and a gift if you have read
[lesson 2](track-data.html).

> The most likely cause is an unbounded queue somewhere between a fast producer
> and a slower consumer. An unbounded queue is not a buffer, it is a deferred
> crash: it converts a temporary rate mismatch into an out-of-memory kill, and
> you lose everything in flight rather than the small amount you could have
> chosen to lose.
>
> So I would confirm that with evidence first, a heap histogram or a profile
> showing what is accumulating, rather than assuming.
>
> The fix is to bound the queue, which forces a deliberate policy choice: block
> the producer, drop the oldest, or drop the newest. For position reports,
> dropping the oldest is usually right, because a stale position has no
> operational value, and that is a decision I would want confirmed with systems
> engineering rather than made unilaterally, because it is arguably a
> behavioral change.
>
> And critically, count the drops and expose the counter. A system that
> silently discards data is worse than one that crashes, because the crash gets
> investigated and the silent loss does not. Then an alert on a nonzero drop
> rate.
>
> For the test: a burst test that drives the producer faster than the consumer
> and asserts both that memory stays bounded and that the drop counter is
> nonzero. That second assertion matters, because a test that only checks
> memory would pass on an implementation that quietly threw everything away.

There is a worked implementation of exactly this in the
[practice repo](../practice/README.html), in both Python and Java. Mentioning
that you have written one is fair and useful.

---

### 7. "Two sites disagree about the air picture."

**What they are testing:** domain reasoning. Very strong ground for you.

> I would want to know first whether they disagree about the **same** object or
> about **how many** objects there are, because those are different problems.
>
> If one object is showing as two tracks, the classic causes are sensor
> registration error, where the sites' contributing sensors have position,
> azimuth, range or timing biases that put the same aircraft in two places, and
> correlation failure across the link, where two participants are reporting the
> same object under different track numbers. The second is dual designation and
> there are network procedures for resolving it, including reporting
> responsibility deciding who owns the track.
>
> If they disagree about the state of one track, I would look at time first.
> Track positions are time-tagged and consumers extrapolate, so clock skew
> between sites shows up as position disagreement that grows with extrapolation
> interval. Then coordinate frame and altitude reference, because ellipsoidal
> height, mean sea level and barometric altitude are three different numbers
> and mixing them looks exactly like a tracking bug.
>
> How I would investigate: capture the link traffic at both sites and the
> internal state, align them on one timeline, and compare. If the reported data
> agrees and the displayed picture does not, the problem is downstream of the
> link; if the reported data already disagrees, it is upstream.
>
> I want to be clear that I would not be the one tuning the tracker. That is
> specialist work. What I would own is making the disagreement observable and
> reproducible, which is usually where the time goes anyway.

That last paragraph is important. It is honest, it shows you know the boundary
of your competence, and it identifies the part you genuinely could own.

---

### 8. "You have a baseline merge with hundreds of conflicts."

> I would do it in a scratch clone first, purely to see the scale and shape of
> the conflict set before committing to an approach, and I would get agreement
> on the merge direction before starting rather than after.
>
> Then I would take the conflicts in batches by subsystem rather than
> alphabetically by file, so I can hold the context for one area at a time. I
> would turn on the conflict style that shows the common ancestor, because
> seeing what each side actually changed is very different from seeing two
> final states and guessing.
>
> The rule I hold to is that I never resolve by taking one side wholesale to
> make the tool stop complaining. That is how a fix silently gets reverted and
> nobody finds out for a year. Where a conflict is not obviously mine, I go and
> find the author of both sides.
>
> Afterwards, the full regression suite, not the tests near my changes, because
> the risk in a baseline merge is exactly the interaction you did not think
> about. And the non-obvious resolutions get recorded in the merge commit
> message, so the next person can see the decision rather than reverse-engineer
> it.

---

### 9. "A flaky test is blocking the pipeline and the team wants to disable it."

**What they are testing:** whether you hold a quality line under pressure.

> I would push back on disabling it, but not by just saying no.
>
> The reason a flaky test is urgent rather than annoying is that it teaches the
> whole team to re-run the pipeline instead of reading the failure. Once that
> habit forms, the suite stops protecting anything, including for real
> failures. So one flaky test is a threat to the value of every other test.
>
> What I would do immediately is take it off the blocking path, but into a
> quarantine with a ticket, an owner and a deadline, not into deletion.
> Quarantine without a deadline is deletion with extra steps.
>
> Then find the actual cause, and it is usually one of a small set: dependence
> on wall clock or timing, shared state between tests, test order dependence,
> a real race in the code under test, or an external dependency that should
> have been faked. That last one is worth saying plainly: quite often the flaky
> test is correctly reporting a real intermittent bug, and disabling it means
> shipping that bug.
>
> What I would not accept is adding a retry and calling it fixed. A retry hides
> the signal and the underlying race stays in the product.

---

### 10. "Hardening the OS broke the application."

> First, this is expected, not surprising. A hardening baseline changes cipher
> suites, umask, mount options, permitted ports, service accounts and mandatory
> access control labels, and applications routinely depend on the previous
> defaults without knowing it.
>
> So I would find the specific control rather than treating it as a black box.
> If it is a mandatory access control denial, the audit log names it exactly. If
> it is cryptographic, the failure usually shows up as a handshake or an
> algorithm-unavailable error, and a common one is an application that assumed
> a legacy digest was available.
>
> Then I would fix the application to work within the control, not disable the
> control. On an accredited system that control exists because someone accepted
> a risk on the basis that it was there, and turning it off is not a decision an
> engineer gets to make alone. If the application genuinely cannot work within
> it, that is a documented conversation with cyber about a compensating control
> or an exception, with a rationale.
>
> The systemic fix, and this is the part I would push for: build and test
> against the hardened baseline in CI rather than a stock image. Otherwise you
> discover every one of these in the lab, which is the most expensive place to
> discover anything.

---

## People and process scenarios

### 11. "Security wants a library upgraded this sprint. It breaks an interface."

> First I would find out what kind of constraint the date actually is. A
> mandated remediation deadline and a prioritization request are different
> conversations, and people often say them the same way.
>
> Then I would size it honestly, including regression testing and the
> coordination with whoever consumes that interface, not just the code change.
> The temptation is to estimate the diff. The diff is rarely the cost.
>
> Then I would go back with options rather than a yes or a no, because "no" is
> almost never the useful answer. Something like: full upgrade next sprint with
> what that displaces; a backported patch now with the upgrade scheduled and
> the fork documented; or a compensating control now with an accepted plan and
> a date. Each with its cost and its residual risk.
>
> And I would do that in week one, not week three, with a recommendation
> attached. The failure mode on a dispersed team is discovering late that the
> commitment was never real, and by then you have spent the schedule and the
> credibility.
>
> If the interface is consumed by another programme, that is not a merge
> request, that is an interface change that goes through change control, and
> the lead time for that is the actual constraint.

---

### 12. "You are behind on your sprint commitment."

**What they are testing:** whether you go dark. They have been burned by this.

> The most important thing is when I say something, not what I say. As soon as
> I believe the commitment is at risk, which is usually well before it is
> provably at risk, I raise it. In standup and in the ticket, not in a private
> message, because on a dispersed team information in a direct message is
> information that is lost.
>
> What I bring is not just the problem. What is done, what is left, what my
> current estimate is, what I have already tried, and a recommendation: whether
> to descope, to get help, or to accept the slip. And I would say which one I
> think is right.
>
> If it is a technical blocker I would timebox my own investigation before
> asking, so I arrive with a specific question rather than "I am stuck," but I
> would keep that box small. Two hours of my own digging is diligence; two days
> is ego.
>
> And I would be honest about the cause in the retrospective, including if the
> cause was that I under-estimated it. Estimates only improve if the misses get
> discussed.

---

### 13. "Your blocker is with someone nine time zones away."

**Direct relevance to this job. They will ask something like this.**

> The structural answer is that I try never to be in that position at the end
> of my day, because a question asked at 17:00 in Abu Dhabi lands at the start
> of their day and comes back at the start of mine, and that is a full day per
> exchange. So the discipline is to look ahead: what will I need from the US
> team, and ask it early enough that the answer arrives before I need it.
>
> When I am blocked anyway, three things. I make it visible in the ticket and
> the board, not just in a message, so it is not dependent on one person seeing
> it. I ask the question in a form that can be answered asynchronously, with
> the context, what I already tried, and what I will do with each possible
> answer, so they can unblock me in one message rather than three. And I find
> something else useful to do rather than idling, then come back.
>
> I would also protect the overlap window and spend it on the things that
> genuinely need conversation, which is design disagreement, ambiguous
> requirements and live debugging. Status does not need a meeting.
>
> And before I sign off, I check that I have not left anyone on their side
> blocked on me. That is the reciprocal obligation and it is the one people
> forget.

---

### 14. "The customer asks you directly for something out of scope."

**Very likely for an in-country role, and directly in your experience.**

> This happens constantly on an in-country assignment, and the wrong answers
> are both easy: saying yes on the spot, or saying no on the spot.
>
> What I would do is take it seriously and take it down. Understand what they
> actually need, which is often different from the thing they asked for, and
> ask the questions that get at the operational reason. Then be clear and
> respectful about the process: this is a good question, it is outside the
> current scope, here is how a change gets considered, and I will make sure it
> reaches the right people.
>
> What I would not do is commit on behalf of the programme. Even a soft "we can
> probably do that" becomes an expectation, and on an FMS programme an
> expectation set informally is very expensive to walk back. The relationship
> is damaged more by a commitment that quietly does not happen than by a
> straight answer at the time.
>
> Then I would actually follow through internally and close the loop with them,
> whatever the answer is, because the thing that builds trust is not saying yes,
> it is that what you said would happen happens.

---

### 15. "A junior engineer's merge request is not good enough."

> In review, specifically, about the code, with reasons. Not "this is wrong,"
> but what breaks and under what input. I try to make the failing case concrete
> because a concrete case teaches and an opinion does not.
>
> I separate blocking issues from preferences explicitly, because a reviewer
> who marks style opinions as blocking trains people to dread review, and then
> you stop getting early reviews, which is when review is cheapest.
>
> If it is a pattern rather than one instance, that is a conversation, not
> twelve more comments. And privately, and framed as what I want them to be
> able to do rather than what they did wrong.
>
> If we are past two or three rounds of comments, I get on a call. On a
> dispersed team that saves a day per round, and tone survives voice much better
> than it survives text.
>
> The thing I try to remember is that the goal is a better engineer in six
> months, not a better merge request today. Rewriting it myself gets the second
> and prevents the first.

---

### 16. "You disagree with the technical approach the lead has chosen."

> I would first make sure I understand the reasoning, and specifically what
> constraint it is satisfying, because on a programme like this the constraint
> is often something I cannot see: an accreditation requirement, an interface
> commitment to another programme, a customer expectation, or a history where
> the obvious approach was tried and failed.
>
> If after that I still disagree, I would put the concern in writing, concretely:
> what I think happens, under what conditions, and what it costs, plus an
> alternative. Concrete beats general; "I think this will not scale" is
> ignorable and "at the rate in the requirement this queues faster than it
> drains, here is the arithmetic" is not.
>
> If I am overruled, I implement the decision properly and I do not relitigate
> it. I might ask that we agree on what evidence would cause us to revisit,
> which is a reasonable thing to ask and makes the disagreement productive
> rather than a grudge.
>
> The exception is safety, security or something I think puts the mission at
> risk. That is not a preference and I would escalate it, once, formally, and
> then accept the outcome of that.

---

## Practising these

Do not memorize the wording. Memorize the four beats, then rebuild each answer
in your own words, out loud, on a timer. If you can do that for these sixteen,
you can improvise a credible answer to a scenario you have never seen, which is
the actual goal.

A useful drill: take any scenario above, and have someone ask you the two
hardest follow-ups they can think of. Scenario answers are graded on the
follow-ups more than the first pass, because that is where a rehearsed answer
runs out and a real understanding keeps going.
