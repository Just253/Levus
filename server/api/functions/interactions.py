from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from typing import List
from flask import current_app as app
from ..functions.db import statusTable
from ...commandHandler import dbCommands
from commands.command import Command
default_tool = [{
    "type": "function",
    "function": {
        "name": "get_info_tool",
        "description": "Obtiene informacion de otro tool/function/comando",
        "parameters": {
            "type": "object",
            "properties": {
                "tool": {
                    "type": "string",
                    "description": "Nombre del tool"
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
    system_message = list(filter(lambda x: x['role'] == 'system', messages))[0]
    non_system_messages = list(filter(lambda x: x['role'] != 'system', messages))
    last_10_non_system_messages = non_system_messages[-9:]
    messages = [system_message] + last_10_non_system_messages
    try:
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
        tools_calls = response.choices[0].message.tools_calls
        if tools_calls:
            # TODO: Implement tool calls
            pass
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
        messages=tools,
        temperature=0.2,
        tools=default_tool
    )
    calls = 0
    responses = []
    while MAX_CALLS > calls:
        tools_calls: List[ChatCompletionMessageToolCall] = response.choices[0].message.tools_calls
        if tools_calls:
            for tool_call in tools_calls:
                tool_id = tool_call.id
                tool_name = tool_call.function.name
                tool_parameters = eval(tool_call.function.arguments)
                tool_response_object = {
                    "role":"tool",
                    "tool_call_id": tool_id,
                    "name": tool_name,
                    "content": ""
                }
                if commands.exists(tool_name):
                    commandClass: Command = commands.getCommandClass(tool_name)
                    commandClass = commandClass()
                    try:
                        tool_response = commandClass.execute(tool_parameters)
                        if tool_response == None:
                            tool_response = "Comando ejecutado correctamente pero no devolvio respuesta"
                    except Exception as e:
                        full_message = f"Error al ejecutar la herramienta {tool_name}: {e}"
                        tool_response = full_message[-100:]
                        print(f"Error al ejecutar la herramienta {tool_name}: {e}")
                    tool_response_object["content"] = tool_response
                    calls += 1
                else:
                    tool_response_object["content"] = f"Tool {tool_name} no encontrado en DB"
                responses.append(tool_response_object)
    return None if not responses else responses