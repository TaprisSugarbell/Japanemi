import re
import bcrypt
import anilist
import cloudscraper
import pyrogram.errors
from bs4 import BeautifulSoup
from ..helper.buttons import datos
from pyrogram import Client, filters
from google_trans_new import google_translator
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto)

TAG = lambda anything: f"<a href='{anything}'>&#8205;</a>"
order = lambda some_list, x: [some_list[i:i + x] for i in range(0, len(some_list), x)]


def ak():
    txt = b"_animeblix_17"
    return bcrypt.hashpw(txt, bcrypt.gensalt(10, b"2a"))


async def get_caps(anime_uuid: str = None, episode_uuid: str = None, page: int = 1):
    rq = cloudscraper.create_scraper(cloudscraper.Session)
    if anime_uuid:
        _pr = {
            "page": page
        }
        _ep = "https://animeblix.com/api/animes/" + anime_uuid + "/episodes"
    elif episode_uuid:
        _pr = None
        _ep = "https://animeblix.com/api/episodes/" + episode_uuid + "/players"
    else:
        _pr = {
            "page": page
        }
        _ep = "https://animeblix.com/api/episodes"
    return rq.get(_ep,
                  params=_pr,
                  headers={
                      "ak": ak(),
                      "x-requested-with": "XMLHttpRequest"
                  }
                  ).json()


async def find_anime(anime_name: str, limit: int = 10, page: int = 1):
    return await anilist.AsyncClient().search_anime(anime_name, limit, page)


@Client.on_inline_query(filters.regex(r"^\W?$"))
async def __menu__(bot, update):
    print(update)
    inlineQueryId = update.id
    thumb = "https://tinyurl.com/hiiragishinoa"
    results = [
        InlineQueryResultArticle(
            title="Menú",
            input_message_content=InputTextMessageContent(
                message_text=f'Menú <a href="{thumb}">&#8205;</a>'
            ),
            description=f'Menú para no tener que acordarme de los comandos.',
            thumb_url=thumb,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "AniList",
                            switch_inline_query_current_chat="<ani> "
                        )
                    ],
                    [
                        InlineKeyboardButton("AnimeBlix",
                                             switch_inline_query_current_chat='<blix> '),
                        InlineKeyboardButton("Jkanime",
                                             switch_inline_query_current_chat='<jk> ')
                    ]
                ]
            )
        )
        ]
    await bot.answer_inline_query(inlineQueryId,
                                  results,
                                  cache_time=1)


@Client.on_inline_query(filters.regex(r"^<blix>\s*"))
async def __nnl__(bot, update):
    print(update)
    inlineQueryId = update.id
    query = update.query.strip()[1:-1]
    if query == "blix":
        try:
            offset = int(update.offset)
        except ValueError:
            offset = 1

        requests = cloudscraper.create_scraper()
        caps = await get_caps(page=offset)
        print(caps)
        # print(type(caps))
        # a = AnimeFlash("")
        # animes = a.anime(offset)
        results = []
        for cap in caps["data"]:
            title = cap["title"]
            thumb = cap["img"]
            number = cap["number"]
            anime_uuid = cap["uuid"]
            results.append(
                InlineQueryResultArticle(
                    title=title,
                    input_message_content=InputTextMessageContent(
                        message_text=f'{title} <a href="{thumb}">&#8205;</a>'
                    ),
                    description=f'Capítulo {number}',
                    thumb_url=thumb,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Lista de Episodios",
                                                     f'blix_{anime_uuid}'),
                                InlineKeyboardButton("Subir capítulo",
                                                     f'capblix_{anime_uuid}')
                            ]
                        ]
                    )
                )
            )
        await bot.answer_inline_query(inlineQueryId,
                                      results,
                                      next_offset=f"{offset + 1}",
                                      cache_time=1)
        # if animes["pages"] > 1:
        #     for anime in animes["results"]:
        #         thumb = arm_link(anime, 2)
        #         results.append(
        #             InlineQueryResultArticle(
        #                 title=anime["name"],
        #                 input_message_content=InputTextMessageContent(
        #                     message_text=f'{anime["name"]} <a href="{thumb}">&#8205;</a>'
        #                 ),
        #                 description=f'Capítulo {anime["name"].split()[-1]}',
        #                 thumb_url=thumb,
        #                 reply_markup=InlineKeyboardMarkup(
        #                     [
        #                         [
        #                             InlineKeyboardButton("Lista de episodios", f'anime_1_{anime["anime_id"]}'),
        #                             InlineKeyboardButton("Subir capítulo", f'{anime["id"]}!')
        #                         ]
        #                     ]
        #                 )
        #             )
        #         )
        #     await bot.answer_inline_query(inlineQueryId,
        #                                   results,
        #                                   next_offset=f"{offset + 1}",
        #                                   cache_time=1)
    else:
        pass


