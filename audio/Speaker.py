import subprocess


class Speaker:
    def __init__(self):
        pass

    def speak(self, text: str):
        subprocess.call(["espeak", "-ven-us+f5", "-s180", text])
