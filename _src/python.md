# 4. Python foundations

This lesson assumes you know nothing about Python. It builds the language from
the ground up and explains *why* each piece exists, not just what to type. If
you have written code before in another language, read it anyway: several of
Python's core ideas differ from C, Java and C# in ways that cause real bugs
when you assume they are the same.

[Lesson 5](python-practice.html) covers the standard library, testing and the
tooling. Do this one first.

## 1. What Python actually is

**Python is an interpreted, dynamically typed, garbage-collected language.**
Those three words matter, so take them one at a time.

**Interpreted.** In C you compile source code into a machine-code executable
and then run that executable. Python does not work that way. You hand your
source file to a program called the **interpreter**, and it executes your code
directly. The practical consequences:

- You can run code immediately without a build step. The edit-run cycle is
  seconds, not minutes.
- Errors that a compiler would catch before your program ever ran, such as a
  misspelled function name, are only discovered in Python when that line
  actually executes. A typo on an error-handling path can sit undiscovered for
  months. **This is the single strongest argument for automated tests in
  Python**, and it is a good thing to say in an interview.
- Python is slower than compiled languages for raw computation, often by a
  large factor. This rarely matters, because most programs spend their time
  waiting on disk, network or a database rather than computing.

Under the hood the interpreter first compiles your source into **bytecode**, a
compact intermediate form, and then executes that. You will see `.pyc` files
and `__pycache__` directories appear; those are cached bytecode. You never need
to manage them.

**Dynamically typed.** A variable does not have a declared type. The *value*
has a type, and a variable can refer to a string now and a number later.
Compare:

```java
// Java: the type is part of the declaration and cannot change
int count = 5;
count = "hello";     // compiler error
```

```python
# Python: no declaration, and the name can be rebound to anything
count = 5
count = "hello"      # perfectly legal
```

This makes Python fast to write and easy to get wrong. Python is
**strongly** typed as well as dynamically typed, which means it will not
silently coerce unrelated types for you:

```python
>>> "5" + 3
TypeError: can only concatenate str (not "int") to str
```

That error is Python protecting you. JavaScript would have produced `"53"`.

**Garbage-collected.** You never allocate or free memory. When nothing in your
program refers to an object any more, the interpreter reclaims it
automatically. You cannot leak memory the way you can in C, but you *can* hold
on to things longer than you meant to, which looks the same from the outside.

**CPython** is the reference implementation, the one you get from python.org
and from your operating system's package manager. When people say "Python"
they almost always mean CPython. Other implementations exist (PyPy, which is
faster; Jython, on the JVM), but you are unlikely to meet them.

### Which version

Python 2 and Python 3 are incompatible languages that shared a name. Python 2
reached end of life in 2020. If you find Python 2 code on a program like this
one, migrating it is exactly the kind of tech-refresh work the posting
describes.

Use **Python 3.10 or newer**. Check with:

```bash
python3 --version
```

The version matters more than beginners expect, because useful syntax arrived
in specific versions. Type hints like `list[str]` need 3.9, the `match`
statement needs 3.10, and so on.

## 2. Running Python code

There are three ways, and you need all of them.

**The REPL**, or interactive interpreter. Type `python3` with no arguments and
you get a prompt. Every line you type is executed immediately and the result
printed.

```
$ python3
>>> 2 + 2
4
>>> name = "radar"
>>> name.upper()
'RADAR'
>>> exit()
```

REPL stands for read, evaluate, print, loop. **Use it constantly.** When you
cannot remember what a method returns, do not guess and do not search: open a
REPL and try it. This is the single fastest way to rebuild rusty knowledge.

**A script.** Put code in a file ending in `.py` and run it.

```bash
echo 'print("hello")' > hello.py
python3 hello.py
```

**A module.** `python3 -m name` runs an installed module as a program. You will
use this constantly for tools:

```bash
python3 -m pytest          # run the test framework
python3 -m venv .venv      # create a virtual environment
python3 -m http.server     # serve the current directory over HTTP
```

The `-m` form matters because it guarantees you are running the tool from the
Python interpreter you think you are, rather than whatever happens to be first
on your `PATH`. On a machine with several Python installations, which describes
most real machines, that distinction saves hours.

## 3. Names and objects: the mental model that prevents bugs

This section is the most important one in the lesson. Get this right and a
whole category of confusing behavior becomes obvious.

Many languages teach you to think of a variable as a **box** that contains a
value. Assignment puts a value in the box.

**Python does not work like that.** In Python:

- Every value is an **object** living somewhere in memory.
- A **name** is a label attached to an object, like a luggage tag.
- Assignment (`=`) attaches a label to an object. It does not copy anything.

```python
a = [1, 2, 3]     # create a list object; attach the label 'a' to it
b = a             # attach a SECOND label, 'b', to the SAME object
```

