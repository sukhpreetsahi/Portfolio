# MITRE ATT&CK and D3FEND Mapping

This page links the main attacker behaviours found in the investigation to MITRE ATT&CK techniques and defensive ideas from MITRE D3FEND.

The purpose is simple. For each step in the attack, there should be a clear idea of what could have helped prevent it, detect it, or limit the damage.

## Web server compromise

| ATT&CK | Technique | What was seen | D3FEND idea | How it helps |
|---|---|---|---|---|
| T1110 | Brute Force | Many password attempts against the Joomla administrator page | Account Locking / Strong Password Policy | Makes repeated password guessing harder and slower. |
| T1078 | Valid Accounts | A successful login to the Joomla dashboard | Multi-factor Authentication | A password alone would not be enough to log in. |
| T1190 | Exploit Public-Facing Application | The exposed Joomla administrator page was targeted | Web Session Activity Analysis / Web Server Access Mediation | Adds control and monitoring around sensitive web pages. |
| T1105 | Ingress Tool Transfer | `3791.exe` and `agent.php` were uploaded | File Integrity Monitoring | Helps spot unexpected changes to web server files. |
| T1505 | Server Software Component | Server-side PHP content was introduced after login | Process Lineage Analysis | Helps identify unusual processes or scripts running on the server. |

## Ransomware infection

| ATT&CK | Technique | What was seen | D3FEND idea | How it helps |
|---|---|---|---|---|
| T1204 | User Execution | A malicious Office document was opened from removable media | Executable Allowlisting | Blocks software that is not approved to run. |
| T1059 | Command and Scripting Interpreter | `wscript.exe` was used during the execution chain | Script Execution Control | Limits or monitors the use of script tools. |
| T1059.005 | Visual Basic | `20429.vbs` continued the attack | Script Execution Analysis | Helps find unusual VBScript activity. |
| T1036 | Masquerading | The payload used the name `121214.tmp` | File Content Analysis | Checks suspicious files instead of trusting the filename. |
| T1021.002 | SMB / Windows Admin Shares | The workstation connected to the file server over TCP/445 | Remote File Access Mediation | Limits which systems can reach shared files. |
| T1486 | Data Encrypted for Impact | Large numbers of files were changed in a short time | File Access Pattern Analysis / Process Termination | Can spot unusual file activity and help stop the process. |
| T1071 | Application Layer Protocol | Repeated outbound connections were reviewed as possible C2 activity | Connection Attempt Analysis / Outbound Traffic Filtering | Helps identify and block suspicious external communication. |

## Practical defensive controls

The attack shows why a single security control is not enough.

**Protect accounts.** Use MFA for important accounts. Add strong password rules and account lockout controls.

**Protect web servers.** Limit access to administration pages. Monitor important web folders for unexpected files and changes.

**Control script execution.** Keep an eye on `wscript.exe` and `cscript.exe`, especially when they start files from unusual locations.

**Watch file behaviour.** A large number of document changes in a short time can be a better ransomware signal than a file name or hash.

**Limit network access.** Only allow required SMB connections. Separating important servers from user workstations can reduce the damage from a compromised machine.

The related Splunk detections are stored in `../detections/` so that each main behaviour can be tested directly.
