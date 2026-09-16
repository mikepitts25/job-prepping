# 9. The four-hour SDLC sprint

"Experience across the **full Software Development Life Cycle**" is a basic
qualification, and Agile methodologies and GitLab CI/CD are desired skills.
That sounds like a topic you read about. It is not. It is a set of mechanical
skills you either have in your fingers or do not, and four hours is enough to
put them there.

You will spend this sprint in a **real repository** doing real operations:
conflicting merges, recovering lost work, finding a bug across twelve commits
automatically, and writing a pipeline. Every command below was executed while
this lesson was written, and the outputs are the actual ones.

[Lesson 18](git-agile.html) and [lesson 19](testing-ci.html) are the
references. This is the sprint.

## The rules

1. **Type everything.** Git is muscle memory. Reading about `git reset` teaches
   you nothing.
2. **Use a scratch repository**, not anything you care about. You will
   deliberately destroy work.
3. **Run `git status` constantly.** It tells you where you are and what to do
   next. Beginners skip it and get lost.
4. **Run `git log --oneline --graph --all` after every branch operation.** Seeing
   the shape is how the model becomes intuitive.

## What I am cutting

| Cut | Why |
| --- | --- |
| Submodules, worktrees, LFS | Real, rare, and not day-one. |
| Jenkins in depth | GitLab is named on your req; [lesson 19](testing-ci.html) has Jenkins vocabulary. |
| Kubernetes deployment mechanics | [Lesson 8](docker-sprint.html) and [lesson 20](containers.html). |
| Requirements management tools (DOORS) | You need the vocabulary, which is in [lesson 1](program-brief.html). |
| Formal safety standards | Named in [lesson 19](testing-ci.html); not a four-hour topic. |

## Setup: two minutes

```bash
git --version
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global merge.conflictstyle zdiff3
git config --global init.defaultBranch main
```

That third line matters and almost nobody sets it. It is explained in hour two.

Start the clock.

---

## Hour 1: the model, and daily Git

### 0:00 to 0:20 — The mental model

Most Git confusion comes from not knowing what the pieces are. There are four
places a change can be:

```
  working tree  ->  staging area  ->  local repository  ->  remote
   (your edits)      (git add)         (git commit)        (git push)
```

- **Working tree**: the files as they are on disk right now.
- **Staging area** (or index): what will go into the next commit. This is the
  part other version control systems do not have, and it exists so you can
  commit *some* of your changes.
- **Local repository**: the committed history, on your machine.
- **Remote**: the shared copy, on GitLab or GitHub.

A **commit** is a snapshot of the whole tree plus a pointer to its parent. A
**branch is just a movable label pointing at a commit.** That sentence is the
key to everything: creating a branch is instant and free because it writes 40
bytes, and merging is about reconciling two chains of commits.

`HEAD` is a pointer to where you are now.

### 0:20 to 0:50 — The daily loop

```bash
mkdir gitdrill && cd gitdrill && git init -b main
echo "threshold = 0.5" > config.txt
git status                      # untracked
git add config.txt
git status                      # staged
git commit -m "Initial config"
git log --oneline
```

Now the commands you use every day:

```bash
git status                      # constantly
git add -p                      # stage hunk by hunk. Do this more.
git diff                        # unstaged changes
git diff --staged               # what you are about to commit
git commit -m "message"
git log --oneline --graph --decorate --all
git show HEAD~2                 # a specific commit
git blame -L 40,80 file         # who wrote these lines and when
```

**`git add -p` is the one to build a habit around.** It walks you through each
change and asks whether to stage it. It catches the debug statement you forgot,
and it produces commits that contain one idea instead of an afternoon.

**Commit messages.** On a programme with formal change control, reviewers care:

```
EADGE-1234: Bound the ingest queue and drop oldest on overflow

The ingest queue was unbounded. Under a sensor burst of >20k msg/s the
process grew until the OOM killer terminated it, losing the track picture.

Bound the queue at 50,000 detections and drop the oldest on overflow, since
a stale position report has no operational value. Emit a dropped counter so
the condition is visible in monitoring.

Tested: new unit test reproduces the burst and asserts bounded memory plus a
non-zero drop count.
```

Subject under about 72 characters, imperative mood, ticket id. The body
explains **why**, because the diff already says what.

### 0:50 to 1:00 — Undo, which is what actually matters

Anyone can commit. Few can recover. Type all of these.

```bash
git restore file                # discard unstaged changes to a file
git restore --staged file       # unstage, keep the edit
git commit --amend              # fix the last commit (ONLY if unpushed)
git reset --soft HEAD~1         # undo the commit, keep changes staged
git reset --mixed HEAD~1        # undo the commit, keep changes unstaged
git reset --hard HEAD~1         # undo the commit AND the changes. Destructive.
git revert <sha>                # a NEW commit undoing an old one
git stash push -m "wip"; git stash list; git stash pop
git reflog                      # every position HEAD has held
```

