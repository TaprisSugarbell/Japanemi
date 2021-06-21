import requests
from bs4 import BeautifulSoup


async def episodes():
    r = requests.get(f"https://tioanime.com/")
    soup = BeautifulSoup(r.content, "html.parser")
    article = soup.find_all(attrs={"class": "episode"})
    info = {}
    animes = []
    portadas = []
    titles = []
    for i in article:
        animes.append(f'https://tioanime.com{i.find("a").get("href")}')
        portadas.append(f'https://tioanime.com{i.find("img").get("src")}')
        titles.append(i.find("h3").text)
    info["episodes"] = animes
    info["portadas"] = portadas
    info["titles"] = titles
    return info
