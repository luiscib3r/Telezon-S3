import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()

logger = uvicorn.logging.logging.getLogger("uvicorn")


# ENVIRONMENT = os.getenv("ENVIRONMENT")
PROJECT_NAME = os.getenv("PROJECT_NAME")
PORT = int(os.getenv("PORT"))

SECRET_KEY = os.getenv("SECRET_KEY")

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

DATABASE_NAME = os.getenv("DATABASE_NAME")

if MONGO_USER and MONGO_PASSWORD:
    AUTH_URL = f"{MONGO_USER}:{MONGO_PASSWORD}@"
else:
    AUTH_URL = ""

DATABASE_URL = (
    os.getenv("DATABASE_URL") or f"mongodb://{AUTH_URL}{MONGO_HOST}:{MONGO_PORT}"
)

API_KEY = os.getenv("API_KEY")

TOKEN = os.getenv("BOT_TOKEN")
CID = os.getenv("CID")

TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

INITIAL_ADMIN_USER = os.getenv("INITIAL_ADMIN_USER")
INITIAL_ADMIN_PASSWORD = os.getenv("INITIAL_ADMIN_PASSWORD")
