import re
import cloudscraper
from bs4 import BeautifulSoup
from pyromod.helpers import ikb
from pyromod.nav import Pagination
from pyrogram import Client, filters
from ..Japanemi_features.utils import rankey
from ..helper.__vars__ import auth_users_async


def page_data(page):
    return f'jk_{anime_uri}_{page}'


def item_data(item, page):
    if isinstance(item, dict):
        return f'capjk_{anime_uri}_{item["number"]}'
    else:
        return f'{rankey(8)}'


def item_title(item, page):
    if isinstance(item, dict):
        return f'Capítulo {item["number"]}'
    else:
        return f'{rankey(8)}'


async def request_anime_jk(requests, url, slug_title, slug_add="/"):
    r = requests.get(url + slug_title + slug_add, allow_redirects=False)
    if r.status_code == 200:
        return r
    else:
        r = requests.get(
            "https://jkanime.net/ajax/ajax_search/",
            params={
                "q": slug_title
            }
        )
        for anime in r.json()["animes"]:
            mt = re.match(rf"{slug_title}", anime["title"])
            if mt:
                return requests.get(url + anime["slug"] + slug_add)
            else:
                pass


@Client.on_callback_query(filters.regex(r"jk_.*"))
async def __capsjk__(bot, update):
    print(update)
    global anime_uri
    xxs = None
    chat_id = None
    anime_uri = None
    message_id = None
    inline_message_id = None
    query_id = update.id
    user_id = update.from_user.id
    try:
        data = update.data
        chat_id = update.message.chat.id
        message_id = update.message.message_id
    except AttributeError:
        # data = update.data + "$"
        # Ese data es por si falla y lo dejo como antes
        # nt2 = Solo dios sabe que chinga estoy haciendo
        data = update.data
        inline_message_id = update.inline_message_id
    AUTH_USERS = await auth_users_async()
    if user_id in AUTH_USERS:
        requests = cloudscraper.create_scraper(cloudscraper.Session)

        # Limite siempre 12 en jkanime
        limit = 12

        # Datos
        url_base = "https://jkanime.net/"
        data_split = data.split("_")
        page = int(data_split[-1])
        anime_uri = data_split[1]
        # url = url_base + anime_uri
        # r = requests.get(url)
        r = await request_anime_jk(requests, url_base, anime_uri)
        soup = BeautifulSoup(r.content, "html.parser")
        anime_id = soup.find("div", {"id": "guardar-anime"}).get("data-anime")
        # title = soup.find("div", attrs={"class": "anime__details__title"}).find("h3").string
        number_of_pages = len(soup.find("div", {"class": "anime__pagination"}).find_all("a"))

        results = requests.get(
            "https://jkanime.net/ajax/pagination_episodes/" + anime_id + "/" + str(page)
        ).json()
        results_no_recursive = results.copy()

        if number_of_pages == page:
            total = ((number_of_pages - 1) * limit) + len(results_no_recursive)
        else:
            total = number_of_pages * limit
        for i in range(number_of_pages - 1):
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
        lines = 4
        columns = 3
        kb = _page.create(index, lines, columns)
        await bot.edit_inline_reply_markup(inline_message_id, reply_markup=ikb(kb))
    else:
        await bot.answer_callback_query(
            query_id,
            "No puedes usarlo, sorry.\nMejor mira nuestros canales @Japanemision y @JapanAnime_Oficial",
            True
        )



