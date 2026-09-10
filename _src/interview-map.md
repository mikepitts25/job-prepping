# 3. Interview map and 14-day plan

## The loop you should expect

Lockheed Martin hiring for a senior IC role on an FMS program typically runs
something like this. Exact shape varies by hiring manager, but prepare for all of
it and you will not be surprised.

| Round | Who | Length | What it tests |
| --- | --- | --- | --- |
| Recruiter screen | Talent acquisition | 20&ndash;30 min | Clearance, citizenship, expat willingness, comp range, resume walk |
| Hiring manager screen | The lead you would report to | 45&ndash;60 min | Resume depth, program fit, why this job, communication |
| Technical interview | 1&ndash;3 engineers | 60&ndash;90 min | Coding, Python/Java depth, Linux, testing, CI/CD, debugging |
| Panel / team interview | Mixed disciplines | 60 min | Cross-discipline collaboration, systems thinking, behavioral |
| Expat / logistics conversation | International assignments, HR | 30 min | Family situation, medical, visa, term commitment |

Two things differ from a commercial software interview.

**The coding bar is lower, the discussion bar is higher.** You are far more
likely to get "write a function that parses this log format and reports the
worst offender" than "invert a binary tree with O(1) space." What they probe
hard is how you reason about failure, testing, and integration risk.

**Behavioral answers are weighted heavily.** Defense programs are
cross-functional and slow to correct mistakes. Interviewers are genuinely
screening for someone who communicates, escalates early, and does not go dark
for two sprints. Expect several "tell me about a time" questions and expect them
to follow up twice on each.

## What each round wants from you

### Recruiter screen

Have crisp answers to: are you a US citizen; what is your current clearance
status; are you genuinely willing to relocate to the UAE for two to three years;
what is your compensation expectation; when could you start. Do not improvise
the comp number. Decide it beforehand and give a range with a rationale
(see [lesson 16](behavioral.html)).

### Hiring manager screen

This one decides the most. Prepare:

- A **five-minute career narrative** that ends pointing at this job.
- Two **deep project stories** you can go three levels down on. They will ask
  "why did you choose that," then "what broke," then "what would you do
  differently." Have the third-level answers ready.
- A specific, honest answer to **why this job**. "I want to work on
  mission-critical systems where the integration problem is the real problem,
  and I want the international assignment" beats anything generic.
- Two or three **questions for them** that only someone who read about the
  program would ask. Examples in [lesson 18](mock-interview.html).

### Technical interview

Plan for a mix of:

- One or two **small coding problems** in Python or Java, 15&ndash;25 minutes
  each. String and collection manipulation, parsing, a light algorithm.
  See [lesson 7](dsa.html).
- **Language depth questions.** Python: mutability, generators, GIL, context
  managers, virtual environments. Java: collections, equals/hashCode,
  concurrency, streams, memory. See lessons 4, 5 and 6.
- **Linux questions.** Find the file, follow the log, diagnose the full disk,
  read the process list. See [lesson 9](linux.html).
- **Testing and CI questions.** How do you test legacy code with no tests; what
  goes in a pipeline; what makes a test suite trustworthy.
  See [lesson 11](testing-ci.html).
- **A debugging scenario.** "The service works in the lab and fails in
  integration. Walk me through what you do." This is the highest-signal question
  they can ask for this role. Prepare a structured answer.

### Panel

Systems, cyber, and integration engineers ask how you work with them. They are
listening for whether you treat requirements as negotiable, whether you tell
people bad news early, and whether you can explain technical content to a
non-software engineer.

## How to prepare when you are rusty

The core problem is **retrieval fluency**, not knowledge. You know what a
dictionary is. Under observation, with a stranger watching your cursor, you may
blank on `dict.get(key, default)` or on how to sort by a second key. That is
fixed only by typing.

Rules for the next two weeks:

1. **Type every example.** No copy-paste, no reading along. Physically type it,
   run it, break it on purpose, fix it.
2. **Talk while you type**, at least once a day. Narrate out loud what you are
   doing. The single most common failure in a live coding round is going silent
   for six minutes.
3. **Time yourself.** Anything you cannot do in 25 minutes untimed, you cannot
   do in 25 minutes observed.
4. **One language for coding rounds.** Pick Python if you have any choice; it
   costs the fewest keystrokes and the fewest ceremony errors. Keep Java warm
   enough to discuss fluently and write a class on a whiteboard.
5. **Write tests for your own practice solutions.** It builds the habit and it
   is directly what the job is.

## The 14-day plan

Roughly 90 minutes on weekdays, three hours on weekend days. Adjust to your
actual availability; the ordering matters more than the hours.

### Week 1: get the rust off

