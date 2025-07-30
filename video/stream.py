import cv2


class VideoStream:
    def __init__(self):
        self.frame = None
        self.buffer = None

    def generate_frames(self, camera):
        while True:
            success, frame = camera.read()
            if not success:
                break
            ret, buffer = cv2.imencode(".jpg", frame)
            self.frame = frame
            self.buffer = buffer.tobytes()
            yield (
                b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + self.buffer + b"\r\n"
            )
