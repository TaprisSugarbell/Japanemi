import os
from shutil import rmtree
from decouple import config
from pyrogram import Client
from ..helper import filterx
from .. import AUTH_USERS, sayulog


@Client.on_message(filterx.command(["clear"]))
async def flash(bot, update):
    sayulog.info(update)
    user = update.from_user.id
    chat_id = update.chat.id
    if user in AUTH_USERS:
        try:
            rmtree(f"./Downloads/{user}")
        except Exception as e:
            print(e)
            sayulog.error("Ha ocurrido un error.", exc_info=e)
        sayulog.info(os.listdir("./Downloads"))
