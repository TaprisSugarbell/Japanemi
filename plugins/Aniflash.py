import os
import random
import string
from shutil import rmtree
from dotenv import load_dotenv
from pyrogram import Client, filters
from moviepy.editor import VideoFileClip
from Japanemi_features.anime_ import foriter
from helper.texts import capupload_text, ani_desc

load_dotenv()
AUTH_USERS_STR = os.getenv("AUTH_USERS")
AUTH_USERS = [int(i) for i in AUTH_USERS_STR.split(" ")]


async def reader(file):
    links = []
    with open(file, "r") as r:
        for line in r.readlines():
            links.append(line.strip())
    file = file.split("/")[-1]
    title = file.split(".")[0]
    return {"links": links,
            "title": title}


@Client.on_message(filters.command(["flash"]))
async def flash(bot, update):
    chat_id = update.chat.id
    if chat_id in AUTH_USERS:
        file_id = update.reply_to_message.document.file_id
        file_name = update.reply_to_message.document.file_name
        key = string.hexdigits
        session_random = "".join([random.choice(key) for i in range(5)])
        # Carpeta
        tmp_directory = "./Downloads/" + str(update.from_user.id) + "/" + session_random + "/"
        if not os.path.isdir(tmp_directory):
            os.makedirs(tmp_directory)
        file = await bot.download_media(file_id, tmp_directory + file_name)
        dats = await reader(file)
        os.unlink(file)
        filename = await foriter(dats["links"], tmp_directory)
        caption = await capupload_text(dats["title"])
        clip = VideoFileClip(filename)
        duration = int(clip.duration)
        print(duration)
        try:
            await bot.send_video(chat_id=chat_id,
                                 video=filename,
                                 thumb=tmp_directory + "thumb.jpg",
                                 caption=caption,
                                 duration=duration)
        except Exception as e:
            print(e)
            await bot.send_video(chat_id=chat_id,
                                 video=filename,
                                 caption=caption,
                                 duration=duration)
        rmtree(tmp_directory)
    else:
        pass


