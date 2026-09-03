# Investigation Findings

This section brings together the main findings from the Splunk searches and shows how each one was supported by more than one piece of evidence where possible.

## Finding 1: Automated attack on the Joomla login page

The Joomla administrator page received **412 different password attempts in about 90 seconds** from `23.22.63.114`.

The requests were sent to `/joomla/administrator/index.php` and targeted the `admin` account. The high number of attempts in such a short period makes automated password guessing the most likely explanation.

A later request from `40.80.148.42` successfully logged in and reached the Joomla dashboard. The two source addresses are important because the investigation should follow the events themselves rather than assume that the same address was used for every step.

## Finding 2: Suspicious files were uploaded after the successful login

After the successful Joomla login, the web server received two files called `3791.exe` and `agent.php`.

An executable upload is unusual for a web application and should be treated as high risk. The PHP file is also important because it could be used as server-side code. The timing of the uploads, shortly after the successful login, makes this activity more suspicious than an isolated file upload.

## Finding 3: A document started a script-based ransomware chain

On `we8105desk`, process logs show this sequence:

`Miranda Tate unveiled.dotm` → `wscript.exe` → `20429.vbs` → `121214.tmp`

The process relationships are more useful than the filenames on their own. They show that the document led to a script, which then started another file from a temporary location.

This is a useful detection point because unusual use of scripting tools can be spotted before the final damage takes place.

## Finding 4: The workstation reached the file server over SMB

Network logs show `we8105desk` (`192.168.250.100`) connecting to `we9041srv` (`192.168.250.20`) on TCP/445.

This connection is important because it explains how the ransomware could reach a shared file location. The damage was therefore not limited to the original workstation.

## Finding 5: Large numbers of files were changed very quickly

On `we8105desk`, **406 unique `.txt` files** were affected in about **5.5 minutes**.

On `we9041srv`, **257 unique `.pdf` files** were affected over roughly **10 minutes**.

The scale and speed of the file changes are very different from normal user activity. When combined with the earlier process chain and SMB connection, the evidence strongly supports ransomware behaviour.

## Indicators of compromise

| Type | Value | Why it matters |
|---|---|---|
| Source IP | `23.22.63.114` | High-volume password guessing |
| Source IP | `40.80.148.42` | Successful Joomla login and later upload activity |
| Web payload | `3791.exe` | Suspicious executable upload |
| Web payload | `agent.php` | Suspicious PHP upload |
| Document | `Miranda Tate unveiled.dotm` | Start of the ransomware execution chain |
| Script | `20429.vbs` | Script stage in the execution chain |
| Temporary payload | `121214.tmp` | File started by the script stage |
| Web server | `192.168.250.70` | Joomla server |
| Workstation | `192.168.250.100` | Ransomware execution host |
| File server | `192.168.250.20` | Shared server affected by file encryption |

## Impacted systems

### Web server

`imreallynotbatman.com` at `192.168.250.70` was targeted through its Joomla administrator page. The evidence shows a password attack, a successful login, and suspicious file uploads.

### Workstation

`we8105desk` at `192.168.250.100` was the starting point for the ransomware activity. It ran the malicious document and later connected to the file server.

### File server

`we9041srv` at `192.168.250.20` was reached over SMB and later showed a large number of affected PDF files.

## Defensive priorities

### Protect administrator accounts

Use MFA for important accounts. Add strong password rules and account lockout controls. Limit access to public administration pages where possible.

### Watch file uploads

Alert when executable or server-side script files are uploaded to web servers. File integrity monitoring can also show unexpected changes to important application files.

### Watch scripting tools

Monitor `wscript.exe` and `cscript.exe` for unusual use. A script tool starting a temporary file is a useful warning sign.

### Detect ransomware by behaviour

Look for sudden bursts of file changes, especially when many documents are changed within a short period. This is more useful than relying only on a known malware name or hash.

### Limit SMB access

Only allow systems that need SMB access to reach file servers. Network separation can help stop a compromised workstation from affecting shared storage.

## What this investigation shows

The strongest detections come from combining simple signals. Login volume, password variety, unusual uploads, process relationships, SMB connections, and rapid file changes each provide a useful clue. When they occur together, they give a much clearer picture of the attack.

The SPL files in `../detections/` turn these findings into practical searches that can be tested and adapted for other environments.
