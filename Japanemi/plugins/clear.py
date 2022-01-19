import os
from .. import sayulog
from shutil import rmtree
from decouple import config
from pyrogram import Client
from ..helper import filterx
from ..helper.__vars__ import auth_users_async


@Client.on_message(filterx.command(["clear"]))
async def flash(bot, update):
    sayulog.info(update)
    user = update.from_user.id
    chat_id = update.chat.id
    AUTH_USERS = await auth_users_async()
    if user in AUTH_USERS:
        try:
            rmtree(f"./Downloads/{user}")
        except Exception as e:
            print(e)
            sayulog.error("Ha ocurrido un error.", exc_info=e)
        sayulog.info(os.listdir("./Downloads"))
