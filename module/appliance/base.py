class ApplianceBase(object):
    """
        ApplianceBase: 家电基类
    """
    def __init__(self, type, status, location):
        self.type = type
        self.status = status
        self.location = location

    def exec(self, cmd):
        """
        执行指令
        """
        pass

    def report(self):
        """
        返回当前状态
        """
        pass
