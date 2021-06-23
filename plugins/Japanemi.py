import os
from helper.buttons import *
from dotenv import load_dotenv
from pyrogram import Client, filters


load_dotenv()
AUTH_USERS_STR = os.getenv("AUTH_USERS")
AUTH_USERS = [int(i) for i in AUTH_USERS_STR.split(" ")]


async def anime(bot, update):
    chat_id = update.chat.id
    message_id = update.message_id
    inline = await buttons()
    await bot.send_message(chat_id=chat_id,
                           text="Ultimos episodios",
                           reply_markup=inline,
                           reply_to_message_id=message_id)


@Client.on_message(filters.command(["on"]))
async def load(bot, update):
    chat_id = update.chat.id
    if chat_id in AUTH_USERS:
        await anime(bot, update)
    else:
        pass

