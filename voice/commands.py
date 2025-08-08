from gen_ai.groq_handler import Groqy
import speech_recognition as sr
import time
from audio import Speaker


class VoiceCommands:
    def __init__(self, buzzer, headlight, tubelight, state, groqy):
        self.recognizer = sr.Recognizer()
        self.buzzer = buzzer
        self.buzzer.mode = 1
        self.headlight = headlight
        self.speaker = Speaker()
        self.tubelight = tubelight
        self.state = state
        self.groqy = groqy

    def stt(self, timeout=2):
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
                self.state.update_state("headlight", 2)
                self.speaker.speak("Headlight turned on")
        elif "turn off" in cmd:
            if "headlight" in cmd:
                self.headlight.status = 2
                self.headlight.off()
                self.state.update_state("headlight", 2)
                self.speaker.speak("Headlight turned off")
        elif "toggle" in cmd:
            if "headlight mode" in cmd:
                self.headlight.status = 1
                self.state.update_state("headlight", 1)
                self.speaker.speak("Headlight mode toggled")
        elif "tubelight" in cmd:
            self.tubelight.toggle()
            self.speaker.speak("Tubelight toggled")
        else:
            self.groqy.speak(cmd)
