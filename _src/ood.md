# 7. Object-oriented design and SOLID

The posting names "object-oriented design principles" explicitly. On a
sustainment program this is not academic. Legacy code that resists change is the
central daily problem, and design vocabulary is how you argue for restructuring
it in a code review.

## 1. The four pillars, with the answer they want

**Encapsulation.** Hide internal state behind an interface so that invariants
are enforced in one place. The practical payoff: you can change the internal
representation without changing every caller.

**Abstraction.** Expose the operation, not the mechanism. `SensorAdapter.parse`
does not tell callers whether the wire format is XML or a binary struct.

**Inheritance.** Reuse and specialize. Use it sparingly. Inheritance is the
tightest coupling in object-oriented design because a subclass depends on the
parent's implementation, not just its interface.

**Polymorphism.** One call site, many behaviors, selected at runtime. This is
what lets you add a fifth sensor type without touching the correlator.

If asked "inheritance or composition," the answer is **composition by default**.
Inheritance expresses "is a" and should be reserved for genuine subtyping.
Composition expresses "has a" and keeps the pieces replaceable and testable.

## 2. SOLID, with a defense-flavored example each

**S &mdash; Single responsibility.** A class should have one reason to change.

> A `TrackManager` that parses wire messages, correlates detections, *and*
> writes to the database has three reasons to change: a new message format, a
> new correlation rule, a new persistence layer. Split it.

**O &mdash; Open/closed.** Open for extension, closed for modification.

> Adding a new radar type should mean writing a new `SensorAdapter`
> implementation and registering it, not editing a switch statement in the
> ingest loop. Every edit to shared code on an accredited baseline costs
> regression testing.

**L &mdash; Liskov substitution.** A subtype must be usable wherever the base
type is expected, without surprising the caller.

> A `ReadOnlyTrackStore` that extends `TrackStore` and throws on `save()`
> violates this. Callers that legitimately hold a `TrackStore` now break. Model
> it as two interfaces instead.

**I &mdash; Interface segregation.** Many small interfaces beat one large one.

> A `SensorAdapter` interface with `parse`, `calibrate`, `selfTest`, and
> `firmwareUpdate` forces every simple file-based adapter to stub three methods.
> Split into `Parser`, `Calibratable`, and `Diagnosable`.

**D &mdash; Dependency inversion.** Depend on abstractions, not concretions.

> The correlator should take a `TrackStore` interface in its constructor, not
> construct a `PostgresTrackStore` internally. That is what makes it unit
> testable with an in-memory fake, which is exactly the "automated test
> capability" the posting asks for.

That last point is the strongest link between design vocabulary and this job.
Make it explicitly if SOLID comes up.

## 3. Other principles worth naming

- **DRY**, do not repeat yourself. But do not abstract two things that merely
  look alike; premature deduplication couples unrelated code.
- **YAGNI**, you aren't gonna need it. Especially true on a program where every
  line carries verification cost.
- **Law of Demeter.** `order.getCustomer().getAddress().getCity()` reaches
  through three objects. Ask for what you need.
- **Composition over inheritance**, covered above.
- **Fail fast.** Validate at the boundary and throw immediately rather than
  propagating a bad value into the system.
- **Make illegal states unrepresentable.** A `Detection` whose constructor
  rejects a confidence outside 0..1 cannot exist in a bad state anywhere
  downstream.

## 4. Patterns you are likely to be asked about

Know these six cold. Be able to name a real use, not just recite the structure.

### Strategy

Swap an algorithm at runtime.

```python
from abc import ABC, abstractmethod

class CorrelationStrategy(ABC):
    @abstractmethod
    def score(self, track, detection) -> float: ...

class NearestNeighbor(CorrelationStrategy):
    def score(self, track, detection):
        return -distance(track.position, detection.position)

class ProbabilisticGating(CorrelationStrategy):
    def score(self, track, detection):
        return mahalanobis(track, detection)

class Correlator:
    def __init__(self, strategy: CorrelationStrategy):
        self.strategy = strategy      # injected, so it is testable and swappable
```

