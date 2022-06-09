import PySimpleGUI as sg


class VCSView:
    def __init__(self, apps):
        # 智能家具列表
        self.apps = apps
        # 主窗口
        self.main_layout = []
        # 家电表格数据
        self.data = []
        index = 1
        for app in apps:
            self.data.append([index, app.type, app.location])
            index += 1
        self.data.append(["      ", "      ", "           "])

    # 创建主窗口
    def GetMainWindow(self, ):
        f1 = sg.Frame(title='智能家具列表',
                      layout=[
                          [sg.Table(
                              key='-智能家具-表-',
                              values=self.data,
                              headings=['序号', '家具', '位置'],
                              hide_vertical_scroll=True,
                              auto_size_columns=True,  # 自动调整列宽（根据上面第一次的values默认值为准，update时不会调整）
                              justification='center',  # 字符排列 left right center
                              num_rows=26,  # 行数
                              text_color='black',
                              background_color='white')],
                      ],
                      )
        f2 = sg.Frame(title='语音控制',
                      layout=[
                          [sg.Button("开始录音"), sg.Button("停止录音")],
                          [sg.T("语音识别结果：")],
                          [sg.Multiline(key='-语音识别结果-', size=(50, 3))],
                          [sg.T("执行记录：")],
                          [sg.Multiline(key='-执行记录-', size=(50, 17))],
                      ]
                      )
        # 定义主窗口布局
        self.main_layout = [[f1, f2]]

        return sg.Window('智能家具语音控制系统', self.main_layout, finalize=True, default_element_size=(50, 1))
