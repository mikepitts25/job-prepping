# 11. Docker, Kubernetes and Helm

These are listed under **desired** skills, not basic qualifications. That matters
for how you prepare: you need working competence and honest boundaries, not
depth. A candidate who explains containers clearly and says "I have used
Kubernetes manifests but not written a Helm chart from scratch" is in good shape.
A candidate who bluffs and gets three questions deep is not.

## 1. What a container actually is

The answer that distinguishes people who understand this from people who have
only used it:

> A container is a normal Linux process, isolated with kernel features rather
> than virtualized. **Namespaces** give it its own view of the process table,
> network stack, mounts, hostname and users. **cgroups** limit what it can
> consume in CPU, memory and I/O. The filesystem comes from a stack of
> read-only image layers with a thin writable layer on top, joined by a union
> filesystem. There is no guest kernel, which is why a container starts in
> milliseconds while a VM starts in tens of seconds.

Follow-on: **container versus VM.** A VM virtualizes hardware and runs its own
kernel, giving stronger isolation at the cost of size and startup time. A
container shares the host kernel. The security consequence is real and worth
noting: kernel isolation is weaker than hypervisor isolation, which is why
multi-tenant or high-assurance environments still often use VMs, sometimes with
containers inside them.

**Image versus container.** The image is the immutable template. The container
is a running instance of it. Same relationship as a class and an object, which
is a serviceable analogy in an interview.

## 2. Docker commands

```bash
docker build -t eadge-ingest:1.4.0 .
docker images; docker ps; docker ps -a
docker run --rm -it -p 8080:8080 -e LOG_LEVEL=DEBUG eadge-ingest:1.4.0
docker run -d --name ingest -v /data:/data:ro eadge-ingest:1.4.0
docker logs -f ingest
docker exec -it ingest /bin/sh          # get a shell inside
docker inspect ingest | less
docker stats                            # live resource usage
docker stop ingest && docker rm ingest
docker system df; docker system prune -a    # reclaim disk
docker history eadge-ingest:1.4.0       # what each layer added
```

## 3. A Dockerfile worth defending

```dockerfile
# ---- build stage -------------------------------------------------------
FROM registry.access.redhat.com/ubi9/python-311 AS build
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
COPY src/ src/
COPY pyproject.toml .
RUN pip install --no-cache-dir --prefix=/install .

# ---- runtime stage -----------------------------------------------------
FROM registry.access.redhat.com/ubi9/python-311-minimal
LABEL org.opencontainers.image.source="https://gitlab.internal/eadge/ingest" \
      org.opencontainers.image.version="1.4.0"

COPY --from=build /install /usr/local

RUN useradd --system --uid 10001 --no-create-home appuser
USER 10001

WORKDIR /opt/eadge
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 LOG_LEVEL=INFO

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8080/health').status==200 else 1)"

EXPOSE 8080
ENTRYPOINT ["python", "-m", "eadge.ingest"]
```

Every choice here is defensible, and being able to justify them is what gets
asked:

- **Multi-stage build.** Compilers and build tooling never reach the runtime
  image. Smaller image, smaller attack surface, fewer CVEs to remediate.
- **`COPY requirements.txt` before the source.** Layer caching. Source changes
  every commit, dependencies rarely, so dependency installation is cached.
  Getting the order wrong makes every build slow.
- **Non-root `USER`.** A hard requirement in any hardened environment, and
  usually an explicit STIG or Kubernetes policy control.
- **UBI base image.** Red Hat Universal Base Images are the natural choice on a
  RHEL program: same package ecosystem, redistributable, and supported for
  vulnerability remediation.
- **Pinned versions.** In `requirements.txt`, exact. Not `latest`, not a range.
  Reproducibility is a configuration-management requirement here, not a
  preference.
- **`HEALTHCHECK`.** The orchestrator needs to know the difference between a
  running process and a working service.
- **`ENTRYPOINT` in exec form**, so the process is PID 1 and receives signals,
  which means `docker stop` shuts down gracefully instead of being killed after
  the timeout.
