# 11. Architecture and the Software Factory

The desired skills list "comprehensive understanding of Services, Microservices,
Software Factories, Cloud-native and Service-Oriented Architectures." This
lesson gives you the vocabulary and, more importantly, the judgment to use it
without sounding like you are reciting a conference talk.

## 1. Service-oriented architecture

SOA is the older term and it is the one that fits a program like this. The idea:
decompose a system into services that expose capabilities over a network
contract, so that consumers depend on the contract rather than the
implementation.

Classic SOA in defense systems tends to mean coarse-grained services, an
enterprise service bus or a publish-subscribe middleware, formal interface
control documents, and strong versioning discipline because the consumers are
other programs you cannot redeploy at will.

**Microservices** is SOA with smaller services, independent deployment,
per-service data ownership, and an emphasis on team autonomy. The differences
that matter in practice: microservices push away from a central bus toward
lightweight protocols, and they trade operational simplicity for deployment
independence.

The senior framing: *"Microservices buy you independent deployability, and you
pay for it in operational complexity, distributed debugging, and network failure
modes. That trade is worth it when independent deployment is genuinely the
constraint, which usually means many teams shipping at different rates. On a
system that deploys as a qualified baseline on a scheduled window, that
particular benefit is worth much less, so the calculus is different. What still
pays off is clean service boundaries and versioned contracts, whether or not
they deploy separately."*

That answer will do more for you than an enthusiastic endorsement.

## 2. The distributed systems facts you should have ready

- **The fallacies of distributed computing.** The network is not reliable,
  latency is not zero, bandwidth is not infinite, the network is not secure,
  topology changes, there is more than one administrator, transport cost is not
  zero, the network is not homogeneous. On a geographically dispersed air
  defense system, every single one of these is a live design constraint rather
  than a slogan.
- **CAP.** In a partition you choose availability or consistency. Real systems
  choose per-operation. For an air picture, availability of a slightly stale
  track usually beats unavailability of a perfect one, but you must know which
  operations are the exception.
- **Idempotency.** A retried message must not double-apply. Give messages ids
  and make handlers idempotent. This is the single most useful reliability
  property in a message-driven system.
- **At-most-once, at-least-once, exactly-once.** Exactly-once delivery does not
  exist end to end; what you can build is at-least-once delivery plus idempotent
  processing, which is observably equivalent. Saying that precisely is a strong
  signal.
- **Backpressure.** When a consumer is slower than a producer, something must
  give. Bound your queues and choose consciously between blocking, dropping, and
  shedding load. An unbounded queue is a deferred crash.
- **Timeouts, retries, and circuit breakers.** Every remote call gets a timeout.
  Retries need jitter and a budget, or you build a synchronized retry storm that
  finishes off a struggling service. A circuit breaker stops calling a dependency
  that is failing so it can recover.
- **Clock skew.** Never assume two machines agree on the time. Use monotonic
  clocks for durations, and be explicit about the time source when ordering
  events across sites.

## 3. Communication styles

| Style | Use when | Watch out for |
| --- | --- | --- |
| **Synchronous request/response** (REST, gRPC) | Caller needs an answer now | Coupling, cascading failure, timeout budgets |
| **Asynchronous messaging** (queue) | Work can be deferred; producer and consumer decoupled | Ordering, duplicate delivery, poison messages |
| **Publish/subscribe** | Many consumers of the same event | Slow consumers, fan-out cost, no backpressure by default |
| **Streaming** | Continuous high-rate data | Partitioning, replay, retention |

For a sensor-fusion system, publish/subscribe is the natural fit, which is why
**DDS** (Data Distribution Service) is common in this domain. If it comes up:
DDS is a publish/subscribe middleware standard with rich quality-of-service
policies (reliability, durability, deadline, latency budget), peer-to-peer
discovery, and no central broker, which is why real-time defense and robotics
systems use it. You are not expected to have used it. Knowing what it is and why
it exists is enough and it is a nice thing to know on this program.

