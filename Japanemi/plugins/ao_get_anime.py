import re
import cloudscraper
from bs4 import BeautifulSoup
from pyromod.helpers import ikb
from pyromod.nav import Pagination
from pyrogram import Client, filters
from ..helper.mongo_connect import *
from ..Japanemi_features.utils import rankey
from ..helper.__vars__ import auth_users_async


ttls = Mongo(URI, "Japanemi", "slugs")


async def request_anime_ao(requests, url, slug_key, slug_add="/"):
    _c = await confirm(ttls, {"cap_key": slug_key})
    slug_title = _c[0]["title"]
    _dem = _c[0]["dem"] + "/"
    return requests.get(url + _dem + slug_title + slug_add, allow_redirects=False)

