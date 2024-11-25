import getpass
import json
import os

from cryptography.fernet import Fernet

from omnishare.constants import CONFIG_DIR, KEY_FILE, TOKEN_FILE
from omnishare.utils import confirm


def prompt_token():
    return getpass.getpass("Enter your API token: ")


# Ensure the config directory exists
def ensure_config_dir() -> None:
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)


# Generate and save a key (only if it doesn't exist)
def generate_key() -> None:
    if not os.path.exists(KEY_FILE):
        try:
            key = Fernet.generate_key()
            with open(KEY_FILE, "ab") as f:
                f.write(key)
        except Exception as e:
            raise RuntimeError("Failed to generate and save the key") from e


# Load the encryption key
def load_key() -> bytes:
    with open(KEY_FILE, "rb") as f:
        return f.read()


# Save the token securely
def save_token(token_key: str, token_value: str) -> None:
    ensure_config_dir()
    generate_key()  # Ensure key exists
    key = load_key()
    cipher = Fernet(key)
    encrypted_token = cipher.encrypt(token_value.encode())

    # Check and update the token JSON file
    data: dict = {}
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Check if the token key already exists
    token_exists: bool = data.get(token_key)
    override: bool = False

    if token_exists:
        print(f"A token for '{token_key}' already exists.")
        override = confirm("Do you want to override?")

    if override or not token_exists:
        data[token_key] = encrypted_token.decode()
        with open(TOKEN_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("Token saved successfully.")


# Load and decrypt the token
def get_token(token_key: str) -> str:
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError("No token found! Please set up your token first.")

    key = load_key()
    cipher = Fernet(key)

    with open(TOKEN_FILE, "r") as f:
        data = json.load(f)
        encrypted_token = data[token_key]

    return cipher.decrypt(encrypted_token.encode()).decode()


# Delete the key and token file
def delete_token() -> None:
    if os.path.exists(KEY_FILE):
        os.remove(KEY_FILE)
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
