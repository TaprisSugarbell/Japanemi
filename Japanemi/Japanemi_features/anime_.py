import re
import json
import base64
import requests
import urllib.request
from bs4 import BeautifulSoup
from .extractors import generic_extractor
from urllib.parse import quote_plus, unquote


def filter_videos(sc):
    mtch = re.findall(r"var videos = .*?{?.*\[.*;?", sc)
    rslt = json.loads(mtch[0].replace("var videos = ", "").replace(";", "").strip())
    if isinstance(rslt, dict):
        return [i["code"] for i in rslt["SUB"]]
    else:
        return [re.findall(r"https?://.*", i[1])[0] for i in rslt]


class Downcap:
    def __init__(self, url):
        self.url = url

    def anime_site(self):
        return urllib.request.Request(self.url).host

    def site_filter(self):
        site_ = self.anime_site()
        if site_ == "monoschinos2.com":
            site = "mc"
        elif site_ == "tioanime.com":
            site = "ta"
        elif site_ == "www.animefenix.com":
            site = "af"
        elif site_ == "hentaila.com":
            site = "hla"
        else:
            site = False
        return site

    def mc_scraping(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        player = soup.find_all("li", attrs={"id": "play-video"})
        downlinks = soup.find("div", attrs={"class": "downbtns"}).find_all("a")
        list_redis = []
        for i in range(len(player)):
            redis_ = base64.b64decode(player[i].find("a").get("data-player"))
            list_redis.append(redis_.decode("utf-8").split("url=")[-1])
        for i in downlinks:
            if urllib.request.Request(i).host == "monoschinos2.com":
                continue
            else:
                list_redis.append(i.get("href"))

        return list_redis

    def af_scraping(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        player = soup.find_all(attrs={"class": "player-container"})
        links_ = player[0].find("script")
        ptrn = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(ptrn, str(links_))
        list_urls = []
        for i in urls:
            list_urls.append(i.replace("'", ""))
        return list_urls

    def ta_scraping(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        script = soup.find_all("script")[-3]
        lnk = filter_videos(script.string)
        for script in soup.find_all(attrs={"class": "btn btn-success btn-download btn-sm rounded-pill"}):
            url = script['href']
            lnk.append(url)
        return lnk

    def hla_scraping(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        script = soup.find_all("script")[-6]
        lnk = filter_videos(script.string)
        for script in soup.find_all(attrs={"class": "btn sm rnd"}):
            url = script['href']
            lnk.append(url)
        return lnk

    def get_url(self):
        site = self.site_filter()
        if site == "ta":
            lnk = self.ta_scraping()
        elif site == "mc":
            lnk = self.mc_scraping()
        elif site == "af":
            lnk = self.af_scraping()
        elif site == "hla":
            lnk = self.hla_scraping()
        else:
            lnk = None
        return lnk


class InfoAnime:
    def __init__(self, query, site):
        self.query = query
        self.site = site

    def anime_site(self):
        return urllib.request.Request(self.url).host

    def site_filter(self):
        site_ = self.anime_site()
        if site_ == "monoschinos2.com":
            site = "mc"
        elif site_ == "tioanime.com":
            site = "ta"
        elif site_ == "www.animefenix.com":
            site = "af"
        else:
            site = False
        return site

    def info_ta(self):
        query = quote_plus(self.query)
        r = requests.get(f"https://tioanime.com/directorio?q={query}")
        soup = BeautifulSoup(r.content, "html.parser")
        article = soup.find_all(attrs={"class": "anime"})
        info = {}
        animes = []
        portadas = []
        titles = []
        for i in article:
            animes.append(f'https://tioanime.com{i.find("a").get("href")}')
            portadas.append(f'https://tioanime.com{i.find("img").get("src")}')
            titles.append(i.find("h3").text)
        info["animes"] = animes
        info["portadas"] = portadas
        info["titles"] = titles
        return info

    def info_mc(self):
        query = quote_plus(self.query)
        r = requests.get(f"https://monoschinos2.com/search?q={query}")
        soup = BeautifulSoup(r.content, "html.parser")
        section = soup.find_all(attrs={"class": "link-anime"})
        info = {}
        titles = []
        portadas = []
        animes = []
        for i in section:
            titles.append(i.find("h3").text)
            portadas.append(i.find("img").get("src"))
            animes.append(i.get("href"))
        info["titles"] = titles
        info["portadas"] = portadas
        info["animes"] = animes
        return info

    def info_af(self):
        query = quote_plus(self.query)
        r = requests.get(f"https://www.animefenix.com/animes?q={query}")
        soup = BeautifulSoup(r.content, "html.parser")
        article = soup.find_all(attrs={"class": "serie-card"})
        info = {}
        animes = []
        portadas = []
        titles = []
        for i in article:
            titles.append(i.find("h3").text)
            portadas.append(i.find("img").get("src"))
            animes.append((i.find("a").get("href")))
        info["animes"] = animes
        info["portadas"] = portadas
        info["titles"] = titles
        return info

    def fetch_ta(self, no_anime=0):
        info = self.info_ta()
        # info = InfoAnime(self.query, "ta").info_ta()
        anime = str(info["animes"][no_anime])
        sup = BeautifulSoup(requests.get(anime).content, "html.parser")
        ss = sup.find_all("script")[-2]
        ai = ss.contents[0].strip().split("'")[1].split("/")[-1]
        ani = anime.split("/")
        tasks = [f"https://tioanime.com/ver/{ani[-1]}-{i}" for i in range(61)]
        dic_info = {}
        resp = []
        for i in range(len(tasks)):
            response = requests.get(tasks[i]).ok
            if response:
                resp.append(tasks[i])
            elif not response and i > 0:
                break
        dic_info["anime_id"] = ai
        dic_info["ok"] = resp
        return dic_info

    def fetch_mc(self, no_anime=0):
        info = self.info_mc()
        anime = str(info["animes"][no_anime])
        ani = anime.split("/")
        tasks = [f"https://monoschinos2.com/ver/{ani[-1].replace('-sub-espanol', '-episodio')}-{i}" for i in range(61)]
        resp = []
        for i in range(len(tasks)):
            response = requests.get(tasks[i]).ok
            if response:
                resp.append(tasks[i])
            elif not response and i > 0:
                break
        return resp

    def fetch_af(self, no_anime=0):
        info = self.info_af()
        anime = str(info["animes"][no_anime])
        ani = anime.split("/")
        tasks = [f"https://www.animefenix.com/ver/{ani[-1]}-{i}" for i in range(61)]
        resp = []
        for i in range(len(tasks)):
            response = requests.get(tasks[i]).ok
            if response:
                resp.append(tasks[i])
            elif not response and i > 0:
                break
        return resp

    def info(self):
        if self.site == "ta":
            info_ = self.info_ta()
        elif self.site == "mc":
            info_ = self.info_mc()
        elif self.site == "af":
            info_ = self.info_af()
        return info_

    def fetch(self, no_anime=0):
        if self.site == "ta":
            fetch_ = self.fetch_ta(no_anime)
        elif self.site == "mc":
            fetch_ = self.fetch_mc(no_anime)
        elif self.site == "af":
            fetch_ = self.fetch_af(no_anime)
        return fetch_


async def foriter(links=None, out="./", custom=""):
    if links is None:
        links = []
    out_ = ""
    for url in links:
        try:
            if re.match(r"https?://mega.nz", url):
                pass
            else:
                out_ = await generic_extractor(url, out=out, custom=custom)
                out_ = out_["file"]
                break
        except Exception as e:
            print(e)
            out_ = None
    return out_

