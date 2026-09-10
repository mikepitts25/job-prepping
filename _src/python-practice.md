# 5. Python in practice

[Lesson 4](python.html) covered the language. This lesson covers what you
actually use it with: the standard library, the patterns that show up in real
code, how to test, and how to debug. It still assumes no prior knowledge, and
it still explains why each thing exists.

This is the lesson closest to the job description, because "developing unit
tests and automated test capabilities" is what the posting says you would be
doing.

## 1. The standard library

Python ships with a large library of modules. Knowing which one to reach for is
most of being productive, and reaching for a third-party package when the
standard library already does the job is a mark against you on a program where
every dependency has to be scanned, licensed and maintained for years.

### `collections`: better containers

```python
from collections import Counter, defaultdict, deque
```

**`Counter`** counts things. You saw the manual version in lesson 4:

```python
counts = {}
for sensor in sensor_ids:
    counts[sensor] = counts.get(sensor, 0) + 1
```

`Counter` is that, done for you, plus ranking:

```python
counts = Counter(sensor_ids)
counts["radar-a"]                # the count; 0 for anything absent, no KeyError
counts.most_common(3)            # the three most frequent, as (item, count) pairs
```

`most_common` answers "top N by frequency," which is one of the most common
interview questions there is.

**`defaultdict`** removes the "is this key here yet?" check. You give it a
factory, and it calls that factory automatically the first time a key is
touched:

```python
groups = defaultdict(list)                 # missing keys become an empty list
for detection in detections:
    groups[detection.sensor_id].append(detection)
```

Without it you would need `setdefault` or an `if`. The grouping pattern above
appears in nearly every aggregation problem.

Be aware of the one surprise: merely *reading* a missing key creates it.
`groups["nope"]` leaves an empty list behind. If that matters, use `.get`.

**`deque`**, said "deck," is a double-ended queue. A list is fast to append to
at the end and slow to insert or remove at the front, because everything after
the removed item shifts along. A deque is fast at both ends.

```python
recent = deque(maxlen=1000)      # a fixed-size window
recent.append(item)              # when full, the OLDEST is dropped automatically
recent.appendleft(item)
recent.popleft()
```

The `maxlen` behavior is genuinely useful: it gives you a bounded buffer with
no code. An unbounded queue between a fast producer and a slow consumer is a
deferred out-of-memory crash, so bounding it is a design decision, not an
optimization. See [lesson 8](ood.html).

### `itertools`: tools for iteration

```python
import itertools as it

it.chain([1, 2], [3, 4])          # treat several iterables as one sequence
it.islice(source, 5)              # the first 5 items of anything, lazily
it.combinations("ABC", 2)         # every 2-item combination
it.groupby(sorted(rows, key=f), key=f)   # group ADJACENT equal items
```

`groupby` has a sharp edge worth knowing: it groups only *consecutive* items,
so you must sort by the same key first. Forgetting is a classic bug. For most
grouping tasks `defaultdict(list)` is simpler and safer.

### `heapq`: keeping the smallest thing to hand

A **heap** is a structure that keeps the smallest item instantly available
while staying cheap to insert into. Python implements it on top of a plain
list.

```python
import heapq

heap = []
heapq.heappush(heap, (0.4, "T1"))
heapq.heappush(heap, (0.9, "T2"))
heapq.heappop(heap)                       # (0.4, 'T1') -- always the smallest

heapq.nlargest(3, tracks, key=lambda t: t.confidence)
heapq.nsmallest(3, tracks, key=lambda t: t.confidence)
```

**Why not just sort?** Sorting costs O(n log n) and gives you the whole order.
If you only want the top three from ten million items, a heap of size three
costs O(n log 3) and constant memory. Being able to state that trade-off is
worth more in an interview than the code.

### `json`, `csv`, `re`, `datetime`, `os`

```python
import json
json.loads('{"a": 1}')                  # text -> Python object
json.dumps({"a": 1}, indent=2)          # Python object -> text
with open("cfg.json", encoding="utf-8") as f:
    config = json.load(f)               # note: load, not loads, for a file
```

The `s` in `loads`/`dumps` means "string." `load`/`dump` work on a file object.

```python
import csv
with open("data.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):       # each row becomes a dict keyed by header
        print(row["sensor_id"])
```

Use the `csv` module rather than `line.split(",")` whenever the data might
contain quoted fields with commas in them. Real data does.

