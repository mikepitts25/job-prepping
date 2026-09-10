# 2. Track data, standards and fusion

This lesson is domain fluency. You will not be tested on it as an engineer, and
that is exactly why it is worth an hour: almost no candidate for a software
sustainment role can hold a conversation about the data the system actually
moves. Being able to is the cheapest differentiator available to you.

Everything here is from public sources, listed at the end. **The specific
implementation on EADGE-T is not public**, and neither are the details of any
program you have worked on. Talk about the domain in public terms and let them
tell you how their system does it.

## 1. Detection, plot, track

The vocabulary is precise and people notice when you use it correctly.

- **Detection / hit / return.** Raw energy above threshold in a radar's signal
  processing.
- **Plot / measurement / target report.** A processed detection with an
  estimated position, usually range, azimuth and sometimes elevation, plus a
  timestamp and quality information. One scan produces many plots, including
  clutter and false alarms.
- **Track.** The system's running estimate of one real object's state over
  time, built from many plots. A track has an identity, a state vector, an
  uncertainty, a history and a lifecycle.
- **Air picture.** The set of tracks the system currently believes in.
- **Recognized Air Picture (RAP)** adds identification and is the operational
  product a battle manager works from.
- **Single Integrated Air Picture (SIAP)** is the goal state: every
  participating site sees the same object as the same track with the same
  number and the same identity.

The distinction that matters most: **a plot is an observation, a track is a
belief.** Everything hard in this domain lives in the gap between the two.

## 2. The processing chain

```
 radar / sensor
      |  detections
      v
 [ plot extraction ]         thresholding, centroiding, clutter rejection
      |  plots (measurements)
      v
 [ alignment ]               time, coordinate frame, units, sensor bias
      |
      v
 [ gating & association ]    which plot belongs to which existing track?
      |
      v
 [ filtering / estimation ]  Kalman, IMM: update the state and covariance
      |
      v
 [ track management ]        initiate, confirm, coast, drop, split, merge
      |
      v
 [ multi-sensor fusion ]     one object seen by three radars is ONE track
      |
      v
 [ identification ]          IFF, flight plans, ADS-B, ROE, operator input
      |
      v
 [ dissemination ]           Link 16 / Link 11 / national formats / displays
```

You will most likely work on the boxes at the top and bottom, not the middle.
The estimation core of a fielded system is stable, verified code that nobody
touches casually. The adapters, the alignment, the dissemination and the test
harness around all of it are where sustainment and tech-refresh work lands.
Saying that shows you understand where a new engineer is actually useful.

### Gating and association

**Gating** is the cheap filter: given a track's predicted position and its
uncertainty, define a region and consider only plots inside it. **Association**
then decides which plot updates which track.

Approaches, in increasing sophistication, and you only need to name them:

- **Nearest neighbour**, and **global nearest neighbour** which solves the
  assignment across all tracks at once rather than greedily.
- **Probabilistic data association (PDA / JPDA)**, which weights several
  candidate plots rather than committing to one.
- **Multiple hypothesis tracking (MHT)**, which defers the decision by keeping
  competing hypotheses alive until evidence resolves them.

The failure modes have names and they are what operators complain about:
**track seduction** (a track latches onto the wrong object, often a crossing
one), **track swap**, **track break** (one object becomes two tracks over
time), and **ghost tracks** (a track with no real object behind it, classically
from false intersections between passive bearing-only sensors).

### Filtering

The **state vector** is typically position and velocity, sometimes with
acceleration, and the filter maintains a **covariance** describing how much it
trusts each component. A Kalman filter predicts forward, then corrects with the
measurement, weighting the two by their relative uncertainty.

A single Kalman filter tuned for straight-and-level flight lags badly through a
hard turn. The standard answer is an **Interacting Multiple Model (IMM)**
filter: run several motion models in parallel, one for constant velocity, one
for a turn, one for acceleration, and blend them by how well each currently
explains the data. Naming IMM and saying why it exists is more than enough
depth for a software role.

### Track lifecycle

- **Initiation.** A plot that matched nothing starts a tentative track.
- **Confirmation.** A rule like M detections in N scans promotes it. Too eager
  and the picture fills with false tracks; too strict and real targets appear
  late. That tuning knob is an operational decision, not a software one.
- **Coasting.** No update this scan, so predict forward and grow the
  uncertainty.
- **Deletion / drop.** After enough missed updates.

