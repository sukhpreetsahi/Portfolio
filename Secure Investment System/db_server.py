import socket
import ssl
import csv
import os
from crypt_tools import return_key, encrypt_data, decrypt_data, hash_password
import bcrypt
import random
from email.message import EmailMessage
import smtplib
import threading
from dotenv import load_dotenv
import base64

load_dotenv()
_loaded_aes_key = None

SMTP_SERVER = 'smtp.mailersend.net'
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get('SMTP_USER')
SENDER_PASSWORD = os.environ.get('SMTP_PASS')

# For local development, generate a self-signed certificate and private key.
# Private key material is intentionally excluded from version control.
TLS_CERT_FILE = os.environ.get('TLS_CERT_FILE', 'db_server_cert.crt')
TLS_KEY_FILE = os.environ.get('TLS_KEY_FILE', 'db_server_key.key')

def load_aes_key():
    global _loaded_aes_key
    if _loaded_aes_key is None:
        key_b64 = os.environ.get('AES_KEY_B64')
        if not key_b64:
            raise ValueError("AES_KEY_B64 not found in environment variables. Create a local .env file from .env.example.")
        try:
            _loaded_aes_key = base64.b64decode(key_b64)
            if len(_loaded_aes_key) != 32:
                raise ValueError("Decoded AES key is not 32 bytes long.")
        except Exception as e:
            raise ValueError(f"Error decoding AES key: {e}")
    return _loaded_aes_key

class Session:
    def __init__(self):
        self.__otp = ''
        self.__username = ''
        self.__communications = ["Gamazon.Inc stocks fallen by 5%"]

    def get_otp(self):
        return self.__otp

    def get_username(self):
        return self.__username

    def set_otp(self, otp):
        self.__otp = otp

    def set_username(self, username):
        self.__username = username

    def add_communications(self, message):
        self.__communications.append(message)

    def get_communications(self):
        return self.__communications

def serialise_list(contact_info_list):
    return '|'.join(contact_info_list)

def deserialise_list(contact_info_str):
    return contact_info_str.split('|')

def add_client(client, key=return_key(), filename='clients.csv.enc'):
    if not os.path.exists(filename):
        rows = ["username,contact_info,hashed_password"]
        row = f"{client[0]},{client[1]},{client[2]}"
        rows.append(row)
        csv_data = "\n".join(rows)
        encrypted_data = encrypt_data(csv_data, key)
        with open(filename, "wb") as f:
            f.write(encrypted_data)
    else:
        clients_data = load_clients()
        rows = ["username,contact_info,hashed_password"]
        for row in clients_data:
            rows.append(f"{row['username']},{row['contact_info']},{row['hashed_password']}")
        rows.append(f"{client[0]},{client[1]},{client[2]}")
        csv_data = "\n".join(rows)
        encrypted_data = encrypt_data(csv_data, key)
        with open(filename, "wb") as f:
            f.write(encrypted_data)

def modify_clients(client, key=return_key(), filename='clients.csv.enc'):
    clients_data = load_clients()
    modified_rows = ["username,contact_info,hashed_password"]
    for row in clients_data:
        if row['username'] == client[0]:
            row['contact_info'] = client[1]
            row['hashed_password'] = client[2]
        modified_rows.append(f"{row['username']},{row['contact_info']}, {row['hashed_password']}")
    modified_csv_data = "\n".join(modified_rows)
    encrypted_data = encrypt_data(modified_csv_data, key)
    with open(filename, "wb") as f:
        f.write(encrypted_data)

def load_clients(key=return_key(), filename='clients.csv.enc'):
    if not os.path.exists(filename):
        return []
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = decrypt_data(encrypted_data, key)
    if decrypted_data is None:
        print("Decryption failed. Data may be corrupted or invalid key.")
        return []
    lines = decrypted_data.decode().strip().split("\n")
    reader = csv.DictReader(lines)
    clients = []
    for row in reader:
        clients.append({
            'username': row['username'],
            'contact_info': row['contact_info'],
            'hashed_password': row['hashed_password'].strip()})
    return clients

def check_client_exists(username):
    try:
        for row in load_clients():
            if row["username"] == username:
                return True
    except:
        return False

def check_login(username, password):
    try:
        for row in load_clients():
            if row["username"] == username:
                if bcrypt.checkpw(password.encode(), row["hashed_password"].encode()):
                    return row
                else:
                    return False
        return False
    except:
        return False

def otp_sender(client):
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("OTP Error: SMTP credentials not configured.")
        return False
    otp = ''
    for loop in range(6):
        otp += str(random.randint(0, 9))
    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}"
    em = EmailMessage()
    em['From'] = SENDER_EMAIL
    em['To'] = client
    em['Subject'] = subject
    em.set_content(body)
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(em)
        return otp
    except:
        return False

