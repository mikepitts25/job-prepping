# 7. The four-hour API sprint

"Familiarity with Docker, **REST APIs, or SOAP**" is a basic qualification on
your requisition. This sprint covers the REST half properly and gives you
enough SOAP to talk about it honestly.

You build **one thing**: a track API with full validation and correct status
codes, its test suite, and a client that survives a flaky server. That last
part is what separates someone who has called an API from someone who has run
one in production.

[Lesson 13](apis.html) is the reference. This is the sprint.

## The rules

1. **Type everything. Never paste.**
2. **Exercise every endpoint** after you write it. `curl` or the test client.
3. **Write the test before you move on.** In this sprint tests are not an
   afterthought; they are how you check your work.
4. **Break things on purpose** where I say so.
5. **Respect the clock.**

## What I am cutting, and why

| Cut | Why |
| --- | --- |
| Databases | Orthogonal. An in-memory dict teaches the same API design. |
| Authentication implementation | You need the vocabulary, not an OAuth flow. |
| GraphQL | Not on your req. |
| Async frameworks (FastAPI, asyncio) | Flask is named on the req; the design ideas transfer. |
| Deployment, load balancers | Covered in [lesson 20](containers.html). |
| Writing a SOAP service | You will consume and maintain one, not write one. |

## Setup: five minutes, before the clock

```bash
mkdir apisprint && cd apisprint
python3 -m venv .venv
source .venv/bin/activate
pip install flask pytest
```

Start the clock.

---

## Hour 1: HTTP and your first endpoints

### 0:00 to 0:20 — What an API actually is

Two programs need to talk. They agree on five things, and if you can name these
you can specify any API:

1. **A transport.** Usually HTTP over TCP.
2. **An address.** A URL identifying the thing.
3. **A message format.** JSON, XML, or packed binary.
4. **A vocabulary.** What operations exist and what they take.
5. **An error convention.** How failure is signalled.

An HTTP request:

```
GET /api/v1/tracks?affiliation=hostile HTTP/1.1
Host: eadge.internal
Accept: application/json
Authorization: Bearer <token>
```

A **method**, a **path**, **query parameters**, **headers**, sometimes a
**body**. The response has a **status code**, headers and usually a body.

**The methods, and the property that matters:**

| Method | Purpose | Idempotent? |
| --- | --- | --- |
| `GET` | Retrieve. Must change nothing | Yes |
| `POST` | Create, or a general action | **No** |
| `PUT` | Replace entirely | Yes |
| `PATCH` | Modify part | Usually not |
| `DELETE` | Remove | Yes |

**Idempotent** means doing it twice has the same effect as doing it once. This
is not trivia. It decides **what a client may safely retry**, which is the
whole of hour four. A dropped response to a `PUT` can be repeated without
thought. A dropped response to a `POST` may have already created the thing, so
repeating it could create a second one.

**The status codes to know cold:**

| Code | Meaning |
| --- | --- |
| 200 | OK, with a body |
| 201 | Created. `Location` header says where |
| 204 | Success, nothing to return |
| 400 | The client sent something malformed |
| 401 | Not authenticated. "Who are you?" |
| 403 | Authenticated but not permitted. "I know who you are, and no" |
| 404 | No such resource |
| 409 | Conflicts with current state |
| 429 | Rate limited |
| 500 | The server broke |
| 503 | Temporarily unavailable |

**The 4xx versus 5xx split is the one that matters operationally: 4xx means the
client is wrong, 5xx means you are.** A server returning 200 with an error
inside the body is a genuine design defect, because every load balancer, every
monitor and every retry policy reads the status code.

### 0:20 to 0:50 — Your first endpoints

Create `api.py`:

```python
"""A track API, built in the four-hour sprint."""

from flask import Flask, jsonify, request

app = Flask(__name__)

TRACKS = {
    "T-001": {"trackId": "T-001", "affiliation": "hostile", "altitudeFt": 32000, "confidence": 0.92},
    "T-002": {"trackId": "T-002", "affiliation": "friend", "altitudeFt": 12000, "confidence": 0.71},
    "T-003": {"trackId": "T-003", "affiliation": "unknown", "altitudeFt": 8000, "confidence": 0.44},
}

AFFILIATIONS = {"friend", "hostile", "neutral", "unknown"}


def error(message, status, **extra):
    """One error shape for the whole API, so clients can rely on it."""
    return jsonify({"error": message, **extra}), status


@app.get("/api/v1/tracks/<track_id>")
def get_track(track_id):
    track = TRACKS.get(track_id)
    if track is None:
        return error("not found", 404, trackId=track_id)
    return jsonify(track)


@app.get("/health/live")
def live():
    return jsonify({"status": "alive"})


@app.get("/health/ready")
def ready():
    return jsonify({"status": "ready", "tracks": len(TRACKS)})
```

