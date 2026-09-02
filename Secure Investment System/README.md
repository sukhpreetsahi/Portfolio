## MyFinanceInc Secure Investment Management System

This project implements a security-focused client-server investment system designed around the confidentiality, integrity and authenticity of sensitive data.

The system uses a client-server architecture for account management, communications and investment-related functionality. The design is informed by security requirements from the project brief and principles from UK GDPR, ISO 27001 and NIST.

## Dependencies Required

- Python 3
- bcrypt
- pycryptodome
- maskpass
- python-dotenv

Install the dependencies with:

```bash
pip install bcrypt pycryptodome maskpass python-dotenv
```

## Files

- `application.py`: Main client CLI application.
- `key_generator.py`: Generates the symmetric key used for AES encryption.
- `client.py`: Client class and functions for managing client information.
- `crypt_tools.py`: AES-GCM encryption/decryption and password hashing functions.
- `db_server.py`: Server-side socket communication and client request handling.
- `db_server_cert.crt`: Local self-signed certificate used for TLS testing.
- `.env.example`: Safe template showing the required environment variables.

Sensitive environment values and TLS private keys are intentionally excluded from the repository.

## Local Configuration

1. Copy `.env.example` to `.env`.
2. Generate an AES key using `key_generator.py` and place its Base64 value in `AES_KEY_B64`.
3. Add the SMTP username and password to the local `.env` file if OTP email functionality is being tested.
4. Generate a local TLS private key matching `db_server_cert.crt`, or create a new local certificate/key pair for testing.

Example using OpenSSL to create a local self-signed certificate and private key:

```bash
openssl req -x509 -newkey rsa:2048 -keyout db_server_key.key -out db_server_cert.crt -days 365 -nodes -subj "/CN=localhost"
```

The generated `db_server_key.key` must remain local and is ignored by Git.

## How to Run

1. Ensure the local `.env` file is configured.
2. Ensure the TLS certificate and private key exist locally.
3. Run `db_server.py`.
4. Run `application.py` while the server is running.
5. Register a client and log in with the credentials.

For OTP testing, use an appropriate test email address and configure the SMTP credentials locally.

---

## Security Practices Incorporated

- Role-based access control.
- Multi-factor authentication (password + OTP).
- Encryption of data at rest using AES-256-GCM.
- Encryption of data in transit using TLS 1.3.
- Passwords are hashed and salted using bcrypt.
- Symmetric encryption keys are generated using a cryptographically secure random number generator.
- P-256 is used for asymmetric key material in the project design.
- Sensitive configuration is supplied through environment variables rather than committed to source control.
- TLS private key material is kept outside version control.

## System Screenshots

<img width="664" height="223" alt="image" src="https://github.com/user-attachments/assets/abedb3fd-8c8a-45c7-928f-fa778ddc9a1c" />
<img width="445" height="411" alt="image" src="https://github.com/user-attachments/assets/82293c24-d3e0-4971-baa1-c3dedd94f563" />

<img width="490" height="435" alt="image" src="https://github.com/user-attachments/assets/8abc182c-8705-4475-a678-edbd6c0405af" />
