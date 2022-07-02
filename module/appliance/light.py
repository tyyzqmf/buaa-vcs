from module.appliance.base import ApplianceBase
from const import *


class Light(ApplianceBase):
    """
    电灯
    """

    def __init__(self, status="关闭", location=LIVINGROOM):
        super().__init__("电灯", status, location)
        # 操作列表
        self.cmd_list = {'开启', '关闭'}
        # (状态+指令集，(新状态,部分报告内容))
        self.cmd_res = {
            "开启+开启": ("开启", "已处于开启状态"),
            "开启+关闭": ("关闭", "已关闭"),
            "关闭+开启": ("开启", "已开启"),
            "关闭+关闭": ("关闭", "已处于关闭状态"),
        }

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
        if scale is not None:
            self.scale = scale
        return self.report(self.cmd_res[cur][1], scale)


if __name__ == '__main__':
    light = Light()
    print(light.exec("设置", "写作模式"))  # 关闭+设置
    print(light.exec("设置", "观影模式"))  # 开启+设置
    print(light.exec("开启", None))  # 开启+开启
    print(light.exec("关闭", None))  # 开启+关闭
    print(light.exec("待机", None))  # 关闭+待机
    print(light.exec("设置", "轰趴模式"))  # 待机+设置
    print(light.exec("待机", None))  # 开启+待机
    print(light.exec("关闭", None))  # 待机+关闭
    print(light.exec("关闭", None))  # 关闭+关闭
    print(light.exec("开启", None))  # 关闭+开启

    light = Light(status="待机", location=BEDROOM)
    print(light.exec("待机", None))  # 待机+待机
    print(light.exec("开启", None))  # 待机+开启

    print(light.exec("自爆", None))
