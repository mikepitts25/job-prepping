# 8. The four-hour Docker sprint

"Familiarity with **Docker**, REST APIs, or SOAP" is a basic qualification, and
Docker also appears in the desired skills alongside Kubernetes and Helm. Four
hours gets you from nothing to a hardened, multi-stage image you can defend in
a review.

We containerise **the API you built in [lesson 7](apis-sprint.html)**. If you
skipped that sprint, any small Flask app or the Python tool from
[lesson 4](python-sprint.html) works; the Dockerfile barely changes.

[Lesson 20](containers.html) is the reference. This is the sprint.

**One honesty note.** The command outputs shown below are representative rather
than captured, because the environment this lesson was written in had the
Docker client but no daemon. The Dockerfile and compose file were validated
structurally, and the application inside them was run under gunicorn exactly as
the container runs it. Everything else you will verify yourself as you go,
which is the point of a sprint.

## The rules

1. **Type everything.**
2. **Build and run after every change.** The loop is fast; use it.
3. **Read the build output.** It tells you which layers were cached. That is
   the single most useful feedback Docker gives you.
4. **Break things on purpose** where I say so.

## What I am cutting

| Cut | Why |
| --- | --- |
| Kubernetes beyond vocabulary | A sprint of its own. [Lesson 20](containers.html) has what you need to talk about it. |
| Helm | Same. |
| Swarm, Nomad | Not on your req. |
| Networking internals (bridge, overlay) | You need port publishing and compose, not CNI. |
| Writing base images from scratch | You will consume approved bases, not build them. |
| BuildKit cache mounts, buildx | Real, but not day-one. |

## Setup: five minutes, before the clock

```bash
docker --version          # any recent version
docker run --rm hello-world
```

If that second command prints a greeting, you have a working daemon. If it
says it cannot connect to the Docker daemon, start Docker Desktop or
`sudo systemctl start docker` before going further.

Start the clock.

---

## Hour 1: what a container is, and driving one

### 0:00 to 0:20 — The concept

Learn this definition properly, because it is the most common interview
question on the topic and most candidates answer it vaguely:

> A container is a **normal Linux process**, isolated using kernel features
> rather than virtualised. **Namespaces** give it its own view of the process
> table, network stack, mounts, hostname and users. **cgroups** limit what it
> can consume in CPU, memory and I/O. Its filesystem comes from a stack of
> read-only image layers with a thin writable layer on top. There is no guest
> operating system and no guest kernel, which is why it starts in milliseconds.

**Container versus virtual machine**, the inevitable follow-up: a VM
virtualises hardware and runs its own kernel, giving stronger isolation at the
cost of size and startup time. A container shares the host kernel. The security
consequence is real: kernel isolation is weaker than hypervisor isolation,
which is why high-assurance environments often still run containers *inside*
VMs.

**Image versus container**: the image is the immutable template, the container
is a running instance of it. Same relation as a class and an object.

**Why anyone bothers**, stated as the thing the posting cares about: an image
is a **reproducible unit**. The same bytes run identically on a developer
laptop, in CI, and on a server. That kills "works on my machine," and it is the
direct enabler for the disposable test environments a tech refresh needs.

### 0:20 to 0:50 — Driving containers

```bash
docker run --rm -it python:3.11-slim bash
```

You are now inside a container, at a shell, with Python 3.11. Try:

```bash
python -V
ls /
cat /etc/os-release
exit
```

You just ran a different Linux distribution in about a second without
installing anything. That is the demonstration; sit with it for a moment.

The flags matter:

- `--rm` deletes the container when it exits. Without it you accumulate dead
  containers forever.
- `-it` gives you an interactive terminal.

The commands you will use daily:

```bash
docker run -d --name api -p 8080:8080 myimage:1.0   # detached, with a port published
docker ps                        # running containers
docker ps -a                     # including stopped ones
docker logs -f api               # follow the output
docker exec -it api sh           # a shell INSIDE a running container
docker inspect api               # everything, as JSON
docker stats                     # live CPU and memory
docker stop api && docker rm api
docker images                    # local images
docker rmi myimage:1.0
docker system df                 # what is using disk
docker system prune -a           # reclaim it. Careful.
```

