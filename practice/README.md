# Practice repo

Runnable practice for the [EADGE-T interview prep](../index.html). Two modules:
a Python package with 84 tests, and a Maven project with 22 JUnit tests. Both
pass as written, so you have a known-good baseline before you start changing
things.

The exercises are deliberately job-shaped. Version comparison for CVE triage,
config diffing for a migration, bounded queues, rate limiting, out-of-order
timestamp detection. These are closer to what you will be asked on this program
than a binary tree puzzle is.

## Python

```bash
cd python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

pytest -q                              # 84 tests against the reference solutions
PREP_TARGET=exercises pytest -q        # against your own attempts in exercises.py
pytest -q -k version                   # one topic at a time
pytest --cov=solutions --cov-report=term-missing
```

`exercises.py` holds the same functions as stubs, with the docstrings kept so
you know what to build. Anything you have not written yet is reported as a skip
rather than a failure, so you can work through them a few at a time.

| File | What it is |
| --- | --- |
| `exercises.py` | Stubs. Type your solutions here. |
| `solutions.py` | Reference implementations, commented with the reasoning to say out loud. |
| `test_solutions.py` | The tests. Read them first: they are the edge-case answer key. |
| `conftest.py` | Turns a `NotImplementedError` into a skip when running against stubs. |
| `tracks.py` | Domain module: fixed-bit message decoding and track-to-truth metrics. |
| `test_tracks.py` | 30 tests for the above, covering split tracks, renumbering and false tracks. |

### tracks.py

This one is worth reading even if you do not write a line of it. It implements
two things you can talk about in the interview:

* **Fixed-bit field decoding** against a field table, with signed two's
  complement and specification scale factors. This is what a sensor or data
  link adapter actually is, and it is the most likely domain code in the job.
* **Track-to-truth metrics**: completeness, ambiguity, accuracy, continuity and
  spurious track count, plus a regression report comparing two runs. This is
  how you regression-test a fusion system, and proposing it is one of the
  strongest technical contributions you could offer in this interview.

The tests are the interesting part. They encode the distinction between
ambiguity (two tracks on one object at once) and continuity (one object
renumbered over time), which people confuse, and they show why association has
to gate on time before distance.

See lesson 2 of the site for the standards and vocabulary behind it.

## Java

```bash
cd java
mvn -B test                            # 22 tests
mvn -B test -Dtest=SensorStatsTest     # one class
mvn -B clean verify
mvn dependency:tree                    # the command you use for CVE triage
```

| Class | What it demonstrates |
| --- | --- |
| `Detection` | Record, compact constructor validation, chained exceptions |
| `SensorStats` | Streams, `groupingBy`, deterministic tie-breaking |
| `LruCache` | `LinkedHashMap` access order, `removeEldestEntry` |
| `BoundedIngestQueue` | Bounded queue, drop-oldest policy, atomic counters, a latch-based concurrency test |

## How to work through this

**Do not read `solutions.py` first.** Read the test file, write the function in
`exercises.py`, run the tests, and only then compare. Reading a solution feels
like learning and is not.

For each problem:

1. Read the test cases and say the edge cases out loud before writing anything.
2. Set a 20-minute timer.
3. Narrate while you type. Silence is the failure mode in a live round.
4. When it passes, say the complexity out loud, in time and in space.
5. Compare with the reference and read the comments, which are written as things
   to say in an interview rather than as code explanations.

## Suggested order

**Day one:** `chunk`, `merge_counts`, `flatten`, `parse_detections`.
**Day two:** `top_sensors`, `top_k_frequent`, `merge_intervals`, `log_levels_by_hour`.
**Day three:** `find_time_regressions`, `RingBuffer`, `RateLimiter`.
**Day four:** `compare_versions`, `packages_needing_upgrade`, `diff_config`.
**Day five:** `startup_order`, `retry`, `average_speeds_kph`.
**Day six:** redo the four you found hardest, from a blank file, timed.
**Day seven:** the Java module, then read `tracks.py` and its tests and be able
to explain the four metrics out loud.

If you only have time for five, do `parse_detections`, `top_sensors`,
`compare_versions`, `packages_needing_upgrade`, and `RateLimiter`. Those five
cover parsing, aggregation, dependency triage, and bounded state, which is most
of the surface area this role actually touches.

## Extending it

Good self-directed exercises once the basics pass:

- Add a `--json` command line interface over `top_sensors` using `argparse`.
- Write a property-based test with Hypothesis: for any list of intervals, no two
  merged outputs overlap.
- Make `RateLimiter` bound its own memory by evicting clients idle for longer
  than the window, and write the test that proves it.
- Port `diff_config` to Java and compare how the two read.
- Write a `Dockerfile` for the Python module and get `pytest` running inside it.
- Write a `.gitlab-ci.yml` that runs both modules, and explain each stage out
  loud as if to an interviewer.
- Add a `timeliness` metric to `tracks.py`: the age of the newest system report
  relative to truth, and the test that proves it.
- Make `associate` solve the assignment globally rather than greedily, and write
  the test case where greedy gets it wrong.

The last two are the ones most directly aligned with the job description. Do
them even if you feel they are not "real" practice.
