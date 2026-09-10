# 14. Cybersecurity and sustainment

The posting says the Tech Refresh delivers "foundational cybersecurity
enhancements" and that you will be "integrating COTS and FOSS updates." You will
be interviewed by or alongside a cybersecurity engineer. You do not need to be
one. You need to demonstrate that you treat security as part of engineering
rather than as somebody else's checklist.

## 1. The vocabulary

| Term | Meaning |
| --- | --- |
| **RMF** | Risk Management Framework: the NIST process that produces an authorization |
| **ATO** | Authority to Operate, the accreditation permitting operational use |
| **cATO** | Continuous ATO, where a compliant pipeline continuously evidences controls |
| **STIG** | Security Technical Implementation Guide: DISA hardening configuration |
| **SRG** | Security Requirements Guide, the generic form a STIG specializes |
| **SCAP / OpenSCAP** | Automated scanning of a host against a hardening benchmark |
| **CVE** | A specific published vulnerability identifier |
| **CVSS** | The 0&ndash;10 severity score attached to a CVE |
| **KEV** | CISA's Known Exploited Vulnerabilities catalog: exploited in the wild |
| **POA&M** | Plan of Action and Milestones: an accepted finding with a remediation plan |
| **SBOM** | Software Bill of Materials, the inventory of everything you ship |
| **SCA** | Software Composition Analysis, matching your SBOM against advisories |
| **SAST / DAST** | Static / dynamic application security testing |
| **IAVA** | Information Assurance Vulnerability Alert, a mandated remediation with a deadline |
| **Air gap** | No connection to external networks; everything arrives by controlled transfer |

## 2. The dependency upgrade question

This is the single most predictable technical question for this posting, in some
form: *"A library you depend on has a critical CVE. Walk me through what you
do."* Have this answer ready and structured.

**1. Establish the facts before reacting.**

- Which exact version are we on, in which components, in which baselines? An
  SBOM answers this in seconds; without one you are grepping.
- Is the vulnerable code path actually reachable from our usage? A
  deserialization CVE in a library we only use for formatting may not be
  exploitable here. That determination is made carefully, documented, and
  reviewed, not asserted to avoid work.
- What is the exposure? An internet-facing service and an air-gapped subsystem
  have very different risk, even for the same CVE.
- Is it on the KEV catalog, and is there a mandated deadline such as an IAVA?
  That changes the schedule from "prioritized" to "required by this date."

**2. Choose the response.**

- **Upgrade** to a fixed version. First choice.
- **Backport the patch** if upgrading is blocked by a breaking API change and
  the schedule cannot absorb it. Costs you a fork to maintain, so document it.
- **Mitigate** by configuration, by disabling the feature, or by a network
  control, then remediate properly on a plan.
- **Accept with a POA&M** when the risk is genuinely low and the fix is
  genuinely expensive. This is a decision with a named owner and a date, not a
  way of ignoring it.

**3. Do the upgrade properly.**

```bash
mvn dependency:tree -Dincludes=org.example:vulnerable-lib   # where did it come from?
pip-audit -r requirements.txt
mvn org.owasp:dependency-check-maven:check
```

- Find out whether it is a direct or a transitive dependency. If transitive, the
  right fix is usually upgrading the parent, not pinning an override, though an
  override is a legitimate stopgap.
- Read the changelog between your version and the target for behavior changes,
  not just API changes. Behavior changes are what break a fielded system.
- Upgrade one dependency at a time in its own merge request. When something
  breaks in the lab three weeks later, you want a small reversible commit, not a
  forty-library bump.
- Run the full regression suite, not the subset near the change. If coverage is
  thin, this is exactly where you invest in the characterization tests from
  [lesson 11](testing-ci.html).
- Regenerate the SBOM and re-scan.

**4. Close the loop.** Update the record so the finding is demonstrably closed,
and note anything that would make the next upgrade cheaper.

**5. Prevent the recurrence.** Continuous dependency scanning in the pipeline so
you learn about the next one on the day it publishes. And a deliberate policy on
staying current: a library four major versions behind is not stable, it is
accumulating an upgrade you will eventually be forced to do under a deadline.
That last sentence is a good one to say out loud, because it reframes patching
as risk management rather than chores.

## 3. Secure coding, the practical list

You will not be quizzed on OWASP rankings, but you should not write obviously
unsafe code in a live exercise.

**Injection.** Parameterize queries. Never build SQL or a shell command by
string concatenation with untrusted input.

```python
cur.execute("SELECT * FROM tracks WHERE id = %s", (track_id,))    # right
cur.execute(f"SELECT * FROM tracks WHERE id = '{track_id}'")      # wrong

subprocess.run(["grep", pattern, path], check=True)               # right
subprocess.run(f"grep {pattern} {path}", shell=True)              # wrong
```

**Deserialization.** Never deserialize untrusted data into arbitrary objects.
Python's `pickle` and Java's native serialization both allow code execution.
Use a data-only format and validate against a schema.

```python
yaml.safe_load(text)     # right
yaml.load(text)          # wrong: can construct arbitrary objects
```

**XML.** External entity expansion (XXE) and billion-laughs expansion are real
and appear in exactly the kind of legacy message parsing this program has.
Disable external entities and DTDs; use `defusedxml` in Python; set the secure
processing feature in Java parsers.

**Path traversal.** Validate that a resolved path stays inside its intended
root.

```python
base = pathlib.Path("/opt/eadge/data").resolve()
target = (base / user_supplied).resolve()
if not target.is_relative_to(base):
    raise ValueError("path escapes data directory")
```

**Secrets.** Never in source, never in a container image, never in a log line,
never in a ticket. Environment variables injected at runtime, or a secret store.
Rotate on exposure, and treat a secret committed to git as compromised even
after you delete the commit, because the history and every clone still have it.

**Input validation at the boundary.** Validate size, type, range, and encoding
where data enters. A detection with a confidence of 1e300 or a NaN latitude
should be rejected at the adapter, not discovered by the correlator.

**Cryptography.** Use the platform library. Do not implement it. Do not use MD5
or SHA-1 for anything security-relevant. Use a vetted password hash (bcrypt,
scrypt, Argon2) rather than a plain digest. Verify TLS certificates; never
disable verification "temporarily."

**Least privilege.** Services run as a non-root service account, with only the
filesystem and network access they need. Containers non-root and read-only root
filesystem.

**Error messages.** Do not return a stack trace or an internal path to an
external caller. Log the detail internally, return a correlation id.

**Logging.** Good logs are a security control. Log authentication decisions,
configuration changes, and privileged actions with enough context to
reconstruct an event, and protect the logs from tampering.

## 4. Hardening a RHEL host, in outline

Enough to talk credibly:

- Apply the STIG for the OS version, verified by an OpenSCAP scan against the
  benchmark, with findings tracked.
- Remove unneeded packages and disable unneeded services. Minimize attack
  surface.
- Enforce SELinux. Fix labels and write policy; do not set permissive.
- Firewall default-deny, with explicit allows.
- No shared accounts. Individual accounts, sudo with logging, key-based SSH,
  no root login.
- Audit rules (`auditd`) for privileged actions and configuration changes.
- FIPS-validated cryptographic modules where required, which does constrain
  which algorithms your application may use. Worth knowing that this exists,
  because it occasionally breaks application code that assumed MD5 was
  available.
- Time synchronization from an authorized source, since correlated logs across
  sites depend on it.
- Patch cadence with a defined window, and a tested rollback.

The application-side consequence to mention: **hardening breaks things**, and
finding out which things is engineering work. A STIG that disables a cipher
suite, enforces a umask, sets a mount option, or restricts a port will surface
in your application as a mysterious failure. Anticipating that and testing
against a hardened baseline in CI rather than a stock image is the mature move,
and it is precisely the kind of contribution this role wants.

## 5. Supply chain

Increasingly central, and directly relevant to "integrating COTS and FOSS
updates."

- **SBOM** for every artifact, generated by the build, in CycloneDX or SPDX
  format. It is what makes the next Log4Shell a one-hour query instead of a
  two-week audit.
- **Provenance and signing.** Sign artifacts and verify signatures at deploy.
  Pin container images by digest, not by tag, since a tag can be moved.
- **Internal mirrors.** In an air-gapped or controlled environment, no build
  reaches a public registry. Everything comes from an internal repository whose
  contents were reviewed and scanned on entry.
- **License compliance.** FOSS carries license obligations. Copyleft terms can
  be a genuine problem for delivered software on a government contract, so new
  dependencies go through approval. If you introduce a library in a code review
  and cannot say what its license is, expect that to be caught.
- **Dependency hygiene.** Fewer dependencies is a security posture. Pulling a
  package to avoid writing twelve lines is a bad trade when every package is
  something you must monitor, scan, upgrade, and license-clear for the life of
  the program.

That last point is worth making. On a commercial team, adding a dependency is
nearly free. Here it is not, and showing that you know the difference marks you
as someone who understands the environment.

## 6. Where security meets the schedule

A realistic interview question: *"Security wants a library upgraded this sprint
and it breaks an interface. What do you do?"*

A good answer has these parts:

1. **Get the actual constraint.** Is there a mandated date, or is it a
   prioritization? Those are different conversations.
2. **Size the work honestly**, including the regression testing, not just the
   code change.
3. **Offer options with tradeoffs** rather than a yes or a no: full upgrade next
   sprint, a backported patch now with the upgrade scheduled, or a compensating
   control now with a POA&M. Say what each costs and what risk each leaves.
4. **Escalate early, with a recommendation.** The failure mode is discovering in
   week three that it does not fit. Bring it to the product owner and the
   security lead in week one with numbers.
5. **Do not silently accept an impossible commitment.** On a dispersed team that
   is how a schedule slips without anyone noticing until the demo.

That answer demonstrates the collaboration the posting asks for and it shows
you understand that "no" is rarely the useful response; "here are three options
and what each costs" is.

## 7. Clearance and handling, briefly

- Know your own clearance status precisely, including dates.
- Never discuss classified detail in an interview. If asked about past work at a
  level you cannot discuss, say so plainly: *"I can describe the engineering at
  an unclassified level; the specifics of the mission data I would need to
  handle in an appropriate setting."* That answer is expected and respected.
  Volunteering more is a red flag.
- Understand basic handling: classified work happens on accredited systems, no
  personal devices, controlled media, and export control (ITAR/EAR) restricts
  who may receive technical data regardless of clearance. For a foreign military
  sales program in the UAE, export control and foreign disclosure rules are a
  daily consideration, not a formality.
- Expect that the process involves a background investigation and, for an
  overseas assignment, additional screening.
