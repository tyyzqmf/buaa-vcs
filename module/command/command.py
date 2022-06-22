import time
from aip import AipNlp
import re
import const
from const import *


class Command:
    """
    指令模块
    """

    def __init__(self, words):
        self.client = AipNlp(AIP_NLP_APP_ID, AIP_NLP_API_KEY, AIP_NLP_SECRET_KEY)
        # 原始语句
        self.words = words
        # 指令三元素
        # 对象
        self.object_type = None
        # 位置
        self.location = None
        # 动作: 打开 关闭 设置
        self.action = None
        # 度量
        self.scale = None
        # 指令类型
        self.type = None
        # 存储已确认的词id
        self.confirm_ids = []
        # 把语句解析成指令
        self._parse()

    def _parse(self):
        """
        把语句解析成指令
        例：电视、客厅、关闭
        """
        if not self.words:
            return
        print("接收的指令是: ")
        print(self.words)
        dep_data, parent_mapping = self._getDep()
        index = self._getLocation(dep_data)
        index = self._getAppliance(dep_data, index)
        index = self._getAction(dep_data, index)
        self._getScale(dep_data, parent_mapping, index)
        # 1 无度量  2 有度量  e.g 温度
        self.type = 1 if self.scale is not None else 2
        # 格式化结果
        print("location: {}, target: {}, action: {}, scale: {}, type: {}"
              .format(self.location, self.object_type, self.action, self.scale, self.type))
        print("========================================================")

    def _getDep(self):
        """ 调用依存句法分析 """
        res = self.client.depParser(self.words)
        data = {}
        parent_mapping = {}
        for item in res["items"]:
            child_ids = parent_mapping[item['head']] if parent_mapping.keys().__contains__(item['head']) else []
            child_ids.append(item['id'])
            parent_mapping.update(
                {
                    item['head']: child_ids
                }
            )
            data.update(
                {
                    item['id']: {
                        "word": item["word"],
                        "postag": const.POS[item["postag"]],
                        "head": item['head'],
                        "deprel": const.DEPRE[item['deprel']]
                    }
                }
            )
        print(data)
        print(parent_mapping)
        return data, parent_mapping

    def _getLocation(self, data):
        """ 获取location """
        location = None
        parent = 0
        location_id = 0
        # 获取location  卧室 厨房 ...
        for index in data.keys():
            if (data[index]['deprel'] == '定中关系') & (data[index]['postag'] == '普通名词'):
                location = data[index]['word']
                parent = data[index]['head']
                location_id = index
                self.confirm_ids.append(index)
                break
        # 补全location  卧室 -> 卧室A / 卧室1
        if location_id > 1:
            if (data[location_id - 1]['deprel'] == '定中关系') & (data[location_id - 1]['head'] == location_id):
                self.confirm_ids.append(location_id - 1)
                location = data[location_id - 1]['word'] + location
        if data[location_id + 1]['deprel'] == '定中关系':
            if data[location_id + 1]['head'] == location_id:
                self.confirm_ids.append(location_id + 1)
                location = location + data[location_id + 1]['word']
            elif (data[location_id + 1]['head'] == (location_id + 2)) & (data[location_id + 2]['deprel'] == '定中关系'):
                self.confirm_ids.append(location_id + 1)
                location = location + data[location_id + 1]['word']
        print("识别的房间是：" + location)
        self.location = location if location in LOCATIONS else '未知房间'
        return parent

    def _getAppliance(self, data, parent):
        """ 获取家电 """
        if data[parent]['postag'] == '普通名词':
            object_type = data[parent]['word']
            self.confirm_ids.append(parent)
            before_id = parent - 1
            # 补全家电名称
            if (parent > 1) & (data[parent - 1]['deprel'] == '定中关系') & (data[parent - 1]['head'] == parent) & (before_id not in self.confirm_ids):
                object_type = data[parent - 1]['word'] + object_type
                self.confirm_ids.append(parent - 1)
            if data.keys().__contains__(parent + 1):
                if (data[parent + 1]['deprel'] == '定中关系') & (data[parent + 1]['head'] == parent):
                    object_type = object_type + data[parent + 1]['word']
                    self.confirm_ids.append(parent + 1)
                if (data[parent + 1]['deprel'] == '子句结构') & (data[parent + 1]['head'] == data[parent]['head']):
                    object_type = object_type + data[parent + 1]['word']
                    self.confirm_ids.append(parent + 1)
        else:
            object_type = '未知家电'

        print("识别的家电是：" + object_type)
        self.object_type = object_type if object_type in APPS else '未知家电'
        parent = data[parent]['head']
        return parent

    def _getAction(self, data, parent):
        """ 获取Action """
        act = '未知动作'
        action_id = 0
        if parent > 0:
            while True:
                if (data[parent]['postag'] in ['普通动词', '动名词']) & (data[parent]['deprel'] in ['核心关系', '并列关系']):
                    action_id = parent
                    self.confirm_ids.append(action_id)
                    act = data[parent]['word']
                    break
                else:
                    if data[parent]['head'] == 0:
                        action_id = parent
                        self.confirm_ids.append(action_id)
                        act = '未知动作'
                        break
                    else:
                        parent = data[parent]['head']
        print("识别的动作是：" + act)
        self.action = ACTIONS[act] if act in ACTIONS.keys() else '未知动作'
        return action_id

    def _getScale(self, data, parent_mapping, action_id):
        """ 获取Scale """
        scale = None
        flag = True
        """
        {1: {'word': '把', 'postag': '介词', 'head': 5, 'deprel': '介宾关系'},
        2: {'word': '卧室', 'postag': '普通名词', 'head': 4, 'deprel': '定中关系'}, 
        3: {'word': '的', 'postag': '助词', 'head': 2, 'deprel': '虚词成分'}, 
        4: {'word': '空调', 'postag': '普通名词', 'head': 1, 'deprel': '介宾关系'}, 
        5: {'word': '调节', 'postag': '普通动词', 'head': 0, 'deprel': '核心关系'}, 
        6: {'word': '到', 'postag': '介词', 'head': 5, 'deprel': '动补关系'}, 
        7: {'word': '26度', 'postag': '数量词', 'head': 6, 'deprel': '介宾关系'}, 
        8: {'word': '。', 'postag': '标点符号', 'head': 5, 'deprel': '虚词成分'}}
        """
        while flag:
            if (action_id != 0) & (action_id in parent_mapping.keys()) & (len(set(parent_mapping[action_id]).difference(set(self.confirm_ids))) > 0):
                for index in set(parent_mapping[action_id]).difference(set(self.confirm_ids)):
                    if data[index]['deprel'] == '动补关系':
                        action_id = index
                        self.confirm_ids.append(action_id)
                        break
                    if (data[index]['deprel'] == '介宾关系') & (data[index]['postag'] == '介词'):
                        self.confirm_ids.append(index)
                        continue
                    elif data[index]['deprel'] in ['动宾关系', '介宾关系']:
                        action_id = index
                        if data[index]['postag'] == '普通名词':
                            if (index > 1) & (data[index-1]['deprel'] == '定中关系') & (data[index-1]['head'] == index):
                                # 确认
                                scale = data[index-1]['word'] + data[index]['word']
                                self.confirm_ids.append(index - 1)
                                self.confirm_ids.append(index)
                                flag = False
                                break
                        elif data[index]['postag'] in ['动名词']:
                            scale = data[index]['word']
                            self.confirm_ids.append(index)
                            flag = False
                            break
                        elif data[index]['postag'] in ['普通动词']:
                            if index in parent_mapping.keys():
                                if len(parent_mapping[index]) > 0:
                                    break
                            else:
                                scale = data[index]['word']
                                self.confirm_ids.append(index)
                                flag = False
                                break
                        elif data[index]['postag'] == '数量词':
                            scale = re.findall(r"(\d+)", data[index]['word'])[0]
                            self.confirm_ids.append(index)
                            flag = False
                            break
                    else:
                        self.confirm_ids.append(index)
                        # flag = False
                        # break
            else:
                flag = False
        if scale is not None:
            print("识别的模式是：" + scale)
            if (self.object_type in TEMP_APPS) & (scale.isdigit()):
                self.scale = int(scale)
            else:
                if self.object_type in APPS:
                    if scale in SCALES[self.object_type].keys():
                        self.scale = SCALES[self.object_type][scale]
                    elif scale in SCALES_ACTION_MAPPING.keys():
                        self.scale = None
                        self.action = SCALES_ACTION_MAPPING[scale]
                    else:
                        self.scale = "未知模式"
        else:
            print("识别的模式是：None")
            self.scale = None

    def delivery(self, apps):
        """
        指令下发：根据位置和对象确定指令执行的对象
        """
        exec_result = ""
        for app in apps:
            # 通过位置和类型确定指令执行对象
            if self.location == app.location and self.object_type == app.type:
                exec_result = app.exec(self.action, self.scale)
                break
        cur = time.localtime()
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", cur)
        return exec_result, f"{cur_time} {exec_result}"
