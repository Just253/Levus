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
          "text": "Que hora fue hace medio dia"
        }
      ]
    }
  ]

chat_url = "http://localhost:5000/api/chat"
response = requests.post(chat_url, json={"model": model, "messages": messages})
print(response.json())