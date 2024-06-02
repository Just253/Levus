from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from flask import current_app as app
from ..functions.db import statusTable
from ...commandHandler import dbCommands
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
    client = OpenAI(api_key=app.config["OPENAI_API_KEY"])
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