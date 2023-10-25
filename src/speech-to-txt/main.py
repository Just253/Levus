from annyangV2 import Annyang
from eventCommandHandler import CommandHandler
from watchdog.observers import Observer
import os
global annyang

annyang = Annyang()
annyang._debug = True
# obtener la ruta de este archivo main.py con os
actual_dir = os.path.abspath(__file__)
comando_dir = os.path.join(os.path.dirname(actual_dir), "commands")


observer = Observer()
handler = CommandHandler(annyang, comando_dir)
observer.schedule(handler, path=comando_dir, recursive=True)
observer.start()

annyang.start()
annyang.add_callback('end', observer.stop())