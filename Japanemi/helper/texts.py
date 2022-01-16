import re
import anilist
from markdownify import markdownify as md
from google_trans_new import google_translator


async def capupload_text(title):
    titl = re.sub(r"[^a-zA-Z0-9_ .-]", "", title).strip()
    cap = "".join(titl.split(" ")[-1])
    twc = "_".join(titl.strip().split(" ")[:-1]).replace(".", "").replace("-", "_")
    try:
        if twc[-1] == "_":
            twc = twc[:-1]
    except Exception as e:
        print(e)
    try:
        etto = title.split("_")
        if len(etto) > 3:
            twg = " ".join(etto[:-1])
            cap = " ".join(etto[-1])
        else:
            twg = " ".join(title.split(" ")[:-1])
    except Exception as e:
        print(e)
        twg = " ".join(title.split(" ")[:-1])
    try:
        cap = int(cap)
    except ValueError:
        _ec = re.findall(r"\d+\.?\d*", title)
        if len(_ec) > 0:
            cap = _ec[-1]
        else:
            cap = 1
        twc = "_".join(titl.replace(" " + cap, "").split()).replace(".", "").replace("-", "_")
        twg = titl.replace(" " + cap, "")
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
    episodes = f"**Episodios:** **~?**\n"
    ini = ""
    genres = ""
    tags = ""
    hashtag = ""
    stud = ""
    find = ""
    try:
        title = f"**{info.title.romaji}**\n(**{info.title.native}**)\n"
    except Exception as e:
        print(e)
        title = f"**{info.title.romaji}**\n"
    try:
        try:
            tf = f"{tr.translate(info.description_short, lang_tgt='es').strip()}"
            if tf[-1] == ".":
                tf = f"{tf[:-1]}..."
            elif tf != ".":
                tf = f"{tf}..."
            tr_ = md(tf, strip=['br']).replace('*', '__').replace("____", "**")
        except Exception as e:
            print(e)
            tf = f"{tr.translate(info.description, lang_tgt='es').strip()}"
            if tf[-2:] == " .":
                tf = f"{tf[-2:]}."
            tr_ = md(tf, strip=['br']).replace('*', '__').replace("____", "**")
        mm = f"**Descripción:** {' '.join(tr_.split())}"
        descript = re.sub(r"\(Fuente: [\s\S]{0,1000}\)", "", mm)
        print(descript)
    except Exception as e:
        print(e)
    try:
        state = info.status
        if state == "RELEASING":
            state = "Emisión"
        elif state == "FINISHED":
            state = "Finalizado"
        elif state == "NOT_YET_RELEASED":
            state = "Aún no emitido"
        elif state == "CANCELLED":
            state = "Cancelado"
        type_ = f"**Tipo:** {info.format}\n" \
                f"**Estado:** {state}\n"
        try:
            episodes = f"**Episodios:** {info.episodes}\n"
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
    try:
        try:
            fecha = info.start_date
            arm = f'**{fecha.day}/{fecha.month}/{fecha.year}**'
            fecha_ = info.end_date
            arm_ = f'**{fecha_.day}/{fecha_.month}/{fecha_.year}**'
        except Exception as e:
            print(e)
            try:
                fecha = info.start_date
                arm = f'**{fecha.day}/{fecha.month}/{fecha.year}**'
            except Exception as e:
                print(e)
                fecha = info.start_date
                try:
                    arm = f"**~/~/{fecha.year}?**"
                except Exception as e:
                    print(e)
                    arm = "**~/~/~?**"
            arm_ = "**~/~/~?**"
        ini = f"**Emsión:** __De__ {arm} __hasta__ {arm_}\n"
        exg = [f'#{"_".join(re.sub(r"[^a-zA-Z0-9_ ]","", info.genres[i]).strip().split(" "))}'
              for i in range(len(info.genres))]
        arm_g = ', '.join(exg)
        genres = f"**Géneros:** {arm_g}.\n"
    except Exception as e:
        print(e)
    try:
        ob = [f'#{"_".join(re.sub(r"[^a-zA-Z0-9_ ]","", info.tags[i]).strip().split(" "))}'
              for i in range(len(info.tags))]
        arm_t = ', '.join(ob)
        tags = f"**Tags:** {arm_t}.\n"
    except Exception as e:
        print(e)
    try:
        exs = [f'#{"_".join(re.sub(r"[^a-zA-Z0-9_ ]", "", info.studios[i]).strip().split(" "))}'
               for i in range(len(info.studios))]
        arm_s = ', '.join(exs)
        stud = f"**Estudios:** {arm_s}.\n"
    except Exception as e:
        print(e)
    try:
        hashtag = info.hashtag
    except Exception as e:
        print(e)
    try:
        find_ = "_".join(re.sub(r"[^a-zA-Z0-9_ ]", "", info.title.romaji).strip().split(" "))
        find = f"**Find:** #{find_} {hashtag}".strip()
    except Exception as e:
        print(e)
    img = f"<a href='https://img.anili.st/media/{info.id}'>&#8205;</a>"
    DESCRIPTION = title + type_ + episodes + ini + genres + tags + stud +\
                  find + "\n" + descript + img
    DESCRIPTION_ = title + type_ + episodes + ini + genres + tags + stud + find + img

    if mode == 1:
        return DESCRIPTION
    elif mode == 2:
        return DESCRIPTION_
