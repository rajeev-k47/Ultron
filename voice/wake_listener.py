import struct
import pyaudio
import pvporcupine
from voice import VoiceCommands


class WakeListener:
    def __init__(
        self,
        access_key,
        buzzer,
        headlight,
        tubelight,
        state,
        keywords=None,
    ):
        self.porcupine = pvporcupine.create(access_key=access_key, keywords=keywords)
        self.sample_rate = self.porcupine.sample_rate
        self.frame_length = self.porcupine.frame_length
        self.state = state

        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            rate=self.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.frame_length,
        )

        self.vc = VoiceCommands(buzzer, headlight, tubelight, self.state)

    def listen(self):
        try:
            while True:
                pcm = self.stream.read(self.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.frame_length, pcm)
                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    print("Woke up!")
                    cmd = self.vc.stt(timeout=2)
                    if cmd:
                        print(cmd)
                        self.vc.handle_command(cmd)
        finally:
            self.cleanup()

    def cleanup(self):
        self.porcupine.delete()
        self.stream.close()
        self.pa.terminate()