**`-p 8080:8080` is host port to container port.** Getting the order backwards
is the most common beginner mistake. The container's network is its own;
without publishing, nothing outside can reach it.

**`docker exec -it <name> sh` is your debugging lifeline.** When a container
misbehaves, get a shell inside it and look.

### 0:50 to 1:00 — Checkpoint

**Do now.**

1. Run `nginx` detached with `-p 8080:80`, load `http://localhost:8080`, then
   `docker logs` it and watch your own request appear.
2. `docker exec -it` into it and `ls /usr/share/nginx/html`.
3. Stop and remove it.
4. Now run it **without** `-p` and try the browser again. Nothing. That is
   network isolation, and understanding it now saves an hour later.

**Five minutes off.**

---

## Hour 2: your first image

### 1:00 to 1:20 — A naive Dockerfile

A **Dockerfile** is a recipe. Each instruction creates a **layer**.

In your API directory, create `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /opt/app
COPY . .
RUN pip install flask gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "api:app"]
```

```bash
docker build -t trackapi:0.1 .
docker run --rm -p 8080:8080 trackapi:0.1
curl localhost:8080/health/ready
```

It works. It is also wrong in five ways, and the rest of this sprint is fixing
each one.

The instructions:

**`FROM`** picks the base image. Everything starts from something.
**`WORKDIR`** sets the directory for what follows, and creates it.
**`COPY src dest`** copies from your machine into the image.
**`RUN`** executes a command **at build time**, and the result is baked in.
**`CMD`** is what runs **at container start**. It is not executed during build.

**`RUN` versus `CMD` is a real interview question.** Build time versus run
time.

### 1:20 to 1:45 — Layer caching, the thing that makes builds fast

Change one character in `api.py` and rebuild. Watch the output: it reinstalls
Flask. Every time. That is because `COPY . .` comes before `RUN pip install`,
so changing any source file invalidates the install layer and everything after
it.

**Docker caches layers and reuses them until something changes. A change
invalidates that layer and every layer after it.** Therefore: **order
instructions from least to most frequently changed.**

```dockerfile
FROM python:3.11-slim
WORKDIR /opt/app

COPY requirements.txt .                      # changes rarely
RUN pip install --no-cache-dir -r requirements.txt

COPY api.py client.py ./                     # changes constantly

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "api:app"]
```

with

```
flask==3.0.3
gunicorn==23.0.0
```

in `requirements.txt`.

Rebuild twice, changing `api.py` between them. The second build reuses the
install layer and finishes in about a second.

**This is the single highest-value Docker skill**, because it is the difference
between a two second and a two minute inner loop, and between a pipeline that
takes three minutes and one that takes twenty.

**Pin exact versions.** `flask==3.0.3`, never `flask`. An unpinned build pulls
something different next week and is therefore not reproducible. On a
configuration-controlled programme reproducibility is a requirement, not a
preference.

### 1:45 to 2:00 — .dockerignore

Create `.dockerignore`:

```
.git
.venv
__pycache__/
*.pyc
.pytest_cache/
node_modules/
*.md
```

Everything in the directory is sent to the daemon as **build context** before
the build starts. Without this, you ship your `.git` directory and your
virtualenv into the build, which is slow and can leak things.

**Do now.** Run `docker build` and read the first line: `transferring context`.
Add and remove `.dockerignore` and compare the size. **Five minutes off.**

---

## Hour 3: an image you would defend in a review

### 2:00 to 2:40 — Multi-stage, non-root, healthcheck

This is the version that matters. Type it.

