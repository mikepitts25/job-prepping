"""Tests for the practice problems.

By default these run against solutions.py. To grade your own attempts:

    PREP_TARGET=exercises pytest -q

Read these tests before you write code. Naming the edge cases out loud is a
large part of what a technical interview is grading.
"""

import importlib
import os

import pytest

target = importlib.import_module(os.environ.get("PREP_TARGET", "solutions"))


def implemented(name):
    """Skip cleanly when working through exercises.py stubs."""
    fn = getattr(target, name, None)
    if fn is None:
        pytest.skip(f"{name} not defined in {target.__name__}")
    return fn


# --- parse_detections ------------------------------------------------------

def test_parse_detections_happy_path():
    parse = implemented("parse_detections")
    good, bad = parse(["RDR-1,1000,0.9", "RDR-2,1001,0.4"])
    assert bad == 0
    assert [d.sensor_id for d in good] == ["RDR-1", "RDR-2"]
    assert good[0].confidence == pytest.approx(0.9)


def test_parse_detections_counts_malformed():
    parse = implemented("parse_detections")
    good, bad = parse([
        "RDR-1,1000,0.9",
        "not,enough",
        "RDR-2,notanumber,0.5",
        ",1000,0.5",
        "RDR-3,1000,4.2",
    ])
    assert len(good) == 1
    assert bad == 4


def test_parse_detections_ignores_blanks_and_comments():
    parse = implemented("parse_detections")
    good, bad = parse(["", "   ", "# header", "RDR-1,1,0.5"])
    assert len(good) == 1 and bad == 0


def test_parse_detections_empty_input():
    parse = implemented("parse_detections")
    assert parse([]) == ([], 0)


# --- top_sensors -----------------------------------------------------------

def test_top_sensors_orders_by_mean_confidence():
    top = implemented("top_sensors")
    lines = ["A,1,0.2", "A,2,0.4", "B,1,0.9", "C,1,0.5"]
    assert top(lines, k=3) == ["B", "C", "A"]


def test_top_sensors_ties_break_by_id():
    top = implemented("top_sensors")
    assert top(["B,1,0.5", "A,1,0.5"], k=2) == ["A", "B"]


def test_top_sensors_respects_min_records():
    top = implemented("top_sensors")
    lines = ["A,1,0.9"] + [f"B,{i},0.5" for i in range(10)]
    assert top(lines, k=2, min_records=10) == ["B"]


def test_top_sensors_empty_input():
    top = implemented("top_sensors")
    assert top([]) == []


# --- log_levels_by_hour ----------------------------------------------------

def test_log_levels_by_hour():
    fn = implemented("log_levels_by_hour")
    lines = [
        "2026-09-09T14:01:02Z ERROR adapter timed out",
        "2026-09-09T14:59:59Z ERROR adapter timed out",
        "2026-09-09T15:00:00Z INFO started",
        "garbage line",
    ]
    result = fn(lines)
    assert result["2026-09-09T14"]["ERROR"] == 2
    assert result["2026-09-09T15"]["INFO"] == 1
    assert "2026-09-09T16" not in result


# --- chunk -----------------------------------------------------------------

def test_chunk_uneven_tail():
    chunk = implemented("chunk")
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_exact_fit_and_empty():
    chunk = implemented("chunk")
    assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]
    assert chunk([], 3) == []


def test_chunk_rejects_bad_size():
    chunk = implemented("chunk")
    with pytest.raises(ValueError):
        chunk([1, 2, 3], 0)


# --- merge_intervals -------------------------------------------------------

@pytest.mark.parametrize("given,expected", [
    ([], []),
    ([(1, 3)], [(1, 3)]),
    ([(1, 3), (2, 6), (8, 10)], [(1, 6), (8, 10)]),
    ([(8, 10), (1, 3), (2, 6)], [(1, 6), (8, 10)]),
    ([(1, 5), (2, 3)], [(1, 5)]),
    ([(1, 2), (2, 3)], [(1, 3)]),
])
def test_merge_intervals(given, expected):
    merge = implemented("merge_intervals")
    assert merge(given) == expected


# --- flatten / merge_counts / top_k_frequent -------------------------------

def test_flatten_deeply_nested():
    flatten = implemented("flatten")
    assert flatten([1, [2, [3, [4, [5]]]], 6]) == [1, 2, 3, 4, 5, 6]


