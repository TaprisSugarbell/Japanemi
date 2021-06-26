import wget
import requests
import youtube_dl
from PIL import Image
from bs4 import BeautifulSoup
from Japanemi_features.utils import *


async def file_recognize(filename, out="./"):
    images = ["jpg", "png", "webp"]
    videos = ["mp4", "mkv", "webm"]
    songs = ["mp3", "FLAC", "m4a"]
    documents = ["zip", "rar", "apk"]
    direcs = {
        "image": images,
        "video": videos,
        "song": songs,
        "document": documents}
    try:
        ext = filename.split(".")[-1]
        print(ext)
        if ext in direcs["image"]:
            file_type = "image"
        elif ext in direcs["video"]:
            file_type = "video"
        elif ext in direcs["song"]:
            file_type = "song"
        else:
            file_type = "document"
    except:
        file_type = None
        ext = None
    return {
        "file": filename,
        "type": file_type,
        "ext": ext}


async def generic_extractor(url, out="./", custom=""):
    video_info = youtube_dl.YoutubeDL().extract_info(url, download=False)
    videos = ["mp4", "mkv", "webm"]
    # Demás datos, title, ext
    if len(custom) > 0:
        _title = custom
    else:
        _title = video_info["title"]
    try:
        _ext = video_info["ext"]
    except KeyError:
        _ext = video_info["entries"][0]["formats"][0]["ext"]
    if _ext == "unknown_video":
        _ext = "mp4"
    if _title.split(".")[-1] in videos:
        _title = _title.split(".")[0]
    # Options + Download
    options = {"format": "bestaudio+bestvideo/best",
               "outtmpl": out + _title + "." + _ext}
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([url])
    # Filename
    out_ = out + _title + "." + _ext
    # Obtiene el tipo de archivo
    file_data = await file_recognize(out_, out)
    file_type = file_data["type"]
    # Si es video trata de obtener capturas
    if file_type == "video":
        await generate_screen_shots(out_, out, 300, 1)
        yes_thumb = True
    else:
        yes_thumb = False
    return {"file": out_,
            "thumb": yes_thumb}


async def mediafire(url, out, custom=""):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    dwnld = soup.find(id='downloadButton')
    w = dwnld.get('href')
    # if len(custom) > 0:
    #     custom = "/" + custom
    wget.download(w, out)
    # Esto revisa los archivos
    file_direct = os.listdir(out)
    print(file_direct)
    filename = out + file_direct[0]
    # Obtiene el tipo de archivo
    file_data = await file_recognize(filename, out)
    file_type = file_data["type"]
    # Si es video trata de obtener capturas
    if file_type == "video":
        await generate_screen_shots(filename, out, 300, 1)
        yes_thumb = True
    else:
        yes_thumb = False
    return {"file": filename,
            "type": file_data["type"],
            "ext": file_data["ext"],
            "thumb": yes_thumb}


async def zippyshare(url, out="./", custom=""):
    # Extracción de datos para generar el link
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    div = soup.find_all(attrs={"class": "right"})
    separate_filter = ""
    for i in div:
        a = i.find("script")
        if a is not None:
            filter_eq = str(a).split("href =")[1].split(";")[0]
            separate_filter = filter_eq.split("+")
    nums_ = " ".join(separate_filter[1:3]).split("%")
    try:
        separate_nums = nums_[1].strip().split(" ")
    except IndexError:
        etto = soup.find_all("script")
        a = etto[-7]
        filter_eq = str(a).split("href =")[1].split(";")[0]
        separate_filter = filter_eq.split("+")
        nums_ = " ".join(separate_filter[1:3]).split("%")
        separate_nums = nums_[1].strip().split(" ")
    num_1 = int(separate_nums[3])
    num_2 = int(separate_nums[0])
    formuled = num_1 % num_2 + num_1 % 913
    protocol_ = url.split(".")[0]
    fname = separate_filter[-1].replace('"', "").replace("/", "").strip()
    # Link generado
    _link = f"{protocol_}.zippyshare.com/d/" \
            f"{separate_filter[0].split('/')[2]}/{formuled}/{fname}"
    options = {"format": "best/bestaudio+bestvideo",
               "outtmpl": out + fname}
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([_link])
    # Esto revisa los archivos
    file_direct = os.listdir(out)
    filename = out + file_direct[0]
    # Obtiene el tipo de archivo
    file_data = await file_recognize(filename, out)
    file_type = file_data["type"]
    # Si es video trata de obtener capturas
    if file_type == "video":
        await generate_screen_shots(filename, out, 300, 1)
        yes_thumb = True
    else:
        yes_thumb = False
    return {"file": filename,
            "type": file_data["type"],
            "ext": file_data["ext"],
            "thumb": yes_thumb}
