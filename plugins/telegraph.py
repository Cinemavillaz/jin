
import os
import time
import math
import json
import string
import random
import traceback
import asyncio
import datetime
import aiofiles
from random import choice
from telegraph import upload_file

@Client.on_message(filters.command("telegraph"))
async def start(bot, message):
    reply = message.reply_to_message

    if not reply or not reply.text:
        return await message.reply("Reply to a text message")

