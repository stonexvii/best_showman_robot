import os

import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
PROXY = os.getenv('PROXY')
MAX_MESSAGE = 3
