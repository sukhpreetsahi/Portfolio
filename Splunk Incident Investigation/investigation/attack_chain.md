# Attack Chain

The investigation found two main attack paths. Both start with a simple entry point and then move through several steps before causing damage.

## 1. Joomla web server compromise

```text
23.22.63.114
     |
     +--> Repeated login requests to Joomla admin page
     |
     +--> 412 password attempts in about 90 seconds
     |
     +--> Successful login
             |
             +--> 40.80.148.42 reaches Joomla dashboard
             |
             +--> 3791.exe uploaded
             |
             +--> agent.php uploaded
                     |
                     +--> Web server compromised
```

### Why this chain is important

The login activity was unusually fast and involved many different passwords. A successful login followed shortly after. The same period also contains uploads of an executable and a PHP file.

The events are much more convincing when looked at together. The investigation does not need to rely on a single suspicious event. The login pattern, successful access, and file uploads all point in the same direction.

### ATT&CK techniques

`T1110` Brute Force → `T1078` Valid Accounts → `T1190` Exploit Public-Facing Application → `T1105` Ingress Tool Transfer → `T1505` Server Software Component

## 2. Ransomware infection

```text
Removable media
      |
      +--> Miranda Tate unveiled.dotm
                   |
                   +--> Document opened
                          |
                          +--> wscript.exe
                                 |
                                 +--> 20429.vbs
                                        |
                                        +--> 121214.tmp
                                               |
                         +---------------------+---------------------+
                         |                                           |
                         v                                           v
                Files changed locally                         SMB / TCP 445
                         |                                           |
                         +--> 406 unique .txt files        we9041srv file server
                                                                     |
                                                                     +--> 257 unique .pdf files
```

### Why this chain is important

The process logs show the document leading to `wscript.exe`, then `20429.vbs`, and then `121214.tmp`. Network logs show the same workstation connecting to `we9041srv` over TCP/445. File activity then shows a large number of document files being changed.

The speed and number of file changes make this very different from normal user activity and provide a strong basis for detecting ransomware behaviour.

### ATT&CK techniques

`T1204` User Execution → `T1059` Command and Scripting Interpreter → `T1059.005` Visual Basic → `T1036` Masquerading → `T1021.002` SMB / Windows Admin Shares → `T1486` Data Encrypted for Impact

Repeated outbound communication was also reviewed as possible `T1071` Application Layer Protocol activity.

## Detection opportunities

Each stage of the attack leaves a useful signal in the logs.

| Attack stage | What can be seen | Detection |
|---|---|---|
| Password attack | Many login attempts with different passwords in a short time | `../detections/brute_force.spl` |
| File upload | Executable or script files sent through HTTP | `../detections/malicious_file_upload.spl` |
| External communication | Repeated connections to the same external address | `../detections/c2_beaconing.spl` |
| File encryption | Large numbers of document files changed quickly | `../detections/ransomware_activity.spl` |
| Temporary payload execution | `wscript.exe`, `cscript.exe`, or `cmd.exe` starting `.tmp` files | `../detections/suspicious_temp_execution.spl` |

This is the main lesson from the investigation. Useful detections can be built from normal log fields and behaviour, even when the exact malware name or file hash is not known.
