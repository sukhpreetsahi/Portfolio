# Investigation Screenshots

These images show the main stages of the investigation in Splunk. They are included to make it easier to connect the written findings with the searches and results.

| Image | What it shows |
|---|---|
| `splunk_overview.png` | The initial view used to understand the environment and the main web server activity. |
| `brute_force_detection.png` | The login activity that shows the high number of password attempts. |
| `malicious_upload.png` | The suspicious file upload activity on the web server. |
| `ransomware_detection.png` | The large number of file changes linked to the ransomware activity. |
| `web_attack_timeline.png` & `ransomware_attack_timeline.png`| The main events placed in order to show how the two attacks developed. |
|`C2_behaviour_detection.png` | Communication with external C2 IP address activity. |
|`temp_file_execution.png` | Execution of the temporary file. |

The screenshots can be viewed alongside the SPL files in `../detections/` and the investigation notes in `../investigation/`.
