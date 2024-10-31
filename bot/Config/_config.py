import time
import os 

TOKEN = os.environ.get('TOKEN')
TOKEN2 = os.environ.get('TOKEN2')
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
WEBHOOK_URL = os.environ.get('Webhook_url', None)
DATABASE_URL = os.environ.get('DATABASE_URL', None)
PORT = os.environ.get('PORT', None)

START_IMG = 'https://telegra.ph/file/907f8f24b3224343abe4e.jpg'
SEARCHING_IMGS = [
    'https://telegra.ph/file/d8bad077c03eede2cf1a7.jpg', 
    'https://telegra.ph/file/ba718f278b4dc1300aaf1.jpg',
    'https://telegra.ph/file/d3a49440dc046782825ea.jpg',
]


START_TIME = int(time.time())

SUDO_USERS = [5040666523,5844258081,7029204818]

MAIN_CHANNEL: int = -1002330710763
MAIN_GROUP: int = -1002194459452
GROUPS = [MAIN_GROUP,-1004515528181,-1002355907966]
DISCUSSION_GROUP: int = -1001885188788
LECCH_CHAT: int = -1001885188788
MOVIE_STORE: int = -1002230466521
TV_STORE: int = -1001885188788
FILTER_CHAT: int  = -1001885188788

FORCE_SUB_CHAT: int = -1002330710763
FORCE_SUB_CHAT_LINK: str = 'https://t.me/infinity_updates'

BOT_CHAT = -1002223278128
INBOX = 3
REQUEST = 2



