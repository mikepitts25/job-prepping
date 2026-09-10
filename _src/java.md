# 6. Java refresher

The posting pairs Java with Python. On a program like this, Java is likely to be
where the long-lived server-side applications live, so expect depth questions
even if the live coding is in Python.

Check your toolchain:

```bash
java -version      # 17 or 21 is the realistic modern baseline
javac -version
mvn -v             # or: gradle -v
```

## 1. A complete class, written the way they want to see it

```java
package lm.prep;

import java.util.Objects;

/** One system-level estimate of a tracked object. */
public final class Track implements Comparable<Track> {

    private final String trackId;
    private double latitude;
    private double longitude;
    private double altitudeMeters;

    public Track(String trackId, double latitude, double longitude, double altitudeMeters) {
        this.trackId = Objects.requireNonNull(trackId, "trackId");
        this.latitude = latitude;
        this.longitude = longitude;
        this.altitudeMeters = altitudeMeters;
    }

    public String getTrackId() { return trackId; }
    public double getAltitudeFeet() { return altitudeMeters * 3.28084; }

    public void updatePosition(double lat, double lon) {
        this.latitude = lat;
        this.longitude = lon;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Track other)) return false;   // pattern matching, Java 16+
        return trackId.equals(other.trackId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(trackId);
    }

    @Override
    public String toString() {
        return "Track[" + trackId + " @ " + latitude + "," + longitude + "]";
    }

    @Override
    public int compareTo(Track other) {
        return this.trackId.compareTo(other.trackId);
    }
}
```

**The equals/hashCode contract is asked constantly.** Memorize the rule: if two
objects are equal, they must have the same hash code. The converse is not
required. Break it and your objects vanish inside a `HashMap`. Base both on the
same immutable fields.

Records remove most of that boilerplate for value types:

```java
public record Detection(String sensorId, long timestampMillis,
                        double latitude, double longitude, double confidence) {

    public Detection {                                  // compact constructor
        if (confidence < 0.0 || confidence > 1.0) {
            throw new IllegalArgumentException("confidence out of range: " + confidence);
        }
    }

    public boolean isHighConfidence() { return confidence >= 0.8; }
}
```

A record gives you a final class with final fields plus `equals`, `hashCode`,
`toString`, and accessors. Use it for immutable data carriers, which is most of
what flows through a message-driven system.

## 2. Collections

| Interface | Common impl | Notes |
| --- | --- | --- |
| `List` | `ArrayList` | O(1) index, O(n) middle insert. The default choice. |
| `List` | `LinkedList` | O(1) ends. Rarely the right answer; say so. |
| `Set` | `HashSet` | O(1) average, no order |
| `Set` | `LinkedHashSet` | insertion order preserved |
| `Set` | `TreeSet` | sorted, O(log n) |
| `Map` | `HashMap` | O(1) average, no order |
| `Map` | `LinkedHashMap` | insertion or access order; makes an easy LRU cache |
| `Map` | `TreeMap` | sorted keys, O(log n), range queries |
| `Deque` | `ArrayDeque` | preferred stack and queue |
| `Queue` | `PriorityQueue` | heap ordered |

```java
Map<String, List<Detection>> bySensor = new HashMap<>();
bySensor.computeIfAbsent(d.sensorId(), k -> new ArrayList<>()).add(d);

Map<String, Integer> counts = new HashMap<>();
counts.merge(sensorId, 1, Integer::sum);
counts.getOrDefault(sensorId, 0);
counts.putIfAbsent(sensorId, 0);

List<Track> tracks = new ArrayList<>(List.of(a, b, c));   // List.of is immutable
tracks.sort(Comparator.comparingDouble(Track::getAltitudeFeet).reversed()
                      .thenComparing(Track::getTrackId));
tracks.removeIf(t -> t.getAltitudeFeet() < 1000);

Deque<String> stack = new ArrayDeque<>();
stack.push("a"); stack.pop();
Deque<String> queue = new ArrayDeque<>();
queue.offer("a"); queue.poll();

PriorityQueue<Detection> byConfidence =
    new PriorityQueue<>(Comparator.comparingDouble(Detection::confidence).reversed());
```

