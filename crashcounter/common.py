import os
from dotenv import load_dotenv


def get_secret(key: str) -> str:
    load_dotenv()
    secret = os.getenv(key)
    if secret is None:
        raise ValueError(f"Secret {key} not found in environment variables.")

    return secret
