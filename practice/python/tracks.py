"""Track data handling: fixed-bit decoding and track-to-truth metrics.

This is the domain-shaped half of the practice repo. Two things live here, and
both are worth being able to talk about in an interview for an air and missile
defense C2 programme:

1. **Fixed-bit field decoding.** Tactical data link and surveillance formats
   pack fields at bit offsets with scaled integers, not floats, because link
   bandwidth is a planned budget. Writing an adapter for one of these is the
   single most likely piece of domain code in a sustainment role.

2. **Track-to-truth metrics.** The publicly documented Single Integrated Air
   Picture measures of performance -- completeness, ambiguity, accuracy,
   continuity -- computed against a truth set. This is how you regression-test
   a fusion system: replay a scenario through the new baseline and assert the
   metrics have not degraded against the previous one. You cannot unit-test
   "the air picture is still correct", but you can measure it.

Nothing here is specific to any real system. The formats are illustrative and
the metric definitions follow the open literature. See lesson 2 of the site.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Sequence

EARTH_RADIUS_KM = 6371.0088


# ---------------------------------------------------------------------------
# Fixed-bit field decoding
# ---------------------------------------------------------------------------

def extract_bits(buffer: bytes, offset: int, length: int) -> int:
    """Read ``length`` bits starting at bit ``offset``, most significant first.

    Bit ordering is the first thing to confirm against the specification and
    the first thing people get wrong. MSB-first within a byte is the common
    wire convention, and field numbering in a standard may start at 1 rather
    than 0. Ask before writing a line of decoder.

    Raises rather than reading past the end: a truncated message must fail
    loudly at the boundary, not produce a plausible wrong number.
    """
    if length <= 0:
        raise ValueError(f"length must be positive, got {length}")
    if offset < 0 or (offset + length) > len(buffer) * 8:
        raise ValueError(
            f"field [{offset}, {offset + length}) outside a {len(buffer) * 8}-bit buffer"
        )
    value = 0
    for i in range(offset, offset + length):
        bit = (buffer[i // 8] >> (7 - (i % 8))) & 1
        value = (value << 1) | bit
    return value


def to_signed(value: int, bits: int) -> int:
    """Interpret an unsigned field as two's complement of the given width."""
    if bits <= 0:
        raise ValueError("bits must be positive")
    sign_bit = 1 << (bits - 1)
    return value - (1 << bits) if value & sign_bit else value


@dataclass(frozen=True)
class FieldSpec:
    """One field in a packed record.

    Keeping the field map as data rather than as code in a decode function is
    the point: when the specification edition changes you edit one table, and a
    test can assert the table's total width against the documented record
    length. Hand-transcribing a few hundred offsets into if-statements is where
    transcription errors come from.
    """

    name: str
    offset: int
    bits: int
    signed: bool = False
    lsb: float = 1.0          # scale factor from the specification
    units: str = ""


def decode(buffer: bytes, spec: Sequence[FieldSpec]) -> dict[str, float]:
    """Decode a packed record against a field table.

    Scaling is applied here because the raw integer is meaningless on its own:
    getting an LSB value wrong scales every output by a constant, which looks
    like a tracking problem and is not.
    """
    out: dict[str, float] = {}
    for f in spec:
        raw = extract_bits(buffer, f.offset, f.bits)
        if f.signed:
            raw = to_signed(raw, f.bits)
        out[f.name] = raw * f.lsb if f.lsb != 1.0 else raw
    return out


def spec_width_bits(spec: Sequence[FieldSpec]) -> int:
    """Total bits covered by a field table, for asserting against the spec.

    Also catches overlapping fields, which is the transcription error that is
    hardest to spot by eye and easiest to catch with a test.
    """
    covered: set[int] = set()
    for f in spec:
        bits = set(range(f.offset, f.offset + f.bits))
        overlap = covered & bits
        if overlap:
            raise ValueError(f"field {f.name!r} overlaps at bit {min(overlap)}")
        covered |= bits
    return len(covered)


