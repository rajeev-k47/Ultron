import speech_recognition as sr
import time


class VoiceCommands:
    def __init__(self, buzzer, headlight):
        self.recognizer = sr.Recognizer()
        self.buzzer = buzzer
        self.buzzer.mode = 1
        self.headlight = headlight

    def stt(self, timeout=5):
        try:
            mic = sr.Microphone()
            with mic as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            self.buzzer.alert()
            self.buzzer.mode = 0
            return None
        except AttributeError:
            print("AttributeError in VoiceCommands")
            self.buzzer.alert()
            self.buzzer.mode = 0
            return None
        except OSError as e:
            print("OSError:", e)
            self.buzzer.alert()
            self.buzzer.mode = 0
            return None

        try:
            text = self.recognizer.recognize_google(audio)
            self.buzzer.mode = 0
            return text.lower()
        except sr.WaitTimeoutError:
            self.buzzer.alert()
            self.buzzer.mode = 0
            return None
        except sr.UnknownValueError:
            self.buzzer.alert()
            self.buzzer.mode = 0
            return None
        except sr.RequestError:
            self.buzzer.alert()
            self.buzzer.mode = 0
            return None
        except Exception as e:
            print(e)
            self.buzzer.alert()
            self.buzzer.mode = 0
            return None

    def handle_command(self, cmd):
        if "turn on" in cmd:
            if "headlight" in cmd:
                self.headlight.status = 2
                self.headlight.on()
        elif "turn off" in cmd:
            if "headlight" in cmd:
                self.headlight.status = 2
                self.headlight.off()
        elif "toggle" in cmd:
            if "headlight mode" in cmd:
                self.headlight.status = 1
