import os
import anilist
import youtube_dl
from shutil import rmtree
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip
from Japanemi_features.episodes import *
from google_trans_new import google_translator
from helper.texts import capupload_text, ani_desc
from Japanemi_features.anime_ import Downcap, foriter
from helper.buttons import inline_option, send_trailer

load_dotenv()
CHANNEL_ID = int(os.getenv("channel_id"))
CHANNEL_H = int(os.getenv("channel_idh"))


async def ta_callback(bot, data, tmp_directory):
    data = int(data.split("!")[0])
    actu = await ta_episodes()
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
        await bot.send_video(chat_id=CHANNEL_H,
                             video=path,
                             thumb=f"{tmp_directory}thumb.jpg",
                             caption=caption,
                             duration=duration)
    else:
        await bot.send_video(chat_id=CHANNEL_H,
                             video=path,
                             caption=caption,
                             duration=duration)
    rmtree(tmp_directory)


async def ani_callback(bot, update):
    # Variables y llamadas
    tr = google_translator()
    chat_id = update.from_user.id
    chat_type = update.message.chat.type
    message_id = update.message.message_id
    data = update.data

    anime = int(data[:-1])
    a = anilist.Client()
    info = a.get_anime(anime)
    inline = await inline_option(chat_type, info.url, anime)
    if chat_type == "supergroup":
        try:
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=f"**{info.title.romaji}**\n({info.title.native})\n"
                                             f"**Tipo:** {info.format}\n"
                                             f"**Estado:** {tr.translate(info.status, lang_tgt='es')[0]}\n"
                                             f"**Géneros:** {tr.translate(', '.join(info.genres), lang_tgt='es')}\n"
                                             f"**Estudios:** {', '.join(info.studios)}"
                                             f"<a href='https://img.anili.st/media/{info.id}'>&#8205;</a>")
        except AttributeError:
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=f"**{info.title.romaji}**\n({info.title.native})\n"
                                             f"**Tipo:** {info.format}\n"
                                             f"**Estudios:** {', '.join(info.studios)}"
                                             f"<a href='https://img.anili.st/media/{info.id}'>&#8205;</a>")
    elif chat_type == "private":
        try:
            descript = await ani_desc(anime)
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=descript)
        except Exception as e:
            print(e)
            descript = await ani_desc(anime, mode=2)
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=descript,
                                        reply_markup=inline)
    print(info)


async def trailer(bot, update, tmp_directory):
    chat_id = update.from_user.id
    message_id = update.message.message_id
    data = int(str(update.data).split(",")[1])
    a = anilist.Client()
    info = a.get_anime(data)
    link = info.trailer.url
    path = await foriter(link, tmp_directory)
    clip = VideoFileClip(path)
    duration = int(clip.duration)
    print(duration)
    try:
        list_dir_ = os.listdir(tmp_directory)
        if "thumb.jpg" in list_dir_:
            yes_thumb = True
        else:
            yes_thumb = False
    except Exception as e:
        yes_thumb = False
        print(e)
    await send_trailer(bot, chat_id, message_id, info)
    if yes_thumb:
        await bot.send_video(chat_id=chat_id,
                             video=path,
                             thumb=f"{tmp_directory}thumb.jpg",
                             duration=duration)
    else:
        await bot.send_video(chat_id=chat_id,
                             video=path,
                             duration=duration)
    rmtree(tmp_directory)