There is one list here, with two labels on it. So:

```python
b.append(4)       # modify the object that both labels point at
print(a)          # [1, 2, 3, 4]   -- 'a' sees it too, because it is the same list
```

Beginners find this shocking. With the box model it is inexplicable. With the
label model it is obvious: you never made a second list.

You can see it directly. `id()` returns an object's identity, effectively its
memory address:

```python
>>> a = [1, 2, 3]
>>> b = a
>>> id(a) == id(b)
True                  # same object
>>> b = [1, 2, 3]     # now build a genuinely different list
>>> id(a) == id(b)
False                 # different objects...
>>> a == b
True                  # ...that happen to hold equal values
```

That last pair is the difference between the two comparison operators:

- **`is`** asks "are these the same object?" It compares identity.
- **`==`** asks "do these have the same value?" It compares contents.

**Rule: use `is` only for `None`, `True` and `False`.** For everything else use
`==`. Writing `if x is 5` sometimes works by accident, because the interpreter
caches small integers, and then mysteriously fails for larger numbers. Do not
do it.

```python
if value is None:        # correct
if value == None:        # works, but nobody writes this
if name == "radar-1":    # correct: comparing values
```

### Copying

If you actually want a separate object, say so.

```python
import copy

original = [1, 2, 3]

alias      = original                 # not a copy at all: a second label
shallow    = original[:]              # a new list, same elements inside
shallow2   = list(original)           # same thing, clearer
deep       = copy.deepcopy(original)  # new list AND new copies of the contents
```

**Shallow versus deep** matters when the contents are themselves mutable:

```python
rows = [[1, 2], [3, 4]]
shallow = rows[:]           # new outer list...
shallow[0].append(99)       # ...but the INNER lists are still shared
print(rows)                 # [[1, 2, 99], [3, 4]]  -- surprise

deep = copy.deepcopy(rows)  # new outer list and new inner lists
deep[0].append(99)
print(rows)                 # unchanged
```

Deep copies are expensive. Reach for one only when you need it.

## 4. Everything is an object

In Python, *everything* is an object: numbers, strings, functions, classes,
modules. An object is a bundle of data plus the operations that work on it.

You can ask any object what it is and what it can do:

```python
>>> value = "radar-1"
>>> type(value)
<class 'str'>
>>> dir(value)             # every attribute and method available
['__add__', ..., 'startswith', 'strip', 'title', 'upper', ...]
>>> help(value.strip)      # the documentation, right there
```

`type`, `dir` and `help` in a REPL will answer most "how do I do X" questions
faster than a search engine, and they answer for the exact version you are
running. Learn to use them.

The fact that **functions are objects** is not a curiosity, it is the
foundation of decorators, callbacks and the `key=` argument you will use
constantly:

```python
def shout(text):
    return text.upper()

action = shout          # no parentheses: attach a label to the function itself
print(action("hello"))  # HELLO -- called through the second label
```

`shout` is the function. `shout()` is *calling* it. Confusing the two is one of
the most common beginner errors.

## 5. The built-in types

### Numbers

```python
count = 42              # int: whole number, unlimited size
ratio = 3.14            # float: decimal, ~15-17 significant digits
big = 2 ** 200          # ints never overflow; this is exact
```

Integers in Python have **no maximum size**, unlike Java's `int` or `long`.
Floats are standard IEEE 754 doubles and carry the usual surprise:

```python
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
```

This is not a Python bug; it is how binary floating point represents decimal
fractions, and every language does it. The consequence for you: **never compare
floats with `==`.** Compare with a tolerance:

```python
>>> abs((0.1 + 0.2) - 0.3) < 1e-9
True
```

In tests, use the helper:

```python
assert result == pytest.approx(expected)
```

For money or anything requiring exact decimal arithmetic, use the `decimal`
module instead of floats.

Arithmetic:

```python
7 / 2       # 3.5   -- true division, ALWAYS gives a float
7 // 2      # 3     -- floor division, rounds toward negative infinity
7 % 2       # 1     -- remainder ("modulo")
7 ** 2      # 49    -- exponent
-7 // 2     # -4    -- note: floors, does not truncate toward zero
```

The `/` behavior is a Python 2 to 3 change that still bites people: in Python 2
`7 / 2` was `3`.

### Strings

A string is an immutable sequence of characters.

```python
name = "radar-1"
also = 'radar-1'                   # single and double quotes are identical
multi = """spans
several lines"""
```

**Immutable** means you cannot change a string in place. Every operation that
looks like modification actually builds a new string:

```python
>>> s = "hello"
>>> s.upper()
'HELLO'
>>> s
'hello'            # the original is untouched
>>> s = s.upper()  # to keep the result, rebind the name
```

This has a performance consequence worth knowing for interviews. Building a
string by repeated concatenation is O(n²), because each `+=` copies everything
so far:

