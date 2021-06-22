import os
import random
import string
from shutil import rmtree
from pyrogram import Client
from dotenv import load_dotenv
from plugins.Japanemi import buttons
from helper.texts import capupload_text
from moviepy.editor import VideoFileClip
from Japanemi_features.episodes import episodes
from Japanemi_features.anime_ import Downcap, foriter

load_dotenv()
CHANNEL_ID = int(os.getenv("channel_id"))
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
    # ****************************************************************
    if chat_id in AUTH_USERS:
        data = update.data
        # *****************************
        if "!" in data:
            data = int(data.split("!")[0])
            actu = await episodes()
            title = actu["titles"][data]
            links = Downcap(actu["episodes"][data]).get_url()
            path = await foriter(links, tmp_directory)
            caption = await capupload_text(title)
            try:
                list_dir_ = os.listdir(tmp_directory)
                if "thumb.jpg" in list_dir_:
                    yes_thumb = True
                else:
                    yes_thumb = False
            except Exception as e:
                yes_thumb = False
                print(e)
            clip = VideoFileClip(path)
            duration = int(clip.duration)
            print(duration)
            if yes_thumb:
                await bot.send_video(chat_id=CHANNEL_ID,
                                     video=path,
                                     thumb=f"{tmp_directory}thumb.jpg",
                                     caption=caption,
                                     duration=duration)
            else:
                await bot.send_video(chat_id=CHANNEL_ID,
                                     video=path,
                                     caption=caption,
                                     duration=duration)
            rmtree(tmp_directory)
        if data == "reload":
            key = string.hexdigits
            rch = "".join([random.choice(key) for i in range(5)])
            inline = await buttons()
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=f"#{rch}\nUltimos episodios",
                                        reply_markup=inline)
    else:
        pass
