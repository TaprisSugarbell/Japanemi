import os
from shutil import rmtree
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
    # Carpeta
    tmp_directory = "./Downloads/" + str(update.from_user.id) + "/"
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    if chat_id in AUTH_USERS:
        data = update.data
        if "!" in data:
            data = int(data.split("!")[0])
            actu = await episodes()
            title = actu["titles"][data]
            links = Downcap(actu["episodes"][data]).get_url()
            path = await foriter(links, tmp_directory)
            caption = await capupload_text(title)
            try:
                list_dir_ = os.listdir(tmp_directory)
                print(list_dir_)
                if "thumb.jpg" in list_dir_:
                    yes_thumb = True
                else:
                    yes_thumb = False
            except Exception as e:
                yes_thumb = False
                print(e)
            if yes_thumb:
                await bot.send_video(chat_id=chat_id,
                                     video=path,
                                     thumb=f"{tmp_directory}thumb.jpg",
                                     caption=caption)
            else:
                await bot.send_video(chat_id=chat_id,
                                     video=path,
                                     caption=caption)
            rmtree(tmp_directory)
    else:
        pass
