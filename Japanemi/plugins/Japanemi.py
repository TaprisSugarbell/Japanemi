import os
from decouple import config
from ..helper.buttons import buttons
from pyrogram import Client, filters

AUTH_USERS = [int(i) for i in config("AUTH_USERS", default="784148805").split(" ")]


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

