from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from typing import List
from flask import current_app as app
from .db import statusTable
from .commandHandler import dbCommands
from ..commands.command import Command
import json, openai
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
                "to_use":{
                    "type": "boolean",
                    "description": "Si es true se usaran los tools de el parametro tools, si es false solo se obtendra informacion de los tools mencionados",
                }
            },
            "required": ["tool"]
        }
    }
}]

MAX_CALLS = 10

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(2))
def get_response_from_openai(messages, process_id, table: statusTable =None, tools=None, tool_choice=None, model="gpt-3.5-turbo"):
    client: OpenAI = OpenAI(api_key=app.config["OPENAI_API_KEY"])
    default_tool_name = default_tool[0]["function"]["name"]
    
    commands = dbCommands(app)
    all_tools = commands.getToolsNames()
    print("All tools: ", all_tools)
    system_message = list(filter(lambda x: x['role'] == 'system', messages))[0]
    system_message["content"][0]["text"] += f" Llama a herramienta {default_tool_name} para poder tener informacion y usar estos tools {",".join(all_tools) }  | Si no hay un tool que satisfaga no busques, solo responde segun conozcas | "
    print(system_message)
    non_system_messages = list(filter(lambda x: x['role'] != 'system', messages))
    last_10_non_system_messages = non_system_messages[-5:]
    
    messages = [system_message] + last_10_non_system_messages
    def update_status(**kwargs):
        if table:
            table.update_status(process_id=process_id, **kwargs)
    update_status(preview="...")
    try:
        check_if_call_tool, tools_called = send_message_tools_to_openai(client, messages, default_tool, update_status, commands)
        print("Check if call tool: ", check_if_call_tool)
        if tools_called != []:
            print("Tools called: ", tools_called)
            update_status(preview="Se llamaron herramientas\n...")
            messages = messages + check_if_call_tool
            update_status(preview=f"Ejecutando {tools_called}\n...")
            tools_called += default_tool
            responses_tools, _ = send_message_tools_to_openai(client, messages, tools_called, update_status, commands)
            if responses_tools:
                messages = messages + responses_tools
        else:
            update_status(preview="No se llamaron herramientas\n...")
        
        print("Messages: ", messages)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
            stream=True,
        )
        chunk_messages = ""
        for chunk in response:
            message = chunk.choices[0].delta.content
            if message != None:
                chunk_messages += message
                update_status(preview=chunk_messages)
        update_status(status="completed", response=chunk_messages, preview="")
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        print(f"Error: {error_type} - {error_message}")
        if isinstance(e, openai.error.Timeout):
            error_info = "OpenAI API request timed out"
        elif isinstance(e, openai.error.APIError):
            error_info = "OpenAI API returned an API Error"
        elif isinstance(e, openai.error.APIConnectionError):
            error_info = "OpenAI API request failed to connect"
        elif isinstance(e, openai.error.InvalidRequestError):
            error_info = "OpenAI API request was invalid"
        elif isinstance(e, openai.error.AuthenticationError):
            error_info = "OpenAI API request was not authorized"
        elif isinstance(e, openai.error.PermissionError):
            error_info = "OpenAI API request was not permitted"
        elif isinstance(e, openai.error.RateLimitError):
            error_info = "OpenAI API request exceeded rate limit"
        else:
            error_info = "An unexpected error occurred"
        
        update_status(status="error", error=f"{error_info}: {error_message}")
        print(f"Unable to generate ChatCompletion response due to {error_type}")
        return str(e)
    
def send_message_tools_to_openai (client: OpenAI, messages,tools_calling,fun_update_status, commandsDB: dbCommands):
    fun_update_status(preview="Obteniendo herramientas\n...")
    print("DB Commands: ", commandsDB)
    response = None
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.3,
            tools=default_tool if not tools_calling else tools_calling,
        )
        print(response)
    except Exception as e:
        print(f"Ocurrió un error al llamar a la API de OpenAI: {e}")
    responses = []
    tools_to_call = []
    fun_update_status (preview="Iniciando while\n...")
    try:
        tools_calls: List[ChatCompletionMessageToolCall] = response.choices[0].message.tool_calls
    except Exception as e:
        print(f"Error al obtener las herramientas llamadas: {e}")
        tools_calls = None
    print("Tools calls: ", tools_calls)
    print("Iniciando while")
    if tools_calls != None:
        responses = [{
            "role": "assistant",
            "content": None,
            "tool_calls": [{"id": t.id, "function": {"name": t.function.name, "arguments": t.function.arguments}, "type": "function"} for t in tools_calls]
        }]
        tryes = 0
        for tool_call in tools_calls:
            if tryes >= MAX_CALLS:
                break
            tool_id = tool_call.id
            tool_name = tool_call.function.name
            tool_response_object = {
                "role":"tool",
                "tool_call_id": tool_id,
                "content": ""
            }
            try:
                tool_parameters = json.loads(tool_call.function.arguments)
                print("Tool parameters: ", tool_parameters)
                if tool_name == "get_info_tool":
                    tools_list = tool_parameters.get("tools")
                    to_use = tool_parameters.get("to_use", True)
                    
                    if tools_list:
                        tools_info = commandsDB.get_tools_info(tools_list)
                        if to_use:
                            tools_to_call = tools_info
                            tool_response_object["content"] = "Comandos obtenidos correctamente"
                        else:
                            tool_response_object["content"] = ",".join([tool["name"] + " - " + tool["description"] for tool in tools_info]) 
                    else:
                        tool_response_object["content"] = "No se especificaron herramientas"
                elif commandsDB.exists(tool_name):
                    commandClass: Command = commandsDB.getCommandClass(tool_name)
                    commandClass = commandClass()
                    tool_response = commandClass.execute(**tool_parameters)
                    if tool_response == None:
                        tool_response = "Comando ejecutado correctamente pero no devolvio respuesta"
                else:
                    tool_response_object["content"] = f"Tool {tool_name} no encontrado en DB"
            except Exception as e:
                full_message = f"Error al ejecutar la herramienta {tool_name}: {e}"
                tool_response = full_message[-100:]
                print(full_message)
                tool_response_object["content"] = tool_response
            tryes += 1
            responses.append(tool_response_object)
    fun_update_status(preview="Fin del while\n...")
    print("End of tools calls")
    return responses, tools_to_call