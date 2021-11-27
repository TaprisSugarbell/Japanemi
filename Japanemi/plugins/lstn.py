import os
import sys
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
            msd = await bot.send_message(update.from_user.id,
                                         "Descargando video.")
            try:
                fff = await foriter(links, tmp_directory)
                path = fff["file"]
                file_type = fff["type"]
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
            except Exception as e:
                print(e)
                e = sys.exc_info()
                err = '{}: {}'.format(str(e[0]).split("'")[1], e[1].args[0])
                await bot.send_message(chat_id=update.from_user.id,
                                       text=f"{err}\n📮 Envía este error a @SayuOgiwara")
            finally:
                await bot.delete_messages(chat_id=update.from_user.id,
                                          message_ids=int(msd.message_id))
            rmtree(tmp_directory)

