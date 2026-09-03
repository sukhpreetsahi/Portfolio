# Incident Timeline

This timeline reconstructs two separate compromise paths from the available Splunk telemetry. The timestamps are presented in chronological order so the investigation can be followed from first observable action to impact.

## Web-server compromise — 10 August 2016

| Timestamp | Phase | Event | Significance |
|---|---|---|---|
| 21:46:51 | Initial access | Automated brute-force activity begins against `/joomla/administrator/index.php` from `23.22.63.114`. | High-volume credential guessing establishes the initial access attempt. |
| 21:48:05 | Initial access | `40.80.148.42` submits the correct password and receives the Joomla dashboard. | Confirms successful authentication using the compromised administrator credential. |
| 21:52:47 | Post-compromise | `3791.exe` is uploaded to the web server. | Indicates the attacker moved from credential access to introducing a payload. |
| 21:52:47 | Post-compromise | `agent.php` is observed in the same upload activity. | Suggests the attacker also introduced server-side script functionality. |

### Timing observations

The brute-force phase produced **412 unique password attempts in approximately 90 seconds**, making the activity inconsistent with normal interactive administration. The later successful login came from a different external address, linking the authentication phase to the subsequent server activity without assuming both phases originated from the same source.

## Ransomware infection — 24 August 2016

| Timestamp | Phase | Event | Significance |
|---|---|---|---|
| 16:43:21 | Delivery / execution | `Miranda Tate unveiled.dotm` is executed on `we8105desk`. | Establishes the user-driven entry point. |
| 16:43:21 | Execution | The document launches script activity through `wscript.exe`. | Shows the transition from document execution to an interpretable payload. |
| 16:43:21 | Execution | `20429.vbs` is executed. | Identifies the script stage of the payload chain. |
| 16:48:21 | Execution | `121214.tmp` is launched by the VBScript. | Provides the key temporary-payload execution point. |
| 17:04:31 | Impact | First observed `.txt` file is encrypted on the workstation. | Marks the start of measurable file-impact activity. |
| 17:05:47 | Impact | Last observed `.txt` file is encrypted on the workstation. | 406 unique text files were affected during this burst. |
| 17:10:01 | Impact | First observed `.pdf` file is encrypted on `we9041srv`. | Shows impact extending to the network share. |
| 17:13:04 | Impact | Last observed `.pdf` file is encrypted on `we9041srv`. | 257 unique PDF files were affected over roughly ten minutes. |

## Correlation notes

The ransomware sequence is strengthened by three independent telemetry types: Sysmon process creation events reveal the document-to-script-to-temporary-payload lineage; Sysmon network events show the workstation reaching the file server on TCP/445; and Windows Security events show rapid modification of files on the remote share.

The overall sequence can therefore be treated as a connected execution and impact chain rather than a collection of unrelated alerts.
