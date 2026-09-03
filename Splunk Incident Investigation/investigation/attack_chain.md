# Attack Chain

The investigation identified two independent attack paths. They share a common theme: an apparently routine entry point was followed by attacker-controlled execution, then a clear transition into impact.

## 1. Joomla web-server compromise

```text
External source: 23.22.63.114
        |
        +--> HTTP POST requests to Joomla administrator login
        |
        +--> 412 unique password attempts / ~90 seconds
        |
        +--> Credential guessing succeeds using password later observed as "batman"
        |        
        |        External source: 40.80.148.42
        |                |
        |                +--> Successful Joomla dashboard access
        |                |
        |                +--> Upload: 3791.exe
        |                |
        |                +--> Upload: agent.php
        |                         |
        |                         +--> Server-side compromise / defacement
```

### What makes the chain convincing

The strongest correlation is the combination of authentication and follow-on upload activity. The initial source generates an unusually large and rapid password set; a second source then authenticates successfully and is subsequently associated with the malicious file upload. Together, those events form a credible progression from credential attack to application compromise.

### ATT&CK coverage

`T1110` Brute Force → `T1078` Valid Accounts → `T1190` Exploit Public-Facing Application → `T1105` Ingress Tool Transfer → `T1505` Server Software Component.

## 2. Ransomware infection

```text
Removable media
      |
      +--> Miranda Tate unveiled.dotm
                    |
                    +--> Document execution
                           |
                           +--> wscript.exe
                                  |
                                  +--> 20429.vbs
                                         |
                                         +--> 121214.tmp
                                                |
                                                +------------------+
                                                |                  |
                                                v                  v
                                      Local document impact     SMB / TCP 445
                                                |                  |
                                                +--> 406 unique   +--> we9041srv
                                                     .txt files          |
                                                                         +--> 257 unique
                                                                              .pdf files
```

### What makes the chain convincing

Sysmon process telemetry provides the execution lineage from the document to `wscript.exe`, `20429.vbs` and finally `121214.tmp`. Network telemetry shows the same workstation reaching the file server over SMB, while Windows Security events show the subsequent bulk modification of files on that remote share. The speed and scale of the modifications are consistent with automated ransomware behaviour.

### ATT&CK coverage

`T1204` User Execution → `T1059` Command and Scripting Interpreter → `T1059.005` Visual Basic → `T1036` Masquerading → `T1021.002` SMB / Windows Admin Shares → `T1486` Data Encrypted for Impact.

`T1071` Application Layer Protocol is also used as the behavioural context for repeated outbound communications identified during the investigation.

## Detection opportunities

Each major transition in the chains creates an observable defensive opportunity:

| Attack-chain stage | Observable signal | Repository detection |
|---|---|---|
| Credential attack | Rapid POST authentication attempts and high password uniqueness | `../detections/brute_force.spl` |
| Payload introduction | Executable/script uploaded through HTTP POST | `../detections/malicious_file_upload.spl` |
| Periodic outbound communication | Repeated connections to an external destination | `../detections/c2_beaconing.spl` |
| Bulk file impact | Large number of document modifications in a short window | `../detections/ransomware_activity.spl` |
| Scripted temp execution | `wscript.exe` / `cscript.exe` / `cmd.exe` launching `.tmp` content | `../detections/suspicious_temp_execution.spl` |

This separation mirrors a practical SOC workflow: first reconstruct the chain, then detect the behaviours that are both observable and operationally useful.
