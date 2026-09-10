# 9. Git, GitLab and Agile

The posting names Git, GitLab, Jira and Confluence in the basic qualifications,
and describes an Agile Scrum environment with "baseline merges, defect
resolution, peer reviews." That is a specific set of things to be fluent in.

## 1. Git you use every day

```bash
git status
git add -p                          # stage hunks selectively; do this more
git commit -m "Fix off-by-one in dwell window merge"
git log --oneline --graph --decorate --all
git diff                            # unstaged
git diff --staged                   # what you are about to commit
git show HEAD~2
git branch -vv                      # local branches and their upstreams
git switch -c feature/EADGE-1234-adapter-upgrade
git switch main
git fetch origin
git pull --ff-only origin main      # refuse a surprise merge commit
git push -u origin feature/EADGE-1234-adapter-upgrade
```

## 2. Git you use when something is wrong

This is the section that matters in an interview, because everyone can commit
and few can recover.

```bash
git restore path/file               # discard unstaged changes to a file
git restore --staged path/file      # unstage, keep the edit
git commit --amend                  # fix the last commit (only if unpushed)
git reset --soft HEAD~1             # undo the commit, keep changes staged
git reset --mixed HEAD~1            # undo the commit, keep changes unstaged
git reset --hard HEAD~1             # undo the commit and the changes. Destructive.
git revert <sha>                    # new commit that undoes an old one: safe on shared history
git stash push -m "wip adapter"; git stash list; git stash pop
git cherry-pick <sha>               # take one commit onto this branch
git reflog                          # your safety net: every HEAD you have had
```

Two rules to state clearly if asked:

- **`revert` on shared branches, `reset` only on your own unpushed work.**
  Rewriting published history forces everyone else to recover their checkout,
  which on a program with a dispersed team is a genuine disruption.
- **`git reflog` recovers almost anything** you thought you lost, including
  after a bad `reset --hard`, for as long as the reflog retention holds.

Finding the guilty change:

```bash
git log -S "correlationThreshold" --oneline    # commits that changed this string
git log -p path/to/file                        # full history of one file
git blame -L 40,80 path/to/file                # who wrote these lines, and when
git bisect start; git bisect bad; git bisect good v4.2.0
# git checks out midpoints; you test each and say good/bad
git bisect run ./scripts/repro_test.sh         # automated bisect
git bisect reset
```

`git bisect run` with a scripted reproducer is the answer to "how would you find
which of 400 commits introduced this regression." It is an excellent thing to
have ready.

## 3. Merge, rebase, and the baseline merge

**Merge** creates a commit with two parents, preserving what actually happened.
**Rebase** replays your commits onto a new base, producing a linear history but
rewriting your commit SHAs.

The defensible policy, and the one to state:

- Rebase your **own unpublished** feature branch onto the latest main to keep
  the history clean before review.
- **Merge** when integrating a shared or long-lived branch, especially a
  baseline. Never rebase a branch other people have based work on.

A **baseline merge**, as the posting uses the term, is bringing a long-lived
development line together with a configuration-controlled released baseline.
These are large, they touch files nobody has looked at in a year, and they are
where regressions hide. How to do one without wrecking your week:

```bash
git switch integration/baseline-5.2
git fetch origin
git merge --no-ff origin/develop        # explicit merge commit: the record matters
# ... resolve ...
git merge --continue
```

1. **Do it in a scratch clone first** to see the scale of the conflict set.
2. **Merge in the direction policy says**, and get agreement on that before
   starting, not after.
3. **Take the conflicts in batches by subsystem**, not file by file top to
   bottom, so you can hold the context.
4. **When a conflict is not obviously yours, find the author.** `git log` the
   region on both sides. A wrong resolution here is a silent behavior change on
   a fielded system.
5. **Never resolve by taking one side wholesale** to make the tool stop
   complaining. That is how a fix gets silently reverted.
6. **Run the full regression suite after**, not just the tests near your changes.
7. **Record what you decided.** Non-obvious resolutions belong in the merge
   commit message.

Conflict mechanics:

```bash
git status                          # unmerged paths
git diff --name-only --diff-filter=U
git checkout --ours path/file       # keep the target branch version
git checkout --theirs path/file     # keep the incoming version
git mergetool
git merge --abort                   # back out entirely and start over
git config merge.conflictstyle zdiff3    # shows the common ancestor too: much better
```

That last setting is a good detail. Three-way conflict markers with the base
version let you see what each side actually changed, instead of guessing.

## 4. Commits and reviews

Commit message format, which reviewers on regulated programs care about:

```
EADGE-1234: Bound the ingest queue and drop oldest on overflow

The ingest queue was unbounded. Under a sensor burst of >20k msg/s the
process grew until the OOM killer terminated it, losing the track picture.

Bound the queue at 50,000 detections and drop the oldest entry on overflow,
since a stale position report has no operational value. Emit a
detections_dropped_total counter so the condition is visible in monitoring.

Tested: new unit test reproduces the burst and asserts bounded memory plus a
non-zero drop count. Full regression suite passes on the 5.2 baseline.
```

Subject line under about 72 characters, imperative mood, ticket id, then a body
explaining **why**, not what. The diff already says what.

**Reviewing well** is part of a senior role, and they may ask what you look for:

- Does it do what the ticket says, and only that?
- Are the error paths handled, or only the happy path?
- What happens with empty, null, malformed, and enormous input?
- Are there tests, and would they actually fail if the code were wrong?
- Is anything logged that should not be? (Credentials, PII, full payloads.)
- Is a dependency added, and was that vetted? On this program that has license
  and CVE implications.
- Is it reversible? Can this be backed out cleanly if the lab finds a problem?
- Readability: would someone unfamiliar understand it in six months.

**Receiving review well** matters too. Answer every comment, even if only to say
you disagree and why. Do not take a stylistic note personally. If a discussion
runs past three round trips in comments, get on a call; on a dispersed team that
saves a day per exchange.

## 5. GitLab specifics

The posting names GitLab, so know its vocabulary as distinct from GitHub:

| Concept | GitLab term |
| --- | --- |
| Pull request | **Merge request** (MR) |
| Actions | **CI/CD pipelines**, defined in `.gitlab-ci.yml` |
| Runner | **GitLab Runner**, the agent executing jobs |
| Package hosting | **Package Registry**, **Container Registry** |
| Protected branches | Same, plus **push rules** and approval rules |
| Issue tracking | **Issues**, **Epics**, **Boards** |
| Merge checks | **Approval rules**, **Merge trains** |

Things worth being able to say: MRs can require N approvals and green pipelines
before merge; protected branches prevent force pushes; a merge train serializes
merges so each is tested against the result of the ones ahead of it; and
`CODEOWNERS` routes review to the right team automatically. Pipelines are
covered in [lesson 10](testing-ci.html).

## 6. Branching strategies

Be able to compare these, and to say which fits a program with formal baselines.

**Trunk-based development.** Everyone commits to main behind short-lived
branches, feature flags hide incomplete work, releases are cut from main.
Fastest feedback, requires strong automated testing.

**GitFlow.** `develop`, `release/*`, `hotfix/*`, `main`. Heavier, but it maps
naturally onto formal release baselines and long qualification cycles, which is
why defense programs often use something like it.

**Release branch per baseline.** A branch per fielded version, with fixes
cherry-picked back. This is common when several deployed baselines must be
maintained simultaneously, which is likely here.

The mature answer: *"the right strategy is the one that matches your release
cadence and your verification cost. If every release requires a lab
qualification campaign, trunk-based with continuous deployment is fiction, and
you want release branches. Where trunk-based ideas still pay off is in keeping
feature branches short and merging often, so integration pain stays small."*

## 7. Scrum mechanics

The posting says Agile Scrum with a dispersed team, so expect questions.

**Roles.** Product Owner owns the backlog and priority. Scrum Master facilitates
and removes impediments. The development team is cross-functional and
self-organizing.

**Artifacts.** Product backlog, sprint backlog, increment. Definition of Done.

