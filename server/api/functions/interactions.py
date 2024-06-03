from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from typing import List
from flask import current_app as app
from ..functions.db import statusTable
from ...commandHandler import dbCommands
from commands.command import Command
import json
default_tool = [{
    "type": "function",
    "function": {
        "name": "get_info_tool",
        "description": "Obtiene informacion de otro tool/function/comando solo o en conjunto",
        "parameters": {
            "type": "object",
            "properties": {
                "tools": {
                    "type": "list",
                    "description": "Nombre/s del/os tool/s"
                }
            },
            "required": ["tool"]
        }
    }
}]

MAX_CALLS = 10

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def get_response_from_openai(messages, process_id, table: statusTable =None, tools=None, tool_choice=None, model="gpt-3.5-turbo"):
    client: OpenAI = OpenAI(api_key=app.config["OPENAI_API_KEY"])
    default_tool_name = default_tool[0]["function"]["name"]
    
    system_message = list(filter(lambda x: x['role'] == 'system', messages))[0]
    system_message["content"][0]["text"] += f" Llama a herramienta {default_tool_name} solo si es necesario"
    non_system_messages = list(filter(lambda x: x['role'] != 'system', messages))
    last_10_non_system_messages = non_system_messages[-9:]
    
    messages = [system_message] + last_10_non_system_messages
    try:
        check_if_call_tool, tools_called = send_message_tools_to_openai(client, messages, tools, tool_choice, process_id, app, table)
        if check_if_call_tool:
            messages = messages + check_if_call_tool
            responses_tools = send_message_tools_to_openai(client, messages, tools_called, tool_choice, process_id, app, table)
            if responses_tools:
                messages = messages + responses_tools


        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
            stream=True,
            tools=default_tool
        )
        chunk_messages = ""
        for chunk in response:
            message = chunk.choices[0].delta.content
            if message != None:
                chunk_messages += message
                if table:
                    table.update_status(process_id=process_id, preview=chunk_messages)
        if table:
            table.update_status(process_id=process_id, status="completed", response=chunk_messages, preview="")
    except Exception as e:
        if table:
            table.update_status(process_id=process_id, status="error", error=str(e))
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return str(e)
    
def send_message_tools_to_openai (client: OpenAI, messages,tools, tool_choice, process_id,app, table: statusTable = None):
    commands = dbCommands(app)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3,
        tools=default_tool if not tools else tools,
    )
    calls = 0
    responses = []
    tools_to_call = []
    while MAX_CALLS > calls:
        tools_calls: List[ChatCompletionMessageToolCall] = response.choices[0].message.tools_calls
        if tools_calls:
            for tool_call in tools_calls:
                tool_id = tool_call.id
                tool_name = tool_call.function.name
                tool_response_object = {
                    "role":"tool",
                    "tool_call_id": tool_id,
                    "name": tool_name,
                    "content": ""
                }
                try:
                    tool_parameters = json.loads(tool_call.function.arguments)
                    if tool_name == "get_info_tool":
                        tools = tool_parameters.get("tools")
                        if tools:
                            tools_to_call = commands.get_tools_info(tools)
                            tool_response_object["content"] = "Comandos obtenidos correctamente"
                        else:
                            tool_response_object["content"] = "No se especificaron herramientas"
                    elif commands.exists(tool_name):
                        commandClass: Command = commands.getCommandClass(tool_name)
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
                    calls += 1
                responses.append(tool_response_object)
            break
    return responses, tools_to_call