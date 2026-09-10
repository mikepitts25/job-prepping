"""Tests for the track data module.

Read these before reading tracks.py. The edge cases they cover -- time
tolerance, split tracks, renumbered tracks, spurious tracks, truncated
messages -- are the ones worth naming out loud in an interview.
"""

import math

import pytest

from tracks import (
    POSITION_REPORT_SPEC,
    FieldSpec,
    Sample,
    SiapMetrics,
    associate,
    decode,
    extract_bits,
    haversine_km,
    regression_report,
    siap_metrics,
    spec_width_bits,
    to_signed,
)


# --- bit extraction --------------------------------------------------------

def test_extract_bits_msb_first():
    assert extract_bits(bytes([0b10110000]), 0, 4) == 0b1011
    assert extract_bits(bytes([0b10110000]), 4, 4) == 0b0000
    assert extract_bits(bytes([0b10110000]), 1, 3) == 0b011


def test_extract_bits_spans_byte_boundary():
    buf = bytes([0b00000011, 0b11000000])
    assert extract_bits(buf, 6, 4) == 0b1111


def test_extract_bits_rejects_reads_past_the_end():
    with pytest.raises(ValueError, match="outside"):
        extract_bits(bytes([0xFF]), 4, 8)


def test_extract_bits_rejects_zero_length():
    with pytest.raises(ValueError):
        extract_bits(bytes([0xFF]), 0, 0)


@pytest.mark.parametrize("raw,bits,expected", [
    (0b0111, 4, 7),
    (0b1000, 4, -8),
    (0b1111, 4, -1),
    (0, 8, 0),
    (0xFF, 8, -1),
])
def test_to_signed(raw, bits, expected):
    assert to_signed(raw, bits) == expected


# --- field tables ----------------------------------------------------------

def test_spec_width_matches_the_documented_record_length():
    # 88 bits == 11 bytes. Asserting this is how you catch a transcription
    # error in a field table before it reaches the lab.
    assert spec_width_bits(POSITION_REPORT_SPEC) == 88


def test_spec_detects_overlapping_fields():
    bad = (FieldSpec("a", 0, 8), FieldSpec("b", 4, 8))
    with pytest.raises(ValueError, match="overlaps"):
        spec_width_bits(bad)


def test_decode_applies_scaling_and_sign():
    spec = (
        FieldSpec("angle_deg", 0, 8, signed=True, lsb=2.0),
        FieldSpec("count", 8, 8),
    )
    raw = bytes([0xFF, 0x05])          # -1 * 2.0, then 5
    decoded = decode(raw, spec)
    assert decoded["angle_deg"] == pytest.approx(-2.0)
    assert decoded["count"] == 5


def test_decode_round_trips_a_position_report():
    # Build a record with a known track number and quality, then read it back.
    bits = ["0" * 49]                                   # lat, lon: zero
    bits.append(format(40, "013b"))                     # altitude: 40 * 25 ft
    bits.append(format(1234, "015b"))                   # track number
    bits.append(format(12, "04b"))                      # track quality
    bits.append("0" * 7)                                # spare
    stream = "".join(bits)
    raw = bytes(int(stream[i:i + 8], 2) for i in range(0, len(stream), 8))

    decoded = decode(raw, POSITION_REPORT_SPEC)
    assert decoded["track_number"] == 1234
    assert decoded["track_quality"] == 12
    assert decoded["altitude_ft"] == pytest.approx(1000.0)
    assert decoded["latitude_deg"] == pytest.approx(0.0)


# --- geometry --------------------------------------------------------------

def test_haversine_abu_dhabi_to_dubai():
    assert haversine_km(24.4539, 54.3773, 25.2048, 55.2708) == pytest.approx(120, abs=10)


def test_haversine_is_zero_for_one_point():
    assert haversine_km(24.0, 54.0, 24.0, 54.0) == pytest.approx(0.0, abs=1e-9)


# --- association -----------------------------------------------------------

def test_association_requires_time_agreement():
    truth = [Sample("OBJ1", 100.0, 24.0, 54.0)]
    # Same position, but ten seconds later: must not associate.
    system = [Sample("T1", 110.0, 24.0, 54.0)]
    assert associate(truth, system, gate_km=5.0, time_tolerance_s=0.5) == []


def test_association_requires_distance_gate():
    truth = [Sample("OBJ1", 100.0, 24.0, 54.0)]
    system = [Sample("T1", 100.0, 25.0, 55.0)]      # ~140 km away
    assert associate(truth, system, gate_km=5.0) == []


def test_association_picks_the_nearest_truth_object():
    truth = [
        Sample("NEAR", 100.0, 24.000, 54.000),
        Sample("FAR", 100.0, 24.030, 54.000),
    ]
    system = [Sample("T1", 100.0, 24.001, 54.000)]
    pairs = associate(truth, system, gate_km=10.0)
    assert len(pairs) == 1
    assert pairs[0][0].ident == "NEAR"


