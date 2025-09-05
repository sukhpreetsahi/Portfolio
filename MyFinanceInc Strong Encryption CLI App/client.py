import json
import socket
import ssl


class Client:
    def __init__(self, username, contact_info, password=None):
        self.__username = username
        self.__password = password
        self.__contact_info = contact_info

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_contact_info(self):
        return self.__contact_info

    def set_fname(self, fname):
        self.__contact_info[0] = fname

    def set_lname(self, lname):
        self.__contact_info[1] = lname

    def set_email(self, email):
        self.__contact_info[2] = email

    def get_email(self):
        return self.__contact_info[2]

    def set_number(self, number):
        self.__contact_info[3] = number

    def set_password(self, password):
        self.__password = password


def serialise_list(contact_info_list):
    """
    Changes the , in the list to | to stop problems occuring when coverting message to csvDict
    """
    return '|'.join(contact_info_list)


def deserialise_list(contact_info_str):
    """
    Changes | back to , to store back as list.
    """
    return contact_info_str.split('|')


def check_username(username):
    """
    Checks if username passed through exists in the csv file in the server
    """
    try:
        with socket.create_connection(('localhost', 4443)) as sock:
            # SSL setup
            context = ssl._create_unverified_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_3  # TLS 1.3

            with context.wrap_socket(sock, server_hostname='localhost') as secure_sock:
                secure_sock.send(f'CHECK_USERNAME,{username}'.encode())
                response = secure_sock.recv(4096)
                return response.decode()
    except:
        return "Error communicating with server"


def register_client(client, password):
    """
    Sends registered account to server to store in csv file
    """
    try:
        with socket.create_connection(('localhost', 4443)) as sock:
            # SSL setup
            context = ssl._create_unverified_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_3  # TLS 1.3

            with context.wrap_socket(sock, server_hostname='localhost') as secure_sock:
                secure_sock.send(
                    f'REGISTER,{client.get_username()},{json.dumps(serialise_list(client.get_contact_info()))},{password}'.encode())
                response = secure_sock.recv(4096)
                _, hashed_password = response.decode().split(',')
                client.set_password(hashed_password) # Set the hashed password in the client object
            return response.decode()
    except:
        return "Error communicating with server"


def attempt_login(username, password):
    """
    Checks if username and password match in the csv file in server.
    """
    try:
        with socket.create_connection(('localhost', 4443)) as sock:
            # SSL setup
            context = ssl._create_unverified_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_3  # TLS 1.3

            with context.wrap_socket(sock, server_hostname='localhost') as secure_sock:
                secure_sock.send(f'LOGIN,{username},{password}'.encode())
                response = secure_sock.recv(4096)
                return response.decode()
    except:
        return "Error communicating with server"


def otp_sender(client):
    """
    Request for OTP
    """
    try:
        with socket.create_connection(('localhost', 4443)) as sock:
            # SSL setup
            context = ssl._create_unverified_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_3  # TLS 1.3

            with context.wrap_socket(sock, server_hostname='localhost') as secure_sock:
                secure_sock.send(f'OTP_REQUEST,{client.get_email()}'.encode())
                response = secure_sock.recv(4096)
                return response.decode()
    except:
        return "Error communicating with server"


def check_otp(otp):
    """
    Requests server to check entered OTP matches the OTP sent by server
    """
    try:
        with socket.create_connection(('localhost', 4443)) as sock:
            # SSL setup
            context = ssl._create_unverified_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_3  # TLS 1.3

            with context.wrap_socket(sock, server_hostname='localhost') as secure_sock:
                secure_sock.send(f'OTP_TRY,{otp}'.encode())
                response = secure_sock.recv(4096)
                return response.decode()
    except:
        return "Error communicating with server"


def modify(client, new_password=None):
    """
    Sends server the modified details of client to update in the server
    """
    try:
        with socket.create_connection(('localhost', 4443)) as sock:
            # SSL setup
            context = ssl._create_unverified_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_3  # TLS 1.3

            with context.wrap_socket(sock, server_hostname='localhost') as secure_sock:
                if new_password is None:
                    secure_sock.send(
                        f'MODIFY,{client.get_username()},{json.dumps(serialise_list(client.get_contact_info()))},{client.get_password()}'.encode())
                    response = secure_sock.recv(4096).decode()
                else:
                    secure_sock.send(
                    f'MODIFYPWD,{client.get_username()},{json.dumps(serialise_list(client.get_contact_info()))},{new_password}'.encode())
                    response, hashed_password = secure_sock.recv(4096).decode().split(',')
                    client.set_password(hashed_password)  # Set the hashed password in the client object
            return response
    except:
        return "Error communicating with server"


def communicate():
    """
    Sends a request to server to receive communications
    """
    try:
        with socket.create_connection(('localhost', 4443)) as sock:
            # SSL setup
            context = ssl._create_unverified_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_3  # TLS 1.3
            with context.wrap_socket(sock, server_hostname='localhost') as secure_sock:
                secure_sock.send(f'COMMUNICATIONS'.encode())
                response = secure_sock.recv(4096)
            return response.decode()
    except:
        return "Error communicating with server"
