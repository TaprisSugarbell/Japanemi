import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pyrogram import Client, filters
from Japanemi_features.episodes import episodes
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
AUTH_USERS_STR = os.getenv("AUTH_USERS")
AUTH_USERS = [int(i) for i in AUTH_USERS_STR.split(" ")]


async def anime(bot, update):
    chat_id = update.chat.id
    message_id = update.message_id
    actu = await episodes()
    title = actu["titles"]
    stress = [InlineKeyboardButton(f"{title[i]}",
                                   callback_data=f"{i}!") for i in range(len(title))]
    pairs = [stress[i: (i + 1)] for i in range((len(stress)))]
    round_num = len(stress)
    calc = len(stress) - round(round_num)
    if calc == 1:
        pairs.append((stress[-1],))
    elif calc == 2:
        pairs.append((stress[-1],))
    inline = InlineKeyboardMarkup(pairs[:9])
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

