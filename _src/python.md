# 4. Python refresher

The posting lists Python first. Assume the coding round is in Python unless you
are told otherwise. This lesson is the recall pass: type every block, run it,
and change something in it.

Set up first:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip pytest
python -V                        # want 3.10 or newer
```

## 1. Types, mutability, and the trap that gets everyone

```python
a = [1, 2, 3]
b = a                 # same object, not a copy
b.append(4)
print(a)              # [1, 2, 3, 4]

c = a[:]              # shallow copy
c.append(5)
print(a)              # [1, 2, 3, 4]

import copy
d = copy.deepcopy({"nested": [1, 2]})   # when the contents are mutable too
```

Immutable: `int`, `float`, `str`, `bytes`, `tuple`, `frozenset`.
Mutable: `list`, `dict`, `set`, and your own classes by default.

The classic interview trap, and it does get asked:

```python
def add_item(item, bucket=[]):        # WRONG: the default is created once
    bucket.append(item)
    return bucket

print(add_item(1))    # [1]
print(add_item(2))    # [1, 2]  -- surprise

def add_item(item, bucket=None):      # RIGHT
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

Be ready to explain *why*: default arguments are evaluated once, when the
function object is created, not on each call.

## 2. Strings

```python
s = "  Track-4471:ACTIVE:32.5  "
s.strip()                       # 'Track-4471:ACTIVE:32.5'
s.strip().split(":")            # ['Track-4471', 'ACTIVE', '32.5']
"-".join(["a", "b", "c"])       # 'a-b-c'
s.strip().lower().startswith("track")   # True
s.replace("ACTIVE", "DROPPED")

name, state, conf = s.strip().split(":")
float(conf)                     # 32.5

f"{name} is {state} at {float(conf):.1f}%"     # f-strings; know the format spec
f"{3.14159:8.2f}|{42:05d}|{'hi':>10}|{0.87:.1%}"

s2 = "abcdef"
s2[::-1]        # 'fedcba'  -- reverse
s2[1:4]         # 'bcd'
s2[-2:]         # 'ef'
```

Strings are immutable, so building one in a loop with `+=` is O(n^2). Use a list
and `"".join(parts)`. That is a real interview answer.

## 3. Lists, dicts, sets, tuples

```python
xs = [5, 3, 9, 1]
xs.append(7); xs.extend([2, 8]); xs.insert(0, 0)
xs.pop()          # last
xs.pop(0)         # by index, O(n)
xs.remove(9)      # by value, first occurrence
sorted(xs)                       # new list
xs.sort(reverse=True)            # in place
len(xs); sum(xs); min(xs); max(xs)

d = {"radar_a": 12, "radar_b": 7}
d["radar_c"] = 3
d.get("radar_z", 0)              # no KeyError
d.setdefault("radar_z", []).append(1)
for k, v in d.items(): pass
list(d.keys()); list(d.values())
"radar_a" in d                   # O(1)
del d["radar_c"]
d.pop("radar_b", None)

s = {1, 2, 3}
s | {3, 4}       # union        {1,2,3,4}
s & {2, 3, 9}    # intersection {2,3}
s - {1}          # difference   {2,3}
s ^ {3, 4}       # symmetric difference
```

Sorting with a key is the single most common thing you will need:

```python
tracks = [("T3", 5, 0.9), ("T1", 5, 0.4), ("T2", 2, 0.7)]

sorted(tracks, key=lambda t: t[1])                    # by second field
sorted(tracks, key=lambda t: (-t[1], t[0]))           # desc by 2nd, then name
max(tracks, key=lambda t: t[2])                       # ('T3', 5, 0.9)

import operator
sorted(tracks, key=operator.itemgetter(1, 0))
```

Python's sort is stable, which means equal keys keep their original order. Say
that out loud if sorting comes up; it is a small competence signal.

## 4. Comprehensions

```python
nums = [1, 2, 3, 4, 5, 6]
[n * n for n in nums]                        # map
[n for n in nums if n % 2 == 0]              # filter
[n * n for n in nums if n % 2 == 0]          # both
{n: n * n for n in nums}                     # dict comprehension
{n % 3 for n in nums}                        # set comprehension
(n * n for n in nums)                        # generator: lazy, no list built

pairs = [(a, b) for a in "AB" for b in [1, 2]]     # nested loops
flat = [x for row in [[1, 2], [3, 4]] for x in row]
```