# An illustrative packed position report. The layout and scale factors are
# made up for practice; a real one comes from the controlling specification.
POSITION_REPORT_SPEC: tuple[FieldSpec, ...] = (
    FieldSpec("latitude_deg", 0, 24, signed=True, lsb=180.0 / (1 << 23), units="deg"),
    FieldSpec("longitude_deg", 24, 25, signed=True, lsb=180.0 / (1 << 23), units="deg"),
    FieldSpec("altitude_ft", 49, 13, lsb=25.0, units="ft"),
    FieldSpec("track_number", 62, 15),
    FieldSpec("track_quality", 77, 4),
    FieldSpec("spare", 81, 7),
)


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometres. Spherical approximation.

    Good to a few tenths of a percent, which is fine for association gating and
    metric reporting and not fine for a fire-control solution. Know the
    difference and say which one you are doing.
    """
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = phi2 - phi1
    dlambda = math.radians(lon2 - lon1)
    a = (math.sin(dphi / 2) ** 2
         + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


# ---------------------------------------------------------------------------
# Track-to-truth association and metrics
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Sample:
    """One position report at one time, from truth or from the system."""

    ident: str          # truth object id, or system track number
    time_s: float
    lat: float
    lon: float


@dataclass
class SiapMetrics:
    """Track-to-truth measures of performance.

    Definitions follow the public SIAP literature:

    * ``completeness`` -- fraction of truth objects that were tracked at all.
    * ``ambiguity`` -- mean number of distinct system tracks held on one truth
      object. One is correct; above one means the system has split an object.
    * ``position_rms_km`` -- root mean square position error of associated
      tracks against truth.
    * ``continuity`` -- fraction of truth objects that kept a single track
      number for their whole life. A renumbered track breaks an operator's
      situational awareness even when the position is perfect.
    * ``spurious_tracks`` -- system tracks that never associated with any truth
      object. These are false tracks.

    Ambiguity and continuity measure different failures and people confuse
    them: ambiguity is two tracks on one object *at once*, continuity is one
    object being renumbered *over time*.
    """

    truth_objects: int = 0
    tracked_objects: int = 0
    completeness: float = 0.0
    ambiguity: float = 0.0
    position_rms_km: float = 0.0
    continuity: float = 0.0
    spurious_tracks: int = 0
    associations: int = 0
    per_object_tracks: dict[str, set[str]] = field(default_factory=dict)


def associate(
    truth: Iterable[Sample],
    system: Iterable[Sample],
    gate_km: float = 5.0,
    time_tolerance_s: float = 0.5,
) -> list[tuple[Sample, Sample, float]]:
    """Associate system reports to truth objects, nearest neighbour within a gate.

    Time first, then distance: a system track is only compared against truth
    samples within ``time_tolerance_s``, because comparing positions from
    different instants measures the target's speed, not the system's error.
    That mistake is easy to make and it silently inflates every accuracy
    number you report.

    Greedy nearest neighbour per system sample. A production tool would solve
    the assignment globally, and saying so is worth more than implementing it
    here.
    """
    truth_by_time: dict[float, list[Sample]] = defaultdict(list)
    for t in truth:
        truth_by_time[t.time_s].append(t)
    times = sorted(truth_by_time)

    pairs: list[tuple[Sample, Sample, float]] = []
    for s in system:
        best: tuple[Sample, float] | None = None
        for t_time in times:
            if abs(t_time - s.time_s) > time_tolerance_s:
                continue
            for t in truth_by_time[t_time]:
                distance = haversine_km(t.lat, t.lon, s.lat, s.lon)
                if distance <= gate_km and (best is None or distance < best[1]):
                    best = (t, distance)
        if best is not None:
            pairs.append((best[0], s, best[1]))
    return pairs


def siap_metrics(
    truth: Sequence[Sample],
    system: Sequence[Sample],
    gate_km: float = 5.0,
    time_tolerance_s: float = 0.5,
) -> SiapMetrics:
    """Compute track-to-truth metrics for one scenario run.

    This is the shape of a fusion regression test: run a recorded or synthetic
    scenario through the baseline, compute these, and compare against the
    previous baseline's numbers. A tech refresh that changes infrastructure
    should move none of them. If one moves, that is the finding, and it is
    quantified rather than an argument about whether the picture "looks right".
    """
    metrics = SiapMetrics()
    truth_ids = {t.ident for t in truth}
    metrics.truth_objects = len(truth_ids)

    pairs = associate(truth, system, gate_km, time_tolerance_s)
    metrics.associations = len(pairs)

    tracks_per_object: dict[str, set[str]] = defaultdict(set)
    associated_track_ids: set[str] = set()
    squared_error = 0.0

    for truth_sample, system_sample, distance_km in pairs:
        tracks_per_object[truth_sample.ident].add(system_sample.ident)
        associated_track_ids.add(system_sample.ident)
        squared_error += distance_km ** 2

    metrics.per_object_tracks = {k: set(v) for k, v in tracks_per_object.items()}
    metrics.tracked_objects = len(tracks_per_object)

    if metrics.truth_objects:
        metrics.completeness = metrics.tracked_objects / metrics.truth_objects
        metrics.continuity = (
            sum(1 for ids in tracks_per_object.values() if len(ids) == 1)
            / metrics.truth_objects
        )
    if metrics.tracked_objects:
        metrics.ambiguity = (
            sum(len(ids) for ids in tracks_per_object.values()) / metrics.tracked_objects
        )
    if pairs:
        metrics.position_rms_km = math.sqrt(squared_error / len(pairs))

    metrics.spurious_tracks = len({s.ident for s in system} - associated_track_ids)
    return metrics


def regression_report(
    baseline: SiapMetrics,
    candidate: SiapMetrics,
    tolerances: dict[str, float] | None = None,
) -> list[str]:
    """Compare two runs and report metrics that degraded beyond tolerance.

    Returns a list of human-readable regressions, empty when the candidate is
    acceptable. Written to return findings rather than to assert, so it can be
    used both from a test and from a report generator after a lab event.

    The tolerances are the interesting part in practice: they are a
    conversation with systems engineering and the customer, not a number a
    developer picks.
    """
    limits = {
        "completeness": 0.01,        # may not drop by more than 1 percentage point
        "continuity": 0.01,
        "ambiguity": 0.05,           # may not rise
        "position_rms_km": 0.10,     # may not rise
        "spurious_tracks": 0,        # may not rise at all
    }
    if tolerances:
        limits.update(tolerances)

    findings: list[str] = []
    # Higher is better.
    for name in ("completeness", "continuity"):
        drop = getattr(baseline, name) - getattr(candidate, name)
        if drop > limits[name]:
            findings.append(
                f"{name} dropped {drop:.3f} "
                f"({getattr(baseline, name):.3f} -> {getattr(candidate, name):.3f})"
            )
    # Lower is better.
    for name in ("ambiguity", "position_rms_km", "spurious_tracks"):
        rise = getattr(candidate, name) - getattr(baseline, name)
        if rise > limits[name]:
            findings.append(
                f"{name} rose {rise:.3f} "
                f"({getattr(baseline, name):.3f} -> {getattr(candidate, name):.3f})"
            )
    return findings
