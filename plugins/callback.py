import os
import random
import string
from helper.buttons import *
from plugins.Japanemi import *
from helper.callback_helper import *

load_dotenv()
CHANNEL_ID = int(os.getenv("channel_id"))
AUTH_USERS_STR = os.getenv("AUTH_USERS")
AUTH_USERS = [int(i) for i in AUTH_USERS_STR.split(" ")]


@Client.on_callback_query()
async def callback_data(bot, update):
    inline = None
    chat_id = update.from_user.id
    message_id = update.message.message_id
    # Carpeta
    tmp_directory = "./Downloads/" + str(update.from_user.id) + "/"
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    # ****************************************************************
    if chat_id in AUTH_USERS:
        data = update.data
        # *****************************
        if "_" in data:
            data = data.split("_")[0]
            if data == "hentai":
                inline = await hla_buttons()
            elif data == "anime":
                inline = await ta_buttons()
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=f"Ultimos episodios",
                                        reply_markup=inline)
        elif "!" in data:
            await ta_callback(bot, data, tmp_directory)
        elif "|" in data:
            await hla_callback(bot, data, tmp_directory)
        elif "reload" in data:
            key = string.hexdigits
            rch = "".join([random.choice(key) for i in range(5)])
            if "hla" in data:
                inline = await hla_buttons()
            elif "ta" in data:
                inline = await buttons()
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=f"#{rch}\nUltimos episodios",
                                        reply_markup=inline)
    else:
        pass
