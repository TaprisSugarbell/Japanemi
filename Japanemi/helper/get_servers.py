import re
from bs4 import BeautifulSoup
from cloudscraper import create_scraper


requests = create_scraper()


async def get_ao_servers(url, lngj=None):
    lenks = []
    parser = "html.parser"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, parser)
    player_options = soup.find("ul", attrs={"id": "playeroptionsul"}).find_all("li")
    print(player_options)
    options = len(player_options)
    if options > 1:
        pass
    else:
        post_options = soup.find("li", attrs={"id": "player-option-1"})
        post_id = post_options.get("data-post")
        post_type = post_options.get("data-type")
        post_source = post_options.get("data-nume")
        r1 = requests.get(
            "https://www1.animeonline.ninja/wp-json/dooplayer/v1/post/" + post_id,
            params={
                "type": post_type,
                "source": post_source
            }
        ).json()

        r2 = requests.get(r1["embed_url"])

        OptionsLangDisp = BeautifulSoup(r2.content, "html.parser").find("div", attrs={"class": "OptionsLangDisp"})
        # print(OptionsLangDisp)
        audjp = OptionsLangDisp.find("div", attrs={"class": "ODDIV"}).find_all("li")
        audlat = OptionsLangDisp.find("div", attrs={"class": "OD_LAT"})
        audes = OptionsLangDisp.find("div", attrs={"class": "OD_ES"})
        if audlat:
            audlat = audlat.find_all("li")
        if audes:
            audes = audes.find_all("li")
        servers = {
            "JP": audjp,
            "LAT": audlat,
            "ES": audes
        }
        if audlat is None and audes is None:
            for i in audjp:
                lenk = i.get("onclick")
                lenks.append(re.findall(r"https?://[\w./-]*", lenk)[0])
            return lenks
        elif lngj:
            server = servers[lngj]
            for i in server:
                lenk = i.get("onclick")
                lenks.append(re.findall(r"https?://[\w./-]*", lenk)[0])
            return lenks
        else:
            return servers



