"""Reference solutions for the EADGE-T interview practice problems.

Every function here is one you could plausibly be asked to write in a screening
interview for this role. Read the docstrings for the edge cases that matter --
naming those out loud is worth as much as the code.

Run the tests:     pytest -q
Against your own:  PREP_TARGET=exercises pytest -q
"""

from __future__ import annotations

import functools
import logging
import math
import re
import time
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Iterator, Sequence

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# P1 / A19 -- parsing and aggregation
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Detection:
    """One sensor report, normalized."""

    sensor_id: str
    timestamp: float
    confidence: float


def parse_detections(lines: Iterable[str]) -> tuple[list[Detection], int]:
    """Parse ``sensor_id,timestamp,confidence`` lines.

    Returns the good records and a count of the bad ones. Skipping bad input
    rather than raising is the right call for a sustainment ingest path: one
    corrupt record must not stop the stream. Counting them is what makes the
    problem visible instead of silent.

    Blank lines and lines starting with '#' are treated as comments, not errors.
    """
    good: list[Detection] = []
    bad = 0
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(",")
        if len(parts) != 3:
            bad += 1
            continue
        sensor_id, raw_ts, raw_conf = (p.strip() for p in parts)
        if not sensor_id:
            bad += 1
            continue
        try:
            timestamp = float(raw_ts)
            confidence = float(raw_conf)
        except ValueError:
            bad += 1
            continue
        if not (0.0 <= confidence <= 1.0) or math.isnan(timestamp):
            bad += 1
            continue
        good.append(Detection(sensor_id, timestamp, confidence))
    return good, bad


def top_sensors(
    lines: Iterable[str], k: int = 3, min_records: int = 1
) -> list[str]:
    """Sensors with the highest mean confidence, best first.

    Ties break by sensor id so the output is deterministic, which matters
    because a non-deterministic result is untestable. Sensors below
    ``min_records`` are excluded: a single lucky report is not evidence.

    One streaming pass, O(n) time and O(s) space in the number of sensors.
    """
    sums: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)

    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(",")
        if len(parts) != 3:
            continue
        sensor_id = parts[0].strip()
        try:
            confidence = float(parts[2])
        except ValueError:
            continue
        if not sensor_id:
            continue
        sums[sensor_id] += confidence
        counts[sensor_id] += 1

    eligible = [
        (sums[s] / counts[s], s) for s in sums if counts[s] >= min_records
    ]
    eligible.sort(key=lambda pair: (-pair[0], pair[1]))
    return [sensor_id for _, sensor_id in eligible[:k]]


LOG_LINE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2}[T ]\d{2}):\d{2}:\d{2}\S*\s+(?P<level>[A-Z]+)\b"
)


def log_levels_by_hour(lines: Iterable[str]) -> dict[str, Counter]:
    """Count each log level per hour, streaming.

    Keyed by the hour prefix, e.g. ``'2026-09-09T14'``. Takes an iterable so it
    works on an open file handle without loading it: constant memory in the
    file size, linear in the number of distinct hours.
    """
    per_hour: dict[str, Counter] = defaultdict(Counter)
    for line in lines:
        match = LOG_LINE.match(line.strip())
        if match is None:
            continue
        per_hour[match.group("ts")][match.group("level")] += 1
    return dict(per_hour)


# ---------------------------------------------------------------------------
# P2, P6, A11 -- collection manipulation
# ---------------------------------------------------------------------------

def chunk(items: Sequence[Any], size: int) -> list[list[Any]]:
    """Split a sequence into consecutive chunks of at most ``size``.

    Raises on a non-positive size rather than looping forever or returning
    something surprising. Fail fast at the boundary.
    """
    if size <= 0:
        raise ValueError(f"size must be positive, got {size}")
    return [list(items[i : i + size]) for i in range(0, len(items), size)]


def merge_intervals(
    intervals: Iterable[tuple[float, float]]
) -> list[tuple[float, float]]:
    """Merge overlapping and touching intervals.

    Sorting dominates, so O(n log n). Touching intervals (end == next start)
    merge; ask the interviewer whether that is what they want, because both
    answers are defensible and the question earns credit.
    """
    ordered = sorted(intervals)
    if not ordered:
        return []
    merged: list[list[float]] = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [(a, b) for a, b in merged]


def flatten(nested: Iterable[Any]) -> list[Any]:
    """Flatten arbitrarily nested lists and tuples, iteratively.

    Iterative rather than recursive so deep nesting cannot blow the stack.
    Strings and bytes are treated as scalars, which is the behavior people
    actually want.
    """
    out: list[Any] = []
    stack: list[Any] = list(nested)[::-1]
    while stack:
        item = stack.pop()
        if isinstance(item, (list, tuple)):
            stack.extend(list(item)[::-1])
        else:
            out.append(item)
    return out


def merge_counts(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    """Sum two count dictionaries without mutating either input."""
    merged = dict(a)
    for key, value in b.items():
        merged[key] = merged.get(key, 0) + value
    return merged


def top_k_frequent(items: Iterable[Any], k: int) -> list[Any]:
    """The k most common items, most frequent first.

    Ties break by the item's own ordering for determinism. Counter.most_common
    is what you would use in production; the point of writing it out is to be
    able to discuss the O(n log k) heap alternative when n is huge and k small.
    """
    counts = Counter(items)
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [item for item, _ in ranked[:k]]


# ---------------------------------------------------------------------------
# A20 -- stream sanity checks
# ---------------------------------------------------------------------------

def find_time_regressions(
    timestamps: Iterable[float],
) -> list[tuple[int, float, float]]:
    """Report records whose timestamp went backwards.

    Returns (index, timestamp, delta) where delta is how far back it jumped
    relative to the highest timestamp seen so far. Equal timestamps are not
    regressions; duplicate report times are normal in a multi-sensor feed.

    This is a real defect class: an out-of-order report can corrupt a track's
    state estimate, and it usually means clock skew between sites rather than a
    software bug.
    """
    regressions: list[tuple[int, float, float]] = []
    highest: float | None = None
    for index, ts in enumerate(timestamps):
        if highest is not None and ts < highest:
            regressions.append((index, ts, highest - ts))
        if highest is None or ts > highest:
            highest = ts
    return regressions


# ---------------------------------------------------------------------------
# A21 -- geodesy
# ---------------------------------------------------------------------------

EARTH_RADIUS_KM = 6371.0088


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometres between two WGS84 points.

    Spherical approximation. Good to a few tenths of a percent, which is fine
    for a speed sanity check and not fine for a fire-control solution -- know
    the difference and say so.
    """
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = phi2 - phi1
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def average_speeds_kph(
    reports: Iterable[tuple[str, float, float, float]]
) -> dict[str, float]:
    """Mean speed per track from (track_id, epoch_seconds, lat, lon) reports.

    Tracks with fewer than two reports, or with zero elapsed time, are omitted
    rather than reported as zero or infinity. Distance is summed along the
    path, not measured end to end, so a track that returns to its start does
    not report zero speed.
    """
    by_track: dict[str, list[tuple[float, float, float]]] = defaultdict(list)
    for track_id, ts, lat, lon in reports:
        by_track[track_id].append((ts, lat, lon))

    speeds: dict[str, float] = {}
    for track_id, points in by_track.items():
        points.sort()
        if len(points) < 2:
            continue
        elapsed_h = (points[-1][0] - points[0][0]) / 3600.0
        if elapsed_h <= 0:
            continue
        distance = sum(
            haversine_km(points[i][1], points[i][2], points[i + 1][1], points[i + 1][2])
            for i in range(len(points) - 1)
        )
        speeds[track_id] = distance / elapsed_h
    return speeds


# ---------------------------------------------------------------------------
# P7, A22 -- bounded state
# ---------------------------------------------------------------------------

class RingBuffer:
    """Fixed-size buffer keeping the most recent ``capacity`` items.

    Bounded by construction: a deque with maxlen drops the oldest on overflow,
    which is the right policy for position reports because a stale position has
    no operational value. The dropped count makes the condition visible in
    metrics instead of silent.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._items: deque = deque(maxlen=capacity)
        self.capacity = capacity
        self.dropped = 0

    def push(self, item: Any) -> None:
        if len(self._items) == self.capacity:
            self.dropped += 1
        self._items.append(item)

    def latest(self, k: int = 1) -> list[Any]:
        """The k most recent items, newest first."""
        if k <= 0:
            return []
        return list(self._items)[-k:][::-1]

    def __len__(self) -> int:
        return len(self._items)


class RateLimiter:
    """Allow at most ``limit`` calls per client in a rolling window.

    A deque of timestamps per client, evicting from the front. Memory grows
    with the number of distinct clients, which is unbounded if client ids come
    from outside -- in production you would cap it with an LRU or sweep idle
    clients on a timer. Say that; the follow-up question is always about the
    memory.

    The clock is injected so the tests are deterministic. Never reach for
    time.time() inside logic you intend to test.
    """

    def __init__(self, limit: int, window_s: float = 60.0, now: Callable[[], float] = time.monotonic):
        if limit <= 0:
            raise ValueError("limit must be positive")
        self.limit = limit
        self.window_s = window_s
        self._now = now
        self._calls: dict[str, deque] = defaultdict(deque)

    def allow(self, client_id: str) -> bool:
        now = self._now()
        calls = self._calls[client_id]
        cutoff = now - self.window_s
        while calls and calls[0] <= cutoff:
            calls.popleft()
        if len(calls) >= self.limit:
            return False
        calls.append(now)
        return True


# ---------------------------------------------------------------------------
# P8, A23 -- configuration handling, a real tech-refresh task
# ---------------------------------------------------------------------------

def flatten_config(config: dict, prefix: str = "", sep: str = ".") -> dict[str, Any]:
    """Flatten nested config dicts into dotted keys.

    ``{"a": {"b": 1}}`` becomes ``{"a.b": 1}``. An empty dict is preserved as a
    leaf so that "this section exists but is empty" survives the round trip.
    """
    flat: dict[str, Any] = {}
    for key, value in config.items():
        full = f"{prefix}{sep}{key}" if prefix else str(key)
        if isinstance(value, dict) and value:
            flat.update(flatten_config(value, full, sep))
        else:
            flat[full] = value
    return flat


def diff_config(old: dict, new: dict) -> dict[str, Any]:
    """Diff two nested configs: added, removed, changed.

    Returns ``{"added": {...}, "removed": {...}, "changed": {key: (old, new)}}``
    over flattened keys. Comparing flattened keys rather than walking two trees
    keeps the output readable and makes a moved key show up honestly as one
    removal plus one addition.

    This is the shape of a genuine tech-refresh task: proving that a config
    migration changed exactly what you intended and nothing else.
    """
    flat_old = flatten_config(old)
    flat_new = flatten_config(new)
    old_keys, new_keys = set(flat_old), set(flat_new)

    return {
        "added": {k: flat_new[k] for k in sorted(new_keys - old_keys)},
        "removed": {k: flat_old[k] for k in sorted(old_keys - new_keys)},
        "changed": {
            k: (flat_old[k], flat_new[k])
            for k in sorted(old_keys & new_keys)
            if flat_old[k] != flat_new[k]
        },
    }


# ---------------------------------------------------------------------------
# A24 -- dependency upgrade triage
# ---------------------------------------------------------------------------

_VERSION_PART = re.compile(r"^(\d+)")


def parse_version(version: str) -> tuple[int, ...]:
    """Parse a dotted version into a comparable tuple of integers.

    Trailing non-numeric suffixes ('1.4.0-rc1', '2.1.3.el9') are truncated at
    the first non-digit within the component. That is a simplification, not a
    full PEP 440 or SemVer implementation, and saying so out loud is better
    than pretending otherwise.
    """
    parts: list[int] = []
    for component in version.strip().lstrip("vV").split("."):
        match = _VERSION_PART.match(component)
        if match is None:
            break
        parts.append(int(match.group(1)))
    return tuple(parts) or (0,)


def compare_versions(a: str, b: str) -> int:
    """Return -1, 0 or 1 comparing two version strings numerically.

    String comparison is wrong here and it is worth saying why: '1.10' sorts
    before '1.9' lexicographically, so a naive check reports a patched system
    as vulnerable, or worse, a vulnerable one as patched.
    """
    va, vb = parse_version(a), parse_version(b)
    length = max(len(va), len(vb))
    va += (0,) * (length - len(va))
    vb += (0,) * (length - len(vb))
    return (va > vb) - (va < vb)


def packages_needing_upgrade(
    installed: dict[str, str],
    advisories: Iterable[tuple[str, str, str]],
) -> list[tuple[str, str, str]]:
    """Which installed packages fall in a vulnerable range.

    ``advisories`` are ``(package, first_vulnerable, first_fixed)`` with the
    range half-open: vulnerable if ``first_vulnerable <= installed <
    first_fixed``. Returns ``(package, installed_version, required_version)``
    sorted by package, taking the highest required fix when several advisories
    hit the same package.
    """
    required: dict[str, str] = {}
    for package, first_vulnerable, first_fixed in advisories:
        current = installed.get(package)
        if current is None:
            continue
        if compare_versions(current, first_vulnerable) < 0:
            continue
        if compare_versions(current, first_fixed) >= 0:
            continue
        best = required.get(package)
        if best is None or compare_versions(first_fixed, best) > 0:
            required[package] = first_fixed
    return [(pkg, installed[pkg], fix) for pkg, fix in sorted(required.items())]


# ---------------------------------------------------------------------------
# A18 -- dependency ordering
# ---------------------------------------------------------------------------

def startup_order(graph: dict[str, Iterable[str]]) -> list[str]:
    """Topological order for a dependency graph, using Kahn's algorithm.

    ``graph[a] = [b]`` means "a must start before b". Raises ValueError naming
    the nodes involved in a cycle, because "there is a cycle" without saying
    where is not an actionable error message.

    Ready nodes are drained in sorted order so the output is deterministic,
    which is what makes it testable.
    """
    adjacency: dict[str, list[str]] = {n: list(d) for n, d in graph.items()}
    for dependents in list(adjacency.values()):
        for node in dependents:
            adjacency.setdefault(node, [])

    indegree = {node: 0 for node in adjacency}
    for node, dependents in adjacency.items():
        for dependent in dependents:
            indegree[dependent] += 1

    ready = deque(sorted(n for n, d in indegree.items() if d == 0))
    order: list[str] = []
    while ready:
        node = ready.popleft()
        order.append(node)
        newly_ready = []
        for dependent in adjacency[node]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                newly_ready.append(dependent)
        for node_ in sorted(newly_ready):
            ready.append(node_)

    if len(order) != len(adjacency):
        stuck = sorted(set(adjacency) - set(order))
        raise ValueError(f"dependency cycle among: {', '.join(stuck)}")
    return order


# ---------------------------------------------------------------------------
# P5 -- decorators
# ---------------------------------------------------------------------------

def retry(
    times: int = 3,
    delay: float = 0.05,
    backoff: float = 2.0,
    exc: type[BaseException] | tuple[type[BaseException], ...] = Exception,
    sleep: Callable[[float], None] = time.sleep,
):
    """Retry a callable with exponential backoff, re-raising the last failure.

    The sleep function is injected so tests do not actually wait. In production
    you would add jitter: synchronized retries from many clients are how a
    struggling service gets finished off.
    """
    if times < 1:
        raise ValueError("times must be at least 1")

    def decorate(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            wait = delay
            last: BaseException | None = None
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except exc as err:          # noqa: PERF203 -- retry is the point
                    last = err
                    log.warning("attempt %d/%d of %s failed: %s", attempt, times, fn.__name__, err)
                    if attempt < times:
                        sleep(wait)
                        wait *= backoff
            assert last is not None
            raise last

        return wrapper

    return decorate


# ---------------------------------------------------------------------------
# Streaming helper used by several of the above
# ---------------------------------------------------------------------------

def read_records(path: str) -> Iterator[tuple[int, str]]:
    """Yield (line_number, line) lazily, skipping blanks and comments.

    A generator so a 40 GB log can be processed on a machine with 8 GB of RAM.
    That sentence is the whole reason to write it this way, and it is a good
    one to say in an interview.
    """
    with open(path, encoding="utf-8", errors="replace") as handle:
        for lineno, raw in enumerate(handle, start=1):
            line = raw.strip()
            if line and not line.startswith("#"):
                yield lineno, line
