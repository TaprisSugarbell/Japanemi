import re


async def capupload_text(title):
    title = re.sub(r"[^a-zA-Z0-9_ ]", "", title)
    cap = "".join(title.split(" ")[-1])
    twc = "_".join(title.split(" ")[:-1])
    twg = " ".join(title.split(" ")[:-1])
    caption =\
        f"#{twc}_{cap}\n" \
        f"💮*Anime: {twg}*\n" \
        f"🗂*Capítulo {cap}*"
    return caption