Iterating and removing safely:

```java
// WRONG: ConcurrentModificationException
for (Track t : tracks) { if (stale(t)) tracks.remove(t); }

// RIGHT
tracks.removeIf(this::stale);

// RIGHT, when you need the iterator
Iterator<Track> it = tracks.iterator();
while (it.hasNext()) { if (stale(it.next())) it.remove(); }
```

## 3. Streams

```java
import java.util.stream.*;

List<String> highConfidenceSensors = detections.stream()
        .filter(d -> d.confidence() >= 0.8)
        .map(Detection::sensorId)
        .distinct()
        .sorted()
        .toList();                                   // Java 16+; else .collect(toList())

Map<String, Long> countsBySensor = detections.stream()
        .collect(Collectors.groupingBy(Detection::sensorId, Collectors.counting()));

Map<String, Double> avgConfidence = detections.stream()
        .collect(Collectors.groupingBy(Detection::sensorId,
                 Collectors.averagingDouble(Detection::confidence)));

Optional<Detection> best = detections.stream()
        .max(Comparator.comparingDouble(Detection::confidence));

double total = detections.stream().mapToDouble(Detection::confidence).sum();

Map<Boolean, List<Detection>> split = detections.stream()
        .collect(Collectors.partitioningBy(Detection::isHighConfidence));

String joined = sensors.stream().collect(Collectors.joining(", ", "[", "]"));
```

Know that streams are lazy until a terminal operation, that they are single-use,
and that `parallelStream()` is rarely worth it and can be actively wrong with
shared mutable state.

`Optional` is for return values that may be absent:

```java
Optional<Track> found = repo.findById(id);
Track t = found.orElseThrow(() -> new NoSuchElementException(id));
String name = found.map(Track::getTrackId).orElse("unknown");
found.ifPresent(this::publish);
```

Do not use `Optional` for fields or parameters. Do not call `.get()` without
checking.

## 4. Exceptions

```java
public List<Detection> parse(Path file) throws IOException {   // checked
    try (BufferedReader reader = Files.newBufferedReader(file)) {   // try-with-resources
        return reader.lines()
                     .filter(line -> !line.isBlank())
                     .map(this::parseLine)
                     .toList();
    }
}

private Detection parseLine(String line) {
    String[] parts = line.split(",");
    if (parts.length != 5) {
        throw new MalformedRecordException(line);       // unchecked
    }
    try {
        return new Detection(parts[0], Long.parseLong(parts[1]),
                             Double.parseDouble(parts[2]),
                             Double.parseDouble(parts[3]),
                             Double.parseDouble(parts[4]));
    } catch (NumberFormatException e) {
        throw new MalformedRecordException(line, e);    // preserve the cause
    }
}
```

Checked versus unchecked, the answer they want: checked extends `Exception` and
must be declared or handled, and is appropriate for recoverable conditions a
caller should deal with; unchecked extends `RuntimeException` and signals a
programming error or an unrecoverable state. Always chain the cause. Never
swallow an exception into an empty catch block.

## 5. Concurrency

Java is where you get asked real concurrency questions.

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

ExecutorService pool = Executors.newFixedThreadPool(8);
Future<Integer> f = pool.submit(() -> correlate(chunk));
int result = f.get(5, TimeUnit.SECONDS);
pool.shutdown();
pool.awaitTermination(30, TimeUnit.SECONDS);

// Modern composition
CompletableFuture<List<Detection>> cf =
    CompletableFuture.supplyAsync(() -> fetch(sensor), pool)
                     .thenApply(this::normalize)
                     .exceptionally(ex -> List.of());
```

Thread-safe collections and counters:

```java
ConcurrentHashMap<String, Track> live = new ConcurrentHashMap<>();
live.compute(id, (k, existing) -> existing == null ? newTrack(k) : existing.merge(det));

