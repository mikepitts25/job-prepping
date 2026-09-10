# 7. Data structures and algorithms

The posting asks for a "comprehensive understanding of data structures,
algorithms, and object-oriented design principles." On a sustainment program
that means you can pick the right container and reason about cost. It does not
mean you will be asked to derive a suffix automaton. Calibrate accordingly.

## 1. Complexity, said the way an interviewer wants to hear it

Big-O describes how runtime or memory grows as input grows, ignoring constants.

| Class | Name | Example |
| --- | --- | --- |
| O(1) | constant | dict lookup, array index, stack push |
| O(log n) | logarithmic | binary search, balanced tree insert |
| O(n) | linear | one scan of a list |
| O(n log n) | linearithmic | comparison sorting |
| O(n^2) | quadratic | nested loop over the same list |
| O(2^n) | exponential | naive subset enumeration |

Two habits that read as senior:

- **State the space complexity too**, unasked. "Linear time, and linear extra
  space for the map. If memory were tight I could sort in place and do it in
  n log n time with constant space."
- **Say what dominates in practice.** "It is O(n) either way, but the version
  that touches the disk once instead of n times is the one that matters here."

## 2. Cost of the operations you will actually use

| Operation | Python | Java | Cost |
| --- | --- | --- | --- |
| Index a sequence | `xs[i]` | `list.get(i)` | O(1) |
| Append | `xs.append(x)` | `list.add(x)` | amortized O(1) |
| Insert or delete at front | `xs.insert(0,x)` | `list.add(0,x)` | O(n) |
| Deque push/pop both ends | `deque` | `ArrayDeque` | O(1) |
| Membership in list | `x in xs` | `list.contains` | O(n) |
| Membership in set/dict | `x in s` | `HashSet.contains` | O(1) average |
| Sort | `sorted(xs)` | `Collections.sort` | O(n log n) |
| Min/max of heap | `heapq[0]` | `PriorityQueue.peek` | O(1) |
| Push/pop heap | `heappush` | `offer`/`poll` | O(log n) |
| Sorted range query | `bisect` on sorted list | `TreeMap.subMap` | O(log n) |

The most common real-world win, and a great thing to say out loud: **replacing
an O(n) membership check inside an O(n) loop with a set turns O(n^2) into
O(n).** That single move fixes a large fraction of slow production code.

## 3. The structures, one paragraph each

**Array / dynamic list.** Contiguous memory, O(1) index, amortized O(1) append
because it doubles capacity when full. Default choice.

**Linked list.** O(1) insert or delete given the node, O(n) to find it. Poor
cache behavior. In interviews it exists mainly to test pointer manipulation.

**Stack (LIFO).** Undo, expression parsing, depth-first traversal, call frames.

**Queue (FIFO) and deque.** Work queues, breadth-first traversal, sliding
windows, and bounded buffers for backpressure.

**Hash map / hash set.** Average O(1), worst case O(n) with adversarial
collisions. Requires stable hash and equality. Unordered.

**Tree map / balanced BST.** O(log n) with sorted iteration and range queries.
Reach for it when you need "everything between these two timestamps."

**Heap / priority queue.** O(1) peek at the extreme, O(log n) push and pop. Use
for top-k, schedulers, and merging sorted streams.

**Graph.** Nodes plus edges, usually stored as an adjacency map. Dependency
resolution, network topology, and reachability are all graph problems, which is
worth noting on a system built of interconnected sites and services.

## 4. Choosing the structure: a decision script

Say this reasoning out loud during an interview.

1. Do I need **fast lookup by key**? Hash map.
2. Do I need **order**? Sorted structure or sort once up front.
3. Do I need **the extreme element repeatedly**? Heap.
4. Do I need **both ends**? Deque.
5. Do I need **uniqueness**? Set.
6. Do I need **range queries**? Tree map or a sorted list with binary search.
7. Otherwise, a list.

## 5. Patterns that cover most interview problems

### Frequency map

```python
from collections import Counter, defaultdict

counts = Counter(sensor_ids)
counts.most_common(3)

groups = defaultdict(list)
for det in detections:
    groups[det.sensor_id].append(det)
```

### Two pointers

```python
def has_pair_with_sum(sorted_nums, target):
    lo, hi = 0, len(sorted_nums) - 1
    while lo < hi:
        s = sorted_nums[lo] + sorted_nums[hi]
        if s == target:
            return True
        if s < target:
            lo += 1
        else:
            hi -= 1
    return False
```

### Sliding window

```python
def max_sum_window(nums, k):
    if len(nums) < k:
        return None
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]     # add one, drop one: O(n) total
        best = max(best, window)
    return best
```

### Binary search

```python
def binary_search(sorted_xs, target):
    lo, hi = 0, len(sorted_xs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_xs[mid] == target:
            return mid
        if sorted_xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

import bisect
i = bisect.bisect_left(sorted_xs, target)   # use the library in real code
```

Get the boundary conditions right by testing on a two-element list. Off-by-one
in binary search is the most common live-coding failure there is.

### Top-k with a heap

```python
import heapq

def top_k(items, k, key):
    """O(n log k) time, O(k) space -- better than sorting when k << n."""
    heap = []
    for item in items:
        heapq.heappush(heap, (key(item), item))
        if len(heap) > k:
            heapq.heappop(heap)             # drop the smallest
    return [item for _, item in sorted(heap, reverse=True)]
```

### Interval merge

```python
def merge_intervals(intervals):
    if not intervals:
        return []
    ordered = sorted(intervals)
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [tuple(iv) for iv in merged]
```

Real use: coalescing sensor coverage windows or radar dwell times.

### BFS and DFS on a graph

```python
from collections import deque

def bfs(graph, start):
    """Shortest hop count in an unweighted graph."""
    seen = {start}
    order = []
    q = deque([start])
    while q:
        node = q.popleft()
        order.append(node)
        for nbr in graph.get(node, ()):
            if nbr not in seen:
                seen.add(nbr)
                q.append(nbr)
    return order

def dfs(graph, node, seen=None):
    seen = set() if seen is None else seen
    seen.add(node)
    for nbr in graph.get(node, ()):
        if nbr not in seen:
            dfs(graph, nbr, seen)
    return seen
```

### Topological sort

Directly relevant: this is how build systems and service startup ordering work.

```python
def topo_sort(graph):
    """Kahn's algorithm. Raises if there is a cycle."""
    indegree = {n: 0 for n in graph}
    for node in graph:
        for nbr in graph[node]:
            indegree[nbr] = indegree.get(nbr, 0) + 1
            graph.setdefault(nbr, [])
    ready = deque(n for n, d in indegree.items() if d == 0)
    order = []
    while ready:
        node = ready.popleft()
        order.append(node)
        for nbr in graph[node]:
            indegree[nbr] -= 1
            if indegree[nbr] == 0:
                ready.append(nbr)
    if len(order) != len(indegree):
        raise ValueError("dependency cycle detected")
    return order
```

### Recursion with memoization

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def ways(n):
    if n <= 1:
        return 1
    return ways(n - 1) + ways(n - 2)
```

## 6. Sorting, enough to discuss

You will not implement quicksort. You may be asked about it.

| Algorithm | Average | Worst | Space | Stable |
| --- | --- | --- | --- | --- |
| Quicksort | O(n log n) | O(n^2) | O(log n) | no |
| Mergesort | O(n log n) | O(n log n) | O(n) | yes |
| Heapsort | O(n log n) | O(n log n) | O(1) | no |
| Insertion | O(n^2) | O(n^2) | O(1) | yes |
| Timsort (Python, Java objects) | O(n log n) | O(n log n) | O(n) | yes |

Useful things to say: Python's `sorted` and Java's `Collections.sort` use
Timsort, which is a merge sort adapted to exploit existing runs, so nearly
sorted data is close to linear. Java sorts primitives with dual-pivot quicksort
because stability does not matter for primitives.

## 7. A worked example, narrated

**Problem.** Given a large log file of `timestamp,sensor_id,confidence` lines,
find the three sensors with the highest average confidence, ignoring sensors
with fewer than ten records.

**Narrate it like this.**

> First, clarifying questions. How large is the file? If it is tens of gigabytes
> I want to stream it, not load it. Are malformed lines possible? I'll assume
> yes and skip them with a warning count. Is "top three" by average, with ties
> broken how? I'll break ties by sensor id for determinism, and I'll mention
> that because determinism matters for testing.
>
> Approach: one pass, accumulating a running sum and count per sensor. That is
> O(n) time and O(s) space where s is the number of distinct sensors, which is
> small. Then filter by the minimum count and take the top three. Since s is
> small, sorting is fine; if s were huge I'd use a heap for O(s log 3).

```python
from collections import defaultdict

def top_sensors(lines, k=3, min_records=10):
    sums = defaultdict(float)
    counts = defaultdict(int)
    skipped = 0

    for line in lines:
        parts = line.strip().split(",")
        if len(parts) != 3:
            skipped += 1
            continue
        _, sensor_id, raw_conf = parts
        try:
            conf = float(raw_conf)
        except ValueError:
            skipped += 1
            continue
        sums[sensor_id] += conf
        counts[sensor_id] += 1

    eligible = [
        (sums[s] / counts[s], s)
        for s in sums
        if counts[s] >= min_records
    ]
    eligible.sort(key=lambda pair: (-pair[0], pair[1]))
    return [s for _, s in eligible[:k]], skipped
```

> Tests I would write: empty input; a file where every line is malformed; a
> sensor with exactly nine records, which must be excluded; a sensor with
> exactly ten, which must be included; a tie broken by id; and one large
> generated file to confirm memory stays flat.

That last paragraph is what separates a senior answer from a correct one.

## 8. Twenty-four practice problems

Do them timed. Twenty minutes each. Write tests for at least half. Reference
solutions live in the [practice repo](../practice/README.html).

### Warm-up (A1&ndash;A6)

**A1.** Reverse the words in a sentence without using `split` on the whole
string at once. Handle multiple spaces.

**A2.** Return the first non-repeating character in a string, or `None`.

**A3.** Determine whether two strings are anagrams. Give both the sort-based and
the count-based solution and compare their complexity.

**A4.** Given a list of integers, return the two that sum to a target. O(n).

**A5.** Given a list of integers, find the missing number in the range 1..n.
Give two solutions: a set, and the arithmetic sum. Discuss overflow.

**A6.** Compress a string: `"aaabbc"` becomes `"a3b2c1"`, but only return the
compressed version if it is actually shorter.

### Collections and grouping (A7&ndash;A12)

**A7.** Group a list of file paths by extension into a dict of lists.

**A8.** Given a list of `(name, score)` tuples, return a dict of name to average
score, then the top three names.

**A9.** Find the k most frequent elements in a list. Do it in O(n log k).

**A10.** Given two lists of records keyed by id, produce the ids only in the
first, only in the second, and in both. Set operations.

**A11.** Implement `flatten(nested)` for arbitrarily nested lists. Recursive
first, then iterative with an explicit stack.

**A12.** Given a list of dictionaries, sort by one key ascending and a second
key descending.

### Algorithmic (A13&ndash;A18)

**A13.** Merge k sorted lists into one sorted list. Use a heap, O(n log k).

**A14.** Find the longest substring without repeating characters. Sliding
window.

**A15.** Given a list of intervals, return the minimum number of "rooms" needed
so that no two overlapping intervals share one. Classic sweep line.

**A16.** Validate that a string of brackets is balanced. Stack.

**A17.** Binary search for the first element greater than or equal to a target
in a sorted list. Return the insertion index if absent.

**A18.** Given a directed graph of service dependencies, return a valid startup
order, or report the cycle.

### Job-shaped (A19&ndash;A24)

These are closer to what you would actually be asked on this program.

**A19.** Parse a log file and report, per hour, the count of each log level.
Stream it; do not load the file.

**A20.** Given a stream of detections with timestamps that mostly increase,
detect and report any record whose timestamp is earlier than the previous one,
along with how far it went backwards.

**A21.** Given a list of `(track_id, timestamp, lat, lon)` position reports,
compute each track's average speed in km/h. Use the haversine formula. Handle
tracks with only one report.

**A22.** Implement a rate limiter: `allow(client_id, now)` returns `True` at
most `n` times in any rolling sixty-second window per client. Use a deque per
client and explain the memory growth and how you would bound it.

**A23.** Given two versions of a configuration file parsed into nested
dictionaries, produce a diff: keys added, keys removed, and values changed with
old and new. This is a real tech-refresh task.

**A24.** Given a list of installed package versions and a list of advisories of
the form `(package, first_vulnerable, first_fixed)`, report which installed
packages need upgrading. Implement a correct semantic version comparison rather
than comparing strings, and explain why string comparison fails.

A24 is the one I would most expect on this program. If you have limited time, do
A19, A20, A22, A23, and A24.

## 9. What to say when you get stuck

Stalling silently is the only unrecoverable failure mode. Have these lines
ready:

- "Let me do the brute force first so we have something correct, then improve
  it."
- "I want to work a concrete example by hand before I write code." Then actually
  do it on paper or in a comment.
- "I think this is a graph problem in disguise. The nodes are the services and
  the edges are the dependencies. Does that match what you had in mind?"
- "I know there is a linear solution using a hash map here. Let me get the
  quadratic one down first and then see if I can spot it."
- "I'm blanking on the exact library call. The idea is a min-heap of size k."

All of those keep the interviewer engaged and give them a place to help you.
Interviewers want to help. Let them.
