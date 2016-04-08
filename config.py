import os
import paho.mqtt.client as mqtt
import MySQLdb
import json
from .extern import NRF24

"""
The DIM_TABLE constant holds the value that the dimmer has to
be set in order to achieve a specific light intensity level.
e.g. for i=20% we need DIM_TABLE[i/10]=460

"""

basedir = os.path.abspath(os.path.dirname(__file__))
dim_dir = os.path.join(basedir, 'plots', 'dim_table.json')
with open(dim_dir, 'r') as f:
    dim_table_ints = json.loads(f.read())
DIM_TABLE = [str(i) for i in dim_table_ints]
GET_READ = '01' # command to request reading from a sensor
GATEWAY_ADDR = '01' # our address
DIM_MIN = 50
DIM_MAX = 600
DIM_INCR_UP = '02' # command to request an intensity change by increment up..
DIM_INCR_DOWN = '01' # .. and increment down
DIM_TO_VAL = '04' # command to dim to a specific value
THRESH_MIN = 0
THRESH_MAX = 800
NODE_TIMEOUT = 1.5 # max wait time to receive reading in seconds
OPERATION_CYCLE = 20 # duration of each cyle of operation in seconds
MAX_INCR = 40

CONFIGPATH = os.path.join(basedir, 'thesis.conf')
GUI_CONF_DIR = os.path.join(basedir, 'web_server', 'data')
GUI_CONF_PATH = os.path.join(GUI_CONF_DIR, 'gui.conf')
SCT_TRAIN_DATA_DIR = os.path.join(basedir, 'sct_train_data.txt')
SEND_DELAY = 1.0/2

# MySQL setup
SQL_HOST = 'localhost'
SQL_USER = 'root'
SQL_PW = os.environ.get('MYSQL_PW')
SQL_DB = 'thesis'
SQL_TABLE = 'power'
# instantiation
db = MySQLdb.connect(host=SQL_HOST, user=SQL_USER,
                     passwd=SQL_PW, db=SQL_DB)
cur = db.cursor()

# MQTT setup
MQTT_HOST = 'localhost'
MQTT_PORT = 1884
MQTT_BASE = 'thesis/power/'
# instantiation
mqttc = mqtt.Client()
mqttc.connect(MQTT_HOST, MQTT_PORT, 60)
mqttc.loop_start()

# NRF24 setup-instantiation
pipes = [[0xf0, 0xf0, 0xf0, 0xf0, 0xe1],
		 [0xf0, 0xf0, 0xf0, 0xf0, 0xd2]]
radio = NRF24()
radio.begin(0, 0, 25, 18) #set gpio 25 as CE pin
radio.setRetries(5, 15)
radio.setPayloadSize(32)
radio.enableDynamicPayloads()
radio.setChannel(0x4c)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(False)
radio.setCRCLength(NRF24.CRC_8)
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.startListening()
radio.stopListening()
#radio.printDetails()
pipe = [0]
