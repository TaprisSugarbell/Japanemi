import requests
from .. import sayulog
from ..AnimeFlash import AnimeFlash, amz


def servers(s, episode=None):
    servers_dict = s["servers"]
    servers_keys = servers_dict.keys()
    arm_links = []
    a = AnimeFlash()
    if "mediafire" in servers_keys:
        arm_links.append(f'https://www.mediafire.com/file/{servers_dict["mediafire"]}')
    if "zippyshare" in servers_keys:
        arm_links.append(f'{servers_dict["zippyshare"]}/file.html')
    if "plus" in servers_keys:
        arm_links.append(f'{servers_dict["plus"]}.mp4')
    if "amz" in servers_keys:
        # arm_links.append(amz(a.video(servers_dict["amz"], server="amz")))
        try:
            if episode:
                arm_links.append(("Amazon", f'amz_{episode}_{servers_dict["amz"]}'))
            else:
                r = requests.get(f'https://www.amazon.com/drive/v1/shares/{servers_dict["amz"]}?'
                                 f'shareId={servers_dict["amz"]}&resourceVersion=V2&ContentType=JSON')
                am = requests.get(
                    f'https://www.amazon.com/drive/v1/nodes/{r.json()["nodeInfo"]["id"]}/children?'
                    f'asset=ALL&limit=1&searchOnFamily=false&tempLink=true&'
                    f'shareId={servers_dict["amz"]}&offset=0&resourceVersion=V2&ContentType=JSON').json()
                arm_links.append(amz(am))
        except Exception as e:
            sayulog.error("Amazon error.", exc_info=e)
    if "fembed" in servers_keys:
        if episode:
            arm_links.append(("Fembed", f'fmb_{episode}_{servers_dict["fembed"]}'))
        else:
            arm_links.append("https://fembed.com/f/" + servers_dict["fembed"])
    if "mega" in servers_keys:
        arm_links.append(f'https://mega.nz/file/{servers_dict["mega"]}')
    if "nyaa" in servers_keys:
        arm_links.append(f'https://content.jwplatform.com/videos/{servers_dict["nyaa"]}.mp4')
    return arm_links
