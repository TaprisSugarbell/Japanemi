import os
from .. import AUTH_USERS
from ..helper.buttons import buttons
from pyrogram import Client, filters


async def anime(bot, update):
    chat_id = update.chat.id
    message_id = update.message_id
    inline = await buttons()
    await bot.send_message(chat_id=chat_id,
                           text="Que buscas?",
                           reply_markup=inline,
                           reply_to_message_id=message_id)


@Client.on_message(filters.command(["on"]))
async def load(bot, update):
    user = update.from_user.id
    if user in AUTH_USERS:
        await anime(bot, update)
    else:
        pass