Other names worth recognizing: Kafka for durable partitioned streaming, RabbitMQ
or ActiveMQ for classic brokered messaging, ZeroMQ for lightweight patterns, and
**Link 16** as the tactical data link standard that actually carries the air
picture between platforms.

## 4. API design

```
GET    /api/v1/tracks?state=active&updated_since=2026-09-09T12:00:00Z
GET    /api/v1/tracks/{trackId}
POST   /api/v1/tracks
PUT    /api/v1/tracks/{trackId}
PATCH  /api/v1/tracks/{trackId}
DELETE /api/v1/tracks/{trackId}
```

Know the status codes and their meanings: 200 ok, 201 created, 202 accepted,
204 no content, 400 bad request, 401 unauthenticated, 403 unauthorized, 404 not
found, 409 conflict, 422 unprocessable, 429 rate limited, 500 server error, 503
unavailable. Know that GET, PUT and DELETE are idempotent while POST is not, and
know that this is why retry logic can safely repeat the first three.

**Versioning** is where a defense program differs from a startup. You cannot
redeploy the consumers. So: version the contract explicitly, never make a
breaking change in place, add fields rather than repurposing them, and support
the old version until every consumer has migrated on a schedule you agreed in
writing. If asked how you would change a message format used by three other
programs, that is the answer, and the second half of it is that the change goes
through an interface control working group, not a merge request.

## 5. The Software Factory

This is the term in the posting, so be able to speak to it directly.

A software factory is a standardized, reusable set of pipelines, tooling,
hardened base images, environments and processes that programs plug into,
instead of every program inventing its own build and deployment stack. In the
defense world the model was popularized by efforts such as the Air Force's
Kessel Run and Platform One, and every major prime now runs an internal
equivalent. Lockheed Martin's is what the posting refers to.

**What it typically provides:**

- Source control and merge-request workflow with enforced approvals.
- Standard CI templates so a new repository gets a compliant pipeline on day
  one.
- Hardened, accredited base container images that are already STIG-configured
  and scanned.
- Integrated security scanning: SAST, software composition analysis, secret
  scanning, container image scanning, with results routed into the compliance
  record.
- An artifact repository with immutable, signed, traceable artifacts.
- Automated generation of some of the evidence that accreditation requires, so
  the security paperwork is a byproduct of the pipeline rather than a separate
  manual campaign.
- A **continuous ATO** ambition: because the controls are continuously
  evidenced, changes can be authorized far faster than a traditional
  accreditation cycle allows.

**Why a program migrates into it**, which is exactly what the posting says you
would be doing: the legacy build is a hand-maintained script on a machine
someone configured in 2016, nobody can reproduce it, security evidence is
gathered by hand each cycle, and every release costs a manual campaign. Moving
into the factory makes the build reproducible, the artifacts traceable, and the
security evidence continuous.

**What is hard about the migration**, and saying this shows you have done it:

- The legacy build has undocumented assumptions: a tool at a fixed path, a
  network share, a license server, a specific compiler patch level.
- Tests that were never automated because they required hardware. You need
  simulators, recorded data replay, or hardware in the loop wired into the
  pipeline.
- Dependencies that are not in any registry, delivered once by a vendor on
  media.
- The factory's hardened base images may be missing something the application
  needs, and adding it requires justification.
- Air-gapped constraints: no public package repositories, so everything comes
  from an internal mirror with its own approval process.
- Cultural: people who have released this system by hand for a decade need to
  trust the pipeline before they will rely on it.

Have an answer to *"how would you approach migrating a legacy build into our
pipeline?"* It is close to a certainty. Structure it: inventory the current
build and make it reproducible on a clean machine first; get it green in the
pipeline with tests skipped; add the automatable tests; add scanning with a
baselined backlog; add artifact publishing with immutable tags; then move the
deployment step last. One capability at a time, each one merged and working
before the next.

## 6. Cloud-native, stated carefully

The twelve-factor ideas that transfer regardless of cloud:

- Configuration in the environment, not baked into the artifact.
- Stateless processes, with state pushed to backing services.
- Explicit, isolated, pinned dependencies.
- Logs as an event stream to stdout, not files the application manages.
- Strict dev/prod parity, which is the whole argument for containerized test
  environments.
- Disposability: fast startup, graceful shutdown on SIGTERM.

Say the caveat too: an operational air defense site may be disconnected, on
premises, and accredited as a fixed baseline. "Cloud-native" there means the
engineering practices, not a public cloud. The practices that survive are
containerized reproducibility, declarative configuration, health endpoints, and
observability. The ones that do not survive are elastic autoscaling and
continuous deployment straight to production.

## 7. Observability

For a fielded system that engineers cannot easily reach, this is
disproportionately important. The three pillars:

**Logs.** Structured, ideally JSON, with a correlation id threaded through every
service so one operational event can be reconstructed across components. Log
levels used consistently. No secrets, no full payloads.

**Metrics.** Counters, gauges, histograms. The ones that matter for an ingest
and fusion system: messages per second per sensor, **age of the last message per
sensor** (the one that detects a silent sensor), queue depth, drop count,
end-to-end latency percentiles, track count, error rate by type, and resource
saturation.

**Traces.** Distributed tracing shows one request's path across services with
timing at each hop. OpenTelemetry is the vendor-neutral standard worth naming.

Two things to say that show operational maturity:

- **Percentiles, not averages.** The average latency is fine while the 99th
  percentile is catastrophic. Operators feel the tail.
- **Alert on symptoms users experience, not on causes.** Alert that the air
  picture is stale, not that CPU is at 80 percent. Every alert should have a
  runbook and a human action; an alert nobody acts on trains people to ignore
  the console.

## 8. Data and persistence

Worth having a position on, since it comes up.

- **Relational** when you have structured data with relationships and you want
  transactions and constraints. This is most of the time, and the default answer.
- **Key-value or document** for high-volume, schema-flexible, or
  denormalized-read workloads.
- **Time series** for metrics and historical track data, where the query is
  "everything for this id in this window."
- **In-memory** for the hot current picture, with periodic persistence, because
  the live air picture is read constantly and rebuilt on restart from the
  sensors anyway.

Basic SQL you should still be able to write on a whiteboard:

```sql
SELECT s.sensor_id,
       COUNT(*)                AS detections,
       AVG(d.confidence)       AS avg_confidence,
       MAX(d.observed_at)      AS last_seen
  FROM detections d
  JOIN sensors s ON s.id = d.sensor_id
 WHERE d.observed_at >= NOW() - INTERVAL '1 hour'
 GROUP BY s.sensor_id
HAVING COUNT(*) >= 10
 ORDER BY avg_confidence DESC
 LIMIT 5;
```

Know the join types, know that `WHERE` filters rows before grouping while
`HAVING` filters groups after, know what an index costs on write and buys on
read, and know what `EXPLAIN` is for. That is enough for this role.

## 9. Practical architecture questions

1. **Monolith or microservices for a new subsystem?** Start with a well-modularized
   monolith unless you have a specific reason not to. You can extract a service
   from clean module boundaries; you cannot easily un-distribute a system you
   split too early.
2. **How do you handle a slow downstream dependency?** Timeout, bounded retry
   with jitter, circuit breaker, fall back to cached or degraded output, and
   make the degradation visible in metrics rather than silent.
3. **How do you version a message format?** Section 4.
4. **How would you make this system testable end to end without hardware?**
   Recorded data replay, sensor simulators, and a contract test per adapter so
   the simulator and the real device are held to the same interface.
5. **What is the failure mode you worry about most?** A good answer for this
   domain: silent degradation. A crash is loud and someone fixes it. A sensor
   that quietly stops updating, or a correlation that quietly starts producing
   duplicate tracks, can persist for a long time. That is why last-message-age
   and track-count metrics with alerting are not optional.
