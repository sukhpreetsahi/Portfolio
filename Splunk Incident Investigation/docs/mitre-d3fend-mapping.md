# MITRE ATT&CK & D3FEND Mapping

This mapping connects the observed attack behaviours to MITRE ATT&CK techniques and practical D3FEND defensive strategies. The objective is to show not only how an adversary progressed through the environment, but where a SOC could interrupt that progression.

## Web-server compromise

| ATT&CK | Technique | Observed behaviour | D3FEND strategy | Defensive value |
|---|---|---|---|---|
| T1110 | Brute Force | Automated password guessing against the Joomla administrator login | Account Locking / Strong Password Policy | Reduces the rate at which credentials can be guessed and raises the cost of automation. |
| T1078 | Valid Accounts | Successful use of the compromised `admin` credential | Multi-factor Authentication | Prevents a stolen or guessed password from being sufficient on its own. |
| T1190 | Exploit Public-Facing Application | Attack focused on an exposed Joomla administration interface | Web Session Activity Analysis / Web Server Access Mediation | Restricts and monitors access to sensitive application paths. |
| T1105 | Ingress Tool Transfer | `3791.exe` and `agent.php` uploaded to the web server | File Integrity Monitoring | Detects unexpected additions or changes to application content. |
| T1505 | Server Software Component | Server-side script content introduced after authentication | Process Lineage Analysis | Helps surface abnormal application-to-process relationships and suspicious script activity. |

## Ransomware infection

| ATT&CK | Technique | Observed behaviour | D3FEND strategy | Defensive value |
|---|---|---|---|---|
| T1204 | User Execution | Malicious Office document opened from removable media | Executable Allowlisting | Prevents unauthorised payloads from reaching execution. |
| T1059 | Command and Scripting Interpreter | `wscript.exe` used to launch the scripted stage | Script Execution Control | Restricts and monitors script interpreters commonly abused by malware. |
| T1059.005 | Visual Basic | `20429.vbs` used to continue the execution chain | Script Execution Analysis | Provides visibility into suspicious VBScript behaviour and process relationships. |
| T1036 | Masquerading | Payload presented as `121214.tmp` | File Content Analysis | Examines suspicious files whose names or locations do not match expected content. |
| T1021.002 | SMB / Windows Admin Shares | Workstation accessed the file server over TCP/445 | Remote File Access Mediation | Limits unnecessary remote access and helps contain lateral impact. |
| T1486 | Data Encrypted for Impact | Hundreds of files modified rapidly on local and remote storage | File Access Pattern Analysis / Process Termination | Detects high-rate destructive activity and supports rapid containment. |
| T1071 | Application Layer Protocol | Repeated outbound connections provide potential command-and-control context | Connection Attempt Analysis / Outbound Traffic Filtering | Highlights repeated external communications and provides an opportunity to block them. |

## Defensive design

The mapping supports a layered response model:

1. **Identity controls** — MFA, strong passwords and account lockout reduce the chance that exposed administration interfaces become the initial access point.
2. **Application integrity** — monitoring changes to web content can reveal malicious uploads shortly after successful authentication.
3. **Execution controls** — restricting scripting interpreters and unusual parent-child process chains can interrupt the ransomware payload before impact.
4. **Behavioural detection** — rapid password guessing, repeated external connections and bulk file modification are useful signals because they remain valuable even when malware changes names or hashes.
5. **Network containment** — controlling SMB access and segmenting critical servers limits the reach of a compromised workstation.

The full set of detection queries is stored under `../detections/`, linking the ATT&CK behaviours above to concrete Splunk implementation.