```python
# Slow: creates a new string every iteration
result = ""
for word in words:
    result += word

# Fast: collect the pieces, join once
result = "".join(words)
```

The operations you will actually use:

```python
s = "  RADAR-1:ACTIVE:32.5  "

s.strip()                  # remove leading/trailing whitespace
s.strip().lower()          # 'radar-1:active:32.5'
s.strip().split(":")       # ['RADAR-1', 'ACTIVE', '32.5']  -- returns a LIST
":".join(["a", "b"])       # 'a:b'  -- the inverse of split
s.replace("ACTIVE", "DROPPED")
s.startswith("  RAD")      # True
"ACTIVE" in s              # True -- substring test
len(s)                     # length
```

`split` is how you turn a line of text into fields, and it is in nearly every
parsing problem you will be given.

**Indexing and slicing.** Positions start at zero. Negative positions count
from the end.

```python
s = "abcdef"
s[0]        # 'a'      first
s[-1]       # 'f'      last
s[1:4]      # 'bcd'    from 1 up to BUT NOT INCLUDING 4
s[:3]       # 'abc'    from the start
s[3:]       # 'def'    to the end
s[::-1]     # 'fedcba' step of -1: reversed
```

The "up to but not including" rule is universal in Python. It looks odd at
first and has a nice property: `s[:n]` and `s[n:]` split the sequence with no
overlap and no gap, and `len(s[a:b])` is just `b - a`.

**f-strings** are the modern way to build strings from values. The `f` prefix
means "evaluate the expressions inside the braces":

```python
sensor = "radar-1"
confidence = 0.8734

f"{sensor} at {confidence}"          # 'radar-1 at 0.8734'
f"{sensor} at {confidence:.2f}"      # 'radar-1 at 0.87'      2 decimal places
f"{confidence:.1%}"                  # '87.3%'                as a percentage
f"{42:05d}"                          # '00042'                zero-padded
f"{sensor:>12}"                      # '     radar-1'         right-aligned
f"{sensor=}"                         # "sensor='radar-1'"     handy for debugging
```

That last one is a debugging shortcut: it prints the expression and its value.

### Booleans and None

```python
is_active = True
is_stale = False
result = None
```

`None` is Python's "no value." It is not zero, not an empty string, and not
false in the way other languages use null. It is a specific object meaning
"nothing here." A function that does not return anything returns `None`.

**Truthiness.** Any object can be tested as a condition, and Python has rules
about what counts as false:

```python
# These are all FALSY:
False, None, 0, 0.0, "", [], {}, set(), ()

# Everything else is TRUTHY.
```

This lets you write natural conditions:

```python
if detections:              # "if the list is not empty"
    process(detections)

if not name:                # "if the name is empty or None"
    raise ValueError("name required")
```

**The trap:** empty and `None` are both falsy but mean different things. If
`0` is a legitimate value, testing truthiness is a bug:

```python
count = 0

if count:                   # WRONG: skips a legitimate zero
    report(count)

if count is not None:       # RIGHT: distinguishes "zero" from "absent"
    report(count)
```

### Type conversion

```python
int("42")           # 42       string to int; raises ValueError if not numeric
float("3.14")       # 3.14
str(42)             # '42'
list("abc")         # ['a', 'b', 'c']
bool("")            # False
int(3.99)           # 3        truncates toward zero, does NOT round
round(3.99)         # 4
```

Data arriving from a file, a network socket or a command line is **always
text**. Converting it, and handling the conversion failing, is a large part of
every parsing task:

```python
try:
    confidence = float(raw_value)
except ValueError:
    log.warning("not a number: %r", raw_value)
    confidence = None
```

## 6. Containers: what each one is for

Python gives you four workhorse containers. Choosing correctly is most of what
"data structures" means in an interview.

### list: an ordered, changeable sequence

```python
sensors = ["radar-a", "radar-b", "radar-c"]

sensors.append("radar-d")        # add to the end
sensors.insert(0, "radar-z")     # add at a position
sensors.remove("radar-b")        # remove by value (first match)
last = sensors.pop()             # remove and return the last
first = sensors.pop(0)           # remove and return by index
sensors[1] = "replaced"          # change in place
len(sensors)
"radar-a" in sensors             # membership test -- see the warning below
sorted(sensors)                  # a NEW sorted list
sensors.sort()                   # sorts IN PLACE, returns None
sensors.reverse()
```

Note that `sorted(x)` returns a new list while `x.sort()` modifies and returns
`None`. Writing `sensors = sensors.sort()` sets `sensors` to `None`, which is a
classic beginner bug.

**Use a list when** order matters, duplicates are allowed, and you mostly add
to the end or iterate through. It is the default choice.

**The performance trap:** `x in some_list` scans the whole list. Inside a loop
that also runs once per item, you have accidentally written an O(n²) algorithm.
Use a set instead. This one fix accounts for an enormous share of real
performance problems, and mentioning it in an interview is a strong signal.

