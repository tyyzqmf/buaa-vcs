from module.appliance.base import ApplianceBase
from const import *


class Light(ApplianceBase):
    """
    电灯
    """

    def __init__(self, status="关闭", location=LIVINGROOM):
        super().__init__("电灯", status, location)


if __name__ == '__main__':
    light = Light()
    print(light.exec("设置", "写作模式"))        # 关闭+设置
    print(light.exec("设置", "观影模式"))        # 开启+设置
    print(light.exec("开启", None))              # 开启+开启
    print(light.exec("关闭", None))              # 开启+关闭
    print(light.exec("待机", None))              # 关闭+待机
    print(light.exec("设置", "轰趴模式"))        # 待机+设置
    print(light.exec("待机", None))              # 开启+待机
    print(light.exec("关闭", None))              # 待机+关闭
    print(light.exec("关闭", None))              # 关闭+关闭
    print(light.exec("开启", None))              # 关闭+开启

    light = Light(status="待机", location=BEDROOM)
    print(light.exec("待机", None))              # 待机+待机
    print(light.exec("开启", None))              # 待机+开启

    print(light.exec("自爆", None))
