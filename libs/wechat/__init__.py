import platform

if "64" in platform.architecture()[0]:
    from libs.wechat.hooklog64 import HookLog
    from libs.wechat.sendmsg64 import SendMsg
    from libs.wechat.hookmsg64 import HookMsg
    from libs.wechat.anti_revoke64 import AntiRevoke
else:
    from libs.wechat.hooklog32 import HookLog
    from libs.wechat.sendmsg32 import SendMsg
    from libs.wechat.hookmsg32 import HookMsg
    from libs.wechat.anti_revoke32 import AntiRevoke

__version__ = "0.1.1"

__all__ = [
    "SendMsg",
    "HookLog",
    "HookMsg",
    "AntiRevoke"
]