Every one of these has a threshold in a configuration file somewhere, and a
tech refresh that changes timing or ordering can move behavior without changing
a line of the algorithm. That sentence is a very good thing to say in an
interview for this job.

## 3. Multi-sensor fusion

Three architectures, worth being able to compare:

| Architecture | How | Trade |
| --- | --- | --- |
| **Centralized (measurement-level)** | Every sensor's plots go to one tracker | Best accuracy; highest bandwidth; single point of failure |
| **Distributed (track-level)** | Each sensor tracks locally, tracks are fused | Lower bandwidth; correlated errors are hard; the usual real answer |
| **Hybrid** | Plots locally where the link allows, tracks elsewhere | What large fielded systems actually do |

**Track-to-track association** is the distributed version of the association
problem, and it has an extra difficulty: two local tracks of the same object
share errors, because they may both have used the same sensor earlier, so you
cannot treat their estimates as independent evidence.

### Registration and gridlock

Two radars will disagree about where the same aircraft is because of position
survey error, azimuth misalignment, range bias and timing offset. Uncorrected,
one object becomes two tracks a few hundred metres apart, and the system
happily reports a two-ship formation that does not exist.

Correcting this is **sensor registration**, historically called **gridlock**.
It estimates each sensor's biases, often against a commonly seen reference, and
applies the correction before association. It is a persistent operational
problem in multi-site air defense, and mentioning it by name is a strong domain
signal.

### Correlation, decorrelation and dual designation

When two participants on a data link are reporting what is actually the same
object under two different track numbers, that is **dual designation**. The
network has procedures to correlate them into one, and to **decorrelate** when
the correlation was wrong. **Reporting responsibility (R2)** decides which
participant is the authoritative reporter for a given track, so that the
picture has one owner rather than several arguing.

## 4. The standards, publicly documented

This is the table worth skimming twice. You do not need depth in any of these.
You need to not be lost when one is named.

### Tactical data links

| Standard | Also known as | What it is |
| --- | --- | --- |
| **MIL-STD-6016 / STANAG 5516** | Link 16, TADIL-J | The primary tactical data link. Fixed-format binary **J-series** messages over a TDMA network |
| **MIL-STD-6011 / STANAG 5511** | Link 11, TADIL-A | Older HF/UHF link, M-series messages, still widely fielded |
| **STANAG 5522** | Link 22 | Successor to Link 11, layered architecture, F-series messages |
| **MIL-STD-3011 / STANAG 5518** | JREAP | Joint Range Extension Application Protocol: carries Link 16 J-series over other bearers such as IP or satellite, beyond line of sight |
| **MIL-STD-6017** | VMF | Variable Message Format, used more for ground forces |
| **OTH-Gold** | | Character-oriented over-the-horizon reporting format, legacy but persistent |

**Link 16 details** worth knowing, all publicly documented:

- Messages are grouped in **J-series** families by function: J2 for precise
  participant location and identification (**PPLI**), J3 for surveillance
  including air, surface and subsurface tracks, J7 for information management,
  J9 for weapons coordination, J12 for mission tasking, J13 for platform
  status, J28 for free text.
- Each message is a **fixed bit layout**. There are no field tags, no length
  prefixes and no self-description. The bits mean nothing without the field
  map, which lives in the standard and therefore in your encoder and decoder as
  code. That single fact drives an enormous amount of the software difficulty:
  every version change is a coordinated change on both ends.
- **Track numbers** are the shared identity of an object across the network.
  **Track quality**, an integer scale, tells receivers how much to trust a
  reported position, and is used to arbitrate when two reporters disagree.
- The network is **TDMA**: participants transmit in assigned time slots, so
  capacity is allocated in advance rather than negotiated on demand. Bandwidth
  is a hard, planned budget, not an elastic resource. This is why data
  reduction, below, is a design concern rather than an optimization.

### Sensor and surveillance data

| Standard | What it is |
| --- | --- |
| **ASTERIX** (EUROCONTROL) | The dominant civil and widely used military format for surveillance data exchange, organized into numbered **categories** |
| ASTERIX **CAT 048** | Monoradar target reports: plots from one radar, primary, secondary, monopulse or Mode S |
| ASTERIX **CAT 034** | Monoradar service messages: north marker, sector crossing, status |
| ASTERIX **CAT 062** | **System track data**: the fused, multi-sensor output. The processed picture, not the raw plots |
| ASTERIX **CAT 063** | Sensor status messages for a surveillance data processing system |
| ASTERIX **CAT 021** | ADS-B reports |
| ASTERIX **CAT 240** | Radar video |
| **STANAG 4607** | GMTI, ground moving target indicator data |
| **Mode S / ADS-B** | Cooperative identification and position reporting from aircraft transponders |
| **IFF Modes 1, 2, 3/A, C, 4, 5, S** | Identification friend or foe interrogation and reply |

