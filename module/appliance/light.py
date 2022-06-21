from module.appliance.base import ApplianceBase
from const import *


class Light(ApplianceBase):
    """
    电灯
    """

    def __init__(self, status="关闭", location=LIVINGROOM):
        super().__init__("电灯", status, location)
        # 操作列表
        self.cmd_list = {"开启", "关闭"}
        # 状态+指令集，(新状态,部分报告内容)
        self.cmd_res = {"关闭+关闭": ("关闭", "已处于关闭状态"),
                        "开启+关闭": ("关闭", "已关闭"),
                        "关闭+开启": ("开启", "已开启"),
                        "开启+开启": ("开启", "已处于开启状态")}


if __name__ == '__main__':
    light = Light()
    print(light.exec("关闭", None))
    print(light.exec("开启", None))
    print(light.exec("开启", None))
    print(light.exec("关闭", None))

    light = Light(status="开启", location=BEDROOM)
    print(light.exec("开启", None))
    print(light.exec("开启", None))
    print(light.exec("关闭", None))

    print(light.exec("自爆", None))
