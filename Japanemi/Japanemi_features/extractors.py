import os
import re
import sys
import wget
import logging
import requests
import youtube_dl
import cloudscraper
import urllib.parse
from PIL import Image
from bs4 import BeautifulSoup
from .utils import generate_screen_shots


# DEBUG
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


async def file_recognize(filename, out="./"):
    file_type = "document"
    images = ["jpg", "png", "webp"]
    videos = ["mp4", "mkv", "webm"]
    songs = ["mp3", "FLAC", "m4a"]
    documents = ["zip", "rar", "apk"]
    direcs = {
        "photo": images,
        "video": videos,
        "audio": songs,
        "document": documents}
    try:
        ext = filename.split(".")[-1]
        print(ext)
        for i in direcs:
            if ext in direcs[i]:
                file_type = i
                break
    except Exception as e:
        print(e)
        file_type = None
        ext = None
    return {
        "file": filename,
        "type": file_type,
        "ext": ext}


def links_filters(function):
    def wrapper(*args, **kwargs):
        host = args[0].split("/")[2]
        if re.match("www.mediafire.com", host):
            r = requests.get(args[0])
            soup = BeautifulSoup(r.content, 'html.parser')
            dwnld = soup.find(id='downloadButton')
            args = (dwnld.get('href'),)
        elif re.match("www\d*.zippyshare.com", host):
            u = None
            r = requests.get(args[0])
            soup = BeautifulSoup(r.content, "html.parser")
            for i in soup.find_all("script", attrs={"type": "text/javascript"}):
                sm = i.string
                if sm:
                    m = re.findall('"/d/.*"', sm)
                    if m:
                        u = eval(m[0].replace("+ (", "+ str( "))
                        break
            protocol = args[0].split(".")[0]
            if u:
                args = (protocol + ".zippyshare.com" + u,)
        elif re.match("(embedsito|diasfem|fembed|femax20).com", host):
            c = cloudscraper.create_scraper()
            r = c.post("https://diasfem.com/api/source/" + args[0].split("/")[-1])
            args = (r.json()["data"][-1]["file"],)
        return function(*args, **kwargs)
    return wrapper


def extractor_base(function):
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    return wrapper


@links_filters
@extractor_base
async def generic_extractor(url, out="./", custom=None, ext=None):
    if out[-1] != "/":
        out = out + "/"
    video_info = youtube_dl.YoutubeDL().extract_info(url, download=False)
    # Thumbnail?
    print(video_info)
    try:
        try:
            thumbnail = video_info["thumbnail"]
        except KeyError:
            thumbnail = video_info["entries"][0]["thumbnail"]
        data = wget.download(thumbnail, out)
        if data[-4:] == "webp":
            image = Image.open(data).convert("RGB")
            image.save(out + "thumb.jpg", "jpeg")
            os.unlink(data)
        elif data[-4:] == ".jpg":
            os.rename(data, out + "thumb.jpg")
        else:
            os.rename(data, out + "thumb.jpg")
    except Exception as e:
        print(e)
    # Demás datos, title, ext
    _title = custom or re.sub("/", "", video_info["title"])
    try:
        _ext = video_info["ext"]
    except KeyError:
        _ext = video_info["entries"][0]["formats"][0]["ext"]
    if _ext == "unknown_video":
        _ext = ext or "mp4"
    # Options + Download
    options = {"format": "bestaudio+bestvideo/best",
               "outtmpl": out + _title + "." + _ext}
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([url])
    # Filename
    out_ = out + _title + "." + _ext
    file_type = await file_recognize(out_, out)
    # Si es video trata de obtener capturas
    if file_type["type"] == "video":
        await generate_screen_shots(out_, out, 300, 1)
        yes_thumb = True
    else:
        yes_thumb = False
    return {"file": out_,
            "type": file_type["type"],
            "thumb": yes_thumb}
