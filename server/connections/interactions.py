from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from typing import List
from flask import current_app as app
from ..functions.db import statusTable
from ..functions.commandHandler import dbCommands
from ..commands.command import Command
import json
from flask_socketio import emit
default_tool = [{
    "type": "function",
    "function": {
        "name": "get_info_tool",
        "description": "Obtiene informacion de otro tool/function/comando solo o en conjunto",
        "parameters": {
            "type": "object",
            "properties": {
                "tools": {
                    "type": "array",
                    "description": "Nombre/s del/os tool/s",
                    "items": {
                        "type": "string"
                    }
                },
                "only_desc":{
                    "type": "boolean",
                    "description": "True: Solo descripcion, False: se añade al tools de OpenAI, Default: False",
                }
            },
            "required": ["tool"]
        }
    }
}]

class client_updater:
    process_id: str
    content = ""
    def __init__(self, process_id):
        self.process_id = process_id
    def update_content(self, content):
        self.content += content
        emit('chunks', {"process_id": self.process_id, "content": self.content})
    def add_messages(self, messages):
        emit('add_messages', {"process_id": self.process_id, "messages": messages})

MAX_CALLS = 5
system_message_content: str = ""
def get_system_message():
    return {
        "role": "system",
        "content": [{
            "type": "text",
            "text": system_message_content
        }]
    }
def has_system_message(messages: list[dict]) -> bool:
    return any([msg["role"] == "system" for msg in messages])

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(2))
def get_response_from_openai(messages, process_id, table: statusTable =None, tools=None, tool_choice=None, model="gpt-3.5-turbo"):
    global system_message_content
    client: OpenAI = OpenAI(api_key=app.config["OPENAI_API_KEY"])
    default_tool_name = default_tool[0]["function"]["name"]
    
    commands = dbCommands(app)
    all_tools = commands.getToolsNames()
    client_updater_instance = client_updater(process_id)
    print("All tools: ", all_tools)
    import traceback
    try:
        system_message = list(filter(lambda x: x['role'] == 'system', messages))
        system_message_content = f" Llama a herramienta {default_tool_name} para poder tener informacion y usar estos tools {",".join(all_tools) }  | Si no hay un tool que satisfaga no busques, solo responde segun conozcas | No ejecutes si no te lo piden"
        if system_message:
            system_message = system_message[0]
            system_message_content = system_message["content"][0]["text"] + system_message_content
            system_message["content"][0]["text"] = system_message_content
            system_message = [system_message]
    except Exception as e:
        print(f"Error al obtener mensaje del sistema: {e}")
        system_message = [get_system_message()]
        traceback.print_exc()
    
    non_system_messages = list(filter(lambda x: x['role'] != 'system', messages))
    last_10_non_system_messages = non_system_messages[-10:]
    messages = system_message + last_10_non_system_messages
    def update_status(**kwargs):
        if table:
            table.update_status(process_id=process_id, **kwargs)
    update_status(preview="...")
    try:
        messages = get_responses(client, messages, model, commands, client_updater_instance)
        print(messages)
        messages[0]["content"][0]["text"] = client_updater_instance.content
        client_updater_instance.add_messages(messages)
        update_status(status="completed", response=client_updater_instance.content, preview="")
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        print(f"Error: {error_type} - {error_message}")
        
        update_status(status="error", error=f"{error_type}: {error_message}")
        print(f"Unable to generate ChatCompletion response due to {error_type}")
        return str(e)

def handle_tool_calls(delta, tool_calls, current_tool_call):
    if delta.tool_calls:
        print("delta.tool_calls: ", delta.tool_calls)
        for tool_call in delta.tool_calls:
            if hasattr(tool_call, "id"):
                id = tool_call.id
                if id: 
                    print("Tool call id: ", id)
                    if current_tool_call:
                        tool_calls.append(current_tool_call)
                    current_tool_call = toolBody()
                    copy_id = f"{id}"
                    current_tool_call.id = copy_id
                    print("Tool vars: ", vars(current_tool_call))
                    
            if hasattr(tool_call, "function"):
                if hasattr(tool_call.function, "name"):
                    name = tool_call.function.name
                    if name: current_tool_call.function.name += name
                if hasattr(tool_call.function, "arguments"):
                    arguments = tool_call.function.arguments
                    if arguments != None:
                        current_tool_call.function.arguments += arguments
    return tool_calls, current_tool_call
def handle_tool_execution(tool, commandsDB):
    tools = []
    tool_body_response_content = ""
    tool_name = tool.function.name
    try:
        tool_parameters = json.loads(tool.function.arguments)
    except Exception as e:
        error_message = f"Error al obtener parametros de la herramienta {tool_name}: {e}"
        tool_body_response_content = error_message[:100]
        return tool_body_response_content, tools

    try:
        if tool_name == "get_info_tool":
            tools_list = tool_parameters.get("tools")
            only_desc = tool_parameters.get("only_desc", False)
            if tools_list:
                tools_info = commandsDB.get_tools_info(tools_list)
                if only_desc:
                    tool_body_response_content = ",".join([tool["name"] + " - " + tool["description"] for tool in tools_info]) 
                else:
                    tools = default_tool + tools_info
                    tool_body_response_content = "Comandos obtenidos correctamente"         
            else:
                tool_body_response_content = "No se especificaron herramientas"
        else:
            if commandsDB.exists(tool_name):
                commandClass: Command = commandsDB.getCommandClass(tool_name)
                commandClass = commandClass()
                tool_body_response_content = commandClass.execute(**tool_parameters)
                if tool_body_response_content == None:
                    tool_body_response_content = "Ejecutado correctamente sin respuesta"
            else:
                tool_body_response_content = f"Tool {tool_name} no encontrado en DB"
    except Exception as e:
        full_message = f"Error al ejecutar la herramienta {tool_name}: {e}"
        print(full_message)
        tool_body_response_content = full_message[-100:]
    return tool_body_response_content, tools