Real use here: configuration selects the correlation rule per deployment without
recompiling.

### Factory

Centralize construction when the concrete type depends on input.

```python
ADAPTERS = {
    "legacy_radar": LegacyRadarAdapter,
    "link16": Link16Adapter,
    "csv_replay": CsvReplayAdapter,
}

def make_adapter(kind: str, config: dict) -> SensorAdapter:
    try:
        return ADAPTERS[kind](**config)
    except KeyError:
        raise ValueError(f"unknown adapter type: {kind}") from None
```

Adding an adapter is now one dictionary entry, which satisfies open/closed.

### Adapter

Make an incompatible interface fit. This is the pattern that names half the work
on an integration program: wrapping a vendor library or legacy message format
behind your own interface so the rest of the system never sees it.

```java
public final class VendorRadarAdapter implements SensorAdapter {
    private final VendorSdkClient sdk;      // third-party, awkward API

    @Override
    public List<Detection> parse(byte[] raw) {
        VendorFrame frame = sdk.decodeFrame(raw);
        return frame.getPlots().stream()
                    .map(this::toDetection)
                    .toList();
    }
}
```

The strategic value is upgrade isolation: when the vendor SDK goes from 3.x to
4.x during a tech refresh, exactly one class changes. Say that.

### Observer / publish-subscribe

One producer, many interested consumers, decoupled.

```python
class TrackPublisher:
    def __init__(self):
        self._subscribers: list[callable] = []

    def subscribe(self, fn): self._subscribers.append(fn)

    def publish(self, track):
        for fn in self._subscribers:
            try:
                fn(track)
            except Exception:
                log.exception("subscriber failed; continuing")
```

Note the try/except: one bad subscriber must not take down the publish loop.
That detail is a good signal in a reliability-focused interview.

### Decorator

Add behavior without changing the wrapped object.

```python
import functools, time

def retry(times=3, delay=0.5, exc=Exception):
    def wrap(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            last = None
            for attempt in range(times):
                try:
                    return fn(*args, **kwargs)
                except exc as e:
                    last = e
                    log.warning("attempt %d/%d failed: %s", attempt + 1, times, e)
                    time.sleep(delay * (2 ** attempt))
            raise last
        return inner
    return wrap

@retry(times=4, exc=TimeoutError)
def fetch_status(host): ...
```

### Singleton, and the honest answer

Everyone knows it; the senior answer is that it is usually a mistake. It is
global mutable state, it makes testing hard because you cannot substitute it,
and in a concurrent program it needs careful initialization. Prefer one instance
created at composition root and injected. Say that; it lands well.

Also worth naming if they come up: **Builder** for objects with many optional
fields, **Facade** for simplifying a subsystem, **Template Method** for a fixed
algorithm with variable steps, and **Repository** for abstracting persistence.

## 5. Refactoring legacy code, which is the actual job

Expect a question like *"you inherit a 3,000-line class with no tests and need to
change one behavior. What do you do?"* Here is a defensible answer.

1. **Do not refactor first.** Understand what it does and what depends on it.
   Read the change history for why it looks that way.
2. **Get a test harness around it**, even a bad one. Characterization tests:
   run the existing code, capture the output, assert that it stays the same.
   You are not asserting correctness, you are pinning current behavior.
3. **Find a seam.** A seam is a place you can change behavior without editing
   the code in place: an interface, a constructor parameter, a factory. If there
   is no seam, introduce the smallest possible one.
4. **Make the change small and reversible.** On an accredited baseline, a large
   diff is a regression-test bill.
5. **Refactor after, not before, and separately.** Behavior change and structure
   change go in different commits so a reviewer can tell them apart, and so a
   revert is surgical.
6. **Leave the campsite cleaner**, in proportion. Improve what you touched.

Vocabulary worth using: *characterization test*, *seam*, *strangler fig* (route
traffic incrementally from the old implementation to the new one), *branch by
abstraction*, *feature toggle*.

