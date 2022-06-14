"""
输入输出模块
"""
from wsgiref.simple_server import sys_version
import pyaudio  # conda安装
import wave
import threading
from playsound import playsound  # pip安装
from module.voice import voice
import pygame
import os



class Recorder:
    def __init__(self):
        self.CHUNK = 1024  # 每个缓冲区的帧数
        self.FORMAT = pyaudio.paInt16  # 采样位数
        self.CHANNELS = 1  # 单声道
        # self.RATE = 44100  # 采样频率
        self.RATE = 16000
        self.wave_out_path = 'module/io/temp.wav'  # 只保留最近一个的录入音频
        self.stop_flag = 0
        self.max_record_second = 150  # 最大录制时间（秒）

    def record_audio(self):
        """ 录音功能 """
        print("录音开始....")
        p = pyaudio.PyAudio()  # 实例化对象
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)  # 打开流，传入响应参数
        wf = wave.open(self.wave_out_path, 'wb')  # 打开 wav 文件。
        wf.setnchannels(self.CHANNELS)  # 声道设置
        wf.setsampwidth(p.get_sample_size(self.FORMAT))  # 采样位数设置
        wf.setframerate(self.RATE)  # 采样频率设置

        for _ in range(0, int(self.RATE * self.max_record_second / self.CHUNK)):
            if self.stop_flag == 1:
                self.stop_flag = 0
                break
            data = stream.read(self.CHUNK)
            wf.writeframes(data)  # 写入数据
        self.stop_flag = 0
        stream.stop_stream()  # 关闭流
        stream.close()
        p.terminate()
        wf.close()
        print("录音结束....")

    def new_thread_recorder(self):
        t = threading.Thread(target=self.record_audio, name='record', args=())
        t.start()

    def stop_record(self):
        self.stop_flag = 1


recorder = Recorder()


def start():
    """
    开始录音，保存到临时文件 temp.wav
    :return:
    """
    recorder.new_thread_recorder()


def stop():
    """
    停止录音，关闭文件
    :return:
    """
    recorder.stop_record()


def read():
    """
    从临时录音文件读取语音，并解析成文字
    """
    wave_path = 'module/io/temp.wav'

    # 读取文件
    def get_file_content(path):
        with open(path, 'rb') as fp:
            return fp.read()
    
    # 识别本地文件
    words = voice.asr(get_file_content(wave_path),format='wav', rate=16000,dev_dict={'dev_pid':1537})
    
    # 清掉temp.wav文件
    if(os.path.exists(wave_path)):
        os.remove(wave_path)
        print("文件删除成功")
        
    return words

def player(song):
    chunk = 1024
    wf = wave.open(song, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()


def play(words):
    """
    把文字从播放器播出
    """
    # 语音合成
    words= '欢迎使用，已打开'           # 获取到执行结果后删除即可
    result = voice.synthesis(words)

    with open('audio.mp3', 'wb') as f:
        f.write(result)

    # 语音播放
    song = 'audio.mp3'  # TODO 改成语音合成后的位置即可（不支持中文路径）
    # playsound(song)
    pygame.mixer.init()
    pygame.mixer.music.load('audio.mp3')  
    pygame.mixer.music.set_volume(0.5) 
    pygame.mixer.music.play()
    return

