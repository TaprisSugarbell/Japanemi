import re
import anilist
import pyrogram.errors
from ..AnimeFlash import *
from ..helper.buttons import datos
from pyrogram import Client, filters
from google_trans_new import google_translator
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)

TAG = lambda anything: f"<a href='{anything}'>&#8205;</a>"
order = lambda some_list, x: [some_list[i:i + x] for i in range(0, len(some_list), x)]


async def find_anime(anime_name: str, limit: int = 10, page: int = 1):
    return await anilist.AsyncClient().search_anime(anime_name, limit, page)


@Client.on_inline_query(filters.regex(r"^<anime>$"))
async def __nnl__(bot, update):
    print(update)
    inlineQueryId = update.id
    query = update.query[1:-1]
    if query == "anime":
        try:
            offset = int(update.offset)
        except ValueError:
            offset = 1
        a = AnimeFlash("")
        animes = a.anime(offset)
        results = []
        if animes["pages"] > 1:
            for anime in animes["results"]:
                thumb = arm_link(anime, 2)
                results.append(
                    InlineQueryResultArticle(
                        title=anime["name"],
                        input_message_content=InputTextMessageContent(
                            message_text=f'{anime["name"]} <a href="{thumb}">&#8205;</a>'
                        ),
                        description=f'Capítulo {anime["name"].split()[-1]}',
                        thumb_url=thumb,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("Lista de episodios", f'anime_1_{anime["anime_id"]}'),
                                    InlineKeyboardButton("Subir capítulo", f'{anime["id"]}!')
                                ]
                            ]
                        )
                    )
                )
            await bot.answer_inline_query(inlineQueryId,
                                          results,
                                          next_offset=f"{offset + 1}",
                                          cache_time=1)
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


@Client.on_inline_query(filters.regex(r"<anime> (\?|.*)"))
async def __anime__(bot, update):
    print(update)
    query = update.query.replace("<anime> ", "")
    if query.strip() == "?":
        query = ""
    # query = update.query
    inlineQueryId = update.id
    print(query)
    # try:
    try:
        offset = int(update.offset)
    except ValueError:
        offset = 1
    a = AnimeFlash(query)
    animes = a.anime(offset)
    results = []
    print(animes)
    if animes["pages"] > 1:
        for anime in animes["results"]:
            try:
                chapter_s = anime["chapters"]
                thumb = arm_link(anime, 1)
                results.append(
                    InlineQueryResultArticle(
                        title=anime["name"],
                        input_message_content=InputTextMessageContent(
                            message_text=f'{anime["name"]} <a href="{thumb}">&#8205;</a>'
                        ),
                        description=f'Capítulos: {chapter_s} {chapters(anime, "Siguiente:")}',
                        thumb_url=thumb,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("Lista de episodios", f'anime_1_{anime["id"]}')
                                ]
                            ]
                        )
                    )
                )
            except KeyError:
                thumb = arm_link(anime, 2)
                results.append(
                    InlineQueryResultArticle(
                        title=anime["name"],
                        input_message_content=InputTextMessageContent(
                            message_text=f'{anime["name"]} <a href="{thumb}">&#8205;</a>'
                        ),
                        description=f'Capítulo {anime["name"].split()[-1]}',
                        thumb_url=thumb,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("Lista de episodios", f'anime_1_{anime["anime_id"]}'),
                                    InlineKeyboardButton("Subir capítulo", f'{anime["id"]}!')
                                ]
                            ]
                        )
                    )
                )
        await bot.answer_inline_query(inlineQueryId,
                                      results,
                                      next_offset=f"{offset + 1}")
    else:
        for anime in animes["results"]:
            thumb = arm_link(anime, 1)
            results.append(
                InlineQueryResultArticle(
                    title=anime["name"],
                    input_message_content=InputTextMessageContent(
                        message_text=f'{anime["name"]} <a href="{thumb}">&#8205;</a>'
                    ),
                    description=f'Capítulos: {anime["chapters"]} {chapters(anime, "Siguiente:")}',
                    thumb_url=thumb,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Lista de episodios", f'anime_1_{anime["id"]}')
                            ]
                        ]
                    )
                )
            )
        await bot.answer_inline_query(inlineQueryId,
                                      results)