```bash
flask --app api run
# in another terminal:
curl -i localhost:5000/api/v1/tracks/T-001
curl -i localhost:5000/api/v1/tracks/NOPE
```

What is new:

**`@app.get("/path")`** is a decorator registering the function as that route's
handler. Same concept as a Python decorator anywhere.

**`<track_id>`** in the path is a parameter, handed to the function.

**Returning a tuple** `(body, status)` sets the status code.

**One error shape.** Every failure returns `{"error": ..., ...}`. A client can
then handle errors generically instead of guessing per endpoint. Deciding this
once, early, is a real design decision.

**404 names what was missing.** `{"error": "not found", "trackId": "NOPE"}`
puts the reason in the client's logs. A bare 404 does not.

**Two health endpoints**, and the distinction gets asked: **liveness** says the
process is alive, and failing it means restart me. **Readiness** says it can
serve, and failing it means take me out of rotation but do not restart me.
Confusing them causes restart loops during slow startup. Add both from the
start; adding them later always means a deployment argument.

### 0:50 to 1:00 — Checkpoint

**Do now.** Add `DELETE /api/v1/tracks/<track_id>` returning 204.

```python
@app.delete("/api/v1/tracks/<track_id>")
def delete_track(track_id):
    TRACKS.pop(track_id, None)
    return "", 204
```

Call it twice. **Both return 204.** That is deliberate: `DELETE` is idempotent,
so deleting something already gone is a success, not a 404. The end state the
caller wanted is the end state they got. Being able to defend that choice is a
good interview moment.

**Five minutes off.**

---

## Hour 2: validation and the full resource

### 1:00 to 1:30 — Listing, filtering, paging

```python
@app.get("/api/v1/tracks")
def list_tracks():
    affiliation = request.args.get("affiliation")
    if affiliation is not None and affiliation not in AFFILIATIONS:
        return error("unknown affiliation", 400, affiliation=affiliation)

    try:
        min_confidence = float(request.args.get("min_confidence", 0.0))
    except ValueError:
        return error("min_confidence must be a number", 400)

    limit = request.args.get("limit", type=int, default=50)
    if limit < 1 or limit > 200:
        return error("limit must be between 1 and 200", 400, limit=limit)

    results = [
        t for t in TRACKS.values()
        if (affiliation is None or t["affiliation"] == affiliation)
        and t["confidence"] >= min_confidence
    ]
    results.sort(key=lambda t: t["trackId"])
    return jsonify({"tracks": results[:limit], "total": len(results)})
```

Four decisions, all defensible in an interview:

**Every query parameter is validated.** An unknown affiliation is a 400 with
the offending value echoed, not a silent empty list. Silently returning nothing
for a typo is the kind of behaviour that costs an operator an hour.

**`limit` is bounded.** Without a cap, one client eventually asks for
everything and takes the server down. **Any collection that can grow must be
paged.**

**The result is sorted.** Unsorted output means the same request can return a
different order each time, which makes paging incoherent and tests
non-deterministic.

**The response is an object, not a bare array**: `{"tracks": [...], "total": N}`.
That leaves room to add fields later without breaking clients, and it carries
the total separately from the page. Returning a bare array is a decision you
cannot undo.

### 1:30 to 1:55 — Creating, and validating a body

```python
@app.post("/api/v1/tracks")
def create_track():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error("body must be a JSON object", 400)

    track_id = body.get("trackId")
    if not isinstance(track_id, str) or not track_id.strip():
        return error("trackId must be a non-empty string", 400)
    if track_id in TRACKS:
        return error("already exists", 409, trackId=track_id)

    affiliation = body.get("affiliation")
    if affiliation not in AFFILIATIONS:
        return error("affiliation must be one of " + ", ".join(sorted(AFFILIATIONS)), 400)

    confidence = body.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0.0 <= confidence <= 1.0:
        return error("confidence must be between 0 and 1", 400)

    track = {
        "trackId": track_id.strip(),
        "affiliation": affiliation,
        "altitudeFt": body.get("altitudeFt", 0),
        "confidence": float(confidence),
    }
    TRACKS[track["trackId"]] = track
    return jsonify(track), 201, {"Location": f"/api/v1/tracks/{track['trackId']}"}
```

