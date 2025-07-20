from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("ENCRYPTION_KEY")
if key is None:
    raise ValueError("ENCRYPTION_KEY not set in environment variables")

fernet = Fernet(key.encode())

def encrypt_api_key(api_key: str) -> str:
    return fernet.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_api: str) -> str:
    return fernet.decrypt(encrypted_api.encode()).decode()
