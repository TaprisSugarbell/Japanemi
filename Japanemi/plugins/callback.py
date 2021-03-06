import re
import bcrypt
import random
import string
from .. import sayulog
from shutil import rmtree
from decouple import config
from ..helper.buttons import *
from ..plugins.Japanemi import *
from ..helper.mongo_connect import *
from ..helper.callback_helper import *
from moviepy.editor import VideoFileClip
from ..helper.texts import capupload_text
from ..helper.__vars__ import auth_users_async
from ..helper.get_servers import get_ao_servers
from ..Japanemi_features.utils import create_folder
from ..plugins.ao_get_anime import request_anime_ao
from ..plugins.jk_get_anime import request_anime_jk

CHANNEL_ID = config("CHANNEL_ID", default=None, cast=int)
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


async def get_jk_servers(url):
    parser = "html.parser"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, parser)

    _script = soup.find_all("script")
    _lnks = re.compile(r'https?://[\w./?=#-]*')
    # _lnks = re.compile(r'(https?:/)?[\w./?=#-]*')
    _lks = ""
    for i in _script:
        if hasattr(i, "string"):
            if i.string:
                if "var video = [];" in i.string:
                    _lks = i.string
                    break
                else:
                    pass
    _links = _lnks.findall(_lks.replace('src="/', 'src="https://jkanime.net/'))
    print(_links)
    _servers = []
    for _link in _links:
        mode = _link.split("/")[3].split("?")[0]
        if mode == "um2.php":
            _r = requests.get(
                _link,
                headers={
                    "referer": url
                }
            )
            _soup = BeautifulSoup(
                _r.content,
                parser
            )
            _value = _soup.find("input").get("value")
            _r1 = requests.post(
                "https://jkanime.net/gsplay/redirect_post.php",
                data={
                    "data": _value
                },
                headers={
                    "host": "jkanime.net",
                    "origin": "https://jkanime.net",
                    "referer": _link
                },
                allow_redirects=False
            )
            _v = _r1.headers["location"].replace("/gsplay/player.html#", "")
            _r2 = requests.post(
                "https://jkanime.net/gsplay/api.php",
                data={
                    "v": _v
                }
            )
            _servers.append(_r2.json()["file"])
        elif mode == "um.php":
            _r = requests.get(
                _link
            )
            _soup = BeautifulSoup(
                _r.content,
                parser
            )
            _servers.append(_lnks.findall(_soup.find_all("script")[-1].string)[0])
        elif mode == "embed":
            pass
        elif mode == "jk.php":
            _r = requests.get(
                _link
            )
            _soup = BeautifulSoup(
                _r.content,
                parser
            )
            _lnk = _lnks.findall(_soup.find_all("script")[-1].string)[0]
            _r1 = requests.get(_lnk, allow_redirects=False)
            _servers.append(_r1.headers["location"])
        elif mode == "jkokru.php":
            _servers.append("https://ok.ru/videoembed/" + _link.split("u=")[-1])
        elif mode == "jkfembed.php":
            _servers.append("https://fembed.com/v/" + _link.split("u=")[-1])
        elif mode == "jkvmixdrop.php":
            _servers.append("https://mixdrop.co/e/" + _link.split("u=")[-1])
        else:
            _servers.append(_link)
        return [i for i in _servers if i]


@Client.on_callback_query(filters.regex(r"\d*-$"))
async def __an__(bot, update):
    print(update)
    await Ani_callback(bot, update)


# @Client.on_callback_query(filters.regex(r"[ha]?\d*[!|,|-]"))
# async def callback_data(bot, update):
#     print(update)
#     inline = None
#     user = update.from_user.id
#     try:
#         chat_id = update.message.chat.id
#         message_id = update.message.message_id
#         data = update.data
#     except AttributeError:
#         data = update.data + "$"
#         chat_id = None
#         message_id = update.inline_message_id
#     key = string.hexdigits
#     session_random = "".join([random.choice(key) for i in range(5)])
#     # Carpeta
#     tmp_directory = "./Downloads/" + str(user) + "/" + session_random + "/"
#     if not os.path.isdir(tmp_directory):
#         os.makedirs(tmp_directory)
#     # ****************************************************************
#     if user in AUTH_USERS:
#         # data = update.data
#         print(data)
#         # *****************************
#         if "_" in data:
#             data = data.split("_")[0]
#             print(data)
#             if data == "h":
#                 inline = await hla_buttons()
#             elif data == "a":
#                 inline = await af_buttons()
#             KEY = string.hexdigits
#             RCH = "".join([random.choice(KEY) for i in range(5)])
#             try:
#                 await bot.edit_message_text(chat_id=chat_id,
#                                             message_id=message_id,
#                                             text=f"#{RCH}\nUltimos episodios",
#                                             reply_markup=inline)
#             except Exception as e:
#                 print(e)
#         elif "!" in data:
#             await af_callback(bot, data, update, tmp_directory)
#         elif "|" in data:
#             await hla_callback(bot, data, tmp_directory)
#         elif "reload" in data:
#             if "hla" in data:
#                 inline = await hla_buttons()
#             elif "af" in data:
#                 inline = await af_buttons()
#             KEY = string.hexdigits
#             RCH = "".join([random.choice(KEY) for i in range(5)])
#             try:
#                 await bot.edit_message_text(chat_id=chat_id,
#                                             message_id=message_id,
#                                             text=f"#{RCH}\nUltimos episodios",
#                                             reply_markup=inline)
#             except Exception as e:
#                 print(e)
#         elif "," in data:
#             if "trailer" in data:
#                 await trailer(bot, update, tmp_directory)
#             else:
#                 await ani_callback(bot, update)
#         elif "-" in data:
#             await Ani_callback(bot, update)
#     else:
#         pass