**Validate everything that crosses the boundary.** Type, presence, range,
membership. A request body is untrusted input, exactly like a line from a log
file. This is the same discipline as `parseTrack` in
[lesson 6](frontend-sprint.html) and `parse_line` in
[lesson 4](python-sprint.html), and noticing that it is the same discipline is
the point.

**201 plus a `Location` header** is the correct answer to a successful create.
The client learns where the new thing lives without guessing the URL.

**409 for a duplicate**, not 400. The request was well-formed; it conflicts
with current state. Using the right code lets a client tell "you sent rubbish"
from "someone beat you to it."

**`get_json(silent=True)`** returns `None` instead of raising when the body is
not JSON, so you return a clean 400 rather than a 500. **A malformed request
must never produce a 5xx**, because 5xx means you broke, and that misdirects
whoever is on call.

### 1:55 to 2:00 — Break it

Send each of these and confirm the status code:

```bash
curl -i -X POST localhost:5000/api/v1/tracks -H 'Content-Type: application/json' \
  -d '{"trackId":"T-009","affiliation":"hostile","confidence":0.5}'      # 201
curl -i -X POST localhost:5000/api/v1/tracks -H 'Content-Type: application/json' \
  -d '{"trackId":"T-009","affiliation":"hostile","confidence":0.5}'      # 409
curl -i -X POST localhost:5000/api/v1/tracks -H 'Content-Type: application/json' \
  -d '{"trackId":"X","affiliation":"banana","confidence":0.5}'           # 400
curl -i -X POST localhost:5000/api/v1/tracks -H 'Content-Type: application/json' \
  -d 'not json at all'                                                    # 400, not 500
```

That last one is the one people get wrong. **Five minutes off.**

---

## Hour 3: testing the API

### 2:00 to 2:35 — The test suite

```python
import pytest

from api import TRACKS, app


@pytest.fixture
def client():
    """A test client, with the data reset so tests do not affect each other."""
    original = dict(TRACKS)
    yield app.test_client()
    TRACKS.clear()
    TRACKS.update(original)


def test_lists_all_tracks(client):
    body = client.get("/api/v1/tracks").get_json()
    assert body["total"] == 3
    assert [t["trackId"] for t in body["tracks"]] == ["T-001", "T-002", "T-003"]


def test_rejects_an_unknown_affiliation_with_400(client):
    response = client.get("/api/v1/tracks?affiliation=banana")
    assert response.status_code == 400
    assert response.get_json()["affiliation"] == "banana"


@pytest.mark.parametrize("limit", [0, -1, 201, 9999])
def test_rejects_an_out_of_range_limit(client, limit):
    assert client.get(f"/api/v1/tracks?limit={limit}").status_code == 400


def test_limit_caps_the_page_but_total_reports_everything(client):
    body = client.get("/api/v1/tracks?limit=1").get_json()
    assert len(body["tracks"]) == 1
    assert body["total"] == 3


def test_unknown_track_is_404_with_a_reason(client):
    response = client.get("/api/v1/tracks/NOPE")
    assert response.status_code == 404
    assert response.get_json()["trackId"] == "NOPE"


def test_creating_returns_201_and_a_location(client):
    response = client.post("/api/v1/tracks", json={
        "trackId": "T-009", "affiliation": "hostile", "confidence": 0.5,
    })
    assert response.status_code == 201
    assert response.headers["Location"] == "/api/v1/tracks/T-009"
    assert client.get("/api/v1/tracks/T-009").status_code == 200


def test_creating_a_duplicate_is_409(client):
    payload = {"trackId": "T-001", "affiliation": "hostile", "confidence": 0.5}
    assert client.post("/api/v1/tracks", json=payload).status_code == 409


@pytest.mark.parametrize("payload", [
    {},
    {"trackId": "", "affiliation": "hostile", "confidence": 0.5},
    {"trackId": "X", "affiliation": "banana", "confidence": 0.5},
    {"trackId": "X", "affiliation": "hostile", "confidence": 1.5},
    {"trackId": "X", "affiliation": "hostile", "confidence": "high"},
])
def test_rejects_a_bad_body_with_400(client, payload):
    assert client.post("/api/v1/tracks", json=payload).status_code == 400


def test_delete_is_idempotent(client):
    assert client.delete("/api/v1/tracks/T-001").status_code == 204
    assert client.delete("/api/v1/tracks/T-001").status_code == 204
```

