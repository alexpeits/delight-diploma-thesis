from flask import Flask
from flask_socketio import SocketIO, send
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
mqttc = mqtt.Client()

@socketio.on('mqtt/connect')
def test_connect():
    print 'asdf'

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app,
                 debug=True,
                 host='0.0.0.0',
                 port=8000)