import OS
from Command Close_window.py import Close_window

class Bot_Close_window(Close_window):
    def __init__(self):
        super().__init__()

    def execute(self):
    os.system("taskkill /f /im notepad.exe")
    pass
    
    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getRequeriments(self):
        return self.requeriments

    def getKeywords(self):
        return self.keywords

    def setName(self, name):
        self.name = newname

    def setDescription(self, description):
        self.description = new_description

    def setRequeriments(self, requeriments):
        self.requeriments = new_requeriments

    def setKeywords(self, keywords):
        self.keywords = new_keywords

