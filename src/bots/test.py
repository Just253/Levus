from gtp4free import Botia
import asyncio
async def main():
  botManager = Botia()
  while True:
    txt = input(">> ")
    await botManager.newCommand(txt)


if __name__ == "__main__":
  asyncio.run(main())