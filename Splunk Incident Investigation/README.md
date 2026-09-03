# Splunk Incident Investigation

## Case 51489

This folder documents the Splunk-based investigation described in the incident analysis report. It covers two related security incidents observed in the `botsv1` dataset:

1. **Website defacement / web-server compromise** — the Joomla administrator portal for `imreallynotbatman.com` was targeted by an automated brute-force attack. Successful authentication was followed by upload of `3791.exe` and `agent.php` to the web server.
2. **Ransomware infection** — workstation `we8105desk` executed a malicious Word document from USB, which launched `20429.vbs`, then `121214.tmp`; the resulting ransomware activity encrypted local files and files on the connected file server `we9041srv`.

The report identifies the following affected systems and identities:

| Item | Value |
|---|---|
| Web server | `192.168.250.70` (`imreallynotbatman.com`) |
| Workstation | `192.168.250.100` (`we8105desk`) |
| File server | `192.168.250.20` (`we9041srv`) |
| Joomla identity | `admin` |
| User identity | `bob.smith` |
| External IPs | `23.22.63.114`, `40.80.148.42` |
| Malicious files | `3791.exe`, `agent.php`, `20429.vbs`, `121214.tmp` |
| Malicious document | `Miranda Tate unveiled.dotm` |

## Repository layout

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

## Detection coverage

| Detection | Primary ATT&CK mapping | Purpose |
|---|---|---|
| Malicious file upload | T1105 | Identify executable/script/web-shell style uploads through HTTP POST requests. |
| Brute force | T1110 | Detect high-volume credential attempts against the Joomla administrator portal. |
| C2 beaconing | T1071 | Identify repeated outbound connections to external destinations. |
| Ransomware activity | T1486 | Detect rapid bulk modification of document files on local and network locations. |
| Suspicious temp execution | T1059 | Detect script interpreters launching `.tmp` payloads. |

## Investigation highlights

- 412 password attempts were observed from `23.22.63.114` in approximately 90 seconds.
- A later successful administrative login came from `40.80.148.42`.
- `3791.exe` and `agent.php` were uploaded to the web server.
- `we8105desk` connected to `we9041srv` over TCP/445 during the ransomware incident.
- 406 unique `.txt` files were identified as encrypted on the workstation.
- 257 unique `.pdf` files were identified as encrypted on the file server.
- The temporary payload chain was `Miranda Tate unveiled.dotm` → `wscript.exe` / `20429.vbs` → `121214.tmp`.

## Source

Prepared from **OSM_CW2_Report-5-3(1).pdf**, Case #51489. The SPL is reproduced from the report's Detection Rules section, with only file-level headings added for readability.
