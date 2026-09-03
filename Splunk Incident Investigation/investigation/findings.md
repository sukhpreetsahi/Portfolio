# Findings

## Executive findings

- The Joomla administrative interface experienced 412 authentication attempts in approximately 90 seconds from the external source recorded in the report.
- A later request from a second external source successfully authenticated to the Joomla dashboard.
- The web server subsequently received the files `3791.exe` and `agent.php`.
- On 24 August 2016, workstation `we8105desk` executed the document `Miranda Tate unveiled.dotm`, followed by script activity involving `20429.vbs` and the temporary payload `121214.tmp`.
- The workstation communicated with `we9041srv` over TCP/445 during the file-impact activity.
- The investigation identified 406 unique `.txt` files on the workstation and 257 unique `.pdf` files on the file server as affected.

## Impacted assets

| Asset | Address | Role |
|---|---|---|
| `imreallynotbatman.com` web server | `192.168.250.70` | Joomla target and upload destination |
| `we8105desk` | `192.168.250.100` | Affected workstation |
| `we9041srv` | `192.168.250.20` | Remote file server |

## Indicators recorded in the report

- `23.22.63.114`
- `40.80.148.42`
- `3791.exe`
- `agent.php`
- `20429.vbs`
- `121214.tmp`
- `Miranda Tate unveiled.dotm`

## Recommendations recorded in the report

- Implement MFA for critical accounts.
- Enforce account lockout and strong password policies.
- Restrict administrative web portals with network access controls.
- Deploy EDR to detect ransomware activity.
- Monitor or restrict scripting interpreters such as `wscript.exe`.
- Implement file integrity monitoring on web servers.
- Provide security-awareness training for malicious USB devices and documents.
