# 17. Mock interview bank

Work these under time pressure. Cover the answer, say yours out loud, then
compare. Answering silently in your head is not practice.

---

## Round 1: Recruiter screen (10 questions)

**1. Walk me through your background in two minutes.**
Chronological but compressed, ending pointed at this role. Last position gets
half the time; anything more than ten years back gets a clause.

**2. Are you a US citizen and what is your clearance status?**
Precise facts. Level, granting agency if you know it, date of last
investigation, whether it is current or would need reinstatement.

**3. Are you genuinely willing to relocate to the UAE for two to three years?**
Yes, plus one specific sentence about why and one about having discussed it with
family. See [lesson 15](behavioral.html).

**4. Why are you looking to leave your current role?**
Toward something, never away from someone. Never criticize a current employer.

**5. What are your compensation expectations?**
A range with a rationale, plus a request to understand the full expat package.

**6. When could you start?**
A real date allowing a proper notice period. Do not offer to leave immediately;
it reads badly.

**7. Have you interviewed with Lockheed Martin before?**
Just answer.

**8. What do you know about the position?**
Thirty seconds: EADGE-T tech refresh, software modernization, COTS/FOSS updates,
Software Factory migration, test automation, Agile team, UAE assignment.

**9. Do you have any travel or availability constraints?**
Disclose real constraints now.

**10. Do you have questions for me?**
Ask about the process, the timeline, the number of rounds, and who you will
meet.

---

## Round 2: Hiring manager (18 questions)

**11. Tell me about the most technically challenging project you have worked
on.** Story 1. Make the difficulty concrete, and describe method rather than
heroics.

**12. Why this program specifically?**
Cite the actual work: modernizing a fielded, accredited baseline without
changing mission behavior, and the fact that the test-automation work is the
enabler for the rest.

**13. What do you understand about EADGE-T?**
The three-minute summary from [lesson 1](program-brief.html), compressed to
one minute unless they want more.

**14. What is your experience with sustainment versus new development?**
Both if you have both. If mostly new development, name what transfers:
disciplined change control, testing before refactoring, and reading unfamiliar
code.

**15. How would you approach your first ninety days here?**
> Thirty days reading: the architecture, the build, the test suite, the defect
> backlog and the last few post-mortems, plus getting my own environment
> building and testing end to end. I would take a small defect early to exercise
> the whole path from ticket to lab. By sixty days I would want to have shipped
> something real and formed a view on where automated testing pays back
> fastest. By ninety I would want a concrete proposal for one improvement, sized
> and agreed, rather than a list of criticisms.

**16. Tell me about a time you improved a team's engineering practice.**
Story 5, with numbers.

**17. How do you handle competing priorities?**
[Lesson 15](behavioral.html), section 5.

**18. Tell me about a time you disagreed with a decision.**
Story 2.

**19. Describe a mistake that reached production.**
Story 3. Own it, quantify impact, spend the time on the systemic fix.

**20. How do you mentor junior engineers?**
Concrete: what you actually did, and what changed for them. Code review as
teaching, pairing on the hard part not the whole task, and letting them be
wrong safely.

**21. What is your experience with Agile?**
Real specifics: team size, sprint length, your role in ceremonies, what worked
and what did not. Mention the Scrum-plus-Kanban-lane hybrid for defect work if
you have used it.

**22. What is your Python versus Java split?**
Honest. Then say which you would pick for a live exercise.

**23. How do you decide when to refactor?**
> When I am about to change code and the current structure makes the change
> risky. I refactor to make the change easy, then make the change, in separate
> commits. I do not refactor code I am not otherwise touching, because on an
> accredited baseline every diff carries a verification cost.

**24. What is your experience with CI/CD?**
Be specific about the tools and what you built. If you have not built a pipeline
from scratch, say what you have maintained and what you understand about
pipeline design.

**25. How do you deal with an unresponsive teammate in another time zone?**
Escalate the work item, not the person. Make the blocker visible in the ticket
and the standup, offer a specific overlap slot, and if it repeats, one direct
private conversation before involving a lead.

**26. What kind of work do you not want to do?**
Answer honestly but constructively. Do not say "documentation" or "maintenance"
in an interview for a sustainment role.

**27. Where do you want to be in five years?**
Something that is consistent with staying through the assignment.

