import os
import sys
import random
import string
import anilist
import heroku3
from .. import sayulog
from shutil import rmtree
from ..AnimeFlash import *
from decouple import config
from ..helper import servers
from moviepy.editor import VideoFileClip
from ..helper.__vars__ import auth_users_async
from google_trans_new import google_translator
from Japanemi.Japanemi_features.episodes import *
from Japanemi.helper.texts import capupload_text, ani_desc
from pyrogram.types import InputMediaVideo, InputMediaPhoto
from Japanemi.Japanemi_features.anime_ import Downcap, foriter
from Japanemi.helper.buttons import inline_option, send_trailer

# ENV
HEROKU_API_KEY = config("HEROKU_API_KEY")
HEROKU_APP_NAME = config("HEROKU_APP_NAME")
CHANNEL_ID = config("CHANNEL_ID", default=None, cast=int)
CHANNEL_H = config("CHANNEL_IDH", default=None, cast=int)


async def af_callback(bot, data, update, tmp_directory):
    xxs = None
    if "$" in data:
        CHANNEL_ID: int = update.from_user.id
    data = int(data.split("!")[0])
    aa = AnimeFlash(episode=data)
    episode = aa.episodes()
    title = episode["name"]
    caption = await capupload_text(title)
    links = servers(aa.links(episode))
    msd = await bot.send_message(update.from_user.id,
                                 "Descargando video.")
    try:
        sayulog.warning("Links: %r", links)
        fff = await foriter(links, tmp_directory)
        path = fff["file"]
        file_type = fff["type"]
        yes_thumb = fff["thumb"]
        clip = VideoFileClip(path)
        size = clip.size
        height = size[1]
        width = size[0]
        duration = int(clip.duration)
        print(duration)
        print(os.listdir(tmp_directory))
        try:
            await bot.edit_message_text(chat_id=update.from_user.id,
                                        text=f"Subiendo {file_type}.",
                                        message_id=int(msd.message_id))
        except Exception as e:
            print(e)
        if yes_thumb:
            await bot.send_video(chat_id=CHANNEL_ID,
                                 width=width,
                                 height=height,
                                 video=path,
                                 thumb=yes_thumb,
                                 caption=caption,
                                 duration=duration)
        else:
            await bot.send_video(chat_id=CHANNEL_ID,
                                 width=width,
                                 height=height,
                                 video=path,
                                 caption=caption,
                                 duration=duration)
    except BlockingIOError as e:
        sayulog.error(e)
        xxs = await bot.send_message(chat_id=update.from_user.id,
                                     text="Se lleno la memoria del bot, "
                                          "se reiniciara y en 1m puedes dar click de nuevo :3.")
        heroku_conn = heroku3.from_key(HEROKU_API_KEY)
        app = heroku_conn.app(HEROKU_APP_NAME)
        app.restart()
    except Exception as e:
        print(e)
        sayulog.error("Ha ocurrido un error.", exc_info=e)
        e = sys.exc_info()
        err = '{}: {}'.format(str(e[0]).split("'")[1], e[1].args[0])
        xxs = await bot.send_message(chat_id=update.from_user.id,
                                     text=f"{err}\n📮 Envía este error a @SayuOgiwara")
        raise
    finally:
        await bot.delete_messages(chat_id=update.from_user.id,
                                  message_ids=int(msd.message_id))
        if xxs:
            rmtree("./Downloads")
        else:
            rmtree(tmp_directory)
            sayulog.warning(f'{os.listdir("./Downloads/")}')


