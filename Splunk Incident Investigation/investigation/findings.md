# Investigation Findings

This case study focuses on what could be established from the available telemetry, how the evidence was correlated, and what should be carried forward into future detection engineering.

## Finding 1 — Automated credential attack against the Joomla administrator portal

The Joomla administrator endpoint received **412 unique password attempts in approximately 90 seconds** from `23.22.63.114`. The requests were HTTP POSTs to `/joomla/administrator/index.php` and targeted the `admin` username. The request rate and scripted user-agent context make automated guessing far more likely than normal administrative activity.

A later request from `40.80.148.42` successfully authenticated with the correct password and returned the Joomla dashboard. This second source is important because it demonstrates why correlation by behaviour and time is more useful than assuming a single source address must explain an entire intrusion.

## Finding 2 — Malicious payloads were introduced after administrative access

The successful Joomla access was followed by upload activity involving `3791.exe` and `agent.php` to the web server at `192.168.250.70`.

The executable extension is a strong high-risk signal in an HTTP upload workflow. The concurrent presence of a PHP file increases the likelihood that the attacker was attempting to establish executable server-side functionality rather than simply transferring a benign file.

## Finding 3 — A scripted execution chain led to ransomware activity

On `we8105desk`, process telemetry shows a progression from the document `Miranda Tate unveiled.dotm` to `wscript.exe`, then `20429.vbs`, and finally the temporary payload `121214.tmp`.

The numerical filenames are notable because they provide little semantic context and are consistent with a payload attempting to blend into temporary-file activity. The parent/child relationship is stronger evidence than the filename alone: the temporary file was observed as a child of the VBScript stage.

## Finding 4 — The workstation reached a file server over SMB

Sysmon Event ID 3 showed `we8105desk` (`192.168.250.100`) connecting to `we9041srv` (`192.168.250.20`) on TCP/445.

This connection matters because the subsequent file-impact evidence extends beyond the workstation. It establishes the network path that allowed the ransomware activity to affect a shared file location.

## Finding 5 — File encryption occurred at abnormal scale and speed

On the workstation, **406 unique `.txt` files** were affected within approximately **5.5 minutes**. A separate Windows Security analysis identified **257 unique `.pdf` files** on the file server within roughly **10 minutes**.

The combination of scale, speed, document-focused targeting and the earlier process chain provides a strong behavioural basis for ransomware detection without depending on a known malware hash or filename.

## Indicators of compromise

| Type | Value | Context |
|---|---|---|
| Source IP | `23.22.63.114` | High-volume Joomla password guessing |
| Source IP | `40.80.148.42` | Successful Joomla authentication and subsequent upload activity |
| Web payload | `3791.exe` | Uploaded executable |
| Web payload | `agent.php` | Uploaded server-side script |
| Document | `Miranda Tate unveiled.dotm` | Ransomware delivery / execution point |
| Script | `20429.vbs` | VBScript execution stage |
| Temp payload | `121214.tmp` | Temporary executable payload |
| Web server | `192.168.250.70` | Joomla host |
| Workstation | `192.168.250.100` | Ransomware execution host |
| File server | `192.168.250.20` | SMB-connected server affected by encryption |

## Defensive priorities

### Protect privileged web access

Use MFA for administrative accounts, enforce strong password and account-lockout policies, and restrict exposure of administrative web interfaces through network controls.

### Detect the upload-to-execution transition

File-integrity monitoring and upload inspection should alert when executable or server-side script content appears in directories where application code is not normally modified.

### Restrict script interpreters

Monitor and, where appropriate, constrain `wscript.exe` and `cscript.exe`. A script interpreter spawning temporary payloads is a particularly useful behavioural detection point.

### Detect impact behaviour early

Ransomware can often be identified before large-scale damage through file-access velocity, unusual extension patterns and bursts of modifications. Local and network-share telemetry should be correlated rather than monitored in isolation.

### Reduce lateral impact

SMB access should be limited to systems and shares that require it. Network segmentation and mediation of remote file access can constrain the blast radius of a compromised workstation.

## Detection engineering lessons

The most reusable indicators are behavioural: request velocity, password uniqueness, suspicious upload extensions, process lineage, repeated outbound connections, SMB access and rapid bulk file modification. These signals are documented as standalone SPL detections in `../detections/` so they can be adapted to other environments and data schemas.
