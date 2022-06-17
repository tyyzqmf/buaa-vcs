from module.appliance.base import ApplianceBase
from const import *


class AirConditioner(ApplianceBase):
    """
    空调
    """
    def __init__(self, status="关闭", location=LIVINGROOM):
        super().__init__("空调", status, location)
        # 操作列表
        self.cmd_list = {"打开", "关闭", "调温"}
        # 状态+指令集，(新状态,部分报告内容)
        self.cmd_res = {"关闭+关闭": ("关闭", "已处于关闭状态"),
                        "关闭+打开": ("打开", "已打开"),
                        "关闭+调温": ("调温", "已打开,调温至"),
                        "打开+关闭": ("关闭", "已关闭"),
                        "打开+打开": ("打开", "已处于打开状态"),
                        "打开+调温": ("调温", "调温至"),
                        "调温+关闭": ("关闭", "已关闭"),
                        "调温+打开": ("调温", "已处于打开状态"),
                        "调温+调温": ("调温", "调温至")}


if __name__ == '__main__':
    airConditioner = AirConditioner()
    print(airConditioner.exec("关闭", None))    # 关闭+关闭
    print(airConditioner.exec("打开", None))    # 关闭+打开
    print(airConditioner.exec("打开", None))    # 打开+打开
    print(airConditioner.exec("调温", 15))      # 打开+调温
    print(airConditioner.exec("关闭", None))    # 打开+关闭
    print(airConditioner.exec("调温", 28))      # 关闭+调温
    print(airConditioner.exec("打开", None))    # 调温+打开
    print(airConditioner.exec("调温", 25))      # 调温+调温
    print(airConditioner.exec("关闭", None))    # 调温+关闭

    airConditioner = AirConditioner(status="打开", location=BEDROOM)
    print(airConditioner.exec("打开", None))
    print(airConditioner.exec("打开", None))
    print(airConditioner.exec("关闭", None))

    print(airConditioner.exec("自爆", None))
