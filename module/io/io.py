"""
输入输出模块
"""
import pyaudio
import wave
import threading


class Recorder:
    def __init__(self):
        self.CHUNK = 1024  # 每个缓冲区的帧数
        self.FORMAT = pyaudio.paInt16  # 采样位数
        self.CHANNELS = 1  # 单声道
        self.RATE = 44100  # 采样频率
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
    # TODO

    return "打开客厅的电视"

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
    # TODO：语音合成+播放

    # 语音播放
    song = 'module/io/temp.wav'  # TODO 改成语音合成后的位置即可（不支持中文路径）
    player(song)
    return


if __name__ == '__main__':
    # test commit
    play(1)
