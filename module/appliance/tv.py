from .base import ApplianceBase
from const import *


class TV(ApplianceBase):
    """
    电视机
    """
    # 电视机支持的指令集，以及状态转移
    # 例：关闭状态收到"打开"指令，状态更新为：打开
    _CMD_ = {
        "关闭+关闭": "关闭",
        "打开+关闭": "关闭",
        "关闭+打开": "打开",
        "打开+打开": "打开",
    }

    def __init__(self, status="关闭", location=LIVINGROOM):
        super().__init__("电视", status, location)

    def exec(self, cmd):
        """
        执行指令
        """
        # 当前状态+指令
        cur = f"{self.status}+{cmd}"
        if cur not in self._CMD_:
            return "不支持该指令，您可以说打开或者关闭电视机！"
        # 执行指令，返回状态
        self.status = self._CMD_[cur]
        return self.report()

    def report(self):
        """
        返回当前状态
        """
        return f'{self.location}的{self.type}已{self.status}'