**Two rules to state in an interview:**

**`revert` on shared history, `reset` only on your own unpushed work.**
Rewriting published history forces everyone else to repair their checkout,
which on a dispersed team is a genuine disruption.

**`git reflog` recovers almost anything**, including after a bad
`reset --hard`, for as long as the reflog retention holds. It is the safety net
that makes the rest survivable.

**Do now, five minutes.** Deliberately lose work and get it back:

```bash
echo "important" >> config.txt && git commit -qam "Important change"
git reset --hard HEAD~1         # it is gone
git log --oneline               # confirm: gone
git reflog                      # find the sha of "Important change"
git reset --hard <that-sha>     # it is back
```

Doing that once removes the fear permanently. **Five minutes off.**

---

## Hour 2: branching, conflicts, and finding bugs

### 1:00 to 1:25 — Branching and merging

```bash
git switch -c feature/raise-threshold     # create and switch
# ... edit, commit ...
git switch main
git merge feature/raise-threshold
git branch -d feature/raise-threshold
```

**Merge versus rebase**, which gets asked constantly:

- **Merge** creates a commit with two parents. History shows what actually
  happened.
- **Rebase** replays your commits onto a new base. History is linear, but your
  commits get new SHAs, which means it is rewriting.

The defensible policy: **rebase your own unpublished branch** to tidy it before
review; **merge when integrating anything shared**. Never rebase a branch other
people have based work on.

### 1:25 to 1:55 — A conflict, for real

Do this exactly. It is the highest-value drill in the sprint.

```bash
mkdir /tmp/conflict && cd /tmp/conflict && git init -q -b main
git config merge.conflictstyle zdiff3
printf 'threshold = 0.5\nwindow = 30\n' > config.txt
git add . && git commit -qm "Initial config"

git switch -qc feature/raise-threshold
printf 'threshold = 0.8\nwindow = 30\n' > config.txt
git commit -qam "Raise correlation threshold to 0.8"

git switch -q main
printf 'threshold = 0.6\nwindow = 60\n' > config.txt
git commit -qam "Tune threshold and widen window"

git merge feature/raise-threshold
```

```
Auto-merging config.txt
CONFLICT (content): Merge conflict in config.txt
Automatic merge failed; fix conflicts and then commit the result.
```

```bash
cat config.txt
```

```
<<<<<<< HEAD
threshold = 0.6
window = 60
||||||| b219389
threshold = 0.5
window = 30
=======
threshold = 0.8
window = 30
>>>>>>> feature/raise-threshold
```

**This is why `merge.conflictstyle zdiff3` matters.** The middle section is the
**common ancestor**: what the file looked like before either side touched it.
With the default two-way markers you see only the two final states and have to
guess what each side changed. Here you can read it directly: main changed
threshold 0.5 to 0.6 and window 30 to 60; the branch changed threshold 0.5 to
0.8 and left window alone.

So the correct resolution is `threshold = 0.8` and `window = 60`: take the
branch's threshold and main's window. **Neither "ours" nor "theirs" wholesale
would be right**, and that is the lesson.

```bash
printf 'threshold = 0.8\nwindow = 60\n' > config.txt
git add config.txt
git merge --continue
git log --oneline --graph
```

The rules for real conflicts, especially a **baseline merge** where a long
development line meets a configuration-controlled release:

- **Never resolve by taking one side wholesale** just to make the tool stop
  complaining. That is how a fix gets silently reverted and nobody notices for
  a year.
- **Take them in batches by subsystem**, not file by file top to bottom, so you
  can hold the context.
- **When a conflict is not obviously yours, find both authors.**
- **Run the full regression suite afterwards**, not just tests near your
  changes. The risk in a baseline merge is the interaction you did not think
  about.
- **Record non-obvious resolutions in the merge commit message.**

```bash
git merge --abort          # back out entirely and start again
git checkout --ours file   # take the target branch's version
git checkout --theirs file # take the incoming version
```

### 1:55 to 2:00 — Finding the commit that broke it

This is the party trick that is also genuinely useful. You have twelve commits
and something broke somewhere in the middle.

Write a script that exits 0 when things are good and non-zero when broken:

```bash
cat > test.sh <<'EOF'
#!/bin/sh
python3 -c "
from calc import average
assert average([2, 4]) == 3.0, 'wrong average'
"
EOF
chmod +x test.sh
```

Then:

```bash
git bisect start HEAD HEAD~11     # HEAD is bad, eleven back was good
git bisect run ./test.sh
```

