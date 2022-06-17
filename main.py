from module.appliance.tv import TV
from module.command import command
from module.io import io
from view import VCSView
import PySimpleGUI as sg
from const import *

# 记录所有的家电
apps = []


def init():
    """
    初始化家电列表
    """
    apps.append(TV())
    apps.append(TV(location=BEDROOM))


if __name__ == '__main__':
    # 初始化家电列表
    init()
    # 初始化主窗口
    view = VCSView(apps)
    window_main = view.GetMainWindow()
    # 执行记录
    history = ""

    # 更新表格数据
    def updateTableData(apps):
        data = []
        index = 1
        for app in apps:
            data.append([index, app.type, app.location, app.status])
            index += 1
        data.append(["      ", "      ", "      ", "             "])
        window_main["-智能家具-表-"].update(data)

    # 主流程
    while True:
        window, event, value = sg.read_all_windows()
        if window == window_main and event in (None, sg.WIN_CLOSED):
            window.close()
        elif event == '开始录音':
            # 开始从麦克风获取语音
            io.start()
        elif event == '停止录音':
            io.stop()
            # 获取语音
            words = io.read()
            window_main["-语音识别结果-"].update(words)
            # 指令解析
            cmd = command.Command(words)
            # 指令下发并执行
            result = cmd.delivery(apps)
            # 播放执行结果语音
            io.play(result)
            # 更新表格数据
            updateTableData(apps)
            # 更新执行记录
            history += f"{result}\n"
            window_main["-执行记录-"].update(history)
