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








