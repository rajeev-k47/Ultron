import subprocess
import pyttsx3


class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("voice", "english")

    def speak(self, text: str):
        # subprocess.call(["espeak", "-ven-us+f5", "-s180", text])
        self.engine.say(text)
        self.engine.runAndWait()
