# 8. APIs: REST, SOAP, gRPC and Flask

Your requisition lists "familiarity with **Docker, REST APIs, or SOAP**" as a
basic qualification, and **gRPC** and **Flask** under desired skills. This
lesson covers all of it.

The framing that matters: an API is the **contract** between two pieces of
software. On a programme that integrates separately procured systems, the
contract is the product. The code behind it can be rewritten; the contract
cannot, because other people's systems depend on it.

## 1. What an API is, from zero

Two programs need to talk. They may be on different machines, written in
different languages, built by different companies. They agree on:

- **A transport.** Usually HTTP over TCP.
- **An address.** A URL identifying what you are talking to.
- **A message format.** JSON, XML, or a packed binary form.
- **A vocabulary.** Which operations exist, what they take, what they return.
- **An error convention.** How failure is signalled.

Write those five down and you have specified an API. Everything below is a
different set of choices for them.

### HTTP, the thing underneath

```
GET /api/v1/tracks?affiliation=hostile HTTP/1.1
Host: eadge.internal
Accept: application/json
Authorization: Bearer <token>
```

A request has a **method**, a **path**, optional **query parameters**,
**headers**, and sometimes a **body**. The response has a **status code**,
headers, and usually a body.

**Methods**, and the property that matters:

| Method | Purpose | Idempotent? |
| --- | --- | --- |
| `GET` | Retrieve. Must not change anything | Yes |
| `POST` | Create, or a general action | **No** |
| `PUT` | Replace a resource entirely | Yes |
| `PATCH` | Modify part of a resource | Usually not |
| `DELETE` | Remove | Yes |

**Idempotent** means doing it twice has the same effect as doing it once. That
is not trivia: it decides what a client may safely retry. A dropped response to
a `PUT` can be retried without thought. A dropped response to a `POST` might
have created the thing already, so retrying could create a second one. This is
why payment and order APIs use idempotency keys, and it is a very good thing to
raise unprompted.

**Status codes** worth knowing cold:

| Code | Meaning |
| --- | --- |
| 200 OK | Success with a body |
| 201 Created | New resource made; `Location` header says where |
| 202 Accepted | Taken for later processing, not done yet |
| 204 No Content | Success, nothing to return |
| 400 Bad Request | The client sent something malformed |
| 401 Unauthorized | Not authenticated. You are nobody |
| 403 Forbidden | Authenticated but not permitted. You are somebody, but no |
| 404 Not Found | No such resource |
| 409 Conflict | Clashes with current state |
| 422 Unprocessable | Well-formed but semantically invalid |
| 429 Too Many Requests | Rate limited |
| 500 Internal Server Error | The server broke. Your fault, not theirs |
| 503 Service Unavailable | Temporarily down or overloaded |

The 401 versus 403 distinction gets asked. **401 is "who are you?", 403 is "I
know who you are and the answer is no."**

The 4xx versus 5xx split is the one that matters operationally: **4xx means the
client is wrong, 5xx means you are.** A server returning 200 with an error
message inside the body is a genuine design defect, because every piece of
monitoring, every load balancer and every retry policy in the world reads the
status code.

## 2. REST

REST is an architectural style, not a standard. In practice, "a REST API" means
an HTTP API organised around **resources** identified by URLs, using the HTTP
methods for the verbs.

```
GET    /api/v1/tracks                    list them
GET    /api/v1/tracks?affiliation=hostile  filtered
GET    /api/v1/tracks/T-001              one of them
POST   /api/v1/tracks                    create one
PUT    /api/v1/tracks/T-001              replace it
PATCH  /api/v1/tracks/T-001              change part of it
DELETE /api/v1/tracks/T-001              remove it
GET    /api/v1/sensors/RDR-1/tracks      a sub-collection
```

The design conventions:

- **Nouns in paths, verbs as methods.** `/api/v1/tracks` with `DELETE`, never
  `/api/v1/deleteTrack`.
- **Plural collection names.** `/tracks`, not `/track`.
- **Filtering, sorting and paging go in the query string**, not the path.
- **Stateless.** Every request carries what it needs. The server holds no
  session between calls, which is what lets you run several instances behind a
  load balancer.

A JSON body:

```json
{
  "trackId": "T-001",
  "affiliation": "hostile",
  "altitudeFt": 32000,
  "confidence": 0.92,
  "lastSeen": "2026-09-16T12:00:00Z"
}
```

