# 1. Program and role brief

Before any technical prep, you need to be able to talk about the program for
three minutes without hedging. Interviewers on defense programs notice
immediately whether a candidate understood what they applied to.

## What EADGE-T is

EADGE-T stands for **Extended Air Defence Ground Environment &ndash;
Transformation**. Lockheed Martin won it with the United Arab Emirates as launch
customer, and it has been described as the first end-to-end integrated air and
missile defense system of its kind.

Functionally it is a **command and control (C2) system for integrated air and
missile defense (IAMD)**. Break that into the pieces you can name out loud:

1. **Sensors.** Ground-based radars and other sources produce detections and
   tracks. Different sensors, different vendors, different message formats,
   different update rates, different coordinate frames.
2. **Correlation and fusion.** Those inputs get correlated into a single
   consistent air picture, so that one aircraft seen by three radars is one
   track, not three.
3. **Battle management.** Operators and decision aids evaluate threats, assign
   engagements, and deconflict weapons.
4. **Effectors.** Missile systems, including THAAD and Patriot PAC-3, are
   integrated so that the C2 layer can task them coherently rather than each
   running independently.
5. **Communications and data links.** Everything above is distributed across
   geographically separated sites and has to keep working over constrained,
   sometimes degraded links.

If you want a one-sentence framing to say in the interview: *"It takes a set of
separately procured radars and missile systems and makes them behave like one
air defense system, with one air picture and one battle management chain."*

## What "Tech Refresh" means

A fielded defense system typically runs on hardware and operating system
baselines that were locked years ago. Over time three pressures build:

- **Obsolescence.** Servers, network gear, and displays go end-of-life. Spares
  become unobtainable. Vendors stop supporting the firmware.
- **Security debt.** The OS and the third-party libraries accumulate published
  vulnerabilities. The accreditation that lets the system operate depends on
  closing them.
- **Toolchain drift.** The compilers, build systems, and test infrastructure age
  out of support, and nobody can reproduce a clean build.

A tech refresh addresses all three at once: new hardware, a current OS baseline,
updated COTS and FOSS dependencies, and a modern build and deployment pipeline.
The posting names exactly this: hardware modernization plus foundational
cybersecurity enhancements.

The engineering character of the work follows from that. It is **change under
constraint**. The system already works and already has an accredited behavior
that operators depend on. Your changes must not alter the mission behavior while
substantially altering everything underneath it. That is a specific discipline,
and demonstrating that you understand it is worth more in this interview than
any algorithm.

## What the role actually does day to day

From the posting, expanded into the daily reality:

**Modernize and maintain applications.** You will spend real time upgrading a
dependency from an old version to a current one, discovering that an API changed
underneath you, and reworking calling code so behavior stays identical. Java
library major-version bumps, Python 2-to-3 remnants, a logging framework
replaced because of a CVE, an XML parser swapped for one that is not vulnerable
to entity expansion.

**Migrate legacy capability into the Software Factory.** Take something that
built on a developer's machine with a hand-maintained script and get it building
reproducibly in a GitLab or Jenkins pipeline, with unit tests, static analysis,
and artifact publishing. See [lesson 12](architecture.html) for what
"Software Factory" means at LM.

**Write unit tests and automated test capability.** On legacy code with little
coverage, this is characterization testing: capture existing behavior in tests
first, then refactor with a net under you.

**Integration work.** Baseline merges (bringing a long-lived development line
together with a released baseline), defect resolution against a tracker, peer
reviews, and troubleshooting integration failures that appear only when several
subsystems run together.

**Collaboration across disciplines.** Systems engineers own requirements,
cybersecurity owns the hardening posture, integration and test own the lab.
You will negotiate across all of them. See [lesson 13](cyber.html).

## The vocabulary you should be comfortable with

You do not need to be an air-defense expert. You need to not be lost when these
words appear.

| Term | What it means |
| --- | --- |
| IAMD | Integrated Air and Missile Defense |
| C2 / BMC2 | Command and control; battle management command and control |
| Track | The system's estimate of one object's state over time, from many detections |
| Correlation | Deciding that a new detection belongs to an existing track |
| Fusion | Combining multiple sources into one estimate |
| Air picture | The current set of tracks, shared across sites |
| THAAD | Terminal High Altitude Area Defense, an upper-tier missile defense system |
| Patriot PAC-3 | A lower-tier air and missile defense system |
| Link 16 | A tactical data link standard used to exchange the air picture |
| Baseline | A specific configuration-controlled version of the whole system |
| SIL | Systems Integration Lab, where the software meets representative hardware |
| ATO | Authority to Operate, the accreditation permitting fielded use |
| RMF | Risk Management Framework, the process producing an ATO |
| STIG | Security Technical Implementation Guide, a hardening checklist |
| CDRL | Contract Data Requirements List, the deliverable documents |
| IV&V | Independent Verification and Validation |
| FMS | Foreign Military Sales, the mechanism for a program like this |

## Program history: know it, handle it gracefully

In 2017 Lockheed Martin took a roughly $120 million charge on the program and
publicly described its solution as having "proven to be less mature than needed
for this highly complex effort." That is a matter of public record and you may
be interviewed by people who lived through it.

Do not raise it as a gotcha. But if the topic of program challenges comes up, it
is entirely reasonable to say something like: *"I know the program had a hard
stretch several years back on integration maturity. That is part of why the work
interests me. Bringing a fielded, complex baseline onto modern infrastructure
without destabilizing it is a specific skill, and it is the kind of work I like."*

That answer shows you did your homework, does not gossip, and reframes the
history as the reason the job exists.

## The expat dimension

This is a two to three year assignment in the United Arab Emirates, most likely
Abu Dhabi. The team is geographically dispersed, meaning you will work daily
with people in Colorado Springs and elsewhere in the United States across an
eight to eleven hour time difference depending on the season.

They will assess whether you have thought about this seriously. Vagueness reads
as a flight risk, and a candidate who leaves an expat assignment at month eight
is expensive. [Lesson 15](behavioral.html) covers how to prepare that
conversation.

## Clearance and eligibility

Roles on this program typically require US citizenship and a security clearance,
commonly Secret, with the ability to obtain an interim. There may also be an
international assignment eligibility screen: medical clearance, family status,
and passport and visa processing for the UAE. Know your own status precisely
before the interview, including whether any prior clearance is still current or
would need reinstatement.

## Three-minute program summary to rehearse

Say this out loud until it flows.

> EADGE-T is Lockheed Martin's integrated air and missile defense C2 system for
> the UAE. It fuses inputs from a set of separately procured sensors into a
> single air picture, and gives battle managers one place to evaluate threats
> and task effectors including THAAD and Patriot. The current Tech Refresh
> effort modernizes the hardware and OS baseline and closes out foundational
> cybersecurity gaps, which in software terms means updating COTS and FOSS
> dependencies, migrating builds into the Software Factory CI/CD pipelines, and
> building real automated test coverage on code that historically was verified
> mostly by hand in the lab. The hard part is not any one of those changes. It
> is doing all of them to a fielded, accredited system without changing mission
> behavior. That is why the automated test work matters so much: it is the only
> thing that lets you move fast on infrastructure while proving to the customer
> that the mission thread is untouched.

If you can deliver that, you are ahead of most candidates before a line of code
is written.
