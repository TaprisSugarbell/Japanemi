import re
import anilist
from google_trans_new import google_translator


async def capupload_text(title):
    titl = re.sub(r"[^a-zA-Z0-9_ ]", "", title)
    cap = "".join(titl.split(" ")[-1])
    twc = "_".join(titl.split(" ")[:-1])
    twg = " ".join(title.split(" ")[:-1])
    caption = \
        f"#{twc}\n" \
        f"💮 {twg}\n" \
        f"🗂 Capítulo {cap}"
    return caption


async def ani_desc(anime_id, mode=1):
    a = anilist.Client()
    info = a.get_anime(anime_id)
    tr = google_translator()
    title = ""
    descript = ""
    type_ = ""
    genres = ""
    stud = ""
    tags = ""
    try:
        title = f"**{info.title.romaji}**\n({info.title.native})\n"
    except Exception as e:
        print(e)
        title = f"**{info.title.romaji}**\n"
    try:
        try:
            descript = f"{tr.translate(info.description_short, lang_tgt='es')}...\n"
        except Exception as e:
            print(e)
            descript = f"{tr.translate(info.description, lang_tgt='es')}"
    except Exception as e:
        print(e)
    try:
        type_ = f"**Tipo:** {info.format}\n" \
                f"**Estado:** {tr.translate(info.status, lang_tgt='es')[0]}\n"
    except Exception as e:
        print(e)
    try:
        genres = f"**Géneros:** {tr.translate(', '.join(info.genres), lang_tgt='es')}\n"
    except Exception as e:
        print(e)
    try:
        tags = f"**Tags:** {tr.translate(', '.join(info.tags))}\n"
    except Exception as e:
        print(e)
    try:
        stud = f"**Estudios:** {', '.join(info.studios)}"
    except Exception as e:
        print(e)
    img = f"<a href='https://img.anili.st/media/{info.id}'>&#8205;</a>"
    DESCRIPTION = title + descript + type_ + genres + tags + stud + img
    DESCRIPTION_ = title + type_ + genres + tags + stud + img

    if mode == 1:
        return DESCRIPTION
    elif mode == 2:
        return DESCRIPTION_