def test_flatten_keeps_strings_whole():
    flatten = implemented("flatten")
    assert flatten(["ab", ["cd"]]) == ["ab", "cd"]


def test_merge_counts_does_not_mutate():
    merge = implemented("merge_counts")
    a, b = {"x": 1, "y": 2}, {"y": 3, "z": 4}
    assert merge(a, b) == {"x": 1, "y": 5, "z": 4}
    assert a == {"x": 1, "y": 2}
    assert b == {"y": 3, "z": 4}


def test_top_k_frequent():
    fn = implemented("top_k_frequent")
    assert fn(["a", "b", "a", "c", "b", "a"], 2) == ["a", "b"]
    assert fn([], 3) == []


# --- find_time_regressions -------------------------------------------------

def test_no_regressions_when_monotonic():
    fn = implemented("find_time_regressions")
    assert fn([1.0, 2.0, 3.0]) == []


def test_equal_timestamps_are_not_regressions():
    fn = implemented("find_time_regressions")
    assert fn([1.0, 1.0, 1.0]) == []


def test_reports_regression_with_delta():
    fn = implemented("find_time_regressions")
    assert fn([1.0, 5.0, 3.0, 6.0]) == [(2, 3.0, 2.0)]


def test_measures_against_running_max_not_previous():
    fn = implemented("find_time_regressions")
    # index 2 drops below the max of 9, and so does index 3.
    assert fn([1.0, 9.0, 4.0, 5.0]) == [(2, 4.0, 5.0), (3, 5.0, 4.0)]


# --- geodesy ---------------------------------------------------------------

def test_haversine_known_distance():
    fn = implemented("haversine_km")
    # Abu Dhabi to Dubai, roughly 120 km.
    assert fn(24.4539, 54.3773, 25.2048, 55.2708) == pytest.approx(120, abs=10)


def test_haversine_zero_for_same_point():
    fn = implemented("haversine_km")
    assert fn(24.0, 54.0, 24.0, 54.0) == pytest.approx(0.0, abs=1e-9)


def test_average_speed_of_a_straight_track():
    fn = implemented("average_speeds_kph")
    reports = [
        ("T1", 0.0, 24.4539, 54.3773),
        ("T1", 3600.0, 25.2048, 55.2708),
        ("T2", 0.0, 24.0, 54.0),          # only one report: omitted
    ]
    speeds = fn(reports)
    assert "T2" not in speeds
    assert speeds["T1"] == pytest.approx(120, abs=10)


# --- RingBuffer ------------------------------------------------------------

def test_ring_buffer_drops_oldest_and_counts():
    RingBuffer = implemented("RingBuffer")
    buf = RingBuffer(3)
    for i in range(5):
        buf.push(i)
    assert len(buf) == 3
    assert buf.latest(3) == [4, 3, 2]
    assert buf.dropped == 2


def test_ring_buffer_latest_clamps():
    RingBuffer = implemented("RingBuffer")
    buf = RingBuffer(5)
    buf.push("a")
    assert buf.latest(10) == ["a"]
    assert buf.latest(0) == []


def test_ring_buffer_rejects_bad_capacity():
    RingBuffer = implemented("RingBuffer")
    with pytest.raises(ValueError):
        RingBuffer(0)


# --- RateLimiter -----------------------------------------------------------

def test_rate_limiter_allows_then_blocks():
    RateLimiter = implemented("RateLimiter")
    clock = [1000.0]
    limiter = RateLimiter(limit=3, window_s=60.0, now=lambda: clock[0])

    assert [limiter.allow("c1") for _ in range(4)] == [True, True, True, False]


def test_rate_limiter_window_slides():
    RateLimiter = implemented("RateLimiter")
    clock = [1000.0]
    limiter = RateLimiter(limit=2, window_s=60.0, now=lambda: clock[0])

    assert limiter.allow("c1") and limiter.allow("c1")
    assert not limiter.allow("c1")
    clock[0] += 61.0
    assert limiter.allow("c1")


def test_rate_limiter_is_per_client():
    RateLimiter = implemented("RateLimiter")
    limiter = RateLimiter(limit=1, window_s=60.0, now=lambda: 0.0)
    assert limiter.allow("a")
    assert limiter.allow("b")
    assert not limiter.allow("a")


# --- config diffing --------------------------------------------------------

def test_flatten_config():
    fn = implemented("flatten_config")
    assert fn({"a": {"b": {"c": 1}}, "d": 2}) == {"a.b.c": 1, "d": 2}


