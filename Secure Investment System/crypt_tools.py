from Crypto.Cipher import AES
import bcrypt
import os
import base64
from dotenv import load_dotenv

load_dotenv()
_loaded_aes_key = None

def return_key():
    """
    Loads the AES key from the environment variable.
    Decodes it from Base64.
    Raises Error if the key is missing or invalid.
    """
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
            raise ValueError(f"Error decoding AES key from Base64: {e}")
    return _loaded_aes_key

def encrypt_data(data, key=None):
    """
    Encrypts data passed in using the loaded AES key.
    """
    if key is None:
        key = return_key()
    cipher = AES.new(key, AES.MODE_GCM)
    encrypted_data, tag = cipher.encrypt_and_digest(data.encode())
    return cipher.nonce + tag + encrypted_data

def decrypt_data(data, key=None):
    """
    Decrypts data passed in using the loaded AES key.
    """
    if key is None:
        key = return_key()

    if len(data) < 32:
        raise ValueError("Invalid encrypted data length.")

    nonce = data[:16]
    tag = data[16:32]
    encrypted_data = data[32:]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(encrypted_data, tag)
        return plaintext
    except ValueError:
        print("Decryption failed: Data may be corrupted or key incorrect.")
        return None

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