Rule of thumb for the interview: one loop and one condition is fine in a
comprehension. Two nested loops plus a condition should be a real `for` loop.
Readability is being assessed.

## 5. Functions

```python
def score(track, *, weight=1.0, floor=0.0):     # keyword-only after *
    return max(track.confidence * weight, floor)

def summarize(*args, **kwargs):
    print(args)      # tuple of positional
    print(kwargs)    # dict of keyword

def parse(line: str) -> tuple[str, float]:      # type hints; use them
    name, value = line.split("=")
    return name.strip(), float(value)
```

Unpacking:

```python
a, b, *rest = [1, 2, 3, 4, 5]      # rest == [3, 4, 5]
first, *_, last = [1, 2, 3, 4]

def area(w, h): return w * h
dims = {"w": 3, "h": 4}
area(**dims)                        # 12
args = (3, 4)
area(*args)                         # 12
```

## 6. Classes

```python
class Track:
    """One system-level estimate of an object."""

    def __init__(self, track_id: str, lat: float, lon: float, alt_m: float):
        self.track_id = track_id
        self.lat = lat
        self.lon = lon
        self.alt_m = alt_m
        self._history: list[tuple[float, float]] = []

    def update(self, lat: float, lon: float) -> None:
        self._history.append((self.lat, self.lon))
        self.lat, self.lon = lat, lon

    @property
    def altitude_ft(self) -> float:
        return self.alt_m * 3.28084

    @staticmethod
    def from_line(line: str) -> "Track":
        tid, lat, lon, alt = line.split(",")
        return Track(tid, float(lat), float(lon), float(alt))

    def __repr__(self) -> str:
        return f"Track({self.track_id!r}, {self.lat}, {self.lon}, {self.alt_m})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Track):
            return NotImplemented
        return self.track_id == other.track_id

    def __hash__(self) -> int:
        return hash(self.track_id)
```

Know these by name: `__init__`, `__repr__`, `__str__`, `__eq__`, `__hash__`,
`__len__`, `__iter__`, `__enter__`/`__exit__`. If you define `__eq__` and want
the object usable in a set or as a dict key, you must define `__hash__` too.
Same rule as Java; see [lesson 5](java.html).

Dataclasses save a lot of typing and read well:

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Detection:
    sensor_id: str
    timestamp: float
    lat: float
    lon: float
    confidence: float = 1.0
    tags: tuple[str, ...] = ()

d = Detection("RDR-1", 1712345678.0, 24.45, 54.37)
d.sensor_id          # works; __init__, __repr__, __eq__ generated for free
```

Inheritance and the abstract interface pattern:

```python
from abc import ABC, abstractmethod

class SensorAdapter(ABC):
    @abstractmethod
    def parse(self, raw: bytes) -> list[Detection]: ...

class LegacyRadarAdapter(SensorAdapter):
    def parse(self, raw: bytes) -> list[Detection]:
        return [Detection(*line.split(b",")) for line in raw.splitlines()]
```

## 7. Errors and resource handling

```python
try:
    value = int(raw)
except ValueError as exc:
    log.warning("bad record %r: %s", raw, exc)
    value = None
except (KeyError, IndexError):
    raise
else:
    process(value)          # runs only if no exception
finally:
    cleanup()               # always runs
```

Custom exceptions, which you will want in real code:

```python
class SensorError(Exception):
    """Base for all sensor-adapter failures."""

class MalformedRecord(SensorError):
    def __init__(self, line: str):
        super().__init__(f"cannot parse: {line[:80]!r}")
        self.line = line
```

Context managers:

```python
with open("tracks.csv", encoding="utf-8") as f:
    for line in f:
        ...
# file is closed even if the loop raises

from contextlib import contextmanager
import time

@contextmanager
def timed(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"{label}: {time.perf_counter() - start:.3f}s")

with timed("parse"):
    parse_everything()