Note the timestamp: **ISO 8601, UTC, with the zone spelled out.** Never send a
naive local time across an interface. On a system with sites in different
countries that is a defect waiting to happen, as in
[lesson 2](track-data.html).

### Versioning, which is the part that matters here

Commercial teams change an API and redeploy the clients. **You cannot.** Your
consumers may be other programmes, on their own schedules, possibly other
contractors.

So:

- **Version explicitly**, usually in the path: `/api/v1/`.
- **Additive changes only** within a version. Adding a field is safe, because a
  well-written client ignores what it does not recognise. Removing a field,
  renaming one, changing a type, or tightening validation are all breaking
  changes.
- **Never repurpose a field.** Reusing `status` to mean something new is the
  most expensive kind of "small" change, because it fails silently in the
  consumer.
- **Run versions in parallel** and retire the old one on an agreed date.
- **Changes go through interface control**, not a merge request. On a programme
  like this the lead time for agreeing a change with another programme is the
  real constraint, not the code.

If you are asked "how would you change a message format three other systems
depend on?", that list is the answer, and the last point is what makes it a
senior answer.

### Pagination

```
GET /api/v1/tracks?limit=100&cursor=eyJpZCI6IlQtMTAwIn0
```

Any collection that can grow must be paged, or one day a client asks for
everything and takes the server down. Cursor-based paging is more robust than
`offset`/`limit` because it does not skip or duplicate rows when the data
changes underneath you.

## 3. SOAP

SOAP is the older, heavier, XML-based approach. It appears in the basic
qualifications because **fielded defence and enterprise systems are full of
it**, and a tech refresh means meeting it.

Where REST is a style, SOAP is a **specification**. Every message is an XML
envelope with a defined structure:

```xml
<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Header>
    <auth:Credentials xmlns:auth="urn:eadge:auth">
      <auth:Token>...</auth:Token>
    </auth:Credentials>
  </soap:Header>
  <soap:Body>
    <GetTrack xmlns="urn:eadge:tracks">
      <TrackId>T-001</TrackId>
    </GetTrack>
  </soap:Body>
</soap:Envelope>
```

A failure comes back as a **Fault**, not an HTTP status:

```xml
<soap:Body>
  <soap:Fault>
    <soap:Code><soap:Value>soap:Sender</soap:Value></soap:Code>
    <soap:Reason><soap:Text>Unknown track id</soap:Text></soap:Reason>
  </soap:Fault>
</soap:Body>
```

**WSDL** (Web Services Description Language) is the machine-readable contract:
an XML document listing every operation, its inputs and outputs and their
types. Point a tool at a WSDL and it generates client code for you. That
code-generated, strongly-typed contract is genuinely SOAP's strength, and the
reason it persists in regulated environments.

| | REST | SOAP |
| --- | --- | --- |
| Style or standard | Style | Specification |
| Format | Usually JSON | XML only |
| Contract | OpenAPI, optional | WSDL, intrinsic |
| Errors | HTTP status codes | SOAP Fault |
| Transport | HTTP | HTTP, but also message queues |
| Weight | Light | Heavy, verbose |
| Built-in standards | No | WS-Security, WS-ReliableMessaging, transactions |
| Where you meet it | New services | Legacy and enterprise integration |

**The honest summary to give:** SOAP is verbose and out of fashion, but it
brought a formal contract and a set of enterprise standards that REST leaves you
to assemble. On a fielded system it is often already there, and replacing a
working SOAP interface that three other programmes depend on is a large
coordination exercise, not a technical one.

### The security warning

If you work with XML, you must know this. Two attacks:

- **XXE**, XML external entity: a document tells the parser to read a local
  file or fetch a URL, exfiltrating data.
- **Billion laughs**, an entity expansion bomb that consumes all available
  memory from a tiny document.

The fix is to disable external entities and DTDs in the parser.

```python
# Python: use a hardened parser rather than the standard library defaults
from defusedxml.ElementTree import fromstring
root = fromstring(untrusted_xml)
```

Legacy message parsing is exactly where this class of vulnerability lives on a
tech refresh. Raising it unprompted lands very well with a cyber engineer on
the panel. See [lesson 17](cyber.html).

## 4. gRPC

gRPC is the modern high-performance option, listed under desired skills.

You define the service and messages in a `.proto` file, and a compiler
generates client and server code in any supported language:

```protobuf
syntax = "proto3";
package eadge.tracks.v1;

message Track {
  string track_id = 1;
  Affiliation affiliation = 2;
  double altitude_ft = 3;
  double confidence = 4;
}

enum Affiliation {
  AFFILIATION_UNSPECIFIED = 0;
  AFFILIATION_FRIEND = 1;
  AFFILIATION_HOSTILE = 2;
}

service TrackService {
  rpc GetTrack(GetTrackRequest) returns (Track);
  rpc StreamTracks(StreamTracksRequest) returns (stream Track);   // server stream
}
```

What it gives you:

- **Binary encoding** (Protocol Buffers), far smaller and faster to parse than
  JSON or XML. On a bandwidth-planned link, that is the point.
- **A generated, strongly typed contract** in every language.
- **Streaming**, in either or both directions, over HTTP/2. A live track feed
  is a server stream, which fits this domain naturally.
- **Schema evolution rules**: those field numbers are the identity. Add new
  numbered fields freely; never reuse a number.

What it costs: it is not human-readable on the wire, browsers cannot call it
directly without a proxy such as gRPC-Web, and it needs a build step.

**Choosing between the three**, which is the interview question:

- **REST** for anything a browser or a human touches, and for broad
  interoperability.
- **gRPC** for high-rate internal service-to-service traffic, especially
  streaming, where you control both ends.
- **SOAP** when the existing interface is SOAP and the consumers are not yours
  to change.

## 5. Flask

Flask is a small Python web framework, named in the desired skills. "Micro"
means it gives you routing and request handling and leaves the rest to you.

Here is a complete, working API. Every response below was produced by running
it.

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

TRACKS = [
    {"trackId": "T-001", "affiliation": "hostile", "altitudeFt": 32000, "confidence": 0.92},
    {"trackId": "T-002", "affiliation": "friend", "altitudeFt": 12000, "confidence": 0.71},
]


@app.get("/api/v1/tracks")
def list_tracks():
    affiliation = request.args.get("affiliation")
    min_confidence = request.args.get("min_confidence", type=float, default=0.0)

    results = [
        t for t in TRACKS
        if (affiliation is None or t["affiliation"] == affiliation)
        and t["confidence"] >= min_confidence
    ]
    return jsonify(results)


@app.get("/api/v1/tracks/<track_id>")
def get_track(track_id):
    for t in TRACKS:
        if t["trackId"] == track_id:
            return jsonify(t)
    return jsonify({"error": "not found", "trackId": track_id}), 404


@app.get("/health/ready")
def ready():
    return jsonify({"status": "ok"})
```

```bash
pip install flask
flask --app app run          # development server on :5000
```

```
GET /api/v1/tracks                    -> 200, 2 tracks
GET /api/v1/tracks?affiliation=hostile -> 200, ['T-001']
GET /api/v1/tracks?min_confidence=0.8  -> 200, ['T-001']
GET /api/v1/tracks/T-001               -> 200
GET /api/v1/tracks/NOPE                -> 404 {'error': 'not found', 'trackId': 'NOPE'}
GET /health/ready                      -> 200
```

Points to make about that code:

**`@app.get("/path")`** is a decorator registering the function as the handler
for that route. Same decorator concept as [lesson 6](python-practice.html).

**`<track_id>`** in the path is a parameter, passed to the function as an
argument.

**`request.args.get(..., type=float, default=0.0)`** reads and converts a query
parameter, with a default. Converting at the boundary, and failing there if it
is wrong, is the same discipline as everywhere else.

**Returning a tuple** `(body, status)` sets the status code. Returning 404 with
a JSON body that names what was not found is much better than a bare 404,
because the client's logs then contain the reason.

**`/health/ready`** is a readiness endpoint. Kubernetes and load balancers need
one, as in [lesson 15](containers.html). Add it from the start; adding it later
always means a deployment argument.

### Testing a Flask API

```python
def test_filters_by_affiliation():
    client = app.test_client()
    response = client.get("/api/v1/tracks?affiliation=hostile")
    assert response.status_code == 200
    assert [t["trackId"] for t in response.get_json()] == ["T-001"]


def test_unknown_track_returns_404_with_a_reason():
    response = app.test_client().get("/api/v1/tracks/NOPE")
    assert response.status_code == 404
    assert response.get_json()["trackId"] == "NOPE"
