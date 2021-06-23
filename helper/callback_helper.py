import os
from dotenv import load_dotenv
from shutil import rmtree
from helper.texts import capupload_text
from moviepy.editor import VideoFileClip
from Japanemi_features.episodes import *
from Japanemi_features.anime_ import Downcap, foriter

load_dotenv()
CHANNEL_ID = int(os.getenv("channel_id"))


async def ta_callback(bot, data, tmp_directory):
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


async def hla_callback(bot, data, tmp_directory):
    data = int(data.split("|")[0])
    actu = await hla_episodes()
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

