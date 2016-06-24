"""
MQTT client creation
~~~~~~~~~~~~~~~~~~~~

"""

import paho.mqtt.client as mqtt

from delight.config import MQTTConfig


mqtt_client = mqtt.Client()
mqtt_client.connect(MQTTConfig.HOST, MQTTConfig.PORT, 60)
mqtt_client.loop_start()
