import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
TELEGRAM_KEY = os.environ.get('TELEGRAM_TOKEN')

ASKING_SELLER, ASKING_CLIENT = range(2)
