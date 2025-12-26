import time
import serial

DEVICE = "/dev/serial0"
BAUDRATE = 9600


class Matrix:
    def __init__(self):
        self.mode = 0
        self.ser = None
        self.connect_serial()

    def connect_serial(self):
        while True:
            try:
                self.ser = serial.Serial(
                    DEVICE,
                    BAUDRATE,
                    timeout=1
                )
                return
            except serial.SerialException:
                self.ser = None
                time.sleep(1)

    def get_mode(self):
        return self.mode

    def write(self, value):
        self.mode = value

        if self.ser is None or not self.ser.is_open:
            self.connect_serial()

        try:
            self.ser.write(f"{value}\n".encode())
            self.ser.flush()

        except serial.SerialException:
            try:
                self.ser.close()
            except Exception:
                pass
            self.ser = None
            self.connect_serial()

