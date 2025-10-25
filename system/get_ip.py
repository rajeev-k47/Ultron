import socket
import fcntl
import struct

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        packed = fcntl.ioctl(
            s.fileno(),
            0x8915, 
            struct.pack('256s', "wlan0".encode('utf-8'))
        )[20:24]
        return socket.inet_ntoa(packed)
    except OSError
        return None

