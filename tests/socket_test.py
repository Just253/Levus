import socketio

sio = socketio.Client()

model="gpt-3.5-turbo-0125"
messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "Tu nombre es LEVUS"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Que hora es"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "Son las 4:40pm"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Abre youtube"
        }
      ]
    }
]

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('new_message', {"model": model, "messages": messages})
@sio.on('error')
def on_error(data):
    print('error received with ', data)

@sio.on('update')
def on_update(data):
    print(data.get('preview'))

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.on('response_id')
def on_response(data):
    print('response received with ', data)

@sio.on('chunks')
def on_chunks(data):
    print(data,flush=True)

try:
    sio.connect('http://localhost:5000')
    sio.wait()
except KeyboardInterrupt:
    print("Interrupted by user, disconnecting...")
    sio.disconnect()