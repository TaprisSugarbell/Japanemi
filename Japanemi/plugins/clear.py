import os
from shutil import rmtree
from decouple import config
from pyrogram import Client
from Japanemi.helper import filterx

AUTH_USERS = [int(i) for i in config("AUTH_USERS", default="784148805").split(" ")]


@Client.on_message(filterx.command(["clear"]))
async def flash(bot, update):
    user = update.from_user.id
    chat_id = update.chat.id
    if user in AUTH_USERS:
        try:
            rmtree(f"./Downloads/{user}")
        except Exception as e:
            print(e)
        print(os.listdir("./Downloads"))
