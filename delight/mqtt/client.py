"""
MQTT client creation
~~~~~~~~~~~~~~~~~~~~

"""

import paho.mqtt.client as mqtt

from delight.config import MQTTConfig


mqttc = mqtt.Client()
mqttc.connect(MQTTConfig.HOST, MQTTConfig.PORT, 60)
mqttc.loop_start()
