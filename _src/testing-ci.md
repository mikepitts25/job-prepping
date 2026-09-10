# 10. Testing and CI/CD

Read the posting again: *"Developing unit tests and automated test capabilities
to improve software quality, reliability, and deployment efficiency"* and
*"migrating legacy capabilities into Lockheed Martin's Software Factory CI/CD
pipelines."*

That is the job. This lesson is the highest-yield one on the site. If you
prepare nothing else technically, prepare this.

## 1. The test pyramid and why it matters here

```
        /\        End-to-end / lab      few, slow, expensive, brittle
       /  \       ---------------------------------------------------
      /    \      Integration           some, medium
     /      \     ---------------------------------------------------
    /________\    Unit                  many, fast, cheap, precise
```

**Unit.** One class or function, no I/O, milliseconds. Thousands of them.
**Integration.** Several components together, possibly a real database or
message broker. Hundreds.
**End-to-end / lab.** The whole system on representative hardware. A handful,
and each costs hours of lab time and a scheduled slot.

The economic argument, which is the one to make in the interview: **on this
program the lab is the scarce resource.** Every defect a unit test catches is a
lab slot you did not consume and a week you did not lose. That is what "improve
deployment efficiency" in the posting means in practice. Framing it as economics
rather than as best-practice hygiene is a senior framing.

## 2. What makes a test worth having

A test suite is an asset only if people trust it. Trust comes from:

- **Deterministic.** Same input, same result, every run. No dependence on wall
  clock, random seeds, network, or test execution order.
- **Fast.** A suite people wait ten minutes for is a suite people skip.
- **Independent.** Any test can run alone. No shared mutable fixture state.
- **Focused.** One reason to fail. When it goes red you know where to look.
- **Readable.** The test is the specification. Name it after the behavior:
  `rejects_detection_with_confidence_above_one`, not `test3`.
- **Would actually fail.** Mutate the code deliberately and confirm the test
  goes red. A test that passes against broken code is worse than no test,
  because it buys false confidence.

The FIRST acronym covers most of this: Fast, Independent, Repeatable,
Self-validating, Timely.

**Flaky tests are an emergency, not an annoyance.** State this clearly if asked.
One flaky test teaches the whole team to re-run the pipeline instead of reading
the failure, and from that point the suite protects nothing. Quarantine it with
a ticket and a deadline, find the root cause, fix it. Never just add a retry.

## 3. Arrange, Act, Assert

```python
def test_burst_drops_oldest_and_counts_it():
    # Arrange
    queue = IngestQueue(capacity=3, policy="drop_oldest")

    # Act
    for i in range(5):
        queue.offer(detection(seq=i))

    # Assert
    assert [d.seq for d in queue.drain()] == [2, 3, 4]
    assert queue.dropped_count == 2
```

One behavior per test. If you need "and" in the test name, it is probably two
tests.

## 4. Test doubles, named correctly

Interviewers do ask you to distinguish these.

| Double | What it does |
| --- | --- |
| **Dummy** | Filler passed to satisfy a signature, never used |
| **Stub** | Returns canned answers to calls |
| **Spy** | A stub that also records how it was called |
| **Mock** | Pre-programmed with expectations; the assertion is on the interaction |
| **Fake** | A real working implementation, simplified (in-memory store) |

```python
from unittest.mock import MagicMock, patch

def test_publishes_only_high_confidence():
    publisher = MagicMock()                       # spy/mock
    service = IngestService(publisher=publisher)  # dependency injection

    service.handle(detection(confidence=0.95))
    service.handle(detection(confidence=0.10))

    publisher.publish.assert_called_once()
    assert publisher.publish.call_args[0][0].confidence == 0.95

@patch("eadge.client.requests.get")
def test_sensor_timeout_is_not_fatal(mock_get):
    mock_get.side_effect = TimeoutError("no route to host")
    assert poll_sensor("radar-a") == SensorStatus.UNKNOWN
```

**Prefer fakes to mocks** where you can. A test that asserts on a chain of mock
interactions breaks whenever you refactor, even when behavior is unchanged. A
test against an in-memory fake asserts on outcomes and survives refactoring.
That opinion, stated with the reason, is a good answer.

The deeper point: **if a class is hard to test, that is a design defect, not a
testing problem.** Hard-to-test usually means it constructs its own
dependencies, reads global state, or does five things. See
[lesson 7](ood.html).

## 5. Testing the hard things

### Time

Never call `datetime.now()` or `System.currentTimeMillis()` deep inside logic.
Inject a clock.

```python
class TrackAger:
    def __init__(self, now=time.monotonic, max_age_s=30.0):
        self._now = now
        self._max_age = max_age_s

    def stale(self, track):
        return self._now() - track.last_update > self._max_age

def test_track_goes_stale_after_max_age():
    fake_time = [1000.0]
    ager = TrackAger(now=lambda: fake_time[0], max_age_s=30.0)
    track = Track(last_update=1000.0)

    assert not ager.stale(track)
    fake_time[0] = 1031.0
    assert ager.stale(track)
```

