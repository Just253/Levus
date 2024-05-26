## Chat.py

```mermaid
sequenceDiagram
    participant GUI
    participant chat.py
    participant interaction.py
    participant OPENAI
    participant command.py
    GUI->>chat.py: User input
    chat.py->>interaction.py: User input
    interaction.py->>OPENAI: User input
    OPENAI->>interaction.py: Bot response
    interaction.py->>chat.py: If not command response
    chat.py->>GUI: Bot response
    interaction.py->>command.py: If command response
    command.py->>interaction.py: Command response
    interaction.py->>chat.py: Command response
    chat.py->>GUI: Command response
```

# TODO
### chat.py response
```json	
    {
        "state":"correct",
        "process_id": "12312312"
    }
```

### routes/process
```json
    {
        "state": "completed",
        "process_id": "12312312",
        "response": "Son las 12:00"
    }
```
```json
    {
        "state": "pending",
        "process_id": "12312312",
        "preview": "Son las"
    }
```
```json
    {
        "state": "error",
        "process_id": "12312312",
        "preview": "Son las",
        "error": "No se pudo completar la solicitud"
    }
```