BlockingQueue<Detection> inbox = new LinkedBlockingQueue<>(10_000);
inbox.put(d);                    // blocks when full: backpressure
Detection next = inbox.take();   // blocks when empty

AtomicLong processed = new AtomicLong();
processed.incrementAndGet();
```

Synchronization vocabulary you should be able to define on the spot:

- **`synchronized`**: intrinsic lock on an object; only one thread in the block
  at a time; also establishes a happens-before edge.
- **`volatile`**: guarantees visibility of writes across threads and prevents
  certain reorderings. It does *not* make `count++` atomic, because that is a
  read-modify-write.
- **Race condition**: outcome depends on thread interleaving.
- **Deadlock**: two threads each hold a lock the other needs. Prevent by always
  acquiring locks in a globally consistent order, or by using timeouts.
- **Livelock / starvation**: threads run but make no progress, or one thread
  never gets the lock.
- **Immutability** is the cheapest concurrency strategy. Records help.

```java
// The classic bug
private int count;
public void increment() { count++; }        // not atomic: read, add, write

// Fixes
private final AtomicInteger safeCount = new AtomicInteger();
public void increment2() { safeCount.incrementAndGet(); }

private final Object lock = new Object();
public void increment3() { synchronized (lock) { count++; } }
```

Virtual threads, if the team is on Java 21, are worth one sentence: they make
blocking I/O cheap by decoupling a Java thread from an OS thread, so a
thread-per-request design scales again.

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    sensors.forEach(s -> executor.submit(() -> poll(s)));
}
```

## 6. Memory and the JVM

Expect at least one JVM question on a systems program.

- **Stack vs heap.** Locals and frames on the stack, objects on the heap.
- **Garbage collection.** Generational: most objects die young, so the young
  generation is collected frequently and cheaply. Survivors get promoted.
  Modern collectors: G1 (default), ZGC and Shenandoah for low pause times.
- **Memory leak in Java.** Not a leak in the C sense; it is unintended
  retention. A static collection that grows forever, a listener never
  unregistered, a `ThreadLocal` on a pooled thread, a cache with no eviction.
- **Diagnosis.** `jcmd <pid> GC.heap_info`, `jmap -histo <pid>`, a heap dump via
  `jcmd <pid> GC.heap_dump`, then Eclipse MAT or VisualVM. `jstack <pid>` for a
  thread dump when things hang.
- **Flags you might see.** `-Xms` and `-Xmx` for heap sizing,
  `-XX:+HeapDumpOnOutOfMemoryError`, `-XX:MaxMetaspaceSize`.

```bash
jps -l                            # find the pid
jstack 4711 > threads.txt         # hung? get a thread dump, twice, 10s apart
jcmd 4711 GC.heap_dump /tmp/heap.hprof
```

## 7. Testing with JUnit 5

```java
package lm.prep;

import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.junit.jupiter.api.Assertions.*;

class TrackCorrelatorTest {

    private TrackCorrelator correlator;

    @BeforeEach
    void setUp() {
        correlator = new TrackCorrelator(0.5);
    }

    @Test
    @DisplayName("a detection far from every track opens a new track")
    void distantDetectionCreatesTrack() {
        correlator.ingest(new Detection("RDR-1", 1000L, 24.0, 54.0, 0.9));
        correlator.ingest(new Detection("RDR-1", 1100L, 40.0, 10.0, 0.9));
        assertEquals(2, correlator.trackCount());
    }

    @Test
    void rejectsInvalidConfidence() {
        assertThrows(IllegalArgumentException.class,
                     () -> new Detection("RDR-1", 0L, 0, 0, 1.5));
    }

    @ParameterizedTest
    @CsvSource({"0.9, true", "0.8, true", "0.79, false"})
    void confidenceThreshold(double confidence, boolean expected) {
        var d = new Detection("RDR-1", 0L, 0, 0, confidence);
        assertEquals(expected, d.isHighConfidence());
    }

    @AfterEach
    void tearDown() { correlator.close(); }
}
```

