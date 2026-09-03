# Incident Timeline

This timeline shows the main events found during the investigation. It is split into the web server incident and the ransomware incident so the sequence is easy to follow.

## Web server compromise

**10 August 2016**

| Time | What happened | Why it matters |
|---|---|---|
| 21:46:51 | `23.22.63.114` began sending repeated POST requests to `/joomla/administrator/index.php`. | This was the start of the password guessing activity. |
| 21:48:05 | `40.80.148.42` entered the correct password and reached the Joomla dashboard. | This shows that the login attack was successful. |
| 21:52:47 | `3791.exe` was uploaded to the web server. | The attacker moved from gaining access to placing a suspicious file on the server. |
| 21:52:47 | `agent.php` was also seen in the upload activity. | A PHP file in the same activity adds further evidence of a server compromise. |

### What stood out

There were **412 different password attempts in about 90 seconds**. That is not normal interactive administration and strongly suggests automated password guessing.

The successful login came from a different external address. That is worth noting because it shows that the investigation should follow the sequence of events rather than assume that one IP address must be responsible for every step.

## Ransomware infection

**24 August 2016**

| Time | What happened | Why it matters |
|---|---|---|
| 16:43:21 | `Miranda Tate unveiled.dotm` was opened on `we8105desk`. | This is the starting point of the ransomware activity. |
| 16:43:21 | `wscript.exe` was used to run a script. | The document moved into script-based execution. |
| 16:43:21 | `20429.vbs` was executed. | This identifies the next stage of the process chain. |
| 16:48:21 | `121214.tmp` was started by the VBScript. | This is the last known stage before the file impact begins. |
| 17:04:31 | The first `.txt` file was encrypted on `we8105desk`. | This marks the start of the visible file damage. |
| 17:05:47 | The last observed `.txt` file was encrypted on the workstation. | **406 unique text files** were affected during this period. |
| 17:10:01 | The first `.pdf` file was encrypted on `we9041srv`. | The impact had reached the file server. |
| 17:13:04 | The last observed `.pdf` file was encrypted on `we9041srv`. | **257 unique PDF files** were affected. |

## How the events fit together

The ransomware timeline is supported by several types of log data. Process logs show the document leading to `wscript.exe`, then `20429.vbs`, and finally `121214.tmp`. Network logs show the workstation connecting to the file server over TCP/445. Windows Security logs then show the large number of file changes.

Taken together, these events give a clear sequence from document execution to local file encryption and then impact on the shared file server.