### tuple: an ordered, unchangeable sequence

```python
point = (24.45, 54.37)
lat, lon = point                 # "unpacking": assign both at once
```

A tuple is a list that cannot be modified after creation. Why would you want
that?

- **It signals fixed structure.** A list of three things suggests "more may
  arrive." A tuple of three things says "this is a coordinate."
- **It can be used as a dictionary key or set member.** Lists cannot, because
  they are mutable. This matters more often than you would expect.
- **It is protection.** A caller cannot accidentally modify what you handed
  them.

Unpacking is used constantly:

```python
for sensor, confidence in pairs:      # unpack each tuple as you loop
    ...

a, b = b, a                           # swap, with no temporary variable
first, *rest = [1, 2, 3, 4]           # first=1, rest=[2, 3, 4]
```

### dict: a lookup table from keys to values

A dictionary maps **keys** to **values**. It is the most important container in
Python.

```python
counts = {"radar-a": 12, "radar-b": 7}

counts["radar-c"] = 3            # add or overwrite
counts["radar-a"]                # 12   -- raises KeyError if absent
counts.get("radar-z")            # None -- no error
counts.get("radar-z", 0)         # 0    -- with a default
"radar-a" in counts              # True -- checks KEYS
del counts["radar-c"]
counts.pop("radar-b", None)      # remove, tolerating absence

for key in counts: ...                    # iterates over keys
for key, value in counts.items(): ...     # both at once -- what you usually want
list(counts.keys())
list(counts.values())
```

**Why it is so important:** looking a key up in a dict takes roughly constant
time no matter how large the dict is. Searching a list takes time proportional
to its length. For anything keyed by an identifier, a dict turns a slow scan
into an instant lookup.

`.get()` deserves emphasis. `counts["missing"]` raises `KeyError` and stops your
program; `counts.get("missing", 0)` returns a default. In parsing code, where
absent fields are normal, `.get` is usually what you want.

Two patterns you will use in nearly every aggregation problem:

```python
# Counting
counts = {}
for sensor in sensor_ids:
    counts[sensor] = counts.get(sensor, 0) + 1

# Grouping
groups = {}
for detection in detections:
    groups.setdefault(detection.sensor_id, []).append(detection)
```

`setdefault(key, default)` returns the existing value if the key is present,
otherwise inserts the default and returns that. It saves an `if` on every
iteration. [Lesson 5](python-practice.html) shows the cleaner
`collections.defaultdict` version, but understand this form first because it
shows what is actually happening.

**Keys must be hashable**, which in practice means immutable: strings, numbers
and tuples work; lists and dicts do not. Since Python 3.7, dictionaries
remember insertion order as a guaranteed part of the language.

### set: an unordered collection of unique items

```python
seen = {"radar-a", "radar-b"}
seen.add("radar-c")
seen.add("radar-a")              # already there: no effect, no error
"radar-a" in seen                # True, and fast
seen.discard("radar-z")          # remove if present, no error if absent
```

**Use a set when** you care about membership or uniqueness and not about order
or counts.

```python
unique_sensors = set(all_sensor_ids)        # deduplicate in one step
len(set(ids)) != len(ids)                   # "are there duplicates?"
```

Sets support the mathematical operations, which replace loops:

```python
a = {1, 2, 3}
b = {3, 4}

a | b        # {1, 2, 3, 4}   union: in either
a & b        # {3}            intersection: in both
a - b        # {1, 2}         difference: in a but not b
a ^ b        # {1, 2, 4}      symmetric difference: in exactly one
```

That is the whole answer to "which ids are in the new file but not the old
one," which is a real tech-refresh task and a plausible interview question.

**Note the empty-set gotcha:** `{}` is an empty *dict*, not a set. Use `set()`.

### Choosing

| Need | Use |
| --- | --- |
| Ordered, changeable, duplicates fine | `list` |
| Ordered, fixed, usable as a key | `tuple` |
| Look something up by an identifier | `dict` |
| Uniqueness or fast membership tests | `set` |

## 7. Control flow

### Conditionals

```python
if confidence >= 0.8:
    state = "high"
elif confidence >= 0.5:          # "else if"
    state = "medium"
else:
    state = "low"
```

**Python uses indentation, not braces, to define blocks.** The colon opens a
block and the indentation says what is inside it. This is not a style
preference, it is the syntax. Use four spaces, never tabs, and let your editor
handle it. Mixing tabs and spaces produces errors that are invisible on screen.

Comparison and logic:

```python
==  !=  <  >  <=  >=
and  or  not                     # words, not && || !
0 <= confidence <= 1             # chained comparison: reads like maths
if sensor_id and confidence > 0.5:
```

`and` and `or` **short-circuit**: they stop as soon as the answer is known.
That makes this safe:

```python
if data and data[0] == "header":     # data[0] is never evaluated when data is empty
```

### Loops

`for` iterates over the items of a collection. It is not a counter loop as in
C.

```python
for sensor in sensors:               # each ITEM, not an index
    print(sensor)

for i in range(5):                   # 0, 1, 2, 3, 4
    print(i)

for i, sensor in enumerate(sensors):          # index AND item
    print(f"{i}: {sensor}")

for i, sensor in enumerate(sensors, start=1): # numbering from 1
    ...

for sensor, count in zip(sensors, counts):    # walk two lists together
    ...
```

`enumerate` and `zip` are worth memorizing. Writing `for i in range(len(x))` and
then indexing is a sign of someone thinking in C, and interviewers notice.

`while` repeats until a condition goes false:

```python
attempts = 0
while attempts < 3:
    if try_connect():
        break                # exit the loop immediately
    attempts += 1
else:
    log.error("never connected")     # runs only if the loop was NOT broken out of
```

That `else` on a loop is unusual and rarely used, but it does get asked about.
It runs when the loop finishes normally, and is skipped when you `break`.

`continue` skips to the next iteration, which is the standard way to filter
while parsing:

```python
for line in lines:
    line = line.strip()
    if not line or line.startswith("#"):
        continue                      # skip blanks and comments
    process(line)
```

### What "iterable" means

A `for` loop does not need a list. It works on anything **iterable**, meaning
anything that can produce items one at a time. Strings, lists, tuples, sets,
dicts and files are all iterable.

This is why you can loop over a file directly, one line at a time, without
loading it into memory:

```python
with open("big.log") as f:
    for line in f:          # reads one line at a time, not the whole file
        process(line)
```

For a 40 GB log on a machine with 8 GB of RAM, that distinction is the whole
ballgame. [Lesson 5](python-practice.html) develops this into generators.

### Comprehensions

A comprehension is compact syntax for building a list, dict or set from an
existing iterable. Build up to it from the loop you already understand:

```python
# The loop
squares = []
for n in numbers:
    squares.append(n * n)

# The same thing as a comprehension
squares = [n * n for n in numbers]
```

Read it as "n times n, for each n in numbers." Add a condition to filter:

```python
evens = [n for n in numbers if n % 2 == 0]
even_squares = [n * n for n in numbers if n % 2 == 0]
```

The same shape builds dicts and sets:

```python
{name: len(name) for name in names}       # dict comprehension
{n % 3 for n in numbers}                  # set comprehension
```

**Why use them?** They are shorter, they are faster than the equivalent loop,
and they state intent: a comprehension always means "build a new collection
from an old one," while a loop could mean anything.

**When not to use them.** One loop and one condition is readable. Two nested
loops plus a condition is not. Readability is being assessed in an interview,
so if it needs a comment to explain, write the loop.

## 8. Functions

A function is a named, reusable block of code that takes inputs and gives back
a result.

```python
def average_confidence(detections):
    """Return the mean confidence, or None if there are none."""
    if not detections:
        return None
    return sum(d.confidence for d in detections) / len(detections)
```

The parts: `def` starts the definition, the name, parameters in parentheses, a
colon, then the indented body. The string on the first line is a **docstring**,
Python's built-in documentation; `help(average_confidence)` prints it.

`return` sends a value back and exits immediately. A function with no `return`
returns `None`.

**Why functions matter beyond reuse:** a function gives a chunk of logic a
name, which makes code readable, and it creates a unit you can test in
isolation. Code that is not in a function is code you cannot unit test, which
matters given what this job is.

### Arguments

```python
def score(track, weight=1.0, floor=0.0):     # weight and floor have defaults
    return max(track.confidence * weight, floor)

score(t)                          # positional
score(t, 2.0)                     # positional
score(t, weight=2.0)              # by keyword: clearer at the call site
score(t, floor=0.5, weight=2.0)   # keywords can be in any order
```

Passing booleans and numbers by keyword makes calls self-documenting.
`parse(data, True)` tells a reader nothing; `parse(data, strict=True)` tells
them everything.

**The mutable default argument trap.** This is asked in interviews and it does
bite in real code:

```python
def add_item(item, bucket=[]):        # WRONG
    bucket.append(item)
    return bucket

add_item(1)     # [1]
add_item(2)     # [1, 2]   -- where did the 1 come from?
```

The default value is created **once**, when the function is defined, not each
time it is called. So every call without a bucket shares the same list. The
fix:

```python
def add_item(item, bucket=None):      # RIGHT
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

Rule: **never use a mutable object as a default argument.** Use `None` and
create it inside.

### Scope

A name assigned inside a function is **local** to it and disappears when the
function returns:

```python
def f():
    x = 10          # local
    print(x)

