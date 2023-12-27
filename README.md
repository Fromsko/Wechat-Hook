# Wechat-Hook

> 基于 [WeChat-PyRobot](https://github.com/kanadeblisst00/WeChat-PyRobot) 简单封装的一个机器人骨架

## 📑 已实现

- [x] Hook 消息 `on_message | on_command`
- [x] 回调函数 `decorator`
- [ ] 防撤回并记录 `msg_id`
- [ ] 可选重载 or 直接启动

## 🔗 数据定义

### 消息体 `Event`

+ 定义
    ```python
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
    ```

### 消息类型 `MessageType`

+ 定义
    ```python
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
    ```

### 消息事件 `on_message`

<details>
<summary>函数原型</summary>

```python
def handle_message(self, msg_type: MessageType) -> Callable:
    """
    消息处理装饰器。

    参数:
    - `msg_type`: 消息类型

    返回:
    - `Callable`: 装饰器函数
    """
```

</details>

---

**使用案例**

1. 文本消息
   ```python
   @on_message(MessageType.TEXT)
   def handle_public_message(event: Event) -> None:
       """处理文本消息逻辑"""
       log.info(
           "文本消息: {sender}",
           sender=event.Msg.sender,
       )
   ```

2. 图片消息
    ```python
    @on_message(MessageType.IMAGE)
    def handle_image_message(event: Event) -> None:
        """处理图片消息逻辑"""
        log.info(
            "图片消息: {sender}",
            sender=event.Msg.sender,
        )
    ```

### 命令事件 `on_command`

<details>
<summary>函数原型</summary>

```python
def handle_command(self, command_name: str, priority: int = 0) -> Callable:
    """
    命令处理装饰器。

    参数:
    - `command_name`: 命令名称
    - `priority`: 命令优先级

    返回:
    - `Callable`: 装饰器函数
    """
```

</details>

---

**三种固定格式**

1. 触发条件: `#聊天 xxx`
    ```python
    @on_command('聊天', priority=1)
    def handle_chat_command(event: Event) -> None:
        """处理 聊天 命令逻辑"""
    ```

2. 触发条件: 当 `Bot` 被用户 @

   ```python
   @on_command('at', priority=2)
   def handle_at_command(event: Event) -> None:
       """处理被用户 at 命令逻辑"""
   ```

3. 触发条件: `Bot`自身响应
   ```python
   @on_command('bot', priority=2)
   def handle_bot_command(event: Event) -> None:
       """处理机器人自身的信息"""
   ```

**自定义**
> 修改: `libs.bot.event: command_parser`
<details>
<summary>函数原型</summary>

```python
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
```

</details>


## 🙏 鸣谢

感谢以下开源项目，它们为本项目的开发提供了重要支持：

- [Pillow](https://pillow.readthedocs.io/en/stable/): 🖼️ 用于图像处理的 Python 库。
- [WeChat-PyRobot](https://github.com/kanadeblisst00/WeChat-PyRobot) 💉 注入Python到微信实现微信机器人 

## ©️ 许可

本项目基于 MIT 许可证，请查阅 LICENSE 文件以获取更多信息。