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
    BOT = None 
    def __init__(self, BOT):
        self.BOT = BOT
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
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

    async def start(self, options=None):
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


                if self.BOT.get_bot_name() not in text:  # Revisa si menciona el nombre del bot
                  continue
                botName = self.BOT.get_bot_name()
                # Cortar desde que menciona su nombre 
                text = text[text.index(botName) + len(botName):]
                
                command = self.BOT.check_commands(text)
                print(command)
                if command == False:
                    await self.BOT.askIA(text)
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