# Investigation Findings

This section brings together the main findings from the investigation. Each finding starts with what was seen in the logs, followed by why it matters and what could be done with the result.

## Finding 1: Automated password guessing

The Joomla administrator page received **412 unique password attempts in about 90 seconds** from `23.22.63.114`.

The requests were sent to `/joomla/administrator/index.php` and targeted the `admin` account. The number of attempts in such a short period makes automated password guessing much more likely than normal administrator use.

A later login from `40.80.148.42` used the correct password and reached the Joomla dashboard. This is a useful example of why an investigation should look at the events before and after a login rather than looking at one IP address on its own.

## Finding 2: Files were uploaded after access was gained

After the successful Joomla login, two files were uploaded to the web server:

- `3791.exe`
- `agent.php`

An executable file in a web upload is a strong warning sign. The PHP file is also important because it could be used as server-side code.

The timing of the upload after the successful login gives a clear link between the login activity and the later server changes.

## Finding 3: A document led to a scripted payload

On `we8105desk`, the process data showed this sequence:

```text
Miranda Tate unveiled.dotm
        |
        v
    wscript.exe
        |
        v
    20429.vbs
        |
        v
    121214.tmp
```

The important point is the order of execution. The document started the chain, `wscript.exe` ran the script, and the script then started the temporary payload.

The name `121214.tmp` by itself does not prove that the file was malicious. The parent-child process relationship is much stronger evidence because it shows how the file was started.

## Finding 4: The workstation reached the file server over SMB

`we8105desk` (`192.168.250.100`) connected to `we9041srv` (`192.168.250.20`) on TCP/445.

TCP/445 is used by SMB, which allows Windows systems to access files and shares over the network. This connection matters because file changes were later seen on the file server.

This helped show that the ransomware activity was not limited to the workstation.

## Finding 5: A large number of files were changed very quickly

On the workstation, **406 unique `.txt` files** were affected in about **5.5 minutes**.

On `we9041srv`, **257 unique `.pdf` files** were affected over roughly **10 minutes**.

The speed and volume of the file changes are a strong sign of automated file encryption. This type of behaviour is useful for detection because it does not rely on a known ransomware file name or hash.

## Indicators of compromise

| Type | Value | Where it fits |
|---|---|---|
| IP address | `23.22.63.114` | High-volume Joomla password guessing |
| IP address | `40.80.148.42` | Successful Joomla login and later upload activity |
| Web file | `3791.exe` | Uploaded executable |
| Web file | `agent.php` | Uploaded PHP file |
| Document | `Miranda Tate unveiled.dotm` | Start of the ransomware execution chain |
| Script | `20429.vbs` | Script stage of the chain |
| Temp file | `121214.tmp` | Payload started by the script |
| Web server | `192.168.250.70` | Joomla server |
| Workstation | `192.168.250.100` | Ransomware execution host |
| File server | `192.168.250.20` | Server affected through SMB |

## What I would improve

### Protect the Joomla administrator account

Use MFA, strong passwords, and account lockout. The administrator page should also be restricted so that it is not open to unnecessary internet traffic.

### Watch web uploads

Alert when executable or server-side script files are uploaded to web directories. File integrity monitoring would also help show when application files change unexpectedly.

### Control script tools

Monitor `wscript.exe` and `cscript.exe`. A script tool starting an unusual temporary file is a useful signal and should receive extra attention.

### Detect file encryption early

Look for a sudden rise in document changes from one system or one process. A rule based on behaviour can still work when the malware uses a new name or hash.

### Limit SMB access

Only allow systems that need SMB to reach the relevant file servers. This can reduce the amount of damage a compromised workstation can cause.

## Detection lessons

The most useful signals from this investigation were simple behaviours:

- many login attempts in a short time
- unusual upload file types
- suspicious process chains
- repeated outbound connections
- SMB access
- large numbers of file changes in a short period

These behaviours are covered by the SPL files in `../detections/`.
