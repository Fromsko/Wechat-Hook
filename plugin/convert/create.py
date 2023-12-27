"""
    @Author: skong
    @File  : create
    @GitHub: https://github.com/Fromsko
    @notes : 生成
"""

import time
from base64 import b64encode
from pathlib import Path
from .text_to_image import text_to_img


CACHEPATH = Path.cwd().joinpath("cache")
if not CACHEPATH.exists():
    CACHEPATH.mkdir()


def create_img(message: str):
    """
    生成图片
        - `message`: 信息
    """
    # 唯一id

    filename = CACHEPATH.joinpath(f"{time.time()}.png")

    base_text = "[小安] Say:\n"
    img = text_to_img(
        base_text + message
    )

    img.save(filename)

    return filename


def image_to_base64(pathload):
    """ 图片转字节码 """
    with open(pathload, mode="rb+") as img_obj:
        content: bytes = img_obj.read()
    return b64encode(content)
