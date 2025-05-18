import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_KEY = os.getenv('TELEGRAM_TOKEN')
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8443))
APP_PORT = int(os.getenv("APP_PORT", 8080))
MARKET_CAP_THRESHOLD = int(os.getenv("MARKET_CAP_THRESHOLD", 1000000))
CURRENCY_WATCHED = os.getenv("CURRENCY_WATCHED")
