# Attack Chain

The investigation found two different attack paths. Each one started with a fairly normal looking event, then moved through a series of steps that became increasingly suspicious.

## 1. Joomla web server compromise

```text
23.22.63.114
    |
    +--> Joomla administrator login
    |
    +--> 412 password attempts in about 90 seconds
    |
    +--> Successful password found
    |
    +--> 40.80.148.42 logs in successfully
    |
    +--> 3791.exe uploaded
    |
    +--> agent.php uploaded
    |
    +--> Web server compromised
```

### What happened

The Joomla administrator page received a large number of login attempts in a very short time. This was not normal administrator activity. One of the attempts used the correct password and access to the Joomla dashboard was given.

After the successful login, `3791.exe` and `agent.php` were uploaded to the server. This is important because it shows that the attacker did more than gain access. They also placed new files on the server.

### ATT&CK techniques

- **T1110 - Brute Force:** many password attempts were made against the login page.
- **T1078 - Valid Accounts:** the correct administrator password was used to gain access.
- **T1190 - Exploit Public-Facing Application:** the exposed Joomla administrator page was the entry point.
- **T1105 - Ingress Tool Transfer:** files were uploaded after access was gained.
- **T1505 - Server Software Component:** server-side content was introduced to support the compromise.

## 2. Ransomware infection

```text
Removable media
      |
      +--> Miranda Tate unveiled.dotm
                 |
                 +--> Document executed
                        |
                        +--> wscript.exe
                               |
                               +--> 20429.vbs
                                      |
                                      +--> 121214.tmp
                                             |
                              +--------------+--------------+
                              |                             |
                              v                             v
                     Workstation files              SMB / TCP 445
                              |                             |
                              +--> 406 .txt files    we9041srv
                                                           |
                                                           +--> 257 .pdf files
```

### What happened

The workstation `we8105desk` ran `Miranda Tate unveiled.dotm`. The document then started `wscript.exe`, which ran `20429.vbs`. That script launched `121214.tmp`.

The next clear sign of the attack was a large burst of file encryption. The workstation had 406 unique `.txt` files affected. The workstation also reached `we9041srv` over TCP/445, and 257 unique `.pdf` files on that server were affected.

The process chain, the network connection, and the large number of file changes all support the same conclusion. This was not simply a user opening a document. It was a chain that led to ransomware impact.

### ATT&CK techniques

- **T1204 - User Execution:** a user opened the malicious document.
- **T1059 - Command and Scripting Interpreter:** `wscript.exe` was used to run the script.
- **T1059.005 - Visual Basic:** `20429.vbs` was part of the execution chain.
- **T1036 - Masquerading:** `121214.tmp` used a generic temporary-looking name.
- **T1021.002 - SMB / Windows Admin Shares:** the workstation reached the file server over TCP/445.
- **T1486 - Data Encrypted for Impact:** large numbers of files were encrypted.

## Where detection could have helped

| Attack step | What could have been spotted | Detection |
|---|---|---|
| Password guessing | Many login attempts in a short time | `../detections/brute_force.spl` |
| File upload | Executable or script files sent to the web server | `../detections/malicious_file_upload.spl` |
| Outbound communication | Repeated connections to an external address | `../detections/c2_beaconing.spl` |
| Scripted temp file | Script tools starting `.tmp` files | `../detections/suspicious_temp_execution.spl` |
| File encryption | Large numbers of document files changed quickly | `../detections/ransomware_activity.spl` |

The main lesson is that the attack did not depend on one unique file name or one alert. Several simple signals appeared at different stages. Joining those signals makes the overall attack much easier to see.
