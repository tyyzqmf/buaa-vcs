class ApplianceBase(object):
    """
        ApplianceBase: 家电基类
    """

    def __init__(self, type, status, location, scale=None):
        self.type = type
        self.status = status
        self.location = location
        self.scale = scale
        # 操作列表
        self.cmd_list = {"设置", '开启', '关闭', '待机'}
        # (状态+指令集，(新状态,部分报告内容))
        self.cmd_res = {"开启+设置": ("开启", "已设置为"),
                        "开启+开启": ("开启", "已处于开启状态"),
                        "开启+关闭": ("关闭", "已关闭"),
                        "开启+待机": ("待机", "已设置为待机状态"),
                        "关闭+设置": ("开启", "已开启，并设置为"),  # 不确定是否合理
                        "关闭+开启": ("开启", "已开启"),
                        "关闭+关闭": ("关闭", "已处于关闭状态"),
                        "关闭+待机": ("待机", "已设置为待机状态"),  # 不确定是否合理
                        "待机+设置": ("开启", "已开启，并设置为"),  # 不确定是否合理
                        "待机+开启": ("开启", "已开启"),
                        "待机+关闭": ("关闭", "已关闭"),
                        "待机+待机": ("待机", "已处于待机状态")
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

    def report(self, part_report, scale):
        """
        返回当前状态
        """
        return f"{self.location}的{self.type}{part_report}{scale if scale is not None else ''}"