class toolFunction:
    name: str = ""
    arguments: str = ""
class toolBody:
    id: str = ""
    function: toolFunction
    def __init__(self):
        self.function = toolFunction()

def clean_message_tools(messages):
    """Elimina los tools iniciales 0->... hasta toparse con una respuesta de assistant o user, ignorando system, a partir de eso toma los siguientes messages, con el fin de no tener tools sin tool_calls"""
    system_messages  = list(filter(lambda x: x['role'] == 'system', messages))
    messages  = list(filter(lambda x: x['role'] != 'system', messages))
    for i, message in enumerate(messages):
        if message["role"] == "assistant" or message["role"] == "user":
            return system_messages + messages[i:]
    return system_messages
def get_responses(client: OpenAI, messages,model,commandsDB: dbCommands,cui: client_updater, tools=default_tool) -> list[dict]:
    print("Messages: ", messages)
    messages = clean_message_tools(messages)
    print("Messages cleaned: ", messages)
    print("Tools listed: ", tools)
    # TODO: add error messages
    try:
        body_response = {
            "role": "assistant",
            "content": [{
                "type": "text",
                "text": "..."
            }],
        }
        body_response_content_zero = body_response["content"][0]
        tool_calls: List[toolBody] = []
        tools_responses = []
        current_tool_call: toolBody = None

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
            tools=tools,
            stream=True,
        )
    except Exception as e:
        text = f"Error al obtener respuesta de OpenAI: {e}"
        print(text)
        body_response_content_zero["text"] = text[:100]
        return [body_response]

    try:
        streaming_content = ""
        for chunk in response:
          msg = chunk.choices[0]
          #print(msg)
          if hasattr(msg, "delta") and msg.delta:
            delta = msg.delta
            if hasattr(delta, "finish_reason"):
                finish_reason = delta.finish_reason
                if finish_reason is not None:
                    if finish_reason == "tool_calls":
                        print("Tool calls: ", tool_calls)
                    break
            if hasattr(delta, "content"):
                content = delta.content
                if content:
                    cui.update_content(content)
                    streaming_content += content
                    body_response_content_zero["text"] = streaming_content 
            if delta.tool_calls:
                tool_calls, current_tool_call = handle_tool_calls(delta, tool_calls, current_tool_call)
        if current_tool_call:
            tool_calls.append(current_tool_call)            
    except Exception as e:
        text = f"Error chunks: {e}"
        print(text)
        body_response_content_zero["text"] = text[:100]
        return [body_response]
    new_messages = [body_response]
    print(response)
    try:
        tool_calls = tool_calls[-MAX_CALLS:]
        if tool_calls:
            print("Tool calls: ", tool_calls)
            body_response["tool_calls"] = [{"id": t.id, "function": {"name": t.function.name, "arguments": t.function.arguments}, "type": "function"} for t in tool_calls]
            
            for tool in tool_calls:
                tool_body_response = {
                    "role": "tool",
                    "content": "",
                    "tool_call_id": tool.id,
                    "name" : tool.function.name
                }
                tool_body_response_content,_ = handle_tool_execution(tool, commandsDB)
                if len(_): tools = _
                tool_body_response["content"] = tool_body_response_content
                tools_responses.append(tool_body_response)
    except Exception as e:
        text = f"Error al ejecutar comandos: {e}"
        print(text)
        body_response_content_zero["text"] = text[:100]
    try:
        messages = messages[-5:]
        if not has_system_message(messages):
            messages = [get_system_message()] + messages
        # si la respuesta de todos los tools son "Ejecutado correctamente sin respuesta" entonces no se envia final_response
        final_response = []
        new_messages += tools_responses
        print("Tools call", tool_calls)
        print("Tools responses", tools_responses)
        if len(tool_calls):
            if not all([tool["content"] == "Ejecutado correctamente sin respuesta" for tool in tools_responses]) or any([tool["name"] == "get_info_tool" for tool in tools_responses]):
                final_response = get_responses(client, messages + new_messages, model, commandsDB,cui, tools)
            else:
                body_response_content_zero["text"] = "Comandos ejecutados correctamente"
                if cui.content == "":
                    cui.update_content("Comandos ejecutados correctamente")
    except Exception as e:
        text = f"Error al realizar llamadas recursivas: {e}"
        print(text)
        body_response_content_zero["text"] = text[:100]    

    print("Final response: ", new_messages + final_response)
    return new_messages + final_response