```
Bisecting: 2 revisions left to test after this (roughly 2 steps)
Bisecting: 0 revisions left to test after this (roughly 1 step)
Bisecting: 0 revisions left to test after this (roughly 0 steps)
9bb1db833aa7d7baf7631b6f7b29ac20f6296cf3 is the first bad commit
```

```bash
git bisect reset
```

**Three steps to search twelve commits**, because it is a binary search. Over
four hundred commits it is nine. This is the answer to "how would you find
which change introduced this regression," and being able to say `git bisect
run` with a scripted reproducer is a strong senior signal.

**Five minutes off.**

---

## Hour 3: the rest of the lifecycle

### 2:00 to 2:20 — What "full SDLC" actually means

The phrase on your req means you have lived the whole loop, not just the coding
part. Be able to name the phases and what you do in each:

| Phase | What happens | Your part |
| --- | --- | --- |
| **Requirements** | Systems engineering owns what the system shall do | Ask what a requirement is protecting against; make it verifiable |
| **Design** | Architecture and interfaces agreed | Raise ambiguity early; it is free now and expensive later |
| **Implementation** | Code | Small commits, peer review |
| **Verification** | Does it meet the requirement? | Unit, integration, lab |
| **Validation** | Does it meet the *need*? | Customer demonstration |
| **Deployment** | Into the field | Release notes, rollback plan |
| **Sustainment** | Defects, obsolescence, security | Most of this job |

The two sentences worth having ready:

**Traceability** is the thread from a requirement, to the code that implements
it, to the test that verifies it. On an accredited system that thread is
auditable, and a change that breaks it will be rejected.

**Cost of change rises steeply through the phases.** A requirement ambiguity
resolved in analysis costs a conversation. The same ambiguity discovered in
integration costs a lab campaign. That is the argument for raising things
early, and it is why "I flagged it in week one" is the answer to most process
questions.

**Agile in this setting.** Scrum with two-week sprints, a product owner who
owns priority, a definition of done stricter than commercial (code complete,
unit tested, peer reviewed, static analysis clean, merged, documentation and
CDRL artifacts updated, verified in the integration environment). Story points
are relative sizing and velocity is a planning input for one team, not a
productivity metric to compare teams. Many teams run a Kanban lane alongside
for incoming defects, because fixed sprints suit feature work and flow suits
sustainment.

### 2:20 to 2:50 — Code review

Reviewing well is a senior skill and they will ask what you look for.

**As an author:**

- Keep it small. Under about four hundred lines gets read; two thousand gets
  rubber-stamped.
- The description says **why**, and what you tested.
- Separate refactoring from behaviour change into different commits, so a
  reviewer can tell them apart and a revert is surgical.
- Answer every comment, even if only to disagree with a reason.

**As a reviewer**, the checklist:

- Does it do what the ticket says, and only that?
- Are the error paths handled, or only the happy path?
- What happens with empty, null, malformed and enormous input?
- Are there tests, and **would they actually fail if the code were wrong**?
- Is anything logged that should not be: credentials, personal data, full
  payloads?
- Is a dependency added, and was that vetted for licence and CVEs?
- Is it reversible if the lab finds a problem?
- Would someone unfamiliar understand it in six months?

**Distinguish blocking issues from preferences explicitly.** A reviewer who
marks style opinions as blocking trains people to dread review, and then you
stop getting early reviews, which is when review is cheapest.

**After two or three rounds of comments, get on a call.** With a time-zone gap
each round costs a day.

### 2:50 to 3:00 — Branching strategy

Know these three and which fits here:

- **Trunk-based**: everyone on main behind short-lived branches, features
  hidden by flags. Fastest feedback, demands strong automated testing.
- **GitFlow**: `develop`, `release/*`, `hotfix/*`, `main`. Heavier, maps onto
  formal release baselines, which is why defence programmes often use something
  like it.
- **Release branch per baseline**: a branch per fielded version, fixes
  cherry-picked. Common when several deployed baselines are maintained at once,
  which is likely here.

The mature answer: *"the right strategy matches your release cadence and your
verification cost. If every release needs a lab qualification campaign, then
continuous deployment is fiction and you want release branches. What still pays
off from trunk-based thinking is keeping branches short and merging often, so
integration pain stays small."*

**Five minutes off.**

---

## Hour 4: the pipeline

### 3:00 to 3:20 — What CI actually buys

**Continuous integration** means every change is automatically built and tested
on a shared machine, not just on the author's laptop.

The argument to make, and it is the same economic one as
[lesson 4](python-sprint.html): on a programme like this, **the integration lab
is the scarcest resource there is.** Every defect the pipeline catches is a lab
slot you did not consume and a week you did not lose. That is what the posting
means by automated test capability improving deployment efficiency. Framing it
as economics rather than hygiene is the senior version.

**Continuous delivery** means every change that passes is *deployable*.
**Continuous deployment** means it is automatically deployed. On an accredited
system you do delivery, not deployment: the pipeline stops at a human gate.

### 3:20 to 3:50 — Write a pipeline

Create `.gitlab-ci.yml`:

```yaml
stages: [lint, test, build, scan, deploy]

default:
  image: python:3.11-slim
  cache:
    key:
      files: [requirements.txt]
    paths: [.cache/pip]

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  IMAGE: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"

lint:
  stage: lint
  script:
    - pip install ruff
    - ruff check .

unit-tests:
  stage: test
  script:
    - pip install -r requirements.txt -r requirements-dev.txt
    - pytest -q --junitxml=report.xml --cov=. --cov-report=xml
  coverage: '/^TOTAL.*\s+(\d+%)$/'
  artifacts:
    when: always
    reports:
      junit: report.xml

build-image:
  stage: build
  image: docker:27
  services: [docker:27-dind]
  script:
    - docker build -t "$IMAGE" .
    - docker push "$IMAGE"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

dependency-scan:
  stage: scan
  script:
    - pip install pip-audit
    - pip-audit --strict -r requirements.txt

deploy-staging:
  stage: deploy
  environment:
    name: staging
  script:
    - ./deploy.sh staging "$IMAGE"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  stage: deploy
  environment:
    name: production
  when: manual
  script:
    - ./deploy.sh production "$IMAGE"
  rules:
    - if: $CI_COMMIT_TAG
```

Now the principles, each of which you should be able to state:

**Fast feedback first.** Lint before tests, tests before the image build. A
developer should know within three minutes.

**Build once, promote the same artifact.** The image is built once and tagged
by commit SHA, and that exact image is what goes to staging and then
production. **Never rebuild between test and deploy**, or you have shipped
something you did not test. This is the single most important CI principle;
say it emphatically.

**Tag by commit SHA, never `latest`.** Traceability from a running container
back to a commit.

**`rules` control cost.** The image build and deploys only happen on the
default branch; scans do not run on every push to every branch.

**A manual gate before production.** On an accredited system the pipeline stops
at a human decision.

**`artifacts: when: always`** so the test report is published even when tests
fail. A failed job whose report was not uploaded is a job you have to re-run to
understand.

**Cache keyed on `requirements.txt`.** Same layer-ordering logic as
[lesson 8](docker-sprint.html): dependencies change rarely, source changes
constantly.

### 3:50 to 3:57 — Quality gates on legacy code

The practical problem nobody warns you about: you turn on a linter or a scanner
for the first time on a ten-year-old codebase and get four thousand findings.

**Do not try to fix them all, and do not turn the gate off.** Baseline the
existing findings, block anything *new*, and burn the backlog down
deliberately. Otherwise the gate gets disabled within a week and you have lost
it permanently.

The same applies to coverage: set a floor at wherever you are and require that
it not regress, rather than mandating eighty percent on day one.

And the rule from [lesson 19](testing-ci.html) that matters most: **a flaky
test is an emergency, not an annoyance.** One flaky test teaches the whole team
to re-run the pipeline instead of reading the failure, and from that moment the
suite protects nothing. Quarantine with a ticket, an owner and a deadline, then
fix the root cause. A retry is not a fix.

### 3:57 to 4:00 — Self-test

From memory:

1. The four places a change can live, and the command moving it between each.
2. When to use `revert` and when `reset`, and why.
3. What `git reflog` is for.
4. Why `merge.conflictstyle zdiff3` is better than the default.
5. How to find which of four hundred commits broke something.
6. Why you must not rebuild the artifact between test and deploy.
7. What to do when a new linter reports four thousand findings.

## What you can honestly claim

**Say:** you work comfortably in Git including conflict resolution, history
recovery and bisect; you review code against a real checklist; you understand
the full lifecycle from requirement through sustainment and why traceability
matters on an accredited system; and you can write and explain a CI/CD pipeline
including artifact promotion and quality gates.

**Be honest** about which CI system you have used. The concepts transfer
completely between GitLab, Jenkins and GitHub Actions, and saying "I have built
pipelines in X; the stages and the build-once principle are the same" is a
fine answer.

## If you get another four hours

1. **[Lesson 18](git-agile.html)** for GitLab specifics and Agile mechanics.
2. **[Lesson 19](testing-ci.html)** for the testing pyramid and Jenkins.
3. **Put a real pipeline on a real repository.** This site has one; read
   `.github/workflows/pages.yml` in the prep repo, which gates publication on a
   staleness check and a link check.
4. **Do the conflict drill three more times**, with `--abort`, with `--ours`,
   and with a rebase, so all four paths are muscle memory.
5. **Bisect a real bug** in a repository you know.
