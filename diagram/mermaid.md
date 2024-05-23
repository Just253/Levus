```mermaid
graph TD
    A[Inicio] --> B[Leer config.json]
    B --> C[Iniciar start.bash/start.bat]
    C --> D{¿Es Linux o Windows?}
    D -->|Linux| E[Iniciar servidor y GUI con start.bash]
    D -->|Windows| F[Iniciar servidor y GUI con start.bat]
    E --> G[Servidor maneja comandos, conexión con IA, reconocimiento, etc.]
    F --> G
    G --> H[Java GUI simplifica la interacción]
```

# GUI
```mermaid
graph TD
    A[Inicio]
    B[Pide a la función 'Verificar y Obtener método de interacción' el método disponible]
    C{¿Método de interacción disponible?}
    G[Esperar acción]
    H{¿Interacción?}
    I[Reconocer gestos y voz]
    K[Enviar interacción al servidor]
    L[Recibir respuesta del servidor]
    M[Mostrar respuesta]
    

    A --> B
    B --> C
    C -->|No| B
    C -->|Sí| G
    G --> H
    H -->|No| G
    H -->|Sí| I
    I --> K
    K --> L
    L --> M
    M --> G

```
### Verificar y Obtener metodo de interacción 
Retorna  el método de interacción disponible.
```mermaid
graph TD
    A[Inicio] --> B[Leer config.json]
    B --> C{¿Método de interacción configurado?}
    C -->|Sí| D[Retornar método de interacción]
    C -->|No| E[Verificar micrófono y cámara]
    E --> E_microfono_verificar[Verificar micrófono]
    E_microfono_verificar --> E_microfono_disponible{¿Está disponible el micrófono?}
    E_microfono_disponible -->|No| E_microfono_rojo[Cambiar icono de micrófono a rojo y notificar al usuario]
    E_microfono_rojo --> E_microfono_verificar
    E_microfono_disponible -->|Sí| E_microfono_verde[Cambiar icono de micrófono a verde]
    E --> E_camara_verificar[Verificar cámara]
    E_camara_verificar --> E_camara_disponible{¿Está disponible la cámara?}
    E_camara_disponible -->|No| E_camara_rojo[Cambiar icono de cámara a rojo y notificar al usuario]
    E_camara_rojo --> E_camara_verificar
    E_camara_disponible -->|Sí| E_camara_verde[Cambiar icono de cámara a verde]
    E_microfono_verde --> F[Solicitar al usuario que realice una acción específica]
    E_camara_verde --> F
    F --> G{¿Acción realizada?}
    G -->|Sí| H[Establecer el método realizado como configurado y retornar]
    G -->|No| F
```

## Ordenamiento de la API
```mermaid
graph TD
    __init__.py --> __init__.pyDescripcion["Archivo vacio para que \npython reconozca el directorio \ncomo un paquete"]
    Server
    app.py
    app.pyDescripcion["Servidor con flask, \nautomaticamente importar class \nde los directorios de api/"]
    api/
    api/__init__.py["__init__.py"]
    
    api/routes/
    api/routes/__init__.py["__init__.py"]
    api/routes/chat.py["chat.py"]

    api/functions/
    api/functions/__init__.py["__init__.py"]
    api/functions/interaction.py["interaction.py"]




    commands/
    commands/__init__.py["__init__.py"]
    commands/command.py["command.py"]
    commands/command.pyDescripcion["Clase padre de los comandos"]
    nameCommand/
    nameCommand/__init__.py["__init__.py"]
    nameCommand/command.py["BotCommand.py"]
    nameCommand/command.pyDescripcion["Clase del comando nameCommand"]
    nameCommand/config.json["config.json"]
    nameCommand/config.jsonDescripcion["Configuración del \ncomando nameCommand \n(opcional)"]
    
    Server --> app.py
    app.py --> app.pyDescripcion
    Server --> api/
    api/ --> api/__init__.py

    Server --> commands/
    commands/ --> commands/__init__.py
    
    commands/ --> commands/command.py
    commands/command.py --> commands/command.pyDescripcion
    commands/ --> nameCommand/
    
    nameCommand/ --> nameCommand/__init__.py

    nameCommand/ --> nameCommand/command.py
    nameCommand/command.py --> nameCommand/command.pyDescripcion

    nameCommand/ --> nameCommand/config.json
    nameCommand/config.json --> nameCommand/config.jsonDescripcion


    api/ --> api/routes/
    api/routes/ --> api/routes/__init__.py
    api/routes/ --> api/routes/chat.py
     
    api/ --> api/functions/
    api/functions/ --> api/functions/__init__.py
    api/functions/ --> api/functions/interaction.py
    
```

# Class
```mermaid
classDiagram
    class Command{
        +String Name
        +String Description
        +String[] Keywords
        +execute()
        +getName()
        +getDescription()
    }
    class BotCommand{
        +execute()
    }
    Command <|-- BotCommand
```

# Se envia un json a la api/chat.py con el siguiente formato
```json
{
    messages: [
        {
            "content": "Hola",
            "role": "assitant"
        },
        {
            "content": "Hola",
            "role": "user"
        }
    ]
    model: "gpt4o"
}
```
chat.py se encarga de procesar con ayuda de interaccion.py el contenido del json y devolver una respuesta
```json
{
    response: "Hola, ¿en qué puedo ayudarte?",
}
```

Interaction.py tiene que indentificar el metodo de interaccion, si usa funciones externas por ejemplo:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use. Infer this from the users location.",
                    },
                },
                "required": ["location", "format"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_n_day_weather_forecast",
            "description": "Get an N-day weather forecast",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use. Infer this from the users location.",
                    },
                    "num_days": {
                        "type": "integer",
                        "description": "The number of days to forecast",
                    }
                },
                "required": ["location", "format", "num_days"]
            },
        }
    },
]
```

```python
messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
messages.append({"role": "user", "content": "What's the weather like today"})
chat_response = chat_completion_request(
    messages, tools=tools
)
assistant_message = chat_response.choices[0].message
messages.append(assistant_message)
assistant_message
```
Output:
```text
ChatCompletionMessage(content="I need to know your location to provide you with the current weather. Could you please specify the city and state (or country) you're in?", role='assistant', function_call=None, tool_calls=None)
```
 
```python	
messages.append({"role": "user", "content": "I'm in Glasgow, Scotland."})
chat_response = chat_completion_request(
    messages, tools=tools
)
assistant_message = chat_response.choices[0].message
messages.append(assistant_message)
assistant_message
```
Output:
```text
ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_Dn2RJJSxzDm49vlVTehseJ0k', function=Function(arguments='{"location":"Glasgow, Scotland","format":"celsius"}', name='get_current_weather'), type='function')])
```

Mas detalle en https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models