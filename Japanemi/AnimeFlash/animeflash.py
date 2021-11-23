import json
import requests
import cloudscraper
import urllib.parse
from datetime import datetime, timedelta


class AnimeFlash:

    @staticmethod
    def clean_id(url, rev=-2):
        return url.split("/")[rev]

    def __init__(self, query=None, url=None, anime_id=0, episode=0):
        self.url = url
        self.query = query
        self.episode = episode
        self.anime_id = anime_id
        self.base = "https://api.animeflash.xyz/v1/"

    def anime(self, page=1, limit=10, order="desc"):
        if self.query:
            r = requests.get(
                self.base +
                f"anime/searcher?q={urllib.parse.quote_plus(self.query)}&"
                f"order_by=id&order={order}&page={page}&limit={limit}")
            return r.json()["response"]
        elif self.url:
            r = requests.get(self.base +
                             "anime/" +
                             self.clean_id(self.url))
            try:
                return r.json()["response"]
            except json.decoder.JSONDecodeError:
                return "The link is invalid."
        elif self.anime_id > 0:
            r = requests.get(self.base +
                             f"anime/{self.anime_id}")
            return r.json()["response"]
        else:
            r = requests.get(self.base +
                             f"episode/simulcasts?limit={limit}&page={page}")
            return r.json()["response"]

    def episodes(self, page=1, limit=10, order="asc"):
        if self.url:
            r = requests.get(self.base +
                             f"episode/searcher?"
                             f"page={page}&limit={limit}&"
                             f"order_by=weight&order={order}&anime_id={self.clean_id(self.url)}")
            return r.json()["response"]
        elif self.episode > 0:
            r = requests.get(self.base +
                             f"episode/{self.episode}")
            return r.json()["response"]
        else:
            r = requests.get(self.base +
                             f"episode/searcher?"
                             f"page={page}&limit={limit}&"
                             f"order_by=weight&order={order}&anime_id={self.anime_id}")
            return r.json()["response"]

    def links(self, episode):
        if isinstance(episode, dict):
            r = requests.get(self.base +
                             "stream/" +
                             "".join(episode["streams"][2:-2]) +
                             "/public")
            if r.status_code == 404:
                r = requests.get(self.base +
                                 "stream/" +
                                 "".join(episode["streams"][0]) +
                                 "/public")
            return r.json()["response"]["classic"]

    def video(self, servers, server="fembed"):
        if isinstance(servers, str):
            servers = {"servers": {server: servers}}
        if server == "fembed":
            r = requests.get("https://fembed.com/f/" + servers["servers"][server])
            fbed_url = r.url
            donmain = self.clean_id(fbed_url, 2)
            try:
                f = requests.post(f"https://{donmain}/api/source/{servers['servers'][server]}").json()
            except json.decoder.JSONDecodeError:
                c = cloudscraper.create_scraper()
                f = c.post(f"https://{donmain}/api/source/{servers['servers'][server]}").json()
            return f
        elif server == "amz":
            r = requests.get(f"https://www.amazon.com/drive/v1/shares/{servers['servers'][server]}?"
                             f"shareId={servers['servers'][server]}&resourceVersion=V2&ContentType=JSON")
            return


def fembed(server, quality=None):
    file = None
    files = server["data"]
    if quality:
        quality = f"{quality}p"
        for i in files:
            qual = i["label"]
            if qual == quality:
                file = i["file"]
                break
            else:
                file = i["file"]
    else:
        file = []
        for i in files:
            file.append({"file": i["file"],
                         "quality": i["label"]})

    return file


def amz(server):
    return server["data"][0]["tempLink"]


def arm_link(dic, typ=0):
    if typ == 0:
        return f'https://animeflash.xyz/anime/{dic["id"]}/{dic["slug"]}'
    elif typ == 1:
        return f'https://blob.animeflash.xyz/media/{dic["banner_id"]}/medium.jpg'
    elif typ == 2:
        return f'https://blob.animeflash.xyz/media/{dic["wallpaper_id"]}/medium.jpg'
    elif typ == 3:
        return f'https://animeflash.xyz/ver/{dic["id"]}/{dic["slug"]}'
    else:
        return None


def chapters(dic, text="El siguiente capítulo estara disponible en"):
    TIME_SHEMA = "%I horas, %M minutos, %S segundos."
    TIME_SHEMA1 = "%H:%M:%S"
    # DAY_SHEMA = "%I:%M:%S %d/%m/%y"
    DAY_SHEMA = "%Y-%m-%d %H:%M:%S"
    if dic["simulcast"]:
        s = datetime.strptime(dic["simulcasts"], DAY_SHEMA) - datetime.now()
        if s.days > 1:
            d = "días"
        else:
            d = "día"
        return f' {text} {s.days} {d}, ' \
               f'{datetime.strptime(str(timedelta(seconds=s.seconds)), TIME_SHEMA1).strftime(TIME_SHEMA)}'
    else:
        return ""


def date(dic):
    DAY_SHEMA = "%Y-%m-%d"
    DAY_SHEMa = "%d/%m/%Y"
    s = datetime.strptime(dic["premiere"], DAY_SHEMA)
    return s.strftime(DAY_SHEMa)


def description(dic):
    return str(dic["summary"])


def genres(dic):
    gens = dic["genres"]
    li = []
    for i in gens:
        r = requests.get(f"https://api.animeflash.xyz/v1/anime/genre/{i}")
        li.append(r.json()["response"]["name"])
    return li


tag = lambda x: f'<a href="{x}">&#8205;</a>'
order = lambda some_list, x: [some_list[i:i + x] for i in range(0, len(some_list), x)]

