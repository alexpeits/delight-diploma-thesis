import time
from math import floor, ceil
import os
from ..config import *


def mqtt_publish(topic, data):
    mqttc.publish(''.join([MQTT_BASE, topic]), "%s" % data, 1, retain=True)


def db_insert(sensor_id, sensor_value):
    min_val = floor(sensor_value)
    max_val = ceil(sensor_value)
    sensor_value = min_val if (sensor_value-min_val<=max_val-sensor_value) else max_val
    sensor_value = int(sensor_value)
    sql_date = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    sql = """INSERT INTO power (datetime,sensor_id,sensor_value) VALUES (%s,%s,%s)"""

    try:
        #print "Writing to database..."
        cur.execute(sql, (sql_date, sensor_id, sensor_value))
        db.commit()
        #print "Write complete!"

    except:
        # Rollback in case there is any error
        db.rollback()
        #print "Failed writing to database"
