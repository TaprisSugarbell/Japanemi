import re
import random
import string
from decouple import config
from ..helper.buttons import *
from ..plugins.Japanemi import *
from ..helper.callback_helper import *

CHANNEL_ID = config("CHANNEL_ID", default=None, cast=int)
AUTH_USERS = [int(i) for i in config("AUTH_USERS", default="784148805").split(" ")]


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


@Client.on_callback_query()
async def callback_data(bot, update):
    print(update)
    try:
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
    except Exception as e:
        print(e)
        append_btns = None
        chat_id = update.from_user.id
        data = int(update.data.split("_")[-1])
        page = int(update.data.split("_")[1])
        if page > 1:
            li = 9
        else:
            li = 8
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
        eplist = a.episodes(page=page, limit=li)
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

        xname = lambda x: re.findall(r"(\d+ y \d+|\d+ Y \d+|\d+)", x)[-1]

        btns = [
            InlineKeyboardButton(
                f'Capítulo {xname(eplist["results"][i]["name"])}',
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