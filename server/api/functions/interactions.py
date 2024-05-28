from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from flask import current_app as app

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def get_response_from_openai(messages, tools=None, tool_choice=None, model="gpt-3.5-turbo"):
    client = OpenAI(api_key=app.config["OPENAI_API_KEY"])
    system_message = list(filter(lambda x: x['role'] == 'system', messages))[0]
    non_system_messages = list(filter(lambda x: x['role'] != 'system', messages))
    last_10_non_system_messages = non_system_messages[-9:]
    messages = [system_message] + last_10_non_system_messages
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return str(e)