@Client.on_inline_query(filters.regex(r"<ani> (\?|.*)"))
async def __ani__(bot, update):
    print(update)
    # tr = google_translator()
    user_id = update.from_user.id
    query = update.query.replace("<ani> ", "")
    inlineQueryId = update.id
    print(query)
    try:
        offset = int(update.offset)
    except ValueError:
        offset = 1
    animes = await find_anime(query, page=offset)
    results = []
    a = anilist.AsyncClient()
    for anime in animes:
        # print(anime)
        title = anime.title
        get = await a.get_anime(anime.id)
        dsc = ""
        if hasattr(get, "format"):
            dsc += f"{get.format}, "
        if hasattr(get, "episodes"):
            dsc += f"({get.episodes} episodes)"
        else:
            dsc += f"(*?)"
        results.append(
            InlineQueryResultArticle(
                title=title.romaji,
                input_message_content=InputTextMessageContent(
                    message_text=f"**{title.romaji}**\n({title.native})\n"
                                 f"{TAG('https://img.anili.st/media/' + str(anime.id))}"
                ),
                description=dsc,
                thumb_url=f"https://img.anili.st/media/{anime.id}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Información", f"{anime.id}-")
                        ]
                    ]
                )
            )
        )
    try:
        print("inline")
        await bot.answer_inline_query(inlineQueryId,
                                      results,
                                      next_offset=f"{offset + 1}")
    except pyrogram.errors.QueryIdInvalid:
        print("noinline")
        btns_unorder = [InlineKeyboardButton(anime.title.romaji, f"{anime.id}-") for anime in animes]
        btns = order(btns_unorder, 1)
        await bot.send_message(chat_id=user_id,
                               text="Sorry por tardar 😭",
                               reply_markup=InlineKeyboardMarkup(btns))
    except Exception as e:
        print(e)
        raise


