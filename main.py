from src.Levus import Levus
from src.gui import startGui
levus = Levus()
levus._debug = True
levus.start()

startGui(levus.voiceRecognitionToggle, levus.imageRecognitionToggle, levus.stopAll)