The **CAT 048 versus CAT 062 distinction is the single most useful thing in
this table**: CAT 048 is what one radar saw, CAT 062 is what the system
believes after fusion. If you can say that sentence, you have demonstrated that
you understand the difference between a plot and a track in a concrete,
standards-anchored way.

ASTERIX's structure is also a good software talking point: records are built
from a **field specification (FSPEC)** bitmask that says which data items are
present, followed by those items packed in a fixed order. It is compact and
self-describing only to the extent that both ends share the same category
specification and edition. Same versioning problem as Link 16, different
shape.

### Symbology and presentation

| Standard | What it is |
| --- | --- |
| **MIL-STD-2525** | Joint military symbology: how a track is drawn, its affiliation, battle dimension and status |
| **APP-6** | The NATO equivalent |

Worth one sentence because operator display work is real software work, and
because affiliation (friend, hostile, neutral, unknown, assumed friend,
suspect, pending) is data, not decoration.

### Middleware and interfaces

**DDS** (Data Distribution Service, with RTPS as its wire protocol) is the
publish/subscribe middleware standard common in this domain, with quality of
service policies for reliability, durability, deadline and latency budget.
Older systems often used CORBA. Some use proprietary buses or plain multicast.
See [lesson 13](architecture.html).

## 5. Coordinate frames, time and units

This is where the real defects are, and it is excellent interview material
because it is concrete and universally true.

**Coordinate frames.**

- **Geodetic**, latitude, longitude and height above the ellipsoid, on a datum,
  normally **WGS84**.
- **ECEF**, earth-centred earth-fixed Cartesian.
- **ENU / NED**, a local tangent plane at a site, east-north-up or
  north-east-down.
- **Radar-local**, range, azimuth and elevation from the antenna.
- **MGRS / UTM** grids for ground reference.

Conversions between these are where sign errors, hemisphere errors and
ellipsoid-versus-sphere approximations hide. **Height is the classic one**:
height above the WGS84 ellipsoid, height above mean sea level (the geoid) and
barometric pressure altitude are three different numbers for the same aircraft,
differing by tens of metres, and mixing them in a fusion path produces
altitude disagreements that look like a tracking bug.

**Time.**

- UTC has leap seconds; **GPS time and TAI do not**, and the offsets differ.
- Fielded systems synchronize to a common source, and multi-site correlation
  depends on that. Clock skew between sites shows up as position error after
  extrapolation, because a track's position is time-tagged and consumers
  extrapolate it forward.
- Use monotonic clocks for durations. Wall clock can step backwards on a
  correction. See [lesson 11](testing-ci.html).
- Know the difference between **time of measurement** and **time of report**.
  Conflating them is a real and subtle defect class.

**Units and encodings.** Feet versus metres. Knots versus metres per second.
Degrees versus radians versus **BAMs** (binary angular measurement, where a
full circle is the range of the integer type, which is elegant and endlessly
confusing). Big-endian on the wire versus little-endian on the host. Signed
two's complement in an odd bit width. Semicircles. Scaled integers with an
implied least-significant-bit value.

**A very good answer to "what defects do you expect in this domain?"** is:
units and frames at interface boundaries, time-tag handling, and message
version mismatch. Those three account for a large share of real integration
defects, and naming them shows you have thought about the system rather than
the code.

## 6. Data reduction

The term means two different things in this world. Know both, and ask which one
is meant if someone uses it ambiguously. Asking is itself a good signal.

### Meaning one: reducing data in the live system

A radar can produce vastly more plots per second than a tactical data link can
carry or an operator can use. Because the link budget is planned and fixed,
reduction is a design constraint rather than an optimization. Techniques, all
publicly discussed in the surveillance literature:

- **Clutter rejection and CFAR thresholding** in the sensor, before anything
  reaches the network.
- **Plot thinning and decimation**: report every Nth scan, or only on
  significant change.
- **Area, altitude and speed filtering**: only report what is operationally
  relevant to a given consumer.
- **Track-level rather than plot-level reporting**: send the belief, not every
  observation. A track update is a fraction of the bandwidth of the plots
  behind it.
- **Reporting responsibility**: only the owning participant reports a given
  track, so the same object is not broadcast by five sites.
