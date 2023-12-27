"""
    提供 logger 对象。
    > 其他任何 "libs" 模块都应使用此模块的 "logger" 来打印日志。

    Tip:
        移除 `logging` 改用 `loguru.logger`
"""
from loguru import logger
# import logging
#
#
# class ColourFormatter(logging.Formatter):
#     """ Use discord.utils _ColourFormatter """
#
#     LEVEL_COLOURS = [
#         (logging.DEBUG, '\x1b[40;1m'),  # 调试级别为黑色背景
#         (logging.INFO, '\x1b[36;1m'),  # 信息级别为青色
#         (logging.WARNING, '\x1b[33;1m'),  # 警告级别为黄色
#         (logging.ERROR, '\x1b[31m'),  # 错误级别为红色
#         (logging.CRITICAL, '\x1b[41m'),  # 严重错误级别为红色背景
#     ]
#
#     FORMATS = {
#         level: logging.Formatter(
#             f'\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m {colour}%(message)s'
#             f'\x1b[0m',
#             '%Y-%m-%d %H:%M:%S',
#         )
#         for level, colour in LEVEL_COLOURS
#     }
#
#     def format(self, record):
#         formatter = self.FORMATS.get(record.levelno)
#         if formatter is None:
#             formatter = self.FORMATS[logging.DEBUG]
#
#         # Override the traceback to always print in red
#         if record.exc_info:
#             text = formatter.formatException(record.exc_info)
#             record.exc_text = f'\x1b[31m{text}\x1b[0m'
#
#         output = formatter.format(record)
#
#         # Remove the cache layer
#         record.exc_text = None
#         return output
#
#
# class Logger:
#     __slots__ = ("log", "colour_handler", "file_handler")
#
#     def __init__(self, filename="discord.log", level=logging.INFO) -> None:
#         # Get file path
#         library, _, _ = __name__.partition('.')
#         self.log = logging.getLogger(library)
#         # Set log level
#         self.log.setLevel(level)
#         # Set handlers
#         self.colour_handler = logging.StreamHandler()
#         self.file_handler = logging.FileHandler(
#             filename, encoding="utf-8", mode="a"
#         )
#         self.colour_handler.setFormatter(ColourFormatter())
#         self.log.addHandler(self.colour_handler)
#         self.log.addHandler(self.file_handler)
#
#     def close(self) -> None:
#         # 关闭处理程序，避免资源泄漏
#         self.colour_handler.close()
#         self.file_handler.close()
#
#     def __call__(self) -> logging.Logger:
#         return self.log
#
#
# logger = Logger("wechat-bot.log").log

log = logger.bind(name="inject_dll")
log.add(
    "wechat-bot.log",
    format="{time} | {level} | {message}",
    rotation="1 week",
)

__all__ = [
    'logger',
]
