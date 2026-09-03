# Splunk Incident Investigation

A practical Splunk threat-hunting and incident-response case study built around a retrospective compromise discovered in archived security telemetry.

The investigation follows a SOC workflow: establish what happened, identify the affected assets and identities, reconstruct the attack chain, extract useful indicators, and turn the observed behaviours into repeatable detections.

## Scenario

A threat-hunting team identified evidence of a historical compromise that had not been detected by the existing EDR, IDS or SIEM controls. Archived logs covering the suspected period were analysed in Splunk to determine how the intrusion occurred, what the attacker did after initial access, and where security controls could be improved.

The telemetry used for the investigation spans HTTP traffic, Sysmon process and network events, and Windows Security events in the `botsv1` dataset.

Two distinct attack paths emerged:

### Web-server compromise

An exposed Joomla administrator portal at `imreallynotbatman.com` was targeted by automated credential attacks. A successful login was followed by the upload of `3791.exe` and `agent.php`, providing evidence of application compromise and malicious server-side content.

### Ransomware infection

A workstation executed the malicious document `Miranda Tate unveiled.dotm` from removable media. The execution chain moved through `wscript.exe` and `20429.vbs` before launching the temporary payload `121214.tmp`. The payload then modified large numbers of files locally and across an SMB-connected file server.

## Environment

| Asset / identity | Value | Relevance |
|---|---|---|
| Web server | `imreallynotbatman.com` / `192.168.250.70` | Joomla target and malicious upload destination |
| Workstation | `we8105desk` / `192.168.250.100` | Ransomware execution host |
| File server | `we9041srv` / `192.168.250.20` | SMB-accessed network share affected by encryption |
| Joomla account | `admin` | Targeted privileged identity |
| User account | `bob.smith` | User context associated with workstation activity |

## Investigation workflow

1. **Scope the environment** — identify the systems, data sources and time window involved.
2. **Hunt for anomalous behaviour** — use targeted Splunk searches to isolate unusual authentication, uploads, process creation, network connections and file activity.
3. **Correlate events** — connect timestamps, source addresses, parent-child process relationships and destination systems into coherent attack sequences.
4. **Validate findings** — use distinct counts, event fields and supporting telemetry to distinguish malicious behaviour from background noise.
5. **Operationalise the findings** — convert the strongest behavioural indicators into reusable SPL detections and map them to MITRE ATT&CK and D3FEND.

The searches are deliberately separated from the detection rules so the repository shows both the investigative reasoning and the resulting operational coverage.

## Key results

- `23.22.63.114` generated **412 unique password attempts in roughly 90 seconds** against the Joomla administrator endpoint.
- `40.80.148.42` later authenticated successfully and was subsequently associated with malicious upload activity.
- The web server received `3791.exe` and `agent.php`.
- `we8105desk` connected to `we9041srv` over TCP/445 during the ransomware activity.
- **406 unique `.txt` files** were affected on the workstation.
- **257 unique `.pdf` files** were affected on the network file server.
- The process chain `Miranda Tate unveiled.dotm` → `wscript.exe` → `20429.vbs` → `121214.tmp` provides a strong behavioural narrative for the ransomware execution path.

## Detection coverage

| Detection | ATT&CK | What it looks for |
|---|---|---|
| `malicious_file_upload.spl` | T1105 | Executable, script and web-shell style files uploaded through HTTP POST requests |
| `brute_force.spl` | T1110 | High-volume and high-uniqueness authentication attempts against the Joomla administrator endpoint |
| `c2_beaconing.spl` | T1071 | Repeated connections from an internal host to the same external destination |
| `ransomware_activity.spl` | T1486 | Rapid bulk modification of document files on local systems and network shares |
| `suspicious_temp_execution.spl` | T1059 | Script or command interpreters launching temporary `.tmp` payloads |

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

The investigation points to layered controls rather than a single preventive measure: stronger authentication and lockout controls for exposed administration interfaces; tighter restrictions and monitoring around script interpreters and removable media; behavioural detection for bulk file modification; file-integrity monitoring on web servers; and network controls that limit unnecessary SMB exposure.

The project is designed to show the full path from raw telemetry to a defensible finding, and from a finding to an actionable detection or control.
