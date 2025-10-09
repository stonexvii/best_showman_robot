import dotenv
import os

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
PROXY = os.getenv('PROXY')
MODERATOR_ID = int(os.getenv('MODERATOR_ID'))
REDIS_URL = os.getenv('REDIS_URL')

