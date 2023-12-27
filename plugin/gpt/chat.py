# -*- encoding: utf-8 -*-
# @File     : main
# @Time     : 2023-12-27 00:04:23
# @Docs     : LLM
import json
import requests

from plugin.gpt.config import ChatConfig


class GPT(ChatConfig):
    def __init__(self, config=None):
        super(GPT, self).__init__()
        self.start(config)

    def _fetch(self, payload):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.CONFIG["api_key"]}',
        }
        resp = requests.post(
            f'{self.CONFIG["api_base"]}/chat/completions',
            headers=headers,
            data=payload,
        )
        resp.raise_for_status()
        return resp.json()

    def send_to_chatgpt(self, msg: str) -> str:
        """ 发送信息 """
        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": msg
                }
            ]
        })
        resp = self._fetch(payload)
        return resp['choices'][0]['message']['content']

    def sendImg(self, message, imgPath=None):
        """ 发送图片信息 """
        pass


if __name__ == "__main__":
    print(GPT().send_to_chatgpt("你好"))