def handle_client(connstream, current_session):
    try:
        data = connstream.recv(4096).decode()
        if data.startswith('CHECK_USERNAME'):
            _, username = data.split(',')
            print(f'Checking username exists: {username}')
            if check_client_exists(username):
                print(f'Sending username already exists')
                connstream.send(b'USERNAME_EXISTS')
                print("\nEnter a communication message to add: ", end="")
            else:
                print("Sending username is available to use")
                connstream.send(b'USERNAME_AVAILABLE')
                print("\nEnter a communication message to add: ", end="")
        elif data.startswith('REGISTER'):
            _, username, contact_info, password, = data.split(',')
            print("Attempting to register user")
            hashed_password = hash_password(password).decode()
            add_client([username, contact_info, hashed_password])
            connstream.send(f'REGISTRATION_SUCCESS,{hashed_password}'.encode())
            print("User registered")
            print("\nEnter a communication message to add: ", end="")
        elif data.startswith('LOGIN'):
            _, username, password = data.split(',')
            print("Checking if username and password match")
            if check_login(username, password):
                row = check_login(username, password)
                message = f'LOGIN_SUCCESS,{row}'
                print("Username and password match")
                print("\nEnter a communication message to add: ", end="")
                connstream.send(message.encode())
                current_session.set_username(username)
            else:
                print("Username and password don't match")
                connstream.send(b'LOGIN_FAILED')
                print("\nEnter a communication message to add: ", end="")
        elif data.startswith('OTP_REQUEST'):
            _, email, = data.split(',')
            print("Requesting OTP from SMTP server")
            value = otp_sender(email)
            current_session.set_otp(value)
            if value != False:
                print(f"OTP sent to {email}")
                print("\nEnter a communication message to add: ", end="")
                connstream.send('OTP_SENT'.encode())
            else:
                print(f"OTP couldn't be sent to {email}")
                print("\nEnter a communication message to add: ", end="")
                connstream.send('OTP_FAIL'.encode())
        elif data.startswith('OTP_TRY'):
            _, otp_guess = data.split(',')
            print("Checking if OTP entered is correct")
            value = otp_guess
            if value == current_session.get_otp():
                print("OTP entered is correct")
                print("\nEnter a communication message to add: ", end="")
                connstream.send('OTP_SUCCESS'.encode())
            else:
                print("OTP entered is incorrect")
                print("\nEnter a communication message to add: ", end="")
                connstream.send('OTP_WRONG'.encode())
        elif data.startswith('MODIFYPWD'):
            print("Request to modify client password details received")
            _, username, contact_info, password, = data.split(',')
            hashed_password = hash_password(password).decode()
            modify_clients([username, contact_info, hashed_password])
            connstream.send(f'SAVED, {hashed_password}'.encode())
            print("Modified details")
            print("\nEnter a communication message to add: ", end="")
        elif data.startswith('MODIFY'):
            print("Request to modify client details received")
            _, username, contact_info, password, = data.split(',')
            modify_clients([username, contact_info, password])
            connstream.send(b'SAVED')
            print("Modified details")
            print("\nEnter a communication message to add: ", end="")
        elif data.startswith('COMMUNICATIONS'):
            print("Request to send communications to client")
            preset_communications = "\n".join(current_session.get_communications())
            response = (preset_communications)
            connstream.send(response.encode())
            print("Communications sent")
            print("\nEnter a communication message to add: ", end="")
        else:
            print("Invalid request arrived")
            connstream.send(b'INVALID_REQUEST')
            print("\nEnter a communication message to add: ", end="")
    except:
        print("Error handling client request")
        print("\nEnter a communication message to add: ", end="")

def add_communication_thread(current_session):
    while True:
        string = f"\nCommunications list: {str(current_session.get_communications())}"
        print(string)
        print("Enter a communication message to add: ", end="")
        entry = input("")
        if entry:
            print(f"Message added to communications list: {entry}")
            current_session.add_communications(entry)

def main():
    current_session = Session()
    bindsocket = socket.socket()
    bindsocket.bind(('127.0.0.1', 4443))
    bindsocket.listen(5)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.load_cert_chain(certfile=TLS_CERT_FILE, keyfile=TLS_KEY_FILE)
    print(f"Server is listening on {bindsocket.getsockname()}...")
    threading.Thread(target=add_communication_thread, args=(current_session,), daemon=True).start()
    while True:
        newsocket, fromaddr = bindsocket.accept()
        print("\nConnected")
        connstream = context.wrap_socket(newsocket, server_side=True)
        try:
            handle_client(connstream, current_session)
        finally:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()

if __name__ == '__main__':
    main()