```bash
pytest -q
```

The things to notice:

**`app.test_client()` exercises the whole request path with no server and no
network.** That is what makes API tests fast enough to run on every commit,
which is the entire argument for having them.

**The fixture resets the data.** `TRACKS` is module-level mutable state, so a
test that creates a track would otherwise change what the next test sees. **A
test that only passes when another ran first is worse than no test**, because
it fails mysteriously later. Notice that the need for this fixture is a hint
that global mutable state is awkward; a real service would inject a store.

**Test every status code your API can return**, not just the happy path. The
parametrised bad-body test is six tests from one function.

### 2:35 to 3:00 — What to test, and versioning

The checklist for any endpoint. Recite this in an interview:

- the happy path
- every validation failure, with its status code
- the not-found case
- the conflict case
- an empty collection
- the boundary of every limit, both sides
- a malformed body, proving it gives 400 and not 500

Then the design topic that matters most on this programme:

**Versioning.** Commercial teams change an API and redeploy the clients. **You
cannot.** Your consumers may be other programmes, on other schedules, possibly
other contractors.

- **Version in the path**, `/api/v1/`.
- **Additive changes only** within a version. Adding a field is safe, because a
  well-written client ignores what it does not recognise. Removing a field,
  renaming one, changing a type, or tightening validation are all breaking.
- **Never repurpose a field.** Reusing `status` to mean something new is the
  most expensive kind of "small" change, because it fails silently in the
  consumer.
- **Run versions in parallel**, retire on an agreed date.
- **Changes go through interface control, not a merge request.** The
  coordination lead time with another programme is the real constraint, not the
  code.

If asked "how would you change a message format three other systems depend
on?", that list is the answer and the last line is what makes it senior.

**Five minutes off.**

---

## Hour 4: clients that survive

### 3:00 to 3:35 — Timeouts, retries, backoff, jitter

Writing the server is half the job. Most production incidents involve a client
behaving badly when a server misbehaves.

```python
import random
import time

RETRYABLE_STATUS = {429, 500, 502, 503, 504}
IDEMPOTENT_METHODS = {"GET", "PUT", "DELETE", "HEAD"}


class TransientError(Exception):
    """A failure worth retrying."""


class ApiError(Exception):
    """A failure not worth retrying."""

    def __init__(self, status, message):
        super().__init__(f"{status}: {message}")
        self.status = status


def call(send, method, url, *, attempts=3, base_delay=0.5, timeout=5.0,
         sleep=time.sleep, rand=random.random):
    """Make one call, retrying transient failures.

    ``send`` is injected so tests can supply a fake instead of a network.
    """
    last = None

    for attempt in range(1, attempts + 1):
        try:
            status, body = send(method, url, timeout=timeout)
        except TimeoutError as err:
            last = TransientError(f"timeout: {err}")
        else:
            if status < 400:
                return body
            if status in RETRYABLE_STATUS:
                last = TransientError(f"server returned {status}")
            else:
                raise ApiError(status, body)

        if method.upper() not in IDEMPOTENT_METHODS:
            raise last
        if attempt < attempts:
            delay = base_delay * (2 ** (attempt - 1))
            sleep(delay * (0.5 + rand()))

    raise last
```

Every line of that is a decision worth being able to defend:

**A timeout on every call.** A call with no timeout is a thread that may never
come back. This is the single most common omission in client code, and it turns
one slow dependency into a dead application.

**Retry only transient failures.** 429 and 5xx may succeed next time. A 404 or
a 400 will not: retrying is pure waste and hides the real problem.

**Retry only idempotent methods.** Repeating a `POST` could create a second
resource. This is where the idempotency table from hour one pays off.

**Exponential backoff.** 0.5s, 1s, 2s. Hammering a struggling server makes it
worse.