- **Quality gating**: suppress tracks below a track quality threshold.
- **Update rate management**: report a fast-moving or high-interest track more
  often than a slow one.

The trade to be able to state: **every reduction technique buys bandwidth and
sells information.** Thinning by change detection saves enormous capacity and
delays the detection of a manoeuvre. That is an operational decision that
software implements, not one software gets to make.

### Meaning two: data reduction and analysis after a test

In test and evaluation, **data reduction** is turning raw recorded data from a
lab run or a live event into a form analysts can draw conclusions from. This is
the meaning most relevant to your day job on a tech refresh, and it maps
directly onto what the job posting calls automated test capability.

The workflow:

1. **Record everything** during the run, with time tags: sensor inputs, link
   traffic, internal state, operator actions.
2. **Establish truth**, from GPS-instrumented participants, a simulation
   scenario definition, or a reference tracker.
3. **Reduce**: parse the recordings, align them onto one timeline and one
   coordinate frame, and associate system tracks to truth objects.
4. **Compute metrics** against truth.
5. **Compare against a baseline** to show what a change did.

The public **SIAP measures of performance** are the standard vocabulary for
step four, and they are worth memorizing because they are what a customer's
acceptance criteria tend to be written in:

| Metric | Question it answers |
| --- | --- |
| **Completeness** | Of the real objects, what fraction are tracked at all? |
| **Ambiguity** | How many tracks does the system hold on one real object? Ideally one |
| **Accuracy** | How close is the track's position and velocity to truth? |
| **Continuity** | Does the object keep the same track number, or does it get renumbered? |
| **Timeliness** | How current is the picture at the consumer? |
| **Commonality** | Do all participants hold the same track for the same object? |

Why this matters for your interview: **these metrics are the automated
regression test for a fusion system.** You cannot unit-test "the air picture is
still correct," but you can replay a recorded or synthetic scenario through the
new baseline, compute completeness, ambiguity, accuracy and continuity against
truth, and assert that they have not regressed against the previous baseline.
That is a golden-file test with domain-specific metrics instead of a byte
comparison, and proposing it is one of the strongest technical contributions
you could offer in this interview.

There is runnable code for exactly this in the
[practice repo](../practice/README.html): `tracks.py` implements
association-to-truth plus completeness, ambiguity, accuracy and continuity, with
tests.

## 7. Parsing fixed-bit formats: the code you might actually write

The single most likely piece of domain code in this role is a decoder for a
packed binary message, because that is what adapters are. Here is the shape of
it, in Python.

```python
def extract_bits(buffer: bytes, offset: int, length: int) -> int:
    """Read `length` bits starting at bit `offset`, most significant first.

    Bit ordering is the first thing to confirm against the specification and
    the first thing people get wrong. Ask which convention the document uses
    before writing a line: MSB-first within a byte is common on the wire, and
    field numbering in a standard may start at 1, not 0.
    """
    if offset < 0 or length <= 0 or (offset + length) > len(buffer) * 8:
        raise ValueError(f"field [{offset}, {offset + length}) outside buffer")
    value = 0
    for i in range(offset, offset + length):
        byte = buffer[i // 8]
        bit = (byte >> (7 - (i % 8))) & 1
        value = (value << 1) | bit
    return value


def to_signed(value: int, bits: int) -> int:
    """Interpret an unsigned field as two's complement."""
    sign_bit = 1 << (bits - 1)
    return value - (1 << bits) if value & sign_bit else value


def decode_position(raw: bytes) -> dict:
    """A representative packed record: scaled integers, not floats.

    Real formats send angles and distances as scaled integers with an implied
    least-significant-bit value, because floats waste bits on a fixed-bandwidth
    link. The LSB value comes from the specification. Getting it wrong scales
    every output by a constant, which is the kind of bug that looks like a
    tracking problem and is not.
    """
    LAT_LSB_DEG = 180.0 / (1 << 23)     # example scaling only
    ALT_LSB_M = 3.28084                  # example: altitude reported in feet

    latitude = to_signed(extract_bits(raw, 0, 24), 24) * LAT_LSB_DEG
    longitude = to_signed(extract_bits(raw, 24, 25), 25) * LAT_LSB_DEG
    altitude_m = extract_bits(raw, 49, 13) * ALT_LSB_M
    track_number = extract_bits(raw, 62, 15)
    quality = extract_bits(raw, 77, 4)

    return {
        "latitude_deg": latitude,
        "longitude_deg": longitude,
        "altitude_m": altitude_m,
        "track_number": track_number,
        "track_quality": quality,
    }
```