```python
import re                               # regular expressions: pattern matching in text
re.findall(r"TRACK (\d+)", text)        # every captured number
re.sub(r"\s+", " ", text)               # collapse runs of whitespace
m = re.match(r"(?P<level>[A-Z]+) (?P<msg>.*)", line)
if m:
    m.group("level")                    # named capture groups
```

Regular expressions are powerful and easy to overuse. If `split` and
`startswith` will do the job, use them; they are far more readable.

```python
import datetime as dt
now = dt.datetime.now(dt.timezone.utc)  # ALWAYS include the timezone
now.isoformat()                         # '2026-09-10T11:59:00+00:00'
dt.datetime.fromisoformat(text)
```

**Always use timezone-aware datetimes in UTC** and convert to local time only
for display. A naive datetime, one without a timezone, is ambiguous, and on a
system with sites in different countries that ambiguity becomes a real defect.

For measuring *durations*, do not use the wall clock at all:

```python
import time
start = time.monotonic()
do_work()
elapsed = time.monotonic() - start
```

`time.monotonic` never goes backwards. The wall clock can step backwards when
the system corrects against a time source, which on a fielded system with
synchronized sites is a real event and produces negative durations.

```python
import os
os.environ.get("LOG_LEVEL", "INFO")     # read config from the environment
```

Configuration that differs between environments belongs in environment
variables, not in the code and not in the container image. See
[lesson 14](cyber.html).

## 2. Generators: processing data too big to hold

This is one of Python's genuinely important ideas.

A normal function computes a result and returns it. A **generator** produces
values one at a time, pausing between them. You write one by using `yield`
instead of `return`:

```python
def read_records(path):
    """Yield (line_number, line) one at a time, skipping blanks and comments."""
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if line and not line.startswith("#"):
                yield lineno, line
```

Calling it does not run it. It returns a generator object. Each time the `for`
loop asks for the next item, the function runs until the next `yield`, hands
that value over, and freezes exactly where it was:

```python
for lineno, line in read_records("huge.log"):
    process(line)
```

**Why this matters:** memory. The list version below reads the entire file into
RAM before doing anything:

```python
def read_records_list(path):
    records = []
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            records.append((lineno, raw.strip()))
    return records                       # a 40 GB file needs 40 GB of RAM
```

The generator processes that same file in constant memory. The sentence to say
in an interview is: *"a generator produces values lazily, so I can process a
40 GB log on a machine with 8 GB of RAM."*

Generator expressions are the comprehension syntax with parentheses, and they
are lazy in the same way:

```python
squares = (n * n for n in range(10_000_000))     # nothing computed yet
sum(1 for line in open("f.log") if "ERROR" in line)   # counts without building a list
```

**The trade-offs**, which is what a follow-up question will probe:

- A generator can be consumed **once**. Iterate it twice and the second pass is
  empty.
- You cannot index it or take its `len()`.
- It is the right choice for a stream, a large file or an expensive-to-compute
  sequence. A list is the right choice when you need the data more than once.

## 3. Functions as objects, closures and decorators

Decorators look like magic. They are not, and the way to understand them is to
build up in three steps.

**Step one: functions are objects.** You can pass them around and return them.

```python
def shout(text):
    return text.upper()

def apply_twice(fn, value):
    return fn(fn(value))

apply_twice(shout, "hi")            # 'HI'
```

**Step two: a function can create and return another function**, and the inner
one remembers the variables from where it was defined. That memory is called a
**closure**.

```python
def make_multiplier(factor):
    def multiply(value):
        return value * factor        # 'factor' is remembered from the enclosing call
    return multiply

double = make_multiplier(2)
double(21)                           # 42
```

**Step three: a decorator is a function that takes a function and returns a
replacement.** The `@` syntax is shorthand for reassigning the name.

```python
import functools, time, logging

log = logging.getLogger(__name__)

def retry(times=3, delay=0.5, exc=Exception, sleep=time.sleep):
    """Retry a function with exponential backoff."""
    def decorate(fn):
        @functools.wraps(fn)                  # keep fn's name and docstring
        def wrapper(*args, **kwargs):
            wait = delay
            last = None
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except exc as err:
                    last = err
                    log.warning("attempt %d/%d failed: %s", attempt, times, err)
                    if attempt < times:
                        sleep(wait)
                        wait *= 2             # back off: 0.5s, 1s, 2s...
            raise last
        return wrapper
    return decorate

@retry(times=4, exc=TimeoutError)
def fetch_status(host):
    ...
```

