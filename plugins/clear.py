import os
from shutil import rmtree
from helper import filterx
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()
AUTH_USERS_STR = os.getenv("AUTH_USERS")
AUTH_USERS = [int(i) for i in AUTH_USERS_STR.split(" ")]


@Client.on_message(filterx.command(["clear"]))
async def flash(bot, update):
    user = update.from_user.id
    chat_id = update.chat.id
    if user in AUTH_USERS:
        rmtree(f"./Downloads/{user}")
