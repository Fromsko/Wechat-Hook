"""
helpers 文档帮助
"""
from pathlib import Path
from typing import Optional, Union

from libs.bot.error import ParameterError
from libs.bot.event import Event, MessageType
from libs.log import logger as log
from libs.wechat import SendMsg


class Send(SendMsg):
    def to_group(
            self,
            event: Event,
            msg: Union[str, Path], group_id: Optional[str] = None,
            msg_type: MessageType = MessageType.TEXT
    ) -> None:
        """
        发送到群聊

        参数:
            - `event`: 消息体
        :return:
        """
        if group_id is None:
            if all([event.Msg.room_sender, event.Msg.sender]) or "chatroom" in event.Msg.sender:
                """
                > 群聊 且 用户
                """
                group_id = event.Msg.sender
            else:
                raise ParameterError(message="参数不足或不正确: group_id")

        if msg_type == MessageType.TEXT:
            if not isinstance(msg, str):
                raise ParameterError(message="参数不足或不正确: msg")
            self.send_text(group_id, msg)

        elif msg_type == MessageType.IMAGE:
            if Path(msg).exists():
                raise FileNotFoundError()
            self.send_image(group_id, str(msg))

    def to_user(
            self,
            event: Event,
            msg: Union[str, Path], user_id: Optional[str] = None,
            msg_type: MessageType = MessageType.TEXT
    ) -> None:
        if user_id is None:
            if event.Msg.sender is not None:
                """
                > 群聊 且 用户
                """
                user_id = event.Msg.sender
            else:
                raise ParameterError(message="参数不足或不正确: user_id")

        if msg_type == MessageType.TEXT:
            if not isinstance(msg, str):
                raise ParameterError(message="参数不足或不正确: msg")
            self.send_text(user_id, msg)

        elif msg_type == MessageType.IMAGE:
            if Path(msg).exists():
                raise FileNotFoundError()
            self.send_image(user_id, str(msg))


__all__ = [
    'Send'
]
