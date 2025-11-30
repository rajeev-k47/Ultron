import paho.mqtt.client as mqtt
import json
import time
from system.get_ip import get_local_ip


class mqtts:
    def __init__(self, user, passw, tubelight, serialcomm):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.tls_set()
        self.mqtt_client.username_pw_set(user, passw)
        self.mqtt_client.connect(
            "f9ad263f5ab74b5793f827aba57736a3.s1.eu.hivemq.cloud", 8883, 60
        )
        self.topic = "ultron/data"
        self.tubelight = tubelight
        self.ip = get_local_ip()
        self.serialcomm = serialcomm

    def publish_status(self):
        while True:
            payload = {
                "tubelight": 1 if self.tubelight.is_on else 0,
                "ip": self.ip,
                "temp": self.serialcomm.temp,
                "hum": self.serialcomm.hum,
                "raw": self.serialcomm.raw,
            }
            self.mqtt_client.publish(self.topic, json.dumps(payload))
            time.sleep(1)
