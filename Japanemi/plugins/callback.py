import re
import bcrypt
import random
import string
from shutil import rmtree
from decouple import config
from ..helper.buttons import *
from ..plugins.Japanemi import *
from ..helper.callback_helper import *
from moviepy.editor import VideoFileClip
from ..helper.texts import capupload_text

CHANNEL_ID = config("CHANNEL_ID", default=None, cast=int)
AUTH_USERS = [int(i) for i in config("AUTH_USERS", default="784148805").split(" ")]


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
        tmp_directory = "./Downloads/" + str(user_id) + "/" + session_random + "/"
        if not os.path.isdir(tmp_directory):
            os.makedirs(tmp_directory)
        # ****************************************************************
        episode_uuid = data.replace("capblix_", "")
        server_links = await get_caps(episode_uuid=episode_uuid)
        links = [i["url"] for i in server_links]
        caption = f'@Japanemision'
        msd = await bot.send_message(update.from_user.id,
                                     "Descargando video.")
        try:
            sayulog.warning("Links: %r", links)
            fff = await foriter(links, tmp_directory)
            path = fff["file"]
            file_type = fff["type"]
            yes_thumb = fff["thumb"]
            clip = VideoFileClip(path)
            size = clip.size
            height = size[1]
            width = size[0]
            duration = int(clip.duration)
            print(duration)
            print(os.listdir(tmp_directory))
            try:
                await bot.edit_message_text(chat_id=update.from_user.id,
                                            text=f"Subiendo {file_type}.",
                                            message_id=int(msd.message_id))
            except Exception as e:
                print(e)
            if yes_thumb:
                await bot.send_video(chat_id=CHANNEL_ID,
                                     width=width,
                                     height=height,
                                     video=path,
                                     thumb=yes_thumb,
                                     caption=caption,
                                     duration=duration)
            else:
                await bot.send_video(chat_id=CHANNEL_ID,
                                     width=width,
                                     height=height,
                                     video=path,
                                     caption=caption,
                                     duration=duration)
        except BlockingIOError as e:
            sayulog.error(e)
            xxs = await bot.send_message(chat_id=update.from_user.id,
                                         text="Se lleno la memoria del bot, "
                                              "se reiniciara y en 1m puedes dar click de nuevo :3.")
            heroku_conn = heroku3.from_key(HEROKU_API_KEY)
            app = heroku_conn.app(HEROKU_APP_NAME)
            app.restart()
        except Exception as e:
            print(e)
            sayulog.error("Ha ocurrido un error.", exc_info=e)
            e = sys.exc_info()
            err = '{}: {}'.format(str(e[0]).split("'")[1], e[1].args[0])
            xxs = await bot.send_message(chat_id=update.from_user.id,
                                         text=f"{err}\n📮 Envía este error a @SayuOgiwara")
            raise
        finally:
            await bot.delete_messages(chat_id=update.from_user.id,
                                      message_ids=int(msd.message_id))
            if xxs:
                rmtree("./Downloads")
            else:
                rmtree(tmp_directory)
                sayulog.warning(f'{os.listdir("./Downloads/")}')