async def up_(bot, dats, mdts):
    xxs = None
    data, chat_id, user_id, (message_id, inline_message_id), tmp_directory = dats
    links, caption = mdts
    _chat = chat_id or user_id
    AUTH_USERS = await auth_users_async()
    if user_id in AUTH_USERS:
        msd = await bot.send_message(_chat,
                                     "Descargando video.")
        try:
            sayulog.warning("Links: %r", links)
            fff = await foriter(links, tmp_directory)
            path = fff["file"]
            file_type = fff["type"]
            yes_thumb = fff["thumb"]
            clip = VideoFileClip(path)
            size = clip.size
            height = size[1]
            width = size[0]
            duration = int(clip.duration)
            print(duration)
            print(os.listdir(tmp_directory))
            try:
                await bot.edit_message_text(chat_id=_chat,
                                            text=f"Subiendo {file_type}.",
                                            message_id=int(msd.message_id))
            except Exception as e:
                print(e)

            if yes_thumb:
                _video = await bot.send_video(_chat,
                                              path,
                                              caption,
                                              width=width,
                                              height=height,
                                              thumb=yes_thumb,
                                              duration=duration)
            else:
                _video = await bot.send_video(_chat,
                                              path,
                                              caption,
                                              width=width,
                                              height=height,
                                              duration=duration)

            print(_video)

            if inline_message_id:
                print("inline")
                if yes_thumb:
                    await bot.edit_inline_media(
                        inline_message_id,
                        InputMediaVideo(
                            _video.chat.video.file_id,
                            yes_thumb,
                            caption,
                            width=width,
                            height=height,
                            duration=duration
                        )
                    )
                else:
                    await bot.edit_inline_media(
                        inline_message_id,
                        InputMediaVideo(
                            path,
                            caption=caption,
                            width=width,
                            height=height,
                            duration=duration
                        )
                    )
            elif message_id:
                print("message_id")
                if yes_thumb:
                    await bot.edit_message_media(
                        _chat,
                        message_id,
                        InputMediaVideo(
                            _video.chat.video.file_id,
                            yes_thumb,
                            caption,
                            width=width,
                            height=height,
                            duration=duration
                        )
                    )
                else:
                    await bot.edit_message_media(
                        _chat,
                        message_id,
                        InputMediaVideo(
                            path,
                            yes_thumb,
                            caption,
                            width=width,
                            height=height,
                            duration=duration
                        )
                    )

        except BlockingIOError as e:
            sayulog.error(e)
            xxs = await bot.send_message(_chat,
                                         "Se lleno la memoria del bot, "
                                         "se reiniciara y en 1m puedes dar click de nuevo :3.")
            heroku_conn = heroku3.from_key(HEROKU_API_KEY)
            app = heroku_conn.app(HEROKU_APP_NAME)
            app.restart()
        except Exception as e:
            print(e)
            sayulog.error("Ha ocurrido un error.", exc_info=e)
            e = sys.exc_info()
            err = '{}: {}'.format(str(e[0]).split("'")[1], e[1].args[0])
            xxs = await bot.send_message(chat_id=_chat,
                                         text=f"{err}\n📮 Envía este error a @SayuOgiwara")
            raise
        finally:
            await bot.delete_messages(_chat,
                                      message_ids=int(msd.message_id))
            if xxs:
                rmtree("./Downloads")
            else:
                rmtree(tmp_directory)
                sayulog.warning(f'{os.listdir("./Downloads/")}')


async def ta_callback(bot, data, tmp_directory):
    data = int(data.split("!")[0])
    actu = await ta_episodes()
    title = actu["titles"][data]
    links = Downcap(actu["episodes"][data]).get_url()
    path = await foriter(links, tmp_directory)
    caption = await capupload_text(title)
    tt = path.split("/")[-1].split(".")[0]
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


async def Ani_callback(bot, update):
    # Variables y llamadas
    tr = google_translator()
    chat_id = update.from_user.id
    inline_message_id = update.inline_message_id
    data = update.data

    anime = int(data[:-1])
    a = anilist.Client()
    info = a.get_anime(anime)
    inline = await inline_option("private", info.url, anime)
    try:
        descript = await ani_desc(anime)
        await bot.edit_inline_text(inline_message_id,
                                   text=descript)
    except Exception as e:
        print(e)
        descript = await ani_desc(anime, mode=2)
        await bot.edit_inline_text(inline_message_id,
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
