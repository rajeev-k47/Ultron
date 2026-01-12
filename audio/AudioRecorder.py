import sounddevice as sd
import soundfile as sf
import threading
import time
import os
from datetime import datetime

AUDIO_DIR = "records"
SAMPLE_RATE = 16000
CHANNELS = 1
SEGMENT_SECONDS = 300
RETENTION_DAYS = 0.5

os.makedirs(AUDIO_DIR, exist_ok=True)


class AudioRecorder:
    def __init__(self):
        self.file = None
        self.start_time = 0
        self.running = True
        self.lock = threading.Lock()
        self._open_new_file()

        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            device=0,
            callback=self._callback,
        )
        self.stream.start()

        threading.Thread(target=self._rotate_loop, daemon=True).start()

    def _open_new_file(self):
        with self.lock:
            if self.file:
                self.file.flush()
                self.file.close()

            name = datetime.now().strftime("record_%Y%m%d_%H%M%S.wav")
            path = os.path.join(AUDIO_DIR, name)

            self.file = sf.SoundFile(
                path,
                mode="w",
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                subtype="PCM_16",
            )
            self.start_time = time.time()
            self._cleanup()

    def _cleanup(self):
        cutoff = time.time() - RETENTION_DAYS * 86400
        for f in os.listdir(AUDIO_DIR):
            if not f.endswith(".wav"):
                continue
            path = os.path.join(AUDIO_DIR, f)
            if os.path.getmtime(path) < cutoff:
                os.remove(path)

    def _rotate_loop(self):
        while self.running:
            if time.time() - self.start_time >= SEGMENT_SECONDS:
                self._open_new_file()
            time.sleep(1)

    def _callback(self, indata, frames, time_info, status):
        if status:
            print(status)
        with self.lock:
            if self.file:
                self.file.write(indata.copy())

    def stop(self):
        self.running = False
        self.stream.stop()
        self.stream.close()
        with self.lock:
            if self.file:
                self.file.flush()
                self.file.close()


audio_recorder = AudioRecorder()