```

Never use a bare `except:`. Catch the exception you expect. If asked why: a bare
except swallows `KeyboardInterrupt` and `SystemExit` and hides real bugs.

## 8. The standard library worth memorizing

```python
from collections import defaultdict, Counter, deque, namedtuple

counts = defaultdict(int)
for w in words: counts[w] += 1

groups = defaultdict(list)
for det in detections: groups[det.sensor_id].append(det)

Counter("mississippi").most_common(2)      # [('i', 4), ('s', 4)]

q = deque([1, 2, 3], maxlen=1000)          # O(1) at both ends
q.appendleft(0); q.append(4); q.popleft()
```

```python
import itertools as it
list(it.chain([1, 2], [3, 4]))             # [1,2,3,4]
list(it.islice(range(100), 5))             # first 5 of a lazy source
list(it.combinations("ABC", 2))            # [('A','B'), ('A','C'), ('B','C')]
list(it.groupby(sorted(rows, key=k), key=k))   # must sort first

import heapq
h = []
heapq.heappush(h, (0.4, "T1")); heapq.heappush(h, (0.9, "T2"))
heapq.heappop(h)                            # smallest first
heapq.nlargest(3, tracks, key=lambda t: t.confidence)
```

```python
import json, csv, os, re, datetime as dt, pathlib

json.loads('{"a": 1}');  json.dumps({"a": 1}, indent=2)
pathlib.Path("logs").glob("*.log")
re.findall(r"TRACK (\d+)", text)
re.sub(r"\s+", " ", text)
dt.datetime.now(dt.timezone.utc).isoformat()
os.environ.get("LOG_LEVEL", "INFO")
```

Logging, because the job is sustainment and they will care:

```python
import logging

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
log = logging.getLogger(__name__)

log.info("processed %d detections from %s", len(dets), sensor_id)   # lazy %-args
log.exception("adapter failed")     # inside an except block: logs the traceback
```

Use `%s` placeholders, not f-strings, in log calls. The formatting is then
skipped entirely when the level is disabled. That is a good detail to mention.

## 9. Generators and iterators

Important for this role because sustainment code often streams large files.

```python
def read_records(path):
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            yield lineno, line

for lineno, line in read_records("big.log"):
    ...          # constant memory regardless of file size
```

Why it matters, in one sentence you can say: a generator produces values lazily,
so you can process a 40 GB log on a machine with 8 GB of RAM.

```python
squares = (n * n for n in range(10_000_000))    # nothing computed yet
next(squares)                                    # 0
sum(1 for line in open("f.log") if "ERROR" in line)   # counts without a list
```

## 10. Concurrency: the GIL question

Expect: *"Does Python do real multithreading?"*

The reference implementation, CPython, has a Global Interpreter Lock. Only one
thread executes Python bytecode at a time. So:

- **I/O-bound work** (network, disk, subprocesses): threads help, because the
  GIL is released during I/O waits.
- **CPU-bound work**: threads do not help. Use `multiprocessing`, or push the
  work into a native library that releases the GIL, or use another language.

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=8) as pool:            # I/O bound
    results = list(pool.map(fetch_status, hostnames))

with ProcessPoolExecutor(max_workers=4) as pool:           # CPU bound
    results = list(pool.map(correlate_chunk, chunks))
```

Basic asyncio, enough to discuss:

```python
import asyncio

async def poll(sensor):
    await asyncio.sleep(0.1)          # stands in for network I/O
    return f"{sensor}: ok"

async def main():
    results = await asyncio.gather(*(poll(s) for s in ["r1", "r2", "r3"]))
    print(results)

asyncio.run(main())
```

Note that free-threaded CPython builds without the GIL exist in recent versions
as an option. If you mention that, be ready to say it is opt-in and not yet the
default for most deployments.

## 11. Testing with pytest

This is the part of Python the job description cares about most.

```python
# tracks.py
def worst_offender(counts: dict[str, int]) -> str | None:
    if not counts:
        return None
    return max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
```

