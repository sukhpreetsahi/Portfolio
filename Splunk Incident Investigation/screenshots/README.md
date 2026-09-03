# Evidence Screenshots

These images provide visual evidence for the main investigation stages and make the Splunk workflow easier to review alongside the queries and written analysis.

| Image | What it demonstrates |
|---|---|
| `splunk_overview.png` | Initial scoping of the environment and identification of the primary web-server destination. |
| `brute_force_detection.png` | The brute-force detection surfacing the high-volume authentication activity. |
| `malicious_upload.png` | Detection of suspicious executable / script upload activity to the web server. |
| `ransomware_detection.png` | Detection of rapid, high-volume file modification consistent with ransomware. |
| `attack_timeline.png` | The reconstructed sequence of major events across the two attack paths. |

The screenshots are intended to be read together with the SPL in `../detections/` and the investigation notes in `../investigation/`.