`@retry(...)` above `def fetch_status` means exactly
`fetch_status = retry(...)(fetch_status)`. Nothing more.

Notes worth making in an interview:

- **`*args, **kwargs`** means "accept any arguments and pass them straight
  through," which is what lets one decorator wrap any function. `*args`
  collects positional arguments into a tuple; `**kwargs` collects keyword
  arguments into a dict.
- **`functools.wraps`** copies the original function's name and docstring onto
  the wrapper. Without it, every decorated function reports itself as `wrapper`
  in tracebacks and documentation, which is miserable to debug.
- **The `sleep` parameter is injected** so tests can pass a fake and run
  instantly instead of actually waiting. That is a deliberate testability
  choice, and pointing it out is a strong signal.
- **Real retries need jitter**, a small random variation in the delay.
  Synchronized retries from many clients are how a struggling service gets
  finished off.

**Why decorators exist:** they attach cross-cutting behavior, such as retry,
timing, caching, authorization or logging, without editing the function itself
and without repeating that behavior in fifty places.

One you will use directly:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def expensive(n):
    ...
```

That caches results by argument, so repeated calls with the same input are
free. Bounded by `maxsize`, because an unbounded cache is a memory leak.

## 4. Context managers

You met `with` for files. You can write your own, and the reason is the same:
guarantee that cleanup happens even when something raises.

```python
from contextlib import contextmanager
import time

@contextmanager
def timed(label):
    start = time.perf_counter()
    try:
        yield                                   # the body of the 'with' runs here
    finally:
        print(f"{label}: {time.perf_counter() - start:.3f}s")

with timed("parse"):
    parse_everything()
```

Everything before the `yield` is setup, everything after is teardown, and the
`finally` guarantees the teardown runs even on an exception. Use this shape for
anything that must be released: locks, connections, temporary directories,
timing.

## 5. Concurrency and the GIL

Expect the question *"does Python do real multithreading?"* It is a favourite,
and the answer is nuanced.

First, definitions. **Concurrency** is dealing with several things at once by
interleaving them. **Parallelism** is genuinely doing several things at the
same instant on different CPU cores. A **thread** is a separate line of
execution inside one process, sharing memory. A **process** is a separate
program with its own memory.

CPython has a **Global Interpreter Lock**, the GIL: only one thread may execute
Python bytecode at a time. So:

- **I/O-bound work** (network, disk, waiting on another service): threads help
  a great deal, because the GIL is released while a thread waits.
- **CPU-bound work** (computation): threads do not help. Use separate
  processes, or a native library that releases the GIL.

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=8) as pool:           # I/O bound
    results = list(pool.map(fetch_status, hostnames))

with ProcessPoolExecutor(max_workers=4) as pool:          # CPU bound
    results = list(pool.map(correlate_chunk, chunks))
```

The trade with processes is that they do not share memory, so data has to be
serialized to get to them and back. For small inputs and heavy computation that
is a bargain; for large inputs and light computation it is a loss.

Recent Python versions offer an optional free-threaded build without the GIL.
If you mention it, be ready to say it is opt-in and not yet the default in most
deployments.

## 6. Logging

`print` is for you at a terminal. **Logging is for a program running somewhere
you cannot see**, which on this job is every deployment that matters.

```python
import logging, os

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
log = logging.getLogger(__name__)

log.debug("detail useful only when diagnosing")
log.info("processed %d detections from %s", count, sensor_id)
log.warning("queue depth %d, above threshold", depth)
log.error("adapter failed to parse record")
log.critical("cannot reach any sensor")

try:
    risky()
except Exception:
    log.exception("adapter failed")      # inside except: logs the full traceback
```

What logging gives you over `print`:

- **Levels**, so you can turn detail up when diagnosing and down in normal
  operation, without editing code.
- **Structure**: timestamp, level and module name on every line, which is what
  makes logs greppable and correlatable across components.
- **Routing**: the same calls can go to a file, the console, the system journal
  or a collector, decided by configuration.

Two details worth stating in an interview:

**Use `%s` placeholders, not f-strings, in log calls.** Passing arguments
separately means the formatting is skipped entirely when that level is
disabled. With an f-string you pay the cost on every call even when nothing is
written.

```python
log.debug("state: %s", expensive_summary())     # only called if DEBUG is on
log.debug(f"state: {expensive_summary()}")      # ALWAYS called
```

**Never log secrets, credentials or full payloads.** Logs get copied, shipped
and read by people who are not you. See [lesson 14](cyber.html).

