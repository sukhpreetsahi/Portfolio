# Splunk Incident Investigation

A practical Splunk investigation into two security incidents found in archived system and network logs.

The goal of this project was simple: work out what happened, show how the evidence fits together, and turn the useful findings into detections that could help spot similar activity in the future.

## What was investigated

The logs showed two separate attack paths.

### Joomla web server compromise

An exposed Joomla administrator page was hit by a large number of login attempts. A successful login was followed by the upload of `3791.exe` and `agent.php` to the web server.

### Ransomware infection

A workstation ran the file `Miranda Tate unveiled.dotm` from removable media. This started a chain involving `wscript.exe`, `20429.vbs`, and `121214.tmp`. The malware then encrypted files on the workstation and on a connected file server.

## Environment

| Asset | Address | Role |
|---|---|---|
| `imreallynotbatman.com` | `192.168.250.70` | Joomla web server |
| `we8105desk` | `192.168.250.100` | Workstation affected by ransomware |
| `we9041srv` | `192.168.250.20` | File server reached over SMB |
| `admin` | Joomla account | Privileged account targeted by the login attack |
| `bob.smith` | Windows user | User account linked to the workstation activity |

## How I approached the investigation

1. **Set the scope** by identifying the main systems, users, log sources, and time periods.
2. **Search for unusual activity** such as repeated login attempts, file uploads, new processes, network connections, and large bursts of file changes.
3. **Join the events together** using timestamps, source and destination addresses, process names, and parent-child process relationships.
4. **Check the evidence** using counts and related log events so that a finding was supported by more than one clue where possible.
5. **Build detections** from the behaviours that were clear enough to be useful outside this single investigation.

## Key findings

- `23.22.63.114` made **412 unique password attempts in about 90 seconds** against the Joomla administrator page.
- `40.80.148.42` later logged in successfully and was linked to the upload activity that followed.
- `3791.exe` and `agent.php` were uploaded to the web server.
- `we8105desk` connected to `we9041srv` over TCP/445 during the ransomware activity.
- **406 unique `.txt` files** were affected on the workstation.
- **257 unique `.pdf` files** were affected on the file server.
- The ransomware execution path was `Miranda Tate unveiled.dotm` -> `wscript.exe` -> `20429.vbs` -> `121214.tmp`.

## Detection coverage

| File | Technique | What it looks for |
|---|---|---|
| `brute_force.spl` | T1110 | Large numbers of password attempts against the Joomla administrator page |
| `malicious_file_upload.spl` | T1105 | Executable or script files being uploaded through HTTP POST requests |
| `c2_beaconing.spl` | T1071 | Repeated outbound connections to the same external destination |
| `ransomware_activity.spl` | T1486 | Large numbers of document files being changed in a short period |
| `suspicious_temp_execution.spl` | T1059 | Script tools starting temporary `.tmp` files |

## Evidence

The `screenshots` folder contains the main visual evidence used during the investigation. The timeline images are also included in `incident_timeline.md` so the sequence of events can be understood without reading the full investigation notes first.

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
│   ├── web_attack_timeline.svg
│   ├── ransomware_attack_timeline.svg
│   ├── splunk_overview.png
│   ├── brute_force_detection.png
│   ├── malicious_upload.png
│   └── ransomware_detection.png
└── docs/
    └── mitre-d3fend-mapping.md
```

## Defensive takeaways

The main lessons from the investigation are practical controls:

- Protect admin accounts with MFA, strong passwords, and account lockout.
- Limit access to public administration pages.
- Watch for unexpected uploads to web servers.
- Control and monitor script tools such as `wscript.exe` and `cscript.exe`.
- Detect fast bursts of file changes instead of waiting for known ransomware names or hashes.
- Limit unnecessary SMB access between workstations and servers.

This project shows the full process from finding a suspicious event in Splunk to building a repeatable detection from it.
