"""
    消息事件模型
"""
import json
import queue
import threading
from enum import Enum
from typing import Callable, Optional, Union, Tuple, Dict
from pydantic import BaseModel

from libs.bot.error import ParameterError
from libs.log import logger as log
from plugin.gpt.chat import GPT


class MessageType(Enum):
    """
    消息类型枚举。

    枚举值:
    - `TEXT`: 文本消息
    - `IMAGE`: 图片消息
    - `XML`: XML卡片消息
    - `NOTIFY`: 事件通知消息
    - `LOCAL`: 位置信息
    - `CUSTOM_TYPE`: 自定义消息
    """
    TEXT = 1
    IMAGE = 3
    XML = 49
    NOTIFY = 1000
    LOCAL = 48
    CUSTOM_TYPE = 200  # 自定义的消息类型


class Message(BaseModel):
    """
    消息模型。

    属性:
    - `localid`: 本地ID
    - `msgid`: 消息ID
    - `msg_type`: 消息类型
    - `is_self_msg`: 是否自己发送的消息
    - `timestamp`: 时间戳
    - `sender`: 发送者
    - `content`: 消息内容
    - `room_sender`: 房间发送者
    - `sign`: 签名
    - `thumb_path`: 缩略图路径，可以是字符串或者 None
    - `file_path`: 文件路径，可以是字符串或者 None
    """
    localid: Optional[int]
    msgid: Optional[int]
    msg_type: Optional[int]
    is_self_msg: Optional[int]
    timestamp: Optional[int]
    sender: Optional[str]
    content: Optional[str]
    room_sender: Optional[str]
    sign: Optional[str]
    thumb_path: Optional[Union[str, None]]
    file_path: Optional[Union[str, None]]


class Event(BaseModel):
    Msg: Message
    MsgType: MessageType
    CMD: Optional[Tuple[str, Dict]]


def command_parser(event: Event) -> None:
    """
    命令解析

    参数:
        - `event`: 消息体
    """
    try:
        if event.Msg.content.startswith("#"):
            command = event.Msg.content[:3].split("#")[1]
            arg = event.Msg.content[3:]
            event.CMD = ("#", {command: arg})
            MsgHandler.process_command(command, event=event)
        elif event.Msg.content.startswith("@"):
            event_msg = event.Msg.content.split("\u2005")
            command = event_msg[0]  # 调用者
            arg = event_msg[1]  # 内容
            event.CMD = ("at", {command: arg})
            MsgHandler.process_command("at", event=event)
        elif event.Msg.is_self_msg:
            MsgHandler.process_command("bot", event=event)
        else:
            MsgHandler.process_message(event.MsgType, event=event)

    except (IndexError, ParameterError) as err:
        log.error(f"command_parser err: {err}")


class MessageHandler:
    """
    消息处理器类。

    属性:
    - `message_handlers`: 消息处理函数字典，用于存储不同消息类型的处理函数
    - `command_handlers`: 命令处理函数字典，用于存储不同命令名称的处理函数
    """

    def __init__(self):
        self.message_handlers = {}
        self.command_handlers = {}

    def handle_message(self, msg_type: MessageType) -> Callable:
        """
        消息处理装饰器。

        参数:
        - `msg_type`: 消息类型

        返回:
        - `Callable`: 装饰器函数
        """

        def decorator(func: Callable) -> Callable:
            self.message_handlers[msg_type] = func
            return func

        return decorator

    def handle_command(self, command_name: str, priority: int = 0) -> Callable:
        """
        命令处理装饰器。

        参数:
        - `command_name`: 命令名称
        - `priority`: 命令优先级

        返回:
        - `Callable`: 装饰器函数
        """

        def decorator(func: Callable) -> Callable:
            setattr(func, 'command_name', command_name)
            setattr(func, 'priority', priority)
            self.command_handlers[command_name] = func
            return func

        return decorator

    def process_message(self, msg_type: MessageType, event: Event) -> None:
        """
        处理消息。

        参数:
        - `msg_type`: 消息类型
        - `message`: 消息对象
        """
        handler = self.message_handlers.get(msg_type)
        if handler:
            handler(event)

    def process_command(self, command_name: str, event: Event) -> None:
        """
        处理命令。

        参数:
        - `command_name`: 命令名称
        - `message`: 消息对象
        """
        command_handlers = []
        for attr_name, attr_func in self.command_handlers.items():
            if callable(attr_func) and hasattr(attr_func, 'command_name'):
                if getattr(attr_func, 'command_name') == command_name:
                    command_handlers.append(attr_func)

        if command_handlers:
            sorted_handlers = sorted(command_handlers, key=lambda x: getattr(x, 'priority'))
            for handler in sorted_handlers:
                handler(event)


MsgHandler = MessageHandler()
on_command = MsgHandler.handle_command
on_message = MsgHandler.handle_message
default_msg = """\
消息类型: {0}
消息标识: {1}
消息来源: {2}
消息内容: {3}\
"""


class HookHandler:
    def __init__(self, config):
        self.config = config
        self.message_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self.extract)
        self.worker_thread.start()
        self.chatgpt = GPT(config)

    def receive_message(self, received: str):
        """ 加入消息到队列 """
        self.message_queue.put(json.loads(received))

    @staticmethod
    def _invalid_type(received: dict):
        t = received.get("msg_type")
        try:
            msg_type = MessageType(t)
        except ValueError:
            msg_type = MessageType.CUSTOM_TYPE
        return msg_type

    def extract(self):
        while True:
            received: dict = self.message_queue.get()
            msg_type = self._invalid_type(received)
            event = Event(
                **{
                    "Msg": Message(**received),
                    "MsgType": MessageType(msg_type),
                }
            )
            command_parser(event)
            print(default_msg.format(
                event.MsgType,
                event.Msg.msgid,
                event.Msg.room_sender or event.Msg.sender,
                event.Msg.content,
            ))


__all__ = [
    "Event",
    "MsgHandler",
    "Message",
    "MessageType",
    "MessageHandler",
    "HookHandler",
    "on_command",
    "on_message",
]
