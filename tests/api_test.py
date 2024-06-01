import requests

model="gpt-3.5-turbo-0125",
messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "Eres un reloj, dices la hora, no importa si no es verdad"
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
          "text": "Quien era napoleon, en 3 oraciones"
        }
      ]
    }
  ]

chat_url = "http://localhost:5000/chat"
response = requests.post(chat_url, json={"model": model, "messages": messages})
print(response.status_code)
print(response.json())

process_id = response.json().get('process_id')
status_url = f"http://localhost:5000/status/{process_id}"
while True:
    response = requests.get(status_url)
    if response.json().get('status') == 'completed':
        break
    print(response.json())
print(response.json())