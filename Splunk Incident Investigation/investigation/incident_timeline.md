# Incident Timeline

## Website defacement / web-server compromise — 10 August 2016

| Timestamp | Kill Chain phase | Event |
|---|---|---|
| 10/08/2016 21:46:51 | Exploitation | Brute-force attempt started. |
| 10/08/2016 21:48:05 | Exploitation / Initial Access | Correct credential entered, providing access to the dashboard. |
| 10/08/2016 21:52:47 | Installation | Executable uploaded. |

The report associates the brute-force traffic with `23.22.63.114` and the successful login / subsequent upload activity with `40.80.148.42`.

## Ransomware — 24 August 2016

| Timestamp | Kill Chain phase | Event |
|---|---|---|
| 24/08/2016 16:43:21 | Delivery | `Miranda Tate unveiled.dotm` document executed. |
| 24/08/2016 16:43:21 | Exploitation | VBScript executed via malicious macro. |
| 24/08/2016 16:48:21 | Installation | Temporary malicious payload executed. |
| 24/08/2016 17:04:31 | Actions on Objectives | First text file encrypted. |
| 24/08/2016 17:05:47 | Actions on Objectives | Last text file encrypted. |
| 24/08/2016 17:10:01 | Actions on Objectives | First PDF file encrypted. |
| 24/08/2016 17:13:04 | Actions on Objectives | Last PDF file encrypted. |

## Key timing observations

- 412 password attempts occurred in roughly 90 seconds.
- Text-file encryption activity occurred over approximately 5.5 minutes.
- The report identifies approximately 10 minutes of activity for the 257 PDF files on the shared directory.
