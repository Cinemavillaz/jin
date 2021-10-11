from info import ADMINS

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(ADMINS)
