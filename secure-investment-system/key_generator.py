# key_generator.py

# Run once to generate the AES key for the secrets.env file.
# This script generates a secure 256-bit (32-byte) AES key and prints its
# Base64 encoded. The key is the output line and is to be copied into secrets.env.

# Re-running this generates a NEW key, which won't decrypt data encrypted with the old key.
import base64
from Crypto.Random import get_random_bytes


def generate_key_for_env():
    """Generates and prints a Base64 encoded key for .env file."""
    print("Generating new AES-256 key...")
    
    # Generate 32 bytes for AES-256
    data_rest_key = get_random_bytes(32)
    
    # Encode bytes to Base64 string
    key_b64 = base64.b64encode(data_rest_key).decode('utf-8')
    print(f"AES_KEY_B64={key_b64}")

    # Save binary key to file for backup in case the key isn't added to secrets.env
    # or if the secrets.env is deleted.
    try:
        with open("encryptfile.key.backup", "wb") as f:
            f.write(data_rest_key)
            print("Binary key also saved to encryptfile.key.backup for backup.")
    except IOError as e:
        print(f"Could not create binary key backup file: {e}")


if __name__ == '__main__':
    generate_key_for_env()