from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from typing import List
from flask import current_app as app
from ..functions.db import statusTable
from ..functions.commandHandler import dbCommands
from ..commands.command import Command
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
                    "type": "array",
                    "description": "Nombre/s del/os tool/s",
                    "items": {
                        "type": "string"
                    }
                },
                "only_desc":{
                    "type": "boolean",
                    "description": "True: Solo descripcion, False: se añade al tools de OpenAI",
                }
            },
            "required": ["tool"]
        }
    }
}]

MAX_CALLS = 5

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
        messages = get_responses(client, messages, model, commands, tools)
        print(messages)
        last_content = messages[-1]["content"]
        update_status(status="completed", response=last_content, preview="")
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        print(f"Error: {error_type} - {error_message}")
        
        update_status(status="error", error=f"{error_type}: {error_message}")
        print(f"Unable to generate ChatCompletion response due to {error_type}")
        return str(e)

def get_responses(client: OpenAI, messages,model,commandsDB: dbCommands, tools=default_tool) -> list[dict]:
    try:
        body_response = {
            "role": "assistant",
            "content": None,
        }
        tool_calls: List[ChatCompletionMessageToolCall] = []
        tools_responses = []

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
      body_response["content"] = text[:100]
      return [body_response]

    try:
      streaming_content = ""
      body_response["content"] = streaming_content
      for chunk in response:
          msg = chunk.choices[0]
          if hasattr(msg, "delta") and msg.delta:
              delta = msg.delta
              if hasattr(delta, "finish_reason"):
                  finish_reason = delta.finish_reason
                  if finish_reason is not None:
                    if finish_reason == "tool_calls":
                        tool_calls += delta.tool_calls
                    break
              if hasattr(delta, "content"):
                  content = delta.content
                  if content:
                      streaming_content += content        
    except Exception as e:
        text = f"Error chunks: {e}"
        print(text)
        body_response["content"] = text[:100]
        return [body_response]
    new_messages = [body_response]
    try:
        tool_calls = tool_calls[:MAX_CALLS]
        if tool_calls:
            body_response["tool_calls"] = [{"id": t.id, "function": {"name": t.function.name, "arguments": t.function.arguments}, "type": "function"} for t in tool_calls]

            for tool in tool_calls:
                tool_body_response = {
                    "role": "tool",
                    "content": None,
                    "tool_call_id": tool.id,
                }
                tool_name = tool.function.name
                try:
                    tool_parameters = json.loads(tool.function.arguments)
                except Exception as e:
                    tool_body_response["content"] = f"Error al obtener parametros de la herramienta {tool_name}: {e}"
                    tools_responses.append(tool_body_response)
                    continue
                try:
                    if tool_name == "get_info_tool":
                        tools_list = tool_parameters.get("tools")
                        only_desc = tool_parameters.get("only_desc", True)
                        if tools_list:
                            tools_info = commandsDB.get_tools_info(tools_list)
                            if only_desc:
                                tool_body_response["content"] = ",".join([tool["name"] + " - " + tool["description"] for tool in tools_info]) 
                            else:
                                tools = default_tool + tools_info
                                tool_body_response["content"] = "Comandos obtenidos correctamente"         
                        else:
                            tool_body_response["content"] = "No se especificaron herramientas"
                    else:
                        if commandsDB.exists(tool_name):
                            commandClass: Command = commandsDB.getCommandClass(tool_name)
                            commandClass = commandClass()
                            tool_response = commandClass.execute(**tool_parameters)
                            if tool_response == None:
                                tool_response = "Comando ejecutado correctamente pero no devolvio respuesta"
                        else:
                            tool_body_response["content"] = f"Tool {tool_name} no encontrado en DB"
                except Exception as e:
                    full_message = f"Error al ejecutar la herramienta {tool_name}: {e}"
                    tool_response = full_message[-100:]
                    print(full_message)
                    tool_body_response["content"] = tool_response
                new_messages.append(tool_body_response)
    except Exception as e:
        text = f"Error al ejecutar comandos: {e}"
        print(text)
        body_response["content"] = text[:100]
    try:
        final_response = get_responses(client, messages + new_messages, model, commandsDB, tools)
    except Exception as e:
        text = f"Error al realizar llamadas recursivas: {e}"
        print(text)
        body_response["content"] = text[:100]    

    return new_messages + final_response