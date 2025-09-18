import os
import time
import serial
import subprocess


DEVICE = "/dev/rfcomm0"
BAUDRATE = 9600
HC05_MAC = "00:25:02:00:37:83"


class DoorReader:
    def __init__(self, tubelight):
        self.tubelight = tubelight

    def bluetooth_connect(self):
        try:
            subprocess.run(
                ["sudo", "rfcomm", "release", "0"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # subprocess.run(["bluetoothctl", "connect", HC05_MAC], check=False)
            subprocess.run(["sudo", "rfcomm", "bind", "0", HC05_MAC], check=True)

            print("Bound to /dev/rfcomm0")
        except Exception as e:
            print(f"Connection failed: {e}")

    def connect_serial(self):
        while True:
            if not os.path.exists(DEVICE):
                self.bluetooth_connect()

            if os.path.exists(DEVICE):
                try:
                    ser = serial.Serial(DEVICE, BAUDRATE, timeout=1)
                    print(f"Connected to {DEVICE} at {BAUDRATE} baud")
                    return ser
                except serial.SerialException as e:
                    print("Serial Exception")
                except Exception as e:
                    print(f"Connection failed: {e}")

            time.sleep(3)

    def read(self):
        ser = self.connect_serial()
        while True:
            try:
                value = ser.readline().decode("utf-8").strip()
                print(value)
                # if value == "0":
                #     print("IN1")
                #     self.tubelight.off()
                # else:
                #     print("IN2")
                #     self.tubelight.on()

            except serial.SerialException as e:
                ser.close()
                ser = self.connect_serial()
