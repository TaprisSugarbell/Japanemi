import anilist
from Japanemi_features.episodes import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def buttons():
    btn1 = InlineKeyboardButton("Anime", callback_data="anime_")
    btn2 = InlineKeyboardButton("Hentai", callback_data="hentai_")
    inline = InlineKeyboardMarkup([
        [btn1, btn2]
    ])
    return inline


async def ta_buttons():
    actu = await ta_episodes()
    title = actu["titles"]
    stress = [InlineKeyboardButton(f"{title[i]}",
                                   callback_data=f"{i}!") for i in range(len(title))]
    pairs = [stress[i: (i + 1)] for i in range((len(stress)))]
    round_num = len(stress)
    calc = len(stress) - round(round_num)
    count = [1, 2]
    if calc in count:
        pairs.append((stress[-1],))
    new_pair = pairs[:9]
    new_pair.append((InlineKeyboardButton("Hentai", callback_data="hentai_"),
                     InlineKeyboardButton("Reload", callback_data="reloadta")))
    inline = InlineKeyboardMarkup(new_pair)
    return inline


async def hla_buttons():
    actu = await hla_episodes()
    title = actu["titles"]
    stress = [InlineKeyboardButton(f"{title[i]}",
                                   callback_data=f"{i}|") for i in range(len(title))]
    pairs = [stress[i: (i + 1)] for i in range((len(stress)))]
    round_num = len(stress)
    calc = len(stress) - round(round_num)
    count = [1, 2]
    if calc in count:
        pairs.append((stress[-1],))
    new_pair = pairs[:9]
    new_pair.append((InlineKeyboardButton("Anime", callback_data="anime_"),
                     InlineKeyboardButton("Reload", callback_data="reloadhla")))
    inline = InlineKeyboardMarkup(new_pair)
    return inline


async def datos(anime_name):
    a = anilist.Client()
    d = a.search_anime(anime_name, 10)
    b = dict()
    b["id"] = [e.id for e in d]
    b["title"] = [e.title.romaji for e in d]
    b["url"] = [e.url for e in d]
    return b


async def datos_id(anime_id):
    a = anilist.Client()
    d = a.get_anime(anime_id)
    b = dict()
    b["id"] = d.id
    b["title"] = d.title.romaji
    b["url"] = d.url
    return b


async def inline_option(chat_type, url, anime_id):
    if chat_type == "private":
        trailer_btn = InlineKeyboardButton("Trailer", callback_data=f"trailer,{anime_id}")
        more_info = InlineKeyboardButton("More Info", url=url)
        charac_btn = InlineKeyboardButton("Characters", callback_data="characters")
        inline = InlineKeyboardMarkup([[trailer_btn, charac_btn], [more_info]])
    elif chat_type == "supergroup":
        more_info = InlineKeyboardButton("More Info", callback_data="more_info")
        inline = InlineKeyboardMarkup([[more_info]])
    return inline


async def send_trailer(bot, chat_id, message_id, filename, info):
    await bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=InlineKeyboardMarkup(
                                            [[InlineKeyboardButton("Characters", callback_data="characters"),
                                              InlineKeyboardButton("More Info", url=info.url)]]))
    await bot.send_video(chat_id=chat_id,
                         video=filename,
                         thumb=info.trailer.thumbnail,
                         reply_to_message_id=message_id)
