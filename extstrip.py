#!/usr/bin/env python3
import time
import numpy as np
import sounddevice as sd
from rpi_ws281x import PixelStrip, Color
import math
import sys
import threading

LED_COUNT = 100
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

strip = PixelStrip(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
    LED_BRIGHTNESS, LED_CHANNEL
)
strip.begin()

SAMPLE_RATE = 44100
BUFFER_SIZE = 1024
SENSITIVITY = 10

MODE = 4
current_led_count = 0
solid_color = Color(255, 0, 0)


def plasma_wave(wait_ms=20):
    start_time = time.time()
    while MODE == 4:
        current_time = time.time() - start_time
        for i in range(strip.numPixels()):
            pos = i / strip.numPixels()
            value1 = math.sin(pos * 8 + current_time * 2)
            value2 = math.sin(pos * 15 + current_time * 1.3)
            value3 = math.sin(pos * 23 + current_time * 0.7)

            r = int(128 + 127 * math.sin(value1 + current_time))
            g = int(128 + 127 * math.sin(value2 + current_time + 2))
            b = int(128 + 127 * math.sin(value3 + current_time + 4))

            strip.setPixelColor(i, Color(r, g, b))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def vortex_spiral(wait_ms=15):
    angle = 0
    while MODE == 5:
        angle += 0.1
        for i in range(strip.numPixels()):
            pos = i / strip.numPixels()
            spiral_angle = angle + pos * 10
            radius = 0.5 + 0.5 * math.sin(pos * 5 + angle)

            r = int(128 + 127 * math.sin(spiral_angle))
            g = int(128 + 127 * math.sin(spiral_angle + 2))
            b = int(128 + 127 * math.sin(spiral_angle + 4))

            fade = radius
            r = int(r * fade)
            g = int(g * fade)
            b = int(b * fade)

            strip.setPixelColor(i, Color(r, g, b))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def set_strip_gradient(target_led_count):
    global current_led_count
    if target_led_count > current_led_count:
        current_led_count = target_led_count
    elif target_led_count < current_led_count:
        current_led_count -= 2

    for i in range(strip.numPixels()):
        if i < current_led_count:
            frac = i / max(current_led_count - 1, 1)
            r = int(255 * abs(np.sin(frac * np.pi)))
            g = int(255 * abs(np.sin(frac * np.pi + 2)))
            b = int(255 * abs(np.sin(frac * np.pi + 4)))
            strip.setPixelColor(i, Color(r, g, b))
        else:
            strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()


def rainbow_cycle(wait_ms=10, iterations=1):
    for j in range(256 * iterations):
        if MODE != 2:
            break
        for i in range(strip.numPixels()):
            pixel_index = (i * 256 // strip.numPixels()) + j
            strip.setPixelColor(i, wheel(pixel_index & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def color_wipe(color, wait_ms=30):
    for i in range(strip.numPixels()):
        if MODE != 1:
            break
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def smooth_fade(wait_ms=20):
    while MODE == 3:
        for j in range(256):
            if MODE != 3:
                break
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((i + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)


def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def audio_callback(indata, a, b, c):
    if MODE != 0:
        return
    volume_norm = np.linalg.norm(indata) * SENSITIVITY
    leds_to_light = int(np.clip(volume_norm, 0, LED_COUNT))
    set_strip_gradient(leds_to_light)


def switch_mode(new_mode):
    global MODE
    MODE = new_mode
    print(f"Switched to mode: {MODE}")


def main():
    global MODE
    print("Available Modes: AUDIO, COLOR_WIPE, RAINBOW, FADE, PLASMA, VORTEX")

    threading.Thread(target=stdin_listener, daemon=True).start()
    while True:
            if MODE == 1:
                color_wipe(Color(0, 0, 255))
            elif MODE == 2:
                rainbow_cycle(wait_ms=5)
            elif MODE == 3:
                smooth_fade(wait_ms=15)
            elif MODE == 4:
                plasma_wave()
            elif MODE == 5:
                vortex_spiral()
            else:
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(0, 0, 0))
                    strip.show()


def stdin_listener():
    global MODE
    for line in sys.stdin:
        new_mode = line.strip()
        if new_mode.isdigit():
            MODE = int(new_mode)  # convert to int
        else:
            MODE = new_mode.upper()  # for string modes like PLASMA
        print(f"[Ultron] Mode changed to {MODE}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