f()
print(x)            # NameError: x is not defined out here
```

Python resolves a name by looking in order: **L**ocal, then any **E**nclosing
function, then **G**lobal (module level), then **B**uilt-in. That order is
called LEGB and it is a common interview question.

You can *read* a global from inside a function but not *assign* to it without
declaring `global`. Needing `global` is almost always a design smell: pass the
value in and return the result instead.

### Lambdas

A `lambda` is a small anonymous function written inline:

```python
lambda t: t.confidence           # a function taking t, returning t.confidence
```

You will meet it almost exclusively as the `key=` argument to `sorted`, `max`
and `min`. That argument takes a function, applies it to each item, and sorts
or compares by the result:

```python
tracks = [("T3", 5, 0.9), ("T1", 5, 0.4), ("T2", 2, 0.7)]

sorted(tracks, key=lambda t: t[1])              # by the second field
sorted(tracks, key=lambda t: (-t[1], t[0]))     # 2nd descending, then 1st ascending
max(tracks, key=lambda t: t[2])                 # the one with the highest 3rd field
```

The tuple trick in the second line is worth understanding: returning a tuple
sorts by the first element, then breaks ties with the second. Negating a number
reverses its direction. This one line is the answer to a large share of "sort
by X then Y" problems.

Python's sort is **stable**, meaning items that compare equal keep their
original relative order. Saying that out loud is a small competence signal.

### Type hints

Hints declare what types you expect. Python does **not** enforce them at
runtime; they are documentation that tools can check.

```python
def parse(line: str) -> tuple[str, float]:
    name, value = line.split("=")
    return name.strip(), float(value)
```

Use them. They make code readable, they let your editor catch mistakes as you
type, and a static checker such as `mypy` finds the misspelled-attribute class
of bug that an interpreted language otherwise defers until runtime. On a
sustainment program that argument lands well.

## 9. Errors and exceptions

An **exception** is Python's mechanism for signalling that something went
wrong. When one is raised, execution stops and the exception travels up the
call stack until something catches it. If nothing does, the program stops and
prints a **traceback**.

### Reading a traceback

```
Traceback (most recent call last):
  File "ingest.py", line 42, in <module>
    main()
  File "ingest.py", line 30, in main
    process(line)
  File "ingest.py", line 18, in process
    confidence = float(parts[2])
IndexError: list index out of range
```

Read it **bottom up**. The last line is the actual error and its type. The line
above it is where it happened. Above that is the chain of calls that led there.
Beginners read from the top and get lost; the bottom is where the information
is.

Common types and what they mean:

| Exception | Cause |
| --- | --- |
| `SyntaxError` | The code is not valid Python; nothing ran |
| `NameError` | Used a name that does not exist, usually a typo |
| `TypeError` | Wrong type, e.g. `"5" + 3` |
| `ValueError` | Right type, unusable value, e.g. `int("abc")` |
| `KeyError` | Dict key not present |
| `IndexError` | List index out of range |
| `AttributeError` | Object has no such attribute, e.g. `None.strip()` |
| `FileNotFoundError` | The file is not there |
| `ZeroDivisionError` | Divided by zero |

`AttributeError` on `NoneType` is worth calling out: it almost always means a
function returned `None` when you expected an object, usually because it hit a
path with no `return`.

### Handling exceptions

```python
try:
    confidence = float(raw)
except ValueError:
    log.warning("bad value: %r", raw)
    confidence = None
```

The full form:

```python
try:
    value = int(raw)
except ValueError as exc:            # 'as exc' captures the exception object
    handle(exc)
except (KeyError, IndexError):       # several types at once
    raise                            # re-raise unchanged
else:
    process(value)                   # runs only if NO exception occurred
finally:
    cleanup()                        # ALWAYS runs, exception or not
```

**Catch only what you expect.** A bare `except:` catches everything, including
Ctrl-C and genuine programming errors, and turns a visible bug into silent
wrong behavior:

```python
try:
    risky()
except:                # NEVER do this
    pass               # especially not this
```

An empty `except: pass` is the worst two lines in Python. If you catch
something, do something: log it, count it, convert it, re-raise it.

### Raising your own

```python
def set_confidence(value):
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"confidence out of range: {value}")
```

**Validate at the boundary and fail immediately.** A bad value rejected where
it enters the system produces an error message naming the real problem. The
same value accepted and propagated produces a confusing failure somewhere else
ten minutes later.

Custom exception types let callers distinguish your failures:

```python
class SensorError(Exception):
    """Base class for all sensor adapter failures."""

class MalformedRecord(SensorError):
    """A record could not be parsed."""
```

Then `except SensorError` catches the whole family. Defining a base class per
subsystem is standard practice.

### Errors versus exceptions as flow

Not everything unusual deserves an exception. A malformed line in a log file
being parsed is *expected*, so counting and skipping it is right. A
configuration file that does not exist is *not* expected, so raising is right.
The question to ask is whether the caller can reasonably continue.

## 10. Files and the `with` statement

```python
with open("detections.csv", encoding="utf-8") as f:
    for line in f:
        process(line.strip())
