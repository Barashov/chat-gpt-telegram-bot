import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
TELEGRAM_KEY = os.environ.get('TELEGRAM_TOKEN')

MODEL = os.environ.get('MODEL', 'gpt-3.5-turbo-16k')
TEMPERATURE = 0.1
