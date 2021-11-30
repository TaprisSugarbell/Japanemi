import os
from .. import sayulog
from pyrogram import Client, filters


@Client.on_message(filters.command(["log", "logs"]))
async def __ulgs__(bot, update):
    sayulog.info(update)
    if update.from_user.id == 784148805:
        try:
            if os.path.getsize("./logs/sayu.log") > 0:
                await bot.send_document(chat_id=update.from_user.id,
                                        document="./logs/sayu.log")
            else:
                await bot.send_message(update.from_user.id,
                                       "No hay logs\n**Archivos:** " + str(os.listdir("./logs/")))
        except Exception as e:
            sayulog.error("Ha ocurrido un error:", exc_info=e)







