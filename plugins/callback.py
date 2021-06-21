import os
from pyrogram import Client
from dotenv import load_dotenv
from helper.texts import capupload_text
from Japanemi_features.episodes import episodes
from Japanemi_features.anime_ import Downcap, foriter

load_dotenv()
CHANNEL_ID = os.getenv("channel_id")
AUTH_USERS_STR = os.getenv("AUTH_USERS")
AUTH_USERS = [int(i) for i in AUTH_USERS_STR.split(" ")]


@Client.on_callback_query()
async def callback_data(bot, update):
    chat_id = update.from_user.id
    message_id = update.message.message_id
    if chat_id in AUTH_USERS:
        data = update.data
        if "!" in data:
            data = int(data.split("!")[0])
            actu = await episodes()
            title = actu["titles"][data]
            links = Downcap(actu["episodes"][data]).get_url()
            path = await foriter(links, f"./Downloads/{chat_id}/")
            caption = await capupload_text(title)
            await bot.send_video(chat_id=chat_id,
                                 video=path,
                                 caption=caption)
    else:
        pass
