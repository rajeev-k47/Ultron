import paho.mqtt.client as mqtt
import json
import time
from system.get_ip import get_local_ip

class mqtts:
    def __init__(self,tubelight)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect("f9ad263f5ab74b5793f827aba57736a3.s1.eu.hivemq.cloud", 1883, 60)
        self.topic = "ultron/data"
        self.tubelight=tubelight
        self.ip = get_local_ip()
    
    def publish_status(self):
        while True:
            payload = {
                "tubelight": self.tubelight.state if hasattr(self.tubelight, "state") else 0,
                "ip": self.ip
            }
            self.mqtt_client.publish(self.topic, json.dumps(payload))
            time.sleep(1)