def test_flatten_config_keeps_empty_section():
    fn = implemented("flatten_config")
    assert fn({"a": {}}) == {"a": {}}


def test_diff_config():
    fn = implemented("diff_config")
    old = {"log": {"level": "INFO"}, "queue": {"size": 1000}, "gone": True}
    new = {"log": {"level": "DEBUG"}, "queue": {"size": 1000}, "added": 1}
    diff = fn(old, new)
    assert diff["changed"] == {"log.level": ("INFO", "DEBUG")}
    assert diff["added"] == {"added": 1}
    assert diff["removed"] == {"gone": True}


def test_diff_config_identical_is_empty():
    fn = implemented("diff_config")
    cfg = {"a": {"b": 1}}
    diff = fn(cfg, dict(cfg))
    assert diff == {"added": {}, "removed": {}, "changed": {}}


# --- version handling ------------------------------------------------------

@pytest.mark.parametrize("a,b,expected", [
    ("1.9", "1.10", -1),          # the case string comparison gets wrong
    ("1.10", "1.9", 1),
    ("2.0", "2.0.0", 0),
    ("1.4.0", "1.4.1", -1),
    ("v2.1.3", "2.1.3", 0),
    ("1.4.0-rc1", "1.4.0", 0),    # documented simplification
])
def test_compare_versions(a, b, expected):
    fn = implemented("compare_versions")
    assert fn(a, b) == expected


def test_packages_needing_upgrade():
    fn = implemented("packages_needing_upgrade")
    installed = {"log4j": "2.14.1", "requests": "2.32.3", "pyyaml": "5.3.1"}
    advisories = [
        ("log4j", "2.0", "2.17.1"),
        ("pyyaml", "5.1", "5.4"),
        ("requests", "2.0", "2.20.0"),      # installed is already newer
        ("absent-package", "1.0", "2.0"),   # not installed
    ]
    assert fn(installed, advisories) == [
        ("log4j", "2.14.1", "2.17.1"),
        ("pyyaml", "5.3.1", "5.4"),
    ]


def test_packages_needing_upgrade_takes_highest_fix():
    fn = implemented("packages_needing_upgrade")
    installed = {"lib": "1.0"}
    advisories = [("lib", "0.9", "1.2"), ("lib", "0.9", "1.5")]
    assert fn(installed, advisories) == [("lib", "1.0", "1.5")]


# --- startup_order ---------------------------------------------------------

def test_startup_order_respects_dependencies():
    fn = implemented("startup_order")
    graph = {"db": ["api"], "api": ["ui"], "ui": []}
    assert fn(graph) == ["db", "api", "ui"]


def test_startup_order_is_deterministic():
    fn = implemented("startup_order")
    graph = {"z": [], "a": [], "m": []}
    assert fn(graph) == ["a", "m", "z"]


def test_startup_order_detects_cycle():
    fn = implemented("startup_order")
    with pytest.raises(ValueError, match="cycle"):
        fn({"a": ["b"], "b": ["c"], "c": ["a"]})


# --- retry -----------------------------------------------------------------

def test_retry_succeeds_after_transient_failures():
    retry = implemented("retry")
    slept: list[float] = []
    attempts = {"n": 0}

    @retry(times=3, delay=1.0, backoff=2.0, exc=TimeoutError, sleep=slept.append)
    def flaky():
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise TimeoutError("no route")
        return "ok"

    assert flaky() == "ok"
    assert attempts["n"] == 3
    assert slept == [1.0, 2.0]        # exponential, and no sleep after success


def test_retry_reraises_after_exhaustion():
    retry = implemented("retry")

    @retry(times=2, delay=0.0, exc=ValueError, sleep=lambda _: None)
    def always_fails():
        raise ValueError("permanent")

    with pytest.raises(ValueError, match="permanent"):
        always_fails()


def test_retry_does_not_swallow_other_exceptions():
    retry = implemented("retry")
    calls = {"n": 0}

    @retry(times=3, delay=0.0, exc=TimeoutError, sleep=lambda _: None)
    def wrong_error():
        calls["n"] += 1
        raise KeyError("different")

    with pytest.raises(KeyError):
        wrong_error()
    assert calls["n"] == 1            # not retried


def test_retry_preserves_metadata():
    retry = implemented("retry")

    @retry(times=1, sleep=lambda _: None)
    def documented():
        """Keeps its docstring."""

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "Keeps its docstring."