```dockerfile
# ---- build stage --------------------------------------------------------
FROM registry.access.redhat.com/ubi9/python-311 AS build
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- runtime stage ------------------------------------------------------
FROM registry.access.redhat.com/ubi9/python-311-minimal

COPY --from=build /install /usr/local
WORKDIR /opt/app
COPY api.py client.py ./

USER 1001

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 LOG_LEVEL=INFO

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8080/health/ready').status==200 else 1)"

ENTRYPOINT ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8080", "api:app"]
```

Every choice is defensible, and being able to defend them is exactly what a
reviewer probes:

**Multi-stage build.** Compilers and build tooling live in the first stage and
never reach the runtime image. Only `/install` is copied forward. Smaller
image, smaller attack surface, fewer CVEs to remediate for the life of the
programme.

**UBI base image.** Red Hat Universal Base Images are the natural choice on a
RHEL programme: same package ecosystem, redistributable, and supported for
vulnerability remediation. On a defence programme you will likely be required
to use an approved, already-hardened base rather than picking your own.

**`USER 1001`.** The container does not run as root. This is a hard requirement
in any hardened environment and usually an explicit control. **This is the
first thing a reviewer looks for.**

**`ENV PYTHONUNBUFFERED=1`.** Without it, Python buffers stdout and your logs
appear late or not at all when the container dies. A small line that saves real
debugging pain.

**`HEALTHCHECK`.** The orchestrator needs to distinguish "the process is
running" from "the service works." Without one, a hung process looks healthy
forever.

**`ENTRYPOINT` in exec form**, the JSON array. In exec form the process is PID 1
and receives signals, so `docker stop` shuts it down gracefully. In shell form
it runs under `/bin/sh -c`, signals go to the shell, and your process is killed
after the timeout instead of cleaning up.

**gunicorn, not `flask run`.** The Flask development server is single-threaded
and not hardened. Saying this unprompted is a good signal.

```bash
docker build -t trackapi:1.0 .
docker run --rm -p 8080:8080 trackapi:1.0
docker inspect --format '{{.State.Health.Status}}' <container>
```

### 2:40 to 3:00 — Configuration, data, and compose

**Never bake configuration or secrets into an image.** An image is a shareable
artifact; anything inside it travels everywhere it goes, and `docker history`
will show it.

```bash
docker run -e LOG_LEVEL=DEBUG -e DATABASE_URL=... trackapi:1.0
docker run --env-file ./local.env trackapi:1.0
```

**The writable layer dies with the container.** Anything you need to keep goes
in a volume:

```bash
docker run -v trackdata:/var/lib/app trackapi:1.0        # named volume
docker run -v "$PWD/logs:/opt/app/logs" trackapi:1.0      # bind mount
```

For several services at once, `compose.yaml`:

```yaml
services:
  api:
    build: .
    ports: ["8080:8080"]
    environment:
      LOG_LEVEL: DEBUG
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8080/health/ready').status==200 else 1)"]
      interval: 10s
      timeout: 3s
      retries: 3
    depends_on:
      db:
        condition: service_healthy

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

```bash
docker compose up --build
docker compose logs -f api
docker compose down -v
```

**`condition: service_healthy` rather than plain `depends_on`.** Plain
`depends_on` waits for the container to *start*, not to be *ready*, so your app
races the database and fails on first connect. This is a very common bug and a
good thing to know.

The value to state: **a new engineer on a dispersed team gets a working
environment with one command** instead of a two-day setup document. On a
programme with people in several time zones that is a real productivity
argument.

**Five minutes off.**

---

## Hour 4: shipping, security and debugging

### 3:00 to 3:20 — Tags, digests and registries

```bash
docker tag trackapi:1.0 registry.internal/eadge/trackapi:1.4.0
docker push registry.internal/eadge/trackapi:1.4.0
docker pull registry.internal/eadge/trackapi@sha256:abc123...
```

**Never deploy `:latest`.** A tag is a mutable pointer: it can be moved to
different content. `latest` means "whatever someone pushed most recently,"
which makes a deployment untraceable and unrepeatable.

**Tag by version and by commit.** `1.4.0` for humans, the commit SHA for
traceability. Then anyone can map a running container back to the exact source.

**Pin by digest for production.** `@sha256:...` is content-addressed and cannot
be moved. That is the only way to be certain what you deployed.

### 3:20 to 3:40 — Security and the air-gapped reality

```bash
docker scout cves trackapi:1.0        # or: trivy image trackapi:1.0
docker history trackapi:1.0           # what each layer added
```

The rules, which map directly onto [lesson 22](cyber.html):

- **Non-root, always.** And `--read-only` with a writable volume for anything
  that genuinely needs to write.
- **Drop capabilities**: `--cap-drop ALL`, adding back only what is needed.
- **No secrets in the image.** Not in `ENV`, not in a `COPY`ed file, not in a
  `RUN` that is later deleted: earlier layers still contain it and
  `docker history` reveals it.
- **Smaller is safer.** Every package in the image is something you must
  monitor, scan and patch for the life of the programme.
- **Scan on build and on a schedule.** A clean image today is not a clean image
  in three months; the image did not change, the vulnerability database did.

**The air-gapped reality on a programme like this**, which is worth raising
unprompted:

- No pulls from Docker Hub. Everything comes from an **internal registry
  mirror** whose contents were reviewed and scanned on entry.
- Images arrive through a controlled transfer, often as `docker save` tar
  archives, and are imported.
- Approved hardened base images are mandated rather than chosen.
- **The hardened base may be missing something your application assumes**, and
  finding that out is engineering work, not a ticket for someone else.

### 3:40 to 3:55 — Debugging containers

The scenarios, in the order you will meet them:

**It exits immediately.**

```bash
docker ps -a                       # see the exit code
docker logs <container>
```

Exit code 0 usually means the main process finished, often because you ran a
command that returns rather than a server. Exit code 137 is an out-of-memory
kill. Exit code 126 or 127 means the entrypoint was not executable or not
found.

**It builds but the app cannot be reached.**

Check in this order: did you publish the port with `-p`; is the app bound to
`0.0.0.0` and not `127.0.0.1` (**binding to localhost inside a container means
only the container can reach it**, and this is the single most common cause);
is the port in the app the same as the one you published.

**The build fails at a `COPY`.** The file is outside the build context or
excluded by `.dockerignore`.

**It works for you and fails in CI.** Different base image tag pulled at a
different time, missing build context, or a file that exists locally and is not
in git.

**Get inside and look.**

```bash
docker exec -it <container> sh
docker run --rm -it --entrypoint sh trackapi:1.0     # bypass the entrypoint
```

That second one is the trick worth remembering: when the container will not
stay up, override the entrypoint and get a shell so you can look around the
filesystem the image actually produced.

### 3:55 to 4:00 — Self-test

From memory:

1. Define a container in terms of namespaces, cgroups and layers.
2. Why does `COPY requirements.txt` come before `COPY api.py`?
3. Three reasons for a multi-stage build.
4. Why `ENTRYPOINT ["a","b"]` rather than `ENTRYPOINT a b`?
5. Why is `:latest` wrong in production, and what do you use instead?
6. The app is up but unreachable. Name three causes.

## What you can honestly claim

**Say:** you write multi-stage Dockerfiles that run as a non-root user with
pinned dependencies, healthchecks and layer ordering for cache efficiency; you
use compose for multi-service local environments; you understand tagging,
digests, image scanning and the constraints of an air-gapped registry.

**Do not claim** production Kubernetes operations experience unless you have
it. Say you understand the model and would expect a ramp.

## If you get another four hours

1. **[Lesson 20](containers.html)** for Kubernetes and Helm vocabulary.
2. **Add a CI job** that builds and scans the image. See
   [lesson 9](sdlc-sprint.html).
3. **Get the image under 150 MB** and record what each change saved.
4. **Run it read-only** with `--read-only --cap-drop ALL` and fix what breaks.
5. **Rebuild the Dockerfile from empty** without looking.