# --- metrics ---------------------------------------------------------------

def _straight_truth(ident, n=5, lat0=24.0):
    return [Sample(ident, float(t), lat0 + 0.001 * t, 54.0) for t in range(n)]


def test_perfect_tracking_scores_perfectly():
    truth = _straight_truth("OBJ1")
    system = [Sample("T1", s.time_s, s.lat, s.lon) for s in truth]

    m = siap_metrics(truth, system)
    assert m.truth_objects == 1
    assert m.completeness == pytest.approx(1.0)
    assert m.ambiguity == pytest.approx(1.0)
    assert m.continuity == pytest.approx(1.0)
    assert m.position_rms_km == pytest.approx(0.0, abs=1e-9)
    assert m.spurious_tracks == 0


def test_missed_object_lowers_completeness():
    truth = _straight_truth("OBJ1") + _straight_truth("OBJ2", lat0=25.0)
    system = [Sample("T1", s.time_s, s.lat, s.lon) for s in _straight_truth("OBJ1")]

    m = siap_metrics(truth, system)
    assert m.truth_objects == 2
    assert m.tracked_objects == 1
    assert m.completeness == pytest.approx(0.5)


def test_split_track_raises_ambiguity_and_lowers_continuity():
    truth = _straight_truth("OBJ1")
    # The system holds two track numbers on the same object.
    system = (
        [Sample("T1", s.time_s, s.lat, s.lon) for s in truth]
        + [Sample("T2", s.time_s, s.lat, s.lon) for s in truth]
    )

    m = siap_metrics(truth, system)
    assert m.ambiguity == pytest.approx(2.0)
    assert m.continuity == pytest.approx(0.0)
    assert m.completeness == pytest.approx(1.0), "the object IS tracked, just twice"


def test_renumbered_track_breaks_continuity():
    truth = _straight_truth("OBJ1", n=6)
    system = (
        [Sample("T1", s.time_s, s.lat, s.lon) for s in truth[:3]]
        + [Sample("T9", s.time_s, s.lat, s.lon) for s in truth[3:]]
    )

    m = siap_metrics(truth, system)
    assert m.continuity == pytest.approx(0.0)
    assert m.completeness == pytest.approx(1.0)


def test_false_track_counts_as_spurious():
    truth = _straight_truth("OBJ1")
    system = (
        [Sample("T1", s.time_s, s.lat, s.lon) for s in truth]
        + [Sample("GHOST", 0.0, 40.0, 10.0)]        # nowhere near anything
    )

    m = siap_metrics(truth, system)
    assert m.spurious_tracks == 1
    assert m.completeness == pytest.approx(1.0)


def test_position_error_is_reported_in_km():
    truth = [Sample("OBJ1", 0.0, 24.0, 54.0)]
    system = [Sample("T1", 0.0, 24.009, 54.0)]      # ~1 km north

    m = siap_metrics(truth, system, gate_km=5.0)
    assert m.position_rms_km == pytest.approx(1.0, abs=0.1)


def test_empty_inputs_do_not_divide_by_zero():
    m = siap_metrics([], [])
    assert m.truth_objects == 0
    assert m.completeness == 0.0
    assert m.ambiguity == 0.0
    assert not math.isnan(m.position_rms_km)


# --- regression reporting --------------------------------------------------

def test_identical_runs_report_no_regression():
    m = SiapMetrics(completeness=0.99, continuity=0.98, ambiguity=1.0,
                    position_rms_km=0.4, spurious_tracks=2)
    assert regression_report(m, m) == []


def test_small_movement_within_tolerance_is_accepted():
    base = SiapMetrics(completeness=0.99, continuity=0.98, ambiguity=1.00,
                       position_rms_km=0.40, spurious_tracks=2)
    candidate = SiapMetrics(completeness=0.985, continuity=0.975, ambiguity=1.02,
                            position_rms_km=0.45, spurious_tracks=2)
    assert regression_report(base, candidate) == []


def test_degraded_completeness_is_reported():
    base = SiapMetrics(completeness=0.99, continuity=0.98)
    candidate = SiapMetrics(completeness=0.80, continuity=0.98)
    findings = regression_report(base, candidate)
    assert len(findings) == 1
    assert "completeness" in findings[0]


def test_new_false_tracks_are_reported_with_zero_tolerance():
    base = SiapMetrics(spurious_tracks=0)
    candidate = SiapMetrics(spurious_tracks=1)
    findings = regression_report(base, candidate)
    assert any("spurious_tracks" in f for f in findings)


def test_tolerances_can_be_overridden():
    base = SiapMetrics(completeness=0.99)
    candidate = SiapMetrics(completeness=0.80)
    assert regression_report(base, candidate, {"completeness": 0.5}) == []
