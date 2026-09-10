# 8. Linux and RHEL

The posting names RHEL and Windows. Fielded defense systems run RHEL, hardened
per STIG. You will be expected to be self-sufficient on a terminal: find things,
read logs, diagnose a service that will not start, and not need a sysadmin for
routine work.

Do these on a real shell. Reading them does nothing.

## 1. Navigation and files

```bash
pwd; cd /opt/eadge; cd -          # cd - returns to the previous directory
ls -lah                           # long, all, human-readable sizes
ls -lt | head                     # newest first: which file just changed?
tree -L 2                         # if installed
du -sh /var/log/*  | sort -h      # what is eating the disk
df -h                             # filesystem usage
stat config.yaml                  # size, permissions, timestamps, inode
file mystery.bin                  # what kind of file is this
```

```bash
cp -a src/ dest/                  # -a preserves permissions, times, symlinks
mv old new
rm -rf build/                     # think before you type this
mkdir -p a/b/c
ln -s /opt/app/current /opt/app/live     # symlink; note the argument order
tar -czf backup.tgz logs/         # create gzip
tar -xzf backup.tgz -C /tmp/out   # extract to a directory
```

## 2. Finding things, which is most of the job

```bash
find /opt -name "*.log" -mtime -1              # modified in the last day
find . -type f -size +100M                     # large files
find /var/log -name "*.gz" -mtime +30 -delete  # careful
find . -name "*.py" -exec grep -l "TODO" {} +  # combine

grep -rn "TrackCorrelator" src/                # recursive, with line numbers
grep -rin --include="*.java" "deprecated" .    # case-insensitive, filtered
grep -c ERROR app.log                          # count matches
grep -A3 -B3 "NullPointer" app.log             # context lines
grep -v DEBUG app.log                          # invert
grep -E "ERROR|FATAL" app.log                  # extended regex

which python3; type -a python3                 # what will actually run
command -v mvn || echo "maven not installed"
```

## 3. Reading and slicing text

These four commands answer a large share of real questions.

```bash
head -50 app.log; tail -50 app.log
tail -f app.log                    # follow a live log
tail -f app.log | grep --line-buffered ERROR
less +F app.log                    # follow inside less; Ctrl-C to scroll

wc -l app.log                      # line count
sort file.txt | uniq -c | sort -rn | head    # the frequency-count idiom
cut -d',' -f2,4 data.csv           # columns from delimited text
awk -F',' '{ sum += $3 } END { print sum/NR }' data.csv
awk '$0 ~ /ERROR/ { print $1, $5 }' app.log
sed -n '100,200p' app.log          # print a line range
sed 's/oldhost/newhost/g' conf.in > conf.out
tr -s ' ' | tr 'A-Z' 'a-z'
```

The frequency idiom is worth memorizing exactly:

```bash
# Which error message appears most in today's log?
grep ERROR app.log | awk '{ $1=""; $2=""; print }' | sort | uniq -c | sort -rn | head -10
```

## 4. Processes and resources

```bash
ps aux | grep java                 # everything, then filter
ps -ef --forest                    # process tree
pgrep -af eadge                    # pids matching a pattern, with the command
top; htop                          # interactive
kill 4711                          # SIGTERM: polite, lets it clean up
kill -9 4711                       # SIGKILL: last resort, no cleanup
pkill -f "python.*ingest"

uptime                             # load averages: 1, 5, 15 minute
free -h                            # memory, and note the buff/cache column
vmstat 1 5                         # 5 samples, 1s apart
iostat -xz 1                       # disk pressure; needs sysstat
lsof -p 4711                       # what files/sockets does this process hold
lsof -i :8080                      # who is listening on this port
```

Interpreting load average is a good interview answer: it is runnable plus
uninterruptible-sleep processes averaged over the interval. Compare it to core
count. A load of 8 on 16 cores is fine; on 2 cores it is trouble. And high load
with low CPU usually means I/O wait, not compute.

## 5. Permissions

```bash
ls -l                              # -rwxr-xr--  1 user group
chmod 640 secrets.conf             # owner rw, group r, other none
chmod u+x run.sh
chown appuser:appgroup /opt/eadge  # -R for recursive
umask                              # default permission mask for new files
id; groups                         # who am I, what groups
sudo -u appuser whoami             # run as another user
getfacl / setfacl                  # fine-grained ACLs
```

Numeric permissions: read is 4, write is 2, execute is 1. So 750 means owner
rwx, group rx, other nothing. Say it that way if asked.

On a hardened RHEL box you will also meet SELinux:

```bash
getenforce                         # Enforcing / Permissive / Disabled
sestatus
ls -Z /opt/eadge                   # security context
ausearch -m avc -ts recent         # what did SELinux just deny
restorecon -Rv /opt/eadge          # reset contexts to policy defaults
semanage port -a -t http_port_t -p tcp 8080
```

**Do not answer a permissions problem with "set SELinux to permissive."** On an
accredited system that is a security control you are not authorized to disable.
The right answer is: read the AVC denial, then fix the label or add a policy
module. That answer will impress a cyber engineer on the panel.

## 6. systemd, the service lifecycle

```bash
systemctl status eadge-ingest
systemctl start|stop|restart eadge-ingest
systemctl enable --now eadge-ingest      # start now and at boot
systemctl daemon-reload                  # after editing a unit file
systemctl list-units --failed
systemctl cat eadge-ingest               # show the effective unit file

journalctl -u eadge-ingest -n 200        # last 200 lines for one unit
journalctl -u eadge-ingest -f            # follow
journalctl -u eadge-ingest --since "1 hour ago"
journalctl -p err -b                     # errors since this boot
journalctl --disk-usage; journalctl --vacuum-time=7d
```

A minimal unit file, which you should be able to sketch:

```ini
# /etc/systemd/system/eadge-ingest.service
[Unit]
Description=EADGE ingest service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=appuser
Group=appgroup
WorkingDirectory=/opt/eadge
Environment=LOG_LEVEL=INFO
EnvironmentFile=-/etc/sysconfig/eadge-ingest
ExecStart=/opt/eadge/venv/bin/python -m eadge.ingest
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal
# hardening, the kind a STIG will ask for
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/var/lib/eadge

[Install]
WantedBy=multi-user.target
```

## 7. Networking

```bash
ip a                               # addresses (replaces ifconfig)
ip r                               # routes
ss -tulpn                          # listening TCP/UDP sockets with pids
ss -tan state established
ping -c4 10.1.2.3
traceroute 10.1.2.3
dig radar-a.example.mil +short     # DNS
nc -zv 10.1.2.3 8080               # is the port open
curl -sS -o /dev/null -w '%{http_code} %{time_total}\n' http://svc:8080/health
curl -v https://svc/api            # see the TLS handshake and headers
tcpdump -i eth0 -nn port 5000 -c 20        # actually look at the packets
firewall-cmd --list-all                    # RHEL firewalld
firewall-cmd --add-port=8080/tcp --permanent && firewall-cmd --reload
```

`ss -tulpn` and `tcpdump` are the two that separate people who have debugged
real integration problems from people who have not. On a multi-site system,
"the service is up but the peer sees nothing" is usually a firewall rule, a
route, a multicast TTL, or a bind address of `127.0.0.1` instead of `0.0.0.0`.
Have that list ready.

## 8. Packages and RHEL specifics

```bash
dnf list installed | grep openssl
dnf info openssl
dnf provides /usr/bin/python3      # which package owns this file
dnf update --security              # security errata only
dnf history; dnf history undo 42   # yes, you can roll back a transaction
rpm -qa | wc -l
rpm -qi httpd; rpm -ql httpd       # info; file list
rpm -qf /usr/sbin/httpd            # which package owns this file
rpm -V httpd                       # verify against the package manifest

cat /etc/os-release; uname -a
subscription-manager status        # RHEL entitlement
```

`dnf update --security` and `rpm -V` are directly relevant to the tech refresh
work. Bring them up in the CVE conversation ([lesson 13](cyber.html)).

## 9. Shell scripting

You should be able to write a defensible script on request.

```bash
#!/usr/bin/env bash
set -euo pipefail          # exit on error, unset var, and pipeline failure
IFS=$'\n\t'

LOG_DIR="${LOG_DIR:-/var/log/eadge}"
RETENTION_DAYS="${1:-30}"

usage() { echo "usage: $0 [retention_days]" >&2; exit 2; }
[[ "$RETENTION_DAYS" =~ ^[0-9]+$ ]] || usage

log() { printf '%s %s\n' "$(date -Is)" "$*" >&2; }

cleanup() { log "cleaning up"; rm -f "$tmp"; }
tmp="$(mktemp)"
trap cleanup EXIT

log "pruning logs older than ${RETENTION_DAYS}d in ${LOG_DIR}"
count=$(find "$LOG_DIR" -name '*.log.gz' -mtime "+${RETENTION_DAYS}" -print -delete | wc -l)
log "removed ${count} files"
```

`set -euo pipefail` is the single most useful line in shell scripting and a good
thing to be able to explain: exit on any command failure, treat unset variables
as errors, and make a pipeline fail if any stage fails rather than only the
last.

Loops and conditionals:

```bash
for host in radar-a radar-b radar-c; do
  if nc -z -w2 "$host" 8080; then
    echo "$host up"
  else
    echo "$host DOWN" >&2
  fi
done

while IFS=',' read -r sensor ts conf; do
  [[ "$sensor" == \#* ]] && continue
  echo "$sensor -> $conf"
done < detections.csv
```

Always quote your variables. `"$var"`, not `$var`. Unquoted expansion with a
space in a filename is a classic production incident.

## 10. Troubleshooting drills

Practice narrating these. Each is a plausible interview question.

### "The service will not start."

```bash
systemctl status eadge-ingest -l          # exit code and the last log lines
journalctl -u eadge-ingest -n 100 --no-pager
ls -l /opt/eadge/venv/bin/python          # does the ExecStart path exist
sudo -u appuser /opt/eadge/venv/bin/python -m eadge.ingest   # run it by hand
ss -tulpn | grep 8080                     # port already bound?
df -h; free -h                            # disk full? out of memory?
ausearch -m avc -ts recent                # SELinux denial?
```

Order matters, and the order tells the story: unit status, then logs, then run
it by hand as the service user, then resources, then security policy.

### "The disk is full."

```bash
df -h                                     # which filesystem
du -xh /var --max-depth=2 | sort -h | tail -20
journalctl --disk-usage
lsof +L1                                  # deleted files still held open by a process
```

That last one is the answer that impresses. If a process holds a deleted log
file open, `rm` does not free the space until the process closes it or restarts.
`df` shows full while `du` shows nothing. Knowing this is a strong signal.

### "It is slow."

```bash
uptime                       # is load high at all
top -o %CPU                  # one process, or everything
vmstat 1 5                   # look at the wa (I/O wait) column
iostat -xz 1                 # %util near 100 means disk bound
free -h; cat /proc/meminfo   # swapping?
ss -s                        # socket counts; connection exhaustion
```

Then narrow to the application: thread dump for Java, `py-spy` or `cProfile` for
Python, and check the obvious ones first (a log level left at DEBUG in
production is a shockingly common cause).

### "It works in the lab and fails in integration."

The highest-value question for this role. Structure the answer:

1. **Confirm the difference is real.** Same build artifact? Same version? Check
   the checksum, not the tag.
2. **Diff the environments.** OS version, kernel, JVM or Python version, library
   versions, environment variables, config files, locale and timezone, file
   permissions, SELinux mode, firewall state.
3. **Diff the data.** Real sensor input differs from lab replay: bursts,
   duplicates, out-of-order timestamps, unexpected fields, character encodings.
4. **Diff the network.** Latency, MTU, multicast routing, name resolution,
   proxies, certificate trust.
5. **Increase observability rather than guessing.** Turn on debug logging in the
   failing environment; capture packets; capture a thread dump at the moment of
   failure.
6. **Reduce.** Get to the smallest reproducer, ideally an automated one, and
   then add it to the test suite so the class of bug cannot come back.

That last step is the one that earns the job.

## 11. Windows, briefly

The posting names Windows too. You do not need depth, but know that operator
workstations and some tooling are commonly Windows, and be able to say:
PowerShell for scripting (`Get-Service`, `Get-EventLog`, `Get-Process`), Event
Viewer for logs, services.msc for the service lifecycle, and that a
cross-platform build must not assume path separators, line endings, or
case-sensitive filesystems. That last point is a real source of integration
defects and worth mentioning.
