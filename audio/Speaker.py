# import pyttsx3
from groq import Groq
import subprocess


class Speaker:
    def __init__(self, api_key):
        # self.engine = pyttsx3.init()
        # self.engine.setProperty("voice", "english")
        self.api_key = api_key
        self.speech_file_path = "speech.wav"
        self.client = Groq(api_key=self.api_key)

    def speak(self, text: str):
        # self.engine.say(text)
        # self.engine.runAndWait()
        try:
            response = self.client.audio.speech.create(
                model="playai-tts",
                voice="Cheyenne-PlayAI",
                input=text,
                response_format="wav",
            )
        except Exception as e:
            print(e)
            return

        response.write_to_file(self.speech_file_path)
        subprocess.call(["aplay", self.speech_file_path])
