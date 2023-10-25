import json
import asyncio
from getCookiesBingChat import getCookiesBingChat
from re_edge_gpt import Chatbot
from re_edge_gpt import ConversationStyle

async def test_ask(txt) -> None:
   # TODO: solo ejecutar GetCookiesBingChat cuando los cookies guardados en un json ya no sirven

   cookies = getCookiesBingChat()
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
   loop.run_until_complete(test_ask())