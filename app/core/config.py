import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT')
PROJECT_NAME = os.getenv('PROJECT_NAME')
PORT = int(os.getenv('PORT'))

SECRET_KEY = os.getenv('SECRET_KEY')

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

DATABASE_NAME = os.getenv('DATABASE_NAME')

DATABASE_URL = os.getenv(
    'DATABASE_URL'
) or f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{DATABASE_NAME}'

DEVELOPMENT_DATABASE = f'mongodb://127.0.0.1:27017/{DATABASE_NAME}'

API_KEY = os.getenv('API_KEY')

TOKEN = os.getenv('BOT_TOKEN')
CID = os.getenv('CID')

TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
SESSION_STRING = os.getenv('SESSION_STRING')
