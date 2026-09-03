# Attack Chain

## Incident 1 — Joomla website compromise

```text
External attacker
    |
    +-- Automated HTTP POST requests
    |      +-- /joomla/administrator/index.php
    |
    +-- 412 credential attempts
    |      +-- source: 23.22.63.114
    |
    +-- Successful administrative authentication
    |      +-- source: 40.80.148.42
    |
    +-- Malicious file upload
           +-- 3791.exe
           +-- agent.php
                  |
                  +-- Web-server compromise / defacement
```

The report maps this chain to T1110, T1078, T1190, T1105 and T1505.

## Incident 2 — Ransomware infection

```text
USB-delivered malicious document
        |
        +-- Miranda Tate unveiled.dotm
                    |
                    +-- Malicious macro
                           |
                           +-- wscript.exe
                                  |
                                  +-- 20429.vbs
                                         |
                                         +-- 121214.tmp
                                                |
                                                +-- Local file encryption
                                                |      +-- 406 unique .txt files
                                                |
                                                +-- SMB / TCP 445
                                                       |
                                                       +-- we9041srv
                                                              +-- 257 unique .pdf files
```

The report maps this chain to T1204, T1059, T1059.005, T1036, T1021.002, T1486 and T1071.

## Detection coverage

The five SPL detections in `../detections/` are intended to surface the main observable behaviours in these chains rather than reproduce every investigative query from the report.
