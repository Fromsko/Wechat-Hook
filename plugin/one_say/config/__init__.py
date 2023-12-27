# -*- encoding: utf-8 -*-
import json
import random
from pathlib import Path
from typing import Optional

from loguru import logger as log


def file_load(filename: Optional[str] = None,
              splicing_load: Optional[str] = None,
              splicing_check=False) -> dict or None:
    """
    文件导入
    :param filename: 文件名[categories / version]
    :param splicing_load: 拼接路径
    :param splicing_check: 是否拼接
    :return: 文件内容(json|dict)
    """
    try:
        base_file = Path(__file__).parents[1] / "res"
        if filename is not None:
            filename = base_file.joinpath(filename)

        if splicing_check and splicing_load is not None:
            filename = base_file.joinpath(splicing_load)

        if filename.suffix == "":
            filename = f"{filename}.json"

        with open(filename, 'r', encoding="utf-8") as file_obj:
            json_file: dict = json.loads(file_obj.read())

    except FileNotFoundError as err:
        log.info(f"err {err}")
        return None
    else:
        return json_file


def _base_check():
    """ 基础分类 """
    info: dict = {}
    base_load: str = file_load('version')["categories"]["path"]

    # 基础路径
    contents: dict = file_load(
        splicing_load=base_load,
        splicing_check=True
    )

    # 构造分类器
    for content in contents:
        info.update({
            content['id']: {
                'name': content['name'],
                'path': content['path']
            }
        })

    return info


def random_choice():
    """ 分类后导入 """
    info: dict = _base_check()

    # 随机提取 分类
    choice_name, choice_path = random.choices(
        list(info.values()), k=1
    )[0].values()

    # 分类后文件导入
    choice_content = file_load(
        splicing_load=choice_path,
        splicing_check=True
    )

    # 分类后文件 随机提取
    content = random.choices(choice_content, k=1)[0]
    return choice_name, content