**28. What is your weakness?**
A real one, with the compensating mechanism you have built. Not a virtue in
disguise.

---

## Round 3: Coding (12 problems)

Do each in 20&ndash;25 minutes, narrating. Reference solutions in the
[practice repo](../practice/README.html).

**29.** Parse `sensor,timestamp,confidence` lines; return the sensor with the
highest average confidence, ignoring malformed lines.
*Watch for: empty input, division by zero, ties, non-numeric confidence.*

**30.** Find the first non-repeating character in a string.
*Say that Python dicts preserve insertion order, so one Counter pass plus one
scan is enough.*

**31.** Merge overlapping intervals.
*Sort first. State that it is O(n log n) dominated by the sort.*

**32.** Given a log file, count occurrences of each log level per hour, without
loading the file into memory.
*Generator plus nested defaultdict. Mention the malformed-line policy.*

**33.** Implement a fixed-size ring buffer with `push` and `latest(k)`.
*`collections.deque(maxlen=n)`. Discuss what happens on overflow and why
dropping the oldest is right for sensor data.*

**34.** Two sum, then follow-up: what if the list is sorted? What if you need
all pairs?
*Hash map for the general case; two pointers when sorted; watch for duplicate
handling in the all-pairs version.*

**35.** Detect out-of-order timestamps in a stream and report how far each went
backwards.
*One pass, keep the running max. Ask whether equal timestamps count.*

**36.** Compare two semantic version strings correctly.
*Split on dots, compare integer-wise, handle differing lengths, and explain that
string comparison puts "1.10" before "1.9".*

**37.** Diff two nested dictionaries: added, removed, changed.
*Recursion. Decide up front how you represent a value that changed type, and
how you handle lists.*

**38.** Implement a per-client rate limiter allowing n calls per rolling
sixty seconds.
*Deque of timestamps per client, evict from the front. Then discuss unbounded
client growth and how you would bound it.*

**39.** Top k most frequent elements.
*Counter plus heap, O(n log k). Mention `Counter.most_common` and that you would
use it in real code.*

**40.** Given a service dependency graph, produce a valid startup order or
detect a cycle.
*Kahn's algorithm. Note that this is the same problem as build ordering.*

---

## Round 4: Python depth (12 questions)

**41. List vs tuple?** Mutability, hashability, intent.

**42. How does a dict work and what is its complexity?** Hash table, average
O(1), insertion-ordered since 3.7 as a guarantee.

**43. Mutable default argument. What is wrong here?** Evaluated once at function
definition. Use `None`.

**44. Shallow vs deep copy?** Container vs recursive.

**45. What is the GIL and when does it matter?** One thread executes bytecode at
a time. Threads for I/O, processes for CPU.

**46. Generator vs list?** Lazy, constant memory, single pass, not indexable.

**47. What is a decorator? Write one.** Retry with backoff, using
`functools.wraps`.

**48. What is a context manager? Write one.** `__enter__`/`__exit__`, or
`@contextmanager` with try/finally.

**49. `is` vs `==`?** Identity vs value.

**50. How do you manage dependencies?** Virtual environment, pinned versions,
lockfile, and why reproducibility is a configuration-management requirement
here.

**51. How do you find a performance problem?** `cProfile` to locate, `timeit` to
measure a fix, measure before and after, never optimize by intuition.

**52. What is `__slots__` and when would you use it?** Fixed attribute set, no
per-instance dict, saves memory across millions of small objects.

---

## Round 5: Java depth (12 questions)

**53. `==` vs `.equals()`?** Reference vs value.

**54. Why must equals and hashCode be consistent?** Otherwise objects vanish in
hash-based collections. Base both on the same immutable fields.

**55. `ArrayList` vs `LinkedList`?** Almost always ArrayList; cache locality;
LinkedList's O(1) insert needs the node in hand.

**56. `HashMap` vs `TreeMap` vs `LinkedHashMap`?** O(1) unordered, O(log n)
sorted with range queries, insertion or access order.

**57. Checked vs unchecked exceptions?** Recoverable and declared, versus
programming errors.

**58. `volatile` vs `synchronized`?** Visibility versus mutual exclusion plus
visibility. `volatile` does not make `count++` atomic.

**59. How do you make a class thread-safe?** Immutability first, then
confinement, then locks. Records help.

