import asyncio
from src.Levus import Levus

levus = Levus()
levus._debug = True
asyncio.run(levus.start())