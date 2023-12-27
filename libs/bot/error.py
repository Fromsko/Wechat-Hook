"""
    错误定义
"""


class ParameterError(TypeError):
    """ 参数异常 """

    def __init__(self, status=0, message=None):
        self.status = status
        self.message = message