## 7. Testing with pytest

This is the section that matters most for this job.

### Why automated tests, stated as economics

Python is interpreted, so a typo on an error path is not found until that path
runs. On a fielded system, the alternative discovery mechanism is the
integration lab, which is the program's scarcest resource. **Every defect a
unit test catches is a lab slot you did not consume.** That is the argument to
make, and it is much stronger than "tests are good practice."

### Your first test

A test is just a function whose name starts with `test_`, containing an
`assert`.

```python
# tracks.py
def worst_offender(counts):
    """Return the key with the highest count, breaking ties by name."""
    if not counts:
        return None
    return max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
```

```python
# test_tracks.py
from tracks import worst_offender

def test_empty_returns_none():
    assert worst_offender({}) is None

def test_picks_the_highest():
    assert worst_offender({"a": 1, "b": 5}) == "b"

def test_ties_break_by_name():
    assert worst_offender({"a": 3, "b": 3}) == "b"
```

```bash
pip install pytest
pytest -q
```

pytest finds files named `test_*.py`, finds functions named `test_*`, runs
them, and reports which failed. When an assertion fails it shows you the actual
values, which is why plain `assert` is enough and no special assertion methods
are needed.

### Structure: Arrange, Act, Assert

```python
def test_burst_drops_oldest_and_counts_it():
    # Arrange: set up the situation
    queue = IngestQueue(capacity=3, policy="drop_oldest")

    # Act: do the one thing under test
    for i in range(5):
        queue.offer(detection(seq=i))

    # Assert: check the outcome
    assert [d.seq for d in queue.drain()] == [2, 3, 4]
    assert queue.dropped_count == 2
```

**One behavior per test.** If the test name needs the word "and," it is
probably two tests. The name is documentation: `test_ties_break_by_name` tells
a reader what the code is supposed to do. `test3` tells them nothing.

### What to test

Given any function, ask for these, and **say them out loud in an interview even
when you are not asked**:

- The normal case.
- Empty input.
- A single item.
- Duplicates, and ties.
- Malformed or wrong-typed input.
- Boundaries: zero, one, the maximum, one either side of a threshold.
- The error path: does it raise what it should?

That list is most of what separates a senior answer from a correct one.

### Parametrized tests

When the same logic needs many input/output pairs, do not write ten near-
identical functions:

```python
import pytest

@pytest.mark.parametrize("counts,expected", [
    ({}, None),
    ({"a": 1}, "a"),
    ({"a": 1, "b": 2}, "b"),
    ({"a": 3, "b": 3}, "b"),
])
def test_worst_offender(counts, expected):
    assert worst_offender(counts) == expected
```

pytest runs that as four separate tests and names each by its inputs, so a
failure tells you which case broke.

### Testing that something raises

```python
def test_rejects_confidence_above_one():
    with pytest.raises(ValueError, match="out of range"):
        Detection("radar-1", 0.0, 1.5)
```

The test passes only if the exception is raised. If the code wrongly accepts
the value, the test fails. `match` checks the message, so you are testing that
the right error was raised and not merely that something went wrong.

### Fixtures: shared setup

A **fixture** is a function that builds something a test needs. Ask for it by
naming it as a parameter and pytest supplies it.

```python
@pytest.fixture
def sample_log(tmp_path):                 # tmp_path is built into pytest
    p = tmp_path / "sample.log"
    p.write_text("RDR-1,ok\nRDR-2,fail\n", encoding="utf-8")
    return p

def test_counts_failures(sample_log):
    assert count_failures(sample_log) == 1
```

`tmp_path` gives each test a fresh temporary directory that is cleaned up
afterwards, so tests that touch the filesystem stay independent. Independence
matters: a test that only passes when another ran first is worse than no test,
because it fails mysteriously later.

### Comparing floats

```python
assert result == pytest.approx(1.0)
assert distance == pytest.approx(120, abs=10)
```

Never compare floats with `==`, for the reason in [lesson 4](python.html).

### Test doubles: replacing things you cannot call

Tests must not depend on a real network, a real database or the real clock:
those make tests slow, flaky and dependent on the outside world.

The vocabulary, which interviewers do ask you to distinguish:

| Name | What it is |
| --- | --- |
| **Stub** | Returns canned answers |
| **Spy** | A stub that also records how it was called |
| **Mock** | Pre-programmed with expectations; you assert on the interaction |
| **Fake** | A real but simplified implementation, e.g. an in-memory store |

