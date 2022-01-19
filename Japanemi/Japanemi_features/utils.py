import os
import random
import string
from PIL import Image
from moviepy.editor import VideoFileClip


def generate_screenshot(file, name: str = "./thumb.jpg"):
    clip = VideoFileClip(file)
    ss_img = int(clip.duration / random.randint(15, 30))
    frame = clip.get_frame(ss_img)
    nimage = Image.fromarray(frame)
    nimage.save(name)
    return name


def rankey(length: int = 5, _key=string.hexdigits):
    return "".join([random.choice(_key) for _ in range(length)])


def create_folder(user_id, temp_folder: str = rankey()):
    tmp_directory = "./Downloads/" + str(user_id) + "/" + temp_folder + "/"
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    return tmp_directory


class Utils:
    def __init__(self):
        pass



