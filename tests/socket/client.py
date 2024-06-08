# client.py
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('message', 'Hello, server!')

@sio.event
def message(data):
    print('Message received:', data)

sio.connect('http://localhost:5000')
sio.wait()