```python
from unittest.mock import MagicMock, patch

def test_publishes_only_high_confidence():
    publisher = MagicMock()                    # a stand-in that records calls
    service = IngestService(publisher=publisher)

    service.handle(detection(confidence=0.95))
    service.handle(detection(confidence=0.10))

    publisher.publish.assert_called_once()

@patch("eadge.client.requests.get")            # replace it for this test only
def test_timeout_is_not_fatal(mock_get):
    mock_get.side_effect = TimeoutError("no route")
    assert poll_sensor("radar-a") == SensorStatus.UNKNOWN
```

**Prefer fakes to mocks** where you can, and be ready to say why: a test that
asserts on a chain of mock interactions breaks whenever you restructure the
code, even when the behavior is unchanged. A test against an in-memory fake
asserts on outcomes and survives refactoring.

### Making code testable

Notice that `IngestService(publisher=publisher)` accepts its dependency as an
argument. That is **dependency injection**, and it is what makes the test
possible. Compare:

```python
class IngestService:
    def __init__(self):
        self.publisher = KafkaPublisher("broker:9092")   # hard to test
```

You cannot test that without a broker. The version that takes a publisher works
with a real one in production and a fake one in tests.

**If a class is hard to test, that is a design defect, not a testing problem.**
Hard-to-test usually means it builds its own dependencies, reads global state,
or does several unrelated things. That sentence is a very good answer.

The same applies to time:

```python
class TrackAger:
    def __init__(self, now=time.monotonic, max_age_s=30.0):
        self._now = now                       # injected clock
        self._max_age = max_age_s

def test_track_goes_stale():
    clock = [1000.0]
    ager = TrackAger(now=lambda: clock[0], max_age_s=30.0)
    track = Track(last_update=1000.0)

    assert not ager.stale(track)
    clock[0] = 1031.0                          # move time without waiting
    assert ager.stale(track)
```

That test is instant and deterministic. The version using `time.sleep(31)` is
neither.

### Coverage

```bash
pytest --cov=tracks --cov-report=term-missing
```

Coverage reports which lines ran during the tests. Be honest about what it
means: **it is a good detector of untested code and a bad measure of test
quality.** Ninety percent coverage with assertions that can never fail is
worthless. Zero percent on the correlation engine is alarming. Use it to find
gaps and set a floor that must not regress, never as a target in itself.

The honest check is to break the code deliberately and confirm a test goes red.
A test that passes against broken code is worse than no test, because it buys
false confidence.

### Flaky tests

A **flaky** test passes sometimes and fails sometimes with no code change.
Treat it as urgent, not annoying. One flaky test teaches the team to re-run the
pipeline instead of reading the failure, and from then on the suite protects
nothing.

Causes, in rough order of frequency: dependence on wall-clock time, shared
state between tests, dependence on test execution order, a genuine race in the
code, and an unfaked external dependency. Note that the fourth means the flaky
test is correctly reporting a real bug.

**Adding a retry is not a fix.** Quarantine it with a ticket, an owner and a
deadline, then find the cause.

## 8. Debugging

### Read the traceback

Bottom-up, as in [lesson 4](python.html). The last line is the error; the lines
above are how you got there.

### Print, then stop printing

`print` debugging is fine and everyone does it. Two upgrades that cost nothing:

```python
print(f"{confidence=} {sensor_id=}")     # prints names and values
```

and switching to `log.debug` so the statements can stay in the code, turned off
by configuration, instead of being deleted and rewritten next time.

### The debugger

```python
breakpoint()          # execution stops here and drops you into a prompt
```

Then: `n` next line, `s` step into a call, `c` continue, `p expr` print an
expression, `l` list the code around you, `q` quit. Ten minutes learning these
saves many hours of print statements.

### Profiling

Never optimize by intuition. Measure.

```python
import cProfile, pstats
cProfile.run("correlate(all_detections)", "prof.out")
pstats.Stats("prof.out").sort_stats("cumulative").print_stats(15)
```

That tells you which function actually consumes the time. It is almost never
the one you guessed. Then use `timeit` to compare a candidate fix, and measure
before and after.

The most common real cause of slow Python, by a wide margin, is an O(n)
membership test inside an O(n) loop. Look for `x in some_list` first.

## 9. Packaging and dependencies

```
myservice/
  pyproject.toml
  src/myservice/__init__.py
  src/myservice/adapter.py
  tests/test_adapter.py
```

