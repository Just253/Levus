# From original Code snippet
# //! annyang
# //! version : 2.6.1
# //! author  : Tal Ater @TalAter
# //! license : MIT
# //! https://www.TalAter.com/annyang/
# Mi codigo pero pasado a python

import speech_recognition as sr


def getNameBot():
  return 'levus'

class Annyang:
    
    def getName(self):
        return getNameBot()
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.commands = []
        self.is_listening = False
        self.is_paused = False
        self.auto_restart = False
        self.continuous = False
        self.language = 'es-PE'
        self.debug = False
        
        self.botCommandActive = False
        
        

        self.recognizer.pause_threshold = 0.5
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

    def add_commands(self, commands):
        for phrase, callback in commands.items():
            self.commands.append((phrase, callback))
    
    def start(self, options=None):
        if not options:
            options = {}

        self.is_paused = options.get('paused', False)
        self.auto_restart = options.get('auto_restart', False)
        self.continuous = options.get('continuous', False)

        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 4000

        self.is_listening = True
        while self.is_listening:
            if self.is_paused:
                continue

            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio, language=self.language)
                
                if self.debug:
                    print(f'Speech recognized: {text}')

                for phrase, callback in self.commands:
                    if phrase.lower() in text.lower():
                        if self.debug:
                            print(f'Command matched: {phrase}')
                        try:
                            callback(text)
                        except Exception as e:
                            if self.debug:
                                print(f'Error executing {phrase}: {e}')

            except sr.UnknownValueError:
                if self.debug:
                    print('Speech not recognized')
            except sr.RequestError as e:
                if self.debug:
                    print(f'Error: {e}')
            
            if not self.is_listening:
                break

        if self.auto_restart:
            self.start(options)

    def abort(self):
        self.is_listening = False

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def set_language(self, language):
        self.language = language

    def remove_commands(self, commands):
        if isinstance(commands, str):
            commands = [commands]

        self.commands = [(phrase, callback) for phrase, callback in self.commands if phrase not in commands]

    def add_callback(self, event, callback, context=None):
        self.recognizer.pause_threshold = 0.5
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

        if event == 'start':
            self.recognizer.on_start = lambda: callback(context)
        elif event == 'end':
            self.recognizer.on_end = lambda: callback(context)
        elif event == 'error':
            self.recognizer.on_error = lambda error: callback(error, context)
        elif event == 'result':
            self.recognizer.on_result = lambda result: callback(result, context)

    def remove_callback(self, event, callback=None):
        self.recognizer.pause_threshold = 0.5
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

        if event == 'start':
            self.recognizer.on_start = None
        elif event == 'end':
            self.recognizer.on_end = None
        elif event == 'error':
            self.recognizer.on_error = None
        elif event == 'result':
            self.recognizer.on_result = None