```python
# test_tracks.py
import pytest
from tracks import worst_offender

def test_empty_returns_none():
    assert worst_offender({}) is None

def test_single():
    assert worst_offender({"a": 3}) == "a"

def test_ties_broken_by_name():
    assert worst_offender({"a": 3, "b": 3}) == "b"

@pytest.mark.parametrize("counts,expected", [
    ({"a": 1, "b": 2}, "b"),
    ({"z": 9, "y": 1}, "z"),
])
def test_table(counts, expected):
    assert worst_offender(counts) == expected

def test_raises_on_bad_input():
    with pytest.raises(AttributeError):
        worst_offender(["not", "a", "dict"])
```

Fixtures and temp files:

```python
@pytest.fixture
def sample_log(tmp_path):
    p = tmp_path / "sample.log"
    p.write_text("RDR-1,ok\nRDR-2,fail\n", encoding="utf-8")
    return p

def test_reads_file(sample_log):
    assert count_failures(sample_log) == 1
```

Mocking an external dependency:

```python
from unittest.mock import patch, MagicMock

@patch("myapp.client.requests.get")
def test_status_handles_timeout(mock_get):
    mock_get.side_effect = TimeoutError("no route")
    assert fetch_status("radar-1") == "UNKNOWN"
    mock_get.assert_called_once()
```

Run it:

```bash
pytest -q                        # quiet
pytest -v -k "ties"              # filter by name
pytest --cov=tracks --cov-report=term-missing    # needs pytest-cov
```

## 12. Packaging and environments

Be able to describe how a Python service ships.

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

For a program under configuration control, pin exact versions and commit a
lockfile or a fully pinned `requirements.txt` produced by `pip freeze` or
`pip-compile`. Reproducible builds are not optional here; say so if asked.

## 13. Practice problems

Write each one, then write tests for it. Solutions are in the
[practice repo](../practice/README.html).

**P1.** Given a list of `"sensor_id,timestamp,confidence"` lines, return the
sensor id with the highest average confidence. Ignore malformed lines.

**P2.** Write `chunk(items, n)` returning a list of lists of at most `n` items
each. `chunk([1,2,3,4,5], 2) == [[1,2],[3,4],[5]]`.

**P3.** Merge two dictionaries of counts, summing values for shared keys,
without mutating either input.

**P4.** Read a log file lazily and return the five most common ERROR messages,
where the message is everything after the log level.

**P5.** Write a `Retry` decorator that retries a function up to `n` times with
exponential backoff on a given exception type.

**P6.** Given a list of `(start, end)` intervals, merge the overlapping ones.

**P7.** Implement a fixed-size ring buffer class supporting `push` and
`latest(k)`, using `collections.deque`.

**P8.** Given nested dictionaries from a config file, write `flatten(d)`
producing `{"a.b.c": 1}`-style flat keys.

## 14. Ten questions they might ask about Python

1. **List vs tuple?** Tuple is immutable and hashable, so it can be a dict key
   or set member; list is mutable. Tuples signal fixed structure.
2. **`is` vs `==`?** `is` compares identity, `==` compares value. Use `is` only
   for `None`, `True`, `False`.
3. **How does a dict work?** Hash table. Average O(1) lookup, insert, delete.
   Since 3.7 it preserves insertion order as a language guarantee.
4. **Shallow vs deep copy?** Shallow copies the container, sharing the nested
   objects; deep recursively copies everything.
5. **What is a decorator?** A callable that takes a function and returns a
   replacement, used for cross-cutting concerns like timing, retry, auth. Be
   ready to write one.
6. **Generator vs list?** Generator is lazy and constant-memory, single-pass.
   List is eager, re-iterable, indexable.
7. **What does the GIL mean for you?** See section 10.
8. **`__slots__`?** Declares a fixed attribute set, removes the per-instance
   `__dict__`, saves memory when you have millions of small objects such as
   detections.
9. **How do you handle configuration?** Environment variables for deployment
   differences, a file for structure, never secrets in source. See
   [lesson 13](cyber.html).
10. **How do you find a performance problem?** `cProfile` to find the hot
    function, `timeit` to measure a candidate fix, and measure before and after.
    Do not optimize by intuition.

```python
import cProfile, pstats
cProfile.run("correlate(all_detections)", "prof.out")
pstats.Stats("prof.out").sort_stats("cumulative").print_stats(15)
```
