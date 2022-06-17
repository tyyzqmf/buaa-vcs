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
        self.cmd_list = {}
        # (状态+指令集，(新状态,部分报告内容))
        self.cmd_res = {}

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
        return f"{self.location}的{self.type}{part_report}{f'{scale}' if scale is not None else ''}"