```

`with` is a **context manager**: it guarantees cleanup. Here it guarantees the
file is closed when the block ends, even if an exception is raised inside. The
alternative is `try/finally` written out by hand, and people forget.

**Always use `with` for files.** Files left open leak operating-system handles,
and on a long-running service that eventually fails with "too many open files."

**Always pass `encoding`.** Without it Python uses a platform default, so the
same code reads a file correctly on one machine and produces mojibake or an
exception on another. That is a genuine cross-platform integration defect, and
the posting names both RHEL and Windows.

Modes:

```python
open(path)                  # 'r', read text, the default
open(path, "w")             # write text, TRUNCATES an existing file
open(path, "a")             # append
open(path, "rb")            # read binary: gives bytes, not str
```

`"w"` destroying the existing contents surprises people. Note it.

### Paths

```python
from pathlib import Path

p = Path("/var/log/eadge") / "ingest.log"     # '/' joins path parts
p.exists(); p.is_file(); p.stat().st_size
p.name; p.suffix; p.parent
p.read_text(encoding="utf-8")
for log in Path("logs").glob("*.log"): ...
```

`pathlib` replaces older string-based path handling and gets separators right
on both Linux and Windows, which is exactly the class of bug that only shows up
in integration.

## 11. Modules, imports and program structure

A **module** is simply a `.py` file. Importing one runs it and gives you access
to its contents.

```python
import math                      # the whole module
math.sqrt(16)

from math import sqrt            # one name directly
sqrt(16)

from collections import Counter, defaultdict
import numpy as np               # with an alias
```

Prefer `import module` or `from module import specific_name`. Avoid
`from module import *`, which dumps every name into your namespace and makes it
impossible to tell where anything came from.

A **package** is a directory of modules. Dots follow the directory structure:

```python
from eadge.adapters.radar import LegacyRadarAdapter
```

### `if __name__ == "__main__"`

You will see this in nearly every script:

```python
def main():
    ...

if __name__ == "__main__":
    main()
```

Every module has a `__name__` variable. When run directly it is set to
`"__main__"`; when imported it is set to the module's name. So this block means
**"only do this when run as a program, not when imported."**

Why it matters: without it, importing your module to reuse one function would
execute the whole script as a side effect. With it, a file can be both a
runnable program and an importable library, which is precisely what you need to
unit test it.

### Layout

```
myservice/
  pyproject.toml              project metadata and dependencies
  src/myservice/__init__.py   marks the directory as a package
  src/myservice/adapter.py
  tests/test_adapter.py
```

## 12. Classes and objects

### Why classes exist

Suppose you are tracking sensor detections. Without classes you might use a
dict:

```python
detection = {"sensor_id": "radar-1", "timestamp": 1000.0, "confidence": 0.9}
```

That works until it does not. Nothing stops a typo like `detection["sensr_id"]`
from silently creating a new key. Nothing validates that confidence is between
zero and one. And functions that operate on detections live scattered across
the file, unconnected to the data.

A **class** solves this by bundling the data with the operations on it, and
giving the bundle a name and rules.

```python
class Detection:
    """One sensor report."""

    def __init__(self, sensor_id, timestamp, confidence):
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(f"confidence out of range: {confidence}")
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.confidence = confidence

    def is_high_confidence(self):
        return self.confidence >= 0.8

    def __repr__(self):
        return f"Detection({self.sensor_id!r}, {self.timestamp}, {self.confidence})"
```

Using it:

```python
d = Detection("radar-1", 1000.0, 0.9)
d.sensor_id                 # 'radar-1'
d.is_high_confidence()      # True
Detection("radar-1", 0, 5)  # ValueError, immediately
```

**Class versus object.** The class is the template. An object, or instance, is
one thing built from it. `Detection` is the class; `d` is an object.

**What `self` is.** When you call `d.is_high_confidence()`, Python calls the
function with `d` as the first argument. `self` is that first parameter: the
particular object being worked on. It is explicit in Python where other
languages hide it, and you must write it as the first parameter of every
method. Forgetting it is a standard beginner error.

**`__init__`** is the constructor: it runs when you create an object, and its
job is to set up the instance's data. Note that it *validates* here. An object
that cannot be constructed in an invalid state cannot be invalid later
anywhere else in the system, which removes a whole class of defensive checks
downstream.

### Dunder methods

Names with double underscores at each end, said "dunder," hook into Python's
built-in behavior.

| Method | Powers |
| --- | --- |
| `__init__` | Construction |
| `__repr__` | The developer-facing string, shown in the REPL and in logs |
| `__str__` | The user-facing string, used by `print` |
| `__eq__` | The `==` operator |
| `__hash__` | Use as a dict key or set member |
| `__len__` | `len(obj)` |
| `__iter__` | Being usable in a `for` loop |
| `__enter__` / `__exit__` | Use in a `with` block |

**Always write `__repr__`.** Without it, an object prints as
`<Detection object at 0x7f3a...>`, which tells you nothing when a test fails or
a log line is written. With it, you can see what the object was. This is a
small habit with a large payoff in debugging.

**`__eq__` and `__hash__` go together.** By default, two objects are equal only
if they are the same object. If you want value equality, define `__eq__`. But
if you define `__eq__` and want the object usable in a set or as a dict key,
you must also define `__hash__`, and both must be based on the same fields:

```python
def __eq__(self, other):
    if not isinstance(other, Detection):
        return NotImplemented
    return self.sensor_id == other.sensor_id and self.timestamp == other.timestamp