- **`.dockerignore`.** Keep `.git`, tests, and local virtualenvs out of the
  build context.

Layers and caching, said briefly: each instruction creates a layer; layers are
cached and shared; a change invalidates that layer and everything after it.
Combining `RUN` commands with `&&` and cleaning package caches in the same layer
keeps the image small, because deleting a file in a later layer does not shrink
the earlier one.

## 4. docker compose, for the local development story

```yaml
services:
  ingest:
    build: .
    ports: ["8080:8080"]
    environment:
      LOG_LEVEL: DEBUG
      DATABASE_URL: postgresql://dev:dev@db:5432/dev
    depends_on:
      db: { condition: service_healthy }
    volumes: ["./src:/opt/eadge/src:ro"]

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 5s
      retries: 10
```

The value to name: a new developer on a dispersed team gets a working
environment with one command instead of a two-day setup document. On a program
with people in several time zones, that is a real productivity argument.

## 5. Kubernetes, enough to be useful

**What it is for.** Declarative orchestration. You describe the desired state,
controllers continuously reconcile actual state toward it. That reconciliation
loop is the central idea; lead with it.

**Objects to know:**

| Object | Purpose |
| --- | --- |
| **Pod** | One or more co-located containers; the unit of scheduling |
| **ReplicaSet** | Keeps N pod replicas running |
| **Deployment** | Manages ReplicaSets; gives you rolling updates and rollback |
| **StatefulSet** | For workloads with stable identity and storage |
| **DaemonSet** | One pod per node, typically log or metrics agents |
| **Service** | Stable virtual IP and DNS name in front of a changing set of pods |
| **Ingress** | HTTP routing from outside the cluster |
| **ConfigMap** | Non-secret configuration |
| **Secret** | Sensitive values; base64-encoded, so enable encryption at rest |
| **PersistentVolumeClaim** | Storage request |
| **Namespace** | Scoping and isolation boundary |
| **Job / CronJob** | Run to completion, once or on a schedule |

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: eadge-ingest
spec:
  replicas: 3
  selector:
    matchLabels: { app: eadge-ingest }
  template:
    metadata:
      labels: { app: eadge-ingest }
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        seccompProfile: { type: RuntimeDefault }
      containers:
        - name: ingest
          image: registry.internal/eadge-ingest:1.4.0     # never :latest
          ports: [{ containerPort: 8080 }]
          env:
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef: { name: ingest-config, key: log_level }
          resources:
            requests: { cpu: "250m", memory: "256Mi" }
            limits:   { cpu: "1",    memory: "512Mi" }
          livenessProbe:
            httpGet: { path: /health/live, port: 8080 }
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet: { path: /health/ready, port: 8080 }
            periodSeconds: 5
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities: { drop: ["ALL"] }
```

**Liveness versus readiness** is the most commonly asked Kubernetes question and
it has a crisp answer: **liveness** failing means the container is broken and
gets restarted; **readiness** failing means it is temporarily unable to serve
and gets removed from the Service endpoints without a restart. Confusing them
causes restart loops during slow startup, which is why `startupProbe` exists.

**Requests versus limits:** requests drive scheduling and guarantee, limits cap
consumption. Exceeding a memory limit gets the container OOM-killed; exceeding a
CPU limit gets it throttled, not killed. That distinction gets asked.

```bash
kubectl get pods -n staging -o wide
kubectl describe pod eadge-ingest-7d9c -n staging      # events are at the bottom
kubectl logs -f deploy/eadge-ingest -n staging
kubectl logs pod-name --previous                       # the crashed instance
kubectl exec -it pod-name -- /bin/sh
kubectl rollout status deploy/eadge-ingest
kubectl rollout undo deploy/eadge-ingest               # rollback
kubectl get events -n staging --sort-by=.lastTimestamp
kubectl top pods
kubectl apply -f deployment.yaml
kubectl diff -f deployment.yaml                        # what would change
```

**Debugging a `CrashLoopBackOff`**, a likely scenario question: `describe` the
pod and read the events and the last exit code, `logs --previous` for the output
of the instance that died, then check the usual causes in order. Bad image tag
or pull secret, a missing ConfigMap or Secret, a failing liveness probe with too
short a delay, an OOM kill visible as exit code 137, a read-only filesystem the
app tries to write to, or the application simply exiting because a required
environment variable is absent.

## 6. Helm

**What problem it solves.** Kubernetes manifests are static YAML. You need the
same application deployed to lab, staging and production with different replica
counts, image tags, resource sizes and endpoints. Copying the YAML three times
means it drifts. Helm templates the manifests and manages the result as a
versioned **release** you can upgrade and roll back as a unit.

```
chart/
  Chart.yaml           # name, version, appVersion
  values.yaml          # defaults
  values-prod.yaml     # per-environment overrides
  templates/
    deployment.yaml
    service.yaml
    configmap.yaml
    _helpers.tpl       # shared template snippets
  charts/              # vendored dependencies