Use `time.monotonic` rather than wall clock for durations. Wall clock can jump
backwards on an NTP correction, which on a system with sites synchronizing to a
time source is a real failure mode, not a hypothetical one.

### Randomness

Seed it, or inject the generator. Same principle.

### Concurrency

Do not test with `sleep`. Use latches, barriers, and deterministic executors.
For Java, a `CountDownLatch` and a same-thread executor. For Python, drive the
loop deterministically. If a concurrency test genuinely needs timing, it belongs
in a separate slow suite that is not on the fast feedback path.

### Legacy code with no tests

This is the question most likely to come up for this role.

> First, characterization tests. I do not try to write correct tests, I write
> tests that capture what the code does today, including the odd behaviors,
> because on a fielded system those odd behaviors may be what the operator
> depends on. Golden-file testing works well: capture the current output for a
> set of recorded inputs and assert it stays byte-identical.
>
> With that net in place I can find a seam, inject the dependency, and start
> pulling logic out into testable units. The characterization tests catch me if
> I change behavior by accident, and when one of them legitimately needs to
> change, that becomes a conversation with the systems engineer about whether
> the old behavior was a requirement or an accident.

That is close to a perfect answer for this posting.

## 6. Coverage, used honestly

```bash
pytest --cov=eadge --cov-report=term-missing --cov-report=xml
mvn verify        # with jacoco-maven-plugin bound to the verify phase
```

Say the true thing about coverage: **it is a good detector of untested code and
a bad measure of test quality.** Ninety percent line coverage with assertions
that never fail is worthless. Zero percent on the correlation engine is
alarming. Use it to find gaps, set a floor that must not regress, and never
treat the number as a goal in itself. Branch coverage is more informative than
line coverage. Mutation testing (`mutmut`, `PIT`) is the honest measure if the
program will pay for it.

For safety-relevant software, coverage requirements can be contractual, up to
and including modified condition/decision coverage. If you are asked about
DO-178C or similar, it is fine to say you have not worked to that standard but
you understand the intent: the rigor of the evidence scales with the criticality
of the failure.

## 7. Static analysis and quality gates

```bash
# Python
ruff check .                 # fast linting
black --check .              # formatting
mypy src/                    # static typing
bandit -r src/               # security-focused static analysis

# Java
mvn spotbugs:check
mvn checkstyle:check
mvn com.github.spotbugs:spotbugs-maven-plugin:check
mvn org.owasp:dependency-check-maven:check     # known-vulnerable dependencies
```

Programs commonly run SonarQube, Fortify, Coverity, or Black Duck. Know what
each category does: **SAST** analyzes source for defects and vulnerabilities,
**SCA** inventories dependencies and matches them against vulnerability
databases, **DAST** probes a running system, and **secret scanning** catches
credentials committed to the repository. Being able to name those four
categories is enough.

The important practice: **fail the build on new findings, not on the entire
existing backlog.** On legacy code you inherit thousands of findings. Baseline
them, block anything new, and burn the backlog down deliberately. Otherwise the
gate gets disabled within a week.

## 8. A GitLab CI pipeline, explained stage by stage

Write one of these for your practice repo. Being able to read and explain a
pipeline is directly tested by this posting.

```yaml
# .gitlab-ci.yml
stages: [build, test, quality, package, deploy]

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  IMAGE: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"

default:
  image: python:3.11-slim
  cache:
    key:
      files: [requirements.txt]
    paths: [.cache/pip, .venv]

build:
  stage: build
  script:
    - python -m venv .venv
    - .venv/bin/pip install --no-cache-dir -r requirements.txt -e .
  artifacts:
    paths: [.venv]
    expire_in: 1 hour

unit-tests:
  stage: test
  script:
    - .venv/bin/pytest -q --junitxml=report.xml
      --cov=eadge --cov-report=xml --cov-report=term
  coverage: '/^TOTAL.*\s+(\d+%)$/'
  artifacts:
    when: always
    reports:
      junit: report.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

integration-tests:
  stage: test
  services:
    - name: postgres:16
      alias: db
  variables:
    DATABASE_URL: "postgresql://ci:ci@db:5432/ci"
  script:
    - .venv/bin/pytest -q tests/integration
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

lint-and-sast:
  stage: quality
  script:
    - .venv/bin/ruff check .
    - .venv/bin/mypy src/
    - .venv/bin/bandit -r src/ -f json -o bandit.json
  artifacts:
    when: always
    paths: [bandit.json]

dependency-scan:
  stage: quality
  script:
    - .venv/bin/pip install pip-audit
    - .venv/bin/pip-audit --strict -r requirements.txt
  allow_failure: false

container:
  stage: package
  image: docker:27
  services: [docker:27-dind]
  script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
    - docker build -t "$IMAGE" .
    - docker push "$IMAGE"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.internal
  script:
    - helm upgrade --install eadge-ingest ./chart
      --namespace staging --set image.tag="$CI_COMMIT_SHORT_SHA" --wait --atomic
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  stage: deploy
  environment:
    name: production
  when: manual                       # human gate; required on a fielded system
  script:
    - helm upgrade --install eadge-ingest ./chart
      --namespace production --set image.tag="$CI_COMMIT_SHORT_SHA" --wait --atomic
  rules:
    - if: $CI_COMMIT_TAG
```