Things to say while writing something like this, each of which is a real
lesson learned in this domain:

- "I want the bit ordering and the field numbering base confirmed against the
  specification before I trust any of this."
- "The scaling factors belong in one table generated from or checked against
  the spec, not scattered as literals. When the edition changes, I want one
  place to update and a test that fails if I miss one."
- "I would build the decoder against recorded real traffic as well as
  synthetic vectors, because real traffic contains the fields nobody documented
  and the values nobody expected."
- "Malformed input must not throw out of the ingest loop. Count it, log a
  sample, and keep going. One bad message must not cost the air picture."
- "I would generate the field map from the specification rather than hand-code
  it if the format is large enough to justify it, because hand-transcribing a
  few hundred fields is where transcription errors come from."

## 8. What to say, and what not to say

**Say:**

- "I understand the difference between a plot and a track, and where in the
  chain most of the software risk is."
- "The problems I would expect are at the interfaces: coordinate frames, time
  tags, units, and message version mismatch."
- "For regression, I would want scenario replay with track-to-truth metrics
  rather than only unit tests, because that is the only way to show the mission
  behavior is unchanged after an infrastructure change."
- "I know the standards landscape at a vocabulary level. I have not
  implemented [Link 16 / ASTERIX / whichever is true for you], and I would
  expect a ramp on the specific formats you use."

**Do not:**

- Claim implementation experience with a standard you have only read about. The
  second follow-up question will find it.
- Discuss anything specific about a program you have worked on beyond what is
  publicly releasable. For a foreign military sales program, export control and
  foreign disclosure rules apply on top of classification, and the interviewer
  will respect "I can talk about that at an unclassified level" far more than
  the alternative. See [lesson 14](cyber.html).
- Speculate about EADGE-T's internal design. Ask instead. "Is your fusion
  centralized or track-level?" is a much better use of the same thirty seconds
  than a guess.

## 9. Questions to ask them about the data

These are excellent interview questions because only someone who understands
the domain would think to ask, and every answer tells you something real about
the job.

- Is fusion centralized at the measurement level, or track-level across sites?
- Which data links and surveillance formats are in the baseline, and are any of
  them being changed as part of the refresh?
- How is sensor registration handled, and is it a recurring operational issue?
- What does the regression scenario set look like? Recorded live data,
  simulated scenarios, or both?
- Are track-to-truth metrics computed automatically, and are they in the
  pipeline or run by hand after a lab event?
- What is the turnaround from a code change to a metrics report against a
  scenario?

That last question is the one I would ask. The answer tells you the true cycle
time of the whole program, and it sets up everything you would want to improve.

## Sources

All of the above is drawn from public documentation and open literature:

- [EUROCONTROL ASTERIX specifications](https://www.eurocontrol.int/publication/cat062-eurocontrol-specification-surveillance-data-exchange-asterix-part-9-category-062), including [Category 048, monoradar target reports](https://www.eurocontrol.int/publication/cat048-eurocontrol-specification-surveillance-data-exchange-asterix-part4)
- [A comparison of ASTERIX Category 048 and Category 062 (Cambridge Pixel)](https://cambridgepixel.com/insights/a-comparison-of-asterix-category-048-category-062/)
- [Link 16 (Wikipedia)](https://en.wikipedia.org/wiki/Link_16) and [TADIL-J](https://en.wikipedia.org/wiki/TADIL-J)
- [MIL-STD-6011 / Link 11 (Wikipedia)](https://en.wikipedia.org/wiki/MIL-STD-6011) and [Link 22](https://en.wikipedia.org/wiki/Link_22)
- [MIL-STD-3011 / STANAG 5518, JREAP](https://standards.globalspec.com/std/878962/mil-std-3011)
- [SISO-STD-002-2021, Standard for Link 16 Simulation](https://cdn.ymaws.com/www.sisostandards.org/resource/resmgr/standards_products/siso-std-002-2021_link_16.pdf)
- [Single Integrated Air Picture (Wikipedia)](https://en.wikipedia.org/wiki/Single_Integrated_Air_Picture) and [SIAP Integrated Assessment Plan (DTIC ADA405128)](https://archive.org/stream/DTIC_ADA405128/DTIC_ADA405128_djvu.txt)
- Open literature on sensor registration and bias estimation, for example [A practical bias estimation algorithm for multisensor-multitarget tracking](https://arxiv.org/pdf/1603.03449)
