"""
语音模块
"""
from aip import AipSpeech
from const import appid, apikey, secretkey


def asr(file_content, format, rate, dev_dict):
    """
    语音识别
    """
    # 创建客户端
    client = AipSpeech(appid, apikey, secretkey)
    return client.asr(file_content, format, rate, dev_dict)['result'][0]


def synthesis(words):
    """
    语音合成
    """
    # 创建客户端
    client = AipSpeech(appid, apikey, secretkey)
    return client.synthesis(words, 'zh', 1, {'vol': 5, })


def lexer():
    """
    词法分析
    """
    # TODO
    pass


def depParser():
    """
    依存句法分析
    """
    # TODO
    pass
