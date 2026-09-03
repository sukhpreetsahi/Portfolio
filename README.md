# 👋 Hi, I'm Sukhpreet Sahi

🎓 **BSc Cyber Security graduate**  
🔐 **Cybersecurity | Security Operations | Incident Response | Secure Development**

I'm a cybersecurity graduate interested in how attacks can be **detected, investigated and mitigated**, while building software with security considered from the start.

This portfolio contains selected university projects demonstrating practical work across **security operations, incident investigation, secure development, security engineering, machine learning and information security compliance**.

> **Mission:** Integrating security by design rather than as an afterthought.

---

## 🔎 Featured Projects

### 🔎 [Splunk Incident Investigation](./Splunk%20Incident%20Investigation)

A practical SIEM investigation into a Joomla web-server compromise and a ransomware infection using archived system and network logs.

- Reconstructed attack timelines and linked events across multiple log sources
- Identified key indicators of compromise, affected systems and user activity
- Investigated brute-force authentication, malicious file uploads, C2 behaviour and ransomware activity
- Created five Splunk detection rules based on observed attack behaviours
- Mapped attack techniques to MITRE ATT&CK and defensive controls to MITRE D3FEND

**Technologies:** `Splunk` `SPL` `MITRE ATT&CK` `MITRE D3FEND` `Sysmon` `Windows Security Logs`

---

### 🛡️ [DevSecOps Secure Web Application](./DevSecOps%20Web%20Application)

A full-stack Flask e-commerce application demonstrating security integrated into the software development lifecycle.

- Flask backend with role-based access control
- Authentication, sessions and password policy
- PostgreSQL database
- Docker containerisation
- GitHub Actions CI/CD
- Snyk SAST/SCA security scanning
- OWASP ZAP dynamic security testing
- Secrets managed through GitHub Secrets

**Technologies:** `Python` `Flask` `PostgreSQL` `Docker` `GitHub Actions` `Snyk` `OWASP ZAP`

---

### 🤖 [Machine Learning Network Intrusion Detection](./ML%20Network%20Intrusion%20Detection)

A supervised machine-learning project investigating the detection of malicious network traffic using the CIC-IDS2017 benchmark dataset.

- Compared Random Forest and LightGBM classifiers
- Applied correlation filtering and variance-based feature selection
- Addressed class imbalance during model training
- Used RandomizedSearchCV for hyperparameter optimisation
- Evaluated precision, recall, F1-score, false positives and false negatives
- Final LightGBM model achieved approximately **99.9% F1-score** on the held-out benchmark test set

**Technologies:** `Python` `Pandas` `Scikit-learn` `LightGBM` `NumPy` `Jupyter` `CIC-IDS2017`

> The reported performance is a benchmark result on CIC-IDS2017 and is not presented as production-ready intrusion-detection performance.

---

### 📋 [Offline ISO 27001 Policy Compliance Analyser](./AI%20Policy%20Compliance%20Analyser)

A research prototype exploring whether security-policy compliance assessment can be supported through NLP, semantic retrieval and locally hosted language models.

- Compared hybrid semantic similarity and BM25 retrieval against local LLM-based RAG analysis
- Used Sentence Transformer embeddings to identify policy evidence relevant to ISO/IEC 27001:2022 Annex A controls
- Used a locally hosted Llama 3.2 model to assess retrieved policy evidence and identify gaps
- Evaluated the approaches on the original research dataset
- Hybrid similarity achieved **70.37% accuracy** and **0.6281 macro F1**, outperforming the RAG approach on the evaluated dataset
- Designed around offline analysis to avoid sending potentially sensitive policy content to external AI APIs

**Technologies:** `Python` `Sentence Transformers` `BM25` `RAG` `Llama 3.2` `Ollama` `NLP` `ISO/IEC 27001`

> This is a research prototype for decision support, not an ISO certification or replacement for human compliance assessment.

---

### 🦀 [Rust File Integrity Monitor](./Rust%20File%20Integrity%20Monitor)

A Rust-based file integrity monitoring tool that creates file snapshots and compares them across runs to identify suspicious changes.

- SHA-256 hash-based integrity verification
- File creation and deletion detection
- File modification detection
- Possible rename detection using size and hash comparison
- CSV audit logging

**Technologies:** `Rust` `Cargo` `SHA-256` `File I/O`

---

### 🔐 [Secure Investment Management System](./Secure%20Investment%20System)

A client-server investment management system designed around confidentiality, integrity and authenticity requirements.

- Role-based access control
- Multi-factor authentication using password + OTP
- AES-256-GCM authenticated encryption for data at rest
- TLS 1.3 for data in transit
- bcrypt password hashing
- Cryptographically secure random generation
- Secure socket communication

**Technologies:** `Python` `bcrypt` `PyCryptodome` `TLS 1.3` `SMTP`

---

## 🧰 Technical Skills

**Security Operations:** `SIEM` `Incident Response` `Threat Detection` `Digital Forensics` `MITRE ATT&CK` `YARA` `Network Security`

**Security Engineering:** `Secure Coding` `DevSecOps` `Application Security` `Cryptography` `Authentication` `Access Control` `Security Testing`

**Information Security:** `ISO 27001` `Risk Assessment` `Security Controls` `Compliance Analysis`

**Programming:** `Python` `Rust` `JavaScript` `SQL` `Java`

**Tools & Technologies:** `Splunk` `Wireshark` `Ghidra` `Volatility` `GDB` `Docker` `GitHub Actions` `Snyk` `OWASP ZAP` `Flask` `PostgreSQL` `LightGBM`

---

## 🎯 Areas of Interest

- Security Operations & SOC
- Incident Response & Digital Forensics
- Threat Detection & Detection Engineering
- Secure Software Development & DevSecOps
- Security Engineering
- Network Security
- Information Security & GRC
- Applied Machine Learning for Cybersecurity

---

## 📫 Connect

- 💼 **LinkedIn:** [linkedin.com/in/sukhpreet-s-4b5148289](https://www.linkedin.com/in/sukhpreet-s-4b5148289)
- 📧 **Email:** [sukhpreetsahi5@gmail.com](mailto:sukhpreetsahi5@gmail.com)
- 🐙 **GitHub:** [github.com/sukhpreetsahi](https://github.com/sukhpreetsahi)

---

> Building security into systems from the start — not as an afterthought.
