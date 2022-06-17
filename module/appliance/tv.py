from module.appliance.base import ApplianceBase
from const import *


class TV(ApplianceBase):
    """
    电视机
    """

    def __init__(self, status="关闭", location=LIVINGROOM):
        super().__init__("电视", status, location)
        # 操作列表
        self.cmd_list = {"打开", "关闭"}
        # 状态+指令集，(新状态,部分报告内容)
        self.cmd_res = {"关闭+关闭": ("关闭", "已处于关闭状态"),
                        "打开+关闭": ("关闭", "已关闭"),
                        "关闭+打开": ("打开", "已打开"),
                        "打开+打开": ("打开", "已处于打开状态")}


if __name__ == '__main__':
    tv = TV()
    print(tv.exec("关闭", None))
    print(tv.exec("打开", None))
    print(tv.exec("打开", None))
    print(tv.exec("关闭", None))

    tv = TV(status="打开", location=BEDROOM)
    print(tv.exec("打开", None))
    print(tv.exec("打开", None))
    print(tv.exec("关闭", None))

    print(tv.exec("自爆", None))
