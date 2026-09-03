# Splunk Incident Investigation

A practical Splunk investigation project that shows how security logs can be used to find an old compromise, understand what happened, and build detections for future incidents.

## Overview

The investigation starts with archived security logs from a network where a compromise had gone unnoticed. The aim was to work through the data like a SOC analyst would:

1. Find unusual activity.
2. Work out which systems and accounts were involved.
3. Build a timeline of what happened.
4. Identify useful indicators.
5. Turn the strongest findings into Splunk detections.
6. Map the attacker activity to MITRE ATT&CK and possible D3FEND controls.

The logs include HTTP traffic, Sysmon process and network events, and Windows Security events from the `botsv1` dataset.

## What was found

Two attack paths were identified.

### 1. Joomla web server compromise

The public Joomla administrator page on `imreallynotbatman.com` was hit by a large number of login attempts. A single source, `23.22.63.114`, made **412 password attempts in about 90 seconds**.

A different external address, `40.80.148.42`, later logged in successfully and reached the Joomla dashboard. Upload activity then showed two suspicious files:

- `3791.exe`
- `agent.php`

This gave a clear path from password guessing to successful access and then to changes on the web server.

### 2. Ransomware infection

The second attack affected `we8105desk`. A document called `Miranda Tate unveiled.dotm` was opened from removable media. The process then moved through:

`wscript.exe` → `20429.vbs` → `121214.tmp`

The same workstation later connected to `we9041srv` over TCP/445. File activity showed **406 unique `.txt` files** affected on the workstation and **257 unique `.pdf` files** affected on the file server.

The combination of the process chain, SMB connection, and fast file changes is strong evidence of ransomware activity.

## Environment

| Asset or identity | Value | Role in the investigation |
|---|---|---|
| Web server | `imreallynotbatman.com` / `192.168.250.70` | Joomla server targeted by the attacker |
| Workstation | `we8105desk` / `192.168.250.100` | Ransomware execution host |
| File server | `we9041srv` / `192.168.250.20` | Shared storage affected by the ransomware |
| Joomla account | `admin` | Privileged account targeted by the login attack |
| User account | `bob.smith` | User linked to workstation activity |

## Investigation approach

The investigation was built around a simple process.

**Start broad.** Identify the systems, users, time period, and data sources involved.

**Look for unusual behaviour.** Search for large numbers of login attempts, unusual uploads, strange process activity, repeated external connections, and sudden file changes.

**Join the events together.** Compare timestamps, source addresses, parent and child processes, and network destinations to work out what happened in order.

**Check the evidence.** Use event fields and counts to confirm that the activity is unusual and that different log sources support the same conclusion.

**Build detections.** Turn the clearest behaviours into reusable SPL queries that can be tested and adapted in another environment.

## Key results

- `23.22.63.114` made **412 password attempts in roughly 90 seconds** against the Joomla administrator page.
- `40.80.148.42` later completed a successful login and was linked to the upload activity.
- `3791.exe` and `agent.php` were uploaded to the web server.
- `we8105desk` connected to `we9041srv` over TCP/445 during the ransomware activity.
- **406 `.txt` files** were affected on the workstation.
- **257 `.pdf` files** were affected on the file server.
- The ransomware process path was `Miranda Tate unveiled.dotm` → `wscript.exe` → `20429.vbs` → `121214.tmp`.

## Detection coverage

| Detection | ATT&CK | What it looks for |
|---|---|---|
| `brute_force.spl` | T1110 | A high number of login attempts with many different passwords |
| `malicious_file_upload.spl` | T1105 | Executable or script files being uploaded through HTTP |
| `c2_beaconing.spl` | T1071 | Repeated connections from an internal host to an external destination |
| `ransomware_activity.spl` | T1486 | Large numbers of document files being changed in a short period |
| `suspicious_temp_execution.spl` | T1059 | Script interpreters starting `.tmp` files |

## Repository structure

```text
Splunk Incident Investigation/
├── README.md
├── detections/
│   ├── brute_force.spl
│   ├── malicious_file_upload.spl
│   ├── c2_beaconing.spl
│   ├── ransomware_activity.spl
│   └── suspicious_temp_execution.spl
├── investigation/
│   ├── incident_timeline.md
│   ├── attack_chain.md
│   └── findings.md
├── screenshots/
│   ├── splunk_overview.png
│   ├── brute_force_detection.png
│   ├── malicious_upload.png
│   ├── ransomware_detection.png
│   └── attack_timeline.png
└── docs/
    └── mitre-d3fend-mapping.md
```

## Defensive takeaways

The investigation shows why several layers of security are useful together.

- Protect administrator accounts with MFA, strong passwords, and account lockout.
- Limit access to public administration pages.
- Watch for executable and script uploads on web servers.
- Monitor `wscript.exe` and other script tools for unusual use.
- Alert on fast, large-scale file changes that may indicate ransomware.
- Limit SMB access to systems that actually need it.
- Use file integrity monitoring on important web server files.

The main aim of this project is to show the full process from raw logs to findings, detections, and practical security improvements.
