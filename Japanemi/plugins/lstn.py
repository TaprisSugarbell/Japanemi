import os
import random
import string
from . import AUTH_USERS
from shutil import rmtree
from pyrogram import Client, filters
from moviepy.editor import VideoFileClip
from ..Japanemi_features.anime_ import Downcap, foriter


@Client.on_message(filters.regex(r"https?://(www\d*)?"))
async def __lstn__(bot, update):
    print(update)
    if update.from_user.id in AUTH_USERS:
        links = Downcap(update.text).get_url()
        if links:
            key = string.hexdigits
            session_random = "".join([random.choice(key) for i in range(5)])
            # Carpeta
            tmp_directory = "./Downloads/" + str(update.from_user.id) + "/" + session_random + "/"
            if not os.path.isdir(tmp_directory):
                os.makedirs(tmp_directory)
            path = await foriter(links, tmp_directory)
            clip = VideoFileClip(path)
            size = clip.size
            height = size[1]
            width = size[0]
            duration = int(clip.duration)
            print(duration)
            print(os.listdir(tmp_directory))
            try:
                await bot.send_video(chat_id=update.from_user.id,
                                     video=path,
                                     thumb=tmp_directory + "thumb.jpg",
                                     duration=duration,
                                     height=height,
                                     width=width)
            except Exception as e:
                print(e)
                await bot.send_video(chat_id=update.from_user.id,
                                     video=path,
                                     duration=duration,
                                     height=height,
                                     width=width)
            rmtree(tmp_directory)

