from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

env = {
    "INNET_CLIENT_NAME": os.getenv("INNET_CLIENT_NAME"),
    "INNET_CLIENT_SECRET": os.getenv("INNET_CLIENT_SECRET"),
    "INNET_HOST": os.getenv("INNET_HOST"),
    "POSTGRES_USER": os.getenv("POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    "POSTGRES_DB": os.getenv("POSTGRES_DB"),
    "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
}

db_url = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (
    env["POSTGRES_USER"],
    env["POSTGRES_PASSWORD"],
    env["POSTGRES_HOST"],
    env["POSTGRES_DB"],
)


def check_env() -> None:
    for key, value in env.items():
        if not value:
            raise ValueError(f"Ensure {key} is set in '.env' file")
