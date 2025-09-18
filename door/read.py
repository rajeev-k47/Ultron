import serial

ser = serial.Serial("/dev/rfcomm0", 9600, timeout=1)


class DoorReader:
    def read(self):
        while True:
            line = ser.readline().decode("utf-8").strip()
            if line:
                print(line)
