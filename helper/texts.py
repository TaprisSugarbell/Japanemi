import re


async def capupload_text(title):
    titl = re.sub(r"[^a-zA-Z0-9_ ]", "", title)
    cap = "".join(titl.split(" ")[-1])
    twc = "_".join(titl.split(" ")[:-1])
    twg = " ".join(title.split(" ")[:-1])
    caption =\
        f"#{twc}\n" \
        f"💮 {twg}\n" \
        f"🗂 Capítulo {cap}"
    return caption