@Client.on_callback_query(filters.regex(r"capblix_.*"))
async def __capblix__(bot, update):
    print(update)
    xxs = None
    # inline = None
    user_id = update.from_user.id
    AUTH_USERS = await auth_users_async()
    # try:
    #     chat_id = update.message.chat.id
    #     message_id = update.message.message_id
    #     data = update.data
    # except AttributeError:
    # data = update.data + "$"
    # Ese data es por si falla y lo dejo como antes
    data = update.data
    chat_id = None
    message_id = update.inline_message_id
    key = string.hexdigits
    session_random = "".join([random.choice(key) for _ in range(5)])
    if user_id in AUTH_USERS:
        # Carpeta
        tmp_directory = await create_folder(user_id)
        # ****************************************************************
        episode_uuid = data.replace("capblix_", "")
        server_links = await get_caps(episode_uuid=episode_uuid)
        links = [i["url"] for i in server_links]
        caption = f'@Japanemision'
        # UPLOAD
        mdts = links, caption
        dats = data, chat_id, user_id, tmp_directory
        await up_(bot, dats, mdts)


@Client.on_callback_query(filters.regex(r"capjk_.*"))
async def __capjk__(bot, update):
    print(update)
    xxs = None
    chat_id = None
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
        # Carpeta
        tmp_directory = create_folder(user_id)
        # ****************************************************************
        url_base = "https://jkanime.net/"
        data_split = data.split("_")
        anime_uri = data_split[1]
        number = data_split[-1]
        url = url_base + anime_uri + "/" + number
        sayulog.warning(f'{data_split} {url}')
        r = await request_anime_jk(requests, url_base, anime_uri, "/" + number + "/")
        if " " in url:
            url = r.url
        links = await get_jk_servers(url)
        if len(links) == 0:
            links = await get_jk_servers(url)
        sayulog.warning(f'"{r.status_code}" [{r.request.url}] [{r.url}] {links}')
        soup = BeautifulSoup(r.content, "html.parser")
        title = soup.find("div", attrs={"id": "marcar_visto"}).get("data-title")
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


@Client.on_callback_query(filters.regex(r"capao_.*"))
async def __capao__(bot, update):
    print(update)
    xxs = None
    chat_id = None
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
        c = cloudscraper.create_scraper()
        # Carpeta
        tmp_directory = create_folder(user_id)
        # ****************************************************************
        url_base = "https://www1.animeonline.ninja/"
        data_split = data.split("_")
        slug_key = data_split[1]
        lngj = data_split[-1]
        if lngj == "Non":
            lngj = None
        _c = await confirm(ttls, {"cap_key": slug_key})
        _c = _c[0]
        title = _c["title"]
        _dem = _c["dem"]
        slug = _c["slug"]
        episode = _c["episode"]
        url = f'{url_base}{_dem}/{slug}/'
        sayulog.warning(f'{data_split} {url}')
        r = c.get(url, allow_redirects=False)
        soup = BeautifulSoup(r.content, "html.parser")
        # title_find = soup.find("h1", attrs={"class": "epih1"}).text.strip()
        # title = re.subn(r':\s\d*x\d*', "", title)[0]
        sl = await get_ao_servers(url, lngj)
        print(sl)
        if isinstance(sl, dict):
            lbsl = []
            if sl["JP"]:
                lbsl.append(
                    InlineKeyboardButton("JP", f'capao_{slug_key}_JP')
                )
            if sl["LAT"]:
                lbsl.append(
                    InlineKeyboardButton("LAT", f'capao_{slug_key}_LAT')
                )
            if sl["ES"]:
                lbsl.append(
                    InlineKeyboardButton("ES", f'capao_{slug_key}_ES')
                )
            await bot.edit_inline_reply_markup(
                inline_message_id,
                InlineKeyboardMarkup(
                    [
                        lbsl
                    ]
                )
            )
        else:
            caption = await capupload_text(title + " " + str(episode))
            # UPLOAD
            mdts = sl, caption
            dats = data, chat_id, user_id, (message_id, inline_message_id), tmp_directory
            try:
                await bot.answer_callback_query(
                    query_id,
                    f'Se esta subiendo "{title} {episode}"',
                    True
                )
            except Exception as e:
                sayulog.warning(f'{e}')
            await up_(bot, dats, mdts)
    else:
        await bot.answer_callback_query(
            query_id,
            f'Lo lamento pero no sos admin.\nSigue @Japanemision y @JapanAnime_Oficial',
            True
        )




