from pyrogram import Client, filters
from Japanemi.helper.buttons import datos
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# https://img.anili.st/media/{id} esto es para la img del anime_name
# print(a.get_anime(b["id"][0]))
# print(anime_name)
# print(anime_name.title.romaji)
# print(anime_name.title.native)
# print(anime_name.url)
# print(anime_name.episodes)
# s = BeautifulSoup(anime_name.description, "html.parser")
# h = s.get_text()
# i = tr.translate(h)
# print(i)
# print(anime_name.format)
# print(anime_name.status)
# print(anime_name.duration)
# print(anime_name.genres)
# print(anime_name.tags)
# print(anime_name.studios)
# print(anime_name.start_date)
# print(anime_name.end_date)
# print(anime_name.season)
# print(anime_name.cover)
# print(anime_name.banner)
# print(anime_name.source)
# print(anime_name.characters)
# print(anime_name.trailer)
# print(anime_name.score)


# async def inline_option(url):
#     if chat_type == "private":
#         trailer_btn = InlineKeyboardButton("Trailer", callback_data="trailer")
#         more_info = InlineKeyboardButton("More Info", url=url)
#         charac_btn = InlineKeyboardButton("Characters", callback_data="characters")
#         inline = InlineKeyboardMarkup([[trailer_btn, charac_btn], [more_info]])
#     elif chat_type == "supergroup":
#         more_info = InlineKeyboardButton("More Info", callback_data="more_info")
#         inline = InlineKeyboardMarkup([[more_info]])
#     return inline


async def btns(bot, update):
    message_id = update.message_id
    chat_id = update.chat.id
    anime_name = " ".join(update["text"].split(" ")[1:])
    dats = await datos(anime_name)

    buttons = [InlineKeyboardButton(f"{dats['title'][a]}",
                                    callback_data=f"{dats['id'][a]},") for a in range(len(dats["title"]))]
    pairs = [buttons[i: (i + 1)] for i in range((len(buttons)))]
    round_num = len(buttons)
    calc = len(buttons) - round(round_num)
    count = [1, 2]
    if calc in count:
        pairs.append((buttons[-1],))
    inline = InlineKeyboardMarkup(pairs)
    if len(pairs) == 0:
        await bot.send_message(chat_id=chat_id,
                               text="No se encontro ningún anime con ese nombre",
                               reply_to_message_id=message_id)
    elif len(pairs) > 0:
        await bot.send_message(chat_id=chat_id,
                               text="Elige el anime que coincida con tu busqueda",
                               reply_to_message_id=message_id,
                               reply_markup=inline)


@Client.on_message(filters.command(["ani"]))
async def anime_srch(bot, update):
    await btns(bot, update)

