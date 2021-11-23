import os
import random
import string
from shutil import rmtree
from decouple import config
from pyrogram import Client, filters
from moviepy.editor import VideoFileClip
from Japanemi.helper.texts import capupload_text
from Japanemi.Japanemi_features.anime_ import foriter

AUTH_USERS = [int(i) for i in config("AUTH_USERS", default="784148805").split(" ")]


async def reader(file):
    links = []
    with open(file, "r") as r:
        for line in r.readlines():
            links.append(line.strip())
    file = file.split("/")[-1]
    title = ".".join(file.split(".")[0:-1])
    return {"links": links,
            "title": title}


@Client.on_message(filters.document)
async def flash(bot, update):
    print(update)
    user = update.from_user.id
    chat_id = update.chat.id
    if user in AUTH_USERS:
        caption_ = update.caption
        # file_id = update.reply_to_message.document.file_id
        file_id = update.document.file_id
        # file_name = update.reply_to_message.document.file_name
        file_name = update.document.file_name
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
        if caption_ is None:
            caption = await capupload_text(dats["title"])
        else:
            caption = await capupload_text(caption_)
        clip = VideoFileClip(filename)
        size = clip.size
        height = size[1]
        width = size[0]
        duration = int(clip.duration)
        print(duration)
        print(os.listdir(tmp_directory))
        try:
            await bot.send_video(chat_id=chat_id,
                                 video=filename,
                                 thumb=tmp_directory + "thumb.jpg",
                                 caption=caption,
                                 duration=duration,
                                 height=height,
                                 width=width)
        except Exception as e:
            print(e)
            await bot.send_video(chat_id=chat_id,
                                 video=filename,
                                 caption=caption,
                                 duration=duration,
                                 height=height,
                                 width=width)
        rmtree(tmp_directory)
    else:
        pass


