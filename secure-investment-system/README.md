## MyFinanceInc Secure Investment Management System: 

In this project, a secure investment system has been created, whilst keeping the security of data as a top priority.  

The system is a client-server system and clients contact the server for details, changes, investments and communications.  

The design of the MyFinance Inc. cryptosystem is derived from fundamental security requirements specified in the brief and from essential security principles from legislation and international standards such as UK GDPR, ISO 27001 and NIST. The key objectives of the program are to ensure the confidentiality, integrity, and authenticity of sensitive data.
  
## DEPENDENCIES REQUIRED:
- python3
- bcrypt
- pycryptodomex
- maskpass
- python-dotenv

These can be installed with the command:
"pip install bcrypt pycryptodome maskpass python-dotenv"

## FILES:
- application.py:     This is the main program that runs the CLI
- key_generator.py:   This file generates the symmetric key to encrypt the CSV file holding client data.
- secrets.env: 	      This file contains the symmetric key to encrypt the CSV file and the SMTP server username and password.
- client.py: 	      This file contains the client class and functions to manage clients.
- crypt_tools.py:     This file contains functions to encrypt and decrypt the CSV file, hash passwords and a function to return the symmetric key required for file encryption.
- db_server.py:          This file handles the socket and sending and receiving of messages as the server (company).
- db_server_cert.crt: 	      The self-signed certificate for the server for TLS 1.3 socket.
- db_server_key.key: 	      The private key of the server for TLS 1.3 socket.
 

## HOW TO RUN:
1. Run the db_server.py file.
2. Then run the application.py whilst still having db_server.py running.
3. Register a client, then log in with those credentials. (Ensure a legit email is provided to receive OTP).
(3. The symmetric key to encrypt the CSV file was generated using the key_generator.py file and then inserted into secrets.env. This can be done again if the CSV file hasn't been created
and encrypted yet.)


## IMPORTANT INFORMATION:
To ensure random real-life email addresses aren't sent OTPs, when registering an account, enter emails from a temporary email generator such as temp-mail.org.
For testing purposes, a temporary SMTP server has been created to send OTPs to the emails entered. This can be changed to a real SMTP server in the secrets.env file.

---
The following functions can be tested as they are fully functional in the application.py file:

Homescreen function:
- Register
- Login

Dashboard function:
- View/Edit Own Details
- View Communications  

The other functions aren't functional but are available for future development.

---
## Security Practices Incorporated
- Role-based access control.
- Multi-factor authentication (Password + OTP).
- Encryption of data (CSV files) at rest using AES-256-GCM.
- Encryption of data in transit using TLS 1.3.
- Passwords are hashed, salted and stored using Bcrypt.
- Symmetric Encryption key created using CSPRNG (Pseudo-random number generator).
- Asymmetric private key created based on the P-256 Curve.
- .env files used for storing sensitive keys.

## System Screenshots
<img width="664" height="223" alt="image" src="https://github.com/user-attachments/assets/abedb3fd-8c8a-45c7-928f-fa778ddc9a1c" />
<img width="445" height="411" alt="image" src="https://github.com/user-attachments/assets/82293c24-d3e0-4971-baa1-c3dedd94f563" />  

<img width="490" height="435" alt="image" src="https://github.com/user-attachments/assets/8abc182c-8705-4475-a678-edbd6c0405af" />
