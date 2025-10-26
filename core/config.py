import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment manager
env = environ.Env()

# Try to find .env file in multiple possible locations
env_path = os.path.join(BASE_DIR, '.env')

# DJANGO CORE SETTINGS
SECRET_KEY = env('SECRET_KEY', default='unsafe-secret-key')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# DATABASE SETTINGS
DB_NAME = env('DB_NAME', default='myproject')
DB_USER = env('DB_USER', default='myuser')
DB_PASSWORD = env('DB_PASSWORD', default='mypassword')
DB_HOST = env('DB_HOST', default='127.0.0.1')
DB_PORT = env('DB_PORT', default='5432')

# telegram bot
TELEGRAM_BOT_TOKEN = '7933839705:AAFHYePhouFXF4Or4J_FM-KFGHBTzZ_dB3g'
TELEGRAM_CHANNEL_ID = '-1002309236825'
#devise_id
#devise_model, language, devise_vesion, jwt_token, user   jpt(i just wonna create jwt )