Points to make when explaining it:

- **Fast feedback first.** Lint and unit tests before anything slow. A developer
  should know within three minutes.
- **Artifacts flow forward.** Build once, test that artifact, ship that same
  artifact. Never rebuild between test and deploy, or you have shipped something
  you did not test. This is the single most important CI principle and it is
  worth saying emphatically.
- **Rules control cost.** Integration tests on merge requests and the default
  branch, not on every push to every branch.
- **Manual gate on production.** On an accredited system the pipeline stops at a
  human decision. Continuous delivery, not continuous deployment.
- **Immutable tags.** Tag images by commit SHA, never by `latest`, so a
  deployment is traceable to a commit.
- **`--atomic` on Helm** rolls back automatically if the release fails.

## 9. The Jenkins equivalent

Named in the desired skills, so know the vocabulary and the shape.

```groovy
pipeline {
  agent { label 'linux && docker' }

  options {
    timeout(time: 45, unit: 'MINUTES')
    buildDiscarder(logRotator(numToKeepStr: '30'))
    disableConcurrentBuilds()
  }

  environment {
    ARTIFACTORY = credentials('artifactory-deploy')   // never inline a secret
  }

  stages {
    stage('Build')  { steps { sh 'mvn -B clean compile' } }

    stage('Unit test') {
      steps { sh 'mvn -B test' }
      post {
        always {
          junit 'target/surefire-reports/*.xml'
          jacoco()
        }
      }
    }

    stage('Static analysis') {
      parallel {
        stage('SpotBugs')  { steps { sh 'mvn -B spotbugs:check' } }
        stage('Checkstyle'){ steps { sh 'mvn -B checkstyle:check' } }
        stage('OWASP')     { steps { sh 'mvn -B org.owasp:dependency-check-maven:check' } }
      }
    }

    stage('Package') {
      steps { sh 'mvn -B -DskipTests package' }
      post { success { archiveArtifacts artifacts: 'target/*.jar', fingerprint: true } }
    }

    stage('Deploy to lab') {
      when { branch 'main' }
      steps { sh './deploy.sh lab' }
    }
  }

  post {
    failure { emailext to: 'team@example.com', subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}" }
    always  { cleanWs() }
  }
}
```

Vocabulary: declarative versus scripted pipelines, agents and labels,
`Jenkinsfile` in the repository as pipeline-as-code, shared libraries for
reusable steps, the credentials binding plugin so secrets never appear in the
`Jenkinsfile`, and `fingerprint: true` for artifact traceability.

## 10. Deployment strategies

Know these four by name and by tradeoff.

| Strategy | How | Cost / benefit |
| --- | --- | --- |
| **Rolling** | Replace instances a few at a time | No extra capacity; two versions coexist mid-roll |
| **Blue/green** | Stand up the new version fully, then switch traffic | Instant rollback; doubles infrastructure |
| **Canary** | Send a small traffic slice to the new version, watch, expand | Best risk control; needs good metrics |
| **Recreate** | Stop old, start new | Downtime; simplest, sometimes the only option |

For a fielded air defense system, the honest answer is that many of these are
constrained: you may have a scheduled maintenance window, a formal regression
campaign, and an accreditation review before anything reaches the operational
site. Saying that shows you understand the environment rather than reciting
cloud practice. What still applies: build once, deploy the same artifact through
each environment, make rollback a tested procedure rather than a hope, and know
your recovery time before you need it.

## 11. Questions to be ready for

1. **What do you unit test versus integration test?** Unit for logic and edge
   cases; integration for the wiring, the serialization, and the assumptions
   about external systems.
2. **How do you test code with no tests?** Section 5.
3. **What is a flaky test and what do you do about it?** Section 2. Emphasize
   that a retry is not a fix.
4. **What belongs in a pipeline?** Section 8, in order, with the build-once
   principle called out.
5. **How do you test a race condition?** Make the schedule deterministic, use
   latches instead of sleeps, run the suspect section under a stress harness
   with thread-sanitizer-style tooling if available, and prefer a design that
   removes the shared state.
6. **How much coverage is enough?** Section 6, honestly.
7. **A test fails in CI but passes locally. What now?** Diff the environments,
   check test ordering and shared state, check timezone and locale, check
   parallelism, check whether the local run is using stale build output. Then
   reproduce it in CI with extra logging rather than guessing.
8. **How do you keep a pipeline fast?** Cache dependencies, parallelize
   independent jobs, split the slow suite off the merge-request path, fail fast
   on lint, and only run expensive scans on the default branch and tags.
