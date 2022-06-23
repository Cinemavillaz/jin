import re
from os import environ
import os

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))

class Config(object):

      BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
      API_ID = int(os.environ.get("API_ID", 12345))
      API_HASH = os.environ.get("API_HASH")

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ['ADMINS'].split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ['CHANNELS'].split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel
AUTH_GROUPS = [int(admin) for admin in environ.get("AUTH_GROUPS", "").split()]

# MongoDB information
DATABASE_URI = environ['DATABASE_URI']
DATABASE_NAME = environ['DATABASE_NAME']
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# Messages
START_MSG = """
<i>𝖧ey {bot.from_user.mention},

𝖨 𝖺𝗆 𝖺𝗇 𝖠𝖽𝗏𝖺𝗇𝖼𝖾𝖽 𝖠𝗎𝗍𝗈-𝖿𝗂𝗅𝗍𝖾𝗋 𝖻𝗈𝗍, 𝖠𝖽𝖽 𝗆𝖾 𝗍𝗈 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉 , 𝗆𝖺𝗄𝖾 𝗆𝖾 𝖺𝖽𝗆𝗂𝗇 𝖺𝗇𝖽 𝗌𝖾𝖾 𝗆𝗒 𝗉𝗈𝗐𝖾𝗋...😝🔥</i>
"""
FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "")
OMDB_API_KEY = environ.get("OMDB_API_KEY", "")
if FILE_CAPTION.strip() == "":
    CUSTOM_FILE_CAPTION=None
else:
    CUSTOM_FILE_CAPTION=FILE_CAPTION
if OMDB_API_KEY.strip() == "":
    API_KEY=None
else:
    API_KEY=OMDB_API_KEY