**Day 1 &ndash; Orientation.** Read [lesson 1](program-brief.html),
[lesson 2](track-data.html) and this one. Set up your environment: Python 3.11+,
a JDK 17+, Git, an editor, and the [practice repo](../practice/README.html).
Rehearse the three-minute program summary out loud once.

**Day 2 &ndash; Python foundations.** [Lesson 4](python.html) sections
1&ndash;7: what Python is, names and objects, the built-in types, containers and
control flow. Type every example into a REPL. This is the day that matters most
if you are rusty, because it rebuilds the mental model rather than the syntax.

**Day 3 &ndash; Python: functions, classes, testing.** Rest of
[lesson 4](python.html), then [lesson 5](python-practice.html) sections 1, 2 and
7. Do the six REPL exercises at the end of lesson 4, especially the sixth. Write
pytest tests for two practice problems.

**Day 4 &ndash; Java refresher.** [Lesson 6](java.html). Compile and run
everything. Write one class with proper `equals`, `hashCode`, and `toString`
from memory. If Python is still shaky, spend half of today on the rest of
[lesson 5](python-practice.html) instead; Python is the language you will most
likely be asked to code in.

**Day 5 &ndash; Complexity and core structures.** [Lesson 7](dsa.html)
sections 1&ndash;4. Problems A1&ndash;A6, timed at 20 minutes each.

**Day 6 &ndash; Algorithm patterns.** Lesson 7 sections 5&ndash;8. Problems
A7&ndash;A14. Narrate out loud on at least three of them.

**Day 7 &ndash; OO design.** [Lesson 8](ood.html) end to end, including the
design exercise. Then rest. Actually rest.

### Week 2: the job-shaped material

**Day 8 &ndash; Linux and troubleshooting.** [Lesson 9](linux.html) plus the
drills. Do them on a real shell, not from memory.

**Day 9 &ndash; Git, GitLab, Agile.** [Lesson 10](git-agile.html). Do the
merge-conflict exercise for real in a scratch repo.

**Day 10 &ndash; Testing and CI/CD.** [Lesson 11](testing-ci.html). Write a
`.gitlab-ci.yml` for the practice repo and be able to explain each stage.

**Day 11 &ndash; Containers and architecture.** Lessons
[10](containers.html) and [11](architecture.html). Write and run a
Dockerfile for the practice service.

**Day 12 &ndash; Cyber and sustainment.** [Lesson 14](cyber.html). Prepare
your answer to the dependency-upgrade question, which is nearly certain to
appear in some form.

**Day 13 &ndash; Behavioral and your bridge.** [Lesson 15](adoc-bridge.html)
and [lesson 16](behavioral.html). Write out your positioning statement and six
STAR stories in full. Rehearse the expat answer with someone else in the room.

**Day 14 &ndash; Mock and taper.** Work [lesson 18](mock-interview.html)
under time pressure. Two coding problems, timed and narrated, then six scenario
answers from [lesson 17](scenarios.html) out loud. Then stop. Skim
[the cheat sheets](cheatsheets.html) the morning of, and nothing else.

## Compressed plans

**Seven days:** Days 1, 2, 3, 5, 6, 10, 13, 14 compressed into one week. Skip
lessons 12 and 13 as study; skim them for vocabulary only.

**Three days:** Day one, lesson 4 plus problems A1&ndash;A8 timed. Day two,
lesson 11 plus lesson 14's upgrade answer plus lesson 1's program summary and
lesson 2's vocabulary. Day three, lesson 15's positioning statement and six STAR
stories written out in full, plus lesson 17's scenario answers out loud. If
you only have three days, behavioral and program fluency return more than
algorithms.

**One evening:** [Cheat sheets](cheatsheets.html), the program summary in
lesson 1, your positioning statement from lesson 15, and six STAR stories from
lesson 16. In that order.

## During the interview

- **Restate the problem before you code.** "So I need to read a stream of
  detection records and emit the ones where the timestamp goes backwards. Should
  I assume it fits in memory?" This buys thinking time and demonstrates rigor.
- **Ask about scale and input assumptions.** Every time. It is a senior signal
  and it is free.
- **Write the ugly version first, out loud**, then improve it. A working brute
  force beats an unfinished elegant solution every single time.
- **Say what you would test.** Even if you are not asked. "Empty input, single
  element, all duplicates, timestamps equal." That one sentence is worth a lot
  in a role whose whole point is automated test capability.
- **If you blank on syntax, say so and keep going.** "I always forget the exact
  signature for sorting by a key here; I'd look it up, but the idea is a lambda
  returning a tuple." Nobody fails a candidate for that. They fail candidates
  who freeze silently.
- **Do not fake experience you do not have.** "I have not used Helm directly. I
  have used Kubernetes manifests, and my understanding of Helm is that it is
  templating and release management on top of those. Is that how you use it?"
  That answer is respected. A bluffed answer that unravels is fatal.