**60. What is a deadlock and how do you prevent it?** Circular lock acquisition;
consistent global lock ordering, or timeouts.

**61. Streams: lazy or eager?** Lazy until a terminal operation, single-use.

**62. How does GC work?** Generational, most objects die young, collectors G1,
ZGC, Shenandoah.

**63. Can Java leak memory?** Yes, as unintended retention: static collections,
unregistered listeners, ThreadLocals on pooled threads, unbounded caches.

**64. How do you diagnose a hung Java process?** Two thread dumps ten seconds
apart via `jstack`, look for BLOCKED threads and the lock owners.

---

## Round 6: Linux and troubleshooting (10 questions)

**65. Find all files over 100 MB modified in the last week.**
`find /path -type f -size +100M -mtime -7`

**66. What is using all the disk?**
`df -h`, then `du -xh --max-depth=2 | sort -h`, then `lsof +L1` for deleted
files still held open.

**67. A service will not start. Walk me through it.**
[Lesson 8](linux.html), section 10, in that order.

**68. What does load average mean?**
Runnable plus uninterruptible-sleep processes, averaged. Compare to core count.
High load with low CPU means I/O wait.

**69. How do you see what is listening on a port?**
`ss -tulpn` or `lsof -i :8080`.

**70. What does `chmod 750` mean?**
Owner rwx, group rx, other none.

**71. What is SELinux and what do you do about a denial?**
Mandatory access control. Read the AVC denial with `ausearch`, fix the label
with `restorecon` or add a policy module. Do not set permissive.

**72. Explain `set -euo pipefail`.**
Exit on error, error on unset variable, fail a pipeline on any stage.

**73. A process is at 100% CPU. What do you do?**
`top` to identify, then language-specific profiling: thread dump for Java,
`py-spy` for Python. Check log level and any hot loop with a missing sleep.

**74. It works in the lab and fails in integration.**
[Lesson 8](linux.html), section 10. This is the high-value one; rehearse it.

---

## Round 7: Testing, CI/CD, containers (16 questions)

**75. What makes a good unit test?** FIRST, one reason to fail, would actually
fail if the code were wrong.

**76. Unit vs integration test?** Logic and edge cases vs wiring and external
assumptions.

**77. How do you test legacy code with no tests?** Characterization tests, find
a seam, inject, then refactor.

**78. Mock vs stub vs fake?** [Lesson 10](testing-ci.html), section 4. Say you
prefer fakes and why.

**79. How do you test time-dependent code?** Inject the clock. Use monotonic
time for durations.

**80. A test is flaky. What do you do?** Treat it as urgent, quarantine with a
ticket and a deadline, root-cause it. Never add a retry as the fix.

**81. How much coverage is enough?** Detector of gaps, not a measure of quality.
Branch coverage over line coverage. Floor that must not regress.

**82. What stages belong in a pipeline?** Lint, unit, package, integration,
scan, publish, deploy. Fast feedback first.

**83. Why build the artifact only once?** So the thing you tested is the thing
you ship. Rebuilding between test and deploy means you shipped something
untested.

**84. How do you keep a pipeline fast?** Cache, parallelize, split slow suites
off the merge path, fail fast on lint, run expensive scans only on the default
branch.

**85. Container vs VM?** Namespaces and cgroups sharing the host kernel, versus
a virtualized machine with its own kernel. Weaker isolation, far faster start.

**86. Why multi-stage builds?** No build tooling in the runtime image: smaller,
fewer CVEs.

**87. Why does Dockerfile instruction order matter?** Layer caching. Dependencies
before source.

**88. Liveness vs readiness probe?** Restart vs remove from service.

**89. Requests vs limits?** Scheduling guarantee vs cap. Memory over limit means
OOM kill; CPU over limit means throttling.

**90. What does Helm give you?** Templated manifests plus versioned releases with
upgrade and rollback. Use `helm template` to review, `--atomic` to auto-rollback.

---

## Round 8: Design and architecture (10 questions)

**91. Design a sensor ingest and track fusion service.**
[Lesson 7](ood.html), section 6. Clarify first, then components, then
justify each boundary, then tests, then what you deliberately did not build.

**92. How would you add a new sensor format?** New adapter class, register it in
the factory, no change to the pipeline. Open/closed.

**93. Microservices or monolith for a new subsystem?** Modular monolith by
default; distribute when independent deployability is the actual constraint.

