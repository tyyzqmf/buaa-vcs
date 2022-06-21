from module.appliance.base import ApplianceBase
from const import *


class AirConditioner(ApplianceBase):
    """
    空调
    """
    def __init__(self, status="关闭", location=LIVINGROOM):
        super().__init__("空调", status, location)
        # 操作列表
        self.cmd_list = {"开启", "关闭", "设置"}
        # 状态+指令集，(新状态,部分报告内容)
        self.cmd_res = {"关闭+关闭": ("关闭", "已处于关闭状态"),
                        "关闭+开启": ("开启", "已开启"),
                        "关闭+设置": ("设置", "已开启,设置至"),
                        "开启+关闭": ("关闭", "已关闭"),
                        "开启+开启": ("开启", "已处于开启状态"),
                        "开启+设置": ("设置", "设置至"),
                        "设置+关闭": ("关闭", "已关闭"),
                        "设置+开启": ("设置", "已处于开启状态"),
                        "设置+设置": ("设置", "设置至")}


if __name__ == '__main__':
    airConditioner = AirConditioner()
    print(airConditioner.exec("关闭", None))    # 关闭+关闭
    print(airConditioner.exec("开启", None))    # 关闭+开启
    print(airConditioner.exec("开启", None))    # 开启+开启
    print(airConditioner.exec("设置", 15))      # 开启+设置
    print(airConditioner.exec("关闭", None))    # 开启+关闭
    print(airConditioner.exec("设置", 28))      # 关闭+设置
    print(airConditioner.exec("开启", None))    # 设置+开启
    print(airConditioner.exec("设置", 25))      # 设置+设置
    print(airConditioner.exec("关闭", None))    # 设置+关闭

    airConditioner = AirConditioner(status="开启", location=BEDROOM)
    print(airConditioner.exec("开启", None))
    print(airConditioner.exec("开启", None))
    print(airConditioner.exec("关闭", None))

    print(airConditioner.exec("自爆", None))
