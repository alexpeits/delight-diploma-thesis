"""
MQTT broker utilities
~~~~~~~~~~~~~~~~~~~~~

"""

from delight.mqtt.client import mqttc
from delight.config import MQTTConfig


def create_topic_uri(topic):
    """Create the full topic uri by applying the base."""
    base = MQTTConfig.TOPIC_BASE
    if base.endswith('/'):
        return ''.join([base, topic])
    return '/'.join([base, topic])


def publish(topic, data):
    """Publish data to a given topic in the MQTT server."""
    topic_uri = create_topic_uri(topic)
    mqttc.publish(topic_uri, str(data), 1, retain=True)
