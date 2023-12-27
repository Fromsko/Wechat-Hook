"""
    主函数
"""
from libs.bot.event import (
    Event,
    HookHandler, MessageType,
    on_command, on_message
)
from libs.bot.helpers import Send
from libs.log import logger as log
from libs.wechat import HookMsg

hk = HookHandler(
    config={
        # GPT 配置
        "api_key": "sk-xxx",
        "api_base": "https://api.aigcbest.top/v1",
        "proxy": "",
        "async_openai": False
    }
)
wechat = HookMsg(hk.receive_message)
send = Send()
wechat.hook()


@on_message(MessageType.TEXT)
def handle_public_message(event: Event) -> None:
    """处理文本消息逻辑"""
    log.info(
        "文本消息: {sender}",
        sender=event.Msg.sender,
    )


@on_message(MessageType.IMAGE)
def handle_image_message(event: Event) -> None:
    """处理图片消息逻辑"""
    log.info(
        "图片消息: {sender}",
        sender=event.Msg.sender,
    )


@on_message(MessageType.CUSTOM_TYPE)
def handle_custom_message(event: Event) -> None:
    """处理自定义消息逻辑"""
    log.info(
        "自定义消息: {sender}",
        sender=event.Msg.sender,
    )


@on_command('聊天', priority=1)
def handle_chat_command(event: Event) -> None:
    """处理 hello 命令逻辑"""
    log.info(
        "命令消息-聊天: {sender} 命令{cmd}",
        sender=event.Msg.sender,
        cmd=event.CMD[1],
    )
    reply = hk.chatgpt.send_to_chatgpt(
        event.CMD[1],
    )
    send.to_user(event, msg=reply)


@on_command('at', priority=2)
def handle_at_command(event: Event) -> None:
    """处理被用户 at 命令逻辑"""
    log.info(
        "at {sender}",
        sender=event.Msg.sender,
    )
    reply = hk.chatgpt.send_to_chatgpt(
        event.Msg.content,
    )
    send.to_user(event, msg=reply)


@on_command('bot', priority=2)
def handle_bot_command(event: Event) -> None:
    """处理机器人自身的信息"""
    log.info(
        "Bot {sender}",
        sender=event.Msg.sender,
    )
