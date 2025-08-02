import RPi.GPIO as GPIO
import time
import random
import threading
import sounddevice as sd
import numpy as np


class Decor:
    def __init__(self, pin, state):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        self.pin = pin
        self._setup_mic()
        self._running = False
        self._thread = None
        self.pwm = GPIO.PWM(self.pin, 100)
        self.stream = None
        self.state = state
        self.setmode(self.state.load_state().get("decor", 0))

    def _setup_mic(self):
        self.sample_rate = 44100
        self.block_size = 1024

    def cleanup(self):
        self.stop()
        GPIO.cleanup(self.pin)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def stop(self):
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join()
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.pwm.stop()

    def _run_pattern(self, func, *args):
        self.stop()
        self._running = True
        self._thread = threading.Thread(target=func, args=args, daemon=True)
        self._thread.start()

    def setmode(self, mode, interval=0.5):
        self.state.save_state({"decor": mode})
        if mode == 0:
            self._run_pattern(self._blink, interval)
        elif mode == 1:
            self._run_pattern(self._fast_blink)
        elif mode == 2:
            self._run_pattern(self._fade_effect)
        elif mode == 3:
            self._run_pattern(self._random_blink)
        elif mode == 4:
            self._run_pattern(self._music_reactive)
        else:
            self.stop()

    def _blink(self, interval):
        while self._running:
            self.on()
            time.sleep(interval)
            self.off()
            time.sleep(interval)

    def _fast_blink(self):
        while self._running:
            self.on()
            time.sleep(0.1)
            self.off()
            time.sleep(0.1)

    def _fade_effect(self):
        self.pwm.start(0)
        try:
            while self._running:
                for duty_cycle in range(0, 101, 5):
                    if not self._running:
                        break
                    self.pwm.ChangeDutyCycle(duty_cycle)
                    time.sleep(0.05)
                for duty_cycle in range(100, -1, -5):
                    if not self._running:
                        break
                    self.pwm.ChangeDutyCycle(duty_cycle)
                    time.sleep(0.05)
        finally:
            self.pwm.stop()

    def _random_blink(self):
        while self._running:
            self.on()
            time.sleep(random.uniform(0.05, 0.5))
            self.off()
            time.sleep(random.uniform(0.05, 0.5))

    def _music_reactive(self):
        self.pwm.start(0)

        def audio_callback(indata, frames, t, st):
            if not self._running:
                return
            volume_norm = np.linalg.norm(indata)
            noise_floor = 0.8
            if volume_norm < noise_floor:
                duty_cycle = 0
            else:
                scaled = (volume_norm - noise_floor) * 5
                duty_cycle = min(100, max(0, int(scaled)))

            self.pwm.ChangeDutyCycle(duty_cycle)

        try:
            self.stream = sd.InputStream(
                callback=audio_callback,
                channels=1,
                samplerate=self.sample_rate,
                blocksize=self.block_size,
            )
            self.stream.start()
            while self._running:
                time.sleep(0.1)
        finally:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            self.pwm.stop()
