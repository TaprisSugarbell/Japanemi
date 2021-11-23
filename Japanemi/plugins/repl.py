import os, random, string
from pyrogram import Client, filters
from ..helper.texts import capupload_text


@Client.on_message((filters.video | filters.command(["repl"])) & filters.private)
async def __repl__(bot, update):
    print(update)
    v = update.media
    chat_id = update.chat.id
    user_id = update.from_user.id
    message_id = update.message_id
    key = string.hexdigits
    session_random = "".join([random.choice(key) for i in range(5)])
    # Carpeta
    tmp_directory = "./Downloads/"
    file = tmp_directory + str(user_id) + ".txt"
    if not v:
        text = update.text.replace("/repl", "").strip()
        if len(text) > 0:
            if not os.path.isdir(tmp_directory):
                os.makedirs(tmp_directory)
            with open(file, "w") as w:
                w.write(text)
        else:
            if os.path.exists(file):
                with open(file, "r") as r:
                    await bot.send_message(chat_id,
                                           f"💮 {r.read()}")
            else:
                await bot.send_message(chat_id,
                                       "No has ingresado titulo.")
    else:
        if not os.path.exists(file):
            await bot.send_message(chat_id,
                                   "No has ingresado titulo.")
        else:
            video = update.video.file_id
            title = None
            with open(file, "r") as r:
                title = r.read()

            print(title)
            try:
                ans = await bot.ask(chat_id,
                                    "Número de capítulo?")
            except Exception as e:
                ans = None
                print(e)
            print(ans)
            try:
                tt = int(ans.text)
            except ValueError:
                tt = 1
            await bot.delete_messages(chat_id,
                                      ans.message_id)
            caption = await capupload_text(title + " " + str(tt))

            await bot.send_video(chat_id,
                                 video=video,
                                 caption=caption)


@Client.on_message((filters.command(["depl"])) & filters.private)
async def __depl__(bot, update):
    print(update)
    chat_id = update.chat.id
    user_id = update.from_user.id
    message_id = update.message_id
    # Carpeta
    tmp_directory = "./Downloads/"
    file = tmp_directory + str(user_id) + ".txt"
    if os.path.exists(file):
        os.remove(file)