@Client.on_inline_query(filters.regex(r"<blix> (\?|.*)"))
async def __blix__(bot, update):
    print(update)
    # query = update.query.replace("<anime> ", "")
    # if query.strip() == "?":
    #     query = ""
    # # query = update.query
    # inlineQueryId = update.id
    # print(query)
    # # try:
    # try:
    #     offset = int(update.offset)
    # except ValueError:
    #     offset = 1
    # a = AnimeFlash(query)
    # animes = a.anime(offset)
    # results = []
    # print(animes)
    # if animes["pages"] > 1:
    #     for anime in animes["results"]:
    #         try:
    #             chapter_s = anime["chapters"]
    #             thumb = arm_link(anime, 1)
    #             results.append(
    #                 InlineQueryResultArticle(
    #                     title=anime["name"],
    #                     input_message_content=InputTextMessageContent(
    #                         message_text=f'{anime["name"]} <a href="{thumb}">&#8205;</a>'
    #                     ),
    #                     description=f'Capítulos: {chapter_s} {chapters(anime, "Siguiente:")}',
    #                     thumb_url=thumb,
    #                     reply_markup=InlineKeyboardMarkup(
    #                         [
    #                             [
    #                                 InlineKeyboardButton("Lista de episodios", f'anime_1_{anime["id"]}')
    #                             ]
    #                         ]
    #                     )
    #                 )
    #             )
    #         except KeyError:
    #             thumb = arm_link(anime, 2)
    #             results.append(
    #                 InlineQueryResultArticle(
    #                     title=anime["name"],
    #                     input_message_content=InputTextMessageContent(
    #                         message_text=f'{anime["name"]} <a href="{thumb}">&#8205;</a>'
    #                     ),
    #                     description=f'Capítulo {anime["name"].split()[-1]}',
    #                     thumb_url=thumb,
    #                     reply_markup=InlineKeyboardMarkup(
    #                         [
    #                             [
    #                                 InlineKeyboardButton("Lista de episodios", f'anime_1_{anime["anime_id"]}'),
    #                                 InlineKeyboardButton("Subir capítulo", f'{anime["id"]}!')
    #                             ]
    #                         ]
    #                     )
    #                 )
    #             )
    #     await bot.answer_inline_query(inlineQueryId,
    #                                   results,
    #                                   next_offset=f"{offset + 1}")
    # else:
    #     for anime in animes["results"]:
    #         thumb = arm_link(anime, 1)
    #         results.append(
    #             InlineQueryResultArticle(
    #                 title=anime["name"],
    #                 input_message_content=InputTextMessageContent(
    #                     message_text=f'{anime["name"]} <a href="{thumb}">&#8205;</a>'
    #                 ),
    #                 description=f'Capítulos: {anime["chapters"]} {chapters(anime, "Siguiente:")}',
    #                 thumb_url=thumb,
    #                 reply_markup=InlineKeyboardMarkup(
    #                     [
    #                         [
    #                             InlineKeyboardButton("Lista de episodios", f'anime_1_{anime["id"]}')
    #                         ]
    #                     ]
    #                 )
    #             )
    #         )
    # await bot.answer_inline_query(inlineQueryId,
    #                               results)


@Client.on_inline_query(filters.regex(r"^<jk>[.\s]*"))
async def __jk__(bot, update):
    print(update)
    results = []
    parser = "html.parser"
    url = "https://jkanime.net"
    inlineQueryId = update.id
    query = update.query
    quer = query.strip()[1:-1]
    requests = cloudscraper.create_scraper(cloudscraper.Session)
    if quer == "jk":
        try:
            offset = int(update.offset)
        except ValueError:
            offset = 1

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        caps = soup.find("div", {"class": "maximoaltura"}).find_all("a")
        # print(caps)
        # print(type(caps))
        # a = AnimeFlash("")
        # animes = a.anime(offset)
        for cap in caps:
            _ti = cap.find("img")
            title = _ti.get("alt")
            thumb = _ti.get("src")
            link = cap.get("href")
            link_split = link.split("/")
            anime_uri = link_split[3]
            number = link_split[-2]
            results.append(
                InlineQueryResultPhoto(
                    thumb,
                    title=title,
                    description=f'Capítulo {number}',
                    caption=f'**{title}**',
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Lista de Episodios",
                                                     f'jk_{anime_uri}_1'),
                                InlineKeyboardButton("Subir capítulo",
                                                     f'capjk_{anime_uri}_{number}')
                            ]
                        ]
                    )
                )
            )
    else:
        url_find = "https://jkanime.net/ajax/ajax_search/"
        r = requests.get(
            url_find,
            params={
                "q": query.replace("<jk>", "").strip()
            }
        )
        for result in r.json()["animes"]:
            title = result["title"]
            thumb = result["image"]
            anime_uri = result["slug"]
            if len(anime_uri) > 54:
                anime_uri = " ".join(title.split()[:4])
            caption = f'**{title}**'
            results.append(
                InlineQueryResultPhoto(
                    thumb,
                    title=title,
                    caption=caption,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Lista de Episodios",
                                                     f'jk_{anime_uri}_1')
                            ]
                        ]
                    )
                )
            )

    await bot.answer_inline_query(inlineQueryId,
                                  results,
                                  cache_time=1)

