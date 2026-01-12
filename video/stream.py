import cv2
import threading
import time
import os
from datetime import datetime

RECORD_DIR = "records"
SEGMENT_SECONDS = 300  # 5min max
RETENTION_DAYS = 0.5  # 1/2day recordings only
FPS = 20

os.makedirs(RECORD_DIR, exist_ok=True)


class VideoStream:
    def __init__(self, index=0):
        self.camera = cv2.VideoCapture(index)
        self.frame = None
        self.lock = threading.Lock()
        self.running = True

        self.writer = None
        self.segment_start = 0

        self._open_new_file()
        threading.Thread(target=self._update, daemon=True).start()

    def _open_new_file(self):
        if self.writer:
            self.writer.release()

        name = datetime.now().strftime("record_%Y%m%d_%H%M%S.avi")
        path = os.path.join(RECORD_DIR, name)

        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"XVID")

        self.writer = cv2.VideoWriter(path, fourcc, FPS, (width, height))
        self.segment_start = time.time()
        self._cleanup_old_files()

    def _cleanup_old_files(self):
        cutoff = time.time() - RETENTION_DAYS * 86400
        for f in os.listdir(RECORD_DIR):
            path = os.path.join(RECORD_DIR, f)
            if os.path.isfile(path) and os.path.getmtime(path) < cutoff:
                os.remove(path)

    def _update(self):
        while self.running:
            ok, frame = self.camera.read()
            if not ok:
                continue

            self.writer.write(frame)
            if time.time() - self.segment_start >= SEGMENT_SECONDS:
                self._open_new_file()

            ret, buffer = cv2.imencode(".jpg", frame)
            with self.lock:
                self.frame = buffer.tobytes()

            time.sleep(1 / FPS)

    def get_frame(self):
        with self.lock:
            return self.frame

    def stop(self):
        self.running = False
        if self.writer:
            self.writer.release()
        self.camera.release()


video_stream = VideoStream()
