from info import ADMINS
import os

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(ADMINS)
async def start(client, message):
       insert(int(message.chat.id))
    )