**Events.**

| Event | Purpose | Common failure |
| --- | --- | --- |
| Sprint planning | Select and commit to sprint work | Committing to more than capacity, every time |
| Daily standup | Sync and surface blockers | Turns into a status report to the manager |
| Sprint review | Demo the increment to stakeholders | Nothing demonstrable was built |
| Retrospective | Improve the process | Same items raised every sprint, none actioned |
| Backlog refinement | Size and clarify upcoming work | Skipped, so planning takes three hours |

**Estimation.** Story points are relative sizing, not hours, and velocity is a
planning input for one team, not a productivity metric to compare teams. If an
interviewer asks about estimating, that distinction is the answer.

**Definition of Done** on a program like this is stricter than commercial:
code complete, unit tests written and passing, peer reviewed, static analysis
clean, merged, documentation and any CDRL artifact updated, and verified in the
integration environment. Being able to state that shows you understand where you
are.

**Kanban**, which the posting also names, is a pull system: continuous flow,
work-in-progress limits, and metrics of cycle time and throughput rather than
velocity. It suits sustainment and defect work better than Scrum's fixed sprints,
which is why teams often run a hybrid: Scrum for feature work, a Kanban lane for
incoming defects. Saying that shows practical experience.

## 8. Jira and Confluence

Enough vocabulary to sound like you have lived in them.

- **Issue types.** Epic, Story, Task, Sub-task, Bug. On defense programs also
  often a Change Request or Problem Report type tied to formal configuration
  management.
- **Workflow.** To Do, In Progress, In Review, In Test, Done, with transitions
  that may be enforced.
- **Fields that matter.** Fix version and affects version, which map to
  baselines; components; priority and severity, which are different things;
  linked issues (blocks, is blocked by, duplicates, relates to).
- **JQL**, which is worth knowing one line of:
  `project = EADGE AND status = "In Review" AND assignee = currentUser() ORDER BY updated DESC`
- **Confluence** holds design docs, meeting notes, runbooks, and onboarding.
  A good habit to mention: when you solve a hard integration problem, write the
  runbook page, because on a dispersed team the alternative is answering the
  same question at 3 a.m. in six months.

## 9. Working across time zones

This is not a soft topic for this job. You will be in the UAE and much of the
team will be in the United States, roughly eight to eleven hours behind. Have a
real answer.

- **Write, do not ping.** Anything that can be a written update should be. Async
  by default; a synchronous meeting is expensive when it costs somebody their
  evening.
- **Protect one overlap window** and spend it on the things that genuinely need
  conversation: design disagreements, ambiguous requirements, live debugging.
- **Never end your day with a blocked colleague.** Before you sign off, make
  sure anyone waiting on you has what they need, because your reply is otherwise
  a full day late.
- **Over-communicate state.** Update the ticket, not just the person. On a
  dispersed team, information in a direct message is information that is lost.
- **Rotate the pain.** If a recurring meeting is always painful for the same
  side, that is a fairness problem worth naming.

## 10. Exercise: do a real merge conflict

Twenty minutes, on your own machine. Do not skip it; conflict mechanics are much
harder to recall under observation than you expect.

```bash
mkdir /tmp/conflict-drill && cd /tmp/conflict-drill && git init
printf 'threshold = 0.5\nwindow = 30\n' > config.txt
git add . && git commit -m "Initial config"

git switch -c feature/raise-threshold
printf 'threshold = 0.8\nwindow = 30\n' > config.txt
git commit -am "Raise correlation threshold to 0.8"

git switch main
printf 'threshold = 0.6\nwindow = 60\n' > config.txt
git commit -am "Tune threshold and widen window"

git merge feature/raise-threshold        # conflict
git config merge.conflictstyle zdiff3
git merge --abort && git merge feature/raise-threshold   # now with base shown
cat config.txt                           # read all three sections
# resolve by hand to threshold = 0.8, window = 60
git add config.txt && git merge --continue
git log --oneline --graph
```

Then do it again with `git merge --abort`, with `--ours`, and with a rebase, so
all four paths are muscle memory.
