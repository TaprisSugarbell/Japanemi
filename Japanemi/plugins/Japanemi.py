import os
from ..helper.buttons import buttons
from pyrogram import Client, filters
from ..helper.__vars__ import auth_users_async


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
    AUTH_USERS = await auth_users_async()
    if user in AUTH_USERS:
        await anime(bot, update)
    else:
        pass

