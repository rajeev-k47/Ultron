import serial

class SerialComm:
    def __init__(self):
        self.ser = serial.Serial(
        port="/dev/serial0",
            baudrate=9600,
            timeout=1
        )
        self.raw=0
        self.temp=0
        self.hum=0

    def read(self):
        while True:
            line = self.ser.readline().decode().strip()
            if not line:
                continue
    
            try:
                raw, temp, hum = line.split(",")
                self.raw = int(raw)
                self.temp = float(temp)
                self.hum = float(hum)
            except ValueError:
                pass