**94. How do you version a message format used by other programs?** Additive
changes, explicit versioning, support the old one on an agreed schedule, and
change control through an interface working group.

**95. What is backpressure and how do you handle it?** Bounded queues, then a
deliberate choice between block, drop and shed, with the drop counted in
metrics.

**96. Explain idempotency and why it matters.** Retries are inevitable;
at-least-once delivery plus idempotent handlers is how you get correctness.

**97. How do you handle a slow downstream dependency?** Timeout, bounded retry
with jitter, circuit breaker, degraded fallback, visible in metrics.

**98. What would you monitor on this system?** Per-sensor rate and
last-message-age, queue depth, drop count, latency percentiles, track count,
error rate. Alert on symptoms, not causes.

**99. What is a Software Factory and why migrate into one?**
[Lesson 12](architecture.html), section 5.

**100. How would you migrate a legacy build into a pipeline?** Reproducible on a
clean machine first, then green with tests skipped, then tests, then scanning
with a baselined backlog, then artifacts, then deployment. One capability at a
time.

---

## Round 9: Security and sustainment (10 questions)

**101. A critical CVE lands in a library you use. What do you do?**
[Lesson 13](cyber.html), section 2. This is the most likely security question
for this posting.

**102. Direct or transitive dependency, and does it matter?** Yes:
`mvn dependency:tree`, upgrade the parent where possible, override as a stopgap.

**103. What is an SBOM and why does it matter?** Inventory that turns the next
emergency from a two-week audit into a one-hour query.

**104. How do you handle secrets?** Never in source, image, log or ticket.
Injected at runtime from a store. A committed secret is compromised even after
deletion.

**105. Prevent SQL injection?** Parameterized queries, always.

**106. Why is `pickle` dangerous?** Deserialization can execute arbitrary code.
Use a data-only format with schema validation.

**107. What is a STIG?** A DISA hardening configuration guide, scanned with
SCAP, with findings tracked or accepted through a POA&M.

**108. Hardening broke your application. What now?** Find the specific control,
understand what it protects, adapt the application. Do not disable the control.
Test against a hardened image in CI so you find it before the lab does.

**109. Security wants an upgrade that breaks an interface this sprint.**
[Lesson 13](cyber.html), section 6: get the real constraint, size it
honestly, offer three options with costs, escalate early with a recommendation.

**110. Why is adding a dependency not free here?** Monitoring, scanning,
upgrading and license clearance for the life of the program, plus export and
supply-chain considerations.

---

## Round 10: Behavioral and closing (10 questions)

**111. Tell me about a time you failed.** Story 3.

**112. Tell me about a conflict with a colleague.** Story 2.

**113. A time you had to learn something fast.** Recent is better. Bring the
artifact.

**114. A time you pushed back on a schedule.** Show that you brought numbers and
options, not just a refusal.

**115. How do you work with people you never meet in person?**
[Lesson 9](git-agile.html), section 9: write don't ping, protect the overlap,
never leave someone blocked overnight, update the ticket rather than the person.

**116. How do you handle a teammate whose code you think is poor?** In review,
specifically, about the code, with a reason and preferably a suggestion. Private
if it is a pattern rather than an instance.

**117. What are you looking for in your next role?** Consistent with this one.

**118. Why should we hire you?** Three sentences: the durable capability you
bring, the specific thing on this program you would contribute to first, and the
fact that you want the assignment.

**119. What concerns do you have about this role?** Have a real one, framed as a
question. "How the lab access works from the UAE side" is a good one. "Nothing"
is a wasted answer.

**120. Do you have questions for us?** Three or four from
[lesson 15](behavioral.html), section 8. Never zero.

---

## Round 11: Domain and track data (12 questions)

These will not all be asked, and a software interviewer may ask none of them.
They are here because being able to answer even three marks you out from every
other candidate. See [lesson 2](track-data.html).

**121. What is the difference between a plot and a track?**
A plot is an observation from one sensor at one time. A track is the system's
running estimate of one real object's state, built from many plots. Everything
hard in the domain lives in the gap between an observation and a belief.

**122. What does correlation mean in this context?**
Deciding that a new observation belongs to an existing track. Gating narrows the
candidates using the predicted position and its uncertainty; association then
assigns. Failure modes have names: track seduction, track swap, track break,
and ghost tracks.

