from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

env = {
    "INNET_CLIENT_NAME": os.getenv("INNET_CLIENT_NAME"),
    "INNET_CLIENT_SECRET": os.getenv("INNET_CLIENT_SECRET"),
    "INNET_HOST": os.getenv("INNET_HOST"),
    "API_BASE_URL": os.getenv("API_BASE_URL"),
    "CONNECTOR_API_TOKEN": os.getenv("CONNECTOR_API_TOKEN"),
}


def check_env() -> None:
    for key, value in env.items():
        if not value:
            raise ValueError(f"Ensure {key} is set in '.env' file")
