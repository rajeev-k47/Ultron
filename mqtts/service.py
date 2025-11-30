import paho.mqtt.client as mqtt
import json

class mqtts:
    def __init__(self,tubelight)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect("f9ad263f5ab74b5793f827aba57736a3.s1.eu.hivemq.cloud", 1883, 60)
        self.topic = "ultron/data"
        self.tubelight=tubelight
    
    def publish_status(self):
        while True:
            payload = {
                "tubelight": self.tubelight.state if hasattr(self.tubelight, "state") else 0,
            }
            mqtt_client.publish(topic, json.dumps(payload))
            time.sleep(1)

