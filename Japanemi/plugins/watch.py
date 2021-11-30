import os
from shutil import rmtree
from .. import AUTH_USERS
from pyrogram import Client
from ..helper import filterx


@Client.on_message(filterx.command(["watch"]))
async def flash(bot, update):
    user = update.from_user.id
    chat_id = update.chat.id
    dt = " ".join(update["text"].split(" ")[1:])
    if user in AUTH_USERS:
        if "rm" in dt:
            drm = "".join(dt.split("|")[-1])
            rmtree(f"./Downloads/{drm}")
            dt = ""
        try:
            ld = os.listdir(f"./Downloads/{dt}")
        except Exception as e:
            print(e)
            ld = os.listdir("./Downloads/")
        await bot.send_message(chat_id=chat_id,
                               text=ld)