```

```yaml
# templates/deployment.yaml
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

```bash
helm lint ./chart
helm template ./chart -f values-prod.yaml     # render locally, review the diff
helm install eadge-ingest ./chart -n staging
helm upgrade --install eadge-ingest ./chart -n prod -f values-prod.yaml \
     --set image.tag=1.4.1 --wait --atomic --timeout 5m
helm history eadge-ingest -n prod
helm rollback eadge-ingest 3 -n prod
helm uninstall eadge-ingest -n prod
```

Two practices to name: **`helm template` and review the rendered diff before
upgrading a production release** rather than trusting the values file, and
**`--atomic`**, which rolls back automatically on a failed upgrade so you are
never left half-deployed.

If asked what you dislike about Helm, an honest and well-regarded answer is that
templating YAML with a text templating engine produces confusing failures,
whitespace bugs, and charts that are hard to review. Kustomize takes the
overlay approach instead. Both are in wide use.

## 7. Where this fits on a program like EADGE-T

Do not assume a cloud-native deployment on an operational air defense site.
Realistically:

- **Development and CI** almost certainly use containers, because reproducible
  builds and disposable test environments are exactly what the tech refresh is
  buying.
- **The operational deployment** may be containerized on-premises, may be
  virtual machines, or may still be bare metal with a formal installation
  procedure, depending on the accreditation baseline. Air-gapped operation is
  likely, which means a mirrored internal registry, no pulls from Docker Hub, and
  images that must be imported through a controlled process.
- **Kubernetes at the edge** in a disconnected environment is a real pattern but
  brings its own accreditation burden.

The best thing you can say here: *"I would not assume containers on the
operational side without knowing the accreditation baseline. Where I would push
hardest is in the build and test environments, because reproducible, disposable
test environments are the direct enabler for the automated test capability the
program wants."*

## 8. Questions to be ready for

1. Container versus VM. (Section 1.)
2. Why multi-stage builds? (Smaller, fewer CVEs, no build tooling at runtime.)
3. Why is layer order important? (Caching, section 3.)
4. `CMD` versus `ENTRYPOINT`? (`ENTRYPOINT` is the executable, `CMD` supplies
   default arguments; `CMD` alone is overridden entirely by `docker run` args.)
5. How do you get data out of a container? (Volumes and bind mounts; the
   writable layer is discarded when the container is removed.)
6. Liveness versus readiness probes. (Section 5.)
7. How do you handle secrets? (Not in the image, not in the repository. A secret
   store or Kubernetes Secrets with encryption at rest and RBAC, injected at
   runtime. See [lesson 13](cyber.html).)
8. What does Helm give you over plain manifests? (Section 6.)
9. How do you debug a pod that will not start? (Section 5.)
10. How would you run containers in an air-gapped environment? (Internal
    registry mirror, images imported through a controlled transfer, no external
    pulls, digest pinning, and a vulnerability scan on import.)