Mockito, which you will meet on almost any Java program:

```java
import static org.mockito.Mockito.*;

@Test
void publishesOnlyHighConfidence() {
    TrackPublisher publisher = mock(TrackPublisher.class);
    var service = new IngestService(publisher);

    service.handle(new Detection("RDR-1", 0L, 0, 0, 0.95));
    service.handle(new Detection("RDR-1", 1L, 0, 0, 0.10));

    verify(publisher, times(1)).publish(any(Track.class));
    verifyNoMoreInteractions(publisher);
}
```

Maven layout and commands, which you should be able to recite:

```
pom.xml
src/main/java/lm/prep/Track.java
src/main/resources/application.properties
src/test/java/lm/prep/TrackTest.java
```

```bash
mvn clean verify              # compile, test, package, run integration checks
mvn -DskipTests package       # when you only want the artifact
mvn dependency:tree           # find where a transitive version came from
mvn versions:display-dependency-updates
```

`mvn dependency:tree` is genuinely the tool you use for the COTS/FOSS upgrade
work described in the posting. Mention it when that topic comes up.

## 8. Modern Java features worth naming

```java
var detections = new ArrayList<Detection>();          // 10: local type inference

String status = switch (state) {                      // 14: switch expressions
    case ACTIVE, ENGAGED -> "live";
    case DROPPED -> "gone";
    default -> throw new IllegalStateException(state.name());
};

String sql = """
        SELECT track_id, last_seen
          FROM tracks
         WHERE state = 'ACTIVE'
        """;                                          // 15: text blocks

if (obj instanceof Detection d && d.confidence() > 0.8) {   // 16: pattern matching
    publish(d);
}

sealed interface Message permits Heartbeat, TrackUpdate, Alert {}   // 17: sealed types
```

## 9. Practice problems

**J1.** Implement `Map<String, Integer> wordCount(Path file)` using streams,
lowercasing and ignoring punctuation.

**J2.** Write an LRU cache with a fixed capacity by extending `LinkedHashMap` and
overriding `removeEldestEntry`.

**J3.** Given `List<Detection>`, return the top three sensors by average
confidence, using streams only.

**J4.** Implement a thread-safe counter three ways: `synchronized`,
`AtomicLong`, and `LongAdder`. Explain when each is right.

**J5.** Write a producer-consumer pipeline: one thread reads lines from a file
into a `BlockingQueue`, four consumers parse and count, and the main thread
prints totals after a clean shutdown.

**J6.** Given a class whose `equals` is defined but `hashCode` is not,
demonstrate the bug with a `HashSet` and then fix it.

## 10. Ten Java questions to have answers for

1. **`==` vs `.equals()`?** Reference identity vs value equality. String
   interning makes `==` misleadingly work sometimes; never rely on it.
2. **Why must equals and hashCode agree?** Section 1.
3. **`ArrayList` vs `LinkedList`?** Almost always `ArrayList`; better cache
   locality, and `LinkedList`'s O(1) insert requires you to already hold the
   node.
4. **Checked vs unchecked exceptions?** Section 4.
5. **What is `final`?** On a variable, single assignment; on a method, cannot be
   overridden; on a class, cannot be subclassed. Final reference does not mean
   immutable object.
6. **Interface vs abstract class?** Interface for capability and multiple
   inheritance of type, with default methods since Java 8; abstract class when
   you need shared state or constructors.
7. **`static`?** Belongs to the class, not the instance. Static state is a
   frequent source of concurrency and testability problems.
8. **How does `HashMap` work?** Array of buckets, hash then index, collisions
   chained and converted to a balanced tree past a threshold. Resizes at the
   load factor.
9. **String immutability?** Enables safe sharing, caching of hash codes, and
   interning. Use `StringBuilder` for loops.
10. **How would you find a memory leak in production?** Section 6, said calmly:
    heap dump, histogram, dominator tree, find the retaining path.