**123. Why would one aircraft show up as two tracks?**
Sensor registration error, where two radars have position, azimuth, range or
timing biases that put the same object in two places, or a correlation failure
across the data link where two participants report it under different track
numbers. The second is dual designation, and reporting responsibility decides
who owns the track.

**124. What is track quality for?**
A confidence measure carried with a reported track so receivers know how much to
trust the position, and so the network can arbitrate when two reporters
disagree about the same object.

**125. Name some standards in this space.**
Link 16 under MIL-STD-6016 and STANAG 5516, with fixed-format binary J-series
messages; Link 11 under MIL-STD-6011; Link 22 under STANAG 5522; JREAP under
MIL-STD-3011 for carrying Link 16 traffic beyond line of sight; ASTERIX from
EUROCONTROL for surveillance data; MIL-STD-2525 and APP-6 for symbology.

**126. What is the difference between ASTERIX CAT 048 and CAT 062?**
CAT 048 is monoradar target reports, what one radar saw. CAT 062 is system track
data, what the system believes after fusion. Plots versus tracks, in a
standards-anchored form.

**127. Why is a fixed-bit message format hard to maintain?**
There are no field tags and no length prefixes, so the bits mean nothing without
the field map, which lives in code on both ends. Every version change is a
coordinated bilateral change, and a decoder that disagrees with an encoder by
one bit produces plausible wrong numbers rather than an error.

**128. What defects would you expect in this domain?**
Units and coordinate frames at interface boundaries, time-tag handling, and
message version mismatch. Altitude is the classic: ellipsoidal height, mean sea
level and barometric altitude are three different numbers for the same aircraft.

**129. What is sensor registration, or gridlock?**
Estimating and correcting each sensor's systematic biases so that observations
from different sensors land in a common frame before association. Without it,
one object becomes several tracks.

**130. Centralized or distributed fusion?**
Centralized fuses measurements in one place, giving the best accuracy at the
highest bandwidth cost with a single point of failure. Distributed tracks
locally and fuses tracks, which is cheaper on the link but has to handle the
fact that two local tracks of one object share errors and are not independent
evidence. Large fielded systems tend to be hybrid.

**131. What does data reduction mean?**
Two things, and it is worth asking which. In the live system it is reducing what
is reported to fit a planned link budget: thinning, area and quality filtering,
track-level rather than plot-level reporting, reporting responsibility, update
rate management. Every one of them buys bandwidth and sells information. In test
and evaluation it means turning raw recorded data into a form analysts can draw
conclusions from.

**132. How would you regression-test a fusion system?**
Scenario replay with track-to-truth metrics. Run a recorded or synthetic
scenario with known truth through the new baseline and compute completeness,
ambiguity, accuracy, continuity and timeliness against truth, then compare to
the previous baseline. You cannot unit-test "the air picture is still correct",
but you can measure it, and that is what lets you change infrastructure under a
fielded system and prove the mission behavior is unchanged.

---

## Self-scoring

After a mock run, score yourself honestly:

| Area | 1 &ndash; needs work | 3 &ndash; adequate | 5 &ndash; strong |
| --- | --- | --- | --- |
| Program knowledge | Vague | Knows the mission | Can discuss the tech refresh trade-offs |
| Domain fluency | Lost in the vocabulary | Follows the conversation | Plot vs track, and how to test a fusion system |
| Coding fluency | Long silences | Gets there slowly | Fluent, narrating, tests named |
| Python depth | Recognizes terms | Explains correctly | Explains and gives the tradeoff |
| Java depth | Recognizes terms | Explains correctly | Explains and gives the tradeoff |
| Linux | Knows the commands | Diagnoses a scenario | Structured method, not guesses |
| Testing / CI | Describes it | Has built it | Argues the economics of it |
| Design | Jumps to a solution | Clarifies then designs | Also says what they did not build |
| Behavioral | Generic | STAR with results | STAR plus what they learned |
| Scenario answers | Jumps to the fix | Structured method | Clarifies, diagnoses, names the trade, closes the loop |
| Bridging your background | Mentions ADOC in passing | Draws the parallel | Concedes the gap and names what is hard to hire |
| Expat readiness | Enthusiastic | Has thought about it | Has done the homework and the family conversation |

Anything at a 2 or below with three days left is where your remaining time goes.