```

`app.test_client()` exercises the whole request path **without starting a
server or touching the network**. That makes API tests fast enough to run on
every commit, which is the entire argument for having them.

### Flask in production

Say this if it comes up, because it is a common gap:

**The Flask development server is not for production.** It is single-threaded
and not hardened. In production you run the app behind a WSGI server such as
Gunicorn or uWSGI, usually behind a reverse proxy:

```bash
gunicorn --workers 4 --bind 0.0.0.0:8080 app:app
```

Flask versus **FastAPI**: FastAPI is the modern alternative with built-in
request validation from type hints and automatic OpenAPI documentation. Flask
is older, simpler and more widely deployed. Knowing both exist is enough.

## 6. Documenting the contract

**OpenAPI**, formerly Swagger, is the REST equivalent of a WSDL: a
machine-readable description of every endpoint.

```yaml
paths:
  /api/v1/tracks:
    get:
      summary: List current tracks
      parameters:
        - name: affiliation
          in: query
          schema:
            type: string
            enum: [friend, hostile, neutral, unknown]
      responses:
        '200':
          description: The current track list
```

Why bother: it generates client code and interactive documentation, and it
enables **contract testing**, where both sides are verified against the same
document rather than against each other's assumptions. On an integration
programme that is the difference between finding a mismatch in a design review
and finding it in the lab.

## 7. Cross-cutting concerns

Things every API needs, none of which are the happy path.

**Authentication and authorisation.** Who you are, then what you may do. Tokens
go in the `Authorization` header, never in the URL, because URLs are logged.

**Rate limiting.** Return 429 with a `Retry-After` header. Without it, one
misbehaving client can deny service to everyone.

**Timeouts on every call you make.** A call with no timeout is a thread that
may never come back. This is the single most common omission in client code.

**Retry with backoff and jitter.** Retry only idempotent operations. Add random
jitter, or many clients retry in lockstep and finish off a struggling service.

**Circuit breaker.** After enough consecutive failures, stop calling for a
while. It lets a failing dependency recover instead of being hammered.

**Correlation IDs.** Generate an ID at the edge and pass it through every
downstream call and log line. It is the only practical way to reconstruct one
operation across several services.

**Never return a stack trace to a caller.** It leaks internal structure. Log
the detail, return a generic message plus the correlation ID.

## 8. Practice

**A1.** Extend the Flask API with `POST /api/v1/tracks` that validates the body
and returns 201 with a `Location` header, or 400 with a reason.

**A2.** Write tests for every status code your API can return, including 404
and 400.

**A3.** Add pagination with `limit` and `cursor`, and a test proving no row is
skipped or duplicated when a new track is inserted mid-paging.

**A4.** Write the OpenAPI snippet describing your endpoints.

**A5.** Take a JSON payload and write a validating parser that treats the input
as untrusted, as in [lesson 7](frontend.html) section 6.

**A6.** Write a client with a timeout, three retries with exponential backoff
and jitter, and a test using a fake that fails twice then succeeds.

A6 is the most valuable. It is the reliability pattern you will be asked about.

## 9. Questions to be ready for

1. **What makes an API RESTful?** Resources as URLs, HTTP methods as verbs,
   stateless requests, representations in a standard format.
2. **`PUT` versus `PATCH`?** Replace the whole resource versus modify part of
   it.
3. **Which methods are idempotent, and why does it matter?** `GET`, `PUT`,
   `DELETE`. It decides what a client may safely retry.
4. **401 versus 403?** Not authenticated versus not permitted.
5. **How do you version an API?** Section 2, ending on interface control.
6. **REST versus SOAP?** The table in section 3, plus the honest note that SOAP
   persists because it is already there and formally contracted.
7. **What is a WSDL?** SOAP's machine-readable contract; generates client code.
8. **When would you choose gRPC?** High-rate internal traffic and streaming,
   where you control both ends and want a generated typed contract.
9. **How do you handle a slow dependency?** Timeout, bounded retry with jitter,
   circuit breaker, degraded fallback, and make the degradation visible in
   metrics rather than silent.
10. **How do you test an API without a network?** A test client that exercises
    the request path in process, as in section 5.
11. **What is XXE and why do you care?** Section 3. Disable external entities
    and DTDs.
12. **What goes in a health endpoint?** Liveness says the process is alive;
    readiness says it can serve, including that its dependencies are reachable.
    See [lesson 15](containers.html).
