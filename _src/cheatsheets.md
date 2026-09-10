# 18. Cheat sheets

Skim these the morning of the interview. Nothing else.

## Program, in thirty seconds

EADGE-T is Lockheed Martin's integrated air and missile defense C2 system for
the UAE. It fuses many sensors into one air picture and gives battle managers
one place to task effectors including THAAD and Patriot PAC-3. The Tech Refresh
modernizes hardware and closes cybersecurity gaps, which in software means COTS
and FOSS updates, migrating builds into the Software Factory CI/CD pipelines,
and building real automated test coverage. The hard part is doing all of that to
a fielded, accredited baseline without changing mission behavior.

## Python

```python
# collections
d.get(k, default); d.setdefault(k, []).append(v); d.items()
from collections import Counter, defaultdict, deque
Counter(xs).most_common(3)
groups = defaultdict(list); groups[k].append(v)
q = deque(maxlen=100); q.appendleft(x); q.popleft()

# sorting
sorted(xs, key=lambda t: (-t[1], t[0]))
max(xs, key=lambda t: t.confidence)
import heapq; heapq.nlargest(3, xs, key=f)

# strings
s.strip().split(","); ",".join(parts); s.startswith("x")
f"{v:.2f}  {n:05d}  {p:.1%}  {s:>10}"

# comprehensions
[f(x) for x in xs if p(x)]; {k: v for k, v in pairs}; (f(x) for x in xs)

# files
with open(p, encoding="utf-8") as fh:
    for line in fh: ...

# errors
try: ...
except ValueError as e: log.warning("bad: %s", e)
finally: ...

# classes
@dataclass(frozen=True)
class Detection:
    sensor_id: str
    confidence: float = 1.0
```

Traps: mutable default arguments; `+=` on strings in a loop; bare `except`;
`x in list` inside a loop when it should be a set.

## Java

```java
Map<String,List<D>> m = new HashMap<>();
m.computeIfAbsent(k, x -> new ArrayList<>()).add(v);
counts.merge(k, 1, Integer::sum);
list.sort(Comparator.comparingDouble(D::conf).reversed().thenComparing(D::id));
list.removeIf(this::stale);

var byId = ds.stream().collect(Collectors.groupingBy(D::sensorId, Collectors.counting()));
var top  = ds.stream().max(Comparator.comparingDouble(D::conf));
var names = ds.stream().map(D::sensorId).distinct().sorted().toList();

try (var r = Files.newBufferedReader(p)) { ... }

public record Detection(String sensorId, long ts, double conf) {}
```

Rules: equals and hashCode together, on the same immutable fields.
`volatile` is visibility only. Immutability is the cheapest thread safety.
ArrayList unless you have a reason.

## Complexity

Hash lookup O(1). Sort O(n log n). Heap push/pop O(log n). Binary search
O(log n). Nested loop over the same list O(n^2).
The most common real fix: a set membership test instead of a list scan inside a
loop, turning O(n^2) into O(n).

## Linux

```bash
grep -rn "pat" .            find . -name "*.log" -mtime -1
tail -f app.log             journalctl -u svc -n 200 -f
sort | uniq -c | sort -rn | head
ps aux | grep x             ss -tulpn          lsof -i :8080
df -h; du -xh --max-depth=2 | sort -h; lsof +L1
systemctl status|restart|daemon-reload
free -h; uptime; vmstat 1 5; iostat -xz 1
set -euo pipefail
```

Service will not start: status, journal, run it by hand as the service user,
disk and memory, then SELinux (`ausearch -m avc -ts recent`).
Disk full but `du` shows nothing: `lsof +L1`, a deleted file held open.

## Git

```bash
git switch -c feature/EADGE-1234-x       git add -p
git log --oneline --graph --all          git blame -L 40,80 f
git log -S "symbol"                      git bisect run ./repro.sh
git restore [--staged] f                 git reset --soft HEAD~1
git revert <sha>                         git reflog
git merge --no-ff origin/develop         git merge --abort
git config merge.conflictstyle zdiff3
```

Revert on shared history, reset only on your own unpushed work. Reflog recovers
almost anything.

## Testing and CI

Good test: fast, independent, deterministic, one reason to fail, would actually
fail if the code were wrong. Arrange, Act, Assert.
Legacy code: characterization tests, then find a seam, then refactor.
Flaky test is an emergency; a retry is not a fix.
Coverage finds gaps; it does not measure quality.
**Build the artifact once and promote it.** Never rebuild between test and
deploy.
Pipeline order: lint, unit, package, integration, scan, publish, deploy, with a
manual gate before production.

## Containers

Container is a process isolated by namespaces and cgroups, sharing the host
kernel. Multi-stage build, non-root user, pinned versions, dependencies copied
before source for layer caching, `HEALTHCHECK`, exec-form `ENTRYPOINT`.
Liveness fails means restart; readiness fails means remove from service.
Memory over limit means OOM kill; CPU over limit means throttle.
Helm gives templated manifests plus versioned releases; `--atomic` rolls back.

## Security

CVE response: confirm version and reachability and exposure, check KEV and any
mandated date, then upgrade, backport, mitigate, or accept with a POA&M. One
dependency per merge request. Full regression. Regenerate the SBOM. Add
continuous scanning so the next one is not a surprise.
Parameterized queries. No `pickle` or `yaml.load` on untrusted input. No secrets
in source, images, logs, or tickets. Non-root, least privilege. Never disable
SELinux or a STIG control to make a problem go away.

## Design answer skeleton

1. Clarify: scale, rate, latency budget, failure expectations, persistence.
2. Components and boundaries, drawn.
3. Justify each boundary in terms of what changes independently.
4. Name the failure modes: backpressure, slow consumer, silent sensor, clock
   skew, restart.
5. Name what you would test and how, including replay against a golden output.
6. Name what you deliberately did not build, and what would change your mind.

## STAR reminders

Situation twenty seconds. "I", not "we". End with a number. Add what you would
do differently.

Six stories: hard problem, disagreement, failure, deadline, process improvement,
cross-boundary collaboration.

## Lines to have ready

- "Let me restate the problem to make sure I have it."
- "What is the scale here, and can I assume it fits in memory?"
- "I'll write the straightforward version first, then improve it."
- "Cases I'd test: empty, single element, all duplicates, malformed input."
- "I'm blanking on the exact call; the idea is a min-heap of size k."
- "I haven't used that. Here is the closest thing I have done, and here is my
  understanding of it. Is that how you use it?"

## Do not

- Go silent for more than about fifteen seconds.
- Say "we" when they asked what you did.
- Bluff a technology. It always unravels on the second follow-up.
- Criticize a former employer or colleague.
- Answer "no questions."
- Volunteer classified detail. "I can describe that at an unclassified level" is
  the right sentence.

## Do

- Ask about scale before you code.
- Say what you would test, unasked.
- Give the tradeoff, not just the answer.
- Name what you deliberately left out of a design.
- Say plainly that you want the job.
