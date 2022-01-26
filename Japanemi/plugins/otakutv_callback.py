import time
import cloudscraper
from .. import sayulog
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from ..helper.mongo_connect import *
from ..helper.__vars__ import auth_users_async
from ..Japanemi_features.utils import create_folder
from ..helper.callback_helper import up_, capupload_text


ra = Mongo(URI, "Japanemi", "otakustv")


async def get_otakutv_cap(requests, url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    get_value = lambda x: x.get("value")
    _streaming_lst = []
    for i in map(get_value, soup.find("select", attrs={"id": "ssel"}).find_all("option")):
        r1 = requests.get(
            "https://www.otakustv.com/play-video",
            params={
                "id": i
            }
        )
        try:
            orl = r1.json()["url"]
            if "//ok.ru" in orl:
                orl = "https:" + orl
            _streaming_lst.append(
                orl
            )
        except Exception as e:
            print(e)
            print(i)
        time.sleep(3)
    r2 = requests.get(
        url.replace("/anime/", "/descargar/")
    )

    get_down = lambda x: x.get("href")
    _streaming_lst.extend(
        map(
            get_down,
            BeautifulSoup(r2.content, "html.parser").find("div", attrs={"class": "bloque_download"}).find_all("a")
        )
    )
    return _streaming_lst


@Client.on_callback_query(filters.regex(r"capotakustv_.*"))
async def __capotakutv__(bot, update):
    print(update)
    xxs = None
    title = ""
    number = ""
    chat_id = None
    anime_uri = ""
    message_id = None
    anime_episode = ""
    query_id = update.id
    inline_message_id = None
    user_id = update.from_user.id
    requests = cloudscraper.create_scraper(cloudscraper.Session)
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
        # Carpeta
        # tmp_directory = create_folder(user_id)
        tmp_directory = ""
        # ****************************************************************
        blnk = "https://www.otakustv.com/anime/"
        data_split = data.split("_")
        anime_key = data_split[-1]
        _c = await confirm(ra, {"anime_key": anime_key})
        if _c:
            _c = _c[0]
            title = _c["anime"]
            number = _c["episode"]
            anime_uri = _c["anime_uri"]
            anime_episode = _c["anime_episode"]
        else:
            await bot.answer_callback_query(
                query_id,
                "Ha fallado :'C",
                True
            )
        url = blnk + anime_uri + "/" + anime_episode
        sayulog.warning(f'{data_split} {url}')
        links = await get_otakutv_cap(requests, url)
        print(links)
        # r = requests.get(url)
        # soup = BeautifulSoup(r.content, "html.parser")
        # title = soup.find("p", attrs={"class": "text-white font22 mb-0"}).string.strip()
        caption = await capupload_text(title + " " + str(number))
        # UPLOAD
        mdts = links, caption
        dats = data, chat_id, user_id, (message_id, inline_message_id), tmp_directory
        await bot.answer_callback_query(
            query_id,
            f'Se esta subiendo "{title} {number}"',
            True
        )
        await up_(bot, dats, mdts)
    else:
        await bot.answer_callback_query(
            query_id,
            f'Lo lamento pero no sos admin.\nSigue @Japanemision y @JapanAnime_Oficial',
            True
        )









