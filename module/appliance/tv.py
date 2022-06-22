from module.appliance.base import ApplianceBase
from const import *


class TV(ApplianceBase):
    """
    电视机
    """

    def __init__(self, status="关闭", location=LIVINGROOM):
        super().__init__("电视", status, location)


if __name__ == '__main__':
    tv = TV()
    print(tv.exec("关闭", None))     # 关闭 + 关闭
    print(tv.exec("开启", None))     # 关闭 + 开启
    print(tv.exec("开启", None))     # 开启 + 开启
    print(tv.exec("设置", "游戏模式"))     # 开启 + 设置
    print(tv.exec("待机", None))     # 开启 + 待机
    print(tv.exec("关闭", None))     # 待机 + 关闭
    print(tv.exec("待机", None))     # 关闭 + 待机
    print(tv.exec("开启", None))     # 待机 + 开启
    print(tv.exec("关闭", None))     # 开启 + 关闭

    tv = TV(status="待机", location=BEDROOM)
    print(tv.exec("待机", None))    # 待机 + 待机

    print(tv.exec("自爆", None))
