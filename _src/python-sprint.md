# 4. The four-hour Python sprint

Read this first, before the clock starts.

**You cannot become a Python engineer in four hours.** Anyone who tells you
otherwise is selling something. What you can do in four hours, if you spend
them well, is become a Python engineer who has only been doing it for four
hours. That is a genuinely different thing from where you are now, and it is
enough to write a working tool, pass a screening exercise, and hold a technical
conversation without bluffing.

The way we are going to do it is not by covering the language. It is by
**building one real program**, in six stages, and learning each piece of Python
at the moment the program needs it. Knowledge you reach for sticks. Knowledge
you read slides off does not.

The program is a log analyser: it reads sensor detection records, survives
corrupt input, aggregates per sensor, ranks them, and ships as a proper
command-line tool with a test suite. That is not a toy. It is a smaller version
of what the job actually is.

[Lesson 10](python.html) and [lesson 11](python-practice.html) are the thorough
treatment. This lesson is the sprint. Do the sprint first if time is short; do
it first anyway if you learn better by building than by reading.

## The rules

I am going to be strict about these because they are what makes four hours
work rather than feel like work.

1. **Type everything. Never paste.** Typing is how motor memory forms. Pasting
   produces the feeling of learning with none of it.
2. **Run everything.** After every block, run the program. If it breaks, fix it
   before moving on. A broken program at minute 40 becomes an unfixable program
   at minute 90.
3. **Break things on purpose.** Where I say "now break it," do it. Seeing the
   error is worth more than avoiding it.
4. **Keep a REPL open in a second window** the entire four hours. Any time you
   are unsure what something does, try it there rather than wondering.
5. **Respect the clock.** If a block runs over, move on anyway. You can come
   back. Falling behind on hour one and abandoning at hour three is the
   failure mode.
6. **Do not look things up.** Everything you need is in this lesson. Searching
   breaks the flow and costs ten minutes each time.

Take a five minute break at the end of each hour. Actually take it.

## What I am deliberately cutting, and why

A good instructor tells you what you are not learning, so you stop worrying
about it.

| Cut | Why |
| --- | --- |
| Inheritance and class hierarchies | You will read them more than write them. Composition covers the first year. |
| `async` / `await` | A large topic that earns nothing in four hours. |
| Metaclasses, descriptors, `__slots__` | Real, rare, and never asked of a new engineer. |
| Comprehension gymnastics | One loop and one filter is all that is readable anyway. |
| Most of the standard library | You will learn modules when you need them. |
| Type checking with `mypy` | Worth doing on day three, not today. |
| Virtual environment theory | We use one. We do not study it. |

If it is not in this lesson, it is not needed today. That is the deal.

## Setup: ten minutes, before the clock starts

Do this now. Do not start the four hours until it works.

```bash
mkdir sprint && cd sprint
python3 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
python -m pip install pytest
python -V                         # want 3.10 or newer
```

Then create the data file you will work with all session. Type it, or save it
from any editor as `detections.csv`:

```
# sensor_id,timestamp,confidence
RDR-1,1000,0.92
RDR-1,1001,0.88
RDR-2,1002,0.41
RDR-1,1003,0.95
RDR-2,1004,0.38
RDR-3,1005,0.77
RDR-2,1006,notanumber
RDR-3,1007,0.81
BADLINE
RDR-1,1008,0.90
RDR-3,1009,0.79
RDR-2,1010,0.44
```

Note that it contains deliberate garbage: a line with a non-numeric confidence
and a line with no commas at all. **Real data is always like this.** A parser
that only handles clean input is a parser that will fail in the lab.

Now start the clock.

---

## Hour 1: data in, answer out

The single most valuable thing a Python engineer does is turn messy input into
a useful answer. Everything else is decoration. We are going to do exactly that
in the first hour, and pick up the language on the way.

### 0:00 to 0:10 — The REPL is your instrument

```bash
python3
```

You get `>>>`. That is Python's prompt, waiting. Type an expression; it answers.

```python
>>> 2 + 2
4
>>> "radar" + "-1"
'radar-1'
>>> len("radar-1")
7
>>> name = "radar-1"
>>> name.upper()
'RADAR-1'
```

Three things just happened that matter.

**`=` binds a name to a value.** `name = "radar-1"` does not declare a type and
does not reserve a box. It attaches the label `name` to a string object.

**`.upper()` is a method**: a function that belongs to a value. Every value in
Python carries its own methods, and the dot is how you reach them.

**The REPL printed the result.** In a script, results are not printed unless you
say `print(...)`. This trips everyone up once.

Now the two commands that replace a search engine for the rest of your career:

```python
>>> type(name)
<class 'str'>
>>> dir(name)
[..., 'split', 'startswith', 'strip', 'title', 'upper', ...]
```

`type` tells you what something is. `dir` lists everything it can do. When you
are stuck, ask the object.

**Do now, two minutes:** in the REPL, make a string, and find three methods on
it with `dir` that you have never used. Try one.

### 0:10 to 0:30 — The five things that carry eighty percent

Almost all working Python is these five, combined. Type every line.

#### Strings, and turning text into fields

```python
>>> line = "RDR-1,1000,0.92"
>>> line.split(",")
['RDR-1', '1000', '0.92']
```

`split` is the single most important method in log processing. It turns one
line of text into a **list** of pieces.

```python
>>> parts = line.split(",")
>>> parts[0]
'RDR-1'
>>> parts[2]
'0.92'
```

Positions start at **zero**. `parts[0]` is the first. This is universal and
worth burning in now.

```python
>>> "  messy  ".strip()
'messy'
>>> float("0.92")
0.92
>>> int("1000")
1000
```

**Everything read from a file is text.** `"0.92"` is a string, not a number. You
must convert it before doing arithmetic, and `float()` and `int()` are how.
Forgetting this is the most common beginner bug there is.

#### Lists: ordered things

```python
>>> sensors = ["RDR-1", "RDR-2"]
>>> sensors.append("RDR-3")
>>> sensors
['RDR-1', 'RDR-2', 'RDR-3']
>>> len(sensors)
3
>>> sensors[0]
'RDR-1'
>>> sensors[-1]        # negative counts from the end
'RDR-3'
```

#### Dicts: things looked up by name

This is the one that unlocks real work.

```python
>>> counts = {}
>>> counts["RDR-1"] = 4
>>> counts["RDR-2"] = 3
>>> counts
{'RDR-1': 4, 'RDR-2': 3}
>>> counts["RDR-1"]
4
```

A **dict** maps keys to values. Think of it as a lookup table. The critical
method:

```python
>>> counts.get("RDR-9")          # absent: returns None, no error
>>> counts.get("RDR-9", 0)       # absent: returns the default you gave
0
>>> counts["RDR-9"]              # absent: this CRASHES
KeyError: 'RDR-9'
```

**`.get(key, default)` is how you count things you have not seen before**, and
you will use it in ten minutes:

```python
>>> counts["RDR-9"] = counts.get("RDR-9", 0) + 1
>>> counts["RDR-9"]
1
```

Read that line until it is obvious: take the current count or zero if there
isn't one, add one, store it back.

#### Loops

```python
>>> for sensor in sensors:
...     print(sensor)
...
RDR-1
RDR-2
RDR-3
```

In the REPL, the `...` means Python is waiting for the indented block; press
Enter on a blank line to finish it.

A `for` loop walks the **items**, not the indices. There is no counter to
manage. Note the colon and the indentation: **indentation is the syntax in
Python**, not a style choice. Four spaces.

#### Conditionals

```python
>>> confidence = 0.41
>>> if confidence >= 0.8:
...     print("high")
... elif confidence >= 0.5:
...     print("medium")
... else:
...     print("low")
...
low
```

`elif` is "else if." And one enormously useful Python habit:

```python
>>> if not sensors:        # "if the list is empty"
...     print("nothing to do")
```

An empty list, empty string, empty dict, zero and `None` all count as false.
That is called truthiness and it makes conditions read like English.

**Checkpoint, 0:30.** Without looking back, in the REPL: split
`"A,10,0.5"` on commas, convert the third field to a float, and add it to a
dict under the key from the first field, using `.get`. If that took more than
two minutes, redo the dict block above before continuing.

### 0:30 to 0:50 — Version 1: a real program

Leave the REPL (`exit()`). Make a file called `v2.py` and type this. All of it.

```python
totals = {}
counts = {}
skipped = 0

with open("detections.csv", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split(",")
        if len(parts) != 3:
            skipped += 1
            continue

        sensor_id = parts[0]
        try:
            confidence = float(parts[2])
        except ValueError:
            skipped += 1
            continue

        totals[sensor_id] = totals.get(sensor_id, 0.0) + confidence
        counts[sensor_id] = counts.get(sensor_id, 0) + 1

for sensor_id in sorted(totals):
    average = totals[sensor_id] / counts[sensor_id]
    print(f"{sensor_id:<8} {counts[sensor_id]:>3} readings   avg {average:.3f}")

print(f"\nskipped {skipped} bad lines")
```

