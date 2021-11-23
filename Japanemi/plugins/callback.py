import random
import string
from decouple import config
from ..helper.buttons import *
from ..helper.callback_helper import *
from Japanemi.plugins.Japanemi import *

CHANNEL_ID = config("CHANNEL_ID", default=None, cast=int)
AUTH_USERS = [int(i) for i in config("AUTH_USERS", default="784148805").split(" ")]


@Client.on_callback_query()
async def callback_data(bot, update):
    inline = None
    user = update.from_user.id
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    key = string.hexdigits
    session_random = "".join([random.choice(key) for i in range(5)])
    # Carpeta
    tmp_directory = "./Downloads/" + str(user) + "/" + session_random + "/"
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    # ****************************************************************
    if user in AUTH_USERS:
        data = update.data
        print(data)
        # *****************************
        if "_" in data:
            data = data.split("_")[0]
            print(data)
            if data == "hentai":
                inline = await hla_buttons()
            elif data == "anime":
                inline = await af_buttons()
            KEY = string.hexdigits
            RCH = "".join([random.choice(KEY) for i in range(5)])
            try:
                await bot.edit_message_text(chat_id=chat_id,
                                            message_id=message_id,
                                            text=f"#{RCH}\nUltimos episodios",
                                            reply_markup=inline)
            except Exception as e:
                print(e)
        elif "!" in data:
            await af_callback(bot, data, tmp_directory)
        elif "|" in data:
            await hla_callback(bot, data, tmp_directory)
        elif "reload" in data:
            if "hla" in data:
                inline = await hla_buttons()
            elif "ta" in data:
                inline = await af_buttons()
            KEY = string.hexdigits
            RCH = "".join([random.choice(KEY) for i in range(5)])
            try:
                await bot.edit_message_text(chat_id=chat_id,
                                            message_id=message_id,
                                            text=f"#{RCH}\nUltimos episodios",
                                            reply_markup=inline)
            except Exception as e:
                print(e)
        elif "," in data:
            if "trailer" in data:
                await trailer(bot, update, tmp_directory)
            else:
                await ani_callback(bot, update)
    else:
        pass