**Jitter**, the `(0.5 + rand())`. Without it, every client that failed at the
same moment retries at the same moment, and the synchronised wave finishes off
the server that was about to recover. This is the detail that marks out
somebody who has actually run a distributed system.

**A bounded attempt budget.** Infinite retry is a denial-of-service attack on
your own infrastructure.

**`sleep` and `rand` are injected**, so tests run instantly and deterministically.

### 3:35 to 3:50 — Testing the client

```python
def fake_sender(script):
    """Return a send() that yields each scripted outcome in turn."""
    calls = []

    def send(method, url, timeout=None):
        calls.append((method, url, timeout))
        outcome = script[len(calls) - 1]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    send.calls = calls
    return send


def test_retries_a_timeout_then_succeeds():
    send = fake_sender([TimeoutError("no route"), (200, {"ok": True})])
    assert call(send, "GET", "/x", sleep=lambda _: None) == {"ok": True}
    assert len(send.calls) == 2


def test_does_not_retry_a_client_error():
    send = fake_sender([(404, "not found")])
    with pytest.raises(ApiError):
        call(send, "GET", "/x", sleep=lambda _: None)
    assert len(send.calls) == 1, "a 404 will not become a 200; retrying is waste"


def test_does_not_retry_a_post():
    send = fake_sender([(503, "busy"), (200, {"ok": True})])
    with pytest.raises(TransientError):
        call(send, "POST", "/x", sleep=lambda _: None)
    assert len(send.calls) == 1, "repeating a POST could create a second resource"


def test_backoff_grows_and_is_jittered():
    slept = []
    send = fake_sender([(503, "x"), (503, "x"), (200, {})])
    call(send, "GET", "/x", attempts=3, base_delay=1.0,
         sleep=slept.append, rand=lambda: 0.5)
    assert slept == [1.0, 2.0]
```

**This is the highest-value test suite in the sprint.** It proves properties
that are impossible to check by hand: that a POST is not retried, that backoff
grows, that a 404 stops immediately. And it runs in milliseconds because
everything slow is injected.

### 3:50 to 3:57 — SOAP, enough to be honest

You will not write SOAP today. You should be able to discuss it, because
fielded defence systems are full of it.

SOAP is a **specification**, not a style. Every message is an XML envelope:

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Header>...</soap:Header>
  <soap:Body>
    <GetTrack xmlns="urn:eadge:tracks"><TrackId>T-001</TrackId></GetTrack>
  </soap:Body>
</soap:Envelope>
```

Failures come back as a **Fault** inside the body, not as an HTTP status.
**WSDL** is the machine-readable contract; point a tool at it and it generates
client code. That generated, strongly-typed contract is genuinely SOAP's
strength and why it persists in regulated environments.

**The one thing you must know if you touch XML:** disable external entities and
DTDs in the parser. **XXE** lets a document read local files or fetch URLs;
**billion laughs** is an expansion bomb that exhausts memory from a tiny input.
In Python use `defusedxml`. Legacy message parsing is exactly where this lives
on a tech refresh, and raising it unprompted lands very well with a cyber
engineer.

**The honest summary:** SOAP is verbose and out of fashion, but it brought a
formal contract and enterprise standards that REST leaves you to assemble. You
meet it because it is already there and its consumers are not yours to change.

### 3:57 to 4:00 — Self-test

From memory:

1. Which methods are idempotent, and what that decides.
2. The difference between 400, 401, 403, 404 and 409.
3. Why a malformed body must give 400 and not 500.
4. Why `limit` must be bounded.
5. The four rules of versioning an API other programmes consume.
6. Four things a resilient client does, and why jitter matters.

## What you can honestly claim

**Say:** you design and build REST APIs with proper status codes and full input
validation, you test every response path without a network, you understand
versioning under interface control, and you write clients with timeouts,
bounded retries, backoff and jitter.

**Do not claim** SOAP implementation experience. Say you understand the model,
WSDL contracts and the XML security risks, and that you would expect a ramp on
the specific interfaces.

## If you get another four hours

1. **[Lesson 13](apis.html)**, especially gRPC and the cross-cutting concerns.
2. **Add a circuit breaker** to the client: after N consecutive failures, stop
   calling for a cool-down. Test it.
3. **Write the OpenAPI document** for your API, then generate a client from it.
4. **Add `PUT`** and write the test proving it is idempotent where `POST` is
   not.
5. **Rebuild the API from an empty file** without looking.
