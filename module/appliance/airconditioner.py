from module.appliance.base import ApplianceBase
from const import *


class AirConditioner(ApplianceBase):
    """
    空调
    """
    def __init__(self, status="关闭", location=LIVINGROOM, temperature="18度", mode="自动"):
        super().__init__("空调", status, location)
        self.temperature = temperature
        self.mode = mode
        self.scale = self.mode + "&" + self.temperature

    def exec(self, cmd, scale):
        """
        执行指令
        """
        # 当前状态+指令
        cur = f"{self.status}+{cmd}"
        if cur not in self.cmd_res:
            return f"不支持该指令，当前支持的指令为{self.cmd_list}！"
        # 执行指令，返回状态
        self.status = self.cmd_res[cur][0]

        # 根据scale的类型判断设置的是温度还是状态
        if scale is not None:
            if isinstance(scale, int):
                scale = str(scale) + "度"
                self.temperature = scale
            else:
                self.mode = scale
            self.scale = self.mode + "&" + self.temperature
        return self.report(self.cmd_res[cur][1], scale)


if __name__ == '__main__':
    airConditioner = AirConditioner()
    print(airConditioner.exec("开启", None))    # 关闭+关闭
    print(airConditioner.exec("设置", "制冷"))      # 开启+设置
    print(airConditioner.exec("设置", 25))    # 开启+关闭
    print(airConditioner.exec("设置", 28))      # 关闭+设置
    print(airConditioner.exec("开启", None))    # 设置+开启
    print(airConditioner.exec("设置", 25))      # 设置+设置
    print(airConditioner.exec("关闭", None))    # 设置+关闭

    airConditioner = AirConditioner(status="开启", location=BEDROOM)
    print(airConditioner.exec("开启", None))
    print(airConditioner.exec("开启", None))
    print(airConditioner.exec("关闭", None))

    print(airConditioner.exec("自爆", None))