Run it:

```bash
python3 v2.py
```

```
RDR-1      4 readings   avg 0.912
RDR-2      3 readings   avg 0.410
RDR-3      3 readings   avg 0.790

skipped 2 bad lines
```

**You have written a working data processing tool in twenty-five lines.** Now
let us go through what is new, because five important things just appeared.

**`with open(...) as f:`** opens the file and guarantees it gets closed, even if
the code inside raises. Always open files this way. Always pass
`encoding="utf-8"`, or the same code reads differently on Linux and Windows,
which is a genuine integration bug and not a hypothetical one.

**`for line in f:`** reads the file **one line at a time**, not all at once.
That means this program handles a 40 GB log on a laptop. Say that sentence in
an interview; it is the difference between a script and an engineer's script.

**`continue`** skips to the next iteration. It is how you filter while you
parse, and it keeps the code flat instead of nesting three `if`s deep.

**`try` / `except ValueError`** catches a failure and keeps going.
`float("notanumber")` raises `ValueError`. Without the `try`, one corrupt line
kills the whole run. With it, we count the line and continue. That is the right
behaviour for ingest code, and the counting is not optional: **a program that
silently discards data is worse than one that crashes**, because the crash gets
investigated.

**f-strings** build text from values. The `f` prefix means "evaluate what is in
the braces." The bits after the colons are formatting: `:<8` means left-align in
eight characters, `:>3` right-align in three, `:.3f` means three decimal
places. That is how you get columns that line up.

**Do now, five minutes.** Break it deliberately and read each error:

1. Delete the `try`/`except` (keep the `float` line, unindent it). Run it. Read
   the `ValueError` traceback bottom-up: the last line is the error, the lines
   above are how you got there.
2. Put it back. Now change `detections.csv` to `nope.csv`. Run it. That is
   `FileNotFoundError`.
3. Put it back. Change `parts[2]` to `parts[5]`. Run it. That is `IndexError`.

Those three errors are most of what you will ever see. Meeting them on purpose
now means recognising them instantly later.

### 0:50 to 1:00 — Checkpoint and rest

Close the file. On a blank page, from memory, write the six lines that: open a
file, loop its lines, strip whitespace, skip blanks, split on commas, and add
to a dict with `.get`.

Check against the program. Whatever you got wrong, retype that part twice.

**Take five minutes off.** Stand up.

---

## Hour 2: turning a script into code

What you have is a script. It works and it is unmaintainable: one long block,
nothing reusable, nothing testable. This hour turns it into code.

### 1:00 to 1:25 — Functions

A **function** is a named piece of logic that takes inputs and returns a result.

```python
def average(values):
    """Return the mean of a list of numbers, or None if empty."""
    if not values:
        return None
    return sum(values) / len(values)
```

`def`, the name, the parameters in parentheses, a colon, the indented body. The
string on the first line is a **docstring**: documentation that travels with the
function. `return` sends a value back and exits immediately.

Try it in the REPL:

```python
>>> average([1, 2, 3])
2.0
>>> average([]) is None
True
```

**Why functions matter more than reuse.** Three reasons, in order of
importance:

1. **A function is the unit you can test.** Logic that is not in a function is
   logic you cannot write a test for. Given what this job is, that is the whole
   argument.
2. **A name is documentation.** `rank(stats)` tells a reader what a block does
   in a way that eight lines of loop never will.
3. **Isolation.** A bug lives inside one function instead of anywhere in a
   hundred-line script.

Arguments with defaults:

```python
def rank(stats, top=None, min_confidence=0.0):
    ...
```

`top` and `min_confidence` are optional. Callers can say `rank(stats)` or
`rank(stats, top=3)`. **Pass numbers and booleans by keyword** at the call site:
`rank(stats, 3)` tells a reader nothing, `rank(stats, top=3)` tells them
everything.

One trap, because it is asked in interviews and it does bite:

```python
def add(item, bucket=[]):      # WRONG. The default list is created ONCE
    bucket.append(item)
    return bucket

def add(item, bucket=None):    # RIGHT
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

**Never use a mutable default argument.** Use `None` and build it inside.

**Do now, ten minutes.** Rewrite your program with three functions:
`load(lines)` returning detections and a skip count, `summarise(detections)`
returning a dict, and a loop that prints. Do not look at the final version
below. Struggle with it; that is the point. Run it and confirm the output is
unchanged.

### 1:25 to 1:45 — Errors, properly

You have used `try`/`except`. Now the engineering around it.

**Raise your own errors at the boundary.** When a function is handed something
invalid, say so immediately:

```python
def parse_line(line):
    parts = line.split(",")
    if len(parts) != 3:
        raise ValueError(f"expected 3 fields, got {len(parts)}")
    ...
```

**Validate where data enters, and fail loudly.** A bad value rejected at the
boundary produces an error naming the real problem. The same value accepted and
passed along produces a baffling failure somewhere else, ten minutes later, in
code that is not at fault. This single habit separates code that is debuggable
from code that is not.

**Catch narrowly.**

```python
try:
    detections.append(parse_line(line))
except ValueError as err:          # 'as err' captures the exception object
    log.debug("skipping %r: %s", line, err)
    skipped += 1
```

Catch the exception you expect, not everything. A bare `except:` swallows
genuine programming errors and Ctrl-C, and turns a visible bug into silently
wrong output. An empty `except: pass` is the worst two lines in Python. **If you
catch something, do something**: count it, log it, convert it, or re-raise it.

**Reading a traceback.** Bottom-up, always. The last line is the error type and
message. The line above it is where it happened. Above that is the chain of
calls that got you there. Beginners read from the top and get lost.

The errors you will actually meet:

| Error | What it means |
| --- | --- |
| `NameError` | You used a name that does not exist. Usually a typo, or an import you forgot. |
| `TypeError` | Wrong type for the operation. `"5" + 3`. |
| `ValueError` | Right type, unusable value. `int("abc")`. |
| `KeyError` | Dict key not present. Use `.get`. |
| `IndexError` | List index out of range. |
| `AttributeError` | No such method or attribute. On `NoneType`, it almost always means a function returned `None` when you expected an object. |
| `IndentationError` | Your indentation is inconsistent. Never mix tabs and spaces. |
| `FileNotFoundError` | The path is wrong, or you are in the wrong directory. |
| `ModuleNotFoundError` | Not installed, or the virtual environment is not active. |
| `ZeroDivisionError` | Usually an empty collection you did not check for. |

### 1:45 to 2:00 — Checkpoint and rest

Add validation to your `parse_line`: reject an empty sensor id, and reject a
confidence outside zero to one. Run the program. The bad-line count should go
up if you add a bad row to the CSV to prove it.

**Break it:** make `parse_line` raise a `ValueError` on a *good* line and watch
your skip counter climb. Fix it. That is the debugging loop in miniature.

**Five minutes off.**

---

## Hour 3: the part that makes you an engineer

Anyone can write a script that works today. An engineer writes one you can
change in six months without fear. That is what this hour is.

### 2:00 to 2:35 — Tests

This is the highest-value thirty-five minutes in the sprint, and it is the part
of the job description this program is actually about.

**Why.** Python is interpreted, so a typo on an error path is not found until
that path runs. On a fielded system, the alternative discovery mechanism is the
integration lab, which is the scarcest resource on the programme. **Every defect
a unit test catches is a lab slot you did not consume.** That is the argument.
It is much stronger than "tests are good practice," and it is the one to make in
an interview.

**A test is a function whose name starts with `test_`, containing an `assert`.**

`assert` means "this had better be true." If it is, nothing happens at all. If
it is not, it raises `AssertionError`.

```python
>>> assert 1 + 1 == 2        # true: silence
>>> assert 1 + 1 == 3        # false
AssertionError
```

Silence means pass. That is why a passing test suite is quiet.

Make a file `test_sensorstat.py` next to your program:

```python
import pytest

from sensorstat import parse_line, load, summarise


def test_parses_a_good_line():
    d = parse_line("RDR-1,1000,0.92")
    assert d.sensor_id == "RDR-1"
    assert d.confidence == 0.92


def test_rejects_a_line_with_too_few_fields():
    with pytest.raises(ValueError):
        parse_line("RDR-1,1000")


def test_load_counts_bad_lines_and_keeps_going():
    detections, skipped = load(["RDR-1,1,0.5", "GARBAGE", "RDR-2,2,0.6"])
    assert len(detections) == 2
    assert skipped == 1


def test_load_handles_empty_input():
    assert load([]) == ([], 0)