## 6. A design exercise to work through

**Prompt:** *Design a service that ingests position reports from several
heterogeneous sensors, maintains a current track picture, and publishes updates
to downstream consumers. Sensors have different formats and update rates. Some
are unreliable.*

This is very likely the shape of any design question you get. Work it.

### Step 1: clarify before designing

- How many sensors, and what update rate? Ten sensors at 1 Hz is a laptop. A
  thousand at 50 Hz is a different design.
- How many concurrent tracks? Hundreds or hundreds of thousands?
- Is this soft real-time or hard real-time? What is the latency budget?
- Do consumers need every update, or the latest state? That decides push versus
  poll and whether you can drop messages.
- What happens if a sensor floods us, or goes silent?
- Does state need to survive a restart?

Ask at least four of those. It is a large part of what a design question grades.

### Step 2: name the components

```
 sensors --> [ Adapter per sensor type ]
                     |  normalized Detection
                     v
             [ Ingest queue (bounded) ]
                     |
                     v
             [ Correlator ] <---> [ Track store ]
                     |  TrackUpdate
                     v
             [ Publisher ] --> subscribers
                     |
                     v
             [ Metrics + health ]
```

### Step 3: justify each boundary

- **Adapter per sensor.** Isolates format churn. New sensor equals new class.
  Vendor upgrade touches one file. (Adapter pattern, open/closed.)
- **Normalized `Detection` type.** Everything downstream is format-agnostic.
  Make it immutable so it can cross thread boundaries safely.
- **Bounded queue.** This is the important one. An unbounded queue converts a
  fast producer into an out-of-memory crash. Bounded gives you a decision point:
  block the producer, or drop with a counted metric. For sensor data, dropping
  the *oldest* is usually right, because a stale position is worthless. Say that
  tradeoff explicitly.
- **Correlator behind a strategy interface.** The matching rule is the part most
  likely to change per deployment.
- **Track store behind an interface.** In-memory for tests and for the hot path,
  persistent implementation behind the same interface.
- **Publisher decoupled from correlator.** A slow consumer must not stall
  ingest. Per-subscriber queues, and a policy for a subscriber that falls
  behind.
- **Metrics and health.** Detections per second per sensor, queue depth, drop
  count, correlation latency, track count, last-message-age per sensor. On a
  fielded system, a silent sensor is the failure you must detect, and the only
  way to detect it is an age metric.

### Step 4: name what you would test

- Adapter unit tests per format, including malformed and truncated input.
- Correlator tests with a fake clock and synthetic detections.
- A back-pressure test: producer faster than consumer, assert bounded memory and
  a nonzero drop counter.
- A replay test: feed a recorded lab capture and compare the resulting track
  picture against a golden output. This is the characterization test that lets
  you refactor safely, and it is exactly the "automated test capability" the
  posting wants.

### Step 5: name what you deliberately did not do

Saying this out loud is a strong senior move.

> I have not designed for horizontal scaling, because at ten sensors and a few
> thousand tracks a single process is simpler and simpler is more verifiable. If
> the numbers were ten times larger I would partition by sensor or by
> geographic region, and then I would need to solve cross-partition
> correlation, which is a real problem I would not want to take on unless the
> requirement forced it.

## 7. Questions on this topic to expect

1. Explain SOLID with an example of one you have actually applied.
2. When is inheritance the wrong tool?
3. What is dependency injection and what problem does it solve? (Answer:
   testability and lifecycle control, not just decoupling.)
4. Difference between an interface and an abstract class, and when you pick
   each.
5. How do you make a class thread-safe? (Best answer: make it immutable. Then
   confinement, then locks, in that order of preference.)
6. How would you add a new sensor format to an existing ingest pipeline?
7. Walk me through refactoring a class with no tests.
8. What is a code smell you look for in review? (Good answers: a function that
   needs a comment to explain what it does rather than why, boolean parameters,
   deeply nested conditionals, a class that grew a second responsibility, a test
   that asserts nothing.)