```toml
[project]
name = "myservice"
version = "1.4.0"
requires-python = ">=3.11"
dependencies = ["requests==2.32.3", "pyyaml==6.0.2"]

[project.optional-dependencies]
dev = ["pytest==8.3.3", "pytest-cov", "ruff", "mypy"]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
```

**Pin exact versions.** A range means the build pulls something different next
week and is therefore not reproducible. On a configuration-controlled program
that is a requirement, not a preference.

Quality tooling you should be able to name:

```bash
ruff check .           # linting: finds likely mistakes and dead code
ruff format .          # or black: consistent formatting, ends style arguments
mypy src/              # static type checking against your hints
bandit -r src/         # security-focused static analysis
pip-audit              # known vulnerabilities in your dependencies
```

`mypy` deserves the emphasis. It recovers a large part of what a compiler would
have caught, in a language where those errors otherwise wait until runtime.
That is a strong argument on a system where "runtime" may mean the lab or the
field. `pip-audit` connects directly to the COTS and FOSS upgrade work the
posting describes; see [lesson 14](cyber.html).

## 10. Practice problems

Write each one, then write tests for it. Reference solutions with commentary
are in the [practice repo](../practice/README.html).

**P1.** Given a list of `"sensor_id,timestamp,confidence"` lines, return the
sensor with the highest average confidence. Ignore malformed lines and count
how many you skipped.

**P2.** Write `chunk(items, n)` returning a list of lists of at most `n` items.
`chunk([1,2,3,4,5], 2) == [[1,2],[3,4],[5]]`.

**P3.** Merge two dictionaries of counts, summing shared keys, without mutating
either input.

**P4.** Read a log file lazily and return the five most common ERROR messages.

**P5.** Write a `retry` decorator with exponential backoff, with the sleep
function injected so the tests do not wait.

**P6.** Given a list of `(start, end)` intervals, merge the overlapping ones.

**P7.** Implement a fixed-size ring buffer with `push` and `latest(k)`, and a
counter of how many items it dropped.

**P8.** Given nested dictionaries from a config file, write `flatten(d)`
producing `{"a.b.c": 1}`-style flat keys. Then write `diff(old, new)` reporting
keys added, removed and changed.

P8 is the one I would most expect on this program: it is a real tech-refresh
task, proving a configuration migration changed exactly what was intended.

## 11. Interview questions, with answers

1. **List vs tuple?** Tuple is immutable and therefore hashable, so it can be a
   dict key or set member. A tuple signals fixed structure; a list signals a
   collection that may grow.
2. **`is` vs `==`?** Identity versus value. Use `is` only for `None`, `True`,
   `False`.
3. **How does a dict work, and what does it cost?** A hash table. Average O(1)
   lookup, insert and delete. Insertion-ordered since 3.7 as a language
   guarantee. Keys must be hashable, so immutable.
4. **Shallow vs deep copy?** A shallow copy duplicates the container and shares
   the contents; a deep copy recursively duplicates everything. Deep copies are
   expensive.
5. **What is the mutable default argument bug?** Defaults are evaluated once at
   function definition, so a mutable default is shared across calls. Use `None`.
6. **What is the GIL and when does it matter?** Only one thread runs Python
   bytecode at a time. Threads help I/O-bound work; use processes for CPU-bound
   work.
7. **Generator vs list?** Lazy and constant-memory versus eager and re-usable.
   Give the 40 GB log example.
8. **What is a decorator?** A function that takes a function and returns a
   replacement, used for cross-cutting concerns. Be ready to write `retry`.
9. **What is a context manager?** An object with setup and teardown that runs
   the teardown even on an exception. `with` uses it; `@contextmanager` writes
   one.
10. **Why define `__hash__` when you define `__eq__`?** Objects that compare
    equal must hash equal, or they get lost in sets and dicts.
11. **How do you test code with no tests?** Characterization tests that pin
    current behavior, then find a seam, inject the dependency, then refactor.
    See [lesson 11](testing-ci.html).
12. **How do you test time-dependent code?** Inject the clock. Never
    `time.sleep` in a test.
13. **How much coverage is enough?** It finds gaps, it does not measure
    quality. Branch coverage beats line coverage. Set a floor that cannot
    regress.
14. **How do you find a performance problem?** `cProfile` to locate it,
    `timeit` to compare a fix, measure both sides. Check for a membership test
    inside a loop first.
15. **How do you manage dependencies?** Virtual environment, exact pins, a
    lockfile, and continuous vulnerability scanning in the pipeline.
