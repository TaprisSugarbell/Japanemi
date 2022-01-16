import re
import random
import string
from ..AnimeFlash import *
from pyromod.helpers import ikb
from pyromod.nav import Pagination
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


rankey = lambda length=5, _string=string.hexdigits: "".join(
    random.choice(
        _string
    ) for _ in range(length)
)


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
    mtch = re.findall(r"(\d+ y \d+|\d+ Y \d+|\d+\.?\d*)", x)
    if re.match(".* [Oo][Vv][Aa][Ss]? .*", x):
        nn = x.split()[-1]
        try:
            int(nn)
        except ValueError:
            nn = ""
        return "OVA " + nn
    else:
        try:
            return "Capítulo" + " " + mtch[-1]
        except IndexError:
            return "Película"


def page_data(page):
    return f'anime_{page}_{data}'


def item_data(item, page):
    if isinstance(item, dict):
        return f'{item["id"]}!'
    else:
        return f'{rankey(8)}'


def item_title(item, page):
    if isinstance(item, dict):
        return xname(item["name"])
    else:
        return f'{rankey(8)}'


@Client.on_callback_query(filters.regex(r"anime_"))
async def __get_anime__(bot, update):
    global data
    print(update)
    limit = 15
    append_btns = None
    chat_id = update.from_user.id
    page = int(update.data.split("_")[1])
    data = int(update.data.split("_")[-1])
    if "c" in update.data:
        _a = AnimeFlash(episode=page)
        epnumber = _a.episodes()
        fnn = re.findall(r"\d+\.?\d*", epnumber["name"])
        if fnn:
            _nn_ = int(fnn[-1])
            _nd = _nn_ / limit
            if isinstance(_nd, float):
                page = round(_nd) + 1
            else:
                page = _nd
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
          f'{chapters(anime_info, "Siguiente capítulo:").strip()}\n' \
          f'{tag(arm_link(anime_info, 1))}'
    try:
        await bot.edit_inline_text(inline_message_id,
                                   des)
    except Exception as e:
        print(e)
    eplist = a.episodes(page=page, limit=limit)
    print(eplist)
    results = eplist["results"]
    results_no_recursive = results.copy()
    if eplist["pages"] == page:
        total = ((eplist["pages"] - 1) * limit) + len(results_no_recursive)
    else:
        total = eplist["pages"] * limit
    for i in range(eplist["pages"] - 1):
        results.extend(results_no_recursive)
    if len(results) < total:
        for _ in range(total - len(results)):
            results.insert(0, rankey(8))
    _page = Pagination(
        results,
        page_data=page_data,
        item_data=item_data,
        item_title=item_title
    )
    index = page
    lines = 5
    columns = 3
    kb = _page.create(index, lines, columns)
    await bot.edit_inline_reply_markup(inline_message_id, reply_markup=ikb(kb))

    # if 1 < eplist["page"] < eplist["pages"]:
    #     append_btns = [
    #         InlineKeyboardButton("Anterior", f'anime_{page - 1}_{data}'),
    #         InlineKeyboardButton("Siguiente", f'anime_{page + 1}_{data}')
    #     ]
    # elif eplist["page"] == 1 and eplist["pages"] > 1:
    #     append_btns = [
    #         InlineKeyboardButton("Siguiente", f'anime_{page + 1}_{data}')
    #     ]
    # elif eplist["page"] != 1:
    #     append_btns = [
    #         InlineKeyboardButton("Anterior", f'anime_{page - 1}_{data}')
    #     ]
    #
    # btns = [
    #     InlineKeyboardButton(
    #         f'{xname(eplist["results"][i]["name"])}',
    #         f'{eplist["results"][i]["id"]}!') for i in range(len(eplist["results"]))
    # ]
    #
    # if append_btns:
    #     btns.extend(append_btns)
    # btns = order(btns, 3)
    #
    # try:
    #     await bot.edit_inline_reply_markup(inline_message_id,
    #                                        reply_markup=InlineKeyboardMarkup(btns))
    # except Exception as e:
    #     print(e)


@Client.on_callback_query(filters.regex(r"view_page .*"))
async def __vpg__(bot, update):
    print(update)

