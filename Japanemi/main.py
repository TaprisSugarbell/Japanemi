import pyrogram
import pyromod.listen
# from pyromod import listen
from decouple import config


# VARS
API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)

if __name__ == "__main__":
    nb = "Japanemi"
    print(f"Starting {nb}...")
    plugins = dict(root=f"{nb}/plugins")
    app = pyrogram.Client(
        nb,
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    app.run()
