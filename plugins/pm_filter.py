#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
import random
import asyncio
from pyrogram.errors import UserNotParticipant
from utils import get_filter_results, get_file_details, is_subscribed, get_poster
BUTTONS = {}
BOT = {}

RATING = ["5.1/10 | IMDB", "6.2/10 | IMDB", "7.3/10 | IMDB", "8.4/10 | IMDB", "9.5/10 | IMDB", ]
GENRES = ["fun, fact",
         "Thriller, Comedy",
         "Drama, Comedy",
         "Family, Drama",
         "Action, Adventure",
         "Film Noir",
         "Documentary"]
VOTES = ["9221", "303", "56066", "373", "46026", "7736", "1294", "10311", "29458", "372624", "30959", "17725", "25186", "4629", "36926", "463802", "36291", "36281", "294628"]


@Client.on_callback_query()
async def cb_data(bot, update):
    if update.data == "close":
        await update.message.delete()


@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                        ]
                    ] 
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_photo(
                chat_id=message.from_user.id,
                photo="https://telegra.ph/file/ff75af2798e2d3dcc7a91.jpg",
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = [] 
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = file.file_name
                file_size = get_size(file.file_size)
                file_link = f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}"
                btn.append(
                    [
                            InlineKeyboardButton(text=f"{file_name}", url=f"{file_link}"),
                            InlineKeyboardButton(text=f"{file_size}", url=f"{file_link}")
                    ]   
                )          
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAACAgUAAxkBAAID5WFmS1d1T-sETWIs7NgS6C7cAvqIAAKzAwAC3qnpVHxGZ4Q6pqbdHgQ')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📜 1/1",callback_data="pages")]
            )
            
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"**🎬 Title: {search}\n**🌟 Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**🗳️ Votes:** {random.choice(VOTES)}\n🗣️ **Requested BY {message.from_user.mention}\n\n**♻️ {message.chat.title}**", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(f"**🎬 Title: {search}\n**🌟 Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**🗳️ Votes:** {random.choice(VOTES)}\n🗣️ **Requested BY {message.from_user.mention}\n\n**♻️ {message.chat.title}**", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [
                    InlineKeyboardButton(text="• ɢᴏ ᴛᴏ ɴᴇxᴛ ᴘᴀɢᴇ •",callback_data=f"next_0_{keyword}")]
        )
        buttons.append(
            [InlineKeyboardButton(text="ᴘᴀɢᴇ",callback_data="pages"),
             InlineKeyboardButton(text=f"1 - {data['total']}",callback_data="pages"),
             InlineKeyboardButton(text="ᴅᴇʟᴇᴛᴇ",callback_data="close")
            ]
        ) 
        
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>Here is What I Found In My Database For Your Query {search} ‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"**🎬 Title: **{search}**\n🌟 Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**🗳️ Votes:** {random.choice(VOTES)}\n🗣️ **Requested BY {message.from_user.mention}\n\n**★ {message.chat.title} ♻️**", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        
        search = message.text
        result_txt = f"**🎬 Title: **{search}**\n🌟 Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**🗳️ Votes:** {random.choice(VOTES)}\n🗣️ **Requested BY {message.from_user.mention}\n\n**★ {message.chat.title} ♻️**"
       
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                file_name = file.file_name
                file_size = get_size(file.file_size)
                file_link = f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}"
                buttons.append(
                    [
                      InlineKeyboardButton(text="📌 Join On Main Channel📌", url="https://t.me/cv_updatez")]
                )
                btn.append(
                    [
                      InlineKeyboardButton(text=f"{file_name}", url=f"{file_link}"),
                      InlineKeyboardButton(text=f"{file_size}", url=f"{file_link}")
                    ]
                )
        else:
            return
        if not btn:
            return
        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📜 1/1",callback_data="pages")]
            )
            
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"**🎬 Title: **{search}**\n🌟 Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**🗳️ Votes:** {random.choice(VOTES)}\n🗣️ **Requested BY {message.from_user.mention}\n\n**★ {message.chat.title} ♻️**", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(f"**🎬 Title: **{search}**\n🌟 Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**🗳️ Votes:** {random.choice(VOTES)}\n\n**★ {message.chat.title} ♻️**", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [    
               InlineKeyboardButton(text="• ɢᴏ ᴛᴏ ɴᴇxᴛ ᴘᴀɢᴇ •",callback_data=f"next_0_{keyword}")]
        )
        buttons.append(
            [InlineKeyboardButton(text="ᴘᴀɢᴇ",callback_data="pages"),
             InlineKeyboardButton(text=f"1 - {data['total']}",callback_data="pages"),
             InlineKeyboardButton(text="ᴅᴇʟᴇᴛᴇ",callback_data="close")
            ]
        ) 
        
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"**🎬 Title: **{search}**\n🌟 Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**🗳️ Votes:** {random.choice(VOTES)}\n🗣️ **Requested BY {message.from_user.mention}\n\n**★ {message.chat.title} ♻️**", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"**🎬 Title: **{search}**\n🌟 Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**🗳️ Votes:** {random.choice(VOTES)}\n🗣️ **Requested BY {message.from_user.mention}\n\n**★ {message.chat.title} ♻️**", reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = "Bytes", "KB", "MB", "GB", "TB", "PB", "EB"
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [
                        InlineKeyboardButton("☜ 𝐁𝐀𝐂𝐊", callback_data=f"back_{int(index)+1}_{keyword}"),
                        InlineKeyboardButton(f"📜 {int(index)+2}/{data['total']}", callback_data="pages")
                    ]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [
                       InlineKeyboardButton("☜ 𝐁𝐀𝐂𝐊", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ➡️", callback_data=f"next_{int(index)+1}_{keyword}"),
                       InlineKeyboardButton(f"📜 {int(index)+2}/{data['total']}", callback_data="pages")
                    ]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [
                        InlineKeyboardButton("𝐍𝐄𝐗𝐓 ☞", callback_data=f"next_{int(index)-1}_{keyword}"),
                        InlineKeyboardButton(f"📜 {int(index)}/{data['total']}", callback_data="pages")
                    ]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [
                         InlineKeyboardButton("☜ 𝐁𝐀𝐂𝐊", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}"),
                         InlineKeyboardButton(f"📜 {int(index)}/{data['total']}", callback_data="pages")
                    ]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('Update Channel', url='https://t.me/cv_updatez'),
                    InlineKeyboardButton('Source Code', url='https://t.me/nokiyirunnoippokitum')
                ]
                ]
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAACAgQAAxkBAAOZYXTsPU3t8jaR6pnonM8THf3Ip44AAjQMAAK4frlRCj-r5d2VXikeBA', reply_markup=InlineKeyboardMarkup(buttons))



        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('𝐔𝐏𝐃𝐀𝐓𝐄𝐒 ⚒️', url='https://t.me/cv_updatez'),
                        InlineKeyboardButton('𝐉𝐎𝐈𝐍 ♂️', url='https://t.me/CV_Group1')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('New Movies', url='https://t.me/new_movie_z'),
                        InlineKeyboardButton('Update Channel', url='https://t.me/cv_updatez') 
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("ഹായ് {update.from_user.mention}\n സ്വന്തം കാര്യത്തിൽ തലയിട്ടാൽമതി അത് {message.from_user.mention} ഉള്ളതാണു ❕",show_alert=True)
