import time
from const import *


class Command:
    """
    指令模块
    """

    def __init__(self, words):
        # 原始语句
        self.words = words
        # 指令三元素
        # 对象
        self.object_type = None
        # 位置
        self.location = None
        # 动作
        self.action = None
        # 把语句解析成指令
        self._parse()

    def _parse(self):
        """
        把语句解析成指令
        例：电视、客厅、关闭
        """
        # TODO：实现语句解析成指令，【调用语音模块】

        self.object_type = "电视"
        self.location = LIVINGROOM
        self.action = "打开"

    def dilivery(self, apps):
        """
        指令下发：根据位置和对象确定指令执行的对象
        """
        # TODO：实现指令下发
        exec_result = apps[0].exec(self.action)
        cur = time.localtime()
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", cur)
        return f"{cur_time} {exec_result}"
