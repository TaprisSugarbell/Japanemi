import re
from ..AnimeFlash import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def clean_tags(tags):
    if isinstance(tags, str):
        tag_split = tags.split(" ")
    else:
        tag_split = tags
    lista_tag = []
    for tag in tag_split:
        lista_tag.append(f"#{tag}")
    tag_string = " ".join(lista_tag)
    # return " ".join(lista_tag)
    re_tag0 = tag_string.replace("/", "_")
    re_tag = re_tag0.replace("-", "_")
    clean_tag = re.sub(r"[^a-zA-Z0-9_# ]", "", re_tag)
    return clean_tag


def xname(x: str):
    # xname = lambda x: x.split()[-1]
    mtch = re.findall(r"(\d+ y \d+|\d+ Y \d+|\d+|\w*)", x)
    if re.match(".* [Oo][Vv][Aa][Ss]? .*", x.lower()):
        nn = x.split()[-1]
        try:
            int(nn)
        except ValueError:
            nn = ""
        return "OVA " + nn
    else:
        if len(mtch) > 2:
            return mtch[-2]
        else:
            return "Capítulo" + mtch[-1]


@Client.on_callback_query(filters.regex(r"anime_"))
async def __get_anime__(bot, update):
    print(update)
    append_btns = None
    chat_id = update.from_user.id
    data = int(update.data.split("_")[-1])
    page = int(update.data.split("_")[1])
    # if page > 1:
    #     li = 9
    # else:
    #     li = 8
    inline_message_id = update.inline_message_id
    a = AnimeFlash(anime_id=data)
    anime_info = a.anime()
    des = f'[{anime_info["name"]}]({arm_link(anime_info)})\n' \
          f'{date(anime_info)}\n' \
          f'Capítulos: {anime_info["chapters"]}\n' \
          f'{description(anime_info)}\n' \
          f'{clean_tags(genres(anime_info)).strip()}\n' \
          f'{chapters(anime_info, "Siguiente capítulo:")}\n' \
          f'{tag(arm_link(anime_info, 1))}'
    try:
        await bot.edit_inline_text(inline_message_id,
                                   des)
    except Exception as e:
        print(e)
    eplist = a.episodes(page=page, limit=9)
    print(eplist)
    if 1 < eplist["page"] < eplist["pages"]:
        append_btns = [
            InlineKeyboardButton("Anterior", f'anime_{page - 1}_{data}'),
            InlineKeyboardButton("Siguiente", f'anime_{page + 1}_{data}')
        ]
    elif eplist["page"] == 1 and eplist["pages"] > 1:
        append_btns = [
            InlineKeyboardButton("Siguiente", f'anime_{page + 1}_{data}')
        ]
    elif eplist["page"] != 1:
        append_btns = [
            InlineKeyboardButton("Anterior", f'anime_{page - 1}_{data}')
        ]


    btns = [
        InlineKeyboardButton(
            f'{xname(eplist["results"][i]["name"])}',
            f'{eplist["results"][i]["id"]}!') for i in range(len(eplist["results"]))
    ]

    if append_btns:
        btns.extend(append_btns)
    btns = order(btns, 3)

    try:
        await bot.edit_inline_reply_markup(inline_message_id,
                                           reply_markup=InlineKeyboardMarkup(btns))
    except Exception as e:
        print(e)

