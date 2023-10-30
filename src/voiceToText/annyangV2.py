# From original Code snippet
# //! annyang
# //! version : 2.6.1
# //! author  : Tal Ater @TalAter
# //! license : MIT
# //! https://www.TalAter.com/annyang/
# Mi codigo pero pasado a python

import speech_recognition as sr

class Annyang:
    _bot_name = "avestruz"
    def __init__(self):
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
        self._commands = []
        self._is_listening = False
        self._is_paused = False
        self._auto_restart = False
        self._continuous = False
        self._language = 'es-PE'
        self._debug = False
        self._bot_active = False

        self._recognizer.pause_threshold = 0.5
        self._recognizer.phrase_threshold = 0.3
        self._recognizer.non_speaking_duration = 0.5

    def add_commands(self, commands):
        if self._debug: print("[DEBUG] add_commands - NEW COMMANDS - " + str(commands))
        for phrase, callback in commands.items():
            self._commands.append((phrase, callback))

    def start(self, options=None):
        if not options:
            options = {}

        self._is_paused = options.get('paused', False)
        self._auto_restart = options.get('auto_restart', False)
        self._continuous = options.get('continuous', False)

        self._recognizer.dynamic_energy_threshold = False
        self._recognizer.energy_threshold = 4000

        self._is_listening = True
        while self._is_listening:
            if self._is_paused:
                continue

            with self._microphone as source:
                self._recognizer.adjust_for_ambient_noise(source)
                audio = self._recognizer.listen(source)

            try:
                
                text = self._recognizer.recognize_google(audio, language=self._language)
                text = text.lower()
                if self._debug:
                    print(f'Speech recognized: {text}')


                if self.get_bot_name() not in text:  # Revisa si menciona el nombre del bot
                  continue
                botName = self.get_bot_name()
                # Cortar desde que menciona su nombre 
                text = text[text.index(botName) + len(botName):]
                self._bot_active = True
                # 'cambiar nombre asdasdasd'
                # phrase = 'cambiar nombre'
                # text = 'cambiar nombre asdasdasd'
                # cleanText = 'asdasdasd'
                for phrase, callback in self._commands:
                    if phrase.lower() in text.lower():
                        if self._debug:
                            print(f'Command matched: {phrase}')
                        text = text[text.index(phrase) + len(phrase):]
                        try:
                            command = callback(self)
                            command.execute(text)
                        except Exception as e:
                            if self._debug:
                                print(f'Error executing {phrase}: {e}')
                        break

            except sr.UnknownValueError:
                if self._debug:
                    print('Speech not recognized')
            except sr.RequestError as e:
                if self._debug:
                    print(f'Error: {e}')

            if not self._is_listening:
                break

        if self._auto_restart and self._continuous:
            self.start(options)

    def abort(self):
        self._is_listening = False

    def pause(self):
        self._is_paused = True

    def resume(self):
        self._is_paused = False

    def set_language(self, language):
        self._language = language

    def remove_commands(self, commands):
        if isinstance(commands, str):
            commands = [commands]
        
        if self._debug: print("[DEBUG] remove_commands - OLD COMMANDS - " + str(self._commands))
        self._commands = [(phrase, callback) for phrase, callback in self._commands if phrase not in commands]

    def add_callback(self, event, callback, context=None):
        self._recognizer.pause_threshold = 0.5
        self._recognizer.phrase_threshold = 0.3
        self._recognizer.non_speaking_duration = 0.5

        if event == 'start':
            self._recognizer.on_start = lambda: callback(context)
        elif event == 'end':
            self._recognizer.on_end = lambda: callback(context)
        elif event == 'error':
            self._recognizer.on_error = lambda error: callback(error, context)
        elif event == 'result':
            self._recognizer.on_result = lambda result: callback(result, context)

    def remove_callback(self, event, callback=None):
        self._recognizer.pause_threshold = 0.5
        self._recognizer.phrase_threshold = 0.3
        self._recognizer.non_speaking_duration = 0.5

        if event == 'start':
            self._recognizer.on_start = None
        elif event == 'end':
            self._recognizer.on_end = None
        elif event == 'error':
            self._recognizer.on_error = None
        elif event == 'result':
            self._recognizer.on_result = None

    def get_bot_name(self):
        return self._bot_name

    def set_bot_name(self, name):
        self._bot_name = name

    #bot_name = property(get_bot_name, set_bot_name)