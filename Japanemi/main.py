import os
import logging
import pyrogram
import pyromod.listen
from logging import handlers
# from pyromod import listen
from decouple import config

log_ = "./logs/"
if os.path.exists(log_):
    pass
else:
    os.makedirs("./logs/", exist_ok=True)
# logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
# DEBUG
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING,
                    handlers=[
                        handlers.RotatingFileHandler(
                            filename="./logs/sayu.log",
                            maxBytes=3145728,
                            backupCount=1
                        ),
                        logging.StreamHandler()
                    ]
                    )

# vars
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
