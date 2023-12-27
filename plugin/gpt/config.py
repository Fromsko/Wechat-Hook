"""
    配置文件
"""
import json
from pathlib import Path
from libs.log import logger as log


class ChatConfig:
    NAME = "ChatGPT"

    def __init__(
            self,
            configPath: str = "config.json",
            promptPath: str = "prompt.key",
            historyPath: str = "history.json",
    ):
        self.CONFIG_FILE_PATH = configPath
        self.PROMPT_FILE_PATH = promptPath
        self.HISTORY_FILE_PATH = historyPath
        self.CONFIG = None
        self.prompt = "You're a smart robot."
        self.history = None

    def load_config(self):
        if not Path(self.CONFIG_FILE_PATH).exists():
            self.create_config_file()
            exit()

        with open(self.CONFIG_FILE_PATH, "r") as config_file:
            self.CONFIG = json.load(config_file)

    def load_prompt(self):
        if Path(self.PROMPT_FILE_PATH).exists():
            with open(self.PROMPT_FILE_PATH, "r") as prompt_file:
                self.prompt = prompt_file.read()

    def load_history(self):
        if Path(self.HISTORY_FILE_PATH).exists():
            with open("history.json", "r") as history_file:
                self.history = json.load(history_file)
        else:
            log.error("History file not found")

    def save_history(self, msgDict: dict):
        if Path(self.HISTORY_FILE_PATH).exists():
            with open("history.json", "r") as history_file:
                history_file.write(json.dumps(msgDict, ensure_ascii=False))
        else:
            log.error("History file write failed!")

    def create_config_file(self):
        config = {
            "api_key": input("API Key: "),
            "api_base": input("API Base: "),
            "proxy": input("NetWork Proxy: "),
            "async_openai": False,
            "img": {
                "font_size": 30,
                "width": 700,
                "font_path": "C:\Windows\Fonts\consola.ttf",
                "offset_x": 50,
                "offset_y": 50
            }
        }

        with open(self.CONFIG_FILE_PATH, "w") as config_file:
            json.dump(config, config_file, indent=4)

        log.info(
            "The configuration file has been created,"
            " please re-run the program."
        )

    def start(self, config: dict = None):
        if config is None:
            self.load_config()
        else:
            self.CONFIG = config
        self.load_prompt()
        log.info(f'{self.NAME} is Running!')
