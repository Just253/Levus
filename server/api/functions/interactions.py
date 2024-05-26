from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI

client = OpenAI("your_api_key")

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def get_response_from_openai(messages, tools=None, tool_choice=None, model="gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response.choices[0].message['content']
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return str(e)