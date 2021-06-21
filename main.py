import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
TOKEN = os.getenv("bot_token")

bot = Client("Japanemi", api_id=api_id, api_hash=api_hash, bot_token=TOKEN)


if __name__ == "__main__":
    bot.run()
