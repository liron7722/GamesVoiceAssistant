import pyaudio
import wave
from array import array
import time
import math
import struct
import simpleaudio as sa
from extra import change_status

FORMAT=pyaudio.paInt16
CHANNELS = 1  # 2
RATE= 16000  # 44100
CHUNK=1024
Threshold = 10
SHORT_NORMALIZE = (1.0/32768.0)
swidth = 2
Volume_Limit = 500  # 750
TIMEOUT_LENGTH = 0.75  # 1
FILE_NAME = "RECORDING.wav"


class Recorder:
    def open_stream(self):
        self.audio=pyaudio.PyAudio() #instantiate the pyaudio
        #recording prerequisites
        self.stream=self.audio.open(format=FORMAT,channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)

    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def save_to_file(self, frames):
        wavfile=wave.open(FILE_NAME,'wb')
        wavfile.setnchannels(CHANNELS)
        wavfile.setsampwidth(self.audio.get_sample_size(FORMAT))
        wavfile.setframerate(RATE)
        if frames is not None:
            wavfile.writeframes(b''.join(frames))#append frames recorded to file
        wavfile.close()

    @staticmethod
    def get_wave_obj(file_name):
        wave_obj = sa.WaveObject.from_wave_file(file_name)
        return wave_obj

    def play(self, file_name):
        play_obj = self.get_wave_obj(file_name).play()
        play_obj.wait_done()  # Wait until sound has finished playing

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def record(self):
        frames = []
        while len(frames) < 1:
            current = time.time()
            end = time.time() + TIMEOUT_LENGTH

            while current <= end:
                flag = True
                data=self.stream.read(CHUNK)
                data_chunk=array('h',data)
                vol = max(data_chunk)

                if vol >= Volume_Limit:
                    frames.append(data)
                    end = time.time() + TIMEOUT_LENGTH
                    flag = True
                current = time.time()

                if current > (end - (TIMEOUT_LENGTH / 2)):
                    if flag:
                        flag = False
                        print("Detecting Silence, going to stop")

        return frames

    def listen(self):
        change_status('yellow')
        self.open_stream()
        print('Listening beginning')

        while False:
            input = self.stream.read(CHUNK)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                break

        print('Recording beginning')
        change_status('orange')
        frames = self.record()
        self.close_stream()

        print('Recording ended, Listening ended')
        change_status('green')
        # writing to file
        self.save_to_file(frames)
