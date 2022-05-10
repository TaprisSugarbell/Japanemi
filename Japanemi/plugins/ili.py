import re
import bcrypt
import anilist
import cloudscraper
import pyrogram.errors
from bs4 import BeautifulSoup
from ..helper.buttons import datos
from pyrogram import Client, filters
from ..helper.mongo_connect import *
from ..Japanemi_features.utils import rankey
from google_trans_new import google_translator
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto)

TAG = lambda anything: f"<a href='{anything}'>&#8205;</a>"
order = lambda some_list, x: [some_list[i:i + x] for i in range(0, len(some_list), x)]
ra = Mongo(URI, "Japanemi", "otakustv")
ttls = Mongo(URI, "Japanemi", "slugs")


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
                    ],
                    [
                        InlineKeyboardButton(
                            "Otakustv",
                            switch_inline_query_current_chat="<otakustv> "
                        )
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


@Client.on_inline_query(filters.regex(r"^<ani>[.\s]*"))
async def __ani__(bot, update):
    print(update)
    # tr = google_translator()
    user_id = update.from_user.id
    query = update.query.replace("<ani>", "").strip()
    inlineQueryId = update.id
    print(query)
    results = []
    try:
        offset = int(update.offset)
    except ValueError:
        offset = 1
    if len(query) == 0:
        results.append(
            InlineQueryResultArticle(
                title="Busca un anime",
                input_message_content=InputTextMessageContent(
                    "Busca un anime."
                ),
                description="Prueba buscando el anime que te gusta.",
                thumb_url="https://tinyurl.com/iwakuralaln",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "AniList",
                                switch_inline_query_current_chat="<ani> "
                            )
                        ]
                    ]
                )
            )
        )
        await bot.answer_inline_query(inlineQueryId,
                                      results)
    else:
        animes = await find_anime(query, page=offset)
        a = anilist.AsyncClient()
        if isinstance(animes, tuple):
            animes = animes[0]
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
            if len(anime_uri) > 30:
                # anime_uri = " ".join(title.split()[-5:])
                anime_uri = " ".join(anime_uri.split("-")[-5:])
            print(anime_uri)
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


@Client.on_inline_query(filters.regex(r"^<otakustv>[.\s]*"))
async def __otakutv__(bot, update):
    print(update)
    results = []
    anime_key = None
    parser = "html.parser"
    inlineQueryId = update.id
    query = update.query
    quer = query.strip()[1:-1]
    url = "https://www.otakustv.com"
    blnk = "https://www.otakustv.com/anime/"
    requests = cloudscraper.create_scraper(cloudscraper.Session)
    if quer == "otakustv":
        r = requests.get(
            url
        )
        soup = BeautifulSoup(r.content, parser)
        for i in soup.find("div", attrs={"class": "row"}).find_all("div"):
            thumb = i.find("img").get("data-src")
            title = i.find("img").get("alt")
            link = i.find("a").get("href")
            description = i.find("a").get("title")
            episode = i.find("p").string.split()[-1]
            link_split = link.split("/")
            anime_uri = link_split[-2]
            anime_episode = link_split[-1]
            _c = await confirm(ra, {"anime_uri": anime_uri,
                                    "anime_episode": anime_episode})
            if _c:
                _c = _c[0]
                anime_key = _c["anime_key"]
            else:
                anime_key = rankey(30)
                await add_(ra, {
                    "anime": title,
                    "episode": episode,
                    "anime_key": anime_key,
                    "anime_uri": anime_uri,
                    "anime_episode": anime_episode
                }
                           )
            results.append(
                InlineQueryResultArticle(
                    title + " | " + episode,
                    InputTextMessageContent(
                        title + " " + TAG(thumb)
                    ),
                    None,
                    InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Lista de Episodios",
                                                     f'{rankey(8)}'),
                                InlineKeyboardButton(
                                    "Subir capítulo",
                                    f'capotakustv_{anime_key}'
                                )
                            ]
                        ]
                    ),
                    None,
                    description,
                    thumb
                )
            )
        await bot.answer_inline_query(inlineQueryId,
                                      results,
                                      cache_time=1)
    else:
        pass


@Client.on_inline_query(filters.regex(r"^<ao>[.\s]*"))
async def __anime_online__(bot, update):
    print(update)
    results = []
    anime_key = None
    parser = "html.parser"
    inlineQueryId = update.id
    query = update.query
    quer = query.strip()[1:-1]
    url = "https://www1.animeonline.ninja"
    blnk = "https://www1.animeonline.ninja/episodio/{}/"
    requests = cloudscraper.create_scraper(cloudscraper.Session)
    # Get caps
    r = requests.get(
        url
    )
    soup = BeautifulSoup(r.content, parser)
    _items = soup.find("div", attrs={"class": "items"})
    for _item in _items:
        if not isinstance(_item.find("h3"), int):
            # print(_item)
            _spans = _item.find_all("span")
            if len(_spans) > 1:
                qua = f'[{_spans[-1].string}]'
            else:
                qua = ""
            _link_of_cap = _item.find("a").get("href")
            lnk_splt = _link_of_cap.split("/")
            _dem = lnk_splt[-3]
            slug = _link_of_cap.split("/")[-2]
            thumb = _item.find("img").get("data-src")
            title = _item.find("h3").text
            episode = _item.find("h4").text.strip().split()[-1]
            cap_key = rankey(10)
            dts = {
                "cap_key": cap_key,
                "title": title,
                "dem": _dem,
                "slug": slug,
                "episode": episode
            }
            _c = await confirm(
                ttls,
                {
                    "title": title,
                    "dem": _dem,
                    "slug": slug,
                    "episode": episode
                }
            )
            if _c:
                _c = _c[0]
                cap_key = _c["cap_key"]
            else:
                await add_(ttls, dts)
            results.append(
                InlineQueryResultPhoto(
                    thumb,
                    title=title,
                    caption=f'**{title}**',
                    description=f'Capítulo {episode} {qua}',
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Lista de Episodios", "nth"),
                                InlineKeyboardButton("Subir capítulo", f"capao_{cap_key}_Non")
                            ]
                        ]
                    )
                )
            )
        else:
            pass

    await bot.answer_inline_query(inlineQueryId,
                                  results,
                                  cache_time=1)
