import os
import json
import asyncio
from getCookiesBingChat import getCookiesBingChat
from re_edge_gpt import Chatbot
from re_edge_gpt import ConversationStyle

COOKIES_FILE = 'cookies.json'

def save_cookies(cookies):
    with open(COOKIES_FILE, 'w') as f:
        json.dump(cookies, f)

def load_cookies():
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, 'r') as f:
            return json.load(f)
    return None

async def test_ask(txt) -> None:
    cookies = load_cookies()
    if cookies is None:
        print('solicitando cookies...')
        cookies = getCookiesBingChat()
        save_cookies(cookies)
    bot = await Chatbot.create(cookies=cookies)
    response = await bot.ask(
        prompt=txt,
        conversation_style=ConversationStyle.balanced,
        simplify_response=True,
    )
    await bot.close()
    print(json.dumps(response, indent=2))
    assert response

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()
    while True:
        prompt = input(">> ")
        loop.run_until_complete(test_ask(prompt))