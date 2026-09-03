# MITRE ATT&CK and D3FEND Mapping

The mappings below reproduce the technique-to-defensive-strategy relationships presented in the Case #51489 report.

## Website defacement incident

| ATT&CK | Technique | Observed behaviour | D3FEND strategy | Rationale |
|---|---|---|---|---|
| T1110 | Brute Force | Automated authentication attempts against admin login | Account Locking / Strong Password Policy | Limits login attempts and increases time to brute force. |
| T1078 | Valid Accounts | Successful login using compromised admin credentials | MFA | Adds another security layer after credential compromise. |
| T1190 | Exploit Public-Facing Application | Attacker targeted exposed admin portal | Proxy-based Web Server Access Mediation / Web Session Activity Analysis | Restricts access and blocks suspicious upload attempts. |
| T1105 | Ingress Tool Transfer | Upload of `3791.exe` and `agent.php` | File Integrity Monitoring | Detects unauthorised uploads or modifications in server directories. |
| T1505 | Server Software Component | Uploaded scripts used to control the server | Process Lineage Analysis | Identifies unusual processes/scripts and abnormal parent-child chains. |

## Ransomware incident

| ATT&CK | Technique | Observed behaviour | D3FEND strategy | Rationale |
|---|---|---|---|---|
| T1204 | User Execution | User opened malicious document from USB | Executable Allowlisting | Prevents unauthorised payloads from executing. |
| T1059 | Command and Scripting Interpreter | VBScript executed via `wscript.exe` | Script Execution Control | Restricts and monitors scripting interpreters used by malware. |
| T1059.005 | Visual Basic | VBScript used to launch malicious payload | Script Execution Analysis | Detects suspicious script activity and blocks unauthorised processes. |
| T1036 | Masquerading | Payload disguised as temporary file `121214.tmp` | File Content Analysis | Helps identify files with suspicious content. |
| T1021.002 | SMB / Windows Admin Shares | Host accessed file server to encrypt files on network share | Remote File Access Mediation | Restricts remote file access. |
| T1486 | Data Encrypted for Impact | Hundreds of files rapidly encrypted locally and on file server | File Access Pattern Analysis / Process Termination | Detects bulk modification and can stop the process before further spread. |
| T1071 | Application Layer Protocol | Multiple outbound connections indicating potential C2 | Connection Attempt Analysis / Outbound Traffic Filtering | Monitors and restricts abnormal repeated connections to external systems. |

## Layered defensive controls

The report's overall conclusion is that layered controls are appropriate: stronger authentication, script-execution restrictions, behavioural monitoring, file-integrity monitoring, and network segmentation can reduce the likelihood or impact of similar attacks.