def __hash__(self):
    return hash((self.sensor_id, self.timestamp))
```

Break that rule and objects vanish inside sets and dictionaries in ways that
are very hard to debug. Java has the identical rule, and it is a common
interview question in both languages.

### Dataclasses

Most of that boilerplate can be generated:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Detection:
    sensor_id: str
    timestamp: float
    confidence: float = 1.0        # a default

d = Detection("radar-1", 1000.0, 0.9)
d.sensor_id
d == Detection("radar-1", 1000.0, 0.9)     # True: value equality for free
```

`@dataclass` writes `__init__`, `__repr__` and `__eq__` from the annotated
fields. `frozen=True` makes instances immutable, which also makes them hashable
and safe to share across threads.

**Use a dataclass for data that is mostly data.** Write a full class when
behavior dominates. Most of what flows through a message-driven system is the
former.

### Inheritance

A class can build on another, taking its behavior and specializing it:

```python
class SensorAdapter:
    def parse(self, raw):
        raise NotImplementedError            # subclasses must provide this

class CsvAdapter(SensorAdapter):             # CsvAdapter IS A SensorAdapter
    def parse(self, raw):
        return [Detection(*line.split(",")) for line in raw.splitlines()]
```

The value: code that works with a `SensorAdapter` works with every subclass
without knowing which one it has. Adding a new sensor format means writing a
new class, not editing existing logic.

**Use inheritance sparingly.** It is the tightest coupling available, because a
subclass depends on the parent's implementation. Prefer **composition**, where
an object holds another object and delegates to it. The rule of thumb:
inheritance for "is a," composition for "has a." [Lesson 8](ood.html) develops
this.

## 13. Virtual environments

Python installs packages system-wide by default. Two projects needing different
versions of the same library then conflict, and installing something for one
project can break another. On a shared or long-lived machine this gets bad
quickly.

A **virtual environment** is a private directory holding its own Python and its
own packages, isolated from the system and from other projects.

```bash
python3 -m venv .venv                  # create it, once per project
source .venv/bin/activate              # switch into it (Windows: .venv\Scripts\activate)
pip install pytest                     # installs INTO the environment
deactivate                             # leave it
```

Once activated, `python` and `pip` refer to the environment's copies. Your
prompt usually shows the name.

**Always use one.** It is one command, and it prevents an entire category of
"works on my machine" problems. Add `.venv/` to `.gitignore`; the environment
is rebuildable and does not belong in version control.

Recording dependencies so someone else can reproduce your environment:

```bash
pip install -r requirements.txt        # install a recorded set
pip freeze > requirements.txt          # record exactly what is installed
```

For a program under configuration control, **pin exact versions**. Not
`requests>=2`, but `requests==2.32.3`. A build that pulls a different version
next week is not reproducible, and reproducibility is a requirement on an
accredited system rather than a nicety. This session's own site is a live
example: it pins `markdown` and `pygments`, because without the pin the same
source built two different sites on two machines.

## 14. What to practise

Type all of this. Do not read it. Then in a REPL:

1. Make a list, alias it to a second name, modify through one, and confirm the
   other sees it. Then do the same with a copy.
2. Build a dict of counts from a list of repeated strings, using `.get`.
3. Group a list of `"sensor,value"` strings into a dict of lists using
   `setdefault`.
4. Write a function with a mutable default argument and call it twice. Watch it
   misbehave. Fix it.
5. Trigger each of `KeyError`, `IndexError`, `ValueError`, `TypeError` and
   `AttributeError` on purpose, and read each traceback bottom-up.
6. Write a `Detection` class with validation in `__init__` and a `__repr__`.
   Put two equal-valued instances in a set and see that you get two entries.
   Then add `__eq__` and `__hash__` and see that you get one.

Number six is the one that teaches the most per minute.

Then go to [lesson 5](python-practice.html) for the standard library, testing
and the tooling, and to the [practice repo](../practice/README.html) for
problems to solve.