```

Run it:

```bash
pytest -q
```

`pytest` finds files named `test_*.py`, finds functions named `test_*`, runs
them, and reports. When an assertion fails it prints the actual values, which is
why plain `assert` is enough.

**`with pytest.raises(ValueError):`** passes only if the block raises that
error. It is how you test that bad input is rejected. If the code wrongly
accepts it, the test fails.

#### What to test, which is the actual skill

Given any function, ask for these. **Say this list out loud in an interview even
when you are not asked**, because it is what separates a senior answer from a
correct one:

- the normal case
- empty input
- a single item
- duplicates and ties
- malformed input
- boundaries: zero, one, and either side of a threshold
- the error path: does it raise what it should?

#### Table-driven tests

When the same logic needs many cases, do not write ten near-identical
functions:

```python
@pytest.mark.parametrize("bad", [
    "RDR-1,1000",             # too few fields
    "RDR-1,1000,0.9,extra",   # too many
    ",1000,0.9",              # empty sensor id
    "RDR-1,notanint,0.9",     # bad timestamp
    "RDR-1,1000,notafloat",   # bad confidence
    "RDR-1,1000,1.5",         # out of range
])
def test_rejects_bad_lines(bad):
    with pytest.raises(ValueError):
        parse_line(bad)
```

That is six tests from one function, each named by its input so a failure tells
you which case broke.

#### The check that matters most

**Break your code on purpose and confirm a test goes red.** A test that passes
against broken code is worse than no test, because it buys false confidence. Do
this now: change `!= 3` to `!= 4` in `parse_line` and run `pytest`. Watch it
fail. Put it back.

**Do now, fifteen minutes.** Write tests for `summarise`: that it averages
correctly, and that summarising nothing gives an empty result. Then one for your
ranking that proves ties break by sensor id. That last one matters because a
non-deterministic result is untestable, and making output deterministic is a
design decision you should be able to defend.

### 2:35 to 2:55 — Dataclasses

Right now a detection is three loose variables, or a list of strings. That is
fragile: nothing stops a typo, and nothing validates anything.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Detection:
    """One reading from one sensor."""

    sensor_id: str
    timestamp: int
    confidence: float
```

That is the whole definition. You now get:

```python
>>> d = Detection("RDR-1", 1000, 0.92)
>>> d.sensor_id
'RDR-1'
>>> d
Detection(sensor_id='RDR-1', timestamp=1000, confidence=0.92)
>>> d == Detection("RDR-1", 1000, 0.92)
True
```

`@dataclass` writes the constructor, a readable `repr`, and value equality from
the field declarations. `frozen=True` makes it unchangeable after creation,
which means it is safe to pass anywhere without worrying that someone modifies
it behind your back.

**Why this beats a dict.** `d.sensor_id` is checked; `d["sensr_id"]` in a dict
silently gives you a `KeyError` at best and a wrong answer at worst. The
`repr` means a failing test shows you the actual object instead of
`<object at 0x7f3a...>`. And equality makes tests read directly:
`assert d == Detection("RDR-1", 1000, 0.92)`.

**Use a dataclass for things that are mostly data**, which is most of what flows
through a system like this. Write a full class only when behaviour dominates.

**Do now, ten minutes.** Convert `parse_line` to return a `Detection`. Update
your tests to compare whole objects. Run everything.

### 2:55 to 3:00 — Rest

Five minutes. You are through the hard part.

---

## Hour 4: shippable

### 3:00 to 3:20 — The idiom pack

These twelve lines are most of the difference between code that reads as
Python and code that reads as C written in Python. Type each one, and use at
least three in your program.

```python
# 1. Sort by a computed key. The workhorse.
sensors.sort(key=lambda s: s.average_confidence)

# 2. Sort by two things: first ascending, second descending.
sensors.sort(key=lambda s: (s.average_confidence, s.sensor_id))

# 3. Pick the extreme without sorting.
worst = min(sensors, key=lambda s: s.average_confidence)

# 4. Build a new list from an old one: a comprehension.
ids = [s.sensor_id for s in sensors]

# 5. Filter while building.
poor = [s for s in sensors if s.average_confidence < 0.5]

# 6. Count things, without the .get dance.
from collections import Counter
Counter(sensor_ids).most_common(3)

# 7. Group things, without the "is the key there yet" check.
from collections import defaultdict
groups = defaultdict(list)
for d in detections:
    groups[d.sensor_id].append(d)

# 8. Index and item together.
for i, sensor in enumerate(sensors, start=1):
    print(f"{i}. {sensor}")

# 9. Walk two sequences at once.
for sensor, count in zip(sensors, counts):
    ...

# 10. Unpack a tuple into names.
detections, skipped = load(lines)

# 11. Deduplicate.
unique = set(sensor_ids)

# 12. Test membership fast. A set, not a list.
if sensor_id in known_sensors:      # set: instant. list: scans the whole thing.
    ...
```

Number twelve deserves a note. Replacing an `in list` check inside a loop with
an `in set` check turns a slow program into a fast one, and it is the single
most common real performance fix in Python. Interviewers notice when you know
it.

Number one deserves a note too. `key=lambda s: ...` means "sort by this
computed value." The two-element tuple in number two sorts by the first, then
breaks ties with the second. Those two lines answer a large share of "sort by X
then Y" problems.

### 3:20 to 3:45 — A real command-line tool

A script with a hard-coded filename is a script. A tool takes arguments.

```python
import argparse
import logging
import sys
from pathlib import Path

log = logging.getLogger("sensorstat")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Summarise sensor detection logs.")
    parser.add_argument("path", type=Path, help="CSV file of detections")
    parser.add_argument("--min-confidence", type=float, default=0.0,
                        help="only report sensors at or above this average")
    parser.add_argument("--top", type=int, help="only show this many sensors")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="log each skipped line")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    try:
        with args.path.open(encoding="utf-8") as f:
            detections, skipped = load(f)
    except FileNotFoundError:
        log.error("no such file: %s", args.path)
        return 2

    stats = summarise(detections)
    print(format_report(rank(stats, args.top, args.min_confidence), skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Four new things, each earning its place.

**`argparse`** builds a command-line interface from declarations. You get
`--help` for free, type conversion for free, and errors on bad input for free.

```bash
python3 sensorstat.py --help
python3 sensorstat.py detections.csv --min-confidence 0.5 --top 2
```

**`logging` instead of `print`.** `print` is for the answer, which is what the
user asked for. `logging` is for everything else: diagnostics, warnings,
failures. Levels mean you can turn detail up when investigating and down in
normal use, without editing code. Note `log.debug("skipping %r: %s", line, err)`
uses `%s` placeholders rather than an f-string, so the formatting work is
skipped entirely when the level is off.

**`if __name__ == "__main__":`** means "only run this when executed as a
program, not when imported." Without it, your test file importing the module
would run the whole tool as a side effect. **This line is what makes your code
both a runnable program and an importable, testable library**, which is exactly
why every one of your functions was testable in hour three.

**Exit codes.** `return 0` for success, non-zero for failure, handed to
`sys.exit`. That is how a shell script or a CI pipeline knows whether your tool
worked. Scripts that always exit zero cannot be automated around.

**Do now, fifteen minutes.** Wire your program up this way. Run it with
`--help`, with a real file, with a missing file, and check the exit code with
`echo $?`.

### 3:45 to 3:55 — Debugging

Three tools, in the order you should reach for them.

**Read the traceback.** Bottom-up. You have done this three times already.

**Print the values, with names:**

```python
print(f"{sensor_id=} {confidence=}")
```

The `=` inside the braces prints both the expression and its value. It costs
nothing and it answers most questions.

**Stop the program and look around:**

```python
breakpoint()
```

Execution halts there and gives you a prompt inside the running program. `p
expr` prints an expression, `n` runs the next line, `c` continues, `q` quits.
Ten minutes learning those four commands saves many hours of adding and
removing print statements.

**Do now:** put a `breakpoint()` inside your parsing loop, run the program, and
print `line` and `parts` at the prompt. Then `c` a few times to watch it move
through the file. Remove it.

### 3:55 to 4:00 — Self-test

Close everything. On a blank page, from memory, write:

1. Open a file and loop over its lines, skipping blanks and comments.
2. Split a line and convert a field to a float inside a `try`, counting
   failures.
3. Add to a dict using `.get` with a default.
4. Sort a list of objects by a computed value, descending.
5. A function with a docstring and a default argument.
6. A test that asserts a function raises `ValueError` on bad input.

If you can write all six unaided, you have got what the four hours were for.
Anything you cannot write, retype that section twice tomorrow.

---

## The finished program

This is where you should have arrived. Every line of it has been run and every
test passes.

```python
"""Summarise sensor detection logs.

Usage:
    python3 sensorstat.py detections.csv
    python3 sensorstat.py detections.csv --min-confidence 0.5 --top 2
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger("sensorstat")


@dataclass(frozen=True)
class Detection:
    """One reading from one sensor."""

    sensor_id: str
    timestamp: int
    confidence: float


@dataclass
class SensorStats:
    """What we know about one sensor after reading the whole file."""

    sensor_id: str
    count: int
    total_confidence: float

    @property
    def average_confidence(self) -> float:
        return self.total_confidence / self.count


def parse_line(line: str) -> Detection:
    """Turn one CSV line into a Detection.

    Raises ValueError if the line is not a valid record.
    """
    parts = line.split(",")
    if len(parts) != 3:
        raise ValueError(f"expected 3 fields, got {len(parts)}")

    sensor_id = parts[0].strip()
    if not sensor_id:
        raise ValueError("empty sensor id")

    timestamp = int(parts[1])
    confidence = float(parts[2])
    if not 0.0 <= confidence <= 1.0:
        raise ValueError(f"confidence out of range: {confidence}")

    return Detection(sensor_id, timestamp, confidence)


def load(lines) -> tuple[list[Detection], int]:
    """Parse every line, skipping blanks, comments and bad records.

    Returns the good detections and how many lines were skipped as bad. One
    corrupt record must not stop the run, but silence about it is worse than
    the corruption, so we count.
    """
    detections = []
    skipped = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            detections.append(parse_line(line))
        except ValueError as err:
            log.debug("skipping %r: %s", line, err)
            skipped += 1

    return detections, skipped


def summarise(detections) -> dict[str, SensorStats]:
    """Aggregate detections per sensor."""
    stats: dict[str, SensorStats] = {}

    for d in detections:
        if d.sensor_id not in stats:
            stats[d.sensor_id] = SensorStats(d.sensor_id, 0, 0.0)
        entry = stats[d.sensor_id]
        entry.count += 1
        entry.total_confidence += d.confidence

    return stats


def rank(stats, top=None, min_confidence=0.0) -> list[SensorStats]:
    """Sensors worst-first by average confidence, filtered and limited."""
    eligible = [s for s in stats.values() if s.average_confidence >= min_confidence]
    eligible.sort(key=lambda s: (s.average_confidence, s.sensor_id))
    return eligible[:top] if top else eligible


def format_report(ranked, skipped) -> str:
    """Build the printable report. Returns a string so it can be tested."""
    if not ranked:
        return "no sensors matched"

    lines = [f"{'sensor':<10} {'count':>6} {'avg':>8}"]
    lines.append("-" * 26)
    for s in ranked:
        lines.append(f"{s.sensor_id:<10} {s.count:>6} {s.average_confidence:>8.3f}")
    lines.append("")
    plural = "" if len(ranked) == 1 else "s"
    lines.append(f"{len(ranked)} sensor{plural}, {skipped} bad lines skipped")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Summarise sensor detection logs.")
    parser.add_argument("path", type=Path, help="CSV file of detections")
    parser.add_argument("--min-confidence", type=float, default=0.0,
                        help="only report sensors at or above this average")
    parser.add_argument("--top", type=int, help="only show this many sensors")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="log each skipped line")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    try:
        with args.path.open(encoding="utf-8") as f:
            detections, skipped = load(f)
    except FileNotFoundError:
        log.error("no such file: %s", args.path)
        return 2

    stats = summarise(detections)
    print(format_report(rank(stats, args.top, args.min_confidence), skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Two details in there worth naming because they are deliberate.

**`format_report` returns a string rather than printing.** That one decision is
what makes the report testable. A function that prints can only be tested by
capturing stdout, which is awkward; a function that returns text can be
asserted on directly. **Push side effects to the edges and keep the middle
pure** is a design rule you can state in an interview, and this is it in two
lines.

**`@property` on `average_confidence`** lets you write `s.average_confidence`
rather than `s.average_confidence()`. It is a computed value that reads like a
stored one. Use it for cheap derived values.

## The test suite

```python
import pytest

from sensorstat import (
    Detection, SensorStats, format_report, load, parse_line, rank, summarise,
)


def test_parses_a_good_line():
    assert parse_line("RDR-1,1000,0.92") == Detection("RDR-1", 1000, 0.92)


def test_tolerates_surrounding_whitespace():
    assert parse_line(" RDR-1 ,1000,0.92").sensor_id == "RDR-1"


@pytest.mark.parametrize("bad", [
    "RDR-1,1000",             # too few fields
    "RDR-1,1000,0.9,extra",   # too many
    ",1000,0.9",              # empty sensor id
    "RDR-1,notanint,0.9",     # bad timestamp
    "RDR-1,1000,notafloat",   # bad confidence
    "RDR-1,1000,1.5",         # out of range
    "RDR-1,1000,-0.1",        # out of range
])
def test_rejects_bad_lines(bad):
    with pytest.raises(ValueError):
        parse_line(bad)


def test_load_skips_blanks_and_comments_without_counting_them():
    detections, skipped = load(["", "   ", "# header", "RDR-1,1,0.5"])
    assert len(detections) == 1
    assert skipped == 0, "comments are not errors"


def test_load_counts_bad_lines_and_keeps_going():
    detections, skipped = load(["RDR-1,1,0.5", "GARBAGE", "RDR-2,2,0.6"])
    assert len(detections) == 2
    assert skipped == 1


def test_load_handles_empty_input():
    assert load([]) == ([], 0)


def test_summarise_averages_per_sensor():
    stats = summarise([
        Detection("A", 1, 0.2), Detection("A", 2, 0.4), Detection("B", 3, 0.9),
    ])
    assert stats["A"].count == 2
    assert stats["A"].average_confidence == pytest.approx(0.3)


def test_summarise_of_nothing_is_empty():
    assert summarise([]) == {}


def _stats(*pairs):
    return {sid: SensorStats(sid, 1, conf) for sid, conf in pairs}


def test_rank_puts_the_worst_first():
    ranked = rank(_stats(("A", 0.9), ("B", 0.2), ("C", 0.5)))
    assert [s.sensor_id for s in ranked] == ["B", "C", "A"]


def test_rank_breaks_ties_by_sensor_id_for_determinism():
    assert [s.sensor_id for s in rank(_stats(("B", 0.5), ("A", 0.5)))] == ["A", "B"]


def test_rank_applies_the_minimum():
    ranked = rank(_stats(("A", 0.9), ("B", 0.2)), min_confidence=0.5)
    assert [s.sensor_id for s in ranked] == ["A"]


def test_rank_limits_to_top_n():
    ranked = rank(_stats(("A", 0.9), ("B", 0.2), ("C", 0.5)), top=2)
    assert [s.sensor_id for s in ranked] == ["B", "C"]


def test_report_says_so_when_nothing_matched():
    assert format_report([], skipped=0) == "no sensors matched"


def test_report_uses_the_singular_for_one_sensor():
    assert "1 sensor," in format_report(rank(_stats(("A", 0.9))), skipped=0)


def test_report_mentions_the_skipped_count():
    assert "7 bad lines skipped" in format_report(rank(_stats(("A", 0.9))), skipped=7)
```

```bash
$ pytest -q
.....................                                        [100%]
21 passed in 0.03s
```

**Twenty-one tests from six functions and two dataclasses.** That ratio is
normal and healthy: most of the tests are cheap edge cases, and the cheap edge
cases are the ones that catch real defects.

## What you can now honestly claim

Be precise about this, because overclaiming in an interview is fatal and
underclaiming costs you the job.

**You can say:** you write Python, you parse and aggregate real data, you handle
malformed input deliberately, you structure code into tested functions, you use
pytest including parametrised tests and exception tests, you build command-line
tools with argparse and logging, and you understand why testable code is
structured the way it is.

**Do not say:** that you are experienced. If asked directly how long you have
been writing Python, answer honestly and immediately pivot to what you built:
*"Not long, and I have been deliberate about it. I built a log ingest tool with
a proper test suite, and what I took from it is that the design decisions that
make code testable are the same ones that make it maintainable."* That answer is
respected. A bluffed one unravels on the second follow-up.

## If you get another four hours

In this order, because this is the order of return:

1. **[Lesson 10](python.html), sections 3 and 12.** Names and objects, and
   classes. The two things the sprint skipped the theory of.
2. **The [practice repo](../practice/README.html).** Solve the problems in
   `exercises.py` and check yourself with `PREP_TARGET=exercises pytest -q`.
3. **[Lesson 11](python-practice.html), section 7.** Testing in depth: fixtures,
   fakes versus mocks, injecting the clock.
4. **[Lesson 11](python-practice.html), section 2.** Generators. The idea that
   lets you process a file bigger than memory.
5. **Rewrite `sensorstat` from an empty file**, without looking. That is worth
   more than reading anything.

Number five is the real answer. Building the same thing a second time from
nothing is where the knowledge moves from recognised to owned.
