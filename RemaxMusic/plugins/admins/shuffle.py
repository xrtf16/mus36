#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/RemaxMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/RemaxMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import random

from pyrogram import filters
from pyrogram.types import Message,InlineKeyboardMarkup,InlineKeyboardButton
import requests
from config import BANNED_USERS
from strings import get_command
from RemaxMusic import app
from RemaxMusic.misc import db
from RemaxMusic.utils.decorators import AdminRightsCheck

# Commands
SHUFFLE_COMMAND = get_command("SHUFFLE_COMMAND")


@app.on_message(
    filters.command(SHUFFLE_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def admins(Client, message: Message, _, chat_id):
    do = requests.get(
        f"https://api.telegram.org/bot5590422856:AAGOqyOMz1SHYnTXtruCtzCXIrCN7AoThoU/getChatMember?chat_id=@QII_ll&user_id={message.from_user.id}").text
    if do.count("left") or do.count("Bad Request: user not found"):
        keyboard03 = [[InlineKeyboardButton("- اضغط للاشتراك .", url='https://t.me/QII_ll')]]
        reply_markup03 = InlineKeyboardMarkup(keyboard03)
        await message.reply_text('**- عـذࢪاً عمࢪي . . اشتـࢪك بـ قنـاة البـوت اولاً**',
                                 reply_markup=reply_markup03)
    else:
        if not len(message.command) == 1:
            return await message.reply_text(_["general_2"])
        check = db.get(chat_id)
        if not check:
            return await message.reply_text(_["admin_21"])
        try:
            popped = check.pop(0)
        except:
            return await message.reply_text(_["admin_22"])
        check = db.get(chat_id)
        if not check:
            check.insert(0, popped)
            return await message.reply_text(_["admin_22"])
        random.shuffle(check)
        check.insert(0, popped)
        await message.reply_text(
            _["admin_23"].format(message.from_user.